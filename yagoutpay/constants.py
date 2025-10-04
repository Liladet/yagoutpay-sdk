"""
YagoutPay constants (URLs, IDs, defaults).
"""
class YagoutPayConstants:
    BASE_URL_TEST = "https://uatcheckout.yagoutpay.com/ms-transaction-core-1-0"
    BASE_URL_PROD = "https://prodcheckout.yagoutpay.com/ms-transaction-core-1-0"  # Update with real prod if known
    STATIC_ENDPOINT = "/sdk/staticQRPaymentResponse"  # From static_link_sdk.py
    DYNAMIC_ENDPOINT = "/sdk/paymentByLinkResponse"  # Assumed from dynamic; adjust if needed
    HOSTED_ENDPOINT = "/paymentRedirection/checksumGatewayPage"  # From hosted
    DIRECT_ENDPOINT = "/apiRedirection/apiIntegration"  # From direct
    AGGREGATOR_ID = "yagout"
    DEFAULT_PG_ID = "67ee846571e740418d688c3f"  # From direct
    DEFAULT_SCHEME_ID = "7"
    DEFAULT_WALLET_TYPE = "telebirr"
    IV = b"0123456789abcdef"  # Fixed IV from all scripts