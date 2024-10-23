"""handles scraping operation"""
import asyncio
from playwright.async_api import async_playwright
from base.playwright import PlaywrightScraper

urls = [
    f"https://clinicaltrials.gov/search?cond=Breast%20Cancer&aggFilters=phase:1%202%203,results:with,studyType:int&page={cnt}&limit=100" for cnt in range(1, 6)
]


async def main() -> None:
    """runs asynchronously"""
    async with async_playwright() as playwright:
        scraper = PlaywrightScraper(playwright=playwright, headless=False)
        htmls = await scraper.run(urls=urls)

    for i, html in enumerate(htmls):
        with open(f"./htmls/{i}.html", "w") as file:
            file.write(html)


if __name__ == "__main__":
    asyncio.run(main())
