NOME_SCRIPT="minium-requirement-pam.conf"
DEST_DIR="/etc/pam.d"
cd $DEST_DIR
cat <<'EOF' | sudo tee $NOME_SCRIPT > /dev/null
    #%PAM-1.0
    password requisite pam_pwquality.so try_first_pass
    minium_requirement = 8
    dcredit = -1
    ucredit = -1
    ocredit = -1
    lcredit = -1
EOF

# 3) Imposta i permessi corretti (obbligatorio)
sudo chmod 440 $DEST_DIR/$NOME_SCRIPT
sudo chown root:root $DEST_DIR/$NOME_SCRIPT

# 4) Verifica la sintassi del file (IMPORTANTISSIMO)
sudo systemd-analyze verify "$DEST_DIR/$NOME_SCRIPT" || echo "systemd-analyze verify ha restituito errori (vedi sopra)"

# Ricarica systemd, abilita e avvia il servizio
sudo systemctl daemon-reload
sudo systemctl enable --now "$NOME_SCRIPT"

# Mostra stato e log (ultimo passo)
sudo systemctl status "$NOME_SCRIPT" --no-pager
echo "Logs (seguirli in tempo reale): sudo journalctl -fu $NOME_SCRIPT"