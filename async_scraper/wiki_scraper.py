import asyncio
from app.wiki.wiki import Page, BASE_URL, PATTERN


async with aiohttp.ClientSession() as session:
    # start
    for i in range(1, 50):
        task = asyncio.ensure_future(get_char(i, session))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    for r in results:
        print(r)
