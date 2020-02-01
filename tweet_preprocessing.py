#step 1: get data from twitter

import tweepy
import sys

CONSUMER_KEY = "23yKHMkXpuKJcQUcerO0yHwP0"
CONSUMER_SECRET = "BYZg0qFzb2gwFjJqx09C7oWo2olFRN3Wfgu62FU4aVCTFlrgt9"
ACCESS_TOKEN = "1199635731527983104-6kg4PNCcsgBjsX7vdGLnL2zvT4MeQh"
ACCESS_TOKEN_SECRET = "fS2l0tnHCqV754tavS6CmmR44IFYXesSbbmWm6silueXE"

if (len(sys.argv) == 2 and sys.argv[1] == "auth"):
	# Sample authenticaton to Twitter
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	try:
		api.verify_credentials()
		print("Authentication OK")
	except:
		print("Error during authentication")
elif (len(sys.argv) == 2 and sys.argv[1] == "sample"):
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	
	tweets = []
	termlist = []
	search_term = "great" # make to a list, and a loop to get
	termlist.append(search_term)
	search_term = "wonderful"
	termlist.append(search_term)
	search_term = "funny"
	termlist.append(search_term)
	
	for term in termlist:
    #num = 0
		print("term: " + term)
		for tweet in tweepy.Cursor(api.search, q=term, lang="en", tweet_mode="extended").items(10):		
        #num = num + 1
        #print(num)
				if ("retweeted_status" in dir(tweet)):
            #print("retweeted_status")
            #print(tweet.retweeted_status.full_text.replace("\n", ", "))
						tweets.append(tweet.retweeted_status.full_text.replace("\n", ", "))
				else:
						#print("not_retweeted_status")
						#print(tweet.full_text.replace("\n", ", "))
						tweets.append(tweet.full_text.replace("\n", ", "))

	print("Samples:")
	for i in range(0,30):
			print([i])
			print(tweets[i])
else:
	print("Usage: twitter.py [auth|sample]")

#step 2: pre-process
import nltk
from nltk.tokenize import *

tokens = []
for tweet in tweets:
    token = []
    token_sent = []
    sents = []
    sents = sent_tokenize(tweet.lower()) #lower case
    for sent in sents:
        token = word_tokenize(sent)
        token_sent.append(token)
    tokens.append(token_sent)

count = 0
for tweet in tokens:
    if count > 10:
        break
    for sentence in tweet:
        print(sentence)
    count = count + 1