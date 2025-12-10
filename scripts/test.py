from dotenv import load_dotenv
import os

# Load .env from the parent folder
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

bearer_token = os.getenv("BEARER_TOKEN")
if not bearer_token:
    raise ValueError("BEARER_TOKEN not found. Check your .env file and path!")

print("Bearer token loaded successfully")


