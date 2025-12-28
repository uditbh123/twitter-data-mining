import json
import os
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

# Paths
SENTIMENT_FILE = "data/tweets_sentiment.json"
VISUAL_FOLDER = "visualization"
METADATA_FILE = os.path.join(VISUAL_FOLDER, "metadata.json")

os.makedirs(VISUAL_FOLDER, exist_ok=True)

# Load tweets
if not os.path.exists(SENTIMENT_FILE):
    print(f"{SENTIMENT_FILE} not found. Run sentiment_analysis.py first!")
    exit()

with open(SENTIMENT_FILE, "r", encoding="utf-8") as f:
    tweets = json.load(f)

tweet_count = len(tweets)
print(f"Visualizing {tweet_count} tweets...")

# Load or initialize metadata
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)
else:
    metadata = {}

today = datetime.now().strftime("%Y-%m-%d")
base_filename = f"sentiment_distribution_{today}"
existing_files = metadata.get(today, [])

# Determine PNG filename
counter = 0
while True:
    filename = f"{base_filename}" + (f"({counter})" if counter > 0 else "") + ".png"
    filepath = os.path.join(VISUAL_FOLDER, filename)
    if filepath not in existing_files and not os.path.exists(filepath):
        break
    counter += 1

# Sentiment counts
sentiment_counts = Counter(tweet["sentiment"] for tweet in tweets)
labels = ["positive", "neutral", "negative"]
counts = [sentiment_counts.get(label, 0) for label in labels]

# Create plot
plt.figure(figsize=(8, 6))
bars = plt.bar(labels, counts, color=['green', 'blue', 'red'])
plt.title(f"Sentiment Distribution ({tweet_count} tweets)")
plt.xlabel("Sentiment")
plt.ylabel("Number of Tweets")
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, str(height),
             ha='center', va='bottom')

# Save plot
plt.savefig(filepath, bbox_inches='tight')
plt.close()
print(f"Image saved to {filepath}")

# Update metadata
metadata.setdefault(today, []).append(filepath)
with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=4)
