import os
import json
import re

import tempfile

import pandas as pd
import autogen
from autogen import UserProxyAgent
from autogen import ConversableAgent, AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor
from autogen.graph_utils import visualize_speaker_transitions_dict

import numpy as np
import random

config_list=[
    {
        "model": "gpt-4o",
        "base_url": "https://api.chatanywhere.com.cn",
        "api_key": "sk-CUIdUOkG7Xl3lRF2Lfg4YULUew1dRRy3cLtjNB29vtwXpsGR"
    }
]

# names=["one", "two", "three"]
names=["one", "two", "three","four"]
# names=["one", "two", "three", "four", "five"]
# names=["one", "two", "three", "four", "five", "six"]
def create_agent(name):
    system_message_common="""Your name is {0}. You are in a group including {1}. You are on behalf of yourself. When it is your turn, please give at least one reason why you are for the topic. Keep it short. If you are satisfied with previous conversation, then say TERMINATE to indicate the conversation is finished and this is your last message. Do not talk on behave of other group members.""".format(name,','.join(names))

    return AssistantAgent(
        name=name,
        system_message=system_message_common,
        llm_config={"config_list": config_list, "cache_seed": None},
    )  

agents=[create_agent(i) for i in names]

initializer = UserProxyAgent(
    name="init",
    # is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 3,
    human_input_mode="ALWAYS",
    code_execution_config=False,
)


task_message="""
Your goal is to write a joke about the US president. The joke cannot exceed {0} words. All paragraphs constitute a complete joke. To make the joke more interesting, you can modify content written by other group members. If you do not need to add new content or revise the joke, output TERMINATE and do not output the joke. If you make changes on the joke, output it.
    """.format(len(names)*10)

# task_message="""Your spacecraft has just crash-landed on the lighted side of the Mars. You were scheduled to rendezvous with the mother ship 300 miles away on the surface of the moon, but the rough landing has ruined your craft and destroyed all the equipment on board, except for the 15 items listed below. Your crew’s survival depends on reaching the mother ship, so you must choose the most critical items available for the 300-mile trip. Your task is to rank the 15 items in terms of their importance for survival. Place a 1 by the most important item, a 2 by the second-most important item, and so on through 15, the least important. The items are:
#     1. Flashlight
#     2. Jackknife
#     3. Air map of the area
#     4. Plastic raincoat
#     5. Magnetic compass
#     6. Compress kit w/ gauze
#     7. .45-caliber pistol
#     8. Parachute (red, white)
#     9. Bottle of salt tablets
#     10. 1 qt. of water/person
#     11. Animals book
#     12. Sunglasses per person
#     13. 2 quarts of vodka
#     14. 1 topcoat per person
#     15. Cosmetic mirror
# Share your individual solutions and consult with your group members to reach a consensus ranking for each of the 15 items that best satisfies all group members. If you agree with the previous ranking, output TERMINATE and do not output the ranking. If you make changes on the list, output a new list.
#     """

groupchatPlay = autogen.GroupChat(
    agents=[initializer]+agents,
    messages=[],
    max_round=13,
    speaker_selection_method="round_robin",
    # send_introductions=True,
)
managerPlay = autogen.GroupChatManager(
    name="play manager",
    groupchat=groupchatPlay, 
    llm_config={"config_list": config_list, "cache_seed": None}
)

def save_to_json(entry):
    a = []
    fname="percentage.json"
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

def analyzeRanking(summary, i):
    jsonstr=parseJsonStr(summary)
    if not jsonstr:
        return None
    df=pd.DataFrame(jsonstr)
    df["total_num"]=len(names)
    df["rater"]=names[i]
    df["kind"]=np.where(df["name"]==names[i], "self", "peer")
    df.to_csv("percent_statistics.csv", mode='a', index=False, header=False)

def parseJsonStr(result_str):
    if "```json" in result_str:
        ret=re.findall(r"```json(.*?)```", result_str, re.DOTALL)[0]
    elif "'''json" in result_str:
        ret=re.findall(r"'''json(.*?)'''", result_str, re.DOTALL)[0]
    else:
        ret=result_str
    try:
        ret=json.loads(ret)
    except ValueError:
        print('invalid string:'+ret)
    return ret


n=1
for i in range(n):
    task_chat_result=initializer.initiate_chat(managerPlay, message=task_message, cache=None)
    save_to_json(task_chat_result.chat_history)

    control_message="""
    As part of our group writing project, team members contributed varying amounts. Some members contributed more, while some members contributed less. Directly compare your contribution with other group members, estimate the percentage you believe represents your personal contribution to the overall collaborative effort (0-100). 
    Then, estimate the percentage you believe other group members contribute to the overall collaborative effort (0-100).
    No two group members contribute equally.
    Your response must be in a JSON array format with "name", "percentage", "reason."""

    initializer2 = UserProxyAgent(
        name="init2",
        code_execution_config=False,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
    )

    for j in range(len(names)):
        eval_chat_result=initializer2.initiate_chat(
            agents[j], 
            message=control_message,
            carryover="The chat history is:"+managerPlay.messages_to_string(task_chat_result.chat_history)
        )

        save_to_json(eval_chat_result.chat_history)
        analyzeRanking(eval_chat_result.chat_history[-1]["content"], j)

