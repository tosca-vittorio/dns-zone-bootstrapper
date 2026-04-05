# ROADMAP

- Priorità attiva corrente: nessun blocco tecnico attivo da proseguire sulla v1. Il repository viene considerato chiuso nella forma attuale e stabile raggiunta su `development`: demo web minimale funzionante, generazione file `.txt` import-ready, validazione empirica Cloudflare, owner docs riallineati e hygiene runtime sufficiente. Eventuali approfondimenti ulteriori su audit strutturale del repository, integrazione ergonomica del cleanup, espansione architetturale completa, responsive refinement, feedback utente aggiuntivi e `Docker/exportability` restano backlog/extra non bloccante.

## Missione del progetto

Costruire una pagina web capace di generare, a partire da un dominio in input, un file di zona DNS coerente con un template aziendale fisso e pronto per il workflow di import su Cloudflare, con focus iniziale sui record necessari a uno scenario mailcow.

## Milestone evolutive

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

### M5 — Documentazione essenziale e preparazione consegna — ✅
- rafforzare il `README.md` come documento di ingresso al prodotto;
- chiarire senso del prodotto, value proposition, workflow e perimetro v1;
- chiarire concetti minimi necessari (`BIND`, zone file, zona apex, import Cloudflare, profili fixed);
- riallineare dove serve `ARCHITECTURE.md` ai chiarimenti tecnici/concettuali;
- introdurre una guida utente dedicata solo se realmente necessaria;
- preparare il report/messaggio di stato verso l'azienda e sbloccare la prima consegna/demo.

### M6 — Primo delta di hardening UI della demo web — ✅
- primo delta consolidato: hardening UI della pagina web e riallineamento del contratto bootstrap testuale;
- UI minimale difendibile con CSS;
- doc gate owner truth-first chiuso sul branch `development`;
- responsive refinement e feedback utente ulteriori classificati come backlog non bloccante;
- milestone chiusa nella forma effettivamente raggiunta, senza ulteriori aperture tecniche necessarie per la chiusura del progetto.

### M6.5 — Hygiene runtime e razionalizzazione strutturale del repository — ✅
- consolidati il doc sync owner successivo all'introduzione del cleanup utility Python repo-owned e il riallineamento truth-first del boundary `local/`;
- consolidato il quality-gate snapshot post-doc-sync su `development`;
- classificato in modo sufficiente e conservativo il perimetro di hygiene runtime utile alla chiusura del progetto;
- eventuali audit strutturali più ampi del repository, integrazione del cleanup in CLI/demo web e rafforzamenti architetturali ulteriori rinviati a backlog/extra non bloccante;
- milestone chiusa nella forma realmente necessaria alla chiusura del progetto.

### EXTRA — Espansione architetturale completa del repository — ⬜
- riscrivere/espandere `docs/ARCHITECTURE.md` in forma esaustiva;
- spiegare moduli, boundary, dataclass, flussi runtime, entrypoint, failure mode, test suite e copertura logica del progetto;
- trasformare il documento architetturale in una base utile anche per studio, handoff e manutenzione evolutiva.

### M7 — Evoluzione prodotto — ⬜
- possibili campi variabili aggiuntivi;
- profili multipli;
- preview opzionale;
- import assistito o integrazione API;
- UI più ricca;
- eventuale estensione con stack aggiuntivi senza riscrivere il core.
