
from grafico.store import MoleculeStore
from grafico.tools import lookup_molecule, generate_iri

store = MoleculeStore()

print(lookup_molecule("caffeine", store))  # save caffeine in the store
print(store.get(generate_iri("caffeine")))