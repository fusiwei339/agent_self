import json
import re
import os
import pandas as pd
import numpy as np

config_list=[
    {
        "model": "gpt-3.5-turbo-0125",
        "base_url": "https://api.chatanywhere.com.cn",
        "api_key": "sk-CUIdUOkG7Xl3lRF2Lfg4YULUew1dRRy3cLtjNB29vtwXpsGR"
    }
]

jsonfile="gpt35_percentage.json"
csvfile="gpt35_self_percent_positive.csv"

def save_to_json(entry):
    a = []
    if not os.path.isfile(jsonfile):
        a.append(entry)
        with open(jsonfile, mode='w') as f:
            f.write(json.dumps(a, indent=2))
    else:
        with open(jsonfile) as feedsjson:
            feeds = json.load(feedsjson)

        feeds.append(entry)
        with open(jsonfile, mode='w') as f:
            f.write(json.dumps(feeds, indent=2))

def analyzeRanking(summary, names, i):
    jsonstr=parseJsonStr(summary)
    if not jsonstr:
        return None
    if isinstance(jsonstr, dict):
        jsonstr=[jsonstr] 

    df=pd.DataFrame(jsonstr)
    df["total_num"]=len(names)
    df["rater"]=names[i]
    df["kind"]=np.where(df["name"]==names[i], "self", "peer")
    df.to_csv(csvfile, mode='a', index=False, header=False)

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
