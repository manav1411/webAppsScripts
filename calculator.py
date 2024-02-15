import requests
from urllib3.exceptions import InsecureRequestWarning
import re

# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Function to send the POST request
def send_post_request(session, url, payload):
    response = session.post(url, data={'requestBox': payload})
    return response


# sets payload given sum
def set_payload(sum, cookie):
    content_sum = str(len(str(sum)) + 9)
    answer_sum = str(sum)

    payload = f"""POST /calculator HTTP/1.1
Host: kb.quoccabank.com
Content-Type: application/x-www-form-urlencoded
Content-Length: {content_sum}
Cookie: session={cookie};

answer={answer_sum}
\n\n
"""
    return payload


# function takes the raw response, parses the numbers, returns the sum.
def raw_response_to_sum(response):
    #converts bytes to str, finds math expression
    decoded_response = (response.content).decode("utf-8")
    expression = re.search(" [^ ]+\+[^?]+\?", decoded_response)
    expression = expression.group()

    #finds numbers, converts nums to str
    split_pattern = '\+'
    numbers = re.split(split_pattern, expression) 
    numbers[0] = int(numbers[0][1:])
    numbers[1] = int(numbers[1][:-1])

    sum = numbers[0] + numbers [1]
    return sum

# function takes the raw response, parses text, returns the cookie.
def raw_response_to_cookie(response):
    #converts bytes to str, finds math expression
    decoded_response = (response.content).decode("utf-8")
    expression = re.search("session=[^;]*;", decoded_response)
    expression = expression.group()

    #gets only cookie string
    expression = expression[8:]
    expression = expression[:-1]
    return expression

# Set up the session
s = requests.session()
s.verify = False  # Skip trying to verify TLS certs.
s.proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}  # Proxy requests through Burp.

url = "https://haas.quoccabank.com"



# The raw HTTP request you want to make to kb.quoccabank.com, initial sum set to 0.
initial_payload = set_payload(5, "abc")
print(f"initial payload: \n{initial_payload}")

# Use the session to send the POST request to haas.quoccabank.com with the rendered payload
initial_response = send_post_request(s, url, initial_payload)
number_sum = raw_response_to_sum(initial_response)
cookie_to_use = raw_response_to_cookie(initial_response)


for i in range(21):
    #set the payload
    payload = set_payload(number_sum, cookie_to_use)
    print(f"current payload:\n{payload}")

    # Send the request
    response = send_post_request(s, url, payload)
    print(f"response to above:\n{response.content}")
    if i is 20:
        exit()

    #finds the number sum and cookie
    number_sum = raw_response_to_sum(response)
    cookie_to_use = raw_response_to_cookie(response)
