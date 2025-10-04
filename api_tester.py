import streamlit as st
import json
import requests
from datetime import datetime, timedelta
import random
import string
import base64
import time  # Added missing import
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Import your SDK
try:
    from yagoutpay import YagoutPaySDK
except ImportError:
    st.error("❌ yagoutpay SDK not installed. Run: pip install yagoutpay-sdk")
    st.stop()

# Config
MERCHANT_ID = "202508080001"
ENCRYPTION_KEY = "IG3CNW5uNrUO2mU2htUOWb9rgXCF7XMAXmL63d7wNZo="
NGROK_URL = "https://your-ngrok.ngrok-free.app"  # Update to your ngrok
API_URL = "https://uatcheckout.yagoutpay.com/ms-transaction-core-1-0/apiRedirection/apiIntegration"
AGGREGATOR_ID = "yagout"

st.set_page_config(page_title="🪄 YagoutPay SDK Tester", layout="wide")
st.title("🪄 YagoutPay SDK Tester – Enchant Payments in Seconds!")
st.markdown("**Input your spell (params) → Witness the magic (API calls) → Harvest the link/charge.** *Powered by your unified YagoutPaySDK—feel the unification!*")

# Sidebar
with st.sidebar:
    st.header("Your Wand")
    st.code("pip install yagoutpay-sdk")
    st.code("from yagoutpay import YagoutPaySDK\nsdk = YagoutPaySDK(merchant_id='...', encryption_key='...', environment='test')")
    st.markdown("[GitHub Repo](https://github.com/liladet/yagoutpay-sdk) | [Videos](your-loom-link)")

# Initialize SDK
try:
    sdk = YagoutPaySDK(MERCHANT_ID, ENCRYPTION_KEY, environment="test")
except Exception as e:
    st.error(f"❌ SDK Initialization Failed: {e}")
    st.stop()

# Original Direct Encrypt/Decrypt (bypass SDK for testing)
def direct_encrypt(text, key_b64):
    try:
        key = base64.b64decode(key_b64)
        iv = b"0123456789abcdef"
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = PKCS7(128).padder()
        padded_data = padder.update(text.encode()) + padder.finalize()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(ct).decode()
    except Exception as e:
        st.error(f"Direct Encrypt Failed: {e}")
        return None

def direct_decrypt(crypt_b64, key_b64):
    try:
        key = base64.b64decode(key_b64)
        iv = b"0123456789abcdef"
        crypt = base64.b64decode(crypt_b64)
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        padtext = decryptor.update(crypt) + decryptor.finalize()
        unpadder = PKCS7(128).unpadder()
        data = unpadder.update(padtext) + unpadder.finalize()
        return data.decode()
    except Exception as e:
        st.error(f"Direct Decrypt Failed: {e}")
        return None

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔗 Dynamic Link", "📱 Static Link + QR", "🌐 Hosted Checkout", "⚡ Direct API"])

with tab1:
    st.header("🔗 Dynamic Link – Morphing Magic for Carts")
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Amount (ETB)", min_value=1.0, value=500.0, key="amount_dynamic")
        email = st.text_input("Customer Email", value="test@example.com", key="email_dynamic")
        mobile = st.text_input("Mobile No", value="0909260339", key="mobile_dynamic")
    with col2:
        product = st.text_input("Product", value="Premium Subscription", key="product_dynamic")
        order_id = st.text_input("Order ID", value=f"DYN_{datetime.now().strftime('%Y%m%d_%H%M%S')}", key="order_id_dynamic")
    
    if st.button("✨ Conjure Dynamic Link", type="primary", key="btn_dynamic"):
        payload = {
            "req_user_id": "yagou381",
            "me_id": MERCHANT_ID,
            "amount": str(int(amount)),
            "customer_email": email,
            "mobile_no": mobile,
            "expiry_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "media_type": ["API"],
            "order_id": order_id,
            "first_name": "Test",
            "last_name": "User",
            "product": product,
            "dial_code": "+251",
            "failure_url": f"{NGROK_URL}/failure",
            "success_url": f"{NGROK_URL}/success",
            "country": "ETH",
            "currency": "ETB"
        }
        plain_json = json.dumps(payload, indent=2)
        st.subheader("🔮 Before Magic: Plain Payload")
        st.text_area("Plain Payload", plain_json, height=200, key="plain_dynamic")
        
        with st.spinner("Encrypting & Calling API..."):
            try:
                result = sdk.create_dynamic_link(payload)
                if result.get("status") == "success":
                    link = result["link"]
                    encrypted = sdk.encrypt(plain_json)
                    st.subheader("🧙‍♂️ The Veil: Encrypted Payload")
                    st.text_area("Encrypted Payload", encrypted, height=100, key="encrypted_dynamic")
                    st.success(f"🎉 **Magic Complete!** Dynamic Link: {link}")
                    st.code(link)
                    st.balloons()
                else:
                    st.error(f"⚠️ Spell Fizzled: {result.get('message', 'Unknown error')}")
                    with st.expander("Debug Raw Response"):
                        st.write(result)
            except Exception as e:
                st.error(f"Dynamic Link Error: {str(e)}")
                with st.expander("Debug Details"):
                    st.write(f"Exception type: {type(e).__name__}")

