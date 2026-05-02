from grafico.store import MoleculeStore
from grafico.atoms import ConceptualAtoms
import selfies as sf

store = MoleculeStore()

caf = ConceptualAtoms(iri="huh", name="caffeine", selfies=sf.encoder('CN1C=NC2=C1C(=O)N(C(=O)N2C)C'), molecular_formula="bro", molecular_weight=2)
store.save(caf)
print(store.get("huh"))
print(store.get("haha"))


