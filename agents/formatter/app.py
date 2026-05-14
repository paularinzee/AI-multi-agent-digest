import re
import sys
from datetime import datetime
from config import PRIORITIZED_FILE, OUTPUT_FILE
from utils import get_logger

logger = get_logger("formatter")


def format_to_markdown():
    try:
        with open(PRIORITIZED_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logger.error("Input file not found: %s", PRIORITIZED_FILE)
        sys.exit(1)

    if not lines:
        logger.error("Prioritized file is empty — nothing to format.")
        sys.exit(1)

    today = datetime.now().strftime('%Y-%m-%d')

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("# Your Daily AI Digest\n\n")
        out.write(f"**Date:** {today}\n\n")
        out.write("## Top Insights\n\n")
        for line in lines:
            match = re.match(r'^\[(\d+)\]\s+(.+)', line)
            if match:
                score, content = match.group(1), match.group(2)
                out.write(f"- **Priority {score}**: {content}\n")
            else:
                out.write(f"- {line}\n")

    logger.info("Digest written to %s", OUTPUT_FILE)


if __name__ == "__main__":
    format_to_markdown()
