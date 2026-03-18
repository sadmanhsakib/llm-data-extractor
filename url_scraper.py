import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


def main():
    site_url = "https://paste.fitgirl-repacks.site/?fad3baf0fad437cf#HVjnbfAB9Hk8TXWpUndxnjuseaytwd46RLX8SzZfv1Ku"

    soup = asyncio.run(scrape_url(site_url))
    # saving the data to a file

    with open("scraped_data.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())
        print("Data saved to scraped_data.html")


async def scrape_url(site_url):
    async with async_playwright() as playwright:
        # launching the browser
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Navigating to the site.....")
        await page.goto(site_url, wait_until="networkidle")

        html_content = await page.content()

        soup = BeautifulSoup(html_content, "html.parser")

        return soup


main()
