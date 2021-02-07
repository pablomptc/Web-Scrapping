#TWITTER DATA EXTRACION BY TOPIC#

#Libraries
import tweepy
import csv
import pandas as pd
import numpy as np
import re



#Credentials
#Input your credentials here in xxx
#To obtain twitter credentials you must register on the page https://developer.twitter.com/en as a developer
consumer_key = "xxx"
consumer_secret = "xxx"
access_token = "xxx"
access_token_secret = "xxx"



#Extracting tweets by topic
auth = tweepy.OAuthHandler (consumer_key, consumer_secret)
auth.set_access_token (access_token, access_token_secret)
api = tweepy.API (auth, wait_on_rate_limit = True)



# Csv document creation to append data
csvFile = open('tweets.csv', 'a')



# Use csv writer
csvWriter = csv.writer(csvFile)



# In the following loop input:
# q = input topic you want to search for results in Twitter
# count = number of tweets you want to extract
# lang = language
# since = date

for tweet in tweepy.Cursor(api.search,
                           q = "#unitedAIRLINES",
                           count = 100,
                           lang = "en",
                           since = "2017-04-03").items():

    print (tweet.created_at, tweet.text)

    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])



# A csv is created with two columns: date and tweets
tweets_csv.columns = ["Fecha", "Tweet"]
