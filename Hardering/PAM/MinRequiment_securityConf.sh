CONF_FILE="/etc/security/pwquality.conf"

export DEBIAN_FRONTEND=noninteractive

sudo apt install -y libpam-pwquality

sudo tee "$CONF_FILE" > /dev/null <<EOF
# Configurazione requisiti minimi password
minlen = 8
dcredit = -1
ucredit = -1
ocredit = -1
lcredit = -1
EOF

sudo chmod 644 "$CONF_FILE"
sudo chown root:root "$CONF_FILE"
