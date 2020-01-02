# this program scrapes the reviews of individual stores
from function_review_profiles_scrape import profile_scrape
from function_review_profiles_scrape import get_url_long_lat
from function_review_profiles_scrape import hasXpath
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import multiprocessing

os.chdir("C:/Users/NewUsername/vnineteen/A/from_where_scrape/spinneys/profiles")


# browser path
browser_path = r"C:/Users/NewUsername/VENV/chromedriver.exe"
csv_save_path = r'C:/Users/NewUsername/vnineteen/A/from_where_scrape/spinneys/profiles/csvs/'


def scraper_1(user_id, links, name_of_store, address_of_store, latitude, longitude, loc_type):
	browser_1 = webdriver.Chrome(executable_path=browser_path)
	totallist, currentitem, faileditem = len(user_id), 0, 0
	for u_id, u_link, nm_store, ad_store, lati, longi, typei in zip(user_id, links, name_of_store, address_of_store, latitude, longitude, loc_type):
		print('SCRAPER 1')
		try:
			profile_scrape(browser_1, csv_save_path, u_id, u_link,
						   nm_store, ad_store, lati, longi, typei)
			print('failed and successful locations:  ' + str(currentitem) +
				  ' / ' + str(totallist))  # shows current scrape completion rate
			currentitem += 1
			print('failed locations:  ' +
				  str(faileditem) + ' / ' + str(totallist))
		except:
			print('oopsie, error!', u_link)
			print('failed and successful locations:  ' +
				  str(currentitem) + ' / ' + str(totallist))
			print('failed locations:  ' +
				  str(faileditem) + ' / ' + str(totallist))
			faileditem += 1
			currentitem += 1
	browser_1.stop_client()
	browser_1.close()


def scraper_2(user_id, links, name_of_store, address_of_store, latitude, longitude, loc_type):
	browser_2 = webdriver.Chrome(executable_path=browser_path)
	totallist, currentitem, faileditem = len(user_id), 0, 0
	for u_id, u_link, nm_store, ad_store, lati, longi, typei in zip(user_id, links, name_of_store, address_of_store, latitude, longitude, loc_type):
		print('SCRAPER 2')
		try:
			profile_scrape(browser_2, csv_save_path, u_id, u_link,
						   nm_store, ad_store, lati, longi, typei)
			print('failed and successful locations:  ' + str(currentitem) +
				  ' / ' + str(totallist))  # shows current scrape completion rate
			currentitem += 1
			print('failed locations:  ' +
				  str(faileditem) + ' / ' + str(totallist))
		except:
			print('oopsie, error!', u_link)
			print('failed and successful locations:  ' +
				  str(currentitem) + ' / ' + str(totallist))
			print('failed locations:  ' +
				  str(faileditem) + ' / ' + str(totallist))
			faileditem += 1
			currentitem += 1
	browser_2.stop_client()
	browser_2.close()


def scraper_3(user_id, links, name_of_store, address_of_store, latitude, longitude, loc_type):
	browser_3 = webdriver.Chrome(executable_path=browser_path)
	totallist, currentitem, faileditem = len(user_id), 0, 0
	for u_id, u_link, nm_store, ad_store, lati, longi, typei in zip(user_id, links, name_of_store, address_of_store, latitude, longitude, loc_type):
		print('SCRAPER 3')
		try:
			profile_scrape(browser_3, csv_save_path, u_id, u_link,
						   nm_store, ad_store, lati, longi, typei)
			print('failed and successful locations:  ' + str(currentitem) +
				  ' / ' + str(totallist))  # shows current scrape completion rate
			# currentitem += 1
			print('failed locations:  ' +
				  str(faileditem) + ' / ' + str(totallist))
		except:
			print('oopsie, error!', u_link)
			print('failed and successful locations:  ' +
				  str(currentitem) + ' / ' + str(totallist))
			print('failed locations:  ' +
				  str(faileditem) + ' / ' + str(totallist))
			faileditem += 1
			currentitem += 1
	browser_3.stop_client()
	browser_3.close()


def scraper_4(user_id, links, name_of_store, address_of_store, latitude, longitude, loc_type):
	browser_4 = webdriver.Chrome(executable_path=browser_path)
	totallist, currentitem, faileditem = len(user_id), 0, 0
	for u_id, u_link, nm_store, ad_store, lati, longi, typei in zip(user_id, links, name_of_store, address_of_store, latitude, longitude, loc_type):
		print('SCRAPER 4')
		try:
			profile_scrape(browser_4, csv_save_path, u_id, u_link,
						   nm_store, ad_store, lati, longi, typei)
			print('failed and successful locations:  ' + str(currentitem) +
				  ' / ' + str(totallist))  # shows current scrape completion rate
			currentitem += 1
			print('failed locations:  ' +
				  str(faileditem) + ' / ' + str(totallist))
		except:
			print('oopsie, error!', u_link)
			print('failed and successful locations:  ' +
				  str(currentitem) + ' / ' + str(totallist))
			print('failed locations:  ' +
				  str(faileditem) + ' / ' + str(totallist))
			faileditem += 1
			currentitem += 1
	browser_4.stop_client()
	browser_4.close()


