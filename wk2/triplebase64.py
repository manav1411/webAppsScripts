import base64
ticket = input('enter ticket here:\n')
encoded_string = base64.b64encode(ticket.encode()).decode()
encoded2_string = base64.b64encode(encoded_string.encode()).decode()
encoded3_string = base64.b64encode(encoded2_string.encode()).decode()
print(encoded3_string)