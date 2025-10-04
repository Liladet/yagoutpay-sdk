"""
Tests for constants.
"""
from yagoutpay.constants import YagoutPayConstants

def test_constants_values():
    const = YagoutPayConstants()
    assert const.BASE_URL_TEST == "https://uatcheckout.yagoutpay.com/ms-transaction-core-1-0"
    assert const.AGGREGATOR_ID == "yagout"
    assert len(const.IV) == 16  # AES block size