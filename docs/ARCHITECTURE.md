# ARCHITECTURE

## Scopo

Il progetto nasce per generare, a partire da un dominio in input, un file di zona DNS in formato BIND pronto per l'import su Cloudflare, usando come base un template DNS fisso derivato da un file reale di riferimento fornito dall'azienda, con focus iniziale su uno scenario coerente con mailcow.

## Vincoli attuali

- il file reale di riferimento è stato acquisito;
- la v1 prevede un solo input utente: il dominio;
- tutti gli altri valori del template sono fissi per ora;
- il file generato deve essere pronto per l'import su Cloudflare, senza necessità di replicare tutta la forma dell'export originale;
- il sottoinsieme v1 import-ready, privo di preambolo export e record `SOA`, è stato validato empiricamente con import riuscito su una zona Cloudflare pulita;
- la preview non è necessaria nella v1;
- la pagina web è il deliverable principale richiesto;
- non esiste una preferenza di stack imposta dall'azienda.

## Direzione architetturale approvata

### 1. Core Python framework-agnostic
Il cuore del sistema deve vivere in moduli Python indipendenti dalla pagina web e da future estensioni.

Responsabilità attese:
- validazione dominio;
- modello logico del template DNS;
- separazione tra parte derivata dal dominio e parte fissa;
- rendering del zone file;
- orchestrazione del caso d'uso di generazione.

### 2. Pagina web come superficie principale della v1
La prima interfaccia utente richiesta è una pagina web minimale, con una sola interazione essenziale:
- inserimento dominio;
- generazione file;
- download del `.txt`.

La CLI non è il deliverable principale della v1 e resta solo una superficie tecnica di supporto.

### 3. Template fisso internalizzato ma non hardcodato male
Il template DNS deve essere trattato come profilo fisso interno al sistema, mantenendo però una separazione chiara dalla pagina web e dalla logica di orchestrazione.

Questo permette di:
- consegnare rapidamente la v1;
- evitare ridondanze nell'interfaccia;
- restare pronti a futuri valori variabili senza riscrivere il core.

### 4. Rendering separato e testabile
La generazione del file `.txt` deve vivere in un renderer dedicato, separato dall'interfaccia web, così da poter essere testata e confrontata in modo autonomo.

### 5. Risoluzione runtime del profilo fixed

Il repository versionato mantiene come baseline un profilo DNS fixed public-safe, adatto a test, golden e handoff senza esporre valori operativi concreti.

Il punto unico di accesso versionato al profilo attivo è `src/dns_zone_bootstrapper/templates/profile_resolver.py`. Il layer applicativo non conosce direttamente né `local/` né sorgenti esterne di profilo, ma consuma solo `resolve_active_fixed_dns_profile()`.

Il contratto runtime osservato è ora questo:

- il resolver prova prima un path esplicito da variabile d'ambiente `DNS_ZONE_PROFILE_PATH`;
- se il path esplicito non è configurato, prova l'import standard di `local.dns_zone_profile`;
- se il boundary `local` non è risolvibile come package runtime, prova il caricamento esplicito del file `./local/dns_zone_profile.py` rispetto alla current working tree;
- se anche il file locale non è disponibile, ricade sul profilo versionato `PUBLIC_SAFE_FIXED_DNS_PROFILE`.

Questa struttura implica che:

- il profilo public-safe resta la baseline canonica versionata;
- esiste ora un primo meccanismo esplicito, distribuito e documentabile per fornire al runtime un profilo fixed concreto;
- `local/` resta un boundary locale opzionale, gitignored, non pacchettizzato e non più necessario come unico canale implicito per i valori concreti;
- CLI, Web UI e use case applicativo restano disaccoppiati dal dettaglio implementativo della sorgente concreta del profilo.

Nel runtime osservato, il file prodotto dal generatore attraverso questo boundary è stato importato con successo in Cloudflare quando la zona target era pulita. Un primo failure sul record `www` è stato attribuito a collisioni con record preesistenti nella zona di laboratorio, non al formato del file generato.

### 5.1 Decisione progettuale congelata sul ruolo di `local/`

Lo stato AS-IS del repository supporta ancora un fallback runtime opzionale tramite `local/`, utile per retrocompatibilità tecnica e per non interrompere il workspace locale già esistente.

Tuttavia, in assenza di nuovi vincoli esterni e coerentemente con il contratto funzionale del prodotto chiarito in discovery, viene congelata una decisione progettuale più forte: il target finale del software resta un prodotto a input unico (`dominio`) che applica automaticamente un template fixed canonico.

Ne consegue che:

- `local/` non va considerato parte del contratto utente finale;
- `local/` rappresenta un fallback tecnico transitorio/back-compat dell’AS-IS;
- `DNS_ZONE_PROFILE_PATH` costituisce il primo meccanismo esplicito e documentabile per caricare il profilo fixed concreto senza dipendere da un override implicito gitignored;
- la baseline public-safe versionata resta utile come superficie sicura per test, handoff e condivisione del repository;
- il blocco `D8` può considerarsi sostanzialmente chiuso sul piano tecnico, perché il prodotto non dipende più in modo ambiguo dal solo boundary `local/` per ricevere i valori fixed concreti.

### 6. Packaging Docker minimale e boundary del contesto build

Il repository dispone ora di una prima baseline containerizzata valida, introdotta tramite `Dockerfile` multi-stage e `.dockerignore`.

Il comportamento architetturale osservato è questo:

- il `Dockerfile` copia solo `pyproject.toml`, `README.md` e `src/`;
- il package viene installato dentro l'immagine a partire dagli asset versionati;
- il runtime espone la demo FastAPI tramite `uvicorn` sulla porta `8000`;
- il processo applicativo gira come utente non-root `appuser`.

Il `.dockerignore` esclude dal build context aree non necessarie al runtime containerizzato, tra cui:

- ambienti virtuali;
- cache e artefatti di coverage/test;
- `tmp/`;
- `docs/`;
- `tests/`;
- `local/`;
- file locali di supporto non necessari alla demo runtime.

Ne deriva un contratto importante:

- la prima immagine Docker validata è riproducibile e public-safe;
- il container non dipende da asset locali gitignored;
- il boundary `local/` non entra automaticamente nell'immagine;
- l'endpoint `/generate` nel container usa quindi il profilo versionato `PUBLIC_SAFE_FIXED_DNS_PROFILE`.

Questo significa che la containerizzazione attuale valida la portabilità della demo web, ma non replica automaticamente il comportamento locale con valori concreti presenti in `local/`. Un eventuale supporto futuro ai valori locali concreti nel container dovrà essere introdotto con un meccanismo esplicito e documentato, non implicito.

## Macro-struttura del repository

```text
src/dns_zone_bootstrapper/
├─ application/   orchestration use cases
├─ domain/        models, rules, validators
├─ interfaces/    web adapter + technical support surfaces
├─ renderers/     bind/zone rendering
└─ templates/     fixed profile definitions and loaders
```

## Decisioni congelate

* stack iniziale: Python-first;
* deliverable principale v1: pagina web;
* input utente v1: solo dominio;
* valori restanti del template: fissi per ora;
* nessuna preview nella v1;
* core riusabile prima delle interfacce ricche;
* nessuna migrazione di stack necessaria per la v1.

## Decisioni rimandate

* eventuali campi variabili aggiuntivi;
* struttura finale di più profili/template;
* eventuale persistenza;
* eventuale autenticazione;
* eventuale preview del file;
* eventuale frontend React/TypeScript separato;
* eventuale backend enterprise aggiuntivo;
* eventuale integrazione diretta con Cloudflare API.
