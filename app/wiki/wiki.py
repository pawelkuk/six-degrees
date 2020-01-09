from typing import NamedTuple, List

BASE_URL = "https://en.wikipedia.org"
PATTERN = "^/wiki/(?![a-zA-Z]+:)"

Page = NamedTuple("Page", [("title", str), ("url", str), ("links", List[str])])
