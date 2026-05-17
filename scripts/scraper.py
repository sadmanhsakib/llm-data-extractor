"""
Module for scraping web content and converting it to Markdown.

This script uses Playwright to handle dynamic content and converts the resulting 
HTML into a clean Markdown format suitable for LLM processing.
"""

import asyncio, os, time
from playwright_stealth import Stealth
from playwright.async_api import async_playwright
from markdownify import markdownify as md


def main() -> None:
    asyncio.run(fetch_page("https://www.google.com"))


async def fetch_page(site_url: str, wait_until : str = "networkidle") -> str:
    """
    Asynchronously fetches the HTML content of a given URL.
    
    Uses Playwright with stealth techniques to avoid detection by anti-bot
    measures and ensures that dynamic (JavaScript-rendered) content is fully
    loaded before capturing the page content.
    """
    async with async_playwright() as playwright:
        # Headless mode is used to run the browser in the background without a GUI,
        # which is more efficient for automated scraping tasks.
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()

        await Stealth().apply_stealth_async(page)

        print(f"Navigating to the site: {site_url}")

        await page.goto(site_url, wait_until=wait_until)

        html_content = await page.content()
        await browser.close()

        return html_content


def export_as_markdown(html_content: str) -> str:
    """
    Converts HTML content to Markdown and saves it to a file.
    
    Markdown is preferred over HTML for LLM processing because it preserves 
    structural information (headings, lists) while significantly reducing 
    token usage by removing unnecessary tags.
    """
    # Removing non-textual or layout-heavy tags to reduce noise and focus 
    # the LLM on the core content of the page.
    markdown_content = md(
        html_content,
        heading_style="ATX",
        strip=[
            "script", "style", "img", "svg", "head", 
            "footer", "header", "nav", "aside",
        ],
    )

    # Save the processed content for the parser module to read.
    # UTF-8 encoding ensures that special characters are handled correctly.
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    output_path = os.path.join(data_dir, 'webpage.md')
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(markdown_content)
    print(f"✅ Data saved to {output_path}")
    
    return output_path


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"✅ Run Time is {time.time() - start_time:.2f} seconds")
