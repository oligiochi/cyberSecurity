import requests

url="http://web-08.challs.olicyber.it/login"

data = {'username': 'admin', 'password': 'admin'}
r=requests.post(url, data=data)

print(r.content)