from typing import NamedTuple, List
from re import compile
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://en.wikipedia.org"
PATTERN = "^/wiki/(?![a-zA-Z]+:)"

Page = NamedTuple("Page", [("title", str), ("url", str), ("links", List[str])])


def get_wiki_page(response: "requests.response") -> "Page":
    soup = BeautifulSoup(response.text, "html.parser")
    urls = soup.find(id="content").findAll(
        "a", attrs={"href": compile(PATTERN)}
    )
    valid_urls: Iterator[str] = map(
        lambda x: urljoin(BASE_URL, x.get("href")), urls
    )
    title = soup.find(id="firstHeading").get_text()
    return Page(title, response.url, list(valid_urls))
