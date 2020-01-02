# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 00:08:24 2019

@author: NewUsername
"""

import pandas as pd
import os

os.chdir('C:/Users/NewUsername/vnineteen/A/from_where_scrape/spinneys/data_join_processing/resources/geocoding')
df_abbrev = pd.read_csv('country_abbrev.csv', encoding='utf-8')

df = pd.read_csv('../../complete_df3.csv', encoding='utf-8')
df['country'] = df['country'].fillna('')
df['home_country'] = df['home_country'].fillna('')

df_abbrev = df_abbrev[['A2 (ISO)', 'COUNTRY']]
df_abbrev1 = df_abbrev.rename(columns={'A2 (ISO)': 'country_abbrev',
                                       'COUNTRY': 'country_name'})
df_abbrev2 = df_abbrev.rename(columns={'A2 (ISO)': 'home_country_abbrev',
                                       'COUNTRY': 'home_country_name'})



df = pd.merge(df, df_abbrev1, left_on='country', right_on='country_abbrev',
              how='left')

df = pd.merge(df, df_abbrev2, left_on='home_country', right_on='home_country_abbrev',
              how='left')

df.to_csv('complete4.csv', encoding='utf-8')
