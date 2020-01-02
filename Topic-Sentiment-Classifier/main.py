# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 21:55:46 2019

@author: NewUsername
"""

from bs4 import BeautifulSoup
import fasttext
import os
import pandas as pd
from io import StringIO
from word2number import w2n
import csv
import unidecode
from pycontractions import Contractions
import gensim.downloader as api
from tqdm import tqdm
tqdm.pandas()
import numpy as np

from tqdm import tqdm
tqdm.pandas()
import os
from os import chdir, getcwd
wd=getcwd() # lets you navigate using chdir within jupyter/spyder
chdir(wd)
import pandas as pd
import nltk.data
import re
import json
from datetime import datetime, timedelta

os.chdir('C:\\Users\\junch\\Desktop\\Basil Lab\\basil_repository-master\\google_example_spinneys\\data_join_processing')
from resources.text_cleaning.functions_text_cleaning import *
from resources.topic_identification.functions_topic_identification import *
from resources.text_cleaning.functions_text_cleaning import *
from resources.text_cleaning.create_training_set import *
from resources.geocoding.functions_geoloc import *



# prepare
# import df
df = pd.read_csv('C:\\Users\\junch\\Desktop\\Basil Lab\\csvs\\Under Armour , 20 City Blvd. West, Orange.csv',
                 encoding='utf-8')
# remove any rows without user urls -- these are useless
df = df[~pd.isnull(df['user_href'])]

# clean posting date
df['review_data'] = df['review_data'].apply(posting_time_to_num)
df['review_data'] = -df['review_data']
# clean stars column
df.ratings = df.ratings.apply(lambda x: str(x).strip().split(' ')[0])


# create dataset to prepare text
df_with_reviews = df[~pd.isnull(df['text'])]
# create exploded df
exploded_df = create_exploded_df(df_with_reviews)
# SENTIMENT AND TOPIC IDENTIFICATION
# set a relaftive path where the training and valid datasets are saved
ext_path = 'resources/topic_identification/'
# topic predict ('class_simple' is the name of the topic column in the training df)
#function args are:
#training dataset path,   df to run,   column title of labels,
#extension path, learning rate,   epoch #s,   ngrams,
# of rows per topic,   threshold,   single or multi classification'''

exploded_df = exploded_df[~pd.isnull(exploded_df['text'])]
exploded_df = exploded_df[exploded_df['text2'] != '']

# create original text column
exploded_df['orig_text'] = exploded_df['text'].copy()

topic_df = fast_process_io(
    'resources/topic_identification/training_labeled.csv',
    exploded_df, 'class_simple', ext_path, 0.1, 50, 2, 100, 0.6, 'multi')
# sentiment predict ('sent_score' is the name of sentiment good/bad column in training df)
sent_df = fast_process_io(
    'resources/topic_identification/training_labeled.csv',
    exploded_df, 'sent_score', ext_path, 1, 80, 1, 300, 0.6, 'single')
# join dataframes
topic_sent_df = sent_df[['sent_score_pred_label', 'sent_score_pred_acc']]
topic_sent_df = topic_df.join(topic_sent_df)
#erase the extra column generated
del topic_sent_df['fasttext_results']

# create temporary df while i fix this
cached = topic_sent_df.copy()
topic_sent_df = cached.copy()

# make inaccurate prediction rows blank.. lets say 93.4% and below
# topic_sent_df.loc[topic_sent_df['sent_score_pred_acc'] < 0.86, 'sent_score_pred_label'] = np.nan
# topic_sent_df.loc[topic_sent_df['class_simple_pred_acc'] < 0.92, 'class_simple_pred_label'] = np.nan
# remove any pred acc and label if its only one word response
def acc_len_change(row):
    if len(row['text2']) <= 1:
        # row['class_simple_pred_label'] = np.nan
        # row['sent_score_pred_label'] = np.nan
        return pd.Series([np.nan, np.nan])
    else:
        return pd.Series([row['class_simple_pred_label'], row['sent_score_pred_label']])


topic_sent_df[['class_simple_pred_label', 'sent_score_pred_label']] = topic_sent_df.apply(acc_len_change, axis=1)
# topic_sent_df.apply(acc_len_change, axis=1)

# clean up the label columns
topic_sent_df['class_simple_pred_label'] = topic_sent_df[
    'class_simple_pred_label'].fillna('')
topic_sent_df['class_simple_pred_label'] = topic_sent_df[
    'class_simple_pred_label'].apply(lambda x: x.replace('__label__', ''))
topic_sent_df['sent_score_pred_label'] = topic_sent_df[
    'sent_score_pred_label'].fillna('')
topic_sent_df['sent_score_pred_label'] = topic_sent_df[
    'sent_score_pred_label'].apply(lambda x: x.replace('__label__', ''))
# clean up sentiment
topic_sent_df['sent_score_pred_label'] = topic_sent_df['sent_score_pred_label'].replace('good', 1)
topic_sent_df['sent_score_pred_label'] = topic_sent_df['sent_score_pred_label'].replace('bad', -1)
topic_sent_df['sent_score_pred_label'] = topic_sent_df['sent_score_pred_label'].replace('neutral', 0)
# eventually should run averages here for each person and by location (groupby topic)
# going to skip doing this for now because I'm assuming people dont have the
# same topic twice in a single review..

# remove any rows where there is no text or no topic or sentiment
topic_sent_df = topic_sent_df.dropna(subset=['class_simple_pred_label'])
# fill na rows for sentiment
# topic_sent_df['sent_score_pred_label'] = topic_sent_df['sent_score_pred_label'].fillna(value='neutral')

# create dataset to append at the bottom (rows without reviews)
df_no_reviews = df[pd.isnull(df['text'])]
# join exploded df with no reviews df (we need no reviews users for
# joining later with other locations reviewed + geolocations)
all_perception_df = pd.concat([topic_sent_df, df_no_reviews], ignore_index=True)
all_perception_df = all_perception_df.reset_index(drop=True)


# JSON EXPORT OF PERCEPTIONS
perception_json_out = all_perception_df.copy()
perception_json_out = perception_json_out[
    perception_json_out['class_simple_pred_label'] != 'no_topic']
perception_json_out = perception_json_out[
    perception_json_out['class_simple_pred_label'] != '']
perception_json_out = perception_json_out.reset_index(drop=True)
perception_json_out = perception_json_out[pd.notnull(
    perception_json_out['class_simple_pred_label'])]

# drop extra columns
drop_perception_cols = ['ID','user_href','class_simple_pred_acc','name_of_loc','sent_score_pred_acc','text','text2']
# rename topic and sent before export
perception_json_out = perception_json_out.rename(columns={'class_simple_pred_label': 'topic',
                                                    'sent_score_pred_label': 'sentiment',
                                                    'review_data':'review_date'})

# convert review date days ago to date for export
def days_to_date(row):
    days_ago = row * -1
    scrape_date = datetime(2019, 10, 10)
    date_back = scrape_date - timedelta(days=days_ago)
    return date_back
perception_json_out['review_date'] = perception_json_out['review_date'].apply(days_to_date)



j = (perception_json_out.groupby(['name_only', 'address_only', 'avg_review',
                   'num_reviews', 'lat', 'long', 'loc_type'], as_index=False)
             .apply(lambda x: x[['topic','ratings',
                                 'review_date','sentiment']].to_dict('r'))
             .reset_index()
             .rename(columns={0:'perception'})
             .to_json(orient='records'))

json_outfile = open('json_spinneys_out.txt', 'w')
json_outfile.write(j)
json_outfile.close()
perception_json_out.to_csv('spinneys_out_perception.csv', encoding='utf-8')
