# DNS Zone Bootstrapper

Strumento Python-first per generare, a partire da un solo dominio in input, un file di zona DNS in formato BIND pronto per il workflow di import su Cloudflare, applicando un template DNS fisso derivato da un caso reale di riferimento.

## Cos'è

Questo progetto nasce per trasformare un'operazione DNS ripetitiva e soggetta a errori manuali in un flusso deterministico, semplice e riusabile:

- input minimo: un dominio apex;
- logica applicativa: applicazione di un profilo DNS fixed;
- output: file `.txt` in formato BIND orientato all'import su Cloudflare;
- superficie principale della v1: pagina web minimale.

Il focus iniziale è uno scenario coerente con un template aziendale fisso e con record utili a un contesto mail-oriented.

## Perché esiste

L'obiettivo pratico della v1 è ridurre:

- copia/incolla manuali sui record DNS;
- errori di trascrizione;
- variabilità operativa tra configurazioni simili;
- tempo necessario per preparare una zona importabile.

Invece di ricostruire ogni volta i record a mano, il sistema genera un artefatto DNS coerente con un template fisso, mantenendo variabile soltanto il dominio.

## Stato attuale

La v1 è già funzionante nella sostanza del caso d'uso richiesto:

- accetta un solo input utente: il dominio;
- genera un file `.txt` BIND import-ready;
- espone una demo web minimale con generazione e download diretto;
- è stata validata empiricamente con import Cloudflare riuscito su una zona pulita;
- mantiene il repository versionato in forma public-safe;
- conserva la possibilità di usare valori fixed concreti tramite override locale gitignored.

Snapshot tecnico corrente verificato:

- `python run_quality_gates.py` → `pytest 83 passed`, `pylint 10.00/10`, `coverage 230 stmt`, `0 miss`, `100%`

## Workflow end-to-end

Il flusso reale della v1 è il seguente:

1. l'utente inserisce un dominio apex nella pagina web;
2. il sistema valida sintatticamente l'input;
3. il runtime risolve il profilo DNS fixed attivo;
4. il renderer produce il file di zona in formato BIND;
5. la web app restituisce il file `.txt` come download diretto;
6. il file viene importato in Cloudflare.

In laboratorio Cloudflare questo workflow è stato verificato con successo su una zona pulita.

## Lessico minimo

### Dominio apex
È il dominio radice della zona, ad esempio `example.com`.
Non è un sottodominio come `www.example.com`.

### Zone file BIND
È un file testuale che descrive record DNS in un formato standard storicamente associato a BIND.
In questo progetto è il formato usato come artefatto di output.

### Import Cloudflare
Cloudflare consente di importare record DNS a partire da un file di zona.
La v1 genera proprio un file orientato a questo workflow.

### Profilo DNS fixed
È il set di record e valori che il sistema applica automaticamente al dominio in input.
Nella v1 il profilo è fisso: cambia il dominio, non cambia la struttura del template.

## Cosa fa la v1

La prima versione fa in modo esplicito e intenzionale queste cose:

- valida il dominio apex come input minimo;
- applica un template DNS fixed derivato dal caso reale;
- genera il file di zona in formato BIND;
- restituisce un `.txt` pronto per il workflow di import su Cloudflare;
- espone il flusso tramite una pagina web minimale;
- mantiene il core Python riusabile e separato dalle interfacce.

## Cosa non fa ancora

La v1 non fa ancora, per scelta di scope, le seguenti cose:

- non gestisce profili multipli;
- non espone campi variabili aggiuntivi oltre al dominio;
- non offre preview del file prima del download;
- non integra direttamente le API Cloudflare;
- non supporta automaticamente nel runtime Docker il boundary gitignored `local/`: la baseline containerizzata validata resta public-safe e usa di default il profilo versionato;
- non replica integralmente l'export Cloudflare originale;
- non include il record `SOA` nel perimetro runtime della v1.

Questa è una scelta deliberata: il focus è generare il sottoinsieme utile e importabile, non riprodurre tutto l'export sorgente.

## Public-safe versionato vs override locale gitignored

Il repository distingue in modo intenzionale tra baseline versionata e valori concreti locali.

### Baseline versionata public-safe
Il progetto versiona un profilo fixed public-safe, utile per:

- test automatici;
- golden file;
- handoff;
- condivisione del repository senza esporre valori operativi sensibili.

### Override locale gitignored
Quando serve usare valori concreti reali in locale, il runtime può risolvere un override gitignored esterno al package versionato.

- modulo logico atteso: `local.dns_zone_profile`
- file locale supportato: `./local/dns_zone_profile.py` rispetto alla current working tree
- simbolo atteso: `ACTIVE_FIXED_DNS_PROFILE`

Il comportamento runtime è questo:

- il boundary applicativo chiama solo `resolve_active_fixed_dns_profile()`;
- il resolver prova prima l'import standard di `local.dns_zone_profile`;
- se il top-level package `local` non è risolvibile, prova il caricamento esplicito del file `./local/dns_zone_profile.py` rispetto alla current working tree;
- se anche il file locale non esiste, il sistema usa `PUBLIC_SAFE_FIXED_DNS_PROFILE`.

