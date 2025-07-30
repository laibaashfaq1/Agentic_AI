from agents import Agent, Runner, trace
from connection import config
import asyncio
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from dotenv import load_dotenv

load_dotenv()


waiter_agent = Agent(
    name = "Waiter Agent",
    instructions = """You are a waiter agent and provide a list of pizzas to the costumer,
    ## Your Pizza List:
    1. Margherita - $12
    2. Pepperoni - $15
    3. BBQ Chicken - $18
    4. Veggie Supreme - $14
    5. Hawaiian - $16"""
)

welcome_agent = Agent(
    name ="Welcome Agent",
    instructions = """"You are a Welcome agent in Pizza Restaurant your task is to
    grret the customer and handsoff to the Waiter agent.
    1. Welcome the customer warmly.
    2. Ask them to have a seat.
    3. Handoffs to the Waiter Agent with a message to provide the pizza list.
    4. If the customer asks for a specific pizza, provide the list of pizzas.""",
    handoffs = [waiter_agent],
    handoff_description = "You need to handoff to waiter agent after welcome message appear"
) 

async def main():
    while True:
        msg = input("Enter your message")

        with trace ("Class05"):

            result = await Runner.run(welcome_agent, msg, 
                                      run_config = config)
            
            print(result.last_agent.name)
            print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())