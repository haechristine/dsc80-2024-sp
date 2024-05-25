# lab.py


import pandas as pd
import numpy as np
import os
import re


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def match_1(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_1("abcde]")
    False
    >>> match_1("ab[cde")
    False
    >>> match_1("a[cd]")
    False
    >>> match_1("ab[cd]")
    True
    >>> match_1("1ab[cd]")
    False
    >>> match_1("ab[cd]ef")
    True
    >>> match_1("1b[#d] _")
    True
    """
    pattern = r'^..[\[]..[\]].*$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_2(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_2("(123) 456-7890")
    False
    >>> match_2("858-456-7890")
    False
    >>> match_2("(858)45-7890")
    False
    >>> match_2("(858) 456-7890")
    True
    >>> match_2("(858)456-789")
    False
    >>> match_2("(858)456-7890")
    False
    >>> match_2("a(858) 456-7890")
    False
    >>> match_2("(858) 456-7890b")
    False
    """
    pattern = r'^\(858\) \d{3}-\d{4}$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_3(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_3("qwertsd?")
    True
    >>> match_3("qw?ertsd?")
    True
    >>> match_3("ab c?")
    False
    >>> match_3("ab   c ?")
    True
    >>> match_3(" asdfqwes ?")
    False
    >>> match_3(" adfqwes ?")
    True
    >>> match_3(" adf!qes ?")
    False
    >>> match_3(" adf!qe? ")
    False
    """
    pattern = r'^[a-zA-Z0-9\s?]{5,9}\?$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_4(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_4("$$AaaaaBbbbc")
    True
    >>> match_4("$!@#$aABc")
    True
    >>> match_4("$a$aABc")
    False
    >>> match_4("$iiuABc")
    False
    >>> match_4("123$$$Abc")
    False
    >>> match_4("$$Abc")
    True
    >>> match_4("$qw345t$AAAc")
    False
    >>> match_4("$s$Bca")
    False
    >>> match_4("$!@$")
    False
    """
    pattern = r'^\$[^abc$]*\$[Aa]+[Bb]+[Cc]+$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_5(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_5("dsc80.py")
    True
    >>> match_5("dsc80py")
    False
    >>> match_5("dsc80..py")
    False
    >>> match_5("dsc80+.py")
    False
    """
    pattern = r'^[a-zA-Z0-9_]+\.py$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_6(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_6("aab_cbb_bc")
    False
    >>> match_6("aab_cbbbc")
    True
    >>> match_6("aab_Abbbc")
    False
    >>> match_6("abcdef")
    False
    >>> match_6("ABCDEF_ABCD")
    False
    """
    pattern = r'^[a-z]+_[a-z]+$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_7(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_7("_abc_")
    True
    >>> match_7("abd")
    False
    >>> match_7("bcd")
    False
    >>> match_7("_ncde")
    False
    """
    pattern = r'^_.*_$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None



def match_8(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_8("ASJDKLFK10ASDO")
    False
    >>> match_8("ASJDKLFK0ASDo!!!!!!! !!!!!!!!!")
    True
    >>> match_8("JKLSDNM01IDKSL")
    False
    >>> match_8("ASDKJLdsi0SKLl")
    False
    >>> match_8("ASDJKL9380JKAL")
    True
    """
    pattern = r'^[^Oi1]*$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None



def match_9(string):
    '''
    DO NOT EDIT THE DOCSTRING!
    >>> match_9('NY-32-NYC-1232')
    True
    >>> match_9('ca-23-SAN-1231')
    False
    >>> match_9('MA-36-BOS-5465')
    False
    >>> match_9('CA-56-LAX-7895')
    True
    >>> match_9('NY-32-LAX-0000') # If the state is NY, the city can be any 3 letter code, including LAX or SAN!
    True
    >>> match_9('TX-32-SAN-4491')
    False
    '''
    pattern = r'^(NY-\d{2}-[A-Z]{3}-\d{4}|CA-\d{2}-(SAN|LAX)-\d{4})$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_10(string):
    '''
    DO NOT EDIT THE DOCSTRING!
    >>> match_10('ABCdef')
    ['bcd']
    >>> match_10(' DEFaabc !g ')
    ['def', 'bcg']
    >>> match_10('Come ti chiami?')
    ['com', 'eti', 'chi']
    >>> match_10('and')
    []
    >>> match_10('Ab..DEF')
    ['bde']
    
    '''
    string = string.lower()
    string = re.sub(r'[^0-9b-z]', '', string)
    return [string[i:i+3] for i in range(0, len(string), 3) if i+3 <= len(string)]


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def extract_personal(s):
    email_reg = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    ssn_reg = r'\b\d{3}-\d{2}-\d{4}\b'
    bitcoin_reg = r'\b1[a-km-zA-HJ-NP-Z0-9]{26,35}\b'
    street_reg = r'\d{2,5}\s\w+(?:\s\w+)*\s(?:Street|St|Avenue|Ave|Boulevard|Blvd|Court|Ct|Drive|Dr|Lane|Ln|Parkway|Pkwy|Road|Rd|Trail|Trl|Way|Plaza|Plz|Terrace|Ter|Place|Pl|Circle|Cir|Square|Sq|Loop|Lp)'

    email = re.findall(email_reg, s)
    ssn = re.findall(ssn_reg, s)
    bitcoin = re.findall(bitcoin_reg, s)
    street = re.findall(street_reg, s)

    return (email, ssn, bitcoin, street)


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def tfidf_data(reviews_ser, review):
    words = review.replace('  ', ' ').split(' ')
    review_len = len(words)

    ser_len = len(reviews_ser)

    cnt = {}
    tf = {}
    idf = {}
    tfidf = {}

    for word in words:
        count = words.count(word)
        cnt[word] = count

        freq = count/review_len
        tf[word] = freq

        word_appears = sum(1 for review in reviews_ser if re.search(r'\b' + word + r'\b', review))
        inverse = np.log(ser_len / word_appears)
        idf[word] = inverse

        tfidf[word] = freq * inverse

    return pd.DataFrame({'cnt':cnt, 'tf':tf, 'idf':idf, 'tfidf':tfidf})


def relevant_word(out):
    best = tfidf_df['tfidf'].idxmax()
    return best


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def hashtag_list(tweet_text):
    total_hash = []
    for tweet in tweet_text:
        hashtag = re.findall(r'#[^\s]*', tweet)
        hashtag = list(map(lambda x: x[1:], hashtag))
        total_hash.append(hashtag)
    return pd.Series(total_hash)


def most_common_hashtag(tweet_lists):
    count = {}
    for tags in tweet_lists:
        for tag in tags:
            if tag not in count:
                count[tag] = 1
            else:
                count[tag] += 1

    hash_list = []
    for tags in tweet_lists:
        if len(tags) == 0:
            hash_list.append(np.nan)
        elif len(tags) == 1:
            hash_list.append(tags[0])
        else:
            common = ''
            for i in range(len(tags) - 1):
                if count[tags[i]] <= count[tags[i+1]]:
                    common=tags[i+1]
                else:
                    common=tags[i]
            hash_list.append(common)

    return pd.Series(hash_list)


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------

def tag_helper(tweet):
    total = []
    for text in tweet:
        tag = re.findall(r'@[\w]+', text)
        tag = list(map(lambda x: x[1:], tag))
        total.append(tag)
    return pd.Series(total).apply(lambda x: len(x))

def link_helper(tweet):
    total = []
    for text in tweet:
        link = re.findall(r'https*:\/\/[^\s]*', text)
        link = list(map(lambda x: x[1:], link))
        total.append(link)
    return pd.Series(total).apply(lambda x: len(x))

def clean_helper(tweet):
    cleaned = []
    for text in tweet:
        text = re.sub(r'RT', ' ', text)
        text = re.sub(r'@[\w]+', ' ', text)
        text = re.sub(r'https*:\/\/[^\s]*', ' ', text)
        text = re.sub(r'#[^\s]*', ' ', text)
        text = re.sub(r'[^A-Za-z\d\s]+', ' ', text)
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        cleaned.append(text)
    return pd.Series(cleaned)

def create_features(ira):
    df = ira.index
    
    num_hashtags = {}
    mc_hashtags = {}
    num_tags = {}
    num_links = {}
    is_retweet = {}
    text = {}

    texts = ira['text']
    hashtags = hashtag_list(texts)

    common_hashtags = most_common_hashtag(hashtags)

    tags_counts = tag_helper(texts)

    link_counts = link_helper(texts)

    cleaned_texts = clean_helper(texts)
    
    for i in df:
        hashtag_len = len(hashtags.iloc[i])
        num_hashtags[i] = hashtag_len
        
        mc_hashtags[i] = common_hashtags.iloc[i]

        num_tags[i] = tags_counts.iloc[i]

        num_links[i] = link_counts.iloc[i]

        is_retweet[i] = texts.iloc[i][:2] == 'RT'

        text[i] = cleaned_texts.iloc[i]
        
    return pd.DataFrame({
        'text': text,
        'num_hashtags': num_hashtags,
        'mc_hashtags': mc_hashtags,
        'num_tags': num_tags,
        'num_links': num_links,
        'is_retweet':is_retweet
    })
