from app.celery.tasks import concatenate_lists_of_urls


def test_list_concat():
    input_ = [
        ["url1", "url2", "url3"],
        ["url1", "url2", "url3"],
        ["url1", "url2", "url3"],
    ]
    expected_output = [
        "url1",
        "url2",
        "url3",
        "url1",
        "url2",
        "url3",
        "url1",
        "url2",
        "url3",
    ]
    res = concatenate_lists_of_urls(input_)
    assert len(res) == 9
    assert res == expected_output


def test_list_concat_corner_cases():
    assert concatenate_lists_of_urls([[]]) == []
