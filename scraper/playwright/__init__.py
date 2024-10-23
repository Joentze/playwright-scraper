"""classes for handling scrapers"""
import asyncio
from typing import List, Literal, Coroutine, Any
from playwright.async_api import Playwright, Page, Route, Browser, BrowserType


class PlaywrightScraper:
    """
    Base class for playwright scraper for html scraping
    properties:
        playwright (Playwright): playwright client
        optimise (bool): prevent download of images, videos, stylesheets, fonts
    """

    def __init__(self,
                 playwright: Playwright,
                 optimise: bool = True,
                 timeout: int = 10000,
                 headless: bool = True,
                 browser_type: Literal["chromium", "webkit", "firefox"] = "chromium") -> None:
        self.browser_type = browser_type
        self.playwright = playwright
        self.optimise = optimise
        self.timeout = timeout
        self.headless = headless
        self.RESOURCE_TYPES: List[str] = [
            'image', 'stylesheet', 'media', 'font', 'other']

    async def run(self, urls: List[str]) -> List[str]:
        """runs scraper"""
        browser_type: BrowserType = getattr(self.playwright, self.browser_type)
        browser: Browser = await browser_type.launch(headless=self.headless)
        html_returns: List[Coroutine[Any, Any, str]] = [
            self.__get_html(browser=browser, url=url) for url in urls]
        response = await asyncio.gather(*html_returns)
        await browser.close()
        return response

    async def __get_html(self, browser: Browser, url: str) -> Coroutine[str, str, Any]:
        """opens new tab, gets html content"""
        page: Page = await browser.new_page()
        if self.optimise:
            await self.__optimise_page_load(page=page)
        try:
            await page.goto(url=url, wait_until="domcontentloaded", timeout=10000)
            return await page.inner_html(selector="body", timeout=self.timeout)
        except Exception as e:
            return None

    async def __optimise_page_load(self, page: Page) -> None:
        """blocks memory intensive resources"""
        await page.route("**/*", self.__block_resources)

    def __block_resources(self, route: Route) -> None:
        """checks if resources is restricted in optimisation"""
        return route.abort() if route.request.resource_type in self.RESOURCE_TYPES else route.continue_()
