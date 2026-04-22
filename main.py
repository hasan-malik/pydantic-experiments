from pydantic_ai import Agent

agent = Agent(
    model='openai:gpt-4o-mini',
    system_prompt="You are an assistant. Answer concisely."
)