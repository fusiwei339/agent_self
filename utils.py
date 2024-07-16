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

def save_to_csv(summary, names, i, filename):
    jsonstr=parseJsonStr(summary)
    if not jsonstr:
        return None
    if isinstance(jsonstr, dict):
        jsonstr=[jsonstr] 

    df=pd.DataFrame(jsonstr)
    df["total_num"]=len(names)
    df["rater"]=names[i]
    df["kind"]=np.where(df["name"]==names[i], "self", "peer")

    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)   
    else:
        df.to_csv(filename, mode='a', index=False, header=False)

def parseJsonStr(result_str):
    if "```json" in result_str:
        ret=re.findall(r"```json(.*?)```", result_str, re.DOTALL)[0]
    elif "```" in result_str:
        ret=re.findall(r"```(.*?)```", result_str, re.DOTALL)[0]
    elif "'''json" in result_str:
        ret=re.findall(r"'''json(.*?)'''", result_str, re.DOTALL)[0]
    else:
        ret=result_str
    try:
        ret=json.loads(ret)
    except ValueError:
        print('invalid string:'+ret)
    return ret
