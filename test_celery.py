from app.celery.tasks import download_pages, get_page, get_page_with_api
from app.graphs import graph, network
from time import time
import pickle


target_url = (
    "https://en.wikipedia.org/wiki/Conditional_probability_distribution"
)
target_url_2 = "https://en.wikipedia.org/wiki/Probability_mass_function"
source_url = "https://en.wikipedia.org/wiki/Channel_capacity"

source_url = "https://en.wikipedia.org/wiki/August_Kubizek"
target_url_2 = "https://en.wikipedia.org/wiki/Livonian_Order"

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
    print(len(pages))


@timeit
def test_download_pages_network(source, target):
    pages = download_pages(get_page, source, target, "url")
    print("Download complete")
    net = network.PageNetwork()
    net.addNodes(pages, "url")
    net.addEdges(pages, source="url", target="links")
    print("Network initialized")
    net.plotNetwork(source, target)


# test_download_pages_with_api(source, target_1_step)
test_download_pages(source_url, target_url_2)
# test_download_pages_network(source_url, target_url_2)
