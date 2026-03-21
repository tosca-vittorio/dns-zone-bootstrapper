# TIMELINE

## Stato corrente del progetto

- Repo: `dns-zone-bootstrapper`
- Branch operativo: `development`
- Fase corrente: freeze documentale post-clarifica requisiti + preparazione avvio del core
- Baseline contrattuale v1: confermata con l'azienda
- Obiettivo immediato: chiudere l'allineamento dei documenti owner e preparare l'avvio di `B0` e `B1`

## Legenda stati

- ✅ completato
- 🟡 in corso / parziale
- ⬜ non avviato
- ⛔ bloccato da dipendenza esterna

---

## Cycle A — Discovery, baseline e design

### A0 — Bootstrap repository e owner docs — ✅
**Obiettivo**  
Creare baseline del repository, package Python, owner docs e superfici tecniche minime.

**DoD minima**
- `pyproject.toml`, `README.md` e `.gitignore` presenti;
- package Python bootstrap presente;
- entrypoint tecnici presenti e verificati;
- `TIMELINE.md`, `ROADMAP.md`, `ARCHITECTURE.md` e `CHANGELOG.md` inizializzati;
- bootstrap locale verificato con evidenze minime;
- timeline usata come documento operativo centrale, senza dipendere da un backlog separato.

**Stato operativo**
- branch `development` attivo e confermato;
- baseline Python-first impostata;
- package `src/` presente;
- entrypoint CLI e web presenti e verificati;
- owner docs inizializzati;
- `requirements.txt` rigenerato da `.venv` locale pulita come freeze operativo versionato, da aggiornare in modo opportuno ai checkpoint significativi dell'ambiente e non a ogni micro-variazione locale;
- file reale di riferimento ricollocato localmente in area privata gitignored (`samples/private/company_reference/testdomain.com.txt`);
- `README.md` riallineato in italiano;
- quality gate `pytest` verde;
- quality gate `pylint` verificato ed eseguito con esito verde sul bootstrap corrente (`src` e `tests` entrambi `10.00/10`).

**Evidenze correnti**
- `pytest -q` → `4 passed`;
- `python -m pylint src` → `10.00/10`;
- `python -m pylint tests` → `10.00/10`;
- `dns-zone-cli doctor` → `dns-zone-bootstrapper: CLI bootstrap OK`;
- bootstrap tecnico e documentale consolidato nei commit `64278ee` e `a0787f4`, entrambi già pubblicati su `origin/development`;
- `requirements.txt` presente localmente come parte del freeze effettuato;
- artefatto reale di riferimento fornito dall'azienda ricollocato localmente in `samples/private/company_reference/testdomain.com.txt`.
- baseline dev verificata in `.venv` locale isolata (`python -m venv .venv`, install `-e ".[dev]"`, gate verdi);

**Nota di chiusura A0**
- bootstrap repository, owner docs, baseline dev isolata e freeze operativo risultano verificati e consolidati a commit;
- `A0` è chiuso anche a livello Git/remoto e il progetto può proseguire su `B0`.

### A1 — Discovery vincoli Cloudflare + mailcow — ✅
**Obiettivo**  
Formalizzare i vincoli del problema e separare ciò che è confermato da ciò che resta eventualmente evolutivo.

**Fatti confermati**
- il file ricevuto va considerato come template di riferimento da generalizzare;
- l'unico input previsto per la v1 è il dominio;
- tutti gli altri valori sono fissi per ora;
- il file generato non deve replicare integralmente la forma dell'export, ma deve essere pronto per l'import su Cloudflare;
- la preview non è necessaria nella v1;
- la pagina web è il deliverable principale per comodità d'uso;
- non esiste una preferenza di stack imposta dall'azienda.

**Stato operativo**
- la discovery funzionale della v1 è sufficientemente chiusa;
- non è necessario rivalutare lo stack per la v1;
- il progetto può procedere su impostazione Python-first con consegna web-first.

### A2 — Setup laboratorio Cloudflare free + prove import/export — ⬜
**Obiettivo**  
Creare un ambiente di verifica reale per:
- import manuale di zone file;
- export di zone file di riferimento;
- raccolta di fixture golden da usare nei test.

**Attivazione prevista**
- creazione account Cloudflare gratuito di laboratorio;
- uso di un dominio di test non produttivo;
- prove di import/export per ottenere evidenze reali e fixture confrontabili.

