from typing import Optional, List, Iterator
from celery import Celery
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import itertools
from celery import chain, chord, group
from app.celery import celery


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
def get_wikilinks(url: str, session: "requests.sessions.Session" = None) -> List[str]:
    response = session.get(url) if session else requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        links_in_main_article = [
            link.get("href") for link in soup.find(id="content").find_all("a")
        ]
        no_nones: Iterator[str] = filter(None, links_in_main_article)
        only_wiki_links: Iterator[str] = filter(
            lambda x: x.startswith("/wiki/"), no_nones
        )
        valid_urls: Iterator[str] = map(
            lambda x: urljoin("https://en.wikipedia.org", x), only_wiki_links
        )
        return list(valid_urls)
    else:
        return []


@celery.task
def get_article_name(
    url: str, session: "requests.sessions.Session" = None
) -> Optional[str]:
    response = session.get(url) if session else requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find(id="firstHeading").get_text()
    else:
        return None


@celery.task
def check_if_target_reached(
    url: str, target: str, session: "requests.sessions.Session" = None
) -> bool:
    name = get_article_name(url, session) if session else get_article_name(url)
    return name == target


@celery.task
def concatenate_lists_of_urls(list2d: List[List[str]]) -> List[str]:
    return list(itertools.chain(*list2d))


def find_path(source_url: str, target_url: str) -> bool:
    flag = False
    source = get_article_name(source_url)
    target = get_article_name(target_url)
    input_urls = [source_url]
    for _ in range(6):
        url_2dlist = get_wikilinks.map(input_urls).delay().get()
        flat_url_list = concatenate_lists_of_urls(url_2dlist)
        check_list = group(
            check_if_target_reached.s(url, target) for url in flat_url_list
        )().get()
        if any(check_list):
            flag = True
            break
        input_urls = flat_url_list
    return flag


def find_path_with_sessions(source_url: str, target_url: str) -> bool:
    flag = False
    session = requests.session()
    source = get_article_name(source_url, session=session)
    target = get_article_name(target_url, session=session)
    input_urls = [source_url]
    for _ in range(6):
        url_2dlist = [get_wikilinks(input_, session=session) for input_ in input_urls]
        flat_url_list = concatenate_lists_of_urls(url_2dlist)
        check_list = [
            check_if_target_reached(url, target, session=session)
            for url in flat_url_list
        ]
        if any(check_list):
            flag = True
            break
        input_urls = flat_url_list
    return flag
