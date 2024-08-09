import json
import re
import os
import pandas as pd
import numpy as np
import os.path

def save_to_json(entry, filename):
    a = []
    if not os.path.isfile(filename):
        a.append(entry)
        with open(filename, mode='w') as f:
            f.write(json.dumps(a, indent=2))
    else:
        with open(filename) as feedsjson:
            feeds = json.load(feedsjson)

        feeds.append(entry)
        with open(filename, mode='w') as f:
            f.write(json.dumps(feeds, indent=2))

def save_to_csv(summary, name, filename):
    jsonstr=parseJsonStr(summary)
    if not jsonstr:
        return None
    if isinstance(jsonstr, dict):
        jsonstr=[jsonstr] 

    df=pd.DataFrame(jsonstr)
    df["rater"]=name
    df["kind"]=np.where(df["name"]==name, "self", "peer")

    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)   
    else:
        df.to_csv(filename, mode='a', index=False, header=False)

def save_to_csv_gptmix(summary, name, filename, model, *args):
    jsonstr=parseJsonStr(summary)
    if not jsonstr:
        return None
    if isinstance(jsonstr, dict):
        jsonstr=[jsonstr] 

    df=pd.DataFrame(jsonstr)
    df["rater"]=name
    df["kind"]=np.where(df["name"]==name, "self", "peer")
    df["model"]=model
    if len(args)>0:
        df["iter"]=args[0]

    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)   
    else:
        df.to_csv(filename, mode='a', index=False, header=False)

# def save_to_csv_questionnaire(summary, name, filename, model):
#     jsonstr=parseJsonStr(summary)
#     if not jsonstr:
#         return None
#     if isinstance(jsonstr, dict):
#         jsonstr=[jsonstr] 

#     df=pd.DataFrame(jsonstr)
#     df["rater"]=name
#     df["kind"]=np.where(df["name"]==name, "self", "peer")
#     df["model"]=model

#     if not os.path.isfile(filename):
#         df.to_csv(filename, index=False)   
#     else:
#         df.to_csv(filename, mode='a', index=False, header=False)



def parseJsonStr(result_str):
    if "```json" in result_str:
        ret=re.findall(r"```json(.*?)```", result_str, re.DOTALL)[0]
    elif "```" in result_str:
        ret=re.findall(r"```(.*?)```", result_str, re.DOTALL)[0]
    elif "'''json" in result_str:
        ret=re.findall(r"'''json(.*?)'''", result_str, re.DOTALL)[0]
    elif "[" in result_str:
        ret=result_str[result_str.find("[") : result_str.find("]")+1]
    else:
        ret=result_str
    try:
        ret=json.loads(ret)
    except ValueError:
        print('invalid string:\n\n'+ret)
    return ret

Authority=[1,8,10,11,12,32,33,36]
Exhibitionism=[2,3,7,20,28,30,38]
Superiority=[4,9,26,40]
Entitlement=[5,14,18,24,25,27]
Exploitativeness=[6,13,16,23,35]
Self_Sufficiency=[17,21,22,31,34,39]
one=[1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2]