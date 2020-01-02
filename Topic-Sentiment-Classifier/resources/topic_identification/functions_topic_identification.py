# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 11:11:39 2019

@author: NewUsername
"""


import warnings # needed for tqdm
warnings.simplefilter(action='ignore', category=FutureWarning)

# # to find city/state/country from lat, long
# import reverse_geocoder as rg
# from p_tqdm import p_map

# general libraries
import pandas as pd
import numpy as np
from tqdm import tqdm
tqdm.pandas()
from os import chdir, getcwd
wd=getcwd() # lets you navigate using chdir within jupyter/spyder
chdir(wd)

# ML libraries needed
from sklearn.naive_bayes import *
from sklearn.dummy import *
from sklearn.ensemble import *
from sklearn.neighbors import *
from sklearn.tree import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.calibration import *
from sklearn.linear_model import *
from sklearn.multiclass import *
from sklearn.svm import *

import fasttext
import csv
from tqdm import tqdm
tqdm.pandas()

# other libraries for topic identification
import spacy
sp = spacy.load('en_core_web_sm')
from nltk.corpus import stopwords

from resources.text_cleaning.functions_text_cleaning import *


def perform(classifiers, vectorizers, train_data, test_data):
    df_out = pd.DataFrame()
    classifier_list = []
    vectorizer_list = []
    score_list = []
    for classifier in classifiers:
        for vectorizer in vectorizers:
            string = ''
            string += classifier.__class__.__name__ + ' with ' + vectorizer.__class__.__name__

            # train
            vectorize_text = vectorizer.fit_transform(train_data.text)
            classifier.fit(vectorize_text, train_data.label)

            # score
            vectorize_text = vectorizer.transform(test_data.text)
            score = classifier.score(vectorize_text, test_data.label)
            string += '. Has score: ' + str(score)
            print(string)
            classifier_list.append(str(classifier.__class__.__name__))
            vectorizer_list.append(str(vectorizer.__class__.__name__))
            score_list.append(str(score))
    df_out['classifier'] = classifier_list
    df_out['vectorizer'] = vectorizer_list
    df_out['score'] = score_list
    return df_out


def perform_sentiment(classifiers, vectorizers, train_data, test_data):
    df_out = pd.DataFrame()
    classifier_list = []
    vectorizer_list = []
    score_list = []
    for classifier in classifiers:
        for vectorizer in vectorizers:
            string = ''
            string += classifier.__class__.__name__ + ' with ' + vectorizer.__class__.__name__

            # train
            vectorize_text = vectorizer.fit_transform(train_data.text)
            classifier.fit(vectorize_text, train_data.sent_score)

            # score
            vectorize_text = vectorizer.transform(test_data.text)
            score = classifier.score(vectorize_text, test_data.sent_score)
            string += '. Has score: ' + str(score)
            print(string)
            classifier_list.append(str(classifier.__class__.__name__))
            vectorizer_list.append(str(vectorizer.__class__.__name__))
            score_list.append(str(score))
    df_out['classifier'] = classifier_list
    df_out['vectorizer'] = vectorizer_list
    df_out['score'] = score_list
    return df_out


def predict_func(text):
    if len(text) > 0:
        vectorize_message = vectorizer.transform([text])
        predict = classifier.predict(vectorize_message)[0]
        predict_proba = classifier.predict_proba(vectorize_message).tolist()
        predict_proba_first = predict_proba[0][0]
        predict_proba_second = predict_proba[0][1]
        print(str(predict))
        print(text)
        print(str(predict_proba_first))
        print(str(predict_proba_second))
        print()
        return pd.Series([predict, predict_proba_first, predict_proba_second])

    else:
        print('couldnt do it....')
        return pd.Series([None,None,None])


def prep_df_labeling(df):
    df['label']=['__label__'+s.replace(' or ', '$').replace(
        ', or ','$').replace(',','$').replace(' ','_').replace(
            ',','__label__').replace('$$','$').replace(
                '$',' __label__').replace('___','__') for s in df['label']]
    df['text']= df['text'].replace('\n',' ', regex=True).replace('\t',' ', regex=True)
    df['text'] = df['text'].progress_apply(text_preprocessing, punctuations=True, stop_words=True,remove_custom=True)
    df['text'] = df['text'].apply(lambda x: ' '.join(x))
    return df


def fast_process_io(train_csv_df_path, to_run_df, label, ext_path, lr_in,
                    epoch_in, ngrams_in, size_each, threshold_in, single_multi):

    train_csv_df = pd.read_csv(train_csv_df_path, encoding='unicode_escape')

    train_csv_df = train_csv_df.rename(columns={label: "label"})
    train_csv_df['orig_label'] = train_csv_df['label'].copy()
    train_csv_df = train_csv_df[pd.notnull(train_csv_df['label'])] # drop not classified tweets
    # train_csv_df = train_csv_df[train_csv_df['label'] != 'no_topic']
    # train_csv_df = train_csv_df[train_csv_df['label'] != 'neutral']
    train_csv_df = train_csv_df[['label', 'text']] # remove any extra columns

    print('training dataset prep')
    train_csv_df = prep_df_labeling(train_csv_df)

    # check distribution
    print(train_csv_df.groupby('label').count())
    train_csv_df = train_csv_df.groupby('label').filter(lambda x : len(x)>10)


    # make equal number of each label
    size = size_each        # sample size
    replace = True  # with replacement (if you want it to select same row again)
    fn = lambda obj: obj.loc[np.random.choice(obj.index, size, replace),:]
    train_csv_df = train_csv_df.groupby('label', as_index=False).apply(fn)

    train_csv_df['label_text'] = train_csv_df['label'] + ' ' + train_csv_df['text']
    train_csv_df = train_csv_df['label_text']

    # reset index before exporting
    train_csv_df = train_csv_df.reset_index(drop=True)
    # shuffle order ()
    train_csv_df = train_csv_df.sample(frac=1, random_state=123).reset_index(drop=True)

    train_csv_df.iloc[0:int(len(train_csv_df)*0.8)].to_csv(ext_path +
                                       str() + '_train.txt',
                                       index=False, header=False,
                                       sep="\t", quoting=csv.QUOTE_NONE,
                                       quotechar="",  escapechar="\\")
    train_csv_df.iloc[int(len(train_csv_df)*0.8):].to_csv(ext_path +
                                       str() + '_valid.txt',
                                       index=False, header=False,
                                       sep="\t", quoting=csv.QUOTE_NONE,
                                       quotechar="",  escapechar="\\")


    train_in = ext_path + str() + '_train.txt'
    valid_in = ext_path + str() + '_valid.txt'

    print('exported training and valid sets')
    if single_multi == 'single':
        model = fasttext.train_supervised(input=train_in,
                                          lr=lr_in, epoch=epoch_in,
                                          wordNgrams=ngrams_in)
    elif single_multi == 'multi':
        model = fasttext.train_supervised(input=train_in,
                                          lr=lr_in, epoch=epoch_in, wordNgrams=ngrams_in,
                                          dim=50, loss='ova')

    print()
    print('train df accuracy is...')
    print(model.test(train_in))
    print()
    print('valid df accuracy is...')
    print(model.test(valid_in))

    print()
    print('prepare entire dataset')

    # remove blank comments
    to_run_df = to_run_df[~pd.isnull(to_run_df['text2'])]
    to_run_df = to_run_df[to_run_df['text2'] != '']
    to_run_df['text'] = to_run_df['text2'].apply(lambda x: ' '.join(x) if len(x) > 0 else '')
    to_run_df = to_run_df[pd.notnull(to_run_df['text'])]
    to_run_df['text'] = to_run_df['text'].progress_apply(text_preprocessing, punctuations=True, stop_words=True,remove_custom=True)
    to_run_df['text'] = to_run_df['text'].apply(lambda x: ' '.join(x))



    def fasttext_run_single(df, label):
        df['fasttext_results'] = df['text'].apply(
            lambda x: model.predict(x, k=1, threshold=threshold_in))
        df['fasttext_results'] = df['fasttext_results'].apply(
            lambda x: [element for tupl in x for element in tupl])
        # reset df_to_join index before adding in the prediction df
        df = df.reset_index(drop=True)
        # creates a dataframe with two columns for predication and accuracy
        # we join this df to the main dataframe
        pred_df = pd.DataFrame(
            df['fasttext_results'].values.tolist(), columns = [
                (str(label) + '_pred_label'), (str(label) + '_pred_acc')])
        df = df.join(pred_df)
        return df 


    def fasttext_run_multi(df, label):
        # predict the row based on model
        df['fasttext_results'] = df['text'].apply(
            lambda x: model.predict(x, k=-1, threshold=threshold_in))
        # convert resulting tuple into an array
        df['fasttext_results'] = df['fasttext_results'].apply(
            lambda x: [element for tupl in x for element in tupl])
        # reset df_to_join index before adding in the prediction df
        df = df.reset_index(drop=True)
        # set the maximum number of results
        df['fasttext_results'] = df['fasttext_results'].apply(lambda x:
                                                              x[:2])
        print(df['fasttext_results'])
# =============================================================================
#         def multi_result_split(row):
#             if len(row) > 2:
#                 print('11')
#                 return pd.Series(row[0], row[2], row[1], row[3])
#             elif len(row) == 2:
#                 print('22')
#                 return pd.Series(row[0],row[1], '', '')
#             elif len(row) < 2:
#                 return pd.Series('', '', '', '')
#
#         df[[(str(label) + '_pred_label'),
#             (str(label) + '_pred_acc'),
#             (str(label) + '_pred_label_2'),
#             (str(label) + '_pred_acc_2')]] = df['fasttext_results'].apply(multi_result_split)
# =============================================================================

        # creates a dataframe with two columns for predication and accuracy
        # we join this df to the main dataframe
        pred_df = pd.DataFrame(
            df['fasttext_results'].values.tolist(), columns = [
                (str(label) + '_pred_label'), (str(label) + '_pred_acc')])
        df = df.join(pred_df)
        return df


    if single_multi == 'single':
        df_orig_result = fasttext_run_single(to_run_df, label)
    elif single_multi == 'multi':
        df_orig_result = fasttext_run_multi(to_run_df, label)

    return df_orig_result
