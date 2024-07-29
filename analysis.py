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
    cohensd=cohens_d(df["self"], df["peer"])
    print("cohens_d = ", cohensd)


# # analyze percentage file
def analyze_group_percent(filename):
    df=cal_group_sum(filename, "self")
    df["base"]=100
    df.columns=["group", "base"]

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

def analyze_next_percent_1samp(file1):
    df=cal_group_sum(file1, "peer")
    df["control"]=100
    df.columns=["base", "control"]

    obj2=stats.ttest_1samp(df["base"], popmean=100) 
    cohensd=cohens_d(df["base"], df["control"])
    print("mean = ", df["base"].mean())
    print("pvalue = ", obj2[1])
    print("one sample t-test: ", obj2)
    print("cohens_d = ", cohensd)

def analyze_self_percent_1samp(file1):
    df=cal_group_sum(file1, "self")
    df["control"]=100
    df.columns=["base", "control"]

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
            "control":20
        }
        summary.append(comp)
    df=pd.DataFrame(summary)
    print(df.shape)
    
    obj2=stats.ttest_1samp(df["base"], popmean=20) 
    cohensd=cohens_d(df["base"], df["control"])
    print("mean = ", df["base"].mean())
    print("pvalue = ", obj2[1])
    print("one sample t-test: ", obj2)
    print("cohens_d = ", cohensd)

def analyze_self_percent_ind(file1, file2):
    f1=cal_group_sum(file1, "self")
    f2=cal_group_sum(file2, "self")
    if f1.shape!=f2.shape:
        return
    df=pd.concat([f1["group_sum"], f2["group_sum"]], axis=1, keys=["base", "comparison"])

    obj=stats.ttest_ind(df["base"], df["comparison"]) 
    cohensd=cohens_d(df["base"], df["comparison"])
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

def cal_group_sum(file1, ident):
    base=pd.read_csv(file1, header=0)
    if ident=="self":
        base=base.query("kind != 'peer'")
    elif ident=="next" or ident=="peer":
        base=base.query("kind != 'self'")

    nrow, ncol=base.shape
    block=5
    summary=[]

    for i in range(int(nrow/block)):
        p=base.iloc[i*block:i*block+block]
        comp={
            "group_sum":p["percentage"].sum(),
        }
        summary.append(comp)
    return pd.DataFrame(summary)

def oneway_anova(file1, file2, file3):
    a1=cal_group_sum(file1, "self")["group_sum"].values
    a2=cal_group_sum(file2, "self")["group_sum"].values
    a3=cal_group_sum(file3, "self")["group_sum"].values
    lens=min(len(a1), len(a2), len(a3))
    a1=a1[0:lens]
    a2=a2[0:lens]
    a3=a3[0:lens]
    ret=stats.f_oneway(a1, a2, a3)
    print([a1, a2, a3])
    print(ret)
