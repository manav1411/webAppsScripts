import requests

#burp proxy-ing. use variable s to send requests through burp
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
s = requests.session()
s.verify = False
s.proxies = {"https": "http://127.0.0.1:8080"}

r = s.get("https://ctfd.quoccabank.com")
print(r.content)