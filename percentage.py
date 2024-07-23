import pandas as pd
import autogen
from autogen import UserProxyAgent
from autogen import ConversableAgent, AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor
from autogen.graph_utils import visualize_speaker_transitions_dict
import argparse

from prompt import task_prompt, eval_prompt, eval_prompt_next
from utils import *

parser = argparse.ArgumentParser()
parser.add_argument("--temperature", type=float, default=1.0)
parser.add_argument("--iteration", type=int, default=50)
parser.add_argument("--lean", type=str, default="positive")
parser.add_argument("--task", type=str, default="percent")
parser.add_argument("--focus", type=str, default="self")
parser.add_argument("--model", type=str, default="gpt-4o")
parser.add_argument("--demographics", type=str, default="None")
args = parser.parse_args()

model_name = args.model
lean = args.lean
task = args.task
focus = args.focus
iteration = args.iteration
temperature=args.temperature
demographics =args.demographics

def get_model():
    conf_list=[{"model":model_name}]
    if model_name.startswith("gpt"):
        conf_list[0]["base_url"]="https://api.chatanywhere.com.cn"
        conf_list[0]["api_key"]="sk-CUIdUOkG7Xl3lRF2Lfg4YULUew1dRRy3cLtjNB29vtwXpsGR"
        conf_list[0]["temperature"]=temperature
        ret={"config_list": conf_list, "cache_seed":None}
    else:
        conf_list[0]["api_type"]= "together"
        conf_list[0]["api_key"]="794de0b246a52737a9956e719bc1ddd071d04b66cd346e31c951cc1cf1800b68"
        ret={"config_list": conf_list, "cache_seed":None, "temperature": temperature}
    return ret 


def get_demographics(name):
    base="""Your name is "{0}". {1}You are part of a group that includes "One", "Two", "Three", "Four" and "Five". When providing your input: Speak only on your own behalf. Keep your response concise."""
    if demographics=="None":
        return base.format(name, "")
    return base.format(name, "You are "+demographics+". ")


def get_eval_prompt(focus, task, lean, j):
    if focus=="self":
        return eval_prompt["_".join([focus, task, lean])]
    elif focus=="next":
        return eval_prompt_next(j)
    else:
        return eval_prompt["_".join([focus, task])]


names=["One", "Two", "Three", "Four", "Five"]
filename_base="_".join(map(str,[os.path.basename(model_name), lean, task, focus, temperature, demographics.replace(" ", "_")]))

if model_name.startswith("gpt"):
    logging_session_id = autogen.runtime_logging.start(config={"dbname": filename_base+".db"})
    print("Logging session ID: " + str(logging_session_id))

def create_agent(name):
    return AssistantAgent(
        name=name,
        system_message=get_demographics(name),
        llm_config=get_model(),
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
    llm_config=get_model()
)

for i in range(iteration):
    task_chat_result=initializer.initiate_chat(managerPlay, message=task_prompt["joke"].format(len(names)*15), cache=None)

    if model_name.startswith("meta"):
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
            message=get_eval_prompt(focus, task, lean, j),
            carryover=managerPlay.messages_to_string(task_chat_result.chat_history)
        )

        save_to_csv(eval_chat_result.chat_history[-1]["content"], names, j, filename_base+".csv")
        if model_name.startswith("meta"):
            save_to_json(eval_chat_result.chat_history, filename_base+".json")

if model_name.startswith("gpt"):
    autogen.runtime_logging.stop()