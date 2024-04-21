# project.py


import pandas as pd
import numpy as np
from pathlib import Path

import plotly.express as px


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_assignment_names(grades):
    assignment_names = {
        'lab': [],
        'project': [],
        'midterm': [],
        'final': [],
        'disc': [],
        'checkpoint': []
    }

    for column in grades.columns:
        if column.startswith('lab'):
            assignment_names['lab'].append(column)
        elif column.startswith('project'):
            if 'checkpoint' in column:
                assignment_names['checkpoint'].append(column)
            else:
                assignment_names['project'].append(column)
        elif column == 'Midterm':
            assignment_names['midterm'].append(column)
        elif column == 'Final':
            assignment_names['final'].append(column)
        elif column.startswith('discussion'):
            assignment_names['disc'].append(column)

    for key in assignment_names:
        assignment_names[key] = sorted(assignment_names[key])

    return assignment_names


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def projects_total(grades):
    grades = grades.fillna(0)
    
    filtered_columns = grades[[col for col in grades.columns if all(word in col for word in ['project'])]]
    drop_columns = [col for col in filtered_columns.columns if any(word in col for word in['Max Points', 'Lateness', 'checkpoint', 'free'])]
    filtered_columns = filtered_columns.drop(labels = drop_columns, axis = 1)
    for col in filtered_columns:
        if f'{col}_free_response' in grades.columns:
            filtered_columns[col] = filtered_columns[col] + grades[f'{col}_free_response']
            
    max_points = grades[[col for col in grades.columns if all(word in col for word in ['project', 'Max'])]]
    drop_columns = [col for col in max_points.columns if any(word in col for word in['Lateness', 'checkpoint', 'free'])]
    max_points = max_points.drop(labels = drop_columns, axis = 1)
    for col in filtered_columns:
        if f'{col}_free_response - Max Points' in grades.columns:
            max_points[f'{col} - Max Points'] = max_points[f'{col} - Max Points'] + grades[f'{col}_free_response - Max Points']

    for col in filtered_columns:
        filtered_columns[col] = filtered_columns[col] / max_points[f'{col} - Max Points']

    filtered_columns = filtered_columns.sum(axis = 1) / filtered_columns.shape[1]
            
    return filtered_columns


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def lateness_penalty(col):
    def lateness_penalty(late):
    def convert_to_hours(hms):
        if pd.isna(hms):
            return 0
        hours, minutes, seconds = map(int, hms.split(':'))
        total = hours + minutes / 60 + seconds / 3600
        return total

    late_list = []
    hour_week = 168

    for late_time in late:
        hours_late = convert_to_hours(late_time)
        if hours_late <= 2:
            late_list.append(1.0)
        elif hours_late <= hour_week:  # One week = 7 days = 168 hours
            late_list.append(0.9)
        elif hours_late <= hour_week*2:  # Two weeks = 14 days = 336 hours
            late_list.append(0.7)
        else:
            late_list.append(0.4)

    return pd.Series(late_list, index=late.index)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def process_labs(grades):
    def process_labs(grades):
    filtered_columns = grades[[col for col in grades.columns if all(word in col for word in ['lab'])]]
    drop_cols = [col for col in filtered_columns.columns if any(word in col for word in['Max Points', 'Lateness'])]
    filtered_columns = filtered_columns.drop(labels = drop_cols, axis = 1)
    
    labs = []
    for col in filtered_columns:
        labs.append(col)
        
    processed_labs = pd.DataFrame(index=grades.index, columns=labs, dtype=float)
    
    for lab in labs:
        lab_scores = grades[lab].fillna(0)
        max_points = grades[f"{lab} - Max Points"]
        
        lateness = grades[f"{lab} - Lateness (H:M:S)"]
        lateness_multipliers = lateness_penalty(lateness)
        adjusted_scores = lab_scores * lateness_multipliers
        
        normalized_scores = adjusted_scores / max_points
        
        processed_labs[lab] = normalized_scores
    
    return processed_labs


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def lab_total(processed):
    def lab_total(df):
    lab_series = []
    for index, row in df.iterrows():
        drop_lab = row.min()
        lab_sum = row.sum()
        lab_grade = (lab_sum - drop_lab)/(df.shape[1]-1)
        lab_series.append(lab_grade)
    return pd.Series(lab_series)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------

def process_checkpoints(grades):
    filtered_columns = grades[[col for col in grades.columns if all(word in col for word in ['checkpoint'])]]
    drop_cols = [col for col in filtered_columns.columns if any(word in col for word in['Max Points', 'Lateness'])]
    filtered_columns = filtered_columns.drop(labels = drop_cols, axis = 1)
    
    checkpoints = []
    for col in filtered_columns:
        checkpoints.append(col)
        
    processed_checks = pd.DataFrame(index=grades.index, columns=checkpoints, dtype=float)

    for point in checkpoints:
        check_scores = grades[point].fillna(0)
        max_points = grades[f"{point} - Max Points"]
        
        normalized_scores = check_scores / max_points
        
        processed_checks[point] = normalized_scores
    
    return processed_checks

