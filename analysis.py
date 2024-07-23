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

def reformat(filename):
    os.remove("reformat.csv")
    pos=pd.read_csv(filename, header=0)
    pos=pos.query("kind != 'peer'").head(200)

    nrow, ncol=pos.shape
    names=["one", "two", "three","four"]

    block=5
    summary=[]
    for i in range(int(nrow/block)):
        pRow={}
        for j in range(block):
            idx=i*block+j
            pRow[names[j]]=pos.loc[pos.index[idx],"percentage"]
        summary.append(pRow)

    df=pd.DataFrame(summary)
    # print(df.head())
    df.to_csv("reformat.csv", mode='a', index=False, header=False)


# # analyze rating file
def analyze_group_rank(filename):
    stat=pd.read_csv(filename, header=0)
    nrow, ncol=stat.shape
    summary=[]
    block=5
    for i in range(int(nrow/block)):
        d=stat.iloc[i*block:i*block+block]
        comp=d.groupby("kind")["rank"].mean()
        summary.append(comp)

    df=pd.DataFrame(summary)
    print(df.describe())
    ret=stats.ttest_ind(df["peer"], df["self"]) 
    print(ret)


# # analyze percentage file
def analyze_group_percent(filename):
    stat=pd.read_csv(filename, header=0)
    summary=[]

    s=stat.query("kind != 'peer'")
    nrow, ncol=s.shape

    block=5
    for i in range(int(nrow/block)):
        d=s.iloc[i*block:i*block+block]
        summary.append({
            "group":d["percentage"].sum(),
            "base":100,
        })

    df=pd.DataFrame(summary)
    # print(df)
    print(df.describe())
    ret=stats.ttest_1samp(df["group"], popmean=100) 
    cohensd=cohens_d(df["group"], df["base"])
    print("mean = ", df["group"].mean())
    print("one sample t-test: ", ret)
    print("cohens_d = ", cohensd)

def cohens_d(df1, df2):
    c0=df1.to_list()
    c1=df2.to_list()
    return ((mean(c0) - mean(c1)) / (sqrt((stdev(c0) ** 2 + stdev(c1) ** 2) / 2)))

def analyze_self_percent_1samp(file1):
    base=pd.read_csv(file1, header=0)
    base=base.query("kind != 'peer'")
    nrow, ncol=base.shape
    block=5
    summary=[]
    for i in range(int(nrow/block)):
        p=base.iloc[i*block:i*block+block]
        comp={
            "base":p["percentage"].sum(),
            "control":100
        }
        summary.append(comp)

    # summary=cal_self_sum(file1)
    df=pd.DataFrame(summary)
    obj2=stats.ttest_1samp(df["base"], popmean=100) 
    cohensd=cohens_d(df["base"], df["control"])
    print("mean = ", df["base"].mean())
    print("pvalue = ", obj2[1])
    print("one sample t-test: ", obj2)
    print("cohens_d = ", cohensd)

def analyze_other_percent_1samp(file1):
    base=pd.read_csv(file1, header=0)
    base=base.query("kind != 'self'")
    nrow, ncol=base.shape
    block=4
    summary=[]
    for i in range(int(nrow/block)):
        p=base.iloc[i*block:i*block+block]
        comp={
            "base":p["percentage"].mean(),
            "control":100
        }
        summary.append(comp)
    df=pd.DataFrame(summary)
    print(df.shape)
    
    block=5
    summary2=[]
    nrow2, col=df.shape
    for j in range(int(nrow2/5)):
        p2=df.iloc[j*block:j*block+block]
        comp={
            "base":p2["base"].sum(),
            "control":100
        }
        summary2.append(comp)

    df2=pd.DataFrame(summary2)
    print(df2.shape)
    obj2=stats.ttest_1samp(df2["base"], popmean=100) 
    cohensd=cohens_d(df2["base"], df2["control"])
    print("mean = ", df2["base"].mean())
    print("pvalue = ", obj2[1])
    print("one sample t-test: ", obj2)
    print("cohens_d = ", cohensd)

def analyze_self_percent_ind(file1, file2):
    base=pd.read_csv(file1, header=0)
    base=base.query("kind != 'peer'")
    nrow, ncol=base.shape
    block=5
    summary=[]

    neg=pd.read_csv(file2, header=0)
    neg=neg.query("kind != 'peer'")
    nrow2, ncol2=neg.shape

    if nrow!=nrow2:
        print("wrong:\n", nrow, nrow2)
        return
    for i in range(int(nrow/block)):
        p=base.iloc[i*block:i*block+block]
        n=neg.iloc[i*block:i*block+block]
        comp={
            "base":p["percentage"].sum(),
            "negative":n["percentage"].sum(),
        }
        summary.append(comp)
    df=pd.DataFrame(summary)
    obj=stats.ttest_ind(df["base"], df["negative"]) 
    cohensd=cohens_d(df["base"], df["negative"])
    print(df.describe())
    print("pvalue = ", obj[1])
    print("Independent t-test: ", obj)
    print("cohens_d = ", cohensd)


def error_handler(filename):
    file=pd.read_csv(filename, header=0)
    file=file.query("kind != 'peer'")
    nrow, ncol=file.shape
    block=5
    final=[]
    correct=pd.Series(["One", "Two", "Three", "Four", "Five"])
    i=0
    while i<nrow:
        f=file.iloc[i:i+block]
        if not np.array_equal(correct.values,f["name"].values):
            j=1
            while file.iloc[i+j, f.columns.get_loc("name")]!="One":
                j=j+1
            print(file.iloc[i:i+j])
            i=i+j
        else:
            final.append(f)
            i=i+block

    ret=pd.concat(final)
    print(ret.shape)

def cal_self_sum(file1):
    base=pd.read_csv(file1, header=0)
    base=base.query("kind != 'peer'")
    nrow, ncol=base.shape
    block=5
    summary=[]

    for i in range(int(nrow/block)):
        p=base.iloc[i*block:i*block+block]
        comp={
            "self_sum":p["percentage"].sum(),
        }
        summary.append(comp)
    return pd.DataFrame(summary)

def oneway_anova(file1, file2, file3):
    a1=cal_self_sum(file1)["self_sum"].values
    a2=cal_self_sum(file2)["self_sum"].values
    a3=cal_self_sum(file3)["self_sum"].values
    lens=min(len(a1), len(a2), len(a3))
    a1=a1[0:lens]
    a2=a2[0:lens]
    a3=a3[0:lens]
    ret=stats.f_oneway(a1, a2, a3)
    print([a1, a2, a3])
    print(ret)

# analyze_self_percent("Llama-3-70b-chat-hf_neutral_percent_self_1.csv", 100)
# error_handler("Llama-2-70b-chat-hf_neutral_percent_self_1.csv")
# error_handler("gpt-4-1106-preview_neutral_percent_self_1.csv")
# analyze_self_percent('gpt-4o')
# analyze_group_percent('gpt-4o_neutral_percent_group_1.csv')
# analyze_group_percent('gpt-4o_neutral_percent_group_1.csv')
# reformat('gpt-4o')
