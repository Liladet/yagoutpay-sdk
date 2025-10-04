from setuptools import setup, find_packages

setup(
    name="yagoutpay-sdk",
    version="0.1.0",  # Bump to 1.0.0 for first real release
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "cryptography>=41.0.0",
        "pycryptodome>=3.18.0",
        "qrcode[pil]>=7.4.2",
        "Pillow>=10.0.0",
        "streamlit>=1.50.0",
    ],
    extras_require={
        "test": ["pytest>=7.0", "pytest-cov", "requests-mock>=1.10.0"],
    },
    author="Lidiya Alemayehu",
    author_email="lilaalex94@gmail.com",  # Add yours
    description="YagoutPay Python SDK for secure payments",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/liladet/yagoutpay-sdk",  # Add if GitHub repo
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
    ],
    keywords="payments sdk yagoutpay encryption aes",
    python_requires=">=3.8",
)