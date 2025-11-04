#!/usr/bin/env python3
"""
decrypt_aes_openssl.py

Prova decrittazione di ciphertext nel formato OpenSSL "Salted__" (base64),
usando EVP_BytesToKey (MD5) per derivare key e IV, e testando AES-128/192/256-CBC.

Richiede: pip install pycryptodome
"""

import base64
import hashlib
from binascii import hexlify
from Crypto.Cipher import AES

# --- Configurazione: cambia qui se vuoi ---
b64_ciphertext = "U2FsdGVkX1/JEKDXgPl2RqtEgj0LMdp8/Q1FQelH7whIP49sq+WvNOeNjjXwmdrl"
password = "s3cr37"
# -----------------------------------------

def evp_bytes_to_key(password_bytes: bytes, salt: bytes, key_len: int, iv_len: int):
    """
    Implementazione di OpenSSL EVP_BytesToKey con MD5 (una iterazione).
    Restituisce (key, iv).
    """
    dtot = b''
    prev = b''
    while len(dtot) < (key_len + iv_len):
        prev = hashlib.md5(prev + password_bytes + salt).digest()
        dtot += prev
    return dtot[:key_len], dtot[key_len:key_len+iv_len]

def pkcs7_unpad(data: bytes):
    if not data:
        return data
    pad_len = data[-1]
    if pad_len < 1 or pad_len > AES.block_size:
        raise ValueError("Padding non valido")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Padding PKCS#7 incoerente")
    return data[:-pad_len]

def try_decrypt(data: bytes, password: str):
    # controlla formato Salted__
    if data[:8] != b"Salted__":
        raise ValueError("Il dato non sembra essere nel formato OpenSSL 'Salted__'")
    salt = data[8:16]
    cipherbytes = data[16:]
    print(f"Salt (hex): {hexlify(salt).decode()}")

    for key_len in (16, 24, 32):  # AES-128, AES-192, AES-256
        try:
            key, iv = evp_bytes_to_key(password.encode(), salt, key_len, 16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plain = cipher.decrypt(cipherbytes)
            try:
                plain = pkcs7_unpad(plain)
            except Exception as e:
                # se padding invalido, comunque mostriamo il risultato raw
                print(f"[AES-{key_len*8}] Warning padding: {e}")

            print(f"\n--- Tentativo AES-{key_len*8} ---")
            print("Key (hex):", hexlify(key).decode())
            print("IV  (hex):", hexlify(iv).decode())
            print("Plaintext (hex):", hexlify(plain).decode())
            try:
                text = plain.decode('utf-8')
                print("Plaintext (utf-8):", text)
            except UnicodeDecodeError:
                print("Plaintext non decodificabile come UTF-8 (probabilmente dati binari).")
        except Exception as exc:
            print(f"[AES-{key_len*8}] Errore: {exc}")

def main():
    try:
        data = base64.b64decode(b64_ciphertext)
    except Exception as e:
        print("Errore nel decodare base64:", e)
        return

    try:
        try_decrypt(data, password)
    except Exception as e:
        print("Errore:", e)

if __name__ == "__main__":
    main()
