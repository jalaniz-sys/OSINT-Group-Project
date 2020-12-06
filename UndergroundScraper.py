#Beatifulsoup's job is purely for parsing hmtl text with the help of python
import bs4
import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup as soup

def democrat_go(myurl):
#targetted url
	#myurl= 'https://www.democraticunderground.com/?com=forum&id=1002&page=19'
	forumNumber=myurl[-2:]

	page=requests.get(myurl)
	#Parses the HTML
	soup = BeautifulSoup(page.content, 'html.parser')

	results = soup.find(class_='default-table-container')

	job_dark_elems = results.find_all('tr', class_='bg-dark thread-new')
	job_lite_elems = results.find_all('tr', class_='bg-lite thread-new')
	job_dark_elems_deleted = results.find_all('tr', class_='bg-dark deleted-new')
	job_lite_elems_deleted = results.find_all('tr', class_='bg-lite deleted-new')
	job_lite_elems_hot = results.find_all('tr', class_='bg-lite hot-thread-new')
	job_dark_elems_hot = results.find_all('tr', class_='bg-dark hot-thread-new')

	def doesContainKeyPhrase(textToAnalyze):
		textToAnalyze = textToAnalyze.lower()
		for x in coronaDictionary:
			if x in textToAnalyze:
				print("Key word: " + x)
				return True
		return False

	coronaDictionary=["covid-19", "corona", "social distancing","self-isolation", "super spreader", "flatten the curve", "pandemic", "outbreak", "n95", 
"herd immunity", "ventilator", "coronavirus", "asymptomatic" "presymptomatic", "self-quarantine", "fauci"]

	sub_dict = {'Time': [],'Title': [], 'Author': [], 'Views': []}
	new_df = pd.DataFrame(sub_dict)
	csv=f'new_{forumNumber}_posts.csv'

	job_dark_elems.extend(job_lite_elems)
	job_dark_elems.extend(job_dark_elems_deleted)
	job_dark_elems.extend(job_lite_elems_deleted)
	job_dark_elems.extend(job_lite_elems_hot)
	job_dark_elems.extend(job_dark_elems_hot)

	for job_elem  in job_dark_elems:
		title = job_elem.find('td', class_='title').get_text()

		print(title)
		foundKorn=doesContainKeyPhrase(title)
		if foundKorn:
			temp_df = {'Time':job_elem.find('td', class_='time').get_text(), 'Title':job_elem.find('td', class_='title').get_text(), 'Author':job_elem.find('td', class_='author').get_text(), 'Views': job_elem.find('td', class_='views').get_text()}
			new_df = new_df.append(temp_df, ignore_index = True)
			sleep(0.1)
	new_df.to_csv(csv, index=False)

