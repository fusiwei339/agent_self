import os
import json
import re

import tempfile

import pandas as pd
import autogen
from autogen import UserProxyAgent
from autogen import ConversableAgent, AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor

import numpy as np
import random

config_list=[
    {
        "model": "gpt-4o",
        "base_url": "https://api.chatanywhere.com.cn",
        "api_key": "sk-CUIdUOkG7Xl3lRF2Lfg4YULUew1dRRy3cLtjNB29vtwXpsGR"
    }
]

temp="""
    Your response must be in JSON format.
        [
        {
        "reasons": "Analyze the importance of each items"
        },
        {
        "name": "first item",
        "score": "1-15"
        },
        {
        "name": "second item",
        "score": "1-15"
        }
        ] 
"""

def create_agent(name):
    system_message_common="""Your name is {0}. You are in a group. Your responsibility is to maximize the overall effectiveness of the group. You are on behalf of your self. When it is your turn, please give at least one reason why you are for the topic. Keep it short. If you agree with the item prioritization, do not output the list. If you make changes on the list, output a new list.""".format(name)

    return AssistantAgent(
        name=name,
        system_message=system_message_common,
        llm_config={"config_list": config_list, "cache_seed": None},
    )  

names=["one", "two", "three", "four", "five"]
agents=[create_agent(i) for i in names]

initializer = UserProxyAgent(
    name="init",
    # system_message="TERMINATE when the ranking does not change."
    code_execution_config=False,
)

first="First, you will complete this exercise individually."
second="Second, you will be allowed to consult with your group/team members and go through the exercise again. Share your individual solutions and reach a consensus ranking for each of the 15 items that best satisfies all group members."

groupchat = autogen.GroupChat(
    agents=[initializer]+agents,
    messages=[first, second],
    max_round=40,
    speaker_selection_method="round_robin",
    send_introductions=True,
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list, "cache_seed": None})

def save_to_json(entry):
    a = []
    fname="agent_self.json"
    if not os.path.isfile(fname):
        a.append(entry)
        with open(fname, mode='w') as f:
            f.write(json.dumps(a, indent=2))
    else:
        with open(fname) as feedsjson:
            feeds = json.load(feedsjson)

        feeds.append(entry)
        with open(fname, mode='w') as f:
            f.write(json.dumps(feeds, indent=2))

n=1
for i in range(n):
    start_message="""Your spacecraft has just crash-landed on the lighted side of the Mars. You were scheduled to rendezvous with the mother ship 300 miles away on the surface of the moon, but the rough landing has ruined your craft and destroyed all the equipment on board, except for the 15 items listed below. Your crew’s survival depends on reaching the mother ship, so you must choose the most critical items available for the 300-mile trip. Your task is to rank the 15 items in terms of their importance for survival. Place a 1 by the most important item, a 2 by the second-most important item, and so on through 15, the least important. The items are:
    1. Flashlight
    2. Jackknife
    3. Air map of the area
    4. Plastic raincoat
    5. Magnetic compass
    6. Compress kit w/ gauze
    7. .45-caliber pistol
    8. Parachute (red, white)
    9. Bottle of salt tablets
    10. 1 qt. of water/person
    11. Animals book
    12. Sunglasses per person
    13. 2 quarts of vodka
    14. 1 topcoat per person
    15. Cosmetic mirror
    """

    chat_result=initializer.initiate_chat(manager, message=start_message)
    save_to_json(chat_result.chat_history)
