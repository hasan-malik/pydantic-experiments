from pydantic_ai import Agent

from grafico.deps import GraficoDeps
from grafico.store import MoleculeStore
from grafico.tools import lookup_molecule, get_molecule_info

agent = Agent(
    model='anthropic:claude-haiku-4-5-20251001',
    system_prompt="You are a chemistry assistant. Look up a given molecule and report back what you find.",
    deps_type=GraficoDeps,
    tools=[lookup_molecule, get_molecule_info]
)

