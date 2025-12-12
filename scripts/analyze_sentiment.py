import json 
from collections import Counter
import os 

SENTIMENT_FILE = "data/tweets_sentiment.json"
OUTPUT_REPORT = "data/sentiment_report.json"

#load data 
if not os.path.exists(SENTIMENT_FILE):
    print("sentiment_tweets.json not found. Run sentiment_analysis.py first")
    exit ()

with open(SENTIMENT_FILE, "r", encoding="utf-8") as f:
    tweets = json.load(f)

print(f"Loaded {len(tweets)} tweets with sentiment.")

#sentiment distribution

sentiment_counts = Counter(tweet["sentiment"] for tweet in tweets)

print("\n=== Sentiment Distribution ===")
for sent, count in sentiment_counts.items():
    print(f"{sent}: {count} tweets")

total = len(tweets)
percentages = {
    sent: round((count / total) * 100, 2) 
    for sent, count in sentiment_counts.items()
}

print("\n=== Sentiment Percentages ===")
for sent, pct in percentages.items():
    print(f"{sent}: {pct}%")

# 2. most common words per sentiment 

def get_tokens(tweet):
    return tweet["cleaned"].split()

def most_common_words(tweets, sentiment, n=10):
    words = []
    for t in tweets:
        if t["sentiment"] == sentiment:
            words.extend(get_tokens(t))
    return Counter(words).most_common(n)
    
sentiment_labels = ["positive", "neutral", "negative"]
sentiment_top_words = {}

print("\n=== Top Words per Sentiment ===")
for sentiment in sentiment_labels:
    top = most_common_words(tweets, sentiment)
    sentiment_top_words[sentiment] = top
    
    if not top:
        print(f"\n{sentiment.upper()}: No tweets available")
    else:
        print(f"\n{sentiment.upper()} TOP WORDS:")
        for word, count in top:
            print(f"{word}: {count}")

# save report to json

report = {
    "total_tweets": total,
    "sentiment_distribution": dict(sentiment_counts),
    "sentiment_percentages": percentages,
    "top_words": sentiment_top_words,
}

with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=4)

print(f"\nSaved analysis report to {OUTPUT_REPORT}")