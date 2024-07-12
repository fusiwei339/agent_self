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

def analyze_self_percent(filename):
    stat=pd.read_csv(filename, header=0)
    stat=stat.query("kind != 'peer'")
    nrow, ncol=stat.shape
    print(stat.shape)
    block=4
    summary=[]
    for i in range(int(nrow/block)):
        d=stat.iloc[i*block:i*block+block]
        comp={
            "base":100,
            "sum":d["percentage"].sum()
        }
        summary.append(comp)

    df=pd.DataFrame(summary)

    print(df.describe())
    ret=stats.ttest_rel(df["sum"], df["base"]) 
    print(ret)

analyze_self_percent('gpt35_self_percent_negative.csv')
analyze_self_percent('gpt35_self_percent_positive.csv')
# analyze_group_percent()