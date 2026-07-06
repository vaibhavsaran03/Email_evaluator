import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

DATASET_PATH = "data/historical_emails.json"

TEST_DATASET_PATH = "data/test_emails.json"

GENERATED_PATH = "data/generated.json"