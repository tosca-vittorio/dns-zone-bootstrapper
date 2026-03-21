# ROADMAP

## Missione del progetto

Costruire una pagina web capace di generare, a partire da un dominio in input, un file di zona DNS coerente con un template aziendale fisso e pronto per il workflow di import su Cloudflare, con focus iniziale sui record necessari a uno scenario mailcow.

## Milestone evolutive

### M0 — Baseline repository
- bootstrap repository;
- owner docs;
- skeleton Python riusabile;
- entrypoint tecnici minimi;
- verifica locale iniziale.

### M1 — Chiusura requisiti v1 e contratto del generatore
- acquisizione del file reale di riferimento;
- chiarimento con l'azienda del comportamento atteso della v1;
- conferma di input unico = dominio;
- conferma di valori fissi per ora;
- definizione del contratto input/output del generatore.

### M2 — Core engine
- validazione dominio;
- profilo/template DNS fisso;
- renderer BIND;
- test sul testo generato;
- preparazione futura per fixture golden.

### M3 — Delivery demo web
- pagina web minimale;
- form con solo input dominio;
- generazione del file `.txt`;
- download diretto del file pronto per import Cloudflare;
- packaging demo presentabile.

### M4 — Evoluzione prodotto
- possibili campi variabili aggiuntivi;
- profili multipli;
- preview opzionale;
- import assistito o integrazione API;
- UI più ricca;
- eventuale estensione con stack aggiuntivi senza riscrivere il core.
