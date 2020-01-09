from typing import Optional, List, Iterator
from celery import Celery  # noqa
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import itertools
from celery import group
from app.celery import celery
from app.wiki import wiki
from re import compile


@celery.task
def add(x, y):
    return x + y


@celery.task
def mul(x, y):
    return x * y


@celery.task
def xsum(numbers):
    return sum(numbers)


@celery.task
def get_page(
    url: str, session: "requests.sessions.Session" = None
) -> wiki.Page(str, str, List[str]):
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
        return wiki.Page(title, url, list(valid_urls))
    else:
        return None


@celery.task
def check_if_target_reached(page: wiki.Page, target: str) -> bool:
    return page.title == target


@celery.task
def flatten_pages(list2d: List[List[wiki.Page]]) -> List[wiki.Page]:
    return list(itertools.chain(*list2d))


def find_path(
    source_url: str,
    target_url: str,
    session: "requests.sessions.Session" = None,
) -> bool:
    session = requests.session()
    target = get_page(target_url, session=session)
    input_urls = [source_url]
    for _ in range(6):
        page_2dlist = get_page.map(input_urls, session=session).delay().get()
        flat_page_list = flatten_pages(page_2dlist)
        check_list = group(
            check_if_target_reached.s(url, target) for url in flat_page_list
        )().get()
        if any(check_list):
            return True
        input_urls = flat_page_list
    return False

