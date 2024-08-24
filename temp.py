import pandas as pd
import matplotlib.pyplot as plt
import json
import seaborn as sns

def enrich_dataframe(df, json_obj):
    # Convert JSON object to a dictionary
    json_dict = json.loads(json_obj)

    # Get the index of the last row
    last_index = df.index[-1]

    # Enrich the last row with new columns from the JSON object
    for key, value in json_dict.items():
        df.loc[last_index, key] = value

    return df

# # Example usage
# data = {
#     'A': [1, 2, 3],
#     'B': [4, 5, 6]
# }
# df = pd.DataFrame(data)
# json_obj = '{"C": 7, "D": 8}'

# enriched_df = enrich_dataframe(df, json_obj)
# print(enriched_df)


def get_row(df, col1_value, col2_value, col3_value, col1_name='A', col2_name='B', col3_name='C'):
    # Create a condition based on the values of the three columns
    condition = (df[col1_name] == col1_value) & (df[col2_name] == col2_value) & (df[col3_name] == col3_value)
    
    # Filter the DataFrame using the condition
    row = df[condition]
    
    return row

# # Example usage
# data = {
#     'A': [1, 2, 3, 4, 5],
#     'B': [5, 4, 3, 2, 1],
#     'C': [10, 20, 30, 40, 50]
# }
# df = pd.DataFrame(data)

# # Get the row where A=3, B=3, and C=30
# row = get_row(df, 3, 3, 30)
# print(row)

import numpy as np
def revise_iter(ques_file, eval_file):
    ques=pd.read_csv(ques_file, header=0)
    ques=ques.query("kind != 'peer'")
    ques.reset_index(drop=True, inplace=True)
    ques["choice"]=ques["choice"].str.extract(r'(\d+)')
    nrow, ncol=ques.shape
    block=200

    idx=0
    for i in range(int(nrow/block)):
        ques.loc[i*block:i*block+block-1, 'iter']=idx
        idx=idx+1
    ques.to_csv("revised_"+ques_file, index=False)   


    eval_ori=pd.read_csv(eval_file, header=0)
    eval=eval_ori.query("kind != 'peer'")
    eval.reset_index(drop=True, inplace=True)
    eval["percentage"]=eval["percentage"].str.extract(r'(\d+)')
    nrow, ncol=eval.shape
    block=5

    idx=0
    for i in range(int(nrow/block)):
        eval.loc[i*block:i*block+block-1, "iter"]=idx
        idx=idx+1

    eval.to_csv("revised_"+eval_file, index=False)   

def ques_stat(file):
    
    ques=pd.read_csv(file, header=0)
    ques=ques.drop(["percentage"], axis=1)
    model_groups=ques.groupby(["model"])
    for key, item in model_groups:
        model_block=model_groups.get_group(key).reset_index()
        print(key, "description: \n")
        sns.histplot(data=model_block, x="total")
        plt.show()

# ques_stat("re_revised_gptmix_neutral_percent_self_0.7_None.csv")


# import pathlib
# ques="gptmix_neutral_percent_self_0.7_None_questionnaire.csv"
# eval="gptmix_neutral_percent_self_0.7_None.csv"
# pathlib.Path("revised_"+ques).unlink(missing_ok=True)
# pathlib.Path("revised_"+eval).unlink(missing_ok=True)
# revise_iter(ques, eval)
    
def gptmix_clean(file):
    gptmix=pd.read_csv(file, header=0)
