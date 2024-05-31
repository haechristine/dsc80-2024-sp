# lab.py


import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm
from pathlib import Path
from sklearn.preprocessing import Binarizer, QuantileTransformer, FunctionTransformer

import warnings
warnings.filterwarnings('ignore')


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def best_transformation():
    return 1


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------

legend = {
    'cut': ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'],
    'color': ['J', 'I', 'H', 'G', 'F', 'E', 'D'],
    'clarity': ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']
}


def create_ordinal(df):
    ordinal_df = pd.DataFrame()
    for col_name, ranking in legend.items():
        if col_name in df.columns:
            ordinal_df[f'ordinal_{col_name}'] = df[col_name].map({value: index for index, value in enumerate(ranking)})

    return ordinal_df


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------



def create_one_hot(df):
    one_hot = pd.DataFrame()
    
    for col in df.columns:
        if df[col].dtype == 'object':
            unique_vals = df[col].unique()
            for val in unique_vals:
                col_name = f'one_hot_{col}_{val}'
                one_hot[col_name] = (df[col] == val).astype(int)
    
    return one_hot


def create_proportions(df):
    prop_df = pd.DataFrame()
    
    for col in df.columns:
        if df[col].dtype == 'object':
            props = df[col].value_counts(normalize=True)
            prop_df[f'proportion_{col}'] = df[col].map(props)
    
    return prop_df


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def create_quadratics(df):
    quant_cols = df.select_dtypes(include=[float, int]).columns.difference(['price'])
    quadratic_df = pd.DataFrame()
    
    col_pairs = [(quant_cols[i], quant_cols[j]) 
                 for i in range(len(quant_cols)) 
                 for j in range(i + 1, len(quant_cols))]
    
    for col1, col2 in col_pairs:
        quadratic_df[f'{col1} * {col2}'] = df[col1] * df[col2]
    
    return quadratic_df


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------



def comparing_performance():
    # create a model per variable => (variable, R^2, RMSE) table
    ...


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


class TransformDiamonds(object):
    
    def __init__(self, diamonds):
        self.data = diamonds
        
    # Question 6.1
    def transform_carat(self, data):
        binarizer = Binarizer(threshold=1)
        return binarizer.fit_transform(data[['carat']])
    
    # Question 6.2
    def transform_to_quantile(self, data):
        quant_trans = QuantileTransformer(n_quantiles=100)
        quant_trans.fit(self.data[['carat']]) 
        return quant_trans.transform(data[['carat']])
    
    # Question 6.3
    def transform_to_depth_pct(self, data):
        def calculate_depth_pct(arr):
            try:
                x, y, z = arr[0], arr[1], arr[2]  
                depth_pct = 100 * (2 * z) / (x + y)
                return depth_pct
            except ZeroDivisionError:
                return np.nan
        
        trans_depth_pct = []
        for arr in data[['x', 'y', 'z']].values:  
            depth_pct = calculate_depth_pct(arr)
            trans_depth_pct.append(depth_pct) 
        return np.array(trans_depth_pct)
