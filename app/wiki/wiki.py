from typing import List
from dataclasses import dataclass
import json

BASE_URL = "https://en.wikipedia.org"
PATTERN = "^/wiki/(?![a-zA-Z]+:)"

@dataclass
class Page:
    title: str
    url: str
    links: List[str]