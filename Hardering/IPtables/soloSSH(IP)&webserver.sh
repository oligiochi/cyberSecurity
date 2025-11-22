# Svuota regole esistenti
sudo iptables -F
sudo iptables -X

# Politica di default: blocca tutto
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Permetti loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# Permetti connessioni già stabilite
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Permetti solo SSH (porta 22 TCP) e webserver (porte 80 e 443 TCP)
sudo iptables -A INPUT -p tcp --dport 22 -s 1.2.3.4 -j ACCEPT
# sudo iptables -A INPUT -p tcp --dport 22 -d 1.2.3.4 -j ACCEPT # -d per destinazione -s per sorgente
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save
sudo netfilter-persistent reload
sudo iptables -L