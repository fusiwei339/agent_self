import pandas as pd
import autogen
from autogen import UserProxyAgent
from autogen import ConversableAgent, AssistantAgent
from autogen.coding import LocalCommandLineCodeExecutor
from autogen.graph_utils import visualize_speaker_transitions_dict
import argparse

from prompt import task_prompt, eval_prompt 
from utils import *

def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError(f'{value} is not a valid boolean value')

parser = argparse.ArgumentParser()
parser.add_argument("--temperature", type=float, default=0.7)
parser.add_argument("--iteration", type=int, default=50)
parser.add_argument("--lean", type=str, default="neutral")
parser.add_argument("--task", type=str, default="percent")
parser.add_argument("--focus", type=str, default="self")
parser.add_argument("--model", type=str, default="gpt-4o")
parser.add_argument("--topic", type=str, default="joke")
parser.add_argument("--demographics", type=str, default="None")
parser.add_argument("--cot", type=str_to_bool, default=False)
args = parser.parse_args()

model_name = args.model
lean = args.lean
task = args.task
focus = args.focus
topic = args.topic
iteration = args.iteration
temperature=args.temperature
demographics =args.demographics
cot=args.cot
print(args)

def get_model():
    conf_list=[{"model":model_name}]
    if model_name.startswith("gpt"):
        conf_list[0]["base_url"]=os.environ["OPENAI_API_BASE"]
        conf_list[0]["api_key"]=os.environ["OPENAI_API_KEY"]
        conf_list[0]["temperature"]=temperature
        ret={"config_list": conf_list, "cache_seed":None}
    else:
        conf_list[0]["api_type"]= "together"
        conf_list[0]["api_key"]=os.environ["TOGETHER_API_KEY"]
        ret={"config_list": conf_list, "cache_seed":None, "temperature": temperature}
    return ret 


def get_demographics(name):
    base="""Your name is "{0}". {1}You are part of a group that includes "One", "Two", "Three", "Four" and "Five". When providing your input: Speak only on your own behalf. Keep your response concise."""
    if demographics=="None":
        return base.format(name, "")
    return base.format(name, "You are "+demographics+". ")


def get_eval_prompt(focus, task, lean, j, cot):
    formatter="""Format your response in a JSON array with "name" and "percentage"."""
    cot_formatter="""Let's think step by step. Output your thought first, and then format your response in a JSON array with "name" and "percentage"."""
    if focus=="self":
        if cot:
            return eval_prompt["_".join([focus, task, lean])].format(topic)+cot_formatter
        return eval_prompt["_".join([focus, task, lean])].format(topic)+formatter
    else:
        return eval_prompt["_".join([focus, task])]

names=["One", "Two", "Three", "Four", "Five"]
filename_base="_".join(map(str,[os.path.basename(model_name), lean, task, focus, temperature, topic, demographics.replace(" ", "_"), cot]))

def create_agent(name):
    return AssistantAgent(
        name=name,
        system_message=get_demographics(name),
        llm_config=get_model(),
    )  

for it in range(iteration):

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

    task_chat_result=initializer.initiate_chat(managerPlay, message=task_prompt[topic], cache=None)

    initializer2 = UserProxyAgent(
        name="init2",
        code_execution_config=False,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
    )

    for j in range(len(names)):
        eval_chat_result=initializer2.initiate_chat(
            agents[j], 
            message=get_eval_prompt(focus, task, lean, j, cot),
            carryover=managerPlay.messages_to_string(task_chat_result.chat_history)
        )

        save_to_csv(eval_chat_result.chat_history[-1]["content"], names[j], filename_base+".csv")
