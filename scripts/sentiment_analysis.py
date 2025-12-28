import json
import os
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

#File paths
DATA_FOLDER = "data"
CLEANED_FILE = os.path.join(DATA_FOLDER, "cleaned_tweets.json")
SENTIMENT_FILE = os.path.join(DATA_FOLDER, "tweets_sentiment.json")

#Load cleaned tweets
if not os.path.exists(CLEANED_FILE):
    raise FileNotFoundError(f"{CLEANED_FILE} not found. Run clean_tweets.py first!")

with open(CLEANED_FILE, "r", encoding="utf-8") as f:
    cleaned_tweets = json.load(f)

# Initialize vader sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Analyze Sentiment for each tweet
tweets_with_sentiment = []

for tweet in cleaned_tweets:
    text = tweet["cleaned"]
    sentiment_scores = sia.polarity_scores(text)

# Classify sentiment
    if sentiment_scores["compound"] >= 0.05:
        sentiment = "positive"
    elif sentiment_scores["compound"] <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    tweets_with_sentiment.append({
        "id": tweet["id"],
        "original": tweet["original"],
        "cleaned": tweet["cleaned"],
        "created_at": tweet["created_at"],
        "sentiment": sentiment,
        "scores": sentiment_scores
    })

# Save results 
with open(SENTIMENT_FILE, "w", encoding= "utf-8") as f:
    json.dump(tweets_with_sentiment, f, ensure_ascii=False, indent=4)

print(f"Saved sentiment analysis for {len(tweets_with_sentiment)} tweets to {SENTIMENT_FILE}")
