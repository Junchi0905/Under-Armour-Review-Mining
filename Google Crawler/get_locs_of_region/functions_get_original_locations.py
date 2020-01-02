

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
def scrape(shop, city_in, browser, zoom_level):
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
