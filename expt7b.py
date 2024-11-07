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
parser.add_argument("--demographics", type=str, default="None")
parser.add_argument("--prefix", type=str, default="")
parser.add_argument("--cot", type=str_to_bool, default=False)
parser.add_argument("--topic", type=str, default="joke")
args = parser.parse_args()

model= args.model
lean = args.lean
task = args.task
focus = args.focus
topic = args.topic
prefix = args.prefix
iteration = args.iteration
temperature=args.temperature
demographics =args.demographics
cot=args.cot

openai_model={
    "config_list": [{
        "base_url":"https://xiaoai.plus/v1",
        "api_key":"sk-tqPuK5wogqjQ8fodD044AcDbF50845449f94A62aB16f96A8",
        "temperature":temperature,
        "model":"gpt-4o", 
    }], 
    "cache_seed":None
}

sensechat_model={
   "config_list": [{
        "base_url":"https://api.sensenova.cn/compatible-mode/v1/",
        "api_key":"""eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI0QTNFRTE0NUExRDY0Mzc0QUZCNkVFMDQ2M0E4MEIyNSIsImV4cCI6MTczMTAxNTg0MiwibmJmIjoxNzMwOTQ1NjM3LCJpYXQiOjE3MzA5NDU2NDJ9.2Sk7PSG81M6BEXL_G5qtlr_B4uRh2EMqTdzXrbHvRb0""",
        "temperature":temperature,
        "model":"SenseChat-5", 
    }], 
    "cache_seed":None 
}

qwen_model={
   "config_list": [{
        "base_url":"https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key":"sk-839b03350d844cfc90f503ad3c0936e6",
        "temperature":temperature,
        "model":"qwen-max", 
    }], 
    "cache_seed":None 
}

llama_model={
    "config_list": [{
        "model":"meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
        "api_key":"794de0b246a52737a9956e719bc1ddd071d04b66cd346e31c951cc1cf1800b68",
        "api_type": "together"
    }], 
    "cache_seed":None, 
}

# llama_model={
#     "config_list": [{
#         "model":"llama_3_70b",
#         "api_key":"sk-key",
#         "base_url":"http://localhost:9090/v1",
#         "temperature": temperature
#     }], 
#     "cache_seed":None, 
# }

intro_obj={
    "llama": "model is Llama, which is created by an American company, Meta. ",
    "qwen": "model is Qwen, which is created by a Chinese company, Alibaba. ",
    "openai": "model is GPT-4o, which is created by an American company, OpenAI. ",
    "sensechat": "model is SenseChat, which is created by a Chinese company, SenseTime. ",
}

models_obj={
    "llama":llama_model,
    "sensechat":sensechat_model,
    "qwen":qwen_model,
    "openai":openai_model
}

def get_eval_prompt(focus, task, lean, j):
    if focus=="self":
        return eval_prompt["_".join([focus, task, lean])]
    elif focus=="other":
        return eval_prompt["_".join([focus, task])](j)
    else:
        return eval_prompt["_".join([focus, task])]

for it in range(iteration):

    names=["One", "Two", "Three", "Four"]
    models=["openai", "qwen", "llama", "sensechat"]
    np.random.shuffle(models)
    print(models)

    def get_model_info(name):
        ret=""
        prefix=""
        for n in names:
            if n==name:
                prefix="Your "
            else:
                prefix=n+"'s "
            ret+=(prefix+intro_obj[models[names.index(n)]])
        return ret


    def get_demographics(name):

        base="""Your name is "{0}". You are part of a group that includes "One", "Two", "Three", and "Four". 
        When providing your input: Speak only on your own behalf. Keep your response concise."""
        return base.format(name)

    filename_base="_".join(map(str,[prefix, os.path.basename(model), lean, task, focus, temperature, topic, demographics, cot]))

    logging_session_id = autogen.runtime_logging.start(config={"dbname": "data/"+filename_base+".db"})
    print("Logging session ID: " + str(logging_session_id))

    def create_agent(name):
        return AssistantAgent(
            name=name,
            system_message=get_demographics(name),
            llm_config=models_obj[models[names.index(name)]]
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
        llm_config=openai_model
    )

    # task_chat_result=initializer.initiate_chat(managerPlay, message="Introduce yourself briefly.", cache=None)

    initializer2 = UserProxyAgent(
        name="init2",
        code_execution_config=False,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
    )

    for j in range(len(names)):
        eval_chat_result=initializer2.initiate_chat(
            agents[j], 
            message=get_model_info(names[j])+get_eval_prompt(focus, task, lean, j),
            # carryover=managerPlay.messages_to_string(task_chat_result.chat_history)
        )

        save_to_csv_mix(eval_chat_result.chat_history[-1]["content"], names[j], filename_base+".csv", models[names.index(names[j])], it)

    autogen.runtime_logging.stop()