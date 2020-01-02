from selenium import webdriver
from time import sleep
import multiprocessing
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import random


# check if xpath exists. this is used later in the scrape to
# check if we should keep pressing the pg down/ end
# button, or to stop
def hasXpath(browser_in, xpath):
    try:
        browser_in.find_element_by_xpath(xpath)
        return True
    except:
        return False

def hasCss(browser_in, xpath):
	try:
		browser_in.find_element_by_css_selector(xpath)
		return True
	except:
		return False


# main scrape function


def google_review_scrape(browser, csv_save_path, loc_id, loc, nm_store_func, ad_store_func):
    print(browser)
    print()
    print(str(loc_id))
    print(str(loc))
    print(str(nm_store_func))
    print(str(ad_store_func))
    print('\n' * 2)

    os.chdir(csv_save_path)
    print()
    print(csv_save_path)
    print(browser)
    print()

    url = 'https://maps.google.com/?hl=en'
    browser.get(url)
    sleep(random.uniform(2, 3))  # sleep functions are important so your url doesn't get blocked by google

    print(loc)
    search_field = browser.find_element_by_xpath(
        "//input[@id='searchboxinput']")
    search_field.send_keys(loc)  # enter the location name
    sleep(random.uniform(0.5, 1))

    search_button = browser.find_element_by_xpath(
        "//button[@id = 'searchbox-searchbutton'] ")
    search_button.click()  # click the search button

    sleep(random.uniform(4, 6))
    # this is where the browser takes the longest to load.. so I have a long sleep function of 8 seconds
    # to ensure the location is loaded fully before attempting to click the review button

    print('just clicked the searchbutton')

    # check if there are multiple partial matches and click the first selection
    if hasXpath(browser, '//div[@class="section-result"][1]'):
        first_selection = browser.find_element_by_xpath(
            '//div[@class="section-result"][1]')
        first_selection.click()  # click the reviews button
    # elif hasCss(browser, ):
        print()
        print('clicked first selection..')
        sleep(4)

    # get overview info of the place
    try:
        num_reviews = browser.find_element_by_xpath(
            '//span[@class="section-rating-term"]//button[@jsaction="pane.rating.moreReviews"]').text
        num_reviews = str(num_reviews[1:-1])
    except:
        num_reviews = ''
    try:
        avg_review = browser.find_element_by_xpath(
            "//span[@class='section-star-display']").text
    except:
        avg_review = ''
    try:
        loc_type = browser.find_element_by_xpath(
            "//span[@class='section-rating-term']//button[@jsaction='pane.rating.category']").text
    except:
        loc_type = ''

    # check if is hotel
    if hasCss(browser, 'button.gm2-elevation-1'):
        print('HOTEL!')
        try:
            hotel_price = browser.find_element_by_css_selector(
                "span.gm2-headline-6").text
        except:
            hotel_price = ''
        try:
            hotel_type = browser.find_element_by_css_selector(
                "[jsinstance='*1'] span span span[role]").text
        except:
            hotel_type = ''

        loc_dollars = ''
        loc_summary = ''

    else: # all non hotels 
        try:
            loc_dollars = browser.find_element_by_css_selector(
                "span span span[aria-label]").text
        except:
            loc_dollars = ''
        try:
            loc_summary = browser.find_element_by_css_selector("div.section-editorial-attributes-summary").text
        except:
            loc_summary = ''

        hotel_price = ''
        hotel_type = ''


    print()
    print('got overview info about the location')

    # we also want to get the latitude and longitude, so we are extracting it from the URL
    url = browser.current_url
    # sample url
    # https://www.google.com/maps/place/Starbucks/@38.9295492,-77.057497,17z/data=!4m7!3m6!1s0x89b7b81f2affffff:0x4f162f85da6ce61a!8m2!3d38.929545!4d-77.055303!9m1!1b1
    urlstring = url.split('!3d')[1]
    lat = urlstring.split('!4d')[0]
    longi = urlstring.split('!4d')[1]
    longi = longi.split('!')[0]

    # create a unique name based on nameaddress of the location to export as
    csv_name = loc + ".txt"

    export_data = pd.DataFrame()

    print('lat       ' + str(len(lat)) + '     ' + str(lat))
    print('long      ' + str(len(longi)) + '     ' + str(longi))
    print('loc       ' + str(len(loc)) + '     ' + str(loc))
    print('store     ' + str(len(nm_store_func)) +
          '     ' + str(nm_store_func))
    print('ad        ' + str(len(ad_store_func)) +
          '     ' + str(ad_store_func))
    print('num rev   ' + str(len(num_reviews)) + '     ' + str(num_reviews))
    print('type      ' + str(len(loc_type)) + '     ' + str(loc_type))
    print('avg rev   ' + str(len(avg_review)) + '     ' + str(avg_review))
    print('loc summary   ' + str(len(loc_summary)) + '     ' + str(loc_summary))
    print('loc dollars   ' + str(len(loc_dollars)) + '     ' + str(loc_dollars))
    print('hotel type   ' + str(len(hotel_type)) + '     ' + str(hotel_type))
    print('hotel price   ' + str(len(hotel_price)) + '     ' + str(hotel_price))
    # print('id        ' + str(len(loc_id)) + '     ' + str(loc_id))
    print('\n' * 2)

    export_data['lat'] = pd.Series(lat)
    export_data['long'] = pd.Series(longi)
    # add a column for the name of the store
    export_data['name_of_loc'] = pd.Series(loc)
    export_data['name_only'] = pd.Series(nm_store_func)
    export_data['address_only'] = pd.Series(ad_store_func)
    export_data['num_reviews'] = pd.Series(num_reviews)
    export_data['loc_type'] = pd.Series(loc_type)
    export_data['avg_review'] = pd.Series(avg_review)
    export_data['loc_summary'] = pd.Series(loc_summary)
    export_data['loc_dollars'] = pd.Series(loc_dollars)
    export_data['hotel_type'] = pd.Series(hotel_type)
    export_data['hotel_price'] = pd.Series(hotel_price)
    export_data['ID'] = pd.Series(loc_id)

    print(export_data)

    export_data.to_csv(csv_name, header=None, index=None, sep='\t', mode='a') # index=None, header=True
    print('This file has been exported: ' + csv_name)
