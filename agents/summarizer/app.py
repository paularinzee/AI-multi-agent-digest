import sys
import time
from openai import OpenAI, RateLimitError, APIError
from config import (
    INGESTED_FILE, SUMMARY_FILE,
    OPENAI_MODEL, MAX_TOKENS, TEMPERATURE,
    MAX_CHARS, MAX_RETRIES, RETRY_DELAY
)
from utils import get_logger

logger = get_logger("summarizer")

SYSTEM_PROMPT = (
    "You are a helpful assistant that summarizes long text "
    "into key bullet points. Each bullet should be one "
    "concise sentence capturing a core insight."
)


def get_client():
    return OpenAI()


def summarize(text, retries=MAX_RETRIES):
    client = get_client()

    if len(text) > MAX_CHARS:
        logger.warning(
            "Input truncated from %d to %d chars — consider chunking for full coverage.",
            len(text), MAX_CHARS
        )
    text_to_send = text[:MAX_CHARS]

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text_to_send}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
            )
            return response.choices[0].message.content
        except RateLimitError:
            wait = RETRY_DELAY * (attempt + 1)
            logger.warning("Rate limited. Retrying in %ds...", wait)
            time.sleep(wait)
        except APIError as e:
            logger.error("API error: %s", e)
            raise

    raise RuntimeError("Max retries exceeded for LLM API call")


def main():
    with open(INGESTED_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    if not raw_text.strip():
        logger.error("Empty input file — nothing to summarize. Aborting.")
        sys.exit(1)

    try:
        summary = summarize(raw_text)
    except Exception as e:
        logger.error("Summarization failed: %s", e)
        sys.exit(1)

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write(summary)
    logger.info("Summary written to %s", SUMMARY_FILE)


if __name__ == "__main__":
    main()
