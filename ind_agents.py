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

default_model={"config_list": [{
                "base_url":"https://api.chatanywhere.com.cn",
                "api_key":"sk-CUIdUOkG7Xl3lRF2Lfg4YULUew1dRRy3cLtjNB29vtwXpsGR",
                "temperature":temperature,
                "model":"gpt-4o", 
            }], "cache_seed":None}

def get_demographics(name):
    base="""Your name is "{0}". {1}You are part of a group that includes "One", "Two", "Three", "Four" and "Five". When providing your input: Speak only on your own behalf. Keep your response concise."""
    if demographics=="None":
        return base.format(name, "")
    return base.format(name, "You are "+demographics+". ")


def get_eval_prompt(focus, task, lean, j):
    if focus=="self":
        return eval_prompt["_".join([focus, task, lean])]
    elif focus=="other":
        return eval_prompt["_".join([focus, task])](j)
    else:
        return eval_prompt["_".join([focus, task])]



for it in range(iteration):

    names=["One", "Two", "Three", "Four", "Five"]
    models=["gpt-4o", "gpt-3.5-turbo-1106", "gpt-4-turbo-preview", "gpt-4-0613", "gpt-3.5-turbo"]
    np.random.shuffle(models)

    model_obj={}
    for i in range(5):
        model_obj[names[i]]=models[i]

    filename_base="_".join(map(str,[os.path.basename(model_name), lean, task, focus, temperature, demographics.replace(" ", "_")]))

    logging_session_id = autogen.runtime_logging.start(config={"dbname": filename_base+".db"})
    print("Logging session ID: " + str(logging_session_id))

    def create_agent(name):
        return AssistantAgent(
            name=name,
            system_message=get_demographics(name),
            llm_config={"config_list": [{
                "base_url":"https://api.chatanywhere.com.cn",
                "api_key":"sk-CUIdUOkG7Xl3lRF2Lfg4YULUew1dRRy3cLtjNB29vtwXpsGR",
                "temperature":temperature,
                "model":model_obj[name], 
            }], "cache_seed":None}
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
        llm_config=default_model
    )

    task_chat_result=initializer.initiate_chat(managerPlay, message=task_prompt["joke"], cache=None)

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

        save_to_csv_gptmix(eval_chat_result.chat_history[-1]["content"], names[j], filename_base+".csv", model_obj[names[j]], it)

        # questions=task_prompt["questionnaire_Q"]
        # instruction=task_prompt["questionnaire_instruct"]
        # for q in questions:
        #     q_result=initializer2.initiate_chat(
        #         agents[j],
        #         message=instruction+q
        #     )
        #     save_to_csv_gptmix(q_result.chat_history[-1]["content"], names[j], filename_base+"_questionnaire"+".csv", model_obj[names[j]],it)
        
    autogen.runtime_logging.stop()