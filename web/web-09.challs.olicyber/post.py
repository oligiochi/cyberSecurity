import requests
import json

url="http://web-09.challs.olicyber.it/login"

data = {'username': 'admin', 'password': 'admin'}
headers = {'Content-Type': "application/json"}
filejson = json.dumps(data)
r=requests.post(url, data=filejson, headers=headers)

print(r.content)