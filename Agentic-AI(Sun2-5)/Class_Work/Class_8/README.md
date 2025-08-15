
<!-- Required Installments -->
uv init .
uv venv
.venv\Scripts\activate
uv run main.py
uv pip install requests
uv add openai-agents
uv add python-dotenv


GUARDRAILS:-
 Guardrails are safety checks or rules to control and guide AI behavior.

TYPES OF GUARDRAILS:-
1. INPUT GUARDRAILS:-
Control or filter what users can input (e.g., blocking harmful or irrelevant prompts).Input Guardrail function ki form ma hota ha.Input guardrail user ka input sa chalta ha.
2. OUTPUT GUARDRAILS:-
Monitor and adjust AI responses to ensure safe, accurate, and ethical outputs.










<!-- Input GuardRails -->
Exercise # 1 Objective: Make a agent and make an input guardrail trigger. Prompt: I want to change my class timings 😭😭 Outcome: After running the above prompt an InputGuardRailTripwireTriggered in except should be called. See the outcome in LOGS

Exercise # 2 Objective: Make a father agent and father guardrail. The father stopping his child to run below 26C.

Exercise # 3 Objective: Make a gate keeper agent and gate keeper guardrail. The gate keeper stopping students of other school.