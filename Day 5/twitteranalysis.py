from tweepy import API 
from tweepy import OAuthHandler
from textblob import TextBlob
import numpy as np
import pandas as pd
import re
import twitter_credentials


class Twitter():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuth().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets


class TwitterAuth():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth



class TweetAnalysis():
   
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0:
            return ("Not Toxic")
        elif analysis.sentiment.polarity == 0:
            return ("OK")
        else:
            return ("Toxic")

    def tweets_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df


twitter_client = Twitter()
tweet_analyzer = TweetAnalysis()

api = twitter_client.get_twitter_client_api()

tweets = api.user_timeline(screen_name="narendramodi", count=200)

df = tweet_analyzer.tweets_data_frame(tweets)
df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

print(df.head(10))