In questo modo il repository resta public-safe e versionabile, mentre il runtime locale può usare valori fixed concreti non versionati senza far entrare `local/` nel package installato.

## Note operative su Cloudflare

La validazione empirica ha chiarito due punti importanti:

- il file generato è importabile correttamente su una zona Cloudflare pulita;
- un eventuale errore su record come `www` può dipendere da collisioni con record già presenti nella zona target e non dal generatore.

Quindi, se l'import fallisce su una zona già popolata, bisogna distinguere tra:

- problema del file generato;
- conflitto ambientale nella zona Cloudflare di destinazione.

## Avvio rapido

### Requisiti minimi

- Python `>= 3.11`
- ambiente virtuale locale consigliato

### Bootstrap locale

```bash
python -m pip install -e ".[dev]"
python run_quality_gates.py
dns-zone-cli doctor
```

### Avvio demo web

```bash
dns-zone-cli web
```

La demo viene avviata localmente su:

```text
http://127.0.0.1:8000
```

Alternativa tecnica equivalente:

```bash
python -m uvicorn dns_zone_bootstrapper.interfaces.web.app:app --reload
```

## Esecuzione Docker minima

Baseline validata empiricamente del packaging containerizzato:

```bash
docker build -t dns-zone-bootstrapper:local .
docker run --rm -p 8000:8000 dns-zone-bootstrapper:local
```

Contratto osservato della prima immagine Docker validata:

* il container espone correttamente la demo su `http://127.0.0.1:8000`;
* `GET /` restituisce `200 OK`;
* `GET /generate?domain=testdomain.com` restituisce `200 OK`;
* l'output nel container usa il profilo public-safe versionato e quindi mostra placeholder `__FIXED_*__`;
* questo comportamento è atteso, perché `.dockerignore` esclude `local/` e il `Dockerfile` copia solo gli asset versionati minimi necessari al runtime.

Questa validazione Docker chiude la baseline minima containerizzata public-safe della demo web: build reale, avvio del container e smoke runtime risultano verificati. L’eventuale supporto futuro ai valori fixed concreti locali nel container richiederà un meccanismo esplicito e documentato e non fa parte della chiusura attuale.

## Uso della demo

La demo web v1 è volutamente minimale:

1. avvia il server locale;
2. apri la pagina nel browser;
3. inserisci il dominio apex;
4. genera il file;
5. scarica il `.txt`;
6. importa il file in Cloudflare.

Il comportamento atteso è lineare e con poche interazioni, in coerenza con la richiesta iniziale.

## Struttura del repository

```text
docs/                          documenti owner
src/dns_zone_bootstrapper/     codice applicativo
tests/                         test automatici e fixture golden
```

Macro-struttura interna del package:

```text
src/dns_zone_bootstrapper/
├─ application/   use case e orchestrazione
├─ domain/        modelli, regole, validazioni
├─ interfaces/    web adapter e superfici tecniche
├─ renderers/     rendering del zone file BIND
└─ templates/     profili DNS fixed e risoluzione runtime
```

## Direzione architetturale

Le decisioni architetturali principali attualmente congelate sono:

* core Python-first e framework-agnostic;
* logica applicativa separata dalla pagina web;
* pagina web come superficie principale della v1;
* CLI mantenuta come supporto tecnico;
* renderer BIND separato e testabile;
* boundary dedicato per la risoluzione runtime del profilo fixed;
* repository public-safe per default, con override locale solo fuori versionamento.

## Stato di chiusura attuale

Il repository si considera stabile e difendibile come baseline v1 public-safe: demo web, core applicativo, validazione empirica Cloudflare, quality gates e baseline Docker minimale risultano consolidati.

Non si considera però ancora chiusa, senza ulteriori riallineamenti, la forma finale del prodotto autonomo. Allo stato attuale il repository versionato mantiene un profilo public-safe e supporta ancora il boundary `local/` come override runtime opzionale per valori fixed concreti.

Decisione progettuale congelata: il target finale del prodotto resta un workflow a input unico (`dominio`) con template fixed canonico applicato automaticamente dal software. In questa prospettiva `local/` non va considerato parte del contratto utente finale, ma un boundary tecnico transitorio dell'AS-IS, da superare o riclassificare in modo esplicito con un successivo blocco conservativo.

Restano quindi backlog ed extra non bloccanti su UI/UX, cleanup ergonomico e possibili estensioni future del prodotto, ma prima dell’audit strutturale largo del repository resta aperto il chiarimento/assestamento definitivo del profilo fixed concreto.

## Evoluzioni future possibili

Le estensioni future possibili, ma non necessarie per la v1, includono:

* profili DNS multipli;
* campi variabili aggiuntivi;
* preview opzionale del file;
* miglioramenti UI/UX;
* Docker/exportability;
* integrazione assistita o diretta con Cloudflare.
