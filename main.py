from pydantic_ai import Agent
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class CountryData(BaseModel):
    name: str
    capital: str
    population: int

agent = Agent(
    model='anthropic:claude-haiku-4-5-20251001',
    system_prompt="You are an assistant. Answer concisely." # system prompt: sent with every user prompt
)

result = agent.run_sync(
    user_prompt="Liechtenstein",
    output_type=CountryData
)

print(result.output)
