import os
lean="positive"
temperature=1
focus="self"
task="percent"
iteration=2
model="gpt-4o"

os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={lean} --temperature={temperature} --model={model} --focus={focus} --task={task} --iteration={iteration}")