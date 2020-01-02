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
    sleep(random.uniform(3, 4))  # sleep functions are important so your url doesn't get blocked by google

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

    # #check if there are multiple partial matches and click the first selection
    # try:
    #     first_selection = browser.find_element_by_xpath("//DIV[@jstcache='276'][1]")
    #     first_selection.click() #click the reviews button
    # except:
    #     print('no partial matches')

    # check if there are multiple partial matches and click the first selection
    if hasXpath(browser, '//div[@class="section-result"][1]'):
        first_selection = browser.find_element_by_xpath(
            '//div[@class="section-result"][1]')
        first_selection.click()  # click the reviews button
    # elif hasCss(browser, ):
        print()
        print('clicked first selection..')
        sleep(5)

    # get overview info of the place
    try:
        num_reviews = browser.find_element_by_xpath(
            "//ul[@class='section-rating-term-list']//span//button[@jsaction='pane.rating.moreReviews']").text
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
    # try:
    #     loc_summary = browser.find_element_by_xpath("//div[@class='section-editorial-attributes-summary']").text
    # except:
    #     loc_summary = ''

    print()
    print('got overview info about the location')

    sleep(random.uniform(0.2, 0.6))

    if hasXpath(browser, "//button[@class = 'jqnFjrOWMVU__button gm2-caption']") == True:

        review_button = browser.find_element_by_xpath(
            "//button[@class = 'jqnFjrOWMVU__button gm2-caption']")
        review_button.click()  # click the reviews button
        print('clicked reviews button')

        sleep(random.uniform(1.5, 2.5))

        # first time you click "end" key, google scrolls 20 div 'elements', afterwards it scrolls exactly 30
        # so lets scroll once then run our loop for +=30

        # this for loop clicks the end key 12 times (probably can be written as for range(0,11))
        for i in range(0, 4):
            box = browser.find_element_by_xpath(
                "//div[@class = 'section-layout section-scrollbox scrollable-y scrollable-show']")

            box.send_keys(Keys.END)
            sleep(random.uniform(1.2, 2))
            print('SCROLLING..')

        divnum = 31  # so we need a check to see if we have reached the bottom of the reviews for a location
        # what this does is check if the section-listbox section-scroll box etc element exists)
        # this element increases by 4 or 5 for each review, so we press the end button for as long as the path_exists exists
        # when it doesn't exist and hasXpath returns False, the scrolling and pressing of the end key stops
        path_exists = True
        while path_exists == True:
            print('additional scrolling')
            box = browser.find_element_by_xpath(
                "//div[@class = 'section-layout section-scrollbox scrollable-y scrollable-show']")
            box.send_keys(Keys.END)
            #element_same_path = '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[11]/div[' + str(divnum) + ']'
            #element_same_path = 'div.section-divider:nth-of-type(' + str(divnum) + ')'
            element_same_path = '//div[@class="section-divider"]' + \
                '[' + str(divnum) + ']'

            path_exists = hasXpath(browser, element_same_path)
            divnum += 3
            print(divnum)
            sleep(random.uniform(1.5, 2.1))

        print('stopped scrolling, end of the reviews for this location!')

        nm = []  # user names, we don't actually collect this for the final dataset
        rats = []  # ratings
        tm = []  # date posted
        tx = []  # review comment text
        names = []  # user names
        ratings = []  # ratings
        time = []  # date posted
        text = []  # review comment text
        user_href_all = []
        user_href_in = []
        user_href = []
        names = browser.find_elements_by_xpath(
            "//div[@class= 'section-review-title']//span")
        # this is the standard format for getting text from //span elements
        nm = [x.text for x in names]

        ratings = browser.find_elements_by_xpath(
            "//span[@class = 'section-review-stars']")
        rats = [x.get_attribute("aria-label") for x in ratings]

        time = browser.find_elements_by_xpath(
            "//span[@class = 'section-review-publish-date'] ")
        tm = [x.text for x in time]

        text = browser.find_elements_by_xpath(
            "//span[@class = 'section-review-text'] ")
        tx = [x.text for x in text]

        user_href_all = browser.find_elements_by_xpath(
            "//div[@class='section-review-titles section-review-titles-with-menu']//a")
        user_href_in = [x.get_attribute("href") for x in user_href_all]
        print('\n' * 2)
        user_href = [x for x in user_href_in if x is not None]
        print(str(len(user_href)))
        print(user_href)
        print('DONE')
        print('\n' * 2)

        # we also want to get the latitude and longitude, so we are extracting it from the URL
        url = browser.current_url
        # sample url
        # https://www.google.com/maps/place/Starbucks/@38.9295492,-77.057497,17z/data=!4m7!3m6!1s0x89b7b81f2affffff:0x4f162f85da6ce61a!8m2!3d38.929545!4d-77.055303!9m1!1b1
        urlstring = url.split('!3d')[1]
        lat = urlstring.split('!4d')[0]
        longi = urlstring.split('!4d')[1]
        longi = longi.split('!')[0]

        # create a unique name based on nameaddress of the location to export as
        csv_name = loc + ".csv"

        export_data = pd.DataFrame()

        print('ratings   ' + str(len(rats)) + '     ' + str(rats))
        print('date      ' + str(len(tm)) + '     ' + str(tm))
        print('text      ' + str(len(tx)) + '     ' + str(tx))
        print('names     ' + str(len(nm)) + '     ' + str(nm))
        print('user ref  ' + str(len(user_href)) + '     ' + str(user_href))
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
        # print('id        ' + str(len(loc_id)) + '     ' + str(loc_id))
        print('\n' * 2)

        # export_data['url'] = browser.current_url
        export_data['ratings'] = rats
        export_data['review_data'] = tm
        export_data['text'] = tx
        export_data['lat'] = lat
        export_data['long'] = longi
        # add a column for the name of the store
        export_data['name_of_loc'] = loc
        export_data['name_only'] = nm_store_func
        export_data['address_only'] = ad_store_func
        export_data['num_reviews'] = num_reviews
        export_data['loc_type'] = loc_type
        export_data['avg_review'] = avg_review
        # export_data['loc_summary'] = loc_summary
        export_data['user_href'] = user_href
        export_data['ID'] = loc_id
    #    export_data['address'] = address # add a column for the address

        print(export_data)

        export_data.to_csv(csv_name, index=None, header=True)
        print('This file has been exported: ' + csv_name)

    else:

        print('\n' * 2)
        print('NO REVIEWS FOR THIS LOCATION')
        # we also want to get the latitude and longitude, so we are extracting it from the URL
        url = browser.current_url
        # sample url
        # https://www.google.com/maps/place/Starbucks/@38.9295492,-77.057497,17z/data=!4m7!3m6!1s0x89b7b81f2affffff:0x4f162f85da6ce61a!8m2!3d38.929545!4d-77.055303!9m1!1b1
        urlstring = url.split('!3d')[1]
        lat = urlstring.split('!4d')[0]
        longi = urlstring.split('!4d')[1]
        longi = longi.split('!')[0]

        print('got longitude and latitude..')

        # create a unique name based on nameaddress of the location to export as
        csv_name = loc + ".csv"

        print('\n' * 2)
        print('lat       ' + str(len(lat)) + '     ' + str(lat))
        print('long      ' + str(len(longi)) + '     ' + str(longi))
        print('loc       ' + str(len(loc)) + '     ' + str(loc))
        print('store     ' + str(len(nm_store_func)) +
              '     ' + str(nm_store_func))
        print('ad        ' + str(len(ad_store_func)) +
              '     ' + str(ad_store_func))
        print('type      ' + str(len(loc_type)) + '     ' + str(loc_type))
        # print('id        ' + str(len(loc_id)) + '     ' + str(loc_id))
        print('\n' * 2)

        export_data = pd.DataFrame()
        export_data['name_of_loc'] = pd.Series(loc)
        export_data['name_only'] = pd.Series(nm_store_func)
        export_data['address_only'] = pd.Series(ad_store_func)
        export_data['lat'] = pd.Series(lat)
        export_data['long'] = pd.Series(longi)
        export_data['loc_type'] = pd.Series(loc_type)
        export_data['ratings'] = ''
        export_data['review_data'] = ''
        export_data['text'] = ''
        export_data['num_reviews'] = str(0)
        export_data['avg_review'] = ''
        # export_data['loc_summary'] = loc_summary

        export_data['user_href'] = ''
        export_data['ID'] = loc_id
    #    export_data['address'] = address # add a column for the address

        print(export_data)

        export_data.to_csv(csv_name, index=None, header=True)
        print('This file has been exported: ' + csv_name)
