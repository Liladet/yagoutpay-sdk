import json
import requests
import re
from datetime import datetime, timedelta
from typing import Dict, Any
from urllib3.exceptions import InsecureRequestWarning
import warnings
import qrcode
import random
import string
import time
import hashlib
import base64
from Crypto.Cipher import AES  # For hosted AES variant
from Crypto.Util.Padding import pad

from .encryption import EncryptionUtils
from .constants import YagoutPayConstants

warnings.simplefilter('ignore', InsecureRequestWarning)

class YagoutPaySDK:
    def __init__(self, merchant_id: str, encryption_key: str, environment: str = "test"):
        """Initialize SDK with credentials and env (test/prod)."""
        if not merchant_id or not encryption_key:
            raise ValueError("Merchant ID and encryption key are required.")
        try:
            key_bytes = base64.b64decode(encryption_key)
            if len(key_bytes) != 32:
                raise ValueError(f"Encryption key must decode to 32 bytes, got {len(key_bytes)}")
        except Exception as e:
            raise ValueError(f"Invalid encryption key: {e}")
        self.merchant_id = merchant_id
        self.encryption_key = encryption_key
        self.utils = EncryptionUtils()
        self.constants = YagoutPayConstants()
        self.base_url = self.constants.BASE_URL_TEST if environment == "test" else self.constants.BASE_URL_PROD
        self.session = requests.Session()
        self.session.verify = False  # UAT; set True for prod

    def encrypt(self, text: str) -> str:
        return self.utils.encrypt(text, self.encryption_key)

    def decrypt(self, encrypted: str) -> str:
        return self.utils.decrypt(encrypted, self.encryption_key)

    # Static Link (from static_link_sdk.py)
    def create_static_link(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
    Generate a static QR payment link.

    Args:
        payload (Dict[str, Any]): Payment details.
            Required: req_user_id, me_code, qr_transaction_amount, brandName, storeName.
            Optional: status="ACTIVE", store_id, etc. (see YagoutPay docs).

    Returns:
        Dict[str, Any]: {"status": "success/error", "link": str, "qr_id": str, "qr_file": str}
            On error: {"status": "error", "message": str}

    Raises:
        ValueError: If encryption fails.

    Example:
        >>> payload = {"req_user_id": "user123", ...}
        >>> result = sdk.create_static_link(payload)
        >>> if result["status"] == "success": print(result["link"])
    """
        required = {"req_user_id", "me_code", "qr_transaction_amount", "brandName", "storeName"}
        if not all(k in payload for k in required):
            return {"status": "error", "message": f"Missing required fields: {required - set(payload)}"}
        try:
            payload_json = json.dumps(payload)
            encrypted_payload = self.encrypt(payload_json)
            request_body = {"request": encrypted_payload}
            response = self.session.post(
                f"{self.base_url}{self.constants.STATIC_ENDPOINT}",
                json=request_body,
                headers={"Content-Type": "application/json", "me_id": self.merchant_id},
                timeout=30
            )
            response.raise_for_status()
            resp_data = response.json()
            encrypted_resp = resp_data.get("responseData")
            if not encrypted_resp:
                return {"status": "error", "message": "No responseData in API response"}
            decrypted_resp = json.loads(self.decrypt(encrypted_resp))
            resp_data_dec = decrypted_resp.get("responseData", {})
            payment_link = resp_data_dec.get("staticLink")
            qr_id = resp_data_dec.get("qrId")
            if payment_link:
                qr_filename = f"payment_qr_{qr_id or 'unknown'}.png"
                self._generate_qr(payment_link, qr_filename)
                return {"status": "success", "link": payment_link, "qr_id": qr_id, "qr_file": qr_filename}
            return {"status": "error", "message": "No staticLink in response"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _generate_qr(self, data: str, filename: str):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)

    # Dynamic Link (from dynamic_link_sdk.py)
    def create_dynamic_link(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """ Generate a dynamic QR payment link."""
        required = {"req_user_id", "me_id", "amount", "mobile_no", "expiry_date", "media_type", "order_id",
                    "first_name", "last_name", "product", "dial_code", "failure_url", "success_url", "country", "currency", "customer_email"}
        if not all(k in payload for k in required):
            return {"status": "error", "message": f"Missing required fields: {required - set(payload)}"}
        try:
            expiry = datetime.strptime(payload["expiry_date"], "%Y-%m-%d")
            if expiry > datetime.now() + timedelta(days=30):
                return {"status": "error", "message": "Expiry date must be within 30 days"}
            json_str = json.dumps(payload)
            encrypted_request = self.encrypt(json_str)
            response = self.session.post(
                f"{self.base_url}{self.constants.DYNAMIC_ENDPOINT}",
                headers={"me_id": self.merchant_id, "Content-Type": "application/json"},
                json={"request": encrypted_request},
                timeout=30
            )
            response.raise_for_status()
            print(f"Dynamic Debug - Status: {response.status_code}")
            print(f"Dynamic Debug - Headers: {dict(response.headers)}")
            print(f"Dynamic Debug - Raw Text: {response.text[:500]}...")  # First 500 chars
            response.raise_for_status()
            decrypted_response = self.decrypt(response.text)
            link_match = re.search(r'"PaymentLink":"([^"]+)"', decrypted_response)
            if link_match:
                return {"status": "success", "link": link_match.group(1)}
            return {"status": "error", "message": "No PaymentLink found in response"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # Hosted Checkout (from hosted_checkoutpay.py)
    def generate_hosted_checkout(self, amount: str = "1", name: str = "Test User", email: str = "test@email.com",
                                 phone: str = "0909260339", success_url: str = "https://yourdomain.com/success",
                                 failure_url: str = "https://yourdomain.com/failure") -> str:
        """Generate HTML form for hosted checkout."""
        order_no = ''.join(random.choices(string.digits, k=5))
        txn_details = "|".join([self.constants.AGGREGATOR_ID, self.merchant_id, order_no, amount, "ETH", "ETB", "SALE", success_url, failure_url, "WEB"])
        pg_details = "|||"
        card_details = "|||||"
        cust_details = "|".join([name, email, phone, "", "Y"])
        bill_details = "|||||"
        ship_details = "|||||||"
        item_details = "||"
        upi_details = ""
        other_details = "|||||"
        full_message = "~".join([txn_details, pg_details, card_details, cust_details, bill_details, ship_details, item_details, upi_details, other_details])
        
        enc_message = self._encrypt_aes(full_message)
        hash_input = f"{self.merchant_id}~{order_no}~{amount}~ETH~ETB"
        sha256_hex = hashlib.sha256(hash_input.encode()).hexdigest()
        enc_hash = self._encrypt_aes(sha256_hex)
        
        url = f"{self.base_url}{self.constants.HOSTED_ENDPOINT}"
        html = f"""
        <!DOCTYPE html>
        <html><body onload="document.forms[0].submit()">
          <form method="POST" action="{url}">
            <input type="hidden" name="me_id" value="{self.merchant_id}" />
            <input type="hidden" name="merchant_request" value="{enc_message}" />
            <input type="hidden" name="hash" value="{enc_hash}" />
            <noscript><input type="submit" value="Pay Now" /></noscript>
          </form>
        </body></html>
        """
        return html

    def _encrypt_aes(self, plaintext: str) -> str:
        key = base64.b64decode(self.encryption_key)
        iv = self.constants.IV
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded = pad(plaintext.encode("utf-8"), AES.block_size)
        return base64.b64encode(cipher.encrypt(padded)).decode("utf-8")

    # Direct API (from Direct Api.py)
    def initiate_direct_payment(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate direct payment (wallet/card)."""
        txn = payload.get("txn_details", {})
        required = {"amount", "sucessUrl", "failureUrl", "customerName", "emailId", "mobileNumber"}  # From cust/txn
        if not all(k in txn or k in payload.get("cust_details", {}) for k in required):
            return {"status": "error", "message": "Missing required fields in txn_details or cust_details"}
        payload["txn_details"] = txn
        payload["txn_details"]["agId"] = self.constants.AGGREGATOR_ID
        payload["txn_details"]["meId"] = self.merchant_id
        payload["txn_details"]["orderNo"] = txn.get("orderNo", self._generate_order_no())
        payload["txn_details"]["channel"] = "API"
        payload["txn_details"]["country"] = txn.get("country", "ETH")
        payload["txn_details"]["currency"] = txn.get("currency", "ETB")
        payload["txn_details"]["transactionType"] = txn.get("transactionType", "SALE")
        if "pg_details" not in payload:
            payload["pg_details"] = {"pg_Id": self.constants.DEFAULT_PG_ID, "paymode": "WA", "scheme_Id": self.constants.DEFAULT_SCHEME_ID, "wallet_type": self.constants.DEFAULT_WALLET_TYPE}
        cust = payload.get("cust_details", {})
        cust["isLoggedIn"] = "Y"
        payload["cust_details"] = cust
        
        try:
            json_str = json.dumps(payload, separators=(',', ':'))
            encrypted_request = self.encrypt(json_str)
            request_body = {"merchantId": self.merchant_id, "merchantRequest": encrypted_request}
            response = self.session.post(
                f"{self.base_url}{self.constants.DIRECT_ENDPOINT}",
                json=request_body,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            resp_json = response.json()
            if resp_json.get('status') == "Success":
                decrypted = self.decrypt(resp_json['response'])
                return {"status": "success", "decrypted_response": decrypted}
            return {"status": "error", "message": resp_json.get('statusMessage', 'Unknown error')}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _generate_order_no(self) -> str:
        timestamp = int(time.time() * 1000)
        random_part = random.randint(100, 999)
        return f"{timestamp}{random_part}"[-12:]