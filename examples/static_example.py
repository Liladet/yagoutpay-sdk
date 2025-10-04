from yagoutpay import YagoutPaySDK

sdk = YagoutPaySDK("202508080001", "IG3CNW5uNrUO2mU2htUOWb9rgXCF7XMAXmL63d7wNZo=", "test")
payload = {
    "ag_id": "",
    "ag_code": "",
    "ag_name": "",
    "req_user_id": "yagou381",
    "me_code": "202508080001",
    "me_name": "",
    "qr_code_id": "",
    "brandName": "Lidiya",
    "qr_name": "",
    "status": "ACTIVE",
    "storeName": "YP",
    "store_id": "",
    "token": "",
    "qr_transaction_amount": "1",
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
    "successURL": "",
    "failureURL": "",
    "addAll": "",
    "source": ""
}
result = sdk.create_static_link(payload)
print("Static Result:", result)
# Expected: {"status": "success", "link": "https://.../static/...", "qr_id": "...", "qr_file": "payment_qr_....png"}
# Check: File exists? Open PNG—scans to link?