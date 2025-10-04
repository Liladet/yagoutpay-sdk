from yagoutpay import YagoutPaySDK
import requests
from bs4 import BeautifulSoup  # pip install beautifulsoup4 if not installed

sdk = YagoutPaySDK("202508080001", "IG3CNW5uNrUO2mU2htUOWb9rgXCF7XMAXmL63d7wNZo=", "test")
html = sdk.generate_hosted_checkout(
    amount="1",
    name="Test User",
    email="test@email.com",
    phone="0909260339",
    success_url="https://yourdomain.com/success",
    failure_url="https://yourdomain.com/failure"
)
with open("hosted_form.html", "w") as f:
    f.write(html)

# Debug: Extract & test POST manually
soup = BeautifulSoup(html, 'html.parser')
form = soup.find('form')
action_url = form['action']
form_data = {inp.get('name'): inp.get('value') for inp in form.find_all('input') if inp.get('name')}  # Filter for 'name'
print("Form Action:", action_url)
print("Form Data Keys:", list(form_data.keys()))
print("Sample merchant_request (first 50 chars):", form_data.get('merchant_request', '')[:50] if 'merchant_request' in form_data else "Missing merchant_request")

# Simulate submit
response = requests.post(action_url, data=form_data, verify=False)
print(f"Submit Status: {response.status_code}")
print(f"Submit Raw: {response.text[:300]}...")