# Function Calling
# function calling ki need tb hoti ha jab LLM ka pass wo cheez mojood na ho

# instruction jo ha wo developer message ha / system message ha 
# result jo ha wo user input ha 

from agents import Agent, Runner, function_tool
from connection import config
from datetime import datetime
import weather


@function_tool #decorator tool  ka necha hum apna khud ka function define kr skta hain
# 1. 
# 2. jab hum apna python ka function decorator tool ka necha define krein ga to wo us function ki regestry ma chala jaya ga 
def get_date():
    _now = datetime.now()
    return _now.strftime("the date is %d-%m-%Y")



agent = Agent (
    name = "assistant",
    instructions = "you are a helpful assistant",
    tools = [get_date, get_weather]
)

response = Runner.run_sync(
    agent,
    input = "Tell me the current date and time of karachi pakistan",
    # Pass the run config to the agent
    run_config = config
)
print(response.final_output)