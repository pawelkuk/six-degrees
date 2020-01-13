from typing import Optional, List, Iterator, Dict, Callable
from celery import Celery # noqa
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import itertools
from celery import group
from app.celery import celery
from app.wiki import wiki
from re import compile
import wikipedia


@celery.task
def get_page_with_api(title: str) -> Dict:
    page = None
    try:
        page = wikipedia.page(
            title=title, pageid=None, auto_suggest=True, redirect=True
        )
    except wikipedia.DisambiguationError as e:
        title = e.options[0]
        page = wikipedia.page(
            title=title, pageid=None, auto_suggest=True, redirect=True
        )
    except wikipedia.PageError as e:
        return None
    finally:
        return {"title": page.title, "url": page.url, "links": page.links}


@celery.task
def get_page(
    url: str,
    session: "requests.sessions.Session" = None
) -> Dict:
    response = session.get(url) if session else requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        urls = soup.find(id="content").findAll(
            "a", attrs={"href": compile(wiki.PATTERN)}
        )
        valid_urls: Iterator[str] = map(
            lambda x: urljoin(wiki.BASE_URL, x.get("href")), urls
        )
        title = soup.find(id="firstHeading").get_text()
        return {"title": title, "url": url, "links": list(valid_urls)}
    else:
        return None


@celery.task
def check_if_target_reached(page: Dict, target: Dict, field: str) -> bool:
    return page[field] == target[field]


def download_pages(
    download_func: Callable, source: str, target: str, field: str, **kwargs
):
    target = download_func(source, **kwargs)
    source = download_func(target, **kwargs)
    input_pages = [source]
    all_pages = [source]
    iteration = 0
    while True:
        links = [l for page in input_pages for l in page["links"]]
        pages = group(download_func.s(link) for link in links)().get()
        all_pages.extend(pages)
        check_list = group(
            check_if_target_reached.s(page, target, field) for page in pages
        )().get()
        if any(check_list) or iteration == 6:
            break
        input_pages = pages
        iteration += 1
    return all_pages