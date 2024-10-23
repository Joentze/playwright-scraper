"""handles scraping operation"""
from typing import List
import asyncio
from threading import Thread
from datetime import datetime
from playwright.async_api import async_playwright
from scraper.playwright import PlaywrightScraper

urls = [
    "https://www.channelnewsasia.com/",
    "https://nypost.com/",
    "https://www.channelnewsasia.com/",
    "https://nypost.com/",
    "https://www.channelnewsasia.com/",
    "https://nypost.com/",
    "https://www.channelnewsasia.com/",
    "https://nypost.com/",
    "https://www.channelnewsasia.com/",
    "https://nypost.com/",

]

completed_htmls: List[str] = []

NO_OF_THREADS: int = 4


def chunk_urls(urls: List[str], chunk_size: int) -> List[List[str]]:
    """split urls into uniform arrays"""
    if len(urls) <= chunk_size:
        return [urls]
    chunks: List[List[str]] = []
    no_of_chunks = (len(urls)//chunk_size)+1
    for i in range(no_of_chunks):
        start, end = i*chunk_size, (i*chunk_size)+chunk_size
        chunked_urls = urls[start:end]
        chunks.append(chunked_urls)
    return chunks


def create_batches(urls=List[str], chunk_size: int = 10, no_of_threads: int = NO_OF_THREADS) -> List[List[List[str]]]:
    """creates batch to process"""
    chunks = chunk_urls(urls=urls, chunk_size=chunk_size)
    no_of_batches = chunk_urls(urls=chunks, chunk_size=no_of_threads)
    return no_of_batches


async def scrape(urls: List[str]) -> None:
    """runs asynchronously"""
    async with async_playwright() as playwright:
        scraper = PlaywrightScraper(playwright=playwright, headless=False)
        htmls = await scraper.run(urls=urls)
        print("len urls", len(urls), "len htmls",
              len([html for html in htmls if html is not None]))
        global completed_htmls
        completed_htmls += htmls


def run(urls: List[str], no_of_threads: int = NO_OF_THREADS) -> List[str]:
    """runs playwright scraper"""
    batches = create_batches(urls=urls, no_of_threads=no_of_threads)
    for _, chunks in enumerate(batches):
        threads: List[Thread] = []
        for chunk in chunks:
            threads.append(Thread(target=asyncio.run,
                           args=(scrape(urls=chunk),)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


if __name__ == "__main__":

    t1 = datetime.now()
    run(urls=urls)
    print("urls", len(urls), "completed htmls", len(completed_htmls))
    with open("test.md", "w") as file:
        file.write([html for html in completed_htmls if html is not None][0])
    t2 = datetime.now()
    print("time taken:", t2 - t1)
