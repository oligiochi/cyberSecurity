import paramiko

def esegui_sh_remoto(sh:str):
    # Crea il client SSH
    client = paramiko.SSHClient()

    # Accetta automaticamente le chiavi degli host non presenti in known_hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connessione
    client.connect(
        hostname="localhost",   # indirizzo IP o nome host
        username="root",         # nome utente SSH
        password="root",     # password SSH
        port=2223                  # porta SSH (default 22)
    )

    sftp = client.open_sftp()
    sftp.put(sh, "/tmp/mioscript.sh")  # carica lo script
    sftp.close()

    # Esegui un comando remoto
    stdin, stdout, stderr = client.exec_command("bash /tmp/mioscript.sh")

    # Stampa il risultato
    print(stdout.read().decode())
    print(stderr.read().decode())
    

    # Chiudi la connessione
    client.close()
    
if __name__ == "__main__":
    esegui_sh_remoto("/home/giovanni/Uni/cyber/esercizi/Hardering/unitfileSystemctl/Systemctlunit.sh")
