import requests

url="http://nflagt.challs.cyberchallenge.it"
s=requests.Session()
headers = {
    "s": "Add To Cart",
    "qnt": "1",
    "item": "flag"
}
#r = s.post(url, data=headers)
#print(r.text)
url="http://nflagt.challs.cyberchallenge.it/reset.php"
r = s.get(url,allow_redirects=False)
print(r.headers)
print(r.text)