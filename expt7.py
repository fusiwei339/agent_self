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
groups=[{"name": "Group 1", "members": ["One", "Two", "Three", "Four"]}, {"name": "Group 2", "members": ["Five", "Six", "Seven", "Eight"]}]

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


def get_demographics(name):
    group={}
    other={}
    for g in groups:
        if name in g["members"]:
            group=g
        else:
            other=g

    base="""Your name is "{0}". {1}There are two groups. You are in {2} that includes four group members: {3}. And other four members, {4} are in {5}. When providing your input: Speak only on your own behalf. Keep your response concise."""
    if demographics=="None":
        return base.format(name, "", group["name"], ", ".join(group["members"]), ", ".join(other["members"]), other["name"])
    return base.format(name, "You are "+demographics+". ", group["name"], ", ".join(group["members"]), ", ".join(other["members"]), other["name"])


def get_eval_prompt(focus, task, lean, j, cot):
    formatter="""Output their names in a JSON object: \{names\:[]\}."""
    if focus=="self":
        return eval_prompt["_".join([focus, task, lean])].format(topic)+formatter
    else:
        return eval_prompt["_".join([focus, task])]


names=["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]
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


    initializer = UserProxyAgent(
        name="init",
        human_input_mode="NEVER",
        code_execution_config=False,
    )

    group1=[create_agent(i) for i in groups[0]["members"]]
    group2=[create_agent(i) for i in groups[1]["members"]]

    groupchatPlay1 = autogen.GroupChat(
        agents=[initializer]+group1,
        messages=[],
        max_round=4+1,
        speaker_selection_method="round_robin",
        # send_introductions=True,
    )
    managerPlay1 = autogen.GroupChatManager(
        name="play manager1",
        groupchat=groupchatPlay1, 
        llm_config=get_model()
    )

    groupchatPlay2 = autogen.GroupChat(
        agents=[initializer]+group2,
        messages=[],
        max_round=4+1,
        speaker_selection_method="round_robin",
        # send_introductions=True,
    )
    managerPlay2 = autogen.GroupChatManager(
        name="play manager2",
        groupchat=groupchatPlay2, 
        llm_config=get_model()
    )
    task_chat_result1=initializer.initiate_chat(managerPlay1, message=task_prompt[topic], cache=None)
    task_chat_result2=initializer.initiate_chat(managerPlay2, message=task_prompt[topic], cache=None)

    initializer2 = UserProxyAgent(
        name="init2",
        code_execution_config=False,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
    )

    agentGroups=group1+group2
    for j in range(len(names)):
        eval_chat_result=initializer2.initiate_chat(
            agentGroups[j], 
            message=get_eval_prompt(focus, task, lean, j, cot),
            carryover=managerPlay1.messages_to_string(task_chat_result1.chat_history if j<4 else task_chat_result2.chat_history)
        )

        save_to_csv_7(eval_chat_result.chat_history[-1]["content"], names[j], filename_base+".csv")

autogen.runtime_logging.stop()