import json
import os 
from collections import Counter
import matplotlib.pyplot as plt 
from datetime import datetime 

DATA_FILE = "data/tweets_sentiment.json"
OUTPUT_DIR = "visualization"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    tweets = json.load(f)

TOTAL_TWEETS = len(tweets)

# 1. Sentiment Distribution
sentiment_counts = Counter(t["sentiment"] for t in tweets)

labels = ["positive", "neutral", "negative"]
counts = [sentiment_counts.get(l, 0) for l in labels]

dist_path = os.path.join(OUTPUT_DIR, "sentiment_distribution.png")

if not os.path.exists(dist_path):
    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, counts)
    plt.title(f"Sentiment Distribution (n = {TOTAL_TWEETS})")
    plt.xlabel("Sentiment")
    plt.ylabel("Tweet Count")

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height, str(height),
                 ha="center", va="bottom")
                
    plt.savefig(dist_path, bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved {dist_path}")
else:
    print(f"[SKIP] {dist_path} already exists")

# 2. Sentiment percentages 
percent_path = os.path.join(OUTPUT_DIR, "sentiment_percentages.png")

if not os.path.exists(percent_path):
    percentages = [(c / TOTAL_TWEETS) * 100 for c in counts]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, percentages)
    plt.title("Sentiment Percentage Distribution")
    plt.ylabel("Percentages (%)")

    for i, p in enumerate(percentages):
        plt.text(i, p, f"{p:1f}%", ha="center", va="bottom")

    plt.savefig(percent_path, bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved {percent_path}")
else:
    print(f"[SKIP] {percent_path} already exists")

# 3. sentiment over time (daily)
time_path = os.path.join(OUTPUT_DIR, "sentiment_over_time.png")

if not os.path.exists(time_path):
    daily = {}

    for t in tweets:
        date = t["created_at"][:10] # yyyy-mm-dd
        daily.setdefault(date, Counter())
        daily[date][t["sentiment"]] += 1

    dates = sorted(daily.keys())
    pos = [daily[d]["positive"] for d in dates]
    neu = [daily[d]["neutral"] for d in dates]
    neg = [daily[d]["negative"] for d in dates]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, pos, label="positive")
    plt.plot(dates, neu, label="Neutral")
    plt.plot(dates, neg, label="Negative")
    plt.legend()
    plt.xticks(rotation=45)
    plt.title("Sentiment Trend Over Time")
    plt.ylabel("Tweet count")

    plt.savefig(time_path, bbox_inches="tight")
    plt.close()
    print(f"[OK] Saved {time_path}")
else:
    print(f"[Skip] {time_path} already exists")

print(f"\nFinished visualizing {TOTAL_TWEETS} tweets.")