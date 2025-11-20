import paramiko
import os

def esegui_sh_remoto(sh: str):
    # Ricava solo il nome del file
    nome_script = os.path.basename(sh)

    # Crea il client SSH
    client = paramiko.SSHClient()

    # Accetta automaticamente le chiavi degli host non presenti in known_hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connessione come studente
    client.connect(
        hostname="localhost",
        username="studente",
        password="studente",
        port=2223
    )

    # Upload via SFTP nella home dello studente
    sftp = client.open_sftp()
    remote_path = f"/home/studente/{nome_script}"
    sftp.put(sh, remote_path)
    sftp.close()

    # Rendi lo script eseguibile
    client.exec_command(f"chmod +x {remote_path}")

    # Esegui lo script tramite sudo (NON chiede password se hai NOPASSWD)
    comando = f"sudo bash {remote_path}"

    stdin, stdout, stderr = client.exec_command(comando)

    # Leggi output
    print(stdout.read().decode())
    print(stderr.read().decode())

    # Chiudi la connessione
    client.close()


if __name__ == "__main__":
    esegui_sh_remoto("/home/giovanni/Uni/cyber/esercizi/Hardering/unitfileSystemctl/Systemctlunit.sh")
