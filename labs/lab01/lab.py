# lab.py


from pathlib import Path
import io
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 0 
# ---------------------------------------------------------------------


def consecutive_ints(ints):
    if len(ints) == 0:
        return False

    for k in range(len(ints) - 1):
        diff = abs(ints[k] - ints[k+1])
        if diff == 1:
            return True

    return False


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def median_vs_mean(nums):
    nums.sort()
    if len(nums)%2 == 0:
        median = (nums[len(nums)//2] + nums[(len(nums)//2)-1])/2
    else:
        median = nums[len(nums)//2]
    mean = sum(nums)/len(nums)
    return median <= mean


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def n_prefixes(s, n):
    final_string = ''
    for k in range(n):
        final_string += s[:n-k]
    return final_string


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def exploded_numbers(ints, n):
    list = []
    length = len(str(ints[-1] + n))
    min_num = ints[0] - n
    
    for num in ints:
        exploded = [str(i).zfill(length) for i in range(num - n, num + n + 1)]
        list.append(' '.join(exploded))
    
    return list




# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def last_chars(fh):
    string = ""
    for line in fh:
        line = line.strip()
        if line:
            string += line[-1]
    return string


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def add_root(A):
    index_sqrt = np.sqrt(np.arange(len(A)))
    sum = A + index_sqrt
    return sum

def where_square(A):
    sqrt = np.sqrt(A)
    perf_square = np.equal(sqrt.astype(int), sqrt)
    return perf_square



# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_loop(matrix, cutoff):
    mean_array = [sum(col) / len(col) for col in matrix.T]
    final_cols = []
    for i, mean in enumerate(mean_array):
        if mean > cutoff:
            final_cols.append(i)
    filter_matrix = matrix[:, final_cols]
    return filter_matrix 

# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_np(matrix, cutoff):
    mean_array = matrix.mean(axis=0) 
    compare = mean_array > cutoff    
    filter_matrix = matrix[:, compare]
    return filter_matrix


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def growth_rates(A):
    diff = np.diff(A)
    rate = diff/A[:-1]
    rate_rounded = np.round(rate, 2)
    return rate_rounded

def with_leftover(A):
    initial = 20
    # num of shares bought each day 
    stocks_bought = np.floor(initial/A)
    # remaining money after day's purchase
    initial = initial - stocks_bought*A
    #remaining money using cum sum
    leftover = np.cumsum(initial)
    # find when leftover money can buy at least one full share
    day = np.argmax(leftover >= A)
    if leftover[day] < A[day]:
        return -1
    return day 

    

# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def salary_stats(salary):
    num_players = salary.shape[0]
    num_teams = salary['Team'].nunique()
    total_salary = salary['Salary'].sum()
    highest_salary = salary.loc[salary['Salary'].idxmax()]['Player']
    avg_los = salary.loc[salary['Team'] == 'Los Angeles Lakers', 'Salary'].mean()

    fifth = salary.sort_values('Salary').iloc[4]
    fifth_lowest = f"{fifth['Player']}, {fifth['Team']}"

    salary['Last Name'] = salary['Player'].apply(lambda x: x.split()[0])
    dupes = salary['Last Name'].duplicated().any()

    team_high = salary.loc[salary['Salary'].idxmax()]['Team']
    total_highest = salary.loc[salary['Team'] == team_high, 'Salary'].sum()

    stats = pd.Series({
        'num_players': num_players,
        'num_teams': num_teams,
        'total_salary': total_salary,
        'highest_salary': highest_salary,
        'avg_los': round(avg_los, 2),
        'fifth_lowest': fifth_lowest,
        'duplicates': dupes,
        'total_highest': total_highest
    })
    
    return stats

# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def parse_malformed(fp):
    parsed_data = []
    with open(fp, 'r') as file:
        for line in file:
            data = []

            # Iterate through each character in the line
            dupCommaIndex = None
            lastCommaIndex = None
            for i in range(len(line)):
                if lastCommaIndex == None or i == lastCommaIndex + 1:
                    dupCommaIndex = i
                lastCommaIndex = i
                
            newLine = ""
            if dupCommaIndex != None:
                newLine = line[:dupCommaIndex] + line[dupCommaIndex + 1:]
                
            data = newLine.split(',')
            data = [value for value in data if value != '']
            if data[0] == 'first':
                continue
            first_name = data[0].replace('"', '')
            last_name = data[1].replace('"', '')
            weight = float(data[2].replace('"', ''))
            height = float(data[3].replace('"', ''))
            geo = data[4]+ ',' + data[5] 
            geo = geo.replace('"', '')
            
            # Append the cleaned fields to the parsed data
            parsed_data.append([first_name, last_name, weight, height, geo])

    # Create DataFrame with the parsed data
    df = pd.DataFrame(parsed_data)
    df.columns = parsed_data[0]
    df.columns = ['first', 'last', 'weight', 'height', 'geo']

    return df
