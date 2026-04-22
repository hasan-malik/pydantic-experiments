from pydantic_ai import Agent
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    model='openai:gpt-4o-mini',
    system_prompt="You are an assistant. Answer concisely." # system prompt: sent with every user prompt
)

agent.run_sync(user_prompt="What is the capital of Bulgaria?")
