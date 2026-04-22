from pydantic_ai import Agent, ModelRequestContext, ModelResponse
from pydantic_ai.capabilities import Hooks
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

hooks = Hooks()


class UniversityData(BaseModel):
    name: str
    country: str
    city: str

@hooks.on.before_model_request
async def monitor_request(ctx, request_context: ModelRequestContext) -> ModelRequestContext: 
    # didn't use the ctx argument here
    # request_context contains info/context on the request i.e. prompt we sent to the LLM
    print(f"Sending {len(request_context.messages)} messages to the model {request_context.model}")
    return request_context
    # we return request_context, possibly modified

@hooks.on.after_model_request
async def print_model(ctx, request_context: ModelRequestContext, response: ModelResponse) -> ModelResponse: 
    print(f"The model {request_context.model} successfully answered at the time: {response.timestamp}")
    return response


agent = Agent(
    model="anthropic:claude-haiku-4-5-20251001",
    system_prompt="You are an assistant.",
    capabilities=[hooks]
)

result = agent.run_sync("University of Guelph", output_type=UniversityData)
print(result.output)
