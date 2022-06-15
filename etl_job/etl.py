import pymongo
import pandas as pd
import time
import re
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Define functions 

def extract():
    ''' reads data from MongoDB and return the tweets in a dataframe
    '''
    # Select the database you want to use withing the MongoDB server
    db = client.twitter
    # Read a few entries from MongoDB and put text of tweets in a list
    docs = db.tweets.find()
    wanted_keys = ['username','profile_image_url','created_at','text']
    tweets = [ {x:doc[x] for x in wanted_keys} for doc in docs ]
    # Convert list of tweets in pandas dataframe
    df = pd.DataFrame(tweets)
    return df


def transform(df):
    ''' clean tweets, and perform the sentiment analysis and finally return the result in a dataframe
    '''
    # Clean tweets
    df['text_cleared'] = df['text'].apply(clean_tweets)
    # Run the sentiment analysis
    analyser  = SentimentIntensityAnalyzer()
    # Make dataframe of polarity scores
    pol_scores = df['text_cleared'].apply(analyser.polarity_scores).apply(pd.Series)
    # Add the sentiment analysis results to the tweets dataframe
    df=pd.concat([df, pol_scores['compound']], axis=1)
    df.rename(columns = {'compound':'sentiment'},inplace=True) 
      
    return df

def load(df):
    ''' store the result in the a postgres database
    '''
    df.to_sql('tweets', pg, if_exists='replace')
    

def clean_tweets(tweet):
    mentions_regex= '@[A-Za-z0-9]+'
    url_regex='https?:\/\/\S+'
    hashtag_regex= '#'
    rt_regex= 'RT\s'  
    tweet = re.sub(mentions_regex, '', tweet)  # removes @mentions
    tweet = re.sub(hashtag_regex, '', tweet) # removes hashtag symbol
    tweet = re.sub(rt_regex, '', tweet) # removes RT to announce retweet
    tweet = re.sub(url_regex, '', tweet) # removes most URLs
    
    return tweet


time.sleep(10)  # seconds

# Establish a connection to the MongoDB server
client = pymongo.MongoClient(host="mongodb", port=27017)

# Establish a connection to the Postgres server
pg = create_engine('postgresql://postgres:postgres@postgresdb:5432/twitter', echo=True)

while True:
   load(transform(extract()))  
   time.sleep(10) 

