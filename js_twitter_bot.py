# -*- coding: utf-8 -*-

import sys
import traceback
import os
import time

import tweetstream
import twitter

consumer_key = ""
consumer_secret = ""

access_token_key = ""
access_token_secret = ""

twitter_account_username = ""
twitter_account_password = ""

MAX_TPM = round(1000/float(24*60), 2) # 1000 tweets per day. Twitter limit

PRINT_STATS_EVERY = 100

def should_send_tweet_with_tpm(current_tpm):	
	return current_tpm <= MAX_TPM
	
def get_passed_seconds():
	return (time.time() - start_time)

def should_reply_to_tweet(tweet):
	MIN_FOLLOWERS 	= 500
	
	allowed_langs	= ["es"]
	
	language	 	= tweet["user"]["lang"]
	followers 		= tweet["user"]['followers_count']
	rt_count  		= tweet['retweet_count']
	
	return language in allowed_langs and rt_count == 0 and followers >= MIN_FOLLOWERS
	
def get_current_tpm(sent_tweets):
	return float(sent_tweets) * 60 / get_passed_seconds()
	
def print_divider_line():
	print "--------"
	
def print_tweet(tweet):
	original_tweet = "@" + tweet["user"]["screen_name"] + ": " + tweet["text"];
	print "\n" + original_tweet.encode("utf-8")
	
def print_stats(analized_tweets, sent_tweets):
	print ""
	print_divider_line()
	passed_seconds = get_passed_seconds()
	print "Running for " + str(int(passed_seconds)/3600) + "h" + str(int(passed_seconds) / 60) + "min" + str(int(passed_seconds) % 60) + "s"
	
	print "Analized tweets: " + str(analized_tweets)
	percentage = float(sent_tweets) * 100 / analized_tweets
	analized_tps = float(analized_tweets) / passed_seconds
	sent_tpm = get_current_tpm(sent_tweets)
	print "Sent tweets: " + str(sent_tweets)
	print ("%.2f" % percentage) + "% analized / sent"
	print "Analized tps: " + ("%.1f" % analized_tps) 
	print "Sent tpm: " + ("%.2f" % sent_tpm)

	print_divider_line()

print "Authenticating"

api = twitter.Api(consumer_key=consumer_key,consumer_secret=consumer_secret, access_token_key=access_token_key, access_token_secret=access_token_secret)

print "Logged user: @" + api.VerifyCredentials().screen_name

query = ['search'] # words to search
stream = tweetstream.FilterStream(twitter_account_username, twitter_account_password, track=query)

analized_tweets = 0
sent_tweets = 0
start_time = time.time()

for tweet in stream:
	try:
		analized_tweets += 1
		print ".",

		current_tpm = get_current_tpm(sent_tweets)

		if (should_reply_to_tweet(tweet)):
			if should_send_tweet_with_tpm(current_tpm):
				username = tweet["user"]["screen_name"]
				tweet_id = tweet["id"]
				
				print_tweet(tweet)
						
				reply = "@" + username + " I'm replying to your tweet with a bot!"
				print reply
			
				# api.PostUpdate(reply, tweet_id) # Send the tweet 'reply' as a reply to 'tweet_id'

				sent_tweets += 1
			else:
				skipping_alert = "Skipping tweet send because we're exceeding max TPM (" + ("%.2f" % current_tpm) + " > " + str(MAX_TPM) + ")"
				print "\n" + skipping_alert
				
		if analized_tweets % PRINT_STATS_EVERY == 0:
			print_stats(analized_tweets, sent_tweets)	
	except:
		print ""
		traceback.print_exc()
		pass