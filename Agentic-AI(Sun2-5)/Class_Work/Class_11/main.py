from agents import Agent, ModelSettings, RunContextWrapper, Runner, function_tool, trace
import rich
from connection import config
import asyncio
import requests  # For Fetching API

@function_tool(name_override="Get_Location",
               description_override="Get the current location of a user")
def get_current_location() -> str:
    """
    Return the current location
    """
    # url = requests.get('my_google_maps_api')
    # return url.json()
    return "GH Sindh, Karachi"


# @function_tool
# def Addition():
# return 10 * 7

@function_tool(name_override="Add_Number")
def Addition(num1, num2) -> int:
    """
    num1 :int Takes the first number as an arguments
    Return the addition of two numbers
    """
    return 10 + 109


# This function books a cab with three parameters
def book_a_cab(by, to, amount):
    """
    by: users current location
    to: users destination
    amount: int the amount to be charged for the ride

    Return the destination, current location and amount
    """
    return {"by": "GH", "to": "Home", "amount": 400}


# Comment this code from line 42 to 58
# def send_email(from_email, to_email, subject, body) -> :

# # First Example for is_Admin group by a dynamic function
# @function_tool(name_override = "Adding_Member_to_Whatsapp_group",
#                description_override= "Add a member to the whatsapp group only by the Admins",
#                is_enabled = True
#             )
# def add_members():
#     """
#     This function Return the added member to the group
#     """
#     members = []
#
#     members.append("Laiba")
#     return "Member has been added to the group"


# comment the code from line 63 to 73
##################### is_enabled #####################
# def is main():
#     return False

# # Second Example for is_Admin group
# def is_main():
#     # admin_name = "ALi"
#     admins = ["Ali", "Laiba"]
#     if "Ali" in admins or "Laiba" in admins:
#         return True
#     else:
#         return False

def is_admin():
    admin_name = "Ali"
    if admin_name == "Ali":
        return True
    else:
        return False


@function_tool(
    name_override="Adding_Member_to_Whatsapp_group",
    description_override="Add a member to the whatsapp only by the admins",
    is_enabled=is_admin
    # is_enabled = False
)
def add_members():
    """
        This function return the added member to the group.
    """
    return "Member has been added to the group"


personal_agent = Agent(
    name="Agent",
    instructions="""
    You ara a helpful assistant always call a tool to get the location
    """,
    tools=[get_current_location]
)

whatsapp_agent = Agent(
    name="Whatsapp Agent",
    instructions="""
    You are a admin of a whatsapp group your duty is to add members to the group
""",
    tools=[add_members]
)

writer_agent = Agent(
    name="Writer Agent",
    instructions="You are a helpful assistant that helps in writting blogs",
    model_settings=ModelSettings(
        temperature=0.9,
        # tool_choice = "required"
        tool_choice=None
        # tool_choice = "auto"
    )
)


async def main():
    # result = await Runner.run(
    #     whatsapp_agent,
    #     "Add a member to the whatsapp group",
    #     run_config = config,
    # )

    result = await Runner.run(
        writer_agent,
        "Describe blood pressure",
        run_config=config,
    )
    # rich.print(result.new_items)
    rich.print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())

# what is my current location
