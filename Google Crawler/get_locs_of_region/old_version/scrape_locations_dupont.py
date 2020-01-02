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
import random


# check if xpath exists. this is used later in the scrape to check if we should keep pressing the pg down/ end
# button, or to stop
def hasXpath(xpath):
    try:
        browser.find_element_by_xpath(xpath)
        return True
    except:
        return False


#main scrape function
def scrape(shop, city_in, browser):
    # url is effectively creating a URL to input as if you searched it manually
    url = 'https://www.google.com/maps/search/'+ shop + '/' + city_in + ',' + zoom_level + '?hl=en'
    browser.get(url) # go to the url
    time.sleep(6) # make sure the url loads fully before doing anything else
    
    df_out_big = pd.DataFrame() # the eventual export dataset which we append all scraped info to
    

    n = 0 # print out the number of pages we have searched
    path_exists = True
    url_change = True


    zoom_level_float = float(zoom_level.split('z')[0])

    # to give some leeway, we'll minus one so it allows it to zoom out slightly
    zoom_level_float = zoom_level_float - 2
    currenturlzoom = zoom_level_float 
    nzoomedout = 0 # count number of times its zoomed out too far


# you can also add and url_change == True to the while loop
    while path_exists and nzoomedout < 2:
        time.sleep(random.randrange(4,6)) # this is important so that when you click next page, it fully loads
		

        names = browser.find_elements_by_xpath("//h3[@class = 'section-result-title'] ")
        name_of_loc = [x.text for x in names]
        ratings = browser.find_elements_by_xpath("//span[@class = 'cards-rating-score'] ")
        ratings_of_loc = [x.text for x in ratings]
        numbers = browser.find_elements_by_xpath("//span[@class = 'section-result-num-ratings'] ")
        number_of_reviews = [x.text for x in numbers]
        locations = browser.find_elements_by_xpath("//span[@class = 'section-result-location'] ")
        address_of_loc = [x.text for x in locations]

        type_in = browser.find_elements_by_xpath(
            '//span[@class="section-result-details"]')
        type_loc = [x.text for x in type_in]

        price_level_in = browser.find_elements_by_xpath(
        '//span[@class="section-result-cost"]')
        price_level = [x.text for x in price_level_in]

        # printing the length of each of the arrays we collected
        print(len(ratings_of_loc), len(number_of_reviews), len(name_of_loc), len(number_of_reviews))

        df_out = pd.DataFrame() #create an empty dataframe to append our rows into
        df_out['name_of_loc'] = pd.Series(name_of_loc)
        df_out['ratings_of_loc'] = pd.Series(ratings_of_loc)
        df_out['address_of_loc'] = pd.Series(address_of_loc)
        df_out['number_of_reviews'] = pd.Series(number_of_reviews)
        df_out['type_loc'] = pd.Series(type_loc)
        df_out['price_level'] = pd.Series(price_level)

        print('printing dataframe\n')

        print(df_out)
        
        button_next = "//button[@id = 'n7lv7yjyC35__section-pagination-button-next']"
        path_exists = hasXpath(button_next)

        currenturl = browser.current_url
        currenturl_test = str(currenturl).split('/')[6][:12]
        print('current url:   ' + currenturl_test)

        url_test = str(url).split('/')[6][:12]
        print('current url:   ' + url_test)


        # zoom level in url
        currenturlzoom = str(currenturl).split('@')[1].split('z')[0].split(',')[2]
        currenturlzoom = float(currenturlzoom)
        print(' current zoom in url is:      ' + str(currenturlzoom))

        if currenturlzoom < zoom_level_float:
            nzoomedout += 1
            print('zoomed out too far!!')

        # this doesn't work btw... it can change and itll still keep scraping
        if  currenturl_test == url_test:
            url_change = True
        else:
            url_change = False

        df_out_big = df_out_big.append(df_out) #append the data from this page to the larger dataset

        try:
            forward_button = browser.find_element_by_xpath("//button[@id = 'n7lv7yjyC35__section-pagination-button-next'] ")
            forward_button.click()
        except:
            print("retry failed in clicking the next page button")
            break
        
        time.sleep(random.randrange(4,6)) #wait before clicking the next page
        n += 1
        print(n)

    outputname = shop + '.csv' 

    df_out_big.to_csv(outputname, encoding='utf-8')
    print('exported the dataset:  ' + outputname)
    time.sleep(random.randrange(5,9))


# set the zoom level.. 16 or 17z seems like it picks up most locations
# you can check zoom level in the url of google.com/maps when you look a location up
zoom_level = '16z'

# import types of locations
alltypesfile = Path(r"C:/Users/NewUsername/VENV/A/from_where_scrape/britain/locs/dc_placetypes.txt")
alltypes = []
# open file and read the content in a list
with open(alltypesfile, 'r') as filehandle:  
    for line in filehandle:
        # remove linebreak which is the last character of the string
        currentPlace = line[:-1]
        # add item to the list
        alltypes.append(currentPlace)

alltypes = alltypes[57:]

# set the path to your geckodriver, which you can download from online
browser = webdriver.Chrome(executable_path=r"C:/Users/NewUsername/VENV/chromedriver.exe")

directorypath = Path(r"C:/Users/NewUsername/VENV/A/from_where_scrape/britain/locs/csvs")
os.chdir(directorypath)


# city selection, get this from the google URL when you search a specific geographic region
dc = "@38.9191898,-77.0695937"
ny = "@40.7492184,-73.9812202"
boston = "@42.3678856,-71.0619503"
maryland = ",+maryland/@38.6875198,-77.8348248"
chicago = "@41.8249496,-87.8135899"
dupont = '@38.9012052,-77.045355'
dhaka = '@23.7166611,90.3906796'
gloucester = '@42.6338482,-70.7273367'
arlington = '@38.878071,-77.118287'
seaport = '@42.3449273,-71.0387456'
west_ashley = '@32.8030143,-80.0469213'
dupont ='@38.9046304,-77.0314815'
london = '@51.4573128,-0.122152'

# select the city of study
cities = london


# alltypes = ['accounting']

# =============================================================================
# =============================================================================
# # # scrape your choices
# =============================================================================
# =============================================================================
for i in alltypes:
    scrape(i, cities, browser)



browser.quit() # quit after everything is done



