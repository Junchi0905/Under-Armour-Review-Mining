# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 13:24:09 2019

@author: NewUsername
"""


import pandas as pd

data = pd.read_csv('C:/Users/NewUsername/vnineteen/A/from_where_scrape/spinneys/other_locs/csvs/all.txt',
                   sep='\t', header=None)
data.columns = ["lat", "b", "c", "etc.",'as','ag','ght','h','g','adfg','ag','qwer','t']
