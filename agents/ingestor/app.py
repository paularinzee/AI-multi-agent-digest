import os
import sys
from config import INPUT_DIR, INGESTED_FILE
from utils import get_logger

logger = get_logger("ingestor")


def ingest():
    files_processed = 0

    with open(INGESTED_FILE, "w", encoding="utf-8") as out:
        for filename in sorted(os.listdir(INPUT_DIR)):
            if filename.startswith(".") or not filename.endswith(".txt"):
                logger.info("Skipping file: %s", filename)
                continue

            filepath = os.path.join(INPUT_DIR, filename)
            if not os.path.isfile(filepath):
                continue

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    out.write(f"\n--- {filename} ---\n")
                    out.write(f.read())
                    out.write("\n")
                    files_processed += 1
            except Exception as e:
                logger.error("Failed to read %s: %s", filename, e)

    if files_processed == 0:
        logger.error("No input files found in %s — aborting pipeline.", INPUT_DIR)
        sys.exit(1)

    logger.info("Ingested %d files -> %s", files_processed, INGESTED_FILE)


if __name__ == "__main__":
    ingest()
