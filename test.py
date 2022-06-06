import requests
import time

BASE = 'http://127.0.0.1:5000/'

print('\n \n \n \n')

response = requests.put(BASE + 'clients/2000', {'full_name': 'James Watson', 'phone_number': '555888999', 'email_address': 'watson@gmail.com'})
print(response.json())

time.sleep(3)

response = requests.get(BASE + 'clients/2000')
print(response.json())

time.sleep(3)

response = requests.put(BASE + 'clients/2000', {'full_name': 'James Watson', 'phone_number': '555888999', 'email_address': 'watson@gmail.com'})
print(response.json())

time.sleep(3)

response = requests.delete(BASE + 'clients/2001')
print(response.json())

time.sleep(3)

response = requests.delete(BASE + 'clients/2000')
print(response.json())

time.sleep(3)

response = requests.get(BASE + 'clients/2000')
print(response.json())