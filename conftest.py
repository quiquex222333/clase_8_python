import pytest
from playwright.sync_api import sync_playwright
from utils.config import BASE_URL, DEFAULT_TIMEOUT

@pytest.fixture(scope="session")
def api():
    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            timeout=DEFAULT_TIMEOUT * 1000,  # ms
            extra_http_headers={
                "Accept": "application/json; charset=utf-8",
                "Content-Type": "application/json; charset=utf-8",
            },
        )
        yield request_context
        request_context.dispose()
