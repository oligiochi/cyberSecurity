#!/bin/bash

# Svuota regole esistenti
sudo iptables -F
sudo iptables -X

# Politica di default: blocca tutto
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT DROP

# Permetti loopback
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT

# Permetti connessioni già stabilite (risposte alle richieste)
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Permetti webserver in ingresso (HTTP/HTTPS)
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Permetti al server di rispondere alle richieste web (OUTPUT verso client)
sudo iptables -A OUTPUT -p tcp --sport 80 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 443 -j ACCEPT

# Salva le regole in modo persistente
sudo netfilter-persistent save
sudo netfilter-persistent reload

# Controlla le regole attive
sudo iptables -L -v
