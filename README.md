# YagoutPay Python SDK

A secure, easy-to-use Python library for integrating YagoutPay payment methods: static/dynamic links, hosted checkout, and direct API calls. Handles AES encryption, API requests, and validation out-of-the-box.

## Features

- Static QR payment links with auto-QR generation.
- Dynamic links with expiry checks.
- Hosted form redirects (HTML output).
- Direct wallet/card payments.
- Test/prod environment switching.
- Built for Python 3.8+.

## Installation

```bash
git clone <your-repo>  # Or download
cd yagoutpay-sdk
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\Activate.ps1
pip install -e .
```

# or

```bash
pip install yagoutpay-sdk
```
