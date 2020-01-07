from app.celery.tasks import (
    get_wikilinks,
    get_article_name,
    check_if_target_reached,
)
from betamax import Betamax

with Betamax.configure() as config:
    config.cassette_library_dir = "tests/fixtures/cassettes"


def test_wikilinks_returns_list_of_urls(session):
    url = "https://en.wikipedia.org/wiki/Adolf_Hitler"
    with Betamax(session) as vcr:
        vcr.use_cassette("adolf")
        res = get_wikilinks(url=url, session=session)
        assert type(res) == list
        assert len(res) == 2654


def test_wikilinks_returns_empty_list(session):
    url = "https://en.wikipedia.org/wiki/Adolf_Hitler_2"
    with Betamax(session) as vcr:
        vcr.use_cassette("invalid_adolf")
        res = get_wikilinks(url=url, session=session)
        assert res == []


def test_get_article_name_returns_proper_name(session):
    url_1 = "https://en.wikipedia.org/wiki/Adolf_Hitler"
    url_2 = "https://en.wikipedia.org/wiki/Albert_Einstein"
    with Betamax(session) as vcr:
        vcr.use_cassette("adolf")
        res_1 = get_article_name(url=url_1, session=session)
        vcr.use_cassette("einstein")
        res_2 = get_article_name(url=url_2, session=session)
        assert type(res_1) == str
        assert type(res_2) == str
        assert res_1 == "Adolf Hitler"
        assert res_2 == "Albert Einstein"


def test_get_article_name_returns_none(session):
    url = "https://en.wikipedia.org/wiki/Adolf_Hitler_2"
    with Betamax(session) as vcr:
        vcr.use_cassette("invalid_adolf")
        res = get_article_name(url=url, session=session)
        assert res is None


def test_check_resturns_proper_value(session):
    url = "https://en.wikipedia.org/wiki/Adolf_Hitler"
    with Betamax(session) as vcr:
        vcr.use_cassette("adolf")
        res = check_if_target_reached(url, "Adolf Hitler", session=session)
        assert res is True
