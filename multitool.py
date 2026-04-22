from pydantic_ai import Agent, ModelRequestContext, ModelResponse
from pydantic_ai.capabilities import Hooks, AbstractCapability
from pydantic import BaseModel
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

import datetime

def get_current_year() -> int:
    return datetime.date.today().year

def get_years_since(year: int) -> int:
    return datetime.date.today().year - year

agent = Agent(
    model="anthropic:claude-haiku-4-5-20251001",
    system_prompt="You are an assistant.",
    tools=[get_current_year, get_years_since]
)

result = agent.run_sync('How many years ago was the University of Toronto founded?')
print(result.output)

