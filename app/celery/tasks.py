from typing import Optional, List, Iterator, Dict, Callable
from celery import Celery  # noqa
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import itertools
from celery import group
from app.celery import celery
from app.wiki import wiki
from app.wiki.wiki import get_wiki_page
from re import compile
import wikipedia
import logging


@celery.task
def get_page_with_api(title: str) -> Optional[Dict]:
    page = None
    if title is None:
        return None
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
        logging.basicConfig(level=logging.DEBUG)
        logging.error(
            msg="PageError while getting page from wikipedia.", exc_info=True
        )
        return None
    except wikipedia.HTTPTimeoutError as e:
        logging.basicConfig(level=logging.DEBUG)
        logging.error(
            msg="HTTPTimeoutError while getting page from wikipedia.",
            exc_info=True,
        )
        return None
    except wikipedia.RedirectError as e:
        logging.basicConfig(level=logging.DEBUG)
        logging.error(
            msg="RedirectError while getting page from wikipedia.",
            exc_info=True,
        )
        return None
    except wikipedia.DisambiguationError as e:
        logging.basicConfig(level=logging.DEBUG)
        logging.error(
            msg="DisambiguationError while getting page from wikipedia.",
            exc_info=True,
        )
    except Exception as e:
        logging.basicConfig(level=logging.DEBUG)
        logging.error(
            msg="Unidentified while getting page from wikipedia.",
            exc_info=True,
        )
        return None
    if page:
        return {"title": page.title, "url": page.url, "links": page.links}
    else:
        return None


@celery.task
def get_page(url: str, session: "requests.sessions.Session" = None) -> Dict:
    response = session.get(url) if session else requests.get(url)
    if response.ok:
        return get_wiki_page(response).__dict__
    else:
        return None


@celery.task
def check_if_target_reached(page: Dict, target: Dict, field: str) -> bool:
    return page[field] == target[field]


def download_pages(
    download_func: Callable, source_: str, target: str, field: str, **kwargs
):
    target = download_func(target, **kwargs)
    source_ = download_func(source_, **kwargs)
    input_pages = [source_]
    all_pages = [source_]
    iteration = 0
    while True:
        if (
            any([target[field] in page["links"] for page in input_pages])
            or iteration == 6
        ):
            break
        links = [l for page in input_pages if page for l in page["links"]]
        input_pages = group(download_func.s(link) for link in links)().get()
        # input_pages = [download_func(link) for link in links]
        all_pages.extend(input_pages)
        iteration += 1
    return all_pages
