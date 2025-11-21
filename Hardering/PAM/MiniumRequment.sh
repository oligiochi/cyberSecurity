NOME_SCRIPT="minium-requirement-pam.conf"
DEST_DIR="/usr/share/pam-configs/"
export DEBIAN_FRONTEND=noninteractive

sudo apt install -y libpam-pwquality
cd $DEST_DIR
cat <<'EOF' | sudo tee $NOME_SCRIPT > /dev/null
Name: Minimum password requirements
Default: yes
Priority: 900
Password-Type: Primary
Password:
    requisite pam_pwquality.so try_first_pass minlen=8 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1
EOF

# 3) Imposta i permessi corretti (obbligatorio)
sudo chmod 440 $DEST_DIR/$NOME_SCRIPT
sudo chown root:root $DEST_DIR/$NOME_SCRIPT

sudo pam-auth-update --force