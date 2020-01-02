from google_scraper import google_review_scrape
from google_scraper import hasXpath
from selenium import webdriver
from time import sleep
import multiprocessing
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os

'''
EDIT THE FOLLOWING THREE DIRECTORIES
'''

os.chdir(r'C:/Users/NewUsername/VENV/A/from_where_scrape/spinneys')
# browser path
browser_path = r"C:/Users/NewUsername/VENV/chromedriver.exe"
csv_save_path = r'C:/Users/NewUsername/VENV/A/from_where_scrape/spinneys/csvs/'




def scraper_for_loop_1(loc_id, store, name_of_store, address_of_store):
    browser_1 = webdriver.Chrome(executable_path=browser_path)
    totallist, currentitem, faileditem = len(store), 0, 0
    for loc_id, loc, nm_store, ad_store in zip(loc_id, store, name_of_store, address_of_store):
        try:
            google_review_scrape(browser_1, csv_save_path,
                                 loc_id, loc, nm_store, ad_store)
            print('all locations:  ' + str(currentitem) + ' / ' + str(totallist))
            currentitem += 1
            print('failed locations:  ' +
                  str(faileditem) + ' / ' + str(totallist))
        except:
            print('all locations:  ' + str(currentitem) + ' / ' + str(totallist))
            print('failed locations:  ' +
                  str(faileditem) + ' / ' + str(totallist))
            faileditem += 1
            currentitem += 1
    browser_1.stop_client()
    browser_1.close()


def scraper_for_loop_2(loc_id, store, name_of_store, address_of_store):
    browser_2 = webdriver.Chrome(executable_path=browser_path)
    totallist, currentitem, faileditem = len(store), 0, 0
    for loc_id, loc, nm_store, ad_store in zip(loc_id, store, name_of_store, address_of_store):
        try:
            google_review_scrape(browser_2, csv_save_path,
                                 loc_id, loc, nm_store, ad_store)
            print('all locations:  ' + str(currentitem) + ' / ' + str(totallist))
            currentitem += 1
            print('failed locations:  ' +
                  str(faileditem) + ' / ' + str(totallist))
        except:
            print('all locations:  ' + str(currentitem) + ' / ' + str(totallist))
            print('failed locations:  ' +
                  str(faileditem) + ' / ' + str(totallist))
            faileditem += 1
            currentitem += 1
    browser_2.stop_client()
    browser_2.close()


def scraper_for_loop_3(loc_id, store, name_of_store, address_of_store):
    browser_3 = webdriver.Chrome(executable_path=browser_path)
    totallist, currentitem, faileditem = len(store), 0, 0
    for loc_id, loc, nm_store, ad_store in zip(loc_id, store, name_of_store, address_of_store):
        try:
            google_review_scrape(browser_3, csv_save_path,
                                 loc_id, loc, nm_store, ad_store)
            print('all locations:  ' + str(currentitem) + ' / ' + str(totallist))
            currentitem += 1
            print('failed locations:  ' +
                  str(faileditem) + ' / ' + str(totallist))
        except:
            print('all locations:  ' + str(currentitem) + ' / ' + str(totallist))
            print('failed locations:  ' +
                  str(faileditem) + ' / ' + str(totallist))
            faileditem += 1
            currentitem += 1
    browser_3.stop_client()
    browser_3.close()


def scraper_for_loop_4(loc_id, store, name_of_store, address_of_store):
    browser_4 = webdriver.Chrome(executable_path=browser_path)
    totallist, currentitem, faileditem = len(store), 0, 0
    for loc_id, loc, nm_store, ad_store in zip(loc_id, store, name_of_store, address_of_store):
        try:
            google_review_scrape(browser_4, csv_save_path,
                                 loc_id, loc, nm_store, ad_store)
            print('all locations:  ' + str(currentitem) + ' / ' + str(totallist))
            currentitem += 1
            print('failed locations:  ' +
                  str(faileditem) + ' / ' + str(totallist))
        except:
            print('all locations:  ' + str(currentitem) + ' / ' + str(totallist))
            print('failed locations:  ' +
                  str(faileditem) + ' / ' + str(totallist))
            faileditem += 1
            currentitem += 1
    browser_4.stop_client()
    browser_4.close()


