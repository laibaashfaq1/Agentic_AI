import rich
import asyncio
from connection import config
from pydantic import BaseModel
from agents import (
    Agent, 
    OutputGuardrailTripwireTriggered,
    InputGuardrailTripwireTriggered, 
    Runner, 
    input_guardrail, 
    GuardrailFunctionOutput, 
    output_guardrail) 


class PassengerOutput(BaseModel):
    response:str
    isWeightExceed:bool

airport_security_guard = Agent(
    name = "Airport Security Guard",
    instructions = """
        Your task is to check the passenger luggage. If passenger's 
        lagguage is more than 25Kg, gracefully stop them. 
    """,
    output_type = PassengerOutput
)

@input_guardrail
async def security_quardrail(ctx, agent, input): # ctx only use krein ga q ka abhi hum na yh nahi parah ha
    result = await Runner.run(airport_security_guard,
                              input, 
                                run_config = config
                             )
    rich.print(result.final_output)

    return GuardrailFunctionOutput(
        output_info = result.final_output.response,
        # tripwire_triggered ki jo form ha wo hamesha boolean ma ho gi mean true yh false 
        # if agr tripwire_triggered True hua to wo misuse hua ha ar working wahan hi ruk jaya gi aga nahi chal saka gi 
        # if agr False hua to matalb sahi hua ha is ki policy ka against nahi hua
        tripwire_triggered = result.final_output.isWeightExceed
    )

# Main Agent

# Passenger Agent
passenger_agent = Agent(
    name = "Passenger",
    instructions = "You are a passenger agent ",
    input_guardrails = [security_quardrail]
)

async def main():
    try:
        result = await Runner.run(passenger_agent, 
                                  'My luggage weight 25kg',
                                  run_config = config)
        print("Passenger is onboarded")

    except InputGuardrailTripwireTriggered:
        print("Passenger cannot check-in")


##################### Output Guardrails ####################

class MessageOutput(BaseModel): #Model for Agent Output Type
    response: str

class PHDOutput(BaseModel): #Model top trigger the guardrail
    isPHDLevelResponse: bool

phd_guardrail_agent = Agent(
    name = 'PHD Guardrail Agent',
    instructions = """
You are a PHD Guardrail Agent that evaluates if text is too complex 
for 8th grade students. If the response is very hard to read for an eight grade
student deny the agent response.
""",
output_type = PHDOutput
)

@output_guardrail
async def PHD_guardrail(ctx, agent, output) -> GuardrailFunctionOutput:
    result = await Runner.run (phd_guardrail_agent, 
                               output.response,
                               run_config=config)

    return GuardrailFunctionOutput(
        output_info = result.final_output,
        # tripwire_triggered ki jo form ha wo hamesha boolean ma ho gi mean true yh false 
        # if agr tripwire_triggered True hua to wo misuse hua ha ar working wahan hi ruk jaya gi aga nahi chal saka gi 
        # if agr False hua to matalb sahi hua ha is ki policy ka against nahi hua
       
        # tripwire_triggered = True #hard code kiya ha 
        tripwire_triggered = result.final_output.isPHDLevelResponse
    )

# Main executor agent
eight_grade_std = Agent(
    name = "8th Grade Student",
    instructions = """
    1. You are an agent taht answer query to a eight standard student.
       Keep your vocabulary easy and simple.
    2. If asked to give answers in most difficult level use the most difficult level use the most hardest english terms.
""",
    output_type = MessageOutput,
    output_guardrails = [PHD_guardrail]
)

async def og_main():
    query = "What are trees? Explain using most complex scientific terminilogy possible"
    # query = "What are trees? Explain in simple words"
    try:
        result = await Runner.run(eight_grade_std, 
                                  query, 
                                  run_config=config)
    except OutputGuardrailTripwireTriggered:
        print("Agent output is not according to the exceptations")

if __name__ == "__main__":
    asyncio.run(og_main())
    asyncio.run(main())