# ROADMAP

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

- Priorità attiva corrente: `M6` resta consolidata sul primo delta di hardening UI della demo web introdotto dal commit `af20290`; con il presente riallineamento il doc gate owner truth-first risulta chiuso. `Responsive refinement`, feedback utente ulteriori e `Docker/exportability` restano backlog non bloccante, mentre un eventuale freeze documentale/handoff separato dovrà essere valutato solo come passaggio successivo e non ancora consolidato a commit.

### M6 — Primo delta di hardening UI della demo web — 🟡
- primo delta consolidato: hardening UI della pagina web e riallineamento del contratto bootstrap testuale;
- UI minimale difendibile con CSS;
- doc gate owner truth-first ora chiuso sul branch `development`;
- responsive refinement e feedback utente ulteriori classificati come backlog non bloccante;
- eventuale freeze documentale/handoff da valutare separatamente come passaggio successivo, non ancora consolidato a commit.

### M7 — Evoluzione prodotto — ⬜
- possibili campi variabili aggiuntivi;
- profili multipli;
- preview opzionale;
- import assistito o integrazione API;
- UI più ricca;
- eventuale estensione con stack aggiuntivi senza riscrivere il core.
