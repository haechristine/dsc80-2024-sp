# lab.py


from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def after_purchase():
    return ['NMAR','MD','MAR','NMAR','MAR']



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def multiple_choice():
    return ['MAR','MAR','MAR','NMAR','MCAR']


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------



def first_round():
    return [0.0453, 'NR']


def second_round():
    return [0.0235, 'R' ,'D']


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def verify_child(heights):
    p_vals = {}
    for col in heights.columns:
        if col not in ['father', 'child']:
            p_vals[col] = (stats.ks_2samp(heights.loc[heights[col].isna(), 'father'],
                                       heights.loc[heights[col].notna(), 'father']).pvalue)

    return pd.Series(p_vals)


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def cond_single_imputation(new_heights):
    quartiles = pd.qcut(new_heights['father'], q=4, duplicates='drop')
    
    single_mean = new_heights.groupby(quartiles)['child'].transform('mean')
    
    impute = new_heights['child'].fillna(single_mean)
    
    return impute


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def quantitative_distribution(child, N):
    obs_vals = child.dropna().values

    counter, bin_limit = np.histogram(obs_vals, bins=10, density=True)

    bin_widths = np.diff(bin_limit)

    area = counter * bin_widths

    bin_index = np.random.choice(np.arange(len(area)), size=N, p=area)

    impute_vals = []
    for bin in bin_index:
        lower = bin_limit[bin]
        upper = bin_limit[bin + 1]
        impute_vals.append(np.random.uniform(lower, upper))

    return np.array(impute_vals)


def impute_height_quant(child):
    missing_count = child.isna().sum()

    impute_vals = quantitative_distribution(child, missing_count)

    impute_child = child.copy()
    impute_child[child.isna()] = impute_vals

    return impute_child


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def answers():
    mc = [1, 2, 2, 1]
    url = ['soundcloud.com','naver.com']
    return mc,url
