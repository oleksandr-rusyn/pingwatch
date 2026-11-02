import httpx
import respx
from pingwatch import check_url

URL = "https://example.com"


@respx.mock
def test_site_is_up():
    respx.get(URL).mock(return_value=httpx.Response(200))

    result = check_url(URL)

    assert result["status_code"] == 200
    assert result["is_up"] is True


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
