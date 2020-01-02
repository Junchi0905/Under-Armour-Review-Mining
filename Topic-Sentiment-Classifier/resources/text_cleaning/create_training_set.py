# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 03:47:18 2019

@author: NewUsername
"""

from tqdm import tqdm
tqdm.pandas()
import os
from os import chdir, getcwd
wd=getcwd() # lets you navigate using chdir within jupyter/spyder
chdir(wd)
import pandas as pd
import nltk.data
import re

from resources.text_cleaning.functions_text_cleaning import *


def create_exploded_df(df):
    #df = df.rename(columns={"class": "label", "text": "text"})

    # remove empty comments
    df = df[~pd.isnull(df['text'])]
    df = df[~pd.isnull(df['user_href'])]
    # create new column to clean
    df['text2'] = df['text'].copy()
    # clean text
    df['text2'] = df['text2'].progress_apply(text_preprocessing)
    df['text2'] = df['text2'].apply(lambda x: ' '.join(x))

    # change these to periods (nltk tokenizer uses periods to tokenize)
    contra_words = ['however ','but ','although','nevertheless','and ']
    df['text2'] = df['text2'].str.replace('|'.join(contra_words), '. ')

    # remove the words associated for when google translated a review
    translated_terms = ['(translated google)', '(original)',
                        'translated by google''translate by google']
    df['text2'] = df['text2'].str.replace('|'.join(translated_terms), ' ')
    #replace punctuation with period
    df['text2'] = df['text2'].apply(lambda x: re.sub('[^\w\s]', '. ', x))
    # remove more than one space
    df.text2 = df.text2.replace('\s+', ' ', regex=True)

    # and also non english words
    df['text'] = df['text'].apply(remove_non_ascii)


    # tokenize text
    df['text2'] = df['text2'].progress_apply(tokenize_eng_text)
    # now remove periods (nltk tokenizes with periods)
    df['text2'] = df['text2'].apply(lambda x: [y.replace('.', '') for y in x])

    # explode dataframe using tokenized list
    # create df to explode
    dfe = df[['user_href','text2']]
    dfe = dfe.explode('text2')

    # before merging - erase text2 columns on df
    del df['text2']
    # join exploded df to original data
    dfe = pd.merge(dfe, df, how='left', on='user_href')

    # clean resulting text
    # remove more than one space
    dfe.text2 = dfe.text2.replace('\s+', ' ', regex=True)
    # remove custom words and stop words
    dfe['text2'] = dfe['text2'].progress_apply(text_preprocessing,
                                             stop_words=False,
                                             remove_custom=True)

    return dfe