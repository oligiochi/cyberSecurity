NOME_SCRIPT="studente-cat-log-permission"
cd /etc/sudoers.d
cat <<'EOF' | sudo tee $NOME_SCRIPT > /dev/null
    studente ALL=(ALL) NOPASSWD: /usr/bin/cat /var/log/[a-zA-Z0-9._-]*
EOF

# 3) Imposta i permessi corretti (obbligatorio)
sudo chmod 440 /etc/sudoers.d/$NOME_SCRIPT
sudo chown root:root /etc/sudoers.d/$NOME_SCRIPT

# 4) Verifica la sintassi del file (IMPORTANTISSIMO)
sudo visudo -c -f /etc/sudoers.d/$NOME_SCRIPT