# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 10:23:48 2019

@author: NewUsername
"""

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import reverse_geocoder as rg
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import numpy as np
from tqdm import tqdm
tqdm.pandas()
import numpy as np
import os
from p_tqdm import p_map
from os import chdir, getcwd
wd=getcwd()
chdir(wd)


if __name__ == '__main__':

    # set paths
    data_processing_path = 'C:/Users/NewUsername/vnineteen/A/from_where_scrape/spinneys/data_join_processing/'
    os.chdir(data_processing_path)
    from functions_geoloc import *

    joined_df_path = 'resources/loc_and_review_csvs/o_joined_df.csv'

    df = pd.read_csv(joined_df_path, encoding='utf-8')



    # GET GEO DATA ON "OTHER LOCS"
    df_cities_in = pd.read_csv('resources/geocoding/cities_list.csv', encoding='utf-8')


    # create a dataset of non null "other locs" long and lat
    # we will run this smaller dataset for geo coding then rejoin it to the df
    df_with_longlat = df[pd.notnull(df['other_loc_lat'])]
    print(df_with_longlat)

    df_with_longlat['latlong_tuple'] = tuple(list(zip(
        df_with_longlat['other_loc_lat'], df_with_longlat['other_loc_long'])))

    longlat_list = df_with_longlat['latlong_tuple'].tolist()
    # remove duplicates
    longlat_list = list(set(longlat_list))
    # erase this later
    len_list = len(longlat_list)
    print(len_list)
    longlat_list = longlat_list[:] # use this if the file is too big for one go


    # parallel the geocoding.. takes forever
    # https://github.com/swansonk14/p_tqdm
    geocode_result = p_map(get_coord, longlat_list, num_cpus=8)
    df2 = pd.DataFrame(geocode_result)
    print(df2)
    print()
    print(df2.dtypes)


    df2.to_csv('third_ten.csv', encoding='utf-8')





