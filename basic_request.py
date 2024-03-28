import requests
from urllib3.exceptions import InsecureRequestWarning
import json
# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

s = requests.session() # This session object saves our settings for the lifetime of the script.
s.verify = False # Skip trying to verify TLS certs, due to Burp's CA.
s.proxies = {"https": "http://127.0.0.1:8080"} # Proxy requests through Burp.


r = s.get("https://quoccabank.com")
print(r.content)