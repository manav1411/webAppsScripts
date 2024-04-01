import requests, urllib3, re

cert  = ('/path/to/cert.pem', '/path/to/cert.key')

# Create the post
page = requests.post(
	"https://login.quoccabank.com",
	data = {"username": "melon", "password": "Hunter2"},
	certs=cert
)

# you could extract the session cookie like so!
cookie = re.search(r"session=(.+?);", page.headers['Set-Cookie']).group(1)
print(cookie)

# now we can use that cookie, and send it to another page maybe?
page = requests.get("https://quoccabank.com/view/", certs=cert, cookies = { 'session': cookie })
print(page.text)