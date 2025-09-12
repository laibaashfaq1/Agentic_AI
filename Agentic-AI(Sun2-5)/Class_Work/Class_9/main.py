# --- Imports ---
from agents import Agent, RunContextWrapper, Runner, function_tool  # Agent system tools
from pydantic import BaseModel  # For structured data models
from connection import config  # Config (API keys, model setup, etc.)
import asyncio  # To run async code
import rich  # For pretty terminal output


# --- User data model ---
class UserInfo(BaseModel):
    user_id: int | str
    name: str


# --- Local context (user info) ---
user = UserInfo(user_id=122222, name="Laiba Ashfaq")


# --- Tool: fetch user info ---
@function_tool
def get_user_info(wrapper: RunContextWrapper[UserInfo]):
    return f'The user info is {wrapper.context}'


# --- Agent with tool ---
personal_agent = Agent(
    name="Agent",
    instructions="You are a helpful assistant, always call the tool to get user's information",
    tools=[get_user_info]
)


# --- Run agent ---
async def main():
    result = await Runner.run(
        personal_agent,
        'What is my name',  # User query
        run_config=config,
        context=user        # Pass local context
    )
    rich.print(result.final_output)


# --- Entry point ---
if __name__ == "__main__":
    asyncio.run(main())
