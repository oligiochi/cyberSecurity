NOME_SCRIPT="studente-limited-command-regex"
cd /etc/sudoers.d
cat <<'EOF' > $NOME_SCRIPT
    Cmnd_Alias NMAP_BLOCK = /usr/bin/nmap -p *, /usr/bin/nmap * -p *, /usr/bin/nmap *-p*, /usr/bin/nmap * -p*
    studente ALL=(ALL) NOPASSWD: /usr/bin/nmap, !NMAP_BLOCK
EOF

# 3) Imposta i permessi corretti (obbligatorio)
sudo chmod 440 /etc/sudoers.d/$NOME_SCRIPT
sudo chown root:root /etc/sudoers.d/$NOME_SCRIPT

# 4) Verifica la sintassi del file (IMPORTANTISSIMO)
sudo visudo -c -f /etc/sudoers.d/$NOME_SCRIPT