import os

lean="positive"
temperature=1
focus="self"
task="percent"
iteration=2
model="gpt-4o"


os.system("python3 /Users/siwei/repo/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={}".format(lean,model,focus,task,iteration,temperature))