import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
 
class TwitterClient(object):
    # Generic Twitter Class for sentiment analysis.
    def __init__(self):
        # Class constructor or initialization method.
        consumer_key = '243trOMhA8Ks093T0A0Kiteez'
        consumer_secret = 'KQrRguANYbejdzcGunxtnvLi36FJRZm70V9sepTs0UuBLgLryD'
        access_token = '706090681148702720-aNKvlQxPPCBXQHueD8x5yZBHSzQpHvF'
        access_token_secret = '81XE5HrOrrG1nOeZFMQZA0OGQdssLNQq2sh1Y16yd32AB' 

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self,tweet):
        # Utility function to clean tweet text by removing links, special characters
        # using simple regex statements.
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", tweet).split())
 
    def get_tweet_sentiment(self,tweet):
        # Utility function to classify sentiment of passed tweet
        # using textblob's sentiment method
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 10):   
        # Main function to fetch tweets and parse them.
        # empty list to store parsed tweets
        tweets = []
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
 
def main():

    queryTweet = input()
    countLimit = input()

    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(queryTweet, countLimit)
 
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    neutraltweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    print("Neutral tweets percentage: {} %".format(100*len(neutraltweets)/len(tweets)))

    print("\nTotal Tweets = " + str(len(tweets)))

    tweetNumber = 1
    # printing first 5 positive tweets
    print("\n\nPositive tweets:\n")
    for tweet in ptweets[:10]:
        print(str(tweetNumber) + " " + tweet['text']).encode('utf-8')
	tweetNumber = tweetNumber + 1
 
    tweetNumber = 1
    # printing first 5 negative tweets
    print("\n\nNegative tweets:\n")
    for tweet in ntweets[:10]:
        print(str(tweetNumber) + " " + tweet['text']).encode('utf-8')
	tweetNumber = tweetNumber + 1

    tweetNumber = 1
    print("\n\nNeutral tweets:\n")
    for tweet in neutraltweets[:10]:
        print(str(tweetNumber) + " " + tweet['text']).encode('utf-8')
	tweetNumber = tweetNumber + 1
 
if __name__ == "__main__":
    # calling main function
    main()
