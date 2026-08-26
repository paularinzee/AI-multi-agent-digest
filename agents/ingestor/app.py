import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent / "data"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ingestor")

INPUT_DIR = BASE_DIR / "input"
OUTPUT_FILE = BASE_DIR / "ingested.txt"


def ingest():
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    content = ""
    files_processed = 0

    for file_path in sorted(INPUT_DIR.iterdir()):
        if file_path.is_file():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content += f"\n--- {file_path.name} ---\n"
                    content += f.read()
                    content += "\n"
                    files_processed += 1
            except Exception as e:
                logger.error(f"Failed to read {file_path.name}: {e}")

    if files_processed == 0:
        logger.warning(f"No input files found in {INPUT_DIR}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(content)

    logger.info(f"Ingested {files_processed} files -> {OUTPUT_FILE}")


if __name__ == "__main__":
    ingest()