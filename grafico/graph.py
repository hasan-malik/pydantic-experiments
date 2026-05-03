from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal
from pydantic import BaseModel
from pydantic_graph import BaseNode, End, GraphRunContext, Graph
from grafico.atoms import ConceptualAtoms
from grafico.deps import GraficoDeps

import pubchempy as pcp
import selfies as sf

from grafico.tools import generate_iri
from grafico.agent import agent



@dataclass
class MoleculesState():
    query: str  # user query input
    molecule_names: list[str] = field(default_factory=list)
    IRIs: list[str] = field(default_factory=list) 
    molecule_infos: list[str] = field(default_factory=list)

    # the last three attrs are lists.
    # for most nodes e.g. AnalyzeNode we only care about the 0th element.
    # for CompareNode we care about the 0th and 1st elements.
    # this architecture is scalabale: with lists, you can have nodes that operate on as many elements as you need.

    # we use field() rather than = [] to prevent aliasing


@dataclass
class LookupNode(BaseNode[MoleculesState, GraficoDeps]):  # remember, the GraficoDeps contains the store

    async def run(self, graphRunContext: GraphRunContext[MoleculesState, GraficoDeps]) -> AnalyzeNode:

        name = graphRunContext.state.molecule_names[0]
        store = graphRunContext.deps.store

        results = pcp.get_compounds(name, "name")
        # get the compound by searching for arg1 by arg2
        # e.g. get_compounds("caffeine", "name")  

        if results == []:  # if not found
            raise ValueError(f"Molecule '{name}' not found in PubChem")

        atoms = ConceptualAtoms(iri=generate_iri(name), name=name, selfies=sf.encoder(results[0].smiles), molecular_formula=results[0].molecular_formula, molecular_weight=results[0].molecular_weight)
        store.save(atoms)

        graphRunContext.state.IRIs.append(atoms.iri)
        return AnalyzeNode()
    
@dataclass
class AnalyzeNode(BaseNode[MoleculesState, GraficoDeps]):

    async def run(self, graphRunContext: GraphRunContext[MoleculesState, GraficoDeps]) -> RespondNode:

        store = graphRunContext.deps.store
        iri = graphRunContext.state.IRIs[0]

        atoms = store.get(iri)
        if not atoms:
            raise ValueError(f"iri not found: {iri}")
        graphRunContext.state.molecule_infos.append(f"Name: {atoms.name}, Formula: {atoms.molecular_formula}, Weight: {atoms.molecular_weight}, SELFIES: {atoms.selfies}")

        return RespondNode()
    
@dataclass
class CompareNode(BaseNode[MoleculesState, GraficoDeps]):

    async def run(self, graphRunContext: GraphRunContext[MoleculesState, GraficoDeps]) -> RespondNode:
        pass
    
@dataclass
class RouterNode(BaseNode[MoleculesState, GraficoDeps]):

    async def run(self, graphRunContext: GraphRunContext[MoleculesState, GraficoDeps]) -> LookupNode | CompareNode | RespondNode:
        
        result = await agent.run(
            user_prompt=graphRunContext.state.query,
            output_type=OutputModel
        )

        graphRunContext.state.molecule_names = (result.output.molecule_names)

        task_type = result.output.task_type

        if task_type == "analyze":
            return LookupNode()
        elif task_type == "compare":
            return CompareNode()
    
@dataclass
class RespondNode(BaseNode[MoleculesState, GraficoDeps]):

    async def run(self, graphRunContext: GraphRunContext[MoleculesState, GraficoDeps]) -> End:
        return End(graphRunContext.state.molecule_infos[0])
    

graph = Graph(nodes=[RouterNode, LookupNode, AnalyzeNode, CompareNode, RespondNode])

class OutputModel(BaseModel):
    query: str
    molecule_names: list[str]
    task_type: Literal["analyze", "compare"]



