# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def trick_me():
    tricky_1 = pd.DataFrame({'Name': ['Jeno', 'Mark', 'Renjun', 'Haechan', 'Jaemin'],
            'Name': ['nct', 'nct u', 'nct 127','wayv','dream'],
            'Age': ['22', '23', '22','21', '22']})
    tricky_1.to_csv('tricky_1.csv', index=False)
    tricky_2 = pd.read_csv('tricky_1.csv')
    
    df_side_by_side = pd.concat([tricky_1, tricky_2], axis=1)
    
    return 1


def trick_bool():
    return [4, 2, 13]


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def population_stats(df):
    result_df = pd.DataFrame(index=df.columns)
    
    result_df['num_nonnull'] = df.count()
    
    result_df['prop_nonnull'] = result_df['num_nonnull'] / df.shape[0]
    
    result_df['num_distinct'] = df.apply(lambda x: x.nunique(dropna=True))
    
    result_df['prop_distinct'] = result_df['num_distinct'] / result_df['num_nonnull']
    
    return result_df


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_common(df, N=10):
    common_df = pd.DataFrame(index=range(N))
    
    for col in df.columns:
        value_counts = df[col].value_counts()
        
        if len(value_counts) < N:
            missing_count = N - len(value_counts)
            missing_values = [np.NaN] * missing_count
            value_counts = value_counts.append(pd.Series(missing_values))
        
        common_vals = value_counts.iloc[:N]
        
        common_df[col + '_values'] = common_vals.index
    
        common_df[col + '_counts'] = common_vals.values
        
    return common_df


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def super_hero_powers(powers):
    hero_list = []
    
    power_cols = powers.select_dtypes(include= bool).columns
    power_count = (powers[power_cols].sum()).sort_values(ascending=False)
    max_powers = power_count.idxmax()
    
    hero_list.append(max_powers)

    # df consisting of flight being superpower
    flying = powers[(powers['Flight'] == 1)]
    flying_count = flying[power_cols].sum()
    
    hero_list.append(flying_count.index[0])
    
    one_power = powers[df.iloc[:, 0] == 1]
    one_power_count = one_power[power_cols].sum()
    one_power_max = one_power_count.idxmax()

    hero_list.append(one_power_max)
    return hero_list


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def clean_heroes(heroes):
    return heroes.replace(['-', -99.0], np.NaN)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def super_hero_stats():
    return ['Onslaught', 'George Lucas','bad', 'Marvel Comics', 'NBC - Heroes', 'Groot']


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def clean_universities(df):
    ...

def university_info(cleaned):
    ...

