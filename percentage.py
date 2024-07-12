import pandas as pd
import autogen
from autogen import UserProxyAgent
from autogen import ConversableAgent, AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor
from autogen.graph_utils import visualize_speaker_transitions_dict

from prompt import task_prompt, eval_prompt
from utils import *

# names=["one", "two", "three"]
names=["one", "two", "three","four"]
# names=["one", "two", "three", "four", "five"]
# names=["one", "two", "three", "four", "five", "six"]

def create_agent(name):
    system_message_common="""Your name is {0}. You are in a group including {1}. You are on behalf of yourself. When it is your turn, keep it short. If you are satisfied with previous conversation, then say TERMINATE to indicate the conversation is finished and this is your last message. Do not talk on behave of other group members.""".format(name,','.join(names))

    return AssistantAgent(
        name=name,
        system_message=system_message_common,
        llm_config={"config_list": config_list, "cache_seed": None},
    )  

agents=[create_agent(i) for i in names]

initializer = UserProxyAgent(
    name="init",
    human_input_mode="ALWAYS",
    code_execution_config=False,
)

groupchatPlay = autogen.GroupChat(
    agents=[initializer]+agents,
    messages=[],
    max_round=len(names)*2,
    speaker_selection_method="round_robin",
    # send_introductions=True,
)
managerPlay = autogen.GroupChatManager(
    name="play manager",
    groupchat=groupchatPlay, 
    llm_config={"config_list": config_list, "cache_seed": None}
)

n=1
for i in range(n):
    task_chat_result=initializer.initiate_chat(managerPlay, message=task_prompt["joke"].format(len(names)*15), cache=None)

    save_to_json(task_chat_result.chat_history)

    initializer2 = UserProxyAgent(
        name="init2",
        code_execution_config=False,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
    )

    for j in range(len(names)):
        eval_chat_result=initializer2.initiate_chat(
            agents[j], 
            message=eval_prompt["self_percent_positive"],
            carryover=managerPlay.messages_to_string(task_chat_result.chat_history)
        )

        save_to_json(eval_chat_result.chat_history)
        analyzeRanking(eval_chat_result.chat_history[-1]["content"], names, j)

