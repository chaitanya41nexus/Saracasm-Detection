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
	
	search_term = "Python"
	
	tweets = []
	for tweet in tweepy.Cursor(api.search, q=search_term, lang="en", tweet_mode="extended").items(20):
		if ("retweeted_status" in dir(tweet)):
			print(tweet.retweeted_status.full_text.replace("\n", ", "))
		else:
			print(tweet.full_text.replace("\n", ", "))

else:
	print("Usage: twitter.py [auth|sample]")