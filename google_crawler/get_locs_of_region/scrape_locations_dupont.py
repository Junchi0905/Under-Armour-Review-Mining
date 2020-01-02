# -*- coding: utf-8 -*-
"""
Created on Oct 2018

@edited by: Theo G
"""

from selenium import webdriver
import time
import pandas as pd
from pathlib import Path
import os
from os import chdir, getcwd
wd=getcwd() # lets you navigate using chdir within jupyter/spyder
chdir(wd)
import random

# set directory path
folder_path = 'C:/Users/NewUsername/Documents/GitHub/basil_repository/google_example_spinneys/get_locs_of_region'
# set the path to your driver
browser = webdriver.Chrome(executable_path=r"C:/Users/NewUsername/VENV/chromedriver.exe")
# import types of locations (should be placed in your folder directory)
alltypesfile = 'dc_placetypes.txt'
# set the zoom level.. 16 or 17z seems like it picks up most locations
# you can check zoom level in the url of google.com/maps when you look a location up
zoom_level = '16z'
# neighborhood area selection, get this from the google URL 
cities = "@42.3678856,-71.0619503"



os.chdir(folder_path)
from functions_get_original_locations import *

alltypes = []
# open file and read the content in a list
with open(alltypesfile, 'r') as filehandle:  
    for line in filehandle:
        # remove linebreak which is the last character of the string
        currentPlace = line[:-1]
        # add item to the list
        alltypes.append(currentPlace)
# use this to set start and end points for your scrape if needed
alltypes = alltypes[:]

if not os.path.exists('csvs'):
    os.makedirs('csvs')
    print('made csv save folder')
os.chdir('csvs') # set directory for saved files

# no multiprocessing on this one.. sorry
for i in alltypes:
    scrape(i, cities, browser, zoom_level)

browser.quit() # quit after everything is done



