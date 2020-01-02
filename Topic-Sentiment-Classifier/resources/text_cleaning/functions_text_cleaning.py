# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 17:04:27 2019

@author: NewUsername
"""

from bs4 import BeautifulSoup
import spacy
import unidecode
from word2number import w2n
#from pycontractions import Contractions
import gensim.downloader as api
import numpy as np
import re
import nltk.data


nlp = spacy.load('en_core_web_sm')

# Choose model accordingly for contractions function
#model = api.load("glove-twitter-25")
# model = api.load("glove-twitter-100")
# model = api.load("word2vec-google-news-300")

#cont = Contractions(kv_model=model)
#cont.load_models()

# exclude words from spacy stopwords list
deselect_stop_words = ['no', 'not']
for w in deselect_stop_words:
    nlp.vocab[w].is_stop = False


def strip_html_tags(text):
    """remove html tags from text"""
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text(separator=" ")
    return stripped_text


def remove_whitespace(text):
    """remove extra whitespaces from text"""
    text = text.strip()
    return " ".join(text.split())


def remove_accented_chars(text):
    """remove accented characters from text, e.g. café"""
    text = unidecode.unidecode(text)
    return text


def expand_contractions(text):
    """expand shortened words, e.g. don't to do not"""
#    text = list(cont.expand_texts([text], precise=True))[0]
    return text


custom_remove_string = ['a','and','but','its', 'it']

def remove_custom_words(text):
    text = text.split()
    text = [word for word in text if word.lower() not in custom_remove_string]
    text = ' '.join(text)
    return text

def text_preprocessing(text, accented_chars=True, contractions=True,
                       convert_num=True, extra_whitespace=True,
                       lemmatization=False, lowercase=True, punctuations=False,
                       remove_html=True, remove_num=True, special_chars=True,
                       stop_words=False, remove_custom=False):
    if isinstance(text, float):
        return text
    elif len(text) > 0:
        # print('punctuation:   ' + str(punctuations))
        # print('stop_words:   ' + str(stop_words))
        # print('remove_custom:   ' + str(remove_custom))
        """preprocess text with default option set to true for all steps"""
        if remove_html == True: #remove html tags
            text = strip_html_tags(text)
        if extra_whitespace == True: #remove extra whitespaces
            text = remove_whitespace(text)
        if accented_chars == True: #remove accented characters
            text = remove_accented_chars(text)
        if contractions == True: #expand contractions
            text = expand_contractions(text)
        if lowercase == True: #convert all characters to lowercase
            text = text.lower()
        if ((remove_custom == True) and (len(text) > 2)):
            text = remove_custom_words(text)
    
        doc = nlp(text) #tokenise text
    
        clean_text = []
    
        for token in doc:
            flag = True
            edit = token.text
            # remove stop words
            if stop_words == True and token.is_stop and token.pos_ != 'NUM':
                flag = False
            # remove punctuations
            if punctuations == True and token.pos_ == 'PUNCT' and flag == True:
                flag = False
            # remove special characters
            if special_chars == True and token.pos_ == 'SYM' and flag == True:
                flag = False
            # remove numbers
            if remove_num == True and (token.pos_ == 'NUM' or token.text.isnumeric()) \
            and flag == True:
                flag = False
            # convert number words to numeric numbers
            if convert_num == True and token.pos_ == 'NUM' and flag == True:
                edit = w2n.word_to_num(token.text)
            # convert tokens to base form
            elif lemmatization == True and token.lemma_ != "-PRON-" and flag == True:
                edit = token.lemma_
            # append tokens edited and not removed to list
            if edit != "" and flag == True:
                clean_text.append(edit)
        return clean_text
    else:
        return text



#generate relative posting time
def posting_time_to_num(s):
    if s == 'in the last week':
        return 4
    elif s == 'a week ago':
        return 7
    elif s == '2 weeks ago':
        return 14
    elif s == '3 weeks ago':
        return 21
    elif s == '4 weeks ago':
        return 30
    elif s == 'a month ago':
        return 30
    elif s == '2 months ago':
        return 60
    elif s == '3 months ago':
        return 90
    elif s == '4 months ago':
        return 120
    elif s == '5 months ago':
        return 150
    elif s == '6 months ago':
        return 180
    elif s == '7 months ago':
        return 210
    elif s == '8 months ago':
        return 240
    elif s == '9 months ago':
        return 270
    elif s == '10 months ago':
        return 300
    elif s == '11 months ago':
        return 330
    elif s == '12 months ago':
        return 360
    elif s == 'a year ago':
        return 360
    elif s == '2 years ago':
        return 720
    elif s == '3 years ago':
        return 1080
    elif s == '4 years ago':
        return 1440
    elif s == '5 years ago':
        return 1800
    elif s == '6 years ago':
        return 2160
    elif s == '7 years ago':
        return 2520
    elif s == '8 years ago':
        return 2880
    elif s == ' 9 years ago':
        return 3240
    else:
        return 0


def replace_comma(x):
    try:
        return int(x.replace(',', ''))
    except AttributeError:
        return np.NaN


def tokenize_eng_text(col):
   col = nltk.sent_tokenize(col)
   # col = ' '.join(col)
   # print(col)
   return col


def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

