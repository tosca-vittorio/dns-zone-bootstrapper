# ROADMAP

## Missione del progetto

Costruire una pagina web capace di generare, a partire da un dominio in input, un file di zona DNS coerente con un template aziendale fisso e pronto per il workflow di import su Cloudflare, con focus iniziale sui record necessari a uno scenario mailcow.

## Milestone evolutive

- Priorità attiva corrente: consolidare `M5`, cioè il blocco documentale essenziale che rende il prodotto comprensibile, presentabile e pronto alla prima comunicazione/consegna verso l'azienda.

### M0 — Baseline repository — ✅
- bootstrap repository;
- owner docs;
- skeleton Python riusabile;
- entrypoint tecnici minimi;
- verifica locale iniziale.

### M1 — Chiusura requisiti v1 e contratto del generatore — ✅
- acquisizione del file reale di riferimento;
- chiarimento del comportamento atteso della v1;
- conferma di input unico = dominio;
- conferma di valori fissi per ora;
- definizione del contratto input/output del generatore.

### M2 — Core engine — ✅
- validazione dominio;
- profilo/template DNS fisso;
- renderer BIND;
- test sul testo generato;
- protezione tramite golden e fixture realistic-backed;
- boundary runtime tra baseline public-safe e override locale.

### M3 — Delivery demo web — ✅
- pagina web minimale;
- form con solo input dominio;
- generazione del file `.txt`;
- download diretto del file pronto per import Cloudflare;
- packaging demo minimale locale.

### M4 — Validazione empirica Cloudflare e freeze strategico — ✅
- verifica reale dell'import su zona pulita;
- classificazione del primo failure su `www` come conflitto ambientale e non come difetto del generatore;
- hardening conservativo dell'isolamento tra test applicativi versionati e profilo locale gitignored;
- congelamento della sequenza post-validazione.

### M5 — Documentazione essenziale e preparazione consegna — 🟡
- rafforzare il `README.md` come documento di ingresso al prodotto;
- chiarire senso del prodotto, value proposition, workflow e perimetro v1;
- chiarire concetti minimi necessari (`BIND`, zone file, zona apex, import Cloudflare, profili fixed);
- riallineare dove serve `ARCHITECTURE.md` ai chiarimenti tecnici/concettuali;
- introdurre una guida utente dedicata solo se realmente necessaria;
- preparare il report/messaggio di stato verso l'azienda e sbloccare la prima consegna/demo.

### M6 — Hardening esperienza utente ed exportability — ⬜
- UI minimale difendibile con CSS;
- miglioramenti responsive e feedback utente;
- Docker e relativa documentazione di deployment;
- demo più presentabile e più portabile.

### M7 — Evoluzione prodotto — ⬜
- possibili campi variabili aggiuntivi;
- profili multipli;
- preview opzionale;
- import assistito o integrazione API;
- UI più ricca;
- eventuale estensione con stack aggiuntivi senza riscrivere il core.
