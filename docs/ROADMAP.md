# ROADMAP

- Priorità attiva corrente: `D8` è stata chiusa introducendo un meccanismo runtime esplicito (`DNS_ZONE_PROFILE_PATH`) per il profilo fixed concreto; il prossimo passo corretto non è aprire automaticamente l’audit strutturale largo del repository, ma congelare lo stato stabile post-`D8` e decidere con audit conservativo il blocco successivo realmente necessario.

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

### D6 — Packaging/demo finale e Docker/exportability — ✅
- `.dockerignore` e `Dockerfile` introdotti nel commit `1e0b68e`;
- build reale del container eseguita con successo;
- smoke runtime verificato su `GET /` e `GET /generate?domain=testdomain.com`;
- baseline container attuale chiusa come public-safe: `local/` è escluso dal build context e l’output nel container usa quindi i placeholder versionati;
- un successivo tentativo di bind mount di `local/` da Git Bash su Windows non ha materializzato `/app/local` nel container e non costituisce quindi evidenza di supporto consolidato agli override locali nel runtime containerizzato;
- milestone chiusa nella forma realmente consolidata: packaging Docker minimale public-safe, riproducibile e smoke-testato; eventuale supporto futuro ai valori locali concreti nel container rinviato a backlog/extra separato.

### D8 — Canonicalizzazione del profilo fixed concreto e superamento del boundary `local/` — ✅
- audit read-only `public_safe vs local vs snapshot` chiuso con esito `same contract / different values`;
- introdotto nel commit `61a4f73` il path runtime esplicito `DNS_ZONE_PROFILE_PATH` come meccanismo distribuito e documentabile per il profilo fixed concreto;
- `local/` riclassificato in modo difendibile come fallback tecnico transitorio/back-compat dell'AS-IS e non come contratto utente finale;
- quality gates verdi al consolidamento: `python run_quality_gates.py` → `pytest 86 passed`, `pylint 10.00/10`, `coverage 250 stmt`, `0 miss`, `100%`;
- blocco chiuso: il prodotto non dipende più, sul piano del contratto finale, da un override locale implicito come unica strada per i valori fixed concreti.

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
