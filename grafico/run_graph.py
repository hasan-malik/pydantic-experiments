from dotenv import load_dotenv

from grafico.store import MoleculeStore
load_dotenv()
from grafico.deps import GraficoDeps
from grafico.graph import LookupNode, MoleculesState, RouterNode, graph



state = MoleculesState(query="tell about this molecule: caffeine")

store = MoleculeStore()
deps = GraficoDeps(store=store)

result = graph.run_sync(RouterNode(), state=state, deps=deps)
print(result.output)
