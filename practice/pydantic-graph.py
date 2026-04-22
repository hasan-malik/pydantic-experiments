from __future__ import annotations
# from pydantic_ai import Agent, ModelRequestContext, ModelResponse,
# from pydantic_ai.capabilities import Hooks, AbstractCapability
# from pydantic import BaseModel
# from dotenv import load_dotenv
# load_dotenv()

# agent = Agent(
#     model="anthropic:claude-haiku-4-5-20251001",
#     system_prompt="You are an assistant."
# )

from dataclasses import dataclass
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

@dataclass
class CheckDivisibility(BaseNode):
    num: int

    async def run(self, ctx: GraphRunContext) -> Increment | End[int]:
        if not (self.num % 5):
            return End(self.num)
        return Increment(num=self.num)

@dataclass
class Increment(BaseNode):
    num: int

    async def run(self, ctx: GraphRunContext) -> CheckDivisibility:
        return CheckDivisibility(num=(self.num+1))


value=6
graph = Graph(nodes=[CheckDivisibility, Increment])
result = graph.run_sync(CheckDivisibility(num=value))

print(result.output)

