from agents import Agent, RunContextWrapper, Runner, function_tool, trace
from pydantic import BaseModel
from connection import config
import asyncio
import rich
from dotenv import load_dotenv

# Load environment variables (API keys, configs, etc.)
load_dotenv()

# ----------- Example of Local Context (commented out) ----------- #
# This section shows how to pass shopping cart info to an agent as context.
# It’s disabled here, but left as a reference.
#
# class CartItems (BaseModel):
#     product : list
#     user_id : int
#     brand : str
#     total_amount : int
#
# cart = CartItems(product=["Mobile", "Laptop"], 
#                  user_id="930002200",
#                  brand="apple",
#                  total_amount=342398)
#
# async def MypersonalFunction(wrapper: RunContextWrapper[CartItems]):
#     return wrapper
#
# @function_tool
# def products_info(wrapper: RunContextWrapper[CartItems]):
#     print("Checking Context", wrapper)
#     return f'{wrapper.context}'


# ------------ Example of Dynamic Context ------------ #
# Instead of fixed instructions, the agent changes its behavior
# based on the user’s "level" (Junior, Mid_level, PhD, etc.).

class Person(BaseModel):
    name: str
    user_level: str

# Create a Person object as the context
personOne = Person(
    name='Laiba',
    user_level="Junior"
)

# Dynamic instructions function:
# - If user is Junior/Mid_level → simple answers
# - If user is PhD → advanced vocabulary
async def my_dynamic_instructions(ctx: RunContextWrapper[Person],
                                  agent: Agent):
    if ctx.context.user_level == 'junior' or ctx.context.user_level == 'mid_level':
        return """
            Keep your ansewrs simple and easy to understand.
        """
    elif ctx.context.user_level == "PHD":
        return """
            Keep your vocabulary advanced and very like your are talking to a PHD level person.
"""

# Create agent with dynamic instructions
personal_agent = Agent(
    name="Agent",
    instructions=my_dynamic_instructions,
)

# Main function to run the agent
async def main():
    # trace() is used for logging/tracing execution
    with trace("Learn Dynamic Instructions"):
        result = await Runner.run(
            personal_agent,
            'What is light?',   # Question for the agent
            run_config=config,  # Config file (API keys, setup)
            context=personOne   # Pass user info as context
        )
        rich.print(result.final_output)  # Pretty print the result

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
