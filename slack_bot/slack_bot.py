import time
import pandas as pd
import requests
from sqlalchemy import create_engine
from credentials import webhook_url

time.sleep(20)

# Establish a connection to the Postgres server
pg = create_engine('postgresql://postgres:postgres@postgresdb:5432/twitter', echo=True)

# Post the last tweet in the database to a slack channel every 30 seconds
while True:
    time.sleep(30)
    query = "SELECT * FROM tweets;"
    df = pd.read_sql(query, pg)
    last_tweet = df.tail(1)
    last_tweet.reset_index(inplace=True,drop=True)
    data = last_tweet.to_dict()
    message = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*@{data['username'][0]}*\n {data['created_at'][0]}\n  {data['text'][0]} \n *Sentiment:*{data['sentiment'][0]}"
                },
                "accessory": {
                    "type": "image",
                    "image_url": f"{data['profile_image_url'][0]}",
                    "alt_text": "alt text for image"
                }
            }
        ]
    }
    requests.post(url=webhook_url, json = message)