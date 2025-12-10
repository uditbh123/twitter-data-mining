import json 
import os
import re 

# paths
project_root = os.path.dirname(os.path.dirname(__file__))
data_folder = os.path.join(os.path.join(project_root), "data")
os.makedirs(data_folder, exist_ok=True)
input_file = os.path.join(data_folder, "tweets.json")
output_file = os.path.join(data_folder, "cleaned_tweets.json")

#if input files does not exist, create it as empty list
if not os.path.exists(input_file):
    print(f"tweets.json not found. Creating an empty file at: {input_file}")
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)
    print("Created empty tweets.json - run collect_tweets.py first")
    exit()
#cleaning functions
def clean_text(text):
    text = text.lower()

    text = re.sub(r"http\S+|www\S+|https\S+", "", text)     # remove URLs
    text = re.sub(r"@\w+", "", text)                       # remove mentions
    text = re.sub(r"#\w+", "", text)                       # remove hashtags
    text = re.sub(r"rt\s+", "", text)                      # remove RT
    text = re.sub(r"[^\w\s]", "", text)                    # remove punctuation
    text = re.sub(r"\d+", "", text)                        # remove numbers
    text = re.sub(r"\s+", " ", text).strip()               # remove extra spaces

    return text


# Load tweets

with open(input_file, "r", encoding="utf-8") as f:
    tweets = json.load(f)

if not tweets:
    print("tweets.json is empty - run collect_tweets.py first")
    exit()

cleaned = []

# Clean every tweet
for tweet in tweets:
    cleaned_text = clean_text(tweet["text"])
    cleaned.append({
        "id": tweet["id"],
        "original": tweet["text"],
        "cleaned": cleaned_text,
        "created_at": tweet["created_at"]
    })

# save output
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=4)

print(f"Saved {len(cleaned)} cleaned tweets to {output_file}")