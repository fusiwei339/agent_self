import os
import pathlib
from analysis import analyze_self_percent_1samp, analyze_self_percent_ind, analyze_group_rank, analyze_group_percent,error_handler, analyze_other_percent_1samp, oneway_anova
# all parameters
# lean=["positive"] 
# temperature=1
# focus="next" # next, self, group
# task="percent" 
# model="gpt-4o"
# gender="None" 
# iteration=20 

def baseline(iteration=50, lean="neutral", temperature=0.7, focus="self", task="percent", model="gpt-4o", demographics="None", append=True):
    filename_base="_".join(map(str,[os.path.basename(model), lean, task, focus, temperature, demographics]))
    if(not append):
        pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+".db").unlink(missing_ok=True)

    os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))

    return filename_base+".csv"

def group_rank(iteration=50, lean="neutral", temperature=0.7, focus="group", task="rank", model="gpt-4o", demographics="None", append=True):
    filename_base="_".join(map(str,[os.path.basename(model), lean, task, focus, temperature, demographics]))
    if(not append):
        pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+".db").unlink(missing_ok=True)

    os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))

    return filename_base+".csv"

def group_percent(iteration=50, lean="neutral", temperature=0.7, focus="group", task="percent", model="gpt-4o", demographics="None", append=True):
    filename_base="_".join(map(str,[os.path.basename(model), lean, task, focus, temperature, demographics]))
    if(not append):
        pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+".db").unlink(missing_ok=True)

    os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))

    return filename_base+".csv"

def self_percent_pos(iteration=50, lean="positive", temperature=0.7, focus="self", task="percent", model="gpt-4o", demographics="None", append=True):
    filename_base="_".join(map(str,[os.path.basename(model), lean, task, focus, temperature, demographics]))
    if(not append):
        pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+".db").unlink(missing_ok=True)

    os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))

    return filename_base+".csv"

def self_percent_neg(iteration=50, lean="negative", temperature=0.7, focus="self", task="percent", model="gpt-4o", demographics="None", append=True):
    filename_base="_".join(map(str,[os.path.basename(model), lean, task, focus, temperature, demographics]))
    if(not append):
        pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+".db").unlink(missing_ok=True)

    os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))

    return filename_base+".csv"

def diff_demographics(iteration=50, lean="neutral", 
                      temperature=0.7, focus="self", task="percent", model="gpt-4o", 
                      demographics=[
                        #   "a male", 
                        #   "a female", 
                          "an American", 
                          "an Asian American", 
                          "an African American"
                      ], 
                      append=True):

    for d in demographics:
        filename_base="_".join(map(str,[os.path.basename(model), lean, task, focus, temperature, d.replace(' ', "_")]))
        if(not append):
            pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
            pathlib.Path(filename_base+".db").unlink(missing_ok=True)

        os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics='{}'".format(lean,model,focus,task,iteration,temperature, d))

def temperatures(iteration=50, lean="neutral", 
                 temperature=[0, 2], 
                 focus="self", task="percent", model="gpt-4o", demographics="None", append=True):

    for t in temperature:
        filename_base="_".join(map(str,[os.path.basename(model), lean, task, focus, t, demographics]))
        if(not append):
            pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
            pathlib.Path(filename_base+".db").unlink(missing_ok=True)

        os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,t, demographics))

def models(iteration=50, lean="neutral", temperature=0.7, focus="self", task="percent", 
           model=[
            #    "gpt-4-1106-preview", 
            #    "gpt-3.5-turbo-0125", 
            #    "meta-llama/Llama-3-70b-chat-hf", 
            # "meta-llama/Meta-Llama-3-8B-Instruct-Turbo",
               "meta-llama/Llama-2-70b-chat-hf"
               ], 
        #    model=["gpt-4o", "gpt-4-1106-preview", "gpt-3.5-turbo-0125", "meta-llama/Llama-3-70b-chat-hf", "meta-llama/Llama-2-70b-chat-hf"], 
           demographics="None", append=True):

    for m in model:
        filename_base="_".join(map(str,[os.path.basename(m), lean, task, focus, temperature, demographics]))
        if(not append):
            pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
            pathlib.Path(filename_base+".db").unlink(missing_ok=True)

        os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,m,focus,task,iteration,temperature, demographics))




# baseline_file=baseline(iteration=0, append=True)
# group_rank_file=group_rank(iteration=0, append=True)

# group_percent_file=group_percent(iteration=15, append=True)

# models(iteration=50, append=False)

# self_percent_pos_file=self_percent_pos(iteration=35, append=False)
# self_percent_neg_file=self_percent_neg(iteration=35, append=False)

diff_demographics(iteration=35, append=True)

# temperatures(iteration=15, append=True)
# temperatures(iteration=9, append=True, temperature=[1.4])

print("\n\n\n========== Baseline =========\n")
analyze_self_percent_1samp("gpt-4o_neutral_percent_self_0.7_None.csv")
print("\n\n\n========== Group Rank =========\n")
analyze_group_rank("gpt-4o_neutral_rank_group_0.7_None.csv")

print("\n\n\n========== Group Percent =========\n")
analyze_group_percent("gpt-4o_neutral_percent_group_0.7_None.csv")
analyze_other_percent_1samp("gpt-4o_neutral_percent_group_0.7_None.csv")

print("\n\n\n========== Pos and Neg =========\n")
analyze_self_percent_ind("gpt-4o_positive_percent_self_0.7_None.csv", "gpt-4o_negative_percent_self_0.7_None.csv")

print("\n\n\n========== American =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.7_an_American.csv')
print("\n\n\n========== Asian American =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.7_an_Asian_American.csv')
print("\n\n\n========== African American =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.7_an_African_American.csv')
print("\n\n\n========== Female =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.7_female.csv')
print("\n\n\n========== Male =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.7_male.csv')


print("\n\n\n========== Temperature=0 =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.0_None.csv')
print("\n\n\n========== Temperature=1.4 =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_1.4_None.csv')
print("\n\n\n========== one way anova =========\n")
oneway_anova('gpt-4o_neutral_percent_self_0.0_None.csv','gpt-4o_neutral_percent_self_0.7_None.csv','gpt-4o_neutral_percent_self_1.4_None.csv')

print("\n\n\n========== LLAMA-3-8b =========\n")
analyze_self_percent_1samp('Meta-Llama-3-8B-Instruct-Turbo_neutral_percent_self_0.7_None.csv')
print("\n\n\n========== LLAMA-2-70b =========\n")
analyze_self_percent_1samp('Llama-2-70b-chat-hf_neutral_percent_self_0.7_None.csv')
print("\n\n\n========== LLAMA-3-70b =========\n")
analyze_self_percent_1samp('Llama-3-70b-chat-hf_neutral_percent_self_0.7_None.csv')
print("\n\n\n========== gpt-3.5-turbo-0125 =========\n")
analyze_self_percent_1samp('gpt-3.5-turbo-0125_neutral_percent_self_0.7_None.csv')
print("\n\n\n========== gpt-4-1106-preview =========\n")
analyze_self_percent_1samp('gpt-4-1106-preview_neutral_percent_self_0.7_None.csv')
print("\n\n\n========== gpt-4o =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.7_None.csv')