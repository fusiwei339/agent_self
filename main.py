import os
import shutil
import pathlib
from analysis import * 

# fullpath="/Users/siwei/repos/agent_self/"
fullpath=""

def baseline(iteration=50, lean="neutral", temperature=0.7, focus="self", task="percent", model="gpt-4o", demographics="None", append=True, topic="joke", cot=False):
    filename_base="_".join(map(str,[os.path.basename(model), lean, task, focus, temperature, topic, demographics, cot]))
    print(filename_base)
    if(not append):
        pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+".db").unlink(missing_ok=True)

    os.system("python3 "+fullpath+"expt.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --topic={} --demographics={} --cot={}".format(lean,model,focus,task,iteration, temperature, topic, demographics, cot))

    return filename_base+".csv"

def other_percent(iteration=50, lean="neutral", temperature=0.7, focus="other", task="percent", model="gpt-4o", demographics="None", append=True):
    filename_base="_".join(map(str,[os.path.basename(model), lean, task, focus, temperature, demographics]))
    if(not append):
        pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+".db").unlink(missing_ok=True)

    os.system("python3 "+fullpath+"expt.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))

    return filename_base+".csv"

def group_percent(iteration=50, lean="neutral", temperature=0.7, focus="group", task="percent", model="gpt-4o", demographics="None", append=True):
    filename_base="_".join(map(str,[os.path.basename(model), lean, task, focus, temperature, demographics]))
    if(not append):
        pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+".db").unlink(missing_ok=True)

    os.system("python3 "+fullpath+"expt.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))

    return filename_base+".csv"

def diff_demographics(iteration=50, lean="neutral", 
                      temperature=0.7, focus="self", task="percent", model="gpt-4o", 
                      demographics=[
                          "a male", 
                          "a female", 
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

        os.system("python3 "+fullpath+"expt.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics='{}'".format(lean,model,focus,task,iteration,temperature, d))

def temperatures(iteration=50, lean="neutral", 
                 temperature=[0.7, 1.4], 
                 focus="self", task="percent", model="gpt-4o", demographics="None", append=True):

    for t in temperature:
        filename_base="_".join(map(str,[os.path.basename(model), lean, task, focus, t, demographics]))
        if(not append):
            pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
            pathlib.Path(filename_base+".db").unlink(missing_ok=True)

        os.system("python3 "+fullpath+"expt.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,t, demographics))

def models(iteration=50, lean="neutral", temperature=0.7, focus="group", task="percent", 
           model=[
               "gpt-4-1106-preview", 
               "gpt-3.5-turbo-0125", 
               ], 
           demographics="None", topic="joke", append=True):

    for m in model:
        filename_base="_".join(map(str,[os.path.basename(m), lean, task, focus, temperature, demographics]))
        if(not append):
            pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
            pathlib.Path(filename_base+".db").unlink(missing_ok=True)
            pathlib.Path(filename_base+".json").unlink(missing_ok=True)

        os.system("python3 "+fullpath+"expt.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={} --topic={}".format(lean,m,focus,task,iteration,temperature, demographics, topic))

def gptmix(iteration=50, lean="neutral", temperature=0.7, focus="self", task="percent", model="gptmix", demographics="None", append=True):

    filename_base="_".join(map(str,[model, lean, task, focus, temperature, demographics]))
    if(not append):
        pathlib.Path(filename_base+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+"_questionnaire"+".csv").unlink(missing_ok=True)
        pathlib.Path(filename_base+".db").unlink(missing_ok=True)

    os.system("python3 "+fullpath+"expt5b.py --lean={} --model={} --focus={} --task={} --iteration={} --temperature={} --demographics={}".format(lean,model,focus,task,iteration,temperature, demographics))



os.system('clear')

# Expt 1a
# baseline(iteration=50, topic="joke") # run your own experiment
print("\n\n\n========== Baseline joke =========\n")
analyze_self_percent_1samp("data/gpt-4o_neutral_percent_self_0.7_None.csv")

# Expt 1b
# baseline(iteration=50, topic="poem") # run your own experiment
print("\n\n\n========== Baseline poem =========\n")
analyze_self_percent_1samp("data/gpt-4o_neutral_percent_self_0.7_poem_None.csv")

# Expt 2a
# group_percent(iteration=50, append=True) # run your own experiment
print("\n\n\n========== Other focus =========\n")
error_handler("data/gpt-4o_neutral_percent_group_0.7_None.csv")
analyze_group_percent("data/gpt-4o_neutral_percent_group_0.7_None.csv")
analyze_other_percent_1samp("data/gpt-4o_neutral_percent_group_0.7_None.csv")
print("\n\n\n========== Compare Self & Group Percent =========\n")
analyze_self_percent_ind("data/gpt-4o_neutral_percent_self_0.7_None.csv", "data/gpt-4o_neutral_percent_group_0.7_None.csv")

# Expt 2b
# baseline(iteration=50, append=True, focus="group", task="rank") # run your own experiment
print("\n\n\n========== Other focus: Rank =========\n")
analyze_group_rank("data/gpt-4o_neutral_rank_group_0.7_joke_None_False.csv")

# Expt 3
# baseline(iteration=50, append=True, lean="positive") # run your own experiment
# baseline(iteration=50, append=True, lean="negative") # run your own experiment
print("\n\n\n========== joke Pos =========\n")
analyze_self_percent_1samp("data/gpt-4o_positive_percent_self_0.7_joke_None_False.csv")
print("\n\n\n========== joke Neg =========\n")
analyze_self_percent_1samp("data/gpt-4o_negative_percent_self_0.7_joke_None_False.csv")
print("\n\n\n===== compare Pos and Neg revised =====\n")
analyze_self_percent_ind("data/gpt-4o_positive_percent_self_0.7_joke_None_False.csv", "data/gpt-4o_negative_percent_self_0.7_joke_None_False.csv")

# Expt 4a
# temperatures(iteration=50, append=True) # run your own experiment
print("\n\n\n========== Temperature=0 =========\n")
analyze_self_percent_1samp('data/gpt-4o_neutral_percent_self_0.0_None.csv')
print("\n\n\n========== Temperature=1.4 =========\n")
analyze_self_percent_1samp('data/gpt-4o_neutral_percent_self_1.4_None.csv')
print("\n\n\n========== anova of three temperatures =========\n")
oneway_anova('data/gpt-4o_neutral_percent_self_0.0_None.csv','data/gpt-4o_neutral_percent_self_0.7_None.csv','data/gpt-4o_neutral_percent_self_1.4_None.csv')

# Expt 4b
# diff_demographics(iteration=50, append=True) # run your own experiment
print("\n\n\n========== American =========\n")
analyze_self_percent_1samp('data/gpt-4o_neutral_percent_self_0.7_joke_an_American_False.csv')
print("\n\n\n========== Asian American =========\n")
analyze_self_percent_1samp('data/gpt-4o_neutral_percent_self_0.7_joke_an_Asian_American_False.csv')
print("\n\n\n========== African American =========\n")
analyze_self_percent_1samp('data/gpt-4o_neutral_percent_self_0.7_joke_an_African_American_False.csv')
print("\n\n\n========== Female =========\n")
analyze_self_percent_1samp('data/gpt-4o_neutral_percent_self_0.7_female.csv')
print("\n\n\n========== Male =========\n")
analyze_self_percent_1samp('data/gpt-4o_neutral_percent_self_0.7_male.csv')

# Expt 5a
# models(iteration=50, append=True) # run your own experiment
print("\n\n\n========== gpt-3.5-turbo-0125 =========\n")
analyze_self_percent_1samp('data/gpt-3.5-turbo-0125_neutral_percent_self_0.7_None.csv')
print("\n\n\n========== gpt-4-1106-preview =========\n")
analyze_self_percent_1samp('data/gpt-4-1106-preview_neutral_percent_self_0.7_None.csv')

# Expt 5b
# gptmix(iteration=50, append=True) # run your own experiment
print("\n\n\n========== Independent Agent Models =========\n")
error_handler("data/gptmix_neutral_percent_self_0.7_None.csv")
gptmix_stat("data/gptmix_neutral_percent_self_0.7_None.csv")

# Expt 6
# baseline(iteration=50, topic="joke", cot=True) # run your own experiment
print("\n\n\n========== COT intervention =========\n")
analyze_self_percent_ind("data/gpt-4o_neutral_percent_self_0.7_joke_None_True.csv", "data/gpt-4o_neutral_percent_self_0.7_None.csv")