'''
EDIT FILENAME
OS.CHDIR
FROMNUM
TONUM

// NUMBER OF SCRAPERS YOU WANT TO TURN ON
'''

if __name__ == '__main__':
    # add the file path for the actual locations to scrape reviews for
    filename = r"C:/Users/NewUsername/VENV/A/from_where_scrape/spinneys/all_locs.csv"
    # set directory
    os.chdir(
        "C:/Users/NewUsername/VENV/A/from_where_scrape/spinneys/csvs")


    # PLEASE DROP DUPLICATES FIRST

    # which rows to scrape (even number total please)
    fromnum = 0 # starting number to scrape from
    tonum = 2 # the total number of rows of the dataset
    partial_scrape = fromnum   # starting number to scrape from
    # eventually need to scrape 12986 locations
    total_scrape = tonum - 0
    divide_evenly = total_scrape//2 # number of scrapers to run... don't need to change
    print('divided evenly:    ' + str(divide_evenly))

    # make the csv into a dataframe (pandas)
    # with open('filename.csv') as f:
    #     print(f)
    df_in = pd.read_csv(filename, encoding='utf-8') # cp1252
    df_in = df_in[:]

    print('length of dataframe in:    ' + str(len(df_in)))

    # what to search for in google maps
    df_in['address_full'] = df_in['address_of_loc']

    df_in['nameaddress'] = df_in['name_of_loc'] + ', ' + df_in['address_full'] # + ', near Horsford Rd, Brixton, London'

    # df_in = df_in.drop_duplicates(
    #     subset=['nameaddress'], keep='first')  # drop duplicate locations

    print('length of dataframe after duplicate drop:    ' + str(len(df_in)))

    # df_in = df_in[fromnum:tonum] # :tonum
    print('\n' *3)
    print('length of dataframe after start and end rows:    ' + str(len(df_in)))

    # df_in = pd.concat([df_in[325:400], df_in[725:800], df_in[800:4000]], sort=False)
    print('LENGTH OF DF: ' + str(len(df_in)))

    store_in = df_in['nameaddress'].tolist()  # turn the column into a list
    name_of_store_in = df_in['name_of_loc'].tolist()
    address_of_store_in = df_in['address_of_loc'].tolist()
    loc_id = df_in.index.tolist()

    print('length of lists to iterate over:    ' + str(len(store_in)))

    p1 = multiprocessing.Process(target=scraper_for_loop_1,
                                 args=(loc_id[partial_scrape:divide_evenly],
                                       store_in[partial_scrape:divide_evenly],
                                       name_of_store_in[partial_scrape:divide_evenly],
                                       address_of_store_in[partial_scrape:divide_evenly]
                                       ))
    p1.start()
    print('p1 started')
    print()

    p2 = multiprocessing.Process(target=scraper_for_loop_2,
                                 args=(loc_id[divide_evenly + partial_scrape: (divide_evenly * 2)],
                                       store_in[divide_evenly + partial_scrape: (
                                           divide_evenly * 2)],
                                       name_of_store_in[divide_evenly + partial_scrape: (
                                           divide_evenly * 2)],
                                       address_of_store_in[divide_evenly + partial_scrape: (
                                           divide_evenly * 2)]
                                       ))
    p2.start()
    print('p2 started')
    print()

    p3 = multiprocessing.Process(target=scraper_for_loop_3,
                                 args=(loc_id[(divide_evenly * 2) + partial_scrape: (divide_evenly * 3)],
                                       store_in[(divide_evenly * 2)+ partial_scrape: (divide_evenly * 3)],
                                       name_of_store_in[(
                                           divide_evenly * 2)+ partial_scrape: (divide_evenly * 3)],
                                       address_of_store_in[(
                                           divide_evenly * 2)+ partial_scrape: (divide_evenly * 3)]
                                       ))
    p3.start()
    print('p3 started')
    print()

    p4 = multiprocessing.Process(target=scraper_for_loop_4,
                                  args=(loc_id[(divide_evenly * 3)+ partial_scrape:],
                                        store_in[(divide_evenly * 3)+ partial_scrape:],
                                        name_of_store_in[(divide_evenly * 3)+ partial_scrape:],
                                        address_of_store_in[(
                                            divide_evenly * 3)+ partial_scrape:]
                                        ))
    p4.start()
    print('p4 started')
    print()
