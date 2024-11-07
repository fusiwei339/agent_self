import pandas as pd
import random
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
parser.add_argument("--prefix", type=str, default="")
parser.add_argument("--demographics", type=str, default="None")
parser.add_argument("--cot", type=str_to_bool, default=False)
args = parser.parse_args()

model_name = args.model
lean = args.lean
task = args.task
focus = args.focus
topic = args.topic
prefix = args.prefix
iteration = args.iteration
temperature=args.temperature
demographics =args.demographics
cot=args.cot
print(args)

def get_model():
    conf_list=[{"model":model_name}]
    if model_name.startswith("gpt"):
        conf_list[0]["base_url"]="https://xiaoai.plus/v1"
        conf_list[0]["api_key"]="sk-tqPuK5wogqjQ8fodD044AcDbF50845449f94A62aB16f96A8"
        conf_list[0]["temperature"]=temperature
        ret={"config_list": conf_list, "cache_seed":None}
    else:
        conf_list[0]["api_type"]= "together"
        conf_list[0]["api_key"]=os.environ["TOGETHER_API_KEY"]
        ret={"config_list": conf_list, "cache_seed":None, "temperature": temperature}
    return ret 

def random_split(items, size):
    sample = set(random.sample(items, size))
    return sorted(sample), sorted(set(items) - sample)



def get_eval_prompt(focus, task, lean, j, cot):
    formatter="""Output their names in a JSON object: \{names\:[]\}."""
    if focus=="self":
        return eval_prompt["_".join([focus, task, lean])].format(topic)+formatter
    else:
        return eval_prompt["_".join([focus, task])]


filename_base="_".join(map(str,[prefix, os.path.basename(model_name), lean, task, focus, temperature, topic, demographics.replace(" ", "_"), cot]))

def create_agent(name):
    return AssistantAgent(
        name=name,
        system_message=get_demographics(name),
        llm_config=get_model(),
    )  

logging_session_id = autogen.runtime_logging.start(config={"dbname": "data/"+filename_base+".db"})
print("Logging session ID: " + str(logging_session_id))

for it in range(iteration):
    names=["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]
    group1, group2=random_split(names, 4)

    def get_demographics(name):
        groups=[{"name": "Group 1", "members": group1}, {"name": "Group 2", "members": group2}]
        group={}
        other={}
        for g in groups:
            if name in g["members"]:
                group=g
            else:
                other=g

        k=random.randint(0, 1)
        b0="""Your name is "{0}". {1}There are two groups. """
        b1="You are in {2} that includes four group members: {3}. " 
        b2="{5} includes four members, {4}. " 
        b3="When providing your input: Speak only on your own behalf. Keep your response concise."
        base=b0+b1+b2+b3 if k==1 else b0+b2+b1+b3

        if demographics=="None":
            return base.format(name, "", group["name"], ", ".join(group["members"]), ", ".join(other["members"]), other["name"])
        return base.format(name, "You are "+demographics+". ", group["name"], ", ".join(group["members"]), ", ".join(other["members"]), other["name"])



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

    # task_chat_result=initializer.initiate_chat(managerPlay, message=task_prompt[topic], cache=None)

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
            # carryover=managerPlay.messages_to_string(task_chat_result.chat_history)
        )
        friends=group1 if names[j] in group1 else group2

        save_to_csv_7(eval_chat_result.chat_history[-1]["content"], names[j], friends, filename_base+".csv")

autogen.runtime_logging.stop()