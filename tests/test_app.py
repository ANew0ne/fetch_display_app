import asyncio
import json
from http import HTTPStatus

import pytest
import httpx

from fetch_display_app.app import FetchDisplayData


@pytest.mark.asyncio
async def test_success_data_fetch(httpx_mock, test_url, test_data):
    """
    Test successful data fetching from the API.

    Parameters:
    - httpx_mock: HTTPX mock fixture for mocking HTTP responses.
    - test_url: URL used for testing.
    - test_data: Test data to be returned by the mocked API response.
    """

    httpx_mock.add_response(json=test_data, status_code=HTTPStatus.OK)
    fetch_display_data = FetchDisplayData(test_url)
    await fetch_display_data.fetch_data()
    assert fetch_display_data.data == test_data


@pytest.mark.asyncio
async def test_failed_data_fetch(httpx_mock, test_url):
    """
    Test handling of failed data fetching from the API.

    Parameters:
    - httpx_mock: HTTPX mock fixture for mocking HTTP responses.
    - test_url: URL used for testing.
    """

    httpx_mock.add_response(status_code=HTTPStatus.NOT_FOUND)
    fetch_display_data = FetchDisplayData(test_url)
    await fetch_display_data.fetch_data()
    assert fetch_display_data.data is None


@pytest.mark.asyncio
async def test_request_error_data_fetch(httpx_mock, test_url):
    """
    Test handling of request error during data fetching.

    Parameters:
    - httpx_mock: HTTPX mock fixture for mocking HTTP responses.
    - test_url: URL used for testing.
    """

    httpx_mock.add_exception(httpx.RequestError('Connection error'))
    fetch_display_data = FetchDisplayData(test_url)
    await fetch_display_data.fetch_data()
    assert fetch_display_data.data is None


@pytest.mark.asyncio
async def test_display_data_with_data(capfd, test_url, test_data):
    """
    Test displaying data when data is available.

    Parameters:
    - capfd: pytest capfd fixture for capturing stdout.
    - test_url: URL used for testing.
    - test_data: Test data to be displayed.
    """

    fetch_display_data = FetchDisplayData(test_url)
    fetch_display_data.data = test_data
    await fetch_display_data.display_data()
    captured = capfd.readouterr()
    assert captured.out.strip() == json.dumps(test_data, indent=4)


@pytest.mark.asyncio
async def test_display_data_no_data(capfd, test_url):
    """
    Test displaying no data message when data is not available.

    Parameters:
    - capfd: pytest capfd fixture for capturing stdout.
    - test_url: URL used for testing.
    """

    fetch_display_data = FetchDisplayData(test_url)
    fetch_display_data.data = None
    await fetch_display_data.display_data()
    captured = capfd.readouterr()
    assert captured.out.strip() == 'No data available.'


@pytest.mark.asyncio
async def test_fetch_interval(httpx_mock, test_url, test_data):
    """
    Test data fetching interval.

    Parameters:
    - httpx_mock: HTTPX mock fixture for mocking HTTP responses.
    - test_url: URL used for testing.
    - test_data: Test data to be returned by the mocked API response.
    """

    interval = 5
    httpx_mock.add_response(json=test_data, status_code=HTTPStatus.OK)
    fetch_display_data = FetchDisplayData(test_url)
    fetch_task = asyncio.create_task(fetch_display_data.fetch_loop())
    await asyncio.sleep(interval * 2)
    assert len(httpx_mock.get_requests()) == 2
    fetch_task.cancel()
