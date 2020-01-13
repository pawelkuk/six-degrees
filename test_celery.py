from app.celery.tasks import download_pages, get_page, get_page_with_api
from time import time
import pickle

# target_url = 'https://en.wikipedia.org/wiki/Deflection_(engineering)'
# target_url = "https://en.wikipedia.org/wiki/Castigliano%27s_method"
# source_url = "https://en.wikipedia.org/wiki/Span_(engineering)"

source_url = "https://en.wikipedia.org/wiki/Adolf_Hitler"
target_url = "https://en.wikipedia.org/wiki/Nazi_Party"

source = "Hitler"
target = "nazi party"


def test_download_pages_with_api():
    start = time()
    pages = download_pages(get_page_with_api, source, target, "title")
    end = time()
    assert type(pages) == list
    print(end - start)
    pickle.dump(pages, "test_pages")

def test_download_pages(source, target):
    start = time()
    pages = download_pages(get_page, source, target, "title")
    end = time()
    print(pages)
    assert type(pages) == list
    print(end - start)
    pickle.dump(pages, "test_pages")


test_download_pages(source_url, target_url)