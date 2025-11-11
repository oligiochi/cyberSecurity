# Esercizi di hardening (VM Debian 13)

Di seguito trovi una lista di esercizi di preparazione alla prova pratica nella parte di **hardening**. Lo svolgimento è facoltativo ma caldamente consigliato.

> **Nota:** Per marcare un esercizio come completato, sostituisci lo spazio vuoto nel `<span>` con `&check;`, cioè usa: `<span style="float: right;">&check;</span>`.

---

1. Configura `sudo` affinchè un utente possa eseguire solo un comando specifico (es.: `nmap`). <span style="float: right;"> </span>

2. Configura `sudo` affinchè un utente possa eseguire solo un comando specifico ma **senza un parametro** (es.: si può eseguire `nmap` ma non `nmap -p`).

   > Nota: si possono mettere espressioni regolari nel file `sudoers`. <span style="float: right;"> </span>

3. Cercare tutti gli eseguibili con **SUID**. <span style="float: right;"> </span>

4. Cercare tutti gli eseguibili con **SGID**. <span style="float: right;"> </span>

5. Creare uno *unit file* di **systemd** per permettere una shell aperta a tutti sulla rete (netcat in modalità *listen* che esegue `/bin/bash`) e provare a connettersi dalla propria macchina usando `netcat`. <span style="float: right;"> </span>

6. Installare e configurare un modulo **PAM** per richiedere caratteristiche minime alla password (min 8 caratteri, maiuscole, minuscole e simboli). <span style="float: right;"> </span>

7. Imposta una password a **GRUB** così da non permettere l'avvio del sistema operativo con parametri del kernel non standard. <span style="float: right;"> </span>

8. Rendi la cartella `/var/log` leggibile solo da `root`. <span style="float: right;"> </span>

9. Configura un utente per poter **fare `cat` dei log** ma non essere amministratore (va configurato `sudoers` in modo opportuno). <span style="float: right;"> </span>

10. Trova tutti i processi che hanno un file descriptor aperto dentro la cartella `/var/log` (il comando `lsof` tornerà comodo). <span style="float: right;"> </span>

11. Usa **Docker** per effettuare una privilege escalation (esercizio di laboratorio offensivo—esegui solo in ambiente controllato). <span style="float: right;"> </span>

12. Cercare se esiste qualche **file** all'interno della home di un utente che sia **scrivibile da tutti** gli utenti. <span style="float: right;"> </span>

13. Cercare se esiste una **cartella** all'interno della home di un utente che sia **scrivibile da tutti** gli utenti. <span style="float: right;"> </span>

14. Creare un utente con la password che **scade ogni giorno**. <span style="float: right;"> </span>

15. Imposta **iptables** affinchè sia permesso l'accesso alla macchina solo via **SSH (TCP port 22)**. <span style="float: right;"> </span>

16. Imposta **iptables** affinchè sia permesso l'accesso alla macchina solo via **SSH (TCP port 22)** dall'IP `1.2.3.4` e ad un webserver da qualunque IP (TCP port **80** e **443**). <span style="float: right;"> </span>

17. Imposta **iptables** affinchè sia bloccato tutto il traffico Internet sulla macchina (gli utenti non possono navigare) ma sia funzionante il webserver (TCP port **80** e **443**). <span style="float: right;"> </span>

18. Imposta **iptables** affinchè sia permesso l'accesso alla macchina solo via **SSH (TCP port 22)** e ad un webserver (TCP port **80** e **443**). <span style="float: right;"> </span>

---

## Suggerimenti rapidi

* Per cercare SUID/SGID: `find / -perm /4000 -type f 2>/dev/null` e `find / -perm /2000 -type f 2>/dev/null`.
* Per file descriptor in `/var/log`: `lsof +D /var/log`.
* Per trovare file/cartelle world-writable nelle home: `find /home -xdev -type f -perm -o=w` e `find /home -xdev -type d -perm -o=w`.

---

> Modifica il file per marcare gli esercizi completati sostituendo il contenuto dello `span` con `&check;` (es.: `<span style="float: right;">&check;</span>`).
