from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
import datetime

from dotenv import load_dotenv
load_dotenv()

class CountryData(BaseModel):
    name: str
    capital: str
    population: int

def get_todays_date() -> str:
    """Return today's date as a YYYY-MM-DD string."""
    return datetime.date.today().isoformat()

agent = Agent(
    model='anthropic:claude-haiku-4-5-20251001',
    system_prompt="You are an assistant. Answer concisely.", # system prompt: sent with every user prompt
    tools=[get_todays_date],
    deps_type=str
)

@agent.system_prompt  
def append_to_system_prompt(ctx: RunContext[str]) -> str:
    """The string returned by this function will be appended to the system prompt."""
    return f"The user's name is {ctx.deps}. Address them by their name."


print("Welcome!")

result = agent.run_sync(
    user_prompt="Liechtenstein",
    output_type=CountryData
)

print(result.output)

result = agent.run_sync(
    user_prompt="How many days till April 23?",
    deps="Malik"
)

print(result.output)



# Step	What you build	Concept learned
# 1	Ask a question, get a plain text answer	   Basic Agent + API key
# 2	Ask a question, get a structured Python object back	      Pydantic models + typed output
# 3	Add a tool that the agent can call (e.g. get today's date, or fetch a URL)	    Tools
# 4	Pass a dependency (e.g. user name) the agent can reference	          Dependencies

