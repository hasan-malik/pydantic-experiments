from __future__ import annotations
from dataclasses import dataclass
from pydantic_graph import BaseNode, End, GraphRunContext, Graph
from grafico.atoms import ConceptualAtoms
from grafico.deps import GraficoDeps

import pubchempy as pcp
import selfies as sf

from grafico.tools import generate_iri




@dataclass
class MoleculeState():
    molecule_name: str
    iri: str | None =  None
    molecule_info: str | None = None

@dataclass
class LookupNode(BaseNode[MoleculeState, GraficoDeps]):  # remember, the GraficoDeps contains the store

    async def run(self, graphRunContext: GraphRunContext[MoleculeState, GraficoDeps]) -> AnalyzeNode:

        name = graphRunContext.state.molecule_name
        store = graphRunContext.deps.store

        results = pcp.get_compounds(name, "name")
        # get the compound by searching for arg1 by arg2
        # e.g. get_compounds("caffeine", "name")  

        if results == []:  # if not found
            raise ValueError(f"Molecule '{name}' not found in PubChem")

        atoms = ConceptualAtoms(iri=generate_iri(name), name=name, selfies=sf.encoder(results[0].smiles), molecular_formula=results[0].molecular_formula, molecular_weight=results[0].molecular_weight)
        store.save(atoms)

        graphRunContext.state.iri =  atoms.iri
        return AnalyzeNode()
    
@dataclass
class AnalyzeNode(BaseNode[MoleculeState, GraficoDeps]):

    async def run(self, graphRunContext: GraphRunContext[MoleculeState, GraficoDeps]) -> RespondNode:

        store = graphRunContext.deps.store
        iri = graphRunContext.state.iri

        atoms = store.get(iri)
        if not atoms:
            raise ValueError(f"iri not found: {iri}")
        graphRunContext.state.molecule_info = f"Name: {atoms.name}, Formula: {atoms.molecular_formula}, Weight: {atoms.molecular_weight}, SELFIES: {atoms.selfies}"

        return RespondNode()
    
@dataclass
class RespondNode(BaseNode[MoleculeState, GraficoDeps]):

    async def run(self, graphRunContext: GraphRunContext[MoleculeState, GraficoDeps]) -> End:
        return End(graphRunContext.state.molecule_info)
    

graph = Graph(nodes=[LookupNode, AnalyzeNode, RespondNode])


