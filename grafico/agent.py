from pydantic_ai import Agent

from grafico.deps import GraficoDeps

agent = Agent(
    model='anthropic:claude-haiku-4-5-20251001',
    system_prompt="You are a chemistry assistant. Extract molecule names from the user's query and use the correct graph-nodes to operate on those molecules and discover information.",
    deps_type=GraficoDeps
)


