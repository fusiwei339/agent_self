import os
# all parameters
# lean=["positive"] 
# temperature=1
# focus="next" 
# task="percent" 
# model="gpt-4o"
# gender="None" 
# iteration=20 

# evaluate different models
lean="neutral" 
temperature=1
focus="self" 
task="percent" 
model=["gpt-4o", "gpt-4-0613", "gpt-3.5-turbo-0125"]
gender="None" 

iteration=50

for m in model:
    os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={}".format(lean,m,focus,task,iteration,temperature))
