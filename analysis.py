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
# stat=pd.read_csv('statistics_overclaiming.csv', header=0)
# summary=[]

# groups=[y for x, y in stat.groupby("total_num")]
# for g in groups:
#     nrow, ncol=g.shape
#     total_num=g.loc[g.index[0],"total_num"]

#     for i in range(int(nrow/3)):
#         d=g.iloc[i*3:i*3+3]
#         y=d["answer"].mean()*total_num
#         comp={"y":y, "base":100, "total_num":total_num}
#         summary.append(comp)

# df=pd.DataFrame(summary)
# print(df)
# print(df.describe())
# ret=stats.ttest_rel(df["base"], df["y"]) 
# print(ret)
