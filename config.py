import os

# --- Directory paths ---
INPUT_DIR       = os.environ.get("INPUT_DIR",    "/data/input")
INGESTED_FILE   = os.environ.get("INGESTED_FILE", "/data/ingested.txt")
SUMMARY_FILE    = os.environ.get("SUMMARY_FILE",  "/data/summary.txt")
PRIORITIZED_FILE = os.environ.get("PRIORITIZED_FILE", "/data/prioritized.txt")
OUTPUT_FILE     = os.environ.get("OUTPUT_FILE",   "/output/daily_digest.md")

# --- Summarizer settings ---
OPENAI_MODEL    = "gpt-4o-mini"
MAX_TOKENS      = 1000
TEMPERATURE     = 0.3
MAX_CHARS       = 8000
MAX_RETRIES     = 3
RETRY_DELAY     = 5  # seconds

# --- Prioritizer keywords ---
PRIORITY_KEYWORDS = [
    "urgent", "today", "asap", "important",
    "deadline", "critical", "action required"
]
