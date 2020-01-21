from time import time
import os
from dataclasses import dataclass
from typing import List
from urllib.parse import urljoin
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from re import compile


BASE_URL = "https://en.wikipedia.org"
PATTERN = "^/wiki/(?![a-zA-Z]+:)"


async def get_page(url, session):
    response = await session.get(url)
    if response.status == 200:
        return await get_wiki_page(response)
    else:
        return None


@dataclass
class Page:
    title: str
    url: str
    links: List[str]


async def get_wiki_page(response):
    soup = BeautifulSoup(await response.text(), "html.parser")
    urls = soup.find(id="content").findAll(
        "a", attrs={"href": compile(PATTERN)}
    )
    valid_urls: Iterator[str] = map(
        lambda x: urljoin(BASE_URL, x.get("href")), urls
    )
    title = soup.find(id="firstHeading").get_text()
    return Page(title, str(response.url), list(valid_urls)).__dict__


async def async_download_pages(source_, target, field, **kwargs):
    async with aiohttp.ClientSession() as session:
        target = await get_page(target, session)
        source_ = await get_page(source_, session)
        input_pages = [source_]
        all_pages = [source_]
        iteration = 0
        while True:
            print("**")
            if (
                any([target[field] in page["links"] for page in input_pages])
                or iteration == 6
            ):
                break
            links = [l for page in input_pages if page for l in page["links"]]
            input_pages_coros = [await session.get(link) for link in links]
            input_pages = [
                await get_wiki_page(resp) for resp in input_pages_coros
            ]
            all_pages.extend(input_pages)
            iteration += 1
    return all_pages


if __name__ == "__main__":
    # source_url = "https://en.wikipedia.org/wiki/Adolf_Hitler"
    # target_url = "https://en.wikipedia.org/wiki/Nazi_Party"

    loop = asyncio.get_event_loop()
    target_url = (
        "https://en.wikipedia.org/wiki/Conditional_probability_distribution"
    )
    target_url_2 = "https://en.wikipedia.org/wiki/Probability_mass_function"
    source_url = "https://en.wikipedia.org/wiki/Channel_capacity"

    start = time()
    loop = asyncio.get_event_loop()
    pages = loop.run_until_complete(
        async_download_pages(source_url, target_url_2, "url")
    )
    print(pages)
    print(time() - start)
