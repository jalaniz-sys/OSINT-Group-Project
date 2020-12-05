import praw
from praw.models import MoreComments
import csv
import pandas as pd
import datetime 
from time import sleep
import time



def scrap_go(name_subreddit):
	reddit=praw.Reddit(client_id = 'xjxGm-BkDEXWTg',
 					client_secret='kEKFPpSNBctiSSu16Ti9JFiLIi3w8g' ,
 					username ='########', #username omitted 
 					password='########', #password omitted
 					user_agent='degreaser')
	subreddit=reddit.subreddit(name_subreddit)
	maxLimit=10
	hot=subreddit.hot(limit=maxLimit)
	top=subreddit.top(limit=maxLimit)
	sub_dict = {'Time':[], 'Title': [], 'Author': [], 'Upvotes': []}
	new_df = pd.DataFrame(sub_dict)

	def doesContainHateWord(textToAnalyze):
		textToAnalyze = textToAnalyze.lower()
		for x in covidDict:
			if x in textToAnalyze:
				print("Dictionary word found: " + x)
				print("Text is " + textToAnalyze)
				return True
		return False

	#Dictionary to find the latest news on Covid
	covidDict=["covid-19", "corona", "social distancing","self-isolation", "super spreader", "flatten the curve", "pandemic", "outbreak", "n95", 
"herd immunity", "ventilator", "coronavirus", "asymptomatic" "presymptomatic", "self-quarantine"]
	#Dictionary to find the latest news on vaccination. Uncomment to utilize
	#covidDict=["vaccination", "cure", "vaccine"]
	csv=f'new_{subreddit}_posts.csv'

	for count,submission in enumerate(hot):
		if (count % 10 == 0):
			print("finished looking at " + str(count) + " / " + str(maxLimit) + " posts")
		if not submission.stickied:
			foundHate= doesContainHateWord(submission.title) or doesContainHateWord(submission.selftext)
			#For a more thorough analysis of the top comments of a reddit post, uncomment below
			'''
			for top_level_comment in submission.comments:
				try:
					foundHate= foundHate or doesContainHateWord(top_level_comment.body)
				except:
					print("[Warning] No comment body found")
			'''
			if foundHate:
				print('-'*60)
				readable = time.ctime(submission.created_utc)
				print('Time: {}\nTitle: {} \nAuthor: {} \nUpvotes: {}'.format(readable,submission.title,submission.author,submission.ups))
				submission.comments.replace_more(limit=None)
				list_of_top_comments = []
				#For a more thorough analysis of the top comments of a reddit post, uncomment below
				'''
				for top_level_comment in submission.comments:
					try:
						list_of_top_comments.append(top_level_comment.author.name)
					except:
						print("Warning: No author name found")
				'''
				temp_df = {'Time':readable, 'Title':submission.title, 'Author':submission.author, 'Upvotes': submission.ups}
				new_df = new_df.append(temp_df, ignore_index = True)
				#Sleep function lets program go past the limit of the API
				sleep(0.1)
	new_df.to_csv(csv, index=False)
	print("Scrapping succesful")

# add UTC 