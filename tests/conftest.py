import pytest
import requests


@pytest.fixture(scope="session")
def session():
    return requests.session()
