from yagoutpay import YagoutPaySDK
from datetime import datetime, timedelta

sdk = YagoutPaySDK("202508080001", "IG3CNW5uNrUO2mU2htUOWb9rgXCF7XMAXmL63d7wNZo=", "test")
# Expiry within 30 days
expiry = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
payload = {
    "req_user_id": "yagou381",
    "me_id": "202508080001",
    "amount": "500",
    "customer_email": "test@example.com",
    "mobile_no": "0909260339",
    "expiry_date": expiry,
    "media_type": ["API"],
    "order_id": "DYN_20250923_200",  # Unique
    "first_name": "YagoutPay",
    "last_name": "DynamicLink",
    "product": "Premium Subscription",
    "dial_code": "+251",
    "failure_url": "http://localhost:3000/failure",
    "success_url": "http://localhost:3000/success",
    "country": "ETH",
    "currency": "ETB"
}
result = sdk.create_dynamic_link(payload)
print("Dynamic Result:", result)
# Expected: {"status": "success", "link": "https://.../dynamic/..."}
# Test: Paste link in browser—shows payment form? Expires after date?