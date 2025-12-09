import tweepy
import json
import os
import time
from dotenv import load_dotenv

# Load Bearer Token from .env

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

bearer_token = os.getenv("BEARER_TOKEN")
if not bearer_token:
    raise ValueError("BEARER_TOKEN not found. Check your .env file and path!")

print("Bearer token loaded successfully")

# Create Tweepy Client

client = tweepy.Client(bearer_token=bearer_token)

# Parameters
query = "Python"        # keyword to search
max_results = 10        # tweets per request


# Prepare storage
data_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(data_folder, exist_ok=True)
file_path = os.path.join(data_folder, "tweets.json")

#load existing tweets if file exists
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf") as f:
        try:
            tweets_data = json.load(f)
        except json.JSONDecoderError:
            tweets_data = []
else:
    tweets_data = []

# make a set of tweet ids to avoid duplicates 
existing_ids = {tweet['id'] for tweet in tweets_data}

#fetch tweets with rate-limit handling
while True:
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=['id', 'text', 'created_at', 'author_id']
        )

        new_count = 0
        if response.data:
            for tweet in response.data:
                if tweet.id not in existing_ids:
                    tweets_data.append(tweet.data)
                    existing_ids.add(tweet.id)
                    new_count += 1
        
        # save to JSON
        with open(file_path, "w", encoding="utf_8") as f:
            json.dump(tweets_data, f, ensure_ascii=False, indent=4)

        print(f"Added {new_count} new tweets. Total stored tweets: {len(tweets_data)}")
        break # finished successfully

    except tweepy.TooManyRequests:
        print("Rate Limit reached. Waiting 15 minutes...")
        time.sleep(15*60) # sleep 15 minutes 
