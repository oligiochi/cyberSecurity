# cyberSecurity

Raccolta personale di appunti, exploit e soluzioni di challenge di **Cybersecurity**, con focus sulla preparazione alle prove di [OliCyber](https://olicyber.it) (Olimpiadi Italiane di Cybersicurezza).

Il repository copre quattro macro-aree: **Web Security**, **SQL Injection**, **System Hardening** e **Command Injection / SSRF**, oltre a materiale di riferimento (OWASP ASVS).

---

## 📁 Struttura del repository

| Cartella | Contenuto |
|----------|-----------|
| [`web/`](web/) | Soluzioni e writeup delle challenge di Web Security |
| [`sql_w/`](sql_w/) | Tooling e script Python per SQL Injection (blind, time-based, union, ecc.) |
| [`Hardering/`](Hardering/) | Esercizi di hardening di sistema su VM Debian |
| [`commandInjections/`](commandInjections/) | Appunti su Command Injection e SSRF |
| [`docker/`](docker/) | Materiale di riferimento (OWASP Application Security Verification Standard 4.0.2) |
| [`Challenges.md`](Challenges.md) | Elenco delle challenge con difficoltà e stato di completamento |

---

## 🌐 Web Security

La cartella [`web/`](web/) contiene le soluzioni delle challenge di Web Security. Ogni sottocartella corrisponde a una challenge specifica:

`adminSecret`, `curiosojorg`, `delphi`, `flagshop`, `gabibbosay`, `just-a-reminder`,
`magic`, `memeShop`, `nflagt`, `pincode`, `revange shell`, `sn4ck-sh3nan1gans`,
`soundOfSilence`, `time`, `TIMP`, `toSmall`, `ziofrank` e le raccolte
`web-03/04/08/09.challs.olicyber`.

L'elenco completo con la difficoltà indicativa (1–8) e lo stato di completamento è in [`Challenges.md`](Challenges.md).

## 💉 SQL Injection

La cartella [`sql_w/`](sql_w/) raccoglie script Python riutilizzabili per le diverse tecniche di SQL Injection:

- **`blind/`** — SQL injection blind (boolean-based)
- **`time/`** — SQL injection time-based, con script di misurazione dei tempi di risposta
- **`union/`** — attacchi UNION-based, bruteforce e gestione CSRF
- **`snackGame/`** — exploit dedicato a una challenge specifica
- **`util/`** — utility condivise (`Inj.py`) usate dagli exploit

## 🛡️ System Hardening

La cartella [`Hardering/`](Hardering/) contiene una serie di esercizi di hardening su **VM Debian**, con un ambiente Docker per la pratica. Gli argomenti trattati includono:

- Configurazione di `sudo` / `sudoers` (comandi ristretti, espressioni regolari)
- Ricerca di binari **SUID/SGID**
- Unit file di **systemd**
- Moduli **PAM** per i requisiti minimi delle password
- Password su **GRUB**
- Permessi su `/var/log` e ricerca di file world-writable
- Analisi dei file descriptor con **`lsof`**
- Configurazione di **iptables** (SSH, webserver, blocco traffico)

L'elenco completo degli esercizi è in [`Hardering/esercizi.md`](Hardering/esercizi.md).

Ambiente di laboratorio (Docker):

```bash
cd Hardering
./start.sh    # avvia il container
./stop.sh     # ferma il container
./restore.sh  # ripristina lo stato iniziale
```

## 🔀 Command Injection & SSRF

La cartella [`commandInjections/`](commandInjections/) raccoglie appunti su Command Injection e Server-Side Request Forgery (SSRF).

---

## 📚 Materiale di riferimento

- **OWASP ASVS 4.0.2** — Application Security Verification Standard, in [`docker/`](docker/)
- Report PDF sulle vulnerabilità analizzate (es. `web/Vulnerabilita_PHP_POST_password_report.pdf`)

---

## ⚠️ Disclaimer

Questo repository ha scopo **esclusivamente didattico** e di preparazione a competizioni CTF autorizzate. Gli exploit e le tecniche qui contenuti vanno utilizzati **solo su sistemi e ambienti di cui si ha esplicita autorizzazione**. L'autore non è responsabile di alcun uso improprio del materiale.