def total_points(grades):
    grades = grades.fillna(0)
    
    lab_grade = lab_total(process_labs(grades)) * 0.20
    
    project_grade = projects_total(grades) * .30
    
    mt_grade = (grades['Midterm'] / grades['Midterm - Max Points']) * 0.15
    
    final_grade = (grades['Final'] / grades['Final - Max Points']) * 0.30

    check_grade = process_checkpoints(grades)
    check_grade = check_grade.sum(axis = 1) / check_grade.shape[1]
    check_grade = check_grade * 0.025

    for i in range(1,10):
        if i == 1:
            di_grade = grades[f'discussion0{i}']
        else:
            di_grade = di_grade + grades[f'discussion0{i}']
    di_grade = di_grade + grades[f'discussion10']
    di_grade = (di_grade / 100) * 0.025

    final = (
        lab_grade +
        project_grade +
        mt_grade + 
        final_grade + 
        check_grade + 
        di_grade
    )
    return final


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def final_grades(total):
    letter_grade = []
    for grade in total:
        if float(grade) >= 0.9:
            letter_grade.append('A')
        elif 0.8 <= float(grade):
            letter_grade.append('B')
        elif 0.7 <= float(grade):
            letter_grade.append('C')
        elif 0.6 <= float(grade):
            letter_grade.append('D')
        else:
            letter_grade.append('F')
    return pd.Series(letter_grade)

def letter_proportions(total):
    letter_count = (final_grades(final_series)).value_counts()
    prop = letter_count / (final_grades(final_series).count())
    scores = pd.Series(prop)
    return scores


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def raw_redemption(final_breakdown, question_numbers):
    total_redem = 0
    redem_points = 0
    final = final_breakdown.fillna(0)
    for i in range(len(question_numbers)):
        total_redem = total_redem + final.iloc[:,question_numbers[i]].max()
        redem_points = redem_points + final.iloc[:,question_numbers[i]]
    final_prop = redem_points/total_redem
    final['Raw Redemption Score'] = final_prop
    redemp_df = final[['PID','Raw Redemption Score']]
    return redemp_df
    
def combine_grades(grades, raw_redemption_scores):
    merge_df = pd.merge(grades, raw_redemption_scores, on='PID', how='left')
    
    merge_df['Raw Redemption Score'] = merge_df['Raw Redemption Score'].fillna(0) 
    
    return merge_df


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def z_score(ser):
    mean = ser.mean()
    std_dev = ser.std(ddof=0)
    z_scores = (ser - mean) / std_dev
    return z_scores
    
def add_post_redemption(grades_combined):
    pre_mt = (grades['Midterm'] / grades['Midterm - Max Points'])
    grades_combined['Midterm Score Pre-Redemption'] = pre_mt
    pre_z = z_score(pre_mt)
    post_z = z_score(grades_combined['Raw Redemption Score'])
    z_df = df = pd.DataFrame({'pre_z': pre_z, 'post_z': post_z, 'Midterm Score Pre-Redemption': pre_mt})


    post_mt = []
    for index, row in z_df.iterrows():
        if row['pre_z'] < row['post_z']:
            post_mt.append(row['post_z']*grades_combined['Midterm Score Pre-Redemption'].std(ddof=0)+grades_combined['Midterm Score Pre-Redemption'].mean())
        else:
            post_mt.append(row['Midterm Score Pre-Redemption'])
            

    grades_combined['Midterm Score Post-Redemption'] = pd.Series(post_mt)  
    return grades_combined


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def total_points_post_redemption(grades_combined):
    mt_grade = (grades['Midterm'] / grades['Midterm - Max Points']) * 0.15
    new_final = total_points(grades_combined) - mt_grade + grades_combined['Midterm Score Post-Redemption']*0.15
    return new_final
        
def proportion_improved(grades_combined):
    denom = grades_combined.shape[0]
    num = (final_grades(total_points(grades)) > final_grades(total_points_post_redemption(grades_combined))).sum()    
    return num/denom


# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def section_most_improved(grades_analysis):
    ...
    
def top_sections(grades_analysis, t, n):
    ...


# ---------------------------------------------------------------------
# QUESTION 12
# ---------------------------------------------------------------------


def rank_by_section(grades_analysis):
    ...


# ---------------------------------------------------------------------
# QUESTION 13
# ---------------------------------------------------------------------


def letter_grade_heat_map(grades_analysis):
    ...
