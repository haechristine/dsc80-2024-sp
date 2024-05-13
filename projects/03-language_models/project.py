# project.py


import pandas as pd
import numpy as np
from pathlib import Path
import re
import requests
import time


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_book(url):
    robots_url = "https://www.gutenberg.org/robots.txt"
    robots_resp = requests.get(robots_url)
    robots_content = robots_resp.text
    match = re.search(r"Crawl-delay: (\d+\.?\d*)", robots_content)
    pause_length = float(match.group(1)) if match else 0.5

    response = requests.get(url)
    content = response.text

 
    start = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"
    end = r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"
    start_match = re.search(start, content, re.DOTALL)
    end_match = re.search(end, content, re.DOTALL)
    book = content[start_match.end():end_match.start()]

    book = book.replace('\r\n', '\n')

    time.sleep(pause_length)

    return book


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def tokenize(book_string):
    book_string = re.sub(r'\n{2,}', '\x03\x02', book_string)
    
    tokens = ['\x02']
    
    pattern = r"[\w']+|[\.,!?;:()]|[\x03\x02]"

    tokens.extend(re.findall(pattern, book_string))

    tokens.append('\x03')
    if (tokens[1] == '\x03'):
        tokens = tokens[:1] + tokens[3:]
    if (tokens[-3] == '\x03'):
        second_last = len(tokens) - 2
        third_last = len(tokens) - 3
        tokens = tokens[:third_last] + tokens[second_last + 1:]
    return tokens


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


class UniformLM(object):


    def __init__(self, tokens):

        self.mdl = self.train(tokens)
        
    def train(self, tokens):
        ...
    
    def probability(self, words):
        ...
        
    def sample(self, M):
        ...


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


class UnigramLM(object):
    
    def __init__(self, tokens):

        self.mdl = self.train(tokens)
    
    def train(self, tokens):
        ...
    
    def probability(self, words):
        ...
        
    def sample(self, M):
        ...


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


class NGramLM(object):
    
    def __init__(self, N, tokens):
        # You don't need to edit the constructor,
        # but you should understand how it works!
        
        self.N = N

        ngrams = self.create_ngrams(tokens)

        self.ngrams = ngrams
        self.mdl = self.train(ngrams)

        if N < 2:
            raise Exception('N must be greater than 1')
        elif N == 2:
            self.prev_mdl = UnigramLM(tokens)
        else:
            self.prev_mdl = NGramLM(N-1, tokens)

    def create_ngrams(self, tokens):
        ...
        
    def train(self, ngrams):
        # N-Gram counts C(w_1, ..., w_n)
        ...
        
        # (N-1)-Gram counts C(w_1, ..., w_(n-1))
        ...

        # Create the conditional probabilities
        ...
        
        # Put it all together
        ...
    
    def probability(self, words):
        ...
    

    def sample(self, M):
        # Use a helper function to generate sample tokens of length `length`
        ...
        
        # Transform the tokens to strings
        ...
