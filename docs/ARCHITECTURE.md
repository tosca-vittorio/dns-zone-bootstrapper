# ARCHITECTURE

## Scopo

Il progetto nasce per generare, a partire da un dominio in input, un file di zona DNS in formato BIND pronto per l'import su Cloudflare, usando come base un template DNS fisso derivato da un file reale di riferimento fornito dall'azienda, con focus iniziale su uno scenario coerente con mailcow.

## Vincoli attuali

- il file reale di riferimento è stato acquisito;
- la v1 prevede un solo input utente: il dominio;
- tutti gli altri valori del template sono fissi per ora;
- il file generato deve essere pronto per l'import su Cloudflare, senza necessità di replicare tutta la forma dell'export originale;
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

Per il runtime di generazione, la scelta del profilo attivo avviene tramite un boundary dedicato di risoluzione:

- se esiste un modulo locale gitignored `local.dns_zone_profile` con `ACTIVE_FIXED_DNS_PROFILE`, il generatore usa quel profilo;
- se il modulo locale non esiste, il runtime ricade sul profilo versionato `PUBLIC_SAFE_FIXED_DNS_PROFILE`.

Questa scelta permette di:

- mantenere il repository public-safe e versionabile;
- evitare hardcode diretto del runtime su un solo profilo placeholderizzato;
- introdurre valori fixed concreti solo in area locale/non versionata;
- preservare la separazione tra core applicativo, definizione del profilo e superficie web.

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
