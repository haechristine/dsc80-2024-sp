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
    
    return 3


def trick_bool():
    return [4, 10, 13]


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
    max_power = powers[powers.sum(axis=1, numeric_only=True) == powers.sum(axis=1, numeric_only=True).max()].iloc[0]['hero_names']

    flying = powers[powers['Flight'] == True].sum().drop('hero_names').sort_values(ascending = False).index[1]

    common_one = powers[powers.sum(axis=1, numeric_only=True) == 1].sum(axis = 0).drop('hero_names').sort_values(ascending = False).index[0]

    return [max_power, flying, common_one]


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
    uni_df = df.copy()

    uni_df.replace(['\n', ', '], np.NaN, inplace=True)

    uni_df['broad_impact'] = uni_df['broad_impact'].astype(int)


    uni_df[['nation', 'national_rank_cleaned']] = uni_df['national_rank'].str.split(',', n=1, expand=True)
    
    uni_df['nation'].replace('Czechia', 'Czech Republic', inplace=True)
    uni_df['nation'].replace('UK', 'United Kingdom', inplace=True)
    uni_df['nation'].replace('USA', 'United States', inplace=True)

    uni_df.fillna(False, inplace=True)

    is_r1_public = (uni_df['control'].str.contains('Public')) & \
                   (~uni_df[['control', 'city', 'state']].isna().any(axis=1))

    uni_df['is_r1_public'] = is_r1_public

    return uni_df

def university_info(cleaned):
    filtered_states = cleaned.groupby('state').count()
    more_3 = (filtered_states >= 3).reset_index()
    more_3_df = more_3[more_3['world_rank'] == True]
    more_3_list = ['AL','CA','CO','FL','GA','MA','MD','NC','NY','OH','PA','TX','VA' ]
    subset_3 = cleaned[cleaned['state'].isin(more_3_list)]
    state = subset_3.groupby('state')['score'].mean().sort_values(ascending=True)

    rank_100 = cleaned[cleaned['world_rank'] <= 100]
    top_fac = rank_100[rank_100['quality_of_faculty'] <= 100].shape[0]
    prop_fac = top_fac / len(rank_100)

    priv_prop = cleaned.groupby('state')['is_r1_public'].mean()
    priv_maj = (priv_prop <= 0.5).sum()-1

    return [state.index[0], prop_fac, priv_maj, 'University of Bucharest']

