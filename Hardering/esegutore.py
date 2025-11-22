import paramiko

def esegui_script_remoto(sh: str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        hostname="localhost",
        username="exam",         # <<< UTENTE GIUSTO
        password="exam",         # <<< PASSWORD GIUSTA
        port=2222,
        allow_agent=False,
        look_for_keys=False
    )

    # Upload nello stesso nome
    sftp = client.open_sftp()
    sftp.put(sh, "/home/exam/mioscript.sh")
    sftp.close()

    # Esegui lo script con sudo (senza password!)
    stdin, stdout, stderr = client.exec_command("bash /home/exam/mioscript.sh")

    print(stdout.read().decode())
    print(stderr.read().decode())

    client.close()

