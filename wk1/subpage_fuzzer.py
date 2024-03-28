import requests
from urllib3.exceptions import InsecureRequestWarning
import time
# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

s = requests.session() # This session object saves our settings for the lifetime of the script.
s.verify = False # Skip trying to verify TLS certs, due to Burp's CA.
s.proxies = {"https": "http://127.0.0.1:8080"} # Proxy requests through Burp.
base_url = "https://quoccabank.com/"

# sends get request to all quoccabank.com/XXXXX from file
def send_requests(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            # Strip newline and whitespace characters and then build the full URL.
            endpoint = line.strip()
            full_url = f"{base_url}{endpoint}"

            response = s.get(full_url)
            if response.status_code != 404:
                print(f"URL: {full_url} | Response length: {len(response.content)}, Status code: {response.status_code}")
            if response.status_code == 429:
                print(f"too many requests! 429.")
                time.sleep(0.2)



file_path = 'webpages.txt'
send_requests(file_path)