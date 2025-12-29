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

### 2025-12-10

#### Implemented
- Created **`clean_tweets.py`** to **clean raw tweets** stored in `data/tweets.json`.  
  - Cleaning includes:  
    - Converting text to **lowercase**  
    - Removing **URLs, mentions (@username), hashtags (#tag), retweet markers (RT)**  
    - Removing **punctuation, numbers, and extra whitespace**  
  - Cleaned tweets are saved in **`data/cleaned_tweets.json`** with both **original** and **cleaned text**.  

- Updated **`process_tweets.py`** to **tokenize cleaned tweets** from `data/cleaned_tweets.json` instead of raw tweets.  
  - Tokenized tweets are saved in **`data/tokenized_tweets.json`** as a **cumulative file**, appending only new tweets to maintain history.  

- Created **`sentiment_analysis.py`** to perform **sentiment analysis**:  
  - Used **TextBlob** to calculate **polarity** (positive/negative/neutral) and **subjectivity**.  
  - Sentiment results are saved in **`data/sentiment_tweets.json`** along with tweet **ID, cleaned text, and creation date**.  
  - Data is ready for further **visualization or filtering by sentiment**.

#### Key Features
- **Pipeline workflow:** **Collect → Clean → Tokenize → Sentiment analysis → Ready for visualization/NLP**.  
- **Persistent storage:** Avoids overwriting previous tokenized or sentiment data.  
- **Cleaned text preserved:** **Original** and **cleaned text** stored together.  
- **Robust tokenization:** Handles **mentions, hashtags, URLs, words, numbers, and emoticons**.  
- **Safe execution:** Scripts **auto-create missing files** to prevent crashes on first run.  
- **Sentiment ready:** Automatic **polarity and subjectivity scores** for each tweet.

#### Major Problems Faced and Solutions
1. **Missing input files**  
   - Error: `FileNotFoundError` when running `clean_tweets.py` without `tweets.json`.  
   - Cause: Raw tweets not collected yet.  
   - Solution: Added logic to **create an empty `tweets.json` automatically** and instruct user to run `collect_tweets.py` first.

2. **Encoding issues**  
   - Problem: Scripts previously failed with `LookupError: unknown encoding: uft-8` or JSON errors.  
   - Cause: Typo in encoding and inconsistent file formats.  
   - Solution: Corrected all scripts to use **UTF-8** consistently.

3. **Tokenizing cleaned tweets**  
   - Problem: Earlier tokenization used raw tweets including noise like URLs, hashtags, and mentions.  
   - Solution: Tokenized **cleaned tweets** only, improving the quality of tokens.

4. **Maintaining cumulative tokenized and sentiment data**  
   - Problem: Repeated runs risked overwriting previous tokenized or sentiment files.  
   - Solution: Implemented **ID-based duplicate checks** to append only new tweets.

5. **Non-English or messy text in sentiment analysis**  
   - Problem: Tweets with emojis, Arabic text, or mixed characters could mislead **TextBlob**.  
   - Solution: Cleaning removed URLs, mentions, hashtags, extra symbols, and punctuation, improving **sentiment detection accuracy**.

#### Outcome
- All tweets are **cleaned, tokenized, and analyzed for sentiment**.  
- Pipeline is **robust, reproducible, and ready** for NLP, visualization, or dashboard creation.  
- Scripts handle **missing files, malformed JSON, duplicates, and messy text** gracefully, making the workflow **recruiter-ready**.  


---

### 2025-12-12

#### Implemented
- Created **`analyze_sentiment.py`** to **summarize sentiment data** from `data/tweets_sentiment.json`.  
  - Calculates **sentiment distribution** (counts and percentages for positive, neutral, negative).  
  - Extracts **top words per sentiment** from cleaned text to identify common patterns.  
  - Saves a **JSON report** (`data/sentiment_report.json`) for further analysis or visualization.  
  - Prints **summary tables in the terminal** for quick inspection.

#### Key Features
- **Aggregated insights:** Quickly see how many tweets fall into each sentiment category.  
- **Top words per sentiment:** Helps understand which words appear most in positive, neutral, and negative tweets.  
- **Persistent output:** Saves results to a JSON file for reproducibility and sharing.  
- **Error-safe execution:** Handles missing sentiment files or empty datasets gracefully.  
- **Ready for visualization or ML:** Report can be used for plotting charts or feeding into models.

#### Major Problems Faced and Solutions
1. **Top words calculation bug**  
   - Problem: Earlier code returned empty lists or wrong sentiment labels.  
   - Solution: Fixed **looping and label handling**, correctly mapped top words to `positive`, `neutral`, and `negative`.  

2. **Output overwriting concern**  
   - Problem: Each run of the script could overwrite the previous report.  
   - Solution: Output report **always updates**, but can be modified to use timestamps or versioning if historical snapshots are needed.  

3. **Sentiment label consistency**  
   - Problem: Some labels were misspelled (e.g., `neutal`).  
   - Solution: Corrected all scripts to use consistent labels: `positive`, `neutral`, `negative`.  

#### Outcome
- Sentiment report is **complete, accurate, and ready for visualization or analysis**.  
- Pipeline is now fully end-to-end: **Collect → Clean → Tokenize → Sentiment → Summary report**.  
- Can now **analyze trends, build dashboards, or train ML models** on the sentiment data.

### 2025-12-28

#### Implemented
- Created **`visualize_sentiment.py`**:  
  - Generates bar charts for positive, neutral, negative tweets.  
  - Saves PNGs with **dynamic date-based filenames** to avoid overwriting.  
  - Uses `metadata.json` to track previous visualizations.  
  - Annotates bars with tweet counts.  

- Updated **`visualize_insights.py`**:  
  - Creates multiple visualizations: sentiment percentages, distribution over time, top words.  
  - Saves outputs in **`visualization/`** with reproducible filenames.  

- Created **`pipeline_runner.py`**:  
  - Automates the full workflow: Collect → Clean → Tokenize → Sentiment → Analyze → Visualize.  
  - Ensures all new tweets processed, cumulative data maintained, visualizations updated automatically.

#### Key Features
- **End-to-end automation**: Single script runs full pipeline.  
- **Dynamic visualizations**: Versioned PNGs with date and index.  
- **Metadata tracking**: Prevents duplicate plots.  
- **Tweet count in charts**: Clear indication of number of tweets visualized.  
- **Reproducible workflow**: Data, visualizations, and reports are stored separately for sharing and analysis.  

#### Outcome
- All new and existing tweets processed, analyzed, and visualized.  
- Pipeline is **robust, fully automated, and ready for demonstration or ML/NLP tasks**.  

---

## Project Structure


