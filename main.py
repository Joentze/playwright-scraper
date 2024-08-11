"""handles scraping operation"""
import asyncio
from playwright.async_api import async_playwright
from base.playwright import PlaywrightScraper

urls = [
    "https://www.channelnewsasia.com/",
    "https://nypost.com/"
]


async def main() -> None:
    """runs asynchronously"""
    async with async_playwright() as playwright:
        scraper = PlaywrightScraper(playwright=playwright, headless=False)
        htmls = await scraper.run(urls=urls)
    for i, html in enumerate(htmls):
        with open(f"{i}_html.html", "w") as file:
            file.write(html)


if __name__ == "__main__":
    asyncio.run(main())
