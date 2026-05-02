from dotenv import load_dotenv
load_dotenv()
from grafico.agent import agent
from grafico.deps import GraficoDeps
from grafico.store import MoleculeStore

store = MoleculeStore()

result = agent.run_sync(
    user_prompt="Look up ethanol.",
    deps=GraficoDeps(store=store)
)

print(result.output)
print(result.all_messages())