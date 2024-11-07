import json
import os
import re

import pandas as pd
pd.options.display.float_format = "{:,.2f}".format
import numpy as np
import scipy.stats as stats 

import numpy as np
import random
from statistics import mean, stdev
from math import sqrt
import pathlib
import shutil

def reformat_json(filename):
    pos=pd.read_csv(filename, header=0)
    pos=pos.query("kind != 'peer'")

    nrow, ncol=pos.shape
    names=["One", "Two", "Three","Four", "Five"]

    block=5
    summary=[]
    for i in range(int(nrow/block)):
        pRow={}
        for j in range(block):
            idx=i*block+j
            pRow[names[j]]=pos.loc[pos.index[idx],"percentage"]
        summary.append(pRow)

    pd.DataFrame(summary).to_json("vis/json/"+filename+".json", orient='records')

def reformat_summary(inputfile):
    df=cal_group_self_sum(inputfile, "self")
    df.to_csv("summary/"+inputfile, index=False)

def gptmix_reformat_json(filename):
    mix=pd.read_csv(filename, header=0)
    mix=mix.query("kind != 'peer'")

    nrow, ncol=mix.shape
    names=["gpt-3.5-turbo", "gpt-4o", "gpt-4-0613","gpt-4-turbo-preview", "gpt-3.5-turbo-1106"]

    block=5
    summary=[]
    for i in range(int(nrow/block)):
        round=mix.iloc[i*block:i*block+block]
        pRow={"sum":round["percentage"].sum(), "round":i}
        for j in range(block):
            idx=i*block+j
            pRow[names[j]]=mix.loc[mix.index[idx],"percentage"]
        summary.append(pRow)

    pd.DataFrame(summary).to_json("vis/json/"+filename+".json", orient='records')


def analyze_group_rank(filename):
    stat=pd.read_csv(filename, header=0)
    nrow, ncol=stat.shape
    summary=[]
    block=5
    for i in range(int(nrow/block)):
        d=stat.iloc[i*block:i*block+block]
        comp=d.groupby("kind")["rank"].mean()
        summary.append(comp)

    print(len(summary))
    df=pd.DataFrame(summary)
    print(df.describe())
    ret=stats.ttest_ind(df["peer"], df["self"]) 
    print(ret)
    cohensd=cohens_d(df["self"], df["peer"])
    print("cohens_d = ", cohensd)


def analyze_group_percent(filename):
    df=cal_group_self_sum(filename, "self")
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
    df=cal_group_self_sum(file1, "peer")
    df["control"]=100
    df.columns=["base", "control"]

    obj2=stats.ttest_1samp(df["base"], popmean=100) 
    cohensd=cohens_d(df["base"], df["control"])
    print("mean = ", df["base"].mean())
    print("pvalue = ", obj2[1])
    print("one sample t-test: ", obj2)
    print("cohens_d = ", cohensd)

def analyze_self_percent_1samp(file1):
    df=cal_group_self_sum(file1, "self")
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
    print("var = ", df["base"].var())
    print("pvalue = ", obj2[1])
    print("one sample t-test: ", obj2)
    print("cohens_d = ", cohensd)

def analyze_self_percent_ind(file1, file2):
    f1=cal_group_self_sum(file1, "self")
    f2=cal_group_self_sum(file2, "self")
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
    # file=file.query("kind != 'peer'")
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

def cal_group_self_sum(file1, ident):
    base=pd.read_csv(file1, header=0)
    base['percentage']=base['percentage'].astype(str).str.rstrip('%').astype(float)

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

def cal_group_sum(file1):
    base=pd.read_csv(file1, header=0)
    base['percentage']=base['percentage'].astype(str).str.rstrip('%').astype(float)

    nrow, ncol=base.shape
    block=5
    summary=[]

    for i in range(int(nrow/block)):
        p=base.iloc[i*block:i*block+block]
        temp=["One", "Two", "Three", "Four", "Five" ]
        current=p["name"].to_list()
        if current != temp:
            print(current, temp)
        if p["percentage"].sum()!=100:
            print("sum error")
        comp={
            "group_sum":p["percentage"].sum(),
        }
        summary.append(comp)
    return pd.DataFrame(summary)

def oneway_anova(file1, file2, file3):
    a1=cal_group_self_sum(file1, "self")["group_sum"].values
    a2=cal_group_self_sum(file2, "self")["group_sum"].values
    a3=cal_group_self_sum(file3, "self")["group_sum"].values
    lens=min(len(a1), len(a2), len(a3))
    a1=a1[0:lens]
    a2=a2[0:lens]
    a3=a3[0:lens]
    ret=stats.f_oneway(a1, a2, a3)
    print([a1, a2, a3])
    print(ret)

def gptmix_stat(file):
    base=pd.read_csv(file, header=0)
    base=base.query("kind != 'peer'")
    base['percentage']=base['percentage'].astype(str).str.rstrip('%').astype(float)
    
    def get_model_data(name):
       return base.query("model == '{0}'".format(name)) 

    def compareAB(model1, model2):
        print("\n\n\n========== Compare {} & {} =========\n".format(model1, model2))
        m1=get_model_data(model1)["percentage"]
        m2=get_model_data(model2)["percentage"]
        print("mean of {} and {}: \n".format(model1, model2), m1.mean(), m2.mean())
        obj=stats.ttest_ind(m1, m2) 
        cohensd=cohens_d(m1, m2)
        print(obj, "\n")
        print("cohens_d = ", cohensd)

        ret={"model1":model1,"model2":model2,"cohens_d":'{0:.2f}'.format(cohensd), "t":'{0:.2f}'.format(obj[0]), "p":'{0:.2e}'.format(obj[1])}
        filename="data/gptmix_5b_table.csv"
        if not os.path.isfile(filename):
            pd.json_normalize(ret).to_csv(filename, index=False)   
        else:
            pd.json_normalize(ret).to_csv(filename, mode='a', index=False, header=False)

    df=base.groupby("model")["percentage"].mean()
    print(df)
    models=["gpt-4o", "gpt-3.5-turbo-1106", "gpt-4-turbo-preview", "gpt-4-0613", "gpt-3.5-turbo"]
    for i in range(len(models)):
        target_data=get_model_data(models[i]).copy()
        target_data["control"]=20
        ret=stats.ttest_1samp(target_data['percentage'], 20) 
        print(models[i]," compare with 20: \n", ret)
        print("mean: ",target_data['percentage'].mean())
        cohensd=cohens_d(target_data['percentage'], target_data["control"])
        print("cohens_d = ", cohensd, "\n")

    for m1 in models:
        for m2 in models:
            if m1!=m2:
                compareAB(m1, m2)
