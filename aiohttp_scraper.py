from time import time
import os
from dataclasses import dataclass
from typing import List
from urllib.parse import urljoin
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from re import compile
import functools

BASE_URL = "https://en.wikipedia.org"
PATTERN = "^/wiki/(?![a-zA-Z]+:)"

count = 0


def debug(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        global count
        count += 1
        tmp = count
        print(f"{tmp}. Function {func.__name__} started executing")
        res = await func(*args, **kwargs)
        print(f"{tmp}. Function {func.__name__} ended executing")
        return res

    return wrapper


@debug
async def download_wiki_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.text()
            return get_wiki_page(content, resp)


@dataclass
class Page:
    title: str
    url: str
    links: List[str]


def get_wiki_page(content, response):
    title = None
    valid_urls = []
    if content:
        soup = BeautifulSoup(content, "html.parser")
        urls = soup.find(id="content").findAll(
            "a", attrs={"href": compile(PATTERN)}
        )
        valid_urls: Iterator[str] = map(
            lambda x: urljoin(BASE_URL, x.get("href")), urls
        )
        title = soup.find(id="firstHeading").get_text()
    return Page(title or "", str(response.url), list(valid_urls)).__dict__


async def async_download_pages(source_, target, field, **kwargs):
    target, source_ = await asyncio.gather(
        *[download_wiki_html(target), download_wiki_html(source_)]
    )
    input_pages = [source_]
    all_pages = [source_]
    iteration = 0
    while True:
        if (
            any([target[field] in page["links"] for page in input_pages])
            or iteration == 5
        ):
            break
        links = [l for page in input_pages if page for l in page["links"]]
        print(f"There are {len(links)} to scrape...")
        input_pages = await asyncio.gather(
            *[download_wiki_html(link) for link in links]
        )
        all_pages.extend(input_pages)
        iteration += 1
    return all_pages


if __name__ == "__main__":
    # source_url = "https://en.wikipedia.org/wiki/Adolf_Hitler"
    # target_url = "https://en.wikipedia.org/wiki/Nazi_Party"

    target_url = (
        "https://en.wikipedia.org/wiki/Conditional_probability_distribution"
    )
    target_url_2 = "https://en.wikipedia.org/wiki/Probability_mass_function"
    source_url = "https://en.wikipedia.org/wiki/Channel_capacity"

    source_url = "https://en.wikipedia.org/wiki/Adolf_Hitler"
    target_url_2 = (
        "https://en.wikipedia.org/wiki/St._Augustine%27s_Monastery_(Erfurt)"
    )

    start = time()
    pages = asyncio.run(async_download_pages(source_url, target_url_2, "url"))
    print(pages)
    print(time() - start)
