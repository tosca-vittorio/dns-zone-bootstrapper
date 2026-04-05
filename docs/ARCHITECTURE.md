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

Il punto unico di accesso versionato al profilo attivo è `src/dns_zone_bootstrapper/templates/profile_resolver.py`. Il layer applicativo non conosce direttamente `local/`, ma consuma solo `resolve_active_fixed_dns_profile()`.

Il contratto runtime osservato è questo:

- il resolver prova prima l'import standard di `local.dns_zone_profile`;
- se il boundary `local` non è risolvibile come package runtime, prova il caricamento esplicito del file `./local/dns_zone_profile.py` rispetto alla current working tree;
- se anche il file locale non è disponibile, ricade sul profilo versionato `PUBLIC_SAFE_FIXED_DNS_PROFILE`.

Questa struttura implica che:

- `local/` è un boundary locale opzionale, gitignored e non pacchettizzato;
- il profilo public-safe resta la baseline canonica versionata;
- i valori concreti locali restano fuori dalla storia Git;
- CLI, Web UI e use case applicativo restano disaccoppiati dal dettaglio implementativo dell'override locale.

Nel runtime osservato, il file prodotto dal generatore attraverso questo boundary è stato importato con successo in Cloudflare quando la zona target era pulita. Un primo failure sul record `www` è stato attribuito a collisioni con record preesistenti nella zona di laboratorio, non al formato del file generato.

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
