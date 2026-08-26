import logging
import os
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load environment variables (e.g., SLACK_WEBHOOK_URL)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent / "data"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("formatter")

INPUT_FILE = BASE_DIR / "prioritized.txt"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "daily_digest.md"

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def post_to_slack(text):
    """Posts the formatted markdown string directly to Slack via Incoming Webhook."""
    if not SLACK_WEBHOOK_URL:
        logger.warning(
            "SLACK_WEBHOOK_URL not found in environment. Skipping Slack notification."
        )
        return

    payload = {"text": text}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            logger.info("Successfully posted daily digest to Slack!")
        else:
            logger.error(
                f"Failed to post to Slack: {response.status_code} - {response.text}"
            )
    except Exception as e:
        logger.error(f"Error sending request to Slack: {e}")


def format_to_markdown():
    if not INPUT_FILE.exists():
        logger.error(f"Input file not found: {INPUT_FILE}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    today = datetime.now().strftime("%Y-%m-%d")

    # Build markdown digest string
    digest_lines = [
        "# Your Daily AI Digest\n",
        f"**Date:** {today}\n",
        "## Top Insights\n",
    ]

    for line in lines:
        if "] " in line:
            score = line.split("]")[0][1:]
            content = line.split("] ", 1)[1]
            digest_lines.append(f"- **Priority {score}**: {content}")
        else:
            digest_lines.append(f"- {line}")

    digest_content = "\n".join(digest_lines)

    # 1. Save locally to output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(digest_content)

    logger.info(f"Digest written to {OUTPUT_FILE}")

    # 2. Post digest to Slack
    post_to_slack(digest_content)


if __name__ == "__main__":
    format_to_markdown()