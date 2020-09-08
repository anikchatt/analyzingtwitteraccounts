import tweepy
import pandas as pd
import json
import csv
import io
import openpyxl
from datetime import date
from datetime import datetime
import time


consumer_key = "6e92AjMpkCVtzSZNZmmUXLqTL"
consumer_secret = "gPrxX9d2FJoNIe0YzjvbXW5LJmhQgGOgGPDDaSdlfM19ANj346"

key= "473504740-q90U2JhFzaJEgNSYw3ZkIkUIb2eX27vhBD2hANCn"
secret = "D1MhmUS31CK1D4YeaJo6cS5qNOC6BtANtBBPJgpyIclWd"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)
path = r"C:\Users\Anik\Desktop\twitter_analyzer"

# Helper function to handle twitter API rate limit
def limit_handled(cursor, list_name):
  while True:
    try:
      yield cursor.next()
    # Catch Twitter API rate limit exception and wait for 15 minutes
    except tweepy.RateLimitError:
      print("\nData points in list = {}".format(len(list_name)))
      print('Hit Twitter API rate limit.')
      for i in range(3, 0, -1):
        print("Wait for {} mins.".format(i * 5))
        time.sleep(5 * 60)
    # Catch any other Twitter API exceptions
    except tweepy.error.TweepError:
      print('\nCaught TweepError exception' )

# Helper function to get all tweets of a specified user
# NOTE:This method only allows access to the most recent 3200 tweets
# Source: https://gist.github.com/yanofsky/5436496
def get_all_tweets(screen_name):
  # initialize a list to hold all the Tweets
  alltweets = []
  # make initial request for most recent tweets 
  # (200 is the maximum allowed count)
  new_tweets = api.user_timeline(screen_name = screen_name,count=200)
  # save most recent tweets
  alltweets.extend(new_tweets)
  # save the id of the oldest tweet less one to avoid duplication
  oldest = alltweets[-1].id - 1
  # keep grabbing tweets until there are no tweets left
  while len(new_tweets) > 0:
    print("getting tweets before %s" % (oldest))
    # all subsequent requests use the max_id param to prevent
    # duplicates
    new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
    # save most recent tweets
    alltweets.extend(new_tweets)
    # update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    print("...%s tweets downloaded so far" % (len(alltweets)))
    ### END OF WHILE LOOP ###
  # transform the tweepy tweets into a 2D array that will 
  # populate the csv
  outtweets = [[tweet.user.screen_name,tweet.id_str, tweet.created_at, tweet.text, tweet.favorite_count,tweet.in_reply_to_screen_name, tweet.retweet_count,tweet.user.followers_count] for tweet in alltweets]
  # write the csv
  return outtweets


if __name__ == '__main__':
    data = pd.DataFrame()
    
    handles = ['stoolpresidente','EKANardini','barstoolbigcat','pftcommenter','kfcbarstool','return_of_rb','paulloduca16','danab_number3','tomscibelli','marty_mush','ChrisRyan77','netw3rk','BillSimmons','micahpeters_','MalloryRubin']
    for handle in handles:
        tweet_data = get_all_tweets(handle)
        df_user = pd.DataFrame(tweet_data,columns=['twitter_profile','tweet_id','creation','text','favorites','replying_to','retweets','total_followers'])
        data = data.append(df_user)
    data.to_excel(r"C:\Users\Anik\Desktop\twitter_analyzer\data.xlsx")

   
