import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
import math

file_name = "data/algorithm data.xlsx"
df = pd.read_excel(file_name)

def update(time):
    for i, j in enumerate(time):
        if j <= 0.4:
            val = df.iloc[i, 1]
            df.iloc[i, 1] = val + 1
        elif j <= 0.6:
            val = df.iloc[i, 2]
            df.iloc[i, 2] = val + 1
        else:
            val = df.iloc[i, 3]
            df.iloc[i, 3] = val + 1
            
    df.to_excel(file_name, index=False)

def cramer_v():      
    contingency_table = df.iloc[:, 1:].values
    contingency_table = contingency_table[~np.any(contingency_table == 0, axis=1)]

    chi2, p, dof, expected = chi2_contingency(contingency_table)
    n = contingency_table.sum()
    q = min(contingency_table.shape)
    cramers_v = math.sqrt(chi2 / (n * (q - 1)))
    return cramers_v

def main(time):
    update(time)
    value = cramer_v()
    return value
