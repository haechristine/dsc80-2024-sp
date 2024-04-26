# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def read_linkedin_survey(dirname):
    survey_df = []
    cols = ['first name', 'last name', 'current company', 'job title', 'email', 'university']            

    for file_path in Path(dirname).iterdir():
        if file_path.is_file():
            survey = pd.read_csv(file_path)
            survey.columns = [col.lower().replace('_', ' ') for col in survey.columns]
            survey = survey[cols]
            survey_df.append(survey)
            
    combine_df = pd.concat(survey_df, ignore_index=True)
    
    combine_df.reset_index(drop=True, inplace=True)
    
    return combine_df


def com_stats(df):
    df_cleaned = df.dropna(subset=['university', 'job title'])
    ohio_denom = df_cleaned[df_cleaned['university'].str.contains('Ohio', case=False)].shape[0]
    ohio = df_cleaned[df_cleaned['university'].str.contains('Ohio', case=False) & df_cleaned['job title'].str.contains('Programmer', case=False)].shape[0]
    
    unique_job = df_cleaned['job title'].unique()
    last_words = pd.Series(unique_job).str.split().str[-1]
    engineer = (last_words == 'Engineer').sum()

    longest = max(unique_job, key=len)
    
    manager = df_cleaned[df_cleaned['job title'].str.contains('manager', case=False)].shape[0]

    return [ohio/ohio_denom,int(engineer),str(longest),manager]



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def read_student_surveys(dirname):
    ec_question =[]
    for file_path in Path(dirname).iterdir():
        if file_path.is_file():
            ec = pd.read_csv(file_path)
            ec_question.append(ec)

        ec_df = pd.concat(ec_question, axis=1, join='outer')

        # Drop duplicate 'student_id' columns
        ec_df = ec_df.loc[:, ~ec_df.columns.duplicated()]
        ec_df.drop(columns=['id'], inplace=True)
        
    return ec_df


def check_credit(df):
    df.replace('(no genres listed)', np.nan, inplace=True)

    num_questions = len(df.columns)-1
    no_name = df.drop(columns=['name'])
    free = (no_name.count()/len(no_name) >= 0.9).sum()
    if (free > 2):
        free = 2
    else:
        free = np.floor(free)
        
    participation = (no_name.count(axis=1)/num_questions)
    ec_grade = participation.apply(lambda x: 5 + free if x >= 0.5 else free)
    check_df = pd.DataFrame({'name': df['name'],'ec': ec_grade})

        
    return check_df


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_popular_procedure(pets, procedure_history):
    pop_procedure = pd.merge(pets, procedure_history, on = 'PetID', how = 'left')
    procedure = pop_procedure['ProcedureType'].value_counts()
    most_pop = procedure.idxmax()
    return most_pop

def pet_name_by_owner(owners, pets):
    owners_pets = pd.merge(owners, pets, on='OwnerID', how='left')
    
    second_group = owners_pets.groupby(['Name_x','OwnerID']) 
    
    pet = second_group['Name_y'].agg(lambda x: x.tolist() if len(x) > 1 else x.iloc[0])
    pet = pet.reset_index().set_index('Name_x')['Name_y']

    return pet


def total_cost_per_city(owners, pets, procedure_history, procedure_detail):
    owners_pets = pd.merge(owners, pets, on='OwnerID', how='left')
    
    history = pd.merge(owners_pets, procedure_history, on='PetID', how='left')
    
    merged_df = pd.merge(history, procedure_detail, on='ProcedureType', how='left')
    
    total_cost_per_city = merged_df.groupby('City')['Price'].sum()
    
    return total_cost_per_city


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def average_seller(sales):
    pivot = pd.pivot_table(sales, values='Total', index='Name', aggfunc='mean', fill_value=0)
    sales_avg = pivot.reset_index()
    sales_avg.columns = ['Name', 'Average Sales']
    
    return sales_avg

def product_name(sales):
    return sales.pivot_table(index='Name',
               columns='Product',
               values='Total',
               aggfunc='sum')

def count_product(sales):
    return sales.pivot_table(index=['Product','Name'],
               columns='Date',
               values='Total',
               aggfunc='count', fill_value=0)

def total_by_month(sales):
    sales['Month'] = sales['Date'].str.split('.').str[0].astype(int)
    month = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    sales['Month'] = sales['Month'].map(month)

    total_month = sales.pivot_table(index=['Name', 'Product'], columns='Month', values='Total', aggfunc='sum', fill_value=0)
    return total_month
