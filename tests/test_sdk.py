"""
Integration tests for YagoutPaySDK methods.
"""
import pytest
import json
from datetime import datetime, timedelta
from yagoutpay import YagoutPaySDK

# Use fixtures from conftest.py

def test_init_valid(mock_sdk):
    """SDK inits without error on valid creds."""
    assert mock_sdk.merchant_id == "test_merchant"

def test_init_invalid_key():
    """Raises on bad key length (valid Base64, wrong bytes)."""
    short_key = "PiOuBN2nvKts01JYREXPxQ=="  # 16 bytes
    with pytest.raises(ValueError, match="Encryption key must decode to 32 bytes"):
        YagoutPaySDK("id", short_key)

def test_create_static_link_validation(mock_sdk):
    """Fails on missing required fields."""
    incomplete_payload = {"req_user_id": "user"}  # Missing others
    result = mock_sdk.create_static_link(incomplete_payload)
    assert result["status"] == "error"
    assert "Missing required fields" in result["message"]

def test_create_static_link_success(mock_request, mock_sdk):
    """Mocks API success for static link."""
    # Mock response (encrypt a fake responseData)
    mock_url = f"{mock_sdk.base_url}{mock_sdk.constants.STATIC_ENDPOINT}"
    fake_decrypted = '{"responseData": {"staticLink": "https://pay.example/static/123", "qrId": "qr_456"}}'
    mock_response = {"responseData": mock_sdk.encrypt(fake_decrypted)}
    mock_request.post(mock_url, json=mock_response, status_code=200)

    payload = {
        "req_user_id": "yagou381",
        "me_code": "202508080001",
        "qr_transaction_amount": "1",
        "brandName": "Lidiya",
        "storeName": "YP"
    }
    result = mock_sdk.create_static_link(payload)
    assert result["status"] == "success"
    assert "https://pay.example/static/123" in result["link"]
    assert result["qr_id"] == "qr_456"

def test_create_dynamic_link_expiry(mock_sdk):
    """Fails if expiry >30 days."""
    # Full required payload
    payload = {
        "req_user_id": "yagou381",
        "me_id": "202508080001",
        "amount": "500",
        "mobile_no": "0909260339",
        "expiry_date": "2026-01-01",  # Far future (>30 days)
        "media_type": ["API"],
        "order_id": "DYN_20250923_110",
        "first_name": "YagoutPay",
        "last_name": "DynamicLink",
        "product": "Premium Subscription",
        "dial_code": "+251",
        "failure_url": "http://localhost:3000/failure",
        "success_url": "http://localhost:3000/success",
        "country": "ETH",
        "currency": "ETB",
        "customer_email": "test@example.com"
    }
    result = mock_sdk.create_dynamic_link(payload)
    assert result["status"] == "error"
    assert "Expiry date must be within 30 days" in result["message"]

def test_generate_hosted_checkout(mock_sdk):
    """Returns valid HTML string."""
    html = mock_sdk.generate_hosted_checkout(amount="10", name="Test", email="test@test.com")
    assert "<form method=\"POST\"" in html
    assert mock_sdk.merchant_id in html  # me_id hidden input
    assert "Pay Now" in html

def test_initiate_direct_payment_defaults(mock_request, mock_sdk):
    """Fills defaults and mocks success."""
    mock_url = f"{mock_sdk.base_url}{mock_sdk.constants.DIRECT_ENDPOINT}"
    fake_decrypted = '{"success": true}'
    mock_response = {"status": "Success", "response": mock_sdk.encrypt(fake_decrypted)}
    mock_request.post(mock_url, json=mock_response, status_code=200)

    payload = {
        "txn_details": {
            "amount": "1",
            "sucessUrl": "https://success.com",
            "failureUrl": "https://fail.com"
        },
        "cust_details": {
            "customerName": "User",
            "emailId": "user@test.com",
            "mobileNumber": "123"
        }
    }
    result = mock_sdk.initiate_direct_payment(payload)
    assert result["status"] == "success"
    assert '"success": true' in result["decrypted_response"]