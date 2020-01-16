from app.celery.tasks import download_pages, get_page, get_page_with_api
from time import time
import pickle


# source_url = "https://en.wikipedia.org/wiki/Adolf_Hitler"
# target_url = "https://en.wikipedia.org/wiki/Nazi_Party"


target_url = (
    "https://en.wikipedia.org/wiki/Conditional_probability_distribution"
)
target_url_2 = "https://en.wikipedia.org/wiki/Probability_mass_function"
source_url = "https://en.wikipedia.org/wiki/Channel_capacity"

target_2_steps = "probability mass function"
target_1_step = "conditional probability distribution"
source = "channel capacity"


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        print(time() - start)
        return result

    return wrapper


@timeit
def test_download_pages_with_api(source, target):
    pages = download_pages(get_page_with_api, source, target, "title")
    assert type(pages) == list


@timeit
def test_download_pages(source, target):
    pages = download_pages(get_page, source, target, "url")
    assert type(pages) == list


test_download_pages_with_api(source, target_1_step)
test_download_pages(source_url, target_url_2)
