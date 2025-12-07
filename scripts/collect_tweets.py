import tweepy
import json
import os
import time
from dotenv import load_dotenv

# -------------------------------
# Load Bearer Token from .env
# -------------------------------
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

bearer_token = os.getenv("BEARER_TOKEN")
if not bearer_token:
    raise ValueError("BEARER_TOKEN not found. Check your .env file and path!")

print("Bearer token loaded successfully")

# -------------------------------
# Create Tweepy Client
# -------------------------------
client = tweepy.Client(bearer_token=bearer_token)

# -------------------------------
# Parameters
# -------------------------------
query = "Python"        # keyword to search
max_results = 10        # tweets per request

# -------------------------------
# Prepare storage
# -------------------------------
data_folder = r"C:\Users\uditb\OneDrive\Desktop\Study\twitter-data-mining\data"
os.makedirs(data_folder, exist_ok=True)
file_path = os.path.join(data_folder, "tweets.json")

tweets_data = []

# -------------------------------
# Fetch tweets with rate-limit handling
# -------------------------------
while True:
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["created_at", "author_id", "text"]
        )

        if response.data:
            for tweet in response.data:
                tweets_data.append(tweet.data)

        # Save to JSON
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(tweets_data, f, ensure_ascii=False, indent=4)

        print(f"Saved {len(tweets_data)} tweets to {file_path}")
        break  # finished successfully

    except tweepy.TooManyRequests:
        print("Rate limit reached. Waiting 15 minutes...")
        time.sleep(15 * 60)  # sleep 15 minutes
