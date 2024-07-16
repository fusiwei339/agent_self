import pandas as pd
import autogen
from autogen import UserProxyAgent
from autogen import ConversableAgent, AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor
from autogen.graph_utils import visualize_speaker_transitions_dict
import argparse

from prompt import task_prompt, eval_prompt, eval_prompt_func
from utils import *

parser = argparse.ArgumentParser()
parser.add_argument("--temperature", type=int, default=1)
parser.add_argument("--iteration", type=int, default=50)
parser.add_argument("--lean", type=str, default="positive")
parser.add_argument("--task", type=str, default="percent")
parser.add_argument("--focus", type=str, default="self")
parser.add_argument("--model", type=str, default="gpt-4o")
args = parser.parse_args()

model_name = args.model
lean = args.lean
task = args.task
focus = args.focus
iteration = args.iteration
temperature=args.temperature

config_list=[
    {
        "model": model_name,
        "base_url": "https://api.chatanywhere.com.cn",
        "api_key": "sk-CUIdUOkG7Xl3lRF2Lfg4YULUew1dRRy3cLtjNB29vtwXpsGR"
    }
]

names=["one", "two", "three", "four", "five", "six"]
names=names[:4]

def create_agent(name):
    system_message_common="""Your name is {0}. You are in a group including {1}. You are on behalf of yourself. When it is your turn, keep it short. If you are satisfied with previous conversation, then say TERMINATE to indicate the conversation is finished and this is your last message. Do not talk on behave of other group members.""".format(name,','.join(names))

    return AssistantAgent(
        name=name,
        system_message=system_message_common,
        llm_config={"config_list": config_list, "cache_seed": None, "temperature": temperature},
    )  

agents=[create_agent(i) for i in names]

initializer = UserProxyAgent(
    name="init",
    human_input_mode="NEVER",
    code_execution_config=False,
)

groupchatPlay = autogen.GroupChat(
    agents=[initializer]+agents,
    messages=[],
    max_round=len(names)+1,
    speaker_selection_method="round_robin",
    # send_introductions=True,
)
managerPlay = autogen.GroupChatManager(
    name="play manager",
    groupchat=groupchatPlay, 
    llm_config={"config_list": config_list, "cache_seed": None}
)

filename_base="_".join(map(str,[model_name, lean, task, focus, temperature]))

for i in range(iteration):
    task_chat_result=initializer.initiate_chat(managerPlay, message=task_prompt["joke"].format(len(names)*15), cache=None)

    save_to_json(task_chat_result.chat_history, filename_base+".json")

    initializer2 = UserProxyAgent(
        name="init2",
        code_execution_config=False,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
    )

    for j in range(len(names)):
        eval_chat_result=initializer2.initiate_chat(
            agents[j], 
            message=eval_prompt_func(j, lean),
            # message=eval_prompt["_".join([focus, task, lean])],
            carryover=managerPlay.messages_to_string(task_chat_result.chat_history)
        )

        save_to_json(eval_chat_result.chat_history, filename_base+".json")
        save_to_csv(eval_chat_result.chat_history[-1]["content"], names, j, filename_base+".csv")

