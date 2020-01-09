from app.celery.tasks import flatten_pages
from app.wiki import wiki


def test_list_concat():
    input_ = [
        [wiki.Page("1", "1", ["1", "2"]), wiki.Page("2", "2", ["1", "2"])],
        [wiki.Page("3", "3", ["1", "2"]), wiki.Page("4", "4", ["1", "2"])],
        [wiki.Page("5", "5", ["1", "2"]), wiki.Page("6", "6", ["1", "2"])],
    ]
    expected_output = [
        wiki.Page("1", "1", ["1", "2"]),
        wiki.Page("2", "2", ["1", "2"]),
        wiki.Page("3", "3", ["1", "2"]),
        wiki.Page("4", "4", ["1", "2"]),
        wiki.Page("5", "5", ["1", "2"]),
        wiki.Page("6", "6", ["1", "2"]),
    ]
    res = flatten_pages(input_)
    assert len(res) == 6
    assert res == expected_output


def test_list_concat_corner_cases():
    assert flatten_pages([[]]) == []
