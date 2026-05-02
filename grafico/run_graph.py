from dotenv import load_dotenv

from grafico.store import MoleculeStore
load_dotenv()
from grafico.deps import GraficoDeps
from grafico.graph import LookupNode, MoleculeState, graph



state = MoleculeState(molecule_name="Caffeine")

store = MoleculeStore()
deps = GraficoDeps(store=store)

result = graph.run_sync(LookupNode(), state=state, deps=deps)
print(result.output)
