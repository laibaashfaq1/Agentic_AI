import rich 
import asyncio
from connection import config
from pydantic import BaseModel
from agents import(
    Agent,
    InputGuardrailTripwireTriggered,
    Runner,
    input_guardrail,
    GuardrailFunctionOutput
)


######################################
# Exercise 1: Class Timing Guardrail
######################################


# Output model for checking if input is class-related
class ClassOutput(BaseModel):
    reponse: str
    isClassRelated: bool  #True = allowed, False = blocked(guardrail triggers)

# Guardrail Agent Definition
class_agent = Agent(
    name = 'Class Agent',
    instructions = """
    You are a class agent. Only handle queries related to study subjects.
    If user talks about changing class timmings, deny it.
""",
    output_type = ClassOutput
)

# Input Guardrail Function

@input_guardrail
async def class_guardrail(ctx, agent, input) -> GuardrailFunctionOutput:
    # Run guardrail agent to check input
    result = await Runner.run(class_agent, input,  run_config = config)

    # Return guardrail decision
    return GuardrailFunctionOutput(
        ouyput_info = result.final_output.response,
        # If not class related -> tripwire triggered
        tripwire_triggered = not result.final_output.isClassRelated
    )

# Main Student Agent With Guardrail
student_agent = Agent(
    name = "Student Agent",
    instructions = "You are a student asking about studies,",
    input_guardrails = [class_guardrail]
)

# Main runner for Exercise 1
async def excercise():
    try:
        result = await Runner.run(student_agent,
                                 "I want to change my class timings",
                                 run_config = config)
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Guardrail Triggered: Class timing change not allowed!")


######################################
# Exercise 2: Father Guardrail
######################################

# Output model for temperature check
class TempOutput(BaseModel):
    response: str
    isBelow26: bool  # True if below 26°C, False otherwise

# Guardrail Agent
father_agent = Agent(
    name="Father Agent",
    instructions="""
        You are a father. If your child wants to go outside below 26°C, stop him.
    """,
    output_type=TempOutput
)

# Guardrail Function
@input_guardrail
async def father_guardrail(ctx, agent, input) -> GuardrailFunctionOutput:
    result = await Runner.run(father_agent, input, run_config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.isBelow26  # Stop if below 26
    )

# Child Agent with Guardrail
child_agent = Agent(
    name="Child Agent",
    instructions="You are a child who wants to go outside and play.",
    input_guardrails=[father_guardrail]
)

# Main runner for Exercise 2
async def exercise2():
    try:
        result = await Runner.run(child_agent,
                                  "I want to play outside, temperature is 20°C",
                                  run_config=config)
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("❌ Guardrail Triggered: Father stopped the child (too cold)!")


#########################################
# Exercise 3: Gate Keeper Guardrail
#########################################

# Output model for school check
class StudentOutput(BaseModel):
    response: str
    isOtherSchool: bool  # True if from another school, False if correct school

# Guardrail Agent
gate_keeper_agent = Agent(
    name="Gate Keeper",
    instructions="""
        You are a school gatekeeper. Only allow students of this school.
        If student is from another school, stop him.
    """,
    output_type=StudentOutput
)

# Guardrail Function
@input_guardrail
async def gate_guardrail(ctx, agent, input) -> GuardrailFunctionOutput:
    result = await Runner.run(gate_keeper_agent, input, run_config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=result.final_output.isOtherSchool  # Block other school students
    )

# Student Entry Agent with Guardrail
student_entry_agent = Agent(
    name="Student Entry Agent",
    instructions="You are a student trying to enter the school gate.",
    input_guardrails=[gate_guardrail]
)

# Main runner for Exercise 3
async def exercise3():
    try:
        result = await Runner.run(student_entry_agent,
                                  "I am a student from another school",
                                  run_config=config)
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("❌ Guardrail Triggered: Gatekeeper stopped the student!")


#########################################
# Run all exercises
#########################################

async def main():
    print("\n--- Exercise 1 ---")
    await exercise1()

    print("\n--- Exercise 2 ---")
    await exercise2()

    print("\n--- Exercise 3 ---")
    await exercise3()


if __name__ == "__main__":
    asyncio.run(main())