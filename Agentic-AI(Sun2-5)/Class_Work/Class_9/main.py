from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel
from connection import config
import asyncio
import rich

class UserInfo(BaseModel):
    user_id: int | str
    name: str

user = UserInfo(user_id= 122222,
                name = "Laiba Ashfaq")

@function_tool
def get_user_info(wrapper: RunContextWrapper[UserInfo]):
    #rich.print(wrapper.context.name)
    return f'The user info is {wrapper.context}'
    #return f'The user info isw {wrapper.context.model_dump()}'

personal_agent = Agent(
    name = "Agent",
    instructions = "You are a helpful assistant, always call the tool to get user's information",
    tools = [get_user_info]
)

async def main():
    result = await Runner.run(
        personal_agent,
        'What is my name',
        run_config = config,
        context = user #local context
    )
    rich.print(result.final_output)

if __name__ == "__main__":
        asyncio.run(main())
        