from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

load_dotenv()

gemini_api_key = os.getenv("GEMIMI_API_KEY")

# Check if the API key is set; if not raise error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-gemini-2.0-flash", #jo bhi least model ho 
    openai_client = external_client
)

connfig = RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disabled = True
)