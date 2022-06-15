import tweepy
import pymongo
from credentials import BEARER_TOKEN, ACESS_TOKEN_SECRET,API_KEY, API_KEY_SECRET


# Connect to the MONGO database 
client_mongo = pymongo.MongoClient(
    host="mongodb",
    port=27017
)
# Define database
db = client_mongo.twitter


# Authentication 
client_twitter = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True,
)

# Search for Tweets 

search_query = "elon musk -is:retweet -is:reply -is:quote lang:en -has:links"

cursor = tweepy.Paginator(
    method=client_twitter.search_recent_tweets,
    query=search_query,
    tweet_fields=['author_id', 'created_at'],
).flatten()


for tweet in cursor:
    tweet = dict(tweet)
    response = client_twitter.get_user(
    id=tweet['author_id'],
    user_fields=['username','profile_image_url'])
    user = dict(response.data)
    username = user['username']
    profile_image_url = user['profile_image_url']
    tweet["username"] = username
    tweet["profile_image_url"] = profile_image_url
    print(tweet)
    db.tweets.insert_one(tweet)