if __name__ == '__main__':

	# MAKE SURE THAT YOU CREATE A COLUMN OF 1,2,3,4,5,6,7,8... ETC
	# TITLED "ID" for us to use
	# add the file path for the actual locations to scrape reviews for
	filename = "spinneys_locs.csv"
	fromnum = 0
	tonum = 1108


	# make the csv into a dataframe (pandas)
	df_in = pd.read_csv(filename, encoding='utf-8')

	# set directory
	# os.chdir("C:/Users/NewUsername/vnineteen/A/from_where_scrape/spinneys/profiles")

	# google recently changed the direction of url profiles to default to photos so..
	df_in['user_href'] = df_in['user_href'].apply(lambda x: x.replace('?hl', '/reviews?hl'))

	# get the user_href column prepared
	df_in['ID'] = df_in['user_href'].apply(lambda x: x.split('contrib/')[1].split('/reviews?hl')[0])
	print(df_in['ID'][4])


	# df_in = df_in.reset_index()
	# df_in['ID'] = df_in.index
	user_id = df_in['ID'].tolist()
	links = df_in['user_href'].tolist() #turn the column into a list
	name_of_store = df_in['name_only'].tolist()
	address_of_store = df_in['address_only'].tolist()
	latitude = df_in['lat'].tolist()
	longitude = df_in['long'].tolist()
	loc_type = df_in['loc_type'].tolist()



	total_scrape = tonum - fromnum
	divide_evenly = total_scrape//4
	print('divided evenly:    ' + str(divide_evenly))

	df_in = df_in[fromnum:] # :tonum
	print('\n' *3)
	print('length of dataframe after start and end rows:    ' + str(len(df_in)))


	print('length of lists to iterate over:    ' + str(len(user_id)))

	print()
	print(str(len(user_id)))
	print(str(len(links)))
	print(str(len(name_of_store)))
	print(str(len(address_of_store)))
	print(str(len(latitude)))
	print(str(len(longitude)))
	print(str(len(loc_type)))


# user_id, links, name_of_store, address_of_store, latitude, longitude, loc_type, from_where_ID

	p1 = multiprocessing.Process(target=scraper_1,
								 args=(user_id[:divide_evenly],
									   links[:divide_evenly],
									   name_of_store[:divide_evenly],
									   address_of_store[:divide_evenly],
									   latitude[:divide_evenly],
									   longitude[:divide_evenly],
									   loc_type[:divide_evenly]
									   ))
	p1.start()
	print('p1 started')
	print()

	p2 = multiprocessing.Process(target=scraper_2,
								 args=(user_id[divide_evenly: (divide_evenly *2)],
									   links[divide_evenly: (divide_evenly *2)],
									   name_of_store[divide_evenly: (divide_evenly *2)],
									   address_of_store[divide_evenly: (divide_evenly *2)],
									   latitude[divide_evenly: (divide_evenly *2)],
									   longitude[divide_evenly: (divide_evenly *2)],
									   loc_type[divide_evenly: (divide_evenly *2)]
									   ))
	p2.start()
	print('p2 started')
	print()

	p3 = multiprocessing.Process(target=scraper_3,
								 args=(user_id[(divide_evenly *2): (divide_evenly * 3)],
									   links[(divide_evenly *2): (divide_evenly * 3)],
									   name_of_store[(divide_evenly *2): (divide_evenly * 3)],
									   address_of_store[(divide_evenly *2): (divide_evenly * 3)],
									   latitude[(divide_evenly *2): (divide_evenly * 3)],
									   longitude[(divide_evenly *2): (divide_evenly * 3)],
									   loc_type[(divide_evenly *2): (divide_evenly * 3)]
									   ))
	p3.start()
	print('p3 started')
	print()

	p4 = multiprocessing.Process(target=scraper_4,
								 args=(user_id[(divide_evenly *3):],
									   links[(divide_evenly *3):],
									   name_of_store[(divide_evenly *3):],
									   address_of_store[(divide_evenly *3):],
									   latitude[(divide_evenly *3): ],
									   longitude[(divide_evenly *3):],
									   loc_type[(divide_evenly *3):]
									   ))
	p4.start()
	print('p4 started')
	print()
