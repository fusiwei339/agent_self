import os
# all parameters
# lean=["positive"] 
# temperature=1
# focus="next" 
# task="percent" 
# model="gpt-4o"
# gender="None" 
# iteration=20 

# evaluate other agents 
lean="neutral" 
temperature=1
focus="group" 
task="percent" 
model="gpt-4o"
gender="None" 

iteration=20 
os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={}".format(lean,model,focus,task,iteration,temperature))
