import pubchempy as pcp

from grafico.atoms import ConceptualAtoms
from grafico.deps import GraficoDeps
from grafico.store import MoleculeStore
import selfies as sf

from pydantic_ai import RunContext

def lookup_molecule(runContext: RunContext[GraficoDeps], name: str) -> str:
    """
    Lookup a molecule via Pubchempy by <name>. 
    If found, store the molecule in <store>. Return the iri.
    If not found, raise a ValueError.
    """

    store = runContext.deps.store

    results = pcp.get_compounds(name, "name")
    # get the compound by searching for arg1 by arg2
    # e.g. get_compounds("caffeine", "name")  

    if results == []:  # if not found
        raise ValueError(f"Molecule '{name}' not found in PubChem")

    atoms = ConceptualAtoms(iri=generate_iri(name), name=name, selfies=sf.encoder(results[0].smiles), molecular_formula=results[0].molecular_formula, molecular_weight=results[0].molecular_weight)
    store.save(atoms)

    return atoms.iri

def get_molecule_info(runContext: RunContext[GraficoDeps], iri: str):
    store = runContext.deps.store
    atoms = store.get(iri)
    if not atoms:
        raise ValueError(f"iri not found: {iri}")
    return f"Name: {atoms.name}, Formula: {atoms.molecular_formula}, Weight: {atoms.molecular_weight}, SELFIES: {atoms.selfies}"

def generate_iri(name: str):
    return f"mol:{name.lower().replace(' ', '_')}"


# below is an old version of lookup_molecule. This was written before I realized that this tool will be 
# unable to access the MoleculeStore dependency!
# the workaround: use RunContext so the tool can access the MoleculeStore dependency.

# def lookup_molecule(name: str, store: MoleculeStore) -> str:
#     """
#     Lookup a molecule via Pubchempy by <name>. 
#     If found, store the molecule in <store>. Return the iri.
#     If not found, raise a ValueError.
#     """

#     results = pcp.get_compounds(name, "name")
#     # get the compound by searching for arg1 by arg2
#     # e.g. get_compounds("caffeine", "name")  

#     if results == []:  # if not found
#         raise ValueError(f"Molecule '{name}' not found in PubChem")

#     atoms = ConceptualAtoms(iri=generate_iri(name), name=name, selfies=sf.encoder(results[0].smiles), molecular_formula=results[0].molecular_formula, molecular_weight=results[0].molecular_weight)
#     store.save(atoms)

#     return atoms.iri
