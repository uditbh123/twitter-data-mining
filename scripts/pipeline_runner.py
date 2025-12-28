import os
import json

scripts = [
    "collect_tweets.py",
    "clean_tweets.py",
    "process_tweets.py",
    "sentiment_analysis.py",
    "analyze_sentiment.py",
    "visualize_sentiment.py",
    "visualize_insights.py"
]

VISUAL_FOLDER = "visualization"
METADATA_FILE = os.path.join(VISUAL_FOLDER, "metadata.json")

os.makedirs(VISUAL_FOLDER, exist_ok=True)

for script in scripts:
    path = os.path.join("scripts", script)
    if os.path.exists(path):
        print(f"\nRunning {script}...")
        os.system(f'python "{path}"')
    else:
        print(f"Script {script} not found, skipping...")

# At the end, print summary of today's generated visualizations
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    today = max(metadata.keys())  # Last date
    files_today = metadata[today]
    print(f"\nGenerated {len(files_today)} visualization(s) today:")
    for file in files_today:
        print(f" - {file}")
else:
    print("\nNo visualizations generated yet.")