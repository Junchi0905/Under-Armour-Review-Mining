#this program scrapes the reviews of individual stores
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
from random import randint


# check if xpath exists. this is used later in the scrape to check if we should keep pressing the pg down/ end
# button, or to stop
def hasXpath(xpath):
    try:
        browser.find_element_by_xpath(xpath)
        return True
    except:
        return False



def get_url_long_lat(browser):
    # we also want to get the latitude and longitude, so we are extracting it from the URL
    url = browser.current_url 
    # sample url 
    # https://www.google.com/maps/place/Starbucks/@38.9295492,-77.057497,17z/data=!4m7!3m6!1s0x89b7b81f2affffff:0x4f162f85da6ce61a!8m2!3d38.929545!4d-77.055303!9m1!1b1
    urlstring = url.split('!3d')[1]
    lat = urlstring.split('!4d')[0]
    longi = urlstring.split('!4d')[1]
    longi = longi.split('!')[0]
    lat = float(lat)
    longi = float(longi)
    return lat, longi
        


#main scrape function
def profile_scrape(browser, csv_save_path, user_id_func, user_link_func, nm_store_func, ad_store_func, lat_func, long_func, type_func):    
    
    os.chdir(csv_save_path)

    browser.get(str(user_link_func))
    sleep(3) # sleep functions are important so your url doesn't get blocked by google

    print('\n' * 2)
    print('reached persons profile page')

    # get user info
    person_name = browser.find_element_by_xpath("//div[@class='section-profile-header-line']//h1").text

    try:
        person_level = browser.find_element_by_xpath("//div[@class='section-profile-header-line']//span").text
    except:
        person_level = 0
    try:
        person_points = browser.find_element_by_xpath("//div[@class='section-profile-stats-points-line']//span[@class='section-profile-stats-points']").text
    except:
        person_points = 0

    print('got user basic info')
    

    try:
        user_total_reviews = browser.find_element_by_xpath('//span[@class="section-tab-info-stats-label"]').text
        user_total_reviews = str(user_total_reviews).split('reviews')[0]
        user_total_reviews = str(user_total_reviews).strip()

        check_scroll_num = int(user_total_reviews) + 2

        print('got user total reviews:        ' + str(user_total_reviews))
    except:
        print('no total ratings to scrape')
        user_total_reviews = ''
        check_scroll_num = 3

    try:
        for i in range(0,4): # this for loop clicks the end key 12 times (probably can be written as for range(0,11))
            box = browser.find_element_by_xpath("//div[@class = 'section-layout section-scrollbox scrollable-y scrollable-show']")
            box.send_keys(Keys.END)
            sleep(randint(2, 4))

        print('scrolled down four times')

        divnum = 2 # so we need a check to see if we have reached the bottom of the reviews for a location
        # what this does is check if the section-listbox section-scroll box etc element exists)
        # this element increases by 4 or 5 for each review, so we press the end button for as long as the path_exists exists
        # when it doesn't exist and hasXpath returns False, the scrolling and pressing of the end key stops
        path_exists = True
        while (path_exists == True) and (divnum < check_scroll_num):
            print('additional scrolling')
            box = browser.find_element_by_xpath("//div[@class = 'section-layout section-scrollbox scrollable-y scrollable-show']")
            box.send_keys(Keys.END)
            #element_same_path = '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[11]/div[' + str(divnum) + ']'
            #element_same_path = 'div.section-divider:nth-of-type(' + str(divnum) + ')'
            element_same_path = '//div[@class="section-divider section-divider-bottom-line"]' + '[' + str(divnum) + ']'

            path_exists = hasXpath(element_same_path)
            divnum += 7
            print()
            print('path exists:     ' + str(path_exists))
            print(divnum)
            sleep(randint(2,5))
    except:
        print()
        print('no scrolling necessary...')
        
    
    print('stopped scrolling, end of the reviews for this location!')
    sleep(randint(2, 5))


    # get visited locations' information
    v_loc_name_address = browser.find_elements_by_xpath('//div[@class="section-review-titles"]')
    v_loc_name_address_text = [x.text for x in v_loc_name_address]
    v_loc_name = []
    v_loc_address = []

    for i in v_loc_name_address_text:
        split_text = i.splitlines()
        v_loc_name.append(split_text[0])
        v_loc_address.append(split_text[1])

    v_loc_post_date_in = browser.find_elements_by_xpath('//span[@class="section-review-publish-date"]')
    v_loc_post_date = [x.text for x in v_loc_post_date_in]

    v_loc_stars_in = browser.find_elements_by_xpath('//span[@class="section-review-stars"]')
    v_loc_stars = [x.get_attribute('aria-label') for x in v_loc_stars_in]

    v_loc_review_in = browser.find_elements_by_xpath('//span[@class="section-review-text"]')
    v_loc_review = [x.text for x in v_loc_review_in]

    print('got post date, stars, and review text')


    csv_name = str(user_id_func) + ".csv" # create a unique name based on nameaddress of the location to export as
   
    export_data = pd.DataFrame()
  
    print('initialized export dataframe')  

    print()
    print('v_loc_name   ' + str(len(v_loc_name)))
    print('v_loc_address   ' + str(len(v_loc_address)))
    print('v_loc_post_date   ' + str(len(v_loc_post_date)))
    print('v_loc_stars   ' + str(len(v_loc_stars)))
    print('v_loc_review   ' + str(len(v_loc_review)))
    print()
    print('person_name     ' + str(person_name))
    print('person_level    ' + str(person_level))
    print('person_points   ' + str(person_points))
    print('user_total_reviews     ' + str(user_total_reviews))
    print()
    print('user_id    ' + str(user_id_func))
    print('user_link_func    ' + str(user_link_func))
    print('name_of_store    ' + str(nm_store_func))
    print('ad_store_func    ' + str(ad_store_func))
    print('lat_func     ' + str(lat_func))
    print('long_func     ' + str(long_func))
    print('type_func    ' + str(type_func))


    export_data['other_loc_name'] = v_loc_name
    export_data['other_loc_address'] = v_loc_address
    export_data['other_loc_post_date'] = v_loc_post_date
    export_data['other_loc_stars'] = v_loc_stars
    export_data['other_loc_review'] = v_loc_review

    export_data['person_name'] = person_name
    export_data['person_level'] = person_level
    export_data['person_points'] = person_points
    export_data['user_total_reviews'] = user_total_reviews

    export_data['user_id'] = user_id_func
    export_data['user_link'] = user_link_func
    export_data['name_of_store'] = nm_store_func
    export_data['address_of_store'] = ad_store_func # add a column for the name of the store
    export_data['orig_loc_lat'] = lat_func
    export_data['orig_loc_long'] = long_func
    export_data['orig_loc_type'] = type_func
    # export_data['from_where_ID'] = from_where_ID_func

    print(export_data)
    print('\n' * 2)

    export_data.to_csv(csv_name,index = None, header = True)
    print('This file (with reviews) has been exported: ' + csv_name)