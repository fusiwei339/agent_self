import json
import os
import re
history = json.load(open("agent_self.json", 'r'))[1]


import pandas as pd
import numpy as np
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
        {
        "name": "one"
        "rank": "1-5"
        },
        {
        "name": "two"
        "rank": "1-5"
        },"""

def create_agent(n):
    system_message_common="""Your name is {0}. You are in a group including "one", "two", "three", "four", "five". You have finished a group discussion. analyze your discussions and access yourself and other group members on the extent to which you had contributed to the overall effectiveness of the group. The self- and peer rankings ranged from 1 (most effective) to 5 (least effective). Do not give the same ranking to more than 1 group member; that is, no ties are allowed. You must directly compare your own performance with those of the other group members. Your response must be in JSON format with "name" and "rank".""".format(n)

    return AssistantAgent(
        name=n,
        system_message=system_message_common,
        llm_config={"config_list": config_list, "cache_seed": None},
    )  

names=["one", "two", "three", "four", "five"]
agents=[create_agent(i) for i in names]

initializer = UserProxyAgent(
    name="init",
    # system_message="TERMINATE when the ranking does not change."
    code_execution_config=False,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
)

def save_to_json(entry):
    a = []
    fname="rating.json"
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
    ret={"self":0, "peer":0}
    df=pd.DataFrame(jsonstr)
    df["kind"]=np.where(df["name"]==names[i], "self", "peer")
    df.to_csv("statistics.csv", mode='a', index=False, header=False)

def parseJsonStr(result_str):
    if "```json" in result_str:
        ret=re.findall(r"```json(.*?)```", result_str, re.DOTALL)[0]
    elif "'''json" in result_str:
        ret=re.findall(r"'''json(.*?)'''", result_str, re.DOTALL)[0]
    else:
        ret=result_str
    try:
        ret=json.loads(ret)
        print(ret)
    except ValueError:
        print('invalid string:'+ret)
    return ret


# for i in range(5):
#     chat_result=initializer.initiate_chat(agents[i], message="Analyze the chat history and rate the performance of each group member. The history is:"+json.dumps(history))

#     save_to_json(chat_result.chat_history)
#     analyzeRanking(chat_result.chat_history[-1]["content"], i)

stat=pd.read_csv('statistics.csv')
print(stat.groupby('kind').score.describe())