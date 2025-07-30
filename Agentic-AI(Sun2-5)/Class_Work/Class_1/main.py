# Agentic AI (Agentic Artifical Intelligence)


# pip install openai-agents  
# pip install python-dotenv

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
print(gemini_api_key)
# Check if the api key is present if not raise error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider= external_client,
    tracing_disabled=True
)

# Write Agent
writer = Agent(
    # these two things are neccessary for the agent to run
    name = "Write Agent",
    instructions=
    """You are a write agent. 
    Generate a short story, essay, email etc based on the given topic.""",
)

response = Runner.run_sync(
    writer,
    input = "Write a 2 paragraph on the topic of 'The Future of AI'",
    # Pass the run config to the agent
    run_config = config
)
print(response.final_output)