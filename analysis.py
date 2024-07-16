import json
import os
import re

import pandas as pd
import numpy as np
import scipy.stats as stats 

import numpy as np
import random

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
def analyze_group_percent():
    stat=pd.read_csv('group_percent.csv', header=0)
    nrow, ncol=stat.shape
    summary=[]

    # groups=[y for x, y in stat.groupby("total_num")]
    # for g in groups:
    #     nrow, ncol=g.shape
    #     total_num=g.loc[g.index[0],"total_num"]

    block=4
    for i in range(int(nrow/block)):
        d=stat.iloc[i*block:i*block+block]
        comp=d.groupby('kind')['percentage'].mean()*block
        print(d)
        # y=d["answer"].mean()*total_num
        # comp={"y":y, "base":100, "total_num":total_num}
        summary.append(comp)

    df=pd.DataFrame(summary)
    # print(df)
    print(df.describe())
    ret=stats.ttest_rel(df["peer"], df["self"]) 
    print(ret)

def analyze_self_percent(model):
    pos=pd.read_csv("gpt-4o_positive_percent_next_1.csv", header=0)
    neg=pd.read_csv("gpt-4o_negative_percent_next_1.csv", header=0)

    # pos=pos.query("kind != 'peer'")
    # neg=neg.query("kind != 'peer'")
    nrow, ncol=pos.shape
    nrow2, ncol2=neg.shape
    if nrow!=nrow2:
        print("wrong:\n")
        print(nrow, nrow2)
        return

    block=4
    summary=[]
    for i in range(int(nrow/block)):
        p=pos.iloc[i*block:i*block+block]
        n=neg.iloc[i*block:i*block+block]
        comp={
            "pos":p["percentage"].sum(),
            "neg":n["percentage"].sum(),
            "base":100,
        }
        summary.append(comp)

    print(summary)
    df=pd.DataFrame(summary)

    print(df.describe())
    ret=stats.ttest_ind(df["pos"], df["neg"]) 
    print(ret)

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
# analyze_group_percent()
# reformat('gpt-4o')

