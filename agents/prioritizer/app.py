import re
import sys
from config import SUMMARY_FILE, PRIORITIZED_FILE, PRIORITY_KEYWORDS
from utils import get_logger

logger = get_logger("prioritizer")


def score_line(line):
    lower = line.lower()
    return sum(
        1 for kw in PRIORITY_KEYWORDS
        if re.search(rf'\b{re.escape(kw)}\b', lower)
    )


def prioritize():
    try:
        with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logger.error("Input file not found: %s", SUMMARY_FILE)
        sys.exit(1)

    if not lines:
        logger.error("Summary file is empty — nothing to prioritize.")
        sys.exit(1)

    scored = [(line, score_line(line)) for line in lines]
    scored.sort(key=lambda x: x[1], reverse=True)

    with open(PRIORITIZED_FILE, "w", encoding="utf-8") as out:
        for line, score in scored:
            if score > 0:
                out.write(f"[{score}] {line}\n")
            else:
                out.write(f"{line}\n")

    logger.info("Prioritized %d items -> %s", len(scored), PRIORITIZED_FILE)


if __name__ == "__main__":
    prioritize()
