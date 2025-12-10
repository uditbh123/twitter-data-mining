import json
import re
import os
from nltk.tokenize import word_tokenize


# File paths

DATA_FILE = "data/cleaned_tweets.json"
TOKENIZED_FILE = "data/tokenized_tweets.json"

# Regex for tokenizing 
emoticons_str = r"""
    (?:
        [:=;]           # Eyes
        [oO\-]?         # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',                    # HTML tags
    r'(?:@[\w_]+)',                # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hashtags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",   # words with - and '
    r'(?:[\w_]+)',                  # other words
    r'(?:\S)'                       # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    """Tokenizes a string using regex"""
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    """Preprocesses a string (tokenize + lowercase if needed)"""
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


# Load existing tokenized tweets if file exists

if os.path.exists(TOKENIZED_FILE):
    with open(TOKENIZED_FILE, "r", encoding="utf-8") as f:
        tokenized_tweets = json.load(f)
    print(f"Loaded {len(tokenized_tweets)} previously tokenized tweets.")
else:
    tokenized_tweets = []
    print("No previous tokenized tweets found. staring fresh.")

# load new tweets
with open(DATA_FILE, "r", encoding="utf-8") as f:
    new_tweets = json.load(f)

print(f"Total new tweets to loaded: {len(new_tweets)}")

# Process and append only new tweets
existing_ids = {tweet["id"] for tweet in tokenized_tweets}
for tweet in new_tweets:
    if tweet["id"] not in existing_ids: # avoid duplicates
        tokens = preprocess(tweet.get("text", ""))
        tokenized_tweets.append({
            "id": tweet.get("id"),
            "author_id": tweet.get("author_id"),
            "created_at": tweet.get("created_at"),
            "tokens": tokens
        })

#save all tokenized tweets back to the same file 
with open(TOKENIZED_FILE, "w", encoding="utf-8") as f:
    json.dump(tokenized_tweets, f, ensure_ascii=False, indent=4)

print(f"All tokenized tweets saved. Total now: {len(tokenized_tweets)}")