# Twitter Data Mining Project

This project demonstrates how to collect tweets using Python and the Twitter API (v2) with Tweepy. The project is designed to track learning progress, record challenges and solutions, and provide a clear workflow for anyone following along.

---

## Timeline of Work

### 2025-12-07

#### Setup
- Created the Python project folder structure.
- Installed necessary libraries: `tweepy` and `python-dotenv`.
- Created a `.env` file to securely store the Twitter Bearer Token.

#### Implemented
- Wrote `collect_tweets.py` to fetch recent tweets by keyword.
- Tweets are saved into `data/tweets.json`.
- Added error handling for API rate limits (429 Too Many Requests).
- Verified Bearer Token loads correctly from `.env`.

#### Errors Faced and Solutions

1. **SyntaxError on `import tweepy`**  
   - Cause: File was named `streaming.py` previously, which conflicted with Python internal files.  
   - Solution: Renamed the script to `collect_tweets.py`.

2. **403 Forbidden / 401 Unauthorized errors**  
   - Cause: Free Twitter API accounts have limited access to some endpoints or wrong authentication method.  
   - Solution: Switched to using **API v2 with Bearer Token** for recent tweet search.

3. **Environment variable not loading (`BEARER_TOKEN = None`)**  
   - Cause: `.env` file was incorrectly named or in the wrong folder.  
   - Solution: Renamed file to `.env` and used proper path in `load_dotenv()`.

4. **400 Bad Request**  
   - Cause: Typo in parameter `max_result` instead of `max_results`.  
   - Solution: Corrected the parameter name to `max_results`.

5. **429 Too Many Requests (Rate Limit)**  
   - Cause: Exceeded the number of requests allowed by free API tier.  
   - Solution: Added **automatic rate-limit handling** with `time.sleep(15*60)`.

#### Outcome
- Script runs successfully and fetches tweets by keyword `"Python"`.
- Tweets are saved in `data/tweets.json`.
- Able to run repeatedly without authentication or rate-limit issues.

#### Next Steps
- Implement fetching tweets from a specific user (timeline).
- Add more flexible search parameters and data analysis.
- Prepare project for GitHub upload with proper `.gitignore`.

---
### 2025-12-09

#### Implemented
- Created `process_tweets.py` to read saved tweets and tokenize their text.
- Used **regex and NLTK** to handle mentions, hashtags, URLs, emoticons, and words.
- Tokenized tweets stored in a **cumulative JSON file** (`data/tokenized_tweets.json`) that appends new tokenized tweets without overwriting previous data.
- Verified all tweets processed correctly and displayed sample tokenized output.

#### Key Features
- **Persistent storage:** Tokenized tweets are appended to a single file to maintain history.
- **Robust tokenization:** Regex handles URLs, hashtags, mentions, numbers, words, and emoticons.
- **Error handling:** Skips malformed lines, ensures JSON loads safely.
- **Reproducible workflow:** Can run collection and processing scripts repeatedly without losing previous data.

#### Major Problems Faced and Solutions

1. **Malformed JSON errors**  
   - Error: `JSONDecodeError: Expecting value / Extra data` when trying to read `tweets.json`.
   - Cause: Tweets were saved as a full JSON array, but the previous processing script expected **one tweet per line**.
   - Solution: Updated `process_tweets.py` to read the array and iterate through each tweet properly, handling all malformed lines safely.

2. **ModuleNotFoundError for NLTK**  
   - Error: `No module named 'nltk'`.
   - Cause: NLTK not installed in Python environment or script using a different interpreter.
   - Solution: Installed NLTK via `pip install nltk` and ensured the correct Python interpreter was used.

3. **Cumulative storage for tokenized tweets**  
   - Problem: Running the script repeatedly overwrote previous tokenized tweets.
   - Solution: Implemented logic to append new tokenized tweets to `data/tokenized_tweets.json`, preserving history.

#### Outcome
- Successfully processed and tokenized all tweets.
- Stored cumulative tokenized tweets for further analysis.
- Scripts now robust against malformed input, encoding errors, duplicated and repeated runs.

---


## Project Structure

