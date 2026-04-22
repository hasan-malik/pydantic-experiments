from pydantic_ai import Agent
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    model='anthropic:claude-haiku-4-5-20251001',
    system_prompt="You are an assistant. Answer concisely." # system prompt: sent with every user prompt
)

result = agent.run_sync(user_prompt="What is the capital of Bulgaria?")
print(result.output)
