# lab.py


import pandas as pd
import numpy as np
import io
from pathlib import Path
import os


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def prime_time_logins(login):
    login['Time'] = pd.to_datetime(login['Time'])

    prime = login[(login['Time'].dt.hour >= 16) & (login['Time'].dt.hour < 20)]

    prime_count = prime.groupby('Login Id').size()

    prime_df = pd.DataFrame(prime_count, columns=['Time'])
    
    all_login = login['Login Id'].unique()
    
    prime_df = prime_df.reindex(all_login, fill_value = 0)

    return prime_df


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def count_frequency(login):
    login['Time'] = pd.to_datetime(login['Time'])
    today = pd.Timestamp('2024-01-31 23:59:00')
    login['days'] = (today -login['Time']).dt.days
    total = login.groupby('Login Id').size()
    login_frequency = total / login['days'].groupby(login['Login Id']).agg('first')
    return login_frequency


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def cookies_null_hypothesis():
    return [2]
                         
def cookies_p_value(N):
    observed_burnt = 15
    
    total_cookies = 250
    
    null_distribution = np.random.binomial(total_cookies, 0.04, size=N)
    
    p_value = np.mean(null_distribution >= observed_burnt)    
    return p_value


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def car_null_hypothesis():
    return [1,4]


def car_alt_hypothesis():
    return [2,6]


def car_test_statistic():
    return [1,4]


def car_p_value():
    return 3


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def superheroes_test_statistic():
    return [1, 4]

    
def bhbe_col(heroes):
    blonde = heroes['Hair color'].str.contains('blond', case = False)
    blue = heroes['Eye color'].str.contains('blue', case = False)
    blonde_blue = blonde & blue
    return blonde_blue

def superheroes_observed_statistic(heroes):
    bhbe_count = bhbe_col(heroes).sum()
    bhbe_df = heroes[bhbe_col(heroes)]
    good_bhbe = bhbe_df['Alignment'] == 'good'
    return (bhbe_df[good_bhbe].shape[0])/bhbe_count

def simulate_bhbe_null(heroes, N):
    null_prop = (heroes[heroes['Alignment'] == 'good'].shape[0])/heroes.shape[0]
    test_hero = np.random.binomial(bhbe_col(heroes).sum(), null_prop, size=N) / bhbe_col(heroes).sum()
    return test_hero

def superheroes_p_value(heroes):
    obs_stat = superheroes_observed_statistic(heroes)
    
    N_sims = 100000
    sim_stats = simulate_bhbe_null(heroes, N_sims)
    
    p_value = np.mean(sim_stats >= obs_stat)
    
    significance_level = 0.01
    if p_value < significance_level:
        hypothesis_result = 'Reject'
    else:
        hypothesis_result = 'Fail to reject'
    
    return [p_value, hypothesis_result]


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def diff_of_means(data, col='orange'):
    york = data[data['Factory'] == 'Yorkville'][col]
    waco = data[data['Factory'] == 'Waco'][col]
    
    york_mean = york.mean()
    waco_mean = waco.mean()
    
    tvd = abs(york_mean - waco_mean)
    
    return tvd


def simulate_null(data, col='orange'):
    perm_factory = np.random.permutation(data['Factory'])
    
    mix_skittles = data.copy()
    mix_skittles['Factory'] = perm_factory
    
    t_test = diff_of_means(mix_skittles, col)
    
    return t_test


def color_p_value(data, col='orange'):
    observed_tvd = diff_of_means(data, col)
    
    tests = [simulate_null(data, col) for i in range(1000)]
    
    p_value = np.mean(np.array(tests) >= observed_tvd)
    
    return p_value



# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def ordered_colors():
    return [('yellow', 0.0),('orange', 0.052),('red', 0.229),('green', 0.436),('purple', 0.984)]



# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


    
def same_color_distribution():
    return (0.011, 'Fail to Reject')


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def perm_vs_hyp():
        return ['H', 'H', 'P', 'H','P']
