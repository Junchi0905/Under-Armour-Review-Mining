from google_scraper import google_review_scrape
from google_scraper import hasXpath
from selenium import webdriver
from time import sleep
import multiprocessing
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os

'''
EDIT THE FOLLOWING PATHS
-- you shouldn't need to edit anything else below.. just these paths and int
'''

# directory where everythings going downn
folder_directory = 'C:/Users/NewUsername/vnineteen/A/from_where_scrape/spinneys/orig_locs/'
# chromedriver path (make sure chromedriver version matches your version of chrome)
browser_path = r"C:/Users/NewUsername/VENV/chromedriver.exe"

# add the file path for the actual locations to scrape reviews for
filename_in = r"all_locs.csv"  # place this within your directory folder
total_scrapers_to_run = 4
# which rows to scrape (even number total please)
fromnum = 0  # starting number to scrape from

# where to save csv outputs
csv_save_path = folder_directory + '/csvs/'
'''where we save csv outputs of the scrape (create an empty csv folder named csvs
in the folder directory)
-- make sure this has the ending forward slash (/) because we append the export
name to the end of the csv_save_path
--also we are using absolute instead of relative path because exporting with 
relative paths can get iffy'''


''' we define each scraper individually because selenium is strange
in defining the browser within a function within a function'''


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

    # set directory
    os.chdir(folder_directory)

    # create the save folder if it doesn't exist already
    if not os.path.exists('csvs'):
        os.makedirs('csvs')
        print('made csv save folder')

    # read in csv of locations to scrape
    df_in = pd.read_csv(filename_in, encoding='utf-8')  # cp1252
    tonum = len(df_in)

    # starting number to scrape from -- useful if you want to run this in batches
    partial_scrape = fromnum
    # total_scrape is a calculation again in case you need to run in batches
    total_scrape = tonum - 0
    # divide by number of scrapers to run
    # to split up the dataset and run it w/ multiprocessing
    divide_evenly = total_scrape//total_scrapers_to_run
    print('rows to scrape divided evenly:    ' + str(divide_evenly))

    # manually set the rows to run if need be..
    df_in = df_in[:]

    # what to search for in google maps
    df_in['address_full'] = df_in['address_of_loc']

    ''' sometimes it is helpful to add an additional string at the end
    like this:    + ', near Horsford Rd, Brixton, London'
    to help google location the name and address of the location more'''
    df_in['nameaddress'] = df_in['name_of_loc'] + ', ' + \
        df_in['address_full']

    print('LENGTH OF DF: ' + str(len(df_in)))

    # we are creating lists to loop through and add to the generated csv
    store_in = df_in['nameaddress'].tolist()  # turn the column into a list
    name_of_store_in = df_in['name_of_loc'].tolist()
    address_of_store_in = df_in['address_of_loc'].tolist()
    loc_id = df_in.index.tolist()  # not needed but helpful..

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
                                       store_in[(divide_evenly * 2) +
                                                partial_scrape: (divide_evenly * 3)],
                                       name_of_store_in[(
                                           divide_evenly * 2) + partial_scrape: (divide_evenly * 3)],
                                       address_of_store_in[(
                                           divide_evenly * 2) + partial_scrape: (divide_evenly * 3)]
                                       ))
    p3.start()
    print('p3 started')
    print()

    p4 = multiprocessing.Process(target=scraper_for_loop_4,
                                 args=(loc_id[(divide_evenly * 3) + partial_scrape:],
                                       store_in[(divide_evenly * 3) +
                                                partial_scrape:],
                                       name_of_store_in[(
                                           divide_evenly * 3) + partial_scrape:],
                                       address_of_store_in[(
                                           divide_evenly * 3) + partial_scrape:]
                                       ))
    p4.start()
    print('p4 started')
    print()
