import pytest


@pytest.fixture
def test_url():
    return 'https://test_url'


@pytest.fixture
def test_data():
    return [{'key1': 'value1', 'key2': 'value2'}]
