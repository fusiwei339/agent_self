import os
lean="positive" # 正面贡献、负面贡献
temperature=1
focus="self" # 只估计自己、先估计别人再估计自己
task="percent" # percent or rank
model="gpt-4o"
gender="None" # male, female, None

iteration=2 #


os.system("python3 /Users/siwei/repo/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={}".format(lean,model,focus,task,iteration,temperature))