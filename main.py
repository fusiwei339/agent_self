import os
# all parameters
# lean=["positive"] 
# temperature=1
# focus="next" # next, self, group
# task="percent" 
# model="gpt-4o"
# gender="None" 
# iteration=20 

def baseline():
    # self percent
    lean="neutral" 
    temperature=0.7
    focus="self" 
    task="percent" 
    model="gpt-4o"
    demographics="None" # a male, a female, a Chinese, an American, an Indian

    iteration=50

    os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))

def group_rank():
    lean="neutral" 
    temperature=0.7
    focus="group" 
    task="rank" 
    model="gpt-4o"
    demographics="None" # a male, a female, a Chinese, an American, an Indian

    iteration=50

    os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))

def group_percent():
    lean="neutral" 
    temperature=1
    focus="group" 
    task="percent" 
    model="gpt-4o"
    demographics="None" # a male, a female, a Chinese, an American, an Indian

    iteration=50

    os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))


def self_percent_pos():
    lean="positive" 
    temperature=0.7
    focus="self" 
    task="percent" 
    model="gpt-4o"
    demographics="None" # a male, a female, a Chinese, an American, an Indian

    iteration=50

    os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))


def self_percent_neg():
    lean="negative" 
    temperature=0.7
    focus="self" 
    task="percent" 
    model="gpt-4o"
    demographics="None" # a male, a female, a Chinese, an American, an Indian

    iteration=50

    os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))

def gender():
    lean="neutral" 
    temperature=1
    focus="self" 
    task="percent" 
    model="gpt-4o"
    demographics=["a male", "a female"] # a male, a female, a Chinese, an American, an Indian

    iteration=50

    for d in demographics:
        os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics='{}'".format(lean,model,focus,task,iteration,temperature, d))

def nationality():
    lean="neutral" 
    temperature=1
    focus="self" 
    task="percent" 
    model="gpt-4o"
    demographics=["a Chinese", "an American", "an Indian"] # a male, a female, a Chinese, an American, an Indian

    iteration=50

    for d in demographics:
        os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics='{}'".format(lean,model,focus,task,iteration,temperature, d))

def temperatures():
    lean="neutral" 
    temperature=[0, 2]
    focus="self" 
    task="percent" 
    model="gpt-4o"
    demographics="None" # a male, a female, a Chinese, an American, an Indian

    iteration=50

    for t in temperature:
        os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,t, demographics))

def models():
    lean="neutral" 
    temperature=1
    focus="self" 
    task="percent" 
    model=["gpt-4o", "gpt-4-1106-preview", "gpt-3.5-turbo-0125", "Llama-3-70b-chat-hf", "Llama-2-70b-chat-hf"]
    demographics="None" # a male, a female, a Chinese, an American, an Indian

    iteration=50

    for m in model:
        os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,m,focus,task,iteration,temperature, demographics))



baseline()
group_rank()
# group_percent()
self_percent_neg()
self_percent_pos()
# gender()
# nationality()
# temperatures()
# models()
