from agents import Agent, Runner, trace
from connection import connfig 
import asyncio

# POet Agent - generates or processes poems
poet_agent = Agent(
    name= 'Poet Agent',
    instructions = """
    You are a poet agent. Your role is to generate a two-stanza poem or process an input poem.
    Poems can be lyric (emotional), narrative (storytelling), or dramatic (performance)
    If you are asked without a poem, generate a short two-stanzas poem on emotions.
    """,
)

# Analyst Agents for different poetry types
lyric_analyst_agent = Agent(
    name = "Lyric Analyst Agent",
    instructions = """ 
        You analyze lyric poetry focusing on emotions, feelings,
        and musically. Provide insights about the poem's mood, use of rythm, and personal voice.
        """,
)

narrative_analyst_agent = Agent(
    name = "Narrative Analyst Agent",
    isntructions = """
        You analyze narrative poetry focusing on storytelling elements: plot, characters, and imagery.
        """
)

dramatic_analyst_agent = Agent(
    name = "Dramatic Analyst Agent",
    instructions = """
        You analyze dramatic poetry emphasizing voice, dialogue, and performance aspect.
        """
)

#  Custom Parent Agent with post-process logic
class CustomParentAgent(Agent):
    async def run(self, input, config):
        # Step 1 : Send to Poet Agent
        poet_output = await poet_agent.run(input, config)

        # Step 2 : Detect poem type (basic keyword check)
        poem_text = poet_output.output.lower()

        if "dialogue" in poem_text or "voice" in poem_text or "stage" in poem_text:
            next_ageent = dramatic_analyst_agent
        elif "story" in poem_text or "character" in poem_text or "event" in poem_text:
            next_agent = lyric_analyst_agent
        else:
            next_agent = lyric_analyst_agent

        # Step 3 : Send to the correct Analyst Agent
        final_output = await next_agent.run(poet_output.output, config)
        return final_output
    

# Use custom parent agent in place
parent_agent = CustomParentAgent(
    name = "Parent Poet Orchestrator", # Orchestrator Agent: Manages and coordinates tasks between multiple agents
    instruction = """
        You are the orchestor agent for poetry tasks.
        When given a request or poem, first delegate to the poet agent to generate or process poetry.
        After recieving the poem, detect wheater it's lyric, narrative, or dramatic poetry. 
        Delegate the poem to the coresponding analyst agent for deeper analysis.
        If the type is not clear, or multiple types apply, delegate to all analyst.
        If the query is not about poetry, respond with a message indicating that you only handle poetry tasks. 
        """,
    handoffs = [poet_agent, lyric_analyst_agent, narrative_analyst_agent, dramatic_analyst_agent],
)