# A Dockerized Data Pipeline for Sentiment Analysis on tweets
There are 5 steps in data pipeline:
- Extract tweets with [Tweepy API](https://docs.tweepy.org/en/stable/index.html) 
- Load the tweets in a MongoDB
- Extract the tweets from MongoDB, perform sentiment analyisis on the tweets and load the transformed data in a PostgresDB (ETL job)
- Load the tweets and corresponding sentiment assessment in a Postgres database
- Extract the data from the PostgresDB and post it in a slack channel with a slackbot

![workflow](workflow.jpg)

## Usage
- Install [Docker](https://docs.docker.com/get-docker/) on your machine
- Clone the repository: ``` git clone https://github.com/miladbehrooz/Dockerized_Data_Pipeline.git```
- Get credentials for Twitter API and insert them in ```tweet_collector/credentials.py```
- Get credentials for [Slack bot](https://api.slack.com/apps) and insert them in ```slack_bot/credentials.py```
- Run ```docker-compose build```, then ```docker-compose up``` in terminal
