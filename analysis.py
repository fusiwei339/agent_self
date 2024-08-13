import json
import os
import re

import pandas as pd
pd.options.display.float_format = "{:,.2f}".format
# pd.set_option('styler.format.precision', 2)
# pd.option_context('display.precision', 3, 
#                   'display.float_format', '{:.2f}'.format)
import numpy as np
import scipy.stats as stats 

import numpy as np
import random
from statistics import mean, stdev
from math import sqrt
import pathlib

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

def gptmix_stat(file):
    base=pd.read_csv(file, header=0)
    base=base.query("kind != 'peer'")
    base['percentage']=base['percentage'].astype(str).str.rstrip('%').astype(float)
    
    def get_model_data(name):
       return base.query("model == '{0}'".format(name)) 

    df=base.groupby("model")["percentage"].mean()
    print(df)
    models=["gpt-4o", "gpt-3.5-turbo-1106", "gpt-4-turbo-preview", "gpt-4-0613", "gpt-3.5-turbo"]
    for i in range(len(models)):
        target_data=get_model_data(models[i]).copy()
        target_data["control"]=20
        ret=stats.ttest_1samp(target_data['percentage'], 20) 
        print(models[i]," compare with 20: \n", ret)
        print("mean: ",target_data['percentage'].mean(), "\n")
        cohensd=cohens_d(target_data['percentage'], target_data["control"])
        print("cohens_d = ", cohensd)

def gptmix_ques(file, evaluation_csv=""):
    base=pd.read_csv(file, header=0)
    eval_csv=pd.read_csv(evaluation_csv, header=0)

    question_dim={"Authority":[1,8,10,11,12,32,33,36],
    "Exhibitionism":[2,3,7,20,28,30,38],
    "Superiority":[4,9,26,40],
    "Entitlement":[5,14,18,24,25,27],
    "Exploitativeness":[6,13,16,23,35],
    "Self_Sufficiency":[17,21,22,31,34,39]}
    ones=[1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2]

    base_group=base.groupby(["iter", "model"])
    for key, iterm in base_group:
        base_block=base_group.get_group(key).reset_index()
        # print(base_block, "\n\n")

        # get score of each component
        choices=base_block["choice"].tolist()
        ans=[1 if x == y else 0 for x, y in zip(choices, ones)]
        o={"total":sum(ans)-ans[14]-ans[18]-ans[28]-ans[36]}
        for k in question_dim:
            o[k]=0
            for idx in question_dim[k]:
                o[k]=o[k]+ans[idx-1]

        # write score to eval_csv
        condition=( (eval_csv["model"]==base_block["model"].iloc[0]) & (eval_csv["iter"]==base_block["iter"].iloc[0]) & (eval_csv["name"]==base_block["name"].iloc[0]) ) 

        rowNum=eval_csv[condition].index
        for component, score in o.items():
            eval_csv.loc[rowNum, component]=score

    eval_csv=eval_csv.drop("iter", axis=1)
    eval_group=eval_csv.groupby(["model"])
    for key, iterm in eval_group:
        model_block=eval_group.get_group(key).reset_index()
        ret=model_block.corrwith(model_block["percentage"], numeric_only=True)
        print(key, " self evaluation correlates with:", "\n", ret)


    pathlib.Path("re"+evaluation_csv).unlink(missing_ok=True)
    eval_csv.to_csv("re_"+evaluation_csv, index=False)   
        # condition=(eval_csv["model"]==base_block["model"].iloc[0] & eval_csv["iter"]==base_block["iter"].iloc[0] & eval_csv["name"]==base_block["name"].iloc[0]) 
