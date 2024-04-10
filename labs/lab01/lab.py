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
    ...


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def growth_rates(A):
    ...

def with_leftover(A):
    ...


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def salary_stats(salary):
    ...


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def parse_malformed(fp):
    ...
