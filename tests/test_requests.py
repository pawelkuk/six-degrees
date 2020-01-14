from app.celery.tasks import (
    check_if_target_reached,
    get_page_with_api,
    get_page,
    download_pages
)
from betamax import Betamax

with Betamax.configure() as config:
    config.cassette_library_dir = "tests/fixtures/cassettes"


def test_page_returns_none(session):
    url = "https://en.wikipedia.org/wiki/Adolf_Hitler_2"
    with Betamax(session) as vcr:
        vcr.use_cassette("invalid_adolf")
        res = get_page(url=url, session=session)
        assert res is None


def test_check_resturns_proper_value(session):
    url = "https://en.wikipedia.org/wiki/Adolf_Hitler"
    with Betamax(session) as vcr:
        vcr.use_cassette("adolf")
        page = get_page(url=url, session=session)
        target = get_page(url=url)
        res = check_if_target_reached(page, target, "title")
        assert res is True
        res = check_if_target_reached(page, target, "url")
        assert res is True


def test_get_page_returns_proper_values(session):
    url_1 = "https://en.wikipedia.org/wiki/Adolf_Hitler"
    url_2 = "https://en.wikipedia.org/wiki/Albert_Einstein"
    with Betamax(session) as vcr:
        vcr.use_cassette("adolf")
        res_1 = get_page(url=url_1, session=session)
        vcr.use_cassette("einstein")
        res_2 = get_page(url=url_2, session=session)
        assert type(res_1["title"]) == str
        assert type(res_2["title"]) == str
        assert res_1["url"] == url_1
        assert res_2["url"] == url_2
        assert type(res_1["links"]) == list
        assert type(res_2["links"]) == list
        assert res_1["title"] == "Adolf Hitler"
        assert res_2["title"] == "Albert Einstein"


def test_get_page_api(session):
    title = "hitler"
    page = get_page_with_api(title)
    assert page["title"] == 'Adolf Hitler'
    assert page["url"] == "https://en.wikipedia.org/wiki/Adolf_Hitler"
    assert isinstance(page["links"], list)


# def test_download_pages_with_api(session):
#     source = "hitler"
#     target = "nazi party"
#     pages = download_pages(get_page_with_api, source=source, target=target, field="title")
#     assert isinstance(pages, list)
#     print(pages)


# def test_download_pages(session):
#     source = "https://en.wikipedia.org/wiki/Adolf_Hitler"
#     target = "https://en.wikipedia.org/wiki/Nazi_Party"
#     pages = download_pages(get_page, source=source, target=target, field="title", session=session)
#     assert isinstance(pages, list)
#     print(pages)
