from pydantic_ai import Agent
from pydantic import BaseModel
import datetime

from dotenv import load_dotenv
load_dotenv()

class CountryData(BaseModel):
    name: str
    capital: str
    population: int

def get_todays_date():
    """Return today's date as a YYYY-MM-DD string."""
    return datetime.date.today().isoformat()

agent = Agent(
    model='anthropic:claude-haiku-4-5-20251001',
    system_prompt="You are an assistant. Answer concisely.", # system prompt: sent with every user prompt
    tools=[get_todays_date]
)

print("Welcome!")

result = agent.run_sync(
    user_prompt="Liechtenstein",
    output_type=CountryData
)

print(result.output)

result = agent.run_sync(
    user_prompt="How many days till April 23?",
)

print(result.output)
