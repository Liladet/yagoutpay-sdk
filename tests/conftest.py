"""
Pytest fixtures for shared setup.
"""
import pytest
import requests_mock
from yagoutpay import YagoutPaySDK

@pytest.fixture
def mock_sdk():
    """Returns a mocked SDK instance."""
    # Valid 32-byte Base64 key (generated via secrets.token_bytes(32))
    valid_key = "q782YSUUxak8Aofb599N70VRGwvkGcOXn4fmIIQWM4I="
    return YagoutPaySDK("test_merchant", valid_key, "test")

@pytest.fixture
def mock_request():
    """Requests mocker adapter."""
    with requests_mock.Mocker() as m:
        yield m