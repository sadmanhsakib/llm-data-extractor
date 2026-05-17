import asyncio, os, time
import scraper
import parser
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl


load_dotenv()

SITE_URL = os.getenv("SITE_URL")


# Strict instructions to ensure the LLM focuses purely on data extraction
# and does not include conversational filler which could break JSON parsing.
SYSTEM_PROMPT = """
You are a data extraction assistant.
Respond ONLY with a valid JSON object. No explanation, no markdown fences.
Extract only the information related to the VIDEO.
For example, video title, video duration, video url.
"""

class Schema(BaseModel):
    """Schema for a single extracted data."""

    title: str
    duration: str
    url: HttpUrl


def main():
    html_content = asyncio.run(
        scraper.fetch_page(SITE_URL, wait_until="load")
    )

    if html_content:
        md_path = scraper.export_as_markdown(html_content)
    else:
        raise Exception("❌ No HTML content found")

    parser.extract_data_from_markdown(
        md_path=md_path, SYSTEM_PROMPT=SYSTEM_PROMPT, is_local=False
    )


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"✅ Run Time is {time.time() - start_time:.2f} seconds")
