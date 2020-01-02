# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 12:20:41 2019

@author: NewUsername
"""
import reverse_geocoder as rg
from multiprocessing import Pool
import pandas as pd
import numpy as np
from tqdm import tqdm
tqdm.pandas()
import numpy as np
import os

# =============================================================================
# def get_coord(lat, long):
#     coord_list = [lat, long]
#     coord_tuple = tuple(coord_list)
#     print(coord_tuple)
#     try:
#         results = rg.search(coord_tuple)
#         results = results[0]
#         return results
#     except:
#         print('couldnt identify long lat!!')
#         return{'lat': np.nan, 'lon': np.nan, 'name': '',
#                'admin1': '', 'admin2': '', 'cc': ''}
# =============================================================================

def get_coord(coord_tuple):
    try:
        results = rg.search(coord_tuple)
        results = results[0]
        results['coord_tuple'] = coord_tuple
        return results
    except:
        print('couldnt identify long lat!!')
        return{'lat': np.nan, 'lon': np.nan, 'name': '',
                'admin1': '', 'admin2': '', 'cc': '', 'coord_tuple': coord_tuple}


# =============================================================================
# def longlat_loop(df_with_longlat):
#     df_with_longlat[['city_lat', 'city_long', 'city', 'region',
#         'general_region', 'country']] = df_with_longlat.progress_apply(
#             lambda x: pd.Series(
#             get_coord(x['other_loc_lat'], x['other_loc_long'])), axis = 1)
#     return df_with_longlat
#
#
# def parallelize_df(df, func, n_cores=4):
#     df_split = np.array_split(df, n_cores)
#     pool = Pool(n_cores)
#     df = pd.concat(pool.map(func, df_split))
#     pool.close()
#     pool.join()
#     return df
# =============================================================================


def groupby_mode(x):
    s = x.value_counts()
    print(s)
    total_num = len(x)
    top_place = s.index[0]
    top_place_count = x.value_counts()[0]

    if total_num > 45 and top_place_count / total_num > 0.27:
        home_place = top_place
    elif total_num > 6 and top_place_count / total_num > 0.5:
        home_place = top_place
    else:
        home_place = np.nan

    return np.nan if len(s) == 0 else home_place