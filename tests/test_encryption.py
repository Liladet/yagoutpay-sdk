"""
Unit tests for EncryptionUtils.
"""
import pytest
from yagoutpay.encryption import EncryptionUtils

@pytest.fixture
def utils():
    return EncryptionUtils()

@pytest.fixture
def valid_key():
    return "IG3CNW5uNrUO2mU2htUOWb9rgXCF7XMAXmL63d7wNZo="  # Your real 32-byte key

def test_encrypt_decrypt_roundtrip(utils, valid_key):
    """Encrypt then decrypt should match original."""
    text = '{"test": "data"}'
    encrypted = utils.encrypt(text, valid_key)
    decrypted = utils.decrypt(encrypted, valid_key)
    assert decrypted == text

def test_invalid_key_length(utils):
    """Raises on key !=32 bytes."""
    # Valid Base64 but decodes to 16 bytes (not 32)
    short_key = "PiOuBN2nvKts01JYREXPxQ=="
    with pytest.raises(ValueError, match="Invalid key length"):
        utils.encrypt("test", short_key)

def test_encrypt_non_utf8(utils, valid_key):
    """Handles binary-ish data gracefully."""
    text = "Hello ©"  # Non-ASCII
    encrypted = utils.encrypt(text, valid_key)
    decrypted = utils.decrypt(encrypted, valid_key)
    assert decrypted == text

def test_invalid_base64_key(utils):
    """Raises on invalid Base64 (decode fails)."""
    invalid_key = "short"  # Not valid Base64
    with pytest.raises(ValueError, match="Encryption error"):
        utils.encrypt("test", invalid_key)