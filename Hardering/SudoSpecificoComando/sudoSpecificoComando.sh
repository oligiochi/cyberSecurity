NOME_SCRIPT="studente-limited-command"
cd /etc/sudoers.d
echo "studente ALL=(ALL) NOPASSWD: /usr/bin/nmap" > $NOME_SCRIPT

# 3) Imposta i permessi corretti (obbligatorio)
sudo chmod 440 /etc/sudoers.d/$NOME_SCRIPT
sudo chown root:root /etc/sudoers.d/$NOME_SCRIPT

# 4) Verifica la sintassi del file (IMPORTANTISSIMO)
sudo visudo -c -f /etc/sudoers.d/$NOME_SCRIPT