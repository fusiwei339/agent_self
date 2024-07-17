import json
import os
import re

import pandas as pd
import numpy as np
import scipy.stats as stats 

import numpy as np
import random
from statistics import mean, stdev
from math import sqrt

# # analyze rating file
# stat=pd.read_csv('statistics.csv', header=0)
# nrow, ncol=stat.shape
# summary=[]
# for i in range(int(nrow/5)):
#     d=stat.iloc[i*5:i*5+5]
#     comp=d.groupby("kind")["score"].mean()
#     summary.append(comp)

# df=pd.DataFrame(summary)
# print(df.describe())
# ret=stats.ttest_rel(df["peer"], df["self"]) 
# print(ret)



# # analyze percentage file
def analyze_group_percent(filename):
    stat=pd.read_csv(filename, header=0)
    summary=[]

    s=stat.query("kind != 'peer'")
    nrow, ncol=s.shape

    block=4
    for i in range(int(nrow/block)):
        d=s.iloc[i*block:i*block+block]
        summary.append({
            "group":d["percentage"].sum(),
            "base":100,
        })

    df=pd.DataFrame(summary)
    # print(df)
    print(df.describe())
    ret=stats.ttest_ind(df["group"], df["base"]) 
    print(ret)

def cohens_d(df1, df2):
    return (df1.mean()-df2.mean())/(np.sqrt((df1.std() ** 2 + df2.std() ** 2) / 2))

def analyze_self_percent(model):
    base=pd.read_csv("gpt-4o_neutral_percent_others_1.csv", header=0)
    control=pd.read_csv("gpt-4o_neutral_percent_others2_1.csv", header=0)

    base=base.query("kind != 'self'")
    control=control.query("kind != 'self'")
    nrow, ncol=base.shape
    nrow2, ncol2=control.shape
    if nrow!=nrow2:
        print("wrong:\n")
        print(nrow, nrow2)
        return

    block=4
    summary=[]
    for i in range(int(nrow/block)):
        p=base.iloc[i*block:i*block+block]
        n=control.iloc[i*block:i*block+block]
        comp={
            "base":p["percentage"].sum(),
            "control":n["percentage"].sum(),
            "zero":100,
        }
        summary.append(comp)

    df=pd.DataFrame(summary)

    print(df.describe())
    ret=stats.ttest_ind(df["base"], df["control"]) 
    cohensd=cohens_d(df["base"], df["control"])
    print(ret, "\n", cohensd)

def reformat(model):
    os.remove("reformat.csv")
    pos=pd.read_csv("positive_"+model+"_self_percent.csv", header=0)
    neg=pd.read_csv("negative_"+model+"_self_percent.csv", header=0)

    pos=pos.query("kind != 'peer'").head(200)
    neg=neg.query("kind != 'peer'").head(200)
    nrow, ncol=pos.shape
    nrow2, ncol2=neg.shape
    if nrow!=nrow2:
        print("wrong:\n")
        print(nrow, nrow2)
        return
    names=["one", "two", "three","four"]

    block=4
    summary=[]
    for i in range(int(nrow/block)):
        pRow={"success":True}
        for j in range(block):
            idx=i*block+j
            pRow[names[j]]=pos.loc[pos.index[idx],"percentage"]
        summary.append(pRow)
        
        nRow={"success":False}
        for j in range(block):
            idx=i*block+j
            nRow[names[j]]=neg.loc[neg.index[idx],"percentage"]
        summary.append(nRow)

    df=pd.DataFrame(summary)
    # print(df.head())
    df.to_csv("reformat.csv", mode='a', index=False, header=False)


analyze_self_percent('gpt-4o')
# analyze_self_percent('gpt-3.5-turbo-0125')
# analyze_self_percent('gpt35_self_percent_positive.csv')
# analyze_group_percent('gpt-4o_neutral_percent_group_1.csv')
# analyze_group_percent('gpt-4o_neutral_percent_group_1.csv')
# reformat('gpt-4o')

