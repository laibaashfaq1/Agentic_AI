from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Gemini API Key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if API key is set
if not gemini_api_key:
    raise ValueError("❌ Gemini API key is not set. Please add it to your .env file as GEMINI_API_KEY.")

# Show API key (optional — for testing only)
print(f"✅ Gemini API Key Loaded: {gemini_api_key}")

# Set up Gemini-compatible OpenAI client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Load Gemini model via OpenAI interface
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configure the agent run
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Create the translation agent
Translator = Agent(
    name="Translator Agent",
    instructions="""
    You are a Translator Agent.
    Your job is to translate Urdu sentences, paragraphs, or essays into fluent English.
    """
)

# Get user input for translation
user_input = input("📥 Enter Urdu text to translate: ").strip()

if not user_input:
    raise ValueError("⚠️ Input is empty. Please provide some Urdu text.")

# Run the agent synchronously
response = Runner.run_sync(
    Translator,
    input=user_input,
    run_config=config
)

# Output the final translated result
print("📤 Translated Output:")
print(response.final_output)
