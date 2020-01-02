# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:07:40 2019

@author: NewUsername
"""


# https://towardsdatascience.com/nlp-text-preprocessing-a-practical-guide-and-template-d80874676e79

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

os.chdir('C:/Users/NewUsername/vnineteen/A/from_where_scrape/spinneys/data_join_processing')
from resources.text_cleaning.functions_text_cleaning import *
from resources.topic_identification.functions_topic_identification import *


# open data-set
df = pd.read_csv(
    'resources/topic_identification/training_labeled.csv',
    encoding='unicode_escape')

ext_path = 'resources/topic_identification/'

# topic predict
topic_df = fast_process_io(df, 'class_simple', ext_path, 0.1, 50, 2)
# sentiment predict
sent_df = fast_process_io(df, 'sent_score', ext_path, 1, 80, 1)
# join dataframes
topic_sent_df = sent_df[['sent_score_pred_label', 'sent_score_pred_acc']]
topic_sent_df = topic_df.join(topic_sent_df)