**Output attesi**
- almeno un import riuscito di zone file;
- almeno un export Cloudflare usabile come riferimento;
- prime note operative sui vincoli reali del formato.

### A3 — Acquisizione e normalizzazione file di esempio aziendale — ✅
**Obiettivo**  
Ricevere il file reale, assumerlo come template di riferimento e trasformarlo nella baseline contrattuale della v1.

**Stato operativo**
- file reale ricevuto;
- template assunto come riferimento da generalizzare;
- chiarite con l'azienda le regole della v1:
  - input unico = dominio;
  - valori restanti fissi per ora;
  - output solo pronto per import;
  - nessuna preview;
  - pagina web come deliverable principale.

**Nota**
La derivazione tecnica campo-per-campo del template viene demandata al `Cycle B`, perché appartiene al lavoro sul core e non più alla sola discovery.

---

## Cycle B — Core engine

### B0 — Validazione dominio apex — 🟡
**Obiettivo**  
Implementare la prima validazione forte sull'input minimo certo del sistema: il dominio apex.

**DoD minima**
- presenza di un validatore dedicato;
- distinzione chiara tra input valido e input non valido;
- test automatici minimi sui casi base;
- nessuna dipendenza dalla UI o dalla web app per la logica di validazione.

**Primo lavoro previsto**
- introdurre il validatore di dominio apex;
- definire i primi casi validi/non validi;
- collegare il validatore a un use case applicativo minimo ma framework-agnostic.

**Stato operativo**
- introdotto un primo validatore sintattico del dominio apex candidate in modulo domain dedicato;
- coperti casi minimi di input valido e non valido tramite test automatici;
- questa prima iterazione valida solo la forma sintattica DNS/hostname dell'input e non risolve ancora public suffix o registrable domain reali.

**Evidenze correnti**
- `pytest -q` → `14 passed`;
- `python -m pylint src tests` → `10.00/10`;
- aggiunti `src/dns_zone_bootstrapper/domain/domain_validation.py` e `tests/test_domain_validation.py`.

### B1 — Modello record DNS e profilo template fisso — ⬜
**Obiettivo**  
Definire la rappresentazione logica minima del template DNS fisso derivato dal file reale di riferimento.

**Primo lavoro previsto**
- separare ciò che deriva dal dominio da ciò che resta fisso;
- introdurre una struttura dati iniziale per il profilo;
- mantenere il template fuori dalla web app;
- preparare il terreno per eventuali futuri campi variabili.

### B2 — Renderer BIND zone file — ⬜
**Obiettivo**  
Produrre il renderer del file di zona in formato coerente con l'import Cloudflare.

**Primo lavoro previsto**
- introdurre una funzione o servizio di rendering separato;
- mantenere il rendering indipendente dall'interfaccia;
- preparare test confrontabili sul testo generato.

### B3 — Test del generatore e preparazione fixture reali — ⬜
**Obiettivo**  
Proteggere il comportamento del generatore tramite test automatici e preparare l'ingresso di fixture reali.

**Dipendenze**
- file reale di riferimento già acquisito;
- eventuale laboratorio Cloudflare per export/import di verifica.

---

## Cycle C — Delivery surfaces

### C0 — Pagina web minimale — ⬜
**Obiettivo**  
Esporre il core tramite una pagina web minimale coerente con la richiesta aziendale.

**Vincoli della v1**
- una sola pagina;
- una sola interazione principale;
- nessuna preview obbligatoria;
- meno interazioni possibili.

### C1 — Generazione e download del file — ⬜
**Obiettivo**  
Permettere l'inserimento del dominio e il download diretto del file `.txt` generato.

### C2 — Rifinitura demo web e packaging minimo — ⬜
**Obiettivo**  
Preparare una demo semplice, pulita e usabile per la consegna.

---

## Cycle D — Hardening

### D0 — Gestione edge case e validazioni — ⬜
**Obiettivo**  
Coprire casi limite, input errati e incoerenze del template.

### D1 — Allineamento owner docs — ⬜
**Obiettivo**  
Consolidare e riallineare i documenti owner quando i blocchi tecnici saranno maturi.

### D2 — Packaging/demo finale — ⬜
**Obiettivo**  
Preparare una demo presentabile, riproducibile e difendibile.

### D3 — Eventuale import diretto via API come extra — ⬜
**Obiettivo**  
Valutare come estensione futura l'import assistito o diretto verso Cloudflare.
