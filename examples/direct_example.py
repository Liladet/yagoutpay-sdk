from yagoutpay import YagoutPaySDK

sdk = YagoutPaySDK("202508080001", "IG3CNW5uNrUO2mU2htUOWb9rgXCF7XMAXmL63d7wNZo=", "test")
payload = {
    "card_details": {
        "cardNumber": "",  # Empty for wallet
        "expiryMonth": "",
        "expiryYear": "",
        "cvv": "",
        "cardName": ""
    },
    "other_details": {"udf1": "", "udf2": "", "udf3": "", "udf4": "", "udf5": "", "udf6": "", "udf7": ""},
    "ship_details": {
        "shipAddress": "", "shipCity": "", "shipState": "", "shipCountry": "", "shipZip": "", "shipDays": "", "addressCount": ""
    },
    "txn_details": {
        "amount": "1",
        "country": "ETH",
        "currency": "ETB",
        "transactionType": "SALE",
        "sucessUrl": "https://yourdomain.com/success",
        "failureUrl": "https://yourdomain.com/failure"
    },
    "item_details": {"itemCount": "", "itemValue": "", "itemCategory": ""},
    "cust_details": {
        "customerName": "Test User",
        "emailId": "test@example.com",
        "mobileNumber": "0909260339",
        "uniqueId": "",
        "isLoggedIn": "Y"
    },
    "pg_details": {
        "pg_Id": "67ee846571e740418d688c3f",
        "paymode": "WA",
        "scheme_Id": "7",
        "wallet_type": "telebirr"
    },
    "bill_details": {
        "billAddress": "", "billCity": "", "billState": "", "billCountry": "", "billZip": ""
    }
}
result = sdk.initiate_direct_payment(payload)
print("Direct Result:", result)
# Expected: {"status": "success", "decrypted_response": "{\"status\": \"Success\", ...}"}
# Test: Parse decrypted—contains payment ID or next steps?