
import requests
from urllib3.exceptions import InsecureRequestWarning

# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Create a session object to save settings for the lifetime of the script.
s = requests.session()
s.verify = False  # Skip trying to verify TLS certs, due to Burp's CA.
s.proxies = {"https": "http://127.0.0.1:8080"}  # Proxy requests through Burp.

for i in range(10000):
    