with tab2:
    st.header("📱 Static Link + QR – Evergreen Enchantment")
    amount = st.number_input("Amount (ETB)", min_value=1.0, value=1.0, key="amount_static")
    
    if st.button("✨ Generate Static Link & QR", type="primary", key="btn_static"):
        payload = {
            "ag_id": "",
            "ag_code": "",
            "ag_name": "",
            "req_user_id": "yagou381",
            "me_code": MERCHANT_ID,
            "me_name": "",
            "qr_code_id": "",
            "brandName": "Lidiya",
            "qr_name": "",
            "status": "ACTIVE",
            "storeName": "YP",
            "store_id": "",
            "token": "",
            "qr_transaction_amount": str(int(amount)),
            "logo": "",
            "store_email": "",
            "mobile_no": "",
            "udf": "",
            "udfmerchant": "",
            "file_name": "",
            "from_date": "",
            "to_date": "",
            "file_extn": "",
            "file_url": "",
            "file": "",
            "original_file_name": "",
            "successURL": f"{NGROK_URL}/success",
            "failureURL": f"{NGROK_URL}/failure",
            "addAll": "",
            "source": ""
        }
        plain_json = json.dumps(payload, indent=2)
        st.subheader("🔮 Before: Plain Payload")
        st.text_area("Plain Payload", plain_json, height=200, key="plain_static")
        
        with st.spinner("Weaving Encryption..."):
            try:
                result = sdk.create_static_link(payload)
                if result.get("status") == "success":
                    link = result["link"]
                    qr_id = result["qr_id"]
                    qr_file = result["qr_file"]
                    encrypted = sdk.encrypt(plain_json)
                    st.subheader("🧙‍♂️ Encrypted Veil")
                    st.text_area("Encrypted Payload", encrypted, height=100, key="encrypted_static")
                    st.success(f"🎉 **Static Link: {link}** | QR ID: {qr_id}")
                    st.code(link)
                    
                    # Handle QR code display
                    try:
                        if qr_file and isinstance(qr_file, str):
                            if qr_file.startswith(('http://', 'https://')):
                                st.image(qr_file, caption="🖼️ Scan This QR!")
                            else:
                                st.image(qr_file, caption="🖼️ Scan This QR!")
                                with open(qr_file, "rb") as f:
                                    st.download_button("💾 Download QR", data=f.read(), file_name=f"qr_{qr_id}.png")
                        else:
                            st.warning("QR file path not available or invalid")
                    except Exception as qr_error:
                        st.warning(f"Could not display QR: {qr_error}")
                    
                    st.balloons()
                else:
                    st.error(f"API Hiccup: {result.get('message', 'Unknown error')}")
                    with st.expander("Debug Raw Response"):
                        st.write(result)
            except Exception as e:
                st.error(f"Static Link Error: {str(e)}")
                with st.expander("Debug Details"):
                    st.write(f"Exception type: {type(e).__name__}")

with tab3:
    st.header("🌐 Hosted Checkout – Seamless Redirect Ritual")
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Amount (ETB)", min_value=1.0, value=1.0, key="amount_hosted")
        name = st.text_input("Customer Name", value="Test User", key="name_hosted")
        email = st.text_input("Email", value="test@example.com", key="email_hosted")
    with col2:
        phone = st.text_input("Phone", value="0909260339", key="phone_hosted")
        success_url = st.text_input("Success URL", value=f"{NGROK_URL}/success", key="success_hosted")
        failure_url = st.text_input("Failure URL", value=f"{NGROK_URL}/failure", key="failure_hosted")
    
    if st.button("✨ Summon Hosted Form", type="primary", key="btn_hosted"):
        try:
            with st.spinner("Crafting Encrypted Form..."):
                html = sdk.generate_hosted_checkout(
                    amount=str(int(amount)),
                    name=name,
                    email=email,
                    phone=phone,
                    success_url=success_url,
                    failure_url=failure_url
                )
                st.subheader("🔮 The Enchanted Form (Auto-Submits!)")
                st.components.v1.html(html, height=300, scrolling=True)
                st.info("💡 **Real Flow**: Redirects to YagoutPay → Card/Wallet → Back to success URL. Embed in your app!")
                
                # Also show the HTML code for debugging
                with st.expander("View HTML Code"):
                    st.code(html, language="html")
                    
        except Exception as e:
            st.error(f"Hosted Checkout Error: {str(e)}")
            with st.expander("Debug"):
                st.write("Check: pycryptodome installed? (`pip install pycryptodome`) IV in constants? Key decodes to 32 bytes?")
                st.write(f"Error details: {type(e).__name__}: {str(e)}")

