from datetime import UTC

import httpx
import pytest
import respx

from pingwatch.core.checker import check_url

URL = "https://example.com"


@respx.mock
def test_site_is_up():
    respx.get(URL).mock(return_value=httpx.Response(200))

    result = check_url(URL)

    assert result["status_code"] == 200
    assert result["is_up"] is True
    assert result["error"] is None


@respx.mock
def test_server_error_means_down():
    respx.get(URL).mock(return_value=httpx.Response(500))

    result = check_url(URL)

    assert result["status_code"] == 500
    assert result["is_up"] is False


@respx.mock
def test_connection_error_means_down():
    respx.get(URL).mock(side_effect=httpx.ConnectError("no connection"))

    result = check_url(URL)

    assert result["status_code"] is None
    assert result["response_time_ms"] is None
    assert result["is_up"] is False
    assert result["error"] == "ConnectError"


@pytest.mark.parametrize(
    ("status_code", "expected_is_up"),
    [(399, True), (400, False)],
)
@respx.mock
def test_status_boundary(status_code: int, expected_is_up: bool) -> None:
    respx.get(URL).mock(return_value=httpx.Response(status_code))

    result = check_url(URL)

    assert result["status_code"] == status_code
    assert result["is_up"] is expected_is_up


@pytest.mark.parametrize("exc_class", [httpx.ConnectTimeout, httpx.ReadTimeout])
@respx.mock
def test_timeout_means_down(exc_class: type[httpx.TimeoutException]) -> None:
    respx.get(URL).mock(side_effect=exc_class("timed out"))

    result = check_url(URL)

    assert result["status_code"] is None
    assert result["is_up"] is False
    assert result["error"] == exc_class.__name__


@respx.mock
def test_redirect_is_followed() -> None:
    respx.get(f"{URL}/old").mock(
        return_value=httpx.Response(301, headers={"Location": f"{URL}/new"})
    )
    final = respx.get(f"{URL}/new").mock(return_value=httpx.Response(200))

    result = check_url(f"{URL}/old")

    assert final.called
    assert result["status_code"] == 200
    assert result["is_up"] is True


@respx.mock
def test_checked_at_is_utc() -> None:
    respx.get(URL).mock(return_value=httpx.Response(200))

    result = check_url(URL)

    assert result["checked_at"].tzinfo is UTC
