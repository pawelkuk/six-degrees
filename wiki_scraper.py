from time import time
import asyncio
from typing import Callable

# from app.wiki.wiki import Page, BASE_URL, PATTERN
from app.celery.tasks import get_page
from concurrent.futures import ProcessPoolExecutor as Pool


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        print(time() - start)
        return result

    return wrapper


async def calc_fibon(n, pool=None):
    loop = asyncio.get_event_loop()
    fib = await loop.run_in_executor(pool, fibon, n)
    print(f"{n} -  {fib}")
    return fib


@timeit
async def async_download_pages(
    download_func: Callable, source_: str, target: str, field: str, **kwargs
):
    loop = asyncio.get_event_loop()
    pool = Pool(20)

    target = await loop.run_in_executor(None, download_func, target, **kwargs)
    source_ = await loop.run_in_executor(
        None, download_func, source_, **kwargs
    )
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
        input_pages = [
            loop.run_in_executor(pool, download_func, link) for link in links
        ]
        input_pages = await asyncio.gather(*input_pages)
        all_pages.extend(input_pages)
        iteration += 1
    return all_pages


if __name__ == "__main__":
    # source_url = "https://en.wikipedia.org/wiki/Adolf_Hitler"
    # target_url = "https://en.wikipedia.org/wiki/Nazi_Party"

    target_url = (
        "https://en.wikipedia.org/wiki/Conditional_probability_distribution"
    )
    target_url_2 = "https://en.wikipedia.org/wiki/Probability_mass_function"
    source_url = "https://en.wikipedia.org/wiki/Channel_capacity"

    # await asyncio.gather(*[calc_fibon(n) for n in range(35, 0, -1)])
    start = time()
    pages = asyncio.run(
        async_download_pages(get_page, source_url, target_url_2, "url")
    )
    print(pages)
    print(time() - start)
