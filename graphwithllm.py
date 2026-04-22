from __future__ import annotations
from pydantic_ai import Agent, ModelRequestContext, ModelResponse
from pydantic_ai.capabilities import Hooks, AbstractCapability
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()



from dataclasses import dataclass
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

@dataclass
class Classify(BaseNode):
    sentence: str

    async def run(self, ctx: GraphRunContext) -> BaseNode:
        temp = await agent.run(self.sentence)  # not run_sync because it's in an async function
        if isinstance(temp.output, Positive):
            return HandlePositive()
        return HandleNegative()

@dataclass
class HandlePositive(BaseNode):

    async def run(self, ctx: GraphRunContext) -> BaseNode:
        return End(Positive().message)

@dataclass
class HandleNegative(BaseNode):

    async def run(self, ctx: GraphRunContext) -> BaseNode:
        return End(Negative().message)

class Positive(BaseModel):  # they need to be BaseModel otherwise Pydantic can't understand
    
    message: str = "Awesome!"

class Negative(BaseModel):
    
    message: str = "Sorry to hear that."

agent = Agent(
    model="anthropic:claude-haiku-4-5-20251001",
    system_prompt="You are an assistant.",
    output_type= Positive | Negative
)

graph = Graph(nodes=[Classify, HandlePositive, HandleNegative])
result = graph.run_sync(Classify("I'm feeling great!"))
# result = graph.run_sync(Classify("I'm not feeling great!"))
print(result.output)

