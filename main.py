import os
import pathlib
from analysis import * 
# all parameters
# lean=["positive"] 
# temperature=1
# focus="next" # next, self, group
# task="percent" 
# model="gpt-4o"
# gender="None" 
# iteration=20 

def baseline(iteration=50, lean="neutral", temperature=0.7, focus="self", task="percent", model="gpt-4o", demographics="None", append=True, topic="joke"):
    filename_base="_".join(map(str,[os.path.basename(model), lean, task, focus, temperature, topic, demographics]))
    if(not append):
        pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+".db").unlink(missing_ok=True)

    os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --topic={} --demographics={}".format(lean,model,focus,task,iteration, temperature, topic, demographics))

    return filename_base+".csv"

def other_percent(iteration=50, lean="neutral", temperature=0.7, focus="other", task="percent", model="gpt-4o", demographics="None", append=True):
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

def models(iteration=50, lean="neutral", temperature=0.7, focus="group", task="percent", 
           model=[
               "gpt-4-1106-preview", 
               "gpt-3.5-turbo-0125", 
            #    "meta-llama/Llama-3-70b-chat-hf", 
            # "meta-llama/Meta-Llama-3-8B-Instruct-Turbo",
            #    "meta-llama/Llama-2-70b-chat-hf"
               ], 
           demographics="None", append=True):

    for m in model:
        filename_base="_".join(map(str,[os.path.basename(m), lean, task, focus, temperature, demographics]))
        if(not append):
            pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
            pathlib.Path(filename_base+".db").unlink(missing_ok=True)
            pathlib.Path(filename_base+".json").unlink(missing_ok=True)

        os.system("python3 /Users/siwei/repos/agent_self/percentage.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,m,focus,task,iteration,temperature, demographics))

def gptmix(iteration=50, lean="neutral", temperature=0.7, focus="self", task="percent", 
           model="gptmix", demographics="None", append=True):

    filename_base="_".join(map(str,[model, lean, task, focus, temperature, demographics]))
    if(not append):
        pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+"_questionnaire"+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+".db").unlink(missing_ok=True)

    os.system("python3 /Users/siwei/repos/agent_self/ind_agents.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))



os.system('clear')
# baseline(iteration=0, append=True, topic="joke")
# baseline(iteration=50, append=True, topic="poem")
# baseline(iteration=15, append=True, topic="joke", focus="group", task="rank")

# group_percent(iteration=15, append=True)
# group_percent(iteration=7, append=True, model= "gpt-4-1106-preview")
# group_percent(iteration=11, append=True, model= "gpt-3.5-turbo-0125")

# models(iteration=15, append=True)
# other_percent(iteration=15)

# self_percent_pos_file=self_percent_pos(iteration=35, append=False)
# self_percent_neg_file=self_percent_neg(iteration=35, append=False)

# diff_demographics(iteration=35, append=True)

# temperatures(iteration=15, append=True)
# temperatures(iteration=9, append=True, temperature=[1.4])

# gptmix(iteration=15, append=True)




print("\n\n\n========== Baseline joke =========\n")
analyze_self_percent_1samp("gpt-4o_neutral_percent_self_0.7_None.csv")
reformat_json("gpt-4o_neutral_percent_self_0.7_None.csv")

print("\n\n\n========== Baseline poem =========\n")
analyze_self_percent_1samp("gpt-4o_neutral_percent_self_0.7_poem_None.csv")
reformat_json("gpt-4o_neutral_percent_self_0.7_poem_None.csv")

print("\n\n\n========== Group Rank =========\n")
analyze_group_rank("gpt-4o_neutral_rank_group_0.7_None.csv")

print("\n\n\n========== Other focus =========\n")
error_handler("gpt-4o_neutral_percent_group_0.7_None.csv")
analyze_group_percent("gpt-4o_neutral_percent_group_0.7_None.csv")
reformat_json("gpt-4o_neutral_percent_group_0.7_None.csv")

print("\n\n\n========== GPT-4 Other focus =========\n")
error_handler("gpt-4-1106-preview_neutral_percent_group_0.7_joke_None.csv")
analyze_group_percent("gpt-4-1106-preview_neutral_percent_group_0.7_joke_None.csv")
cal_group_sum("gpt-4-1106-preview_neutral_percent_group_0.7_joke_None.csv")

print("\n\n\n========== GPT-3.5 Other focus =========\n")
error_handler("gpt-3.5-turbo-0125_neutral_percent_group_0.7_joke_None.csv")
analyze_group_percent("gpt-3.5-turbo-0125_neutral_percent_group_0.7_joke_None.csv")
cal_group_sum("gpt-3.5-turbo-0125_neutral_percent_group_0.7_joke_None.csv")

# print("\n\n\n========== Llama 2 Group Percent =========\n")
# cal_group_sum("Llama-2-70b-chat-hf_neutral_percent_group_0.7_joke_None.csv")
# analyze_other_percent_1samp("gpt-4o_neutral_percent_group_0.7_None.csv")

print("\n\n\n========== Compare Self & Group Percent =========\n")
analyze_self_percent_ind("gpt-4o_neutral_percent_self_0.7_None.csv", "gpt-4o_neutral_percent_group_0.7_None.csv")

print("\n\n\n========== Pos and Neg =========\n")
analyze_self_percent_ind("gpt-4o_positive_percent_self_0.7_None.csv", "gpt-4o_negative_percent_self_0.7_None.csv")
reformat_json("gpt-4o_negative_percent_self_0.7_None.csv")
reformat_json("gpt-4o_positive_percent_self_0.7_None.csv")

print("\n\n\n========== American =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.7_an_American.csv')
reformat_json('gpt-4o_neutral_percent_self_0.7_an_American.csv')

print("\n\n\n========== Asian American =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.7_an_Asian_American.csv')
reformat_json('gpt-4o_neutral_percent_self_0.7_an_Asian_American.csv')

print("\n\n\n========== African American =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.7_an_African_American.csv')
reformat_json('gpt-4o_neutral_percent_self_0.7_an_African_American.csv')

print("\n\n\n========== Female =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.7_female.csv')
reformat_json('gpt-4o_neutral_percent_self_0.7_female.csv')

print("\n\n\n========== Male =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.7_male.csv')
reformat_json('gpt-4o_neutral_percent_self_0.7_male.csv')


print("\n\n\n========== Temperature=0 =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.0_None.csv')
reformat_json('gpt-4o_neutral_percent_self_0.0_None.csv')

print("\n\n\n========== Temperature=1.4 =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_1.4_None.csv')
reformat_json('gpt-4o_neutral_percent_self_1.4_None.csv')

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
reformat_json('gpt-3.5-turbo-0125_neutral_percent_self_0.7_None.csv')

print("\n\n\n========== gpt-4-1106-preview =========\n")
analyze_self_percent_1samp('gpt-4-1106-preview_neutral_percent_self_0.7_None.csv')
reformat_json('gpt-4-1106-preview_neutral_percent_self_0.7_None.csv')

print("\n\n\n========== gpt-4o =========\n")
analyze_self_percent_1samp('gpt-4o_neutral_percent_self_0.7_None.csv')
reformat_json('gpt-4o_neutral_percent_self_0.7_None.csv')


print("\n\n\n========== Compare GPT 4.0 & GPT 4o =========\n")
analyze_self_percent_ind("gpt-4o_neutral_percent_self_0.7_None.csv", "gpt-4-1106-preview_neutral_percent_self_0.7_None.csv")

print("\n\n\n========== Next team member=========\n")
analyze_next_percent_1samp("gpt-4o_neutral_percent_other_0.7_None.csv")

print("\n\n\n========== Independent Agent Models =========\n")
error_handler("gptmix_neutral_percent_self_0.7_None.csv")
gptmix_stat("gptmix_neutral_percent_self_0.7_None.csv")
gptmix_reformat_json("gptmix_neutral_percent_self_0.7_None.csv")
# gptmix_ques("revised_gptmix_neutral_percent_self_0.7_None_questionnaire.csv", "revised_gptmix_neutral_percent_self_0.7_None.csv")