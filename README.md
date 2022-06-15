# A Dockerized Data Pipeline for Sentiment Analysis on tweets
There are 5 steps in data pipeline:
- Extract tweets with [Tweepy API](https://docs.tweepy.org/en/stable/index.html) 
- Load the tweets in a MongoDB
- Extract the tweets from MongoDB, perform sentiment analyisis on the tweets and load the transformed data in a PostgresDB (ETL job)
- Load the tweets and corresponding sentiment assessment in a Postgres database
- Extract the data from the PostgresDB and post it in a slack channel with a slackbot
![workflow](workflow.jpeg)
