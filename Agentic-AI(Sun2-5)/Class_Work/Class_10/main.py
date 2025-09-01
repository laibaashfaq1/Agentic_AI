from agents import Agent, RunContextWrapper, Runner, function_tool, trace
from pydantic import BaseModel
from connection import config
import asyncio
import rich
from dotenv import load_dotenv

load_dotenv()

# ----------- Example of Local  Context ----------- #

# class CartItems (BaseModel):
#     product : list
#     user_id : int
#     brand : str
#     total_amount : int

# cart = CartItems (product = ["Mobile", "Laptop"], 
#                   user_id = "930002200",
#                   brand = "apple",
#                   total_amount=342398
#                   )

# async def MypersonalFunction(wrapper:  RunContextWrapper[CartItems]):
#     return wrapper

# @function_tool
# def products_info(wrapper: RunContextWrapper[CartItems]):
#     print("Checking Context", wrapper)
#     return f'{wrapper.context}'


# ------------ Example of Dynamic Context ------------ #

class Person(BaseModel):
    name : str
    user_level: str

personOne = Person(
    name = 'Laiba',
    user_level = "Junior"
)

async def my_dynamic_instructions(ctx:RunContextWrapper[Person],
                                  agent: Agent):
    if ctx.context.user_level == 'junior' or ctx.context.user_level == 'mid_level':
        return """
            Keep your ansewrs simple and easy to understand.
        """
    elif ctx.context.user_level == "PHD":
        return """
            Keep your vocabulary advanced and very like your are talking to a PHD level person.
"""

personal_agent = Agent (
    name = "Agent",
    instructions = my_dynamic_instructions,
)

async def main():
    with trace("Learn Dynamic Instructions"):
        result = await Runner.run(
            personal_agent,
            'What is light?',
            run_config = config,
            context = personOne #local context
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())