with tab4:
    st.header("⚡ Direct API – Silent Charge Sorcery")
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Charge Amount (ETB)", min_value=1.0, value=1.0, key="amount_direct")
        customer_name = st.text_input("Customer Name", value="Test User", key="customer_direct")
        email_id = st.text_input("Email ID", value="test@example.com", key="email_direct")
    with col2:
        mobile_number = st.text_input("Mobile Number", value="0909260339", key="mobile_direct")
        success_url = st.text_input("Success URL", value=f"{NGROK_URL}/success", key="success_direct")
        failure_url = st.text_input("Failure URL", value=f"{NGROK_URL}/failure", key="failure_direct")
    
    if st.button("✨ Execute Direct Charge", type="primary", key="btn_direct"):
        try:
            order_no = f"{int(time.time() * 1000)}{random.randint(100,999)}"[-12:]
            # Exact payload from your original Direct Api.py
            payload = {
                "card_details": {"cardNumber": "", "expiryMonth": "", "expiryYear": "", "cvv": "", "cardName": ""},
                "other_details": {"udf1": "", "udf2": "", "udf3": "", "udf4": "", "udf5": "", "udf6": "", "udf7": ""},
                "ship_details": {"shipAddress": "", "shipCity": "", "shipState": "", "shipCountry": "", "shipZip": "", "shipDays": "", "addressCount": ""},
                "txn_details": {
                    "agId": AGGREGATOR_ID,
                    "meId": MERCHANT_ID,
                    "orderNo": order_no,
                    "amount": str(int(amount)),
                    "country": "ETH",
                    "currency": "ETB",
                    "transactionType": "SALE",
                    "sucessUrl": success_url,  # Note: Typo as in original
                    "failureUrl": failure_url,
                    "channel": "API"
                },
                "item_details": {"itemCount": "", "itemValue": "", "itemCategory": ""},
                "cust_details": {
                    "customerName": customer_name,
                    "emailId": email_id,
                    "mobileNumber": mobile_number,
                    "uniqueId": "",
                    "isLoggedIn": "Y"
                },
                "pg_details": {
                    "pg_Id": "67ee846571e740418d688c3f",  # Exact from original
                    "paymode": "WA",
                    "scheme_Id": "7",
                    "wallet_type": "telebirr"
                },
                "bill_details": {"billAddress": "", "billCity": "", "billState": "", "billCountry": "", "billZip": ""}
            }
            plain_json = json.dumps(payload, separators=(',', ':'))  # Minimized as original
            st.subheader("🔮 Before: Plain Payload")
            st.text_area("Plain Payload", plain_json, height=200, key="plain_direct")
            
            with st.spinner("Encrypting & Charging..."):
                encrypted_request = direct_encrypt(plain_json, ENCRYPTION_KEY)
                if not encrypted_request:
                    st.error("Encryption Failed – Check key/IV.")
                    st.stop()
                
                request_body = {"merchantId": MERCHANT_ID, "merchantRequest": encrypted_request}
                headers = {"Content-Type": "application/json"}
                
                try:
                    response = requests.post(API_URL, json=request_body, headers=headers, verify=False, timeout=30)
                    resp_json = response.json()
                    
                    st.subheader("🧙‍♂️ Encrypted Request")
                    st.text_area("Encrypted Payload", encrypted_request, height=100, key="encrypted_direct")
                    
                    if response.status_code == 200 and resp_json.get('status') == "Success":
                        decrypted = direct_decrypt(resp_json['response'], ENCRYPTION_KEY)
                        if decrypted:
                            st.success("🎉 **Charge Enchanted!**")
                            st.json(json.loads(decrypted))
                            st.balloons()
                        else:
                            st.error("Failed to decrypt response")
                    else:
                        st.warning(f"API Response: {resp_json.get('statusMessage', 'Unknown error')}")
                        with st.expander("Debug Raw Response"):
                            st.write(f"Status Code: {response.status_code}")
                            st.json(resp_json)
                            
                except requests.exceptions.RequestException as req_error:
                    st.error(f"Network Error: {req_error}")
                    
        except Exception as e:
            st.error(f"Direct API Error: {str(e)}")
            with st.expander("Debug"):
                st.write("Check: Key decodes to 32 bytes? Network? Update pg_Id if needed.")
                st.write(f"Error details: {type(e).__name__}: {str(e)}")

st.markdown("---")
st.caption("🪄 *Built with your YagoutPaySDK—unifies encryption, APIs, & outputs. Tweak, test, triumph!*")