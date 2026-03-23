# TIMELINE

## Stato corrente del progetto

- Repo: `dns-zone-bootstrapper`
- Branch operativo: `development`
- Fase corrente: `B1` chiuso e consolidato come baseline code-only del profilo DNS fisso public-safe, semanticamente allineata al template reale, irrigidita da freeze test su contratto e superfici principali e formalizzata nel model layer su vocabolari chiusi e metadata espliciti del `rdata`; `B2` aperto con renderer BIND minimale già verificato da test dedicato e quality gates globali, poi irrigidito con golden file public-safe esterno, con test esplicito sulla resa dei placeholder derivati, esteso con un primo boundary `application` framework-agnostic per la generazione del file di zona a partire dallo zone apex input, ulteriormente consolidato con hardening test-side condiviso tra renderer puro e use case applicativo end-to-end e con copertura applicativa aggiuntiva dei failure path `domain_too_long`, `empty_input`, `missing_dot` e `leading_dot` nel generatore BIND
- Baseline contrattuale v1: confermata con l'azienda
- Obiettivo immediato: proseguire con estensioni controllate della copertura del generatore nel core, mantenendo separati application, renderer, web/UI e refactor larghi

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

### B0 — Validazione dominio apex — ✅
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
- introdotto un primo use case applicativo minimale framework-agnostic che consuma il validatore domain e restituisce un esito strutturato semplice;
- questa iterazione valida ancora solo la forma sintattica DNS/hostname dell'input e non risolve public suffix o registrable domain reali.
- il layer `domain` espone ora anche un risultato strutturato con `error_code` deterministici per i principali failure mode sintattici, propagati dal layer `application`;

**Evidenze correnti**
- `pytest -q` → `26 passed`;
- `python -m pylint src tests` → `10.00/10`;
- aggiunti `src/dns_zone_bootstrapper/domain/domain_validation.py` e `tests/test_domain_validation.py`;
- aggiunti `src/dns_zone_bootstrapper/application/zone_apex_validation.py` e `tests/test_zone_apex_validation_use_case.py`;
- coperti esplicitamente anche i failure mode `non_string_input` e `domain_too_long` nei test del layer `domain`;
- avanzamento reale di `B0` consolidato nei commit `9670323`, `18141f5`, `f5f579d` e `4771e11`.

**Nota di chiusura B0**
- la DoD minima del blocco risulta soddisfatta sul repository reale;
- la validazione del dominio apex è ora coperta da layer `domain`, use case `application`, errori strutturati deterministici e test espliciti sui principali failure mode sintattici;
- `B0` si considera chiuso come blocco di validazione sintattica framework-agnostic, mentre tutto ciò che riguarda template DNS, record profile e rendering resta demandato ai blocchi successivi.

### B1 — Modello record DNS e profilo template fisso — ✅
**Obiettivo**
Definire la rappresentazione logica minima del template DNS fisso derivato dal file reale di riferimento.

**Stato operativo**
- introdotti data model versionabili per record template e profilo DNS fisso nel package `templates`;
- introdotto un primo profilo `public_safe_candidate` sanificato e versionabile, coerente con la struttura del template reale ma privo di valori operativi privati;
- mantenuta la separazione tra placeholder derivati dal dominio (`{apex_fqdn}`, `{apex_slug}`) e valori fissi candidati;
- escluso lo `SOA` dalla baseline `B1` e mantenuta fuori dal runtime la dipendenza dagli snapshot privati locali;
- riallineato semanticamente il naming dei selector DKIM e del record TXT token-like al template reale, mantenendo invariata la sanitizzazione public-safe;
- aggiunto un test dedicato che verifica shape minima, assenza di `SOA` e presenza dei placeholder derivati.
- aggiunto un test esplicito che congela inventario record, ordine corrente, flag `cf_proxied` e unicità del record TXT con `manual_flag`.
- aggiunto un test esplicito che congela la superficie placeholder ammessa nel profilo corrente, verificando la presenza controllata di `{apex_slug}` e `{apex_fqdn}` e l'assenza di `{apex}` nei `rdata_template`.
- aggiunto un test esplicito che congela la superficie `rdata_template` fixed-only non derivata dal dominio, proteggendo i valori fissi correnti del profilo public-safe.
- aggiunto un restringimento esplicito del model layer: `record_class` è ora tipizzato come `Literal["IN"]` e `manual_flag` come `Literal["token_like_value"]`, allineando il modello agli invarianti già presenti nel profilo corrente e già difesi dai test.
- formalizzata la semantica del `rdata` nel model layer tramite un value object dedicato, separando in modo esplicito `kind` e `template` senza lasciare la derivazione implicita nella sola stringa del `rdata_template`.

**Evidenze correnti**
- `pytest -q` → `33 passed`;
- `python -m pylint src tests` → `10.00/10`;
- aggiunti `src/dns_zone_bootstrapper/templates/profile_model.py`, `src/dns_zone_bootstrapper/templates/profiles/public_safe_candidate.py` e `tests/test_public_safe_candidate_profile.py`;
- baseline `B1` consolidata nel commit `cf943e6`;
- riallineamento semantico minimale del profilo consolidato nel commit `43c3c3b`.
- freeze contrattuale del profilo consolidato nel commit `87a1e67`.
- freeze della superficie placeholder consolidato nel commit `c4a31b6`.
- freeze della superficie fixed-only `rdata_template` consolidato nel commit `532487a`.
- restringimento del vocabolario del model layer consolidato nel commit `afdf577`.
- formalizzazione semantica del `rdata` consolidata nel commit `1411bea`.

**Nota di chiusura B1**
- la DoD sostanziale del blocco risulta soddisfatta sul repository reale;
- il profilo `public_safe_candidate` costituisce ora una baseline runtime versionabile, public-safe, indipendente dagli asset privati locali e semanticamente allineata al template reale di riferimento;
- il contratto del profilo è difeso da test espliciti su shape minima, inventario, ordine, flag, superficie placeholder ammessa, superficie fixed-only dei `rdata_template` e semantica del `rdata`;
- il model layer esprime ora in modo più rigoroso sia i vocabolari chiusi sia i metadata semantici del `rdata`, riducendo la dipendenza da logica implicita prima dell’apertura del renderer;
- `B1` si considera chiuso; il passo successivo corretto è `B2`, dedicato al renderer BIND e ai primi test sul testo generato.

### B2 — Renderer BIND zone file — 🟡
**Obiettivo**
Produrre il renderer del file di zona in formato coerente con l'import Cloudflare.

**Stato operativo**
- introdotto `src/dns_zone_bootstrapper/renderers/bind_zone_renderer.py` con una funzione pura `render_bind_zone_file(zone_apex, profile)` separata dalle interfacce;
- implementate nel renderer minimo le regole iniziali di risoluzione owner FQDN, placeholder `{apex}`, `{apex_fqdn}`, `{apex_slug}`, quoting dei record `TXT`, annotazioni `cf_tags` e raggruppamento per tipo record;
- aggiunto `tests/test_bind_zone_renderer.py` con contratto testuale esplicito sul profilo `PUBLIC_SAFE_FIXED_DNS_PROFILE`;
- esternalizzato l'expected public-safe del renderer in `tests/golden/public_safe_candidate.bind.txt`, rendendo il confronto testuale più auditabile e manutenibile;
- aggiunto un test esplicito che congela la resa dei placeholder derivati su un apex diverso dal golden corrente, verificando `apex_slug`, `apex_fqdn` e l'assenza di newline finale;
- introdotto `src/dns_zone_bootstrapper/application/bind_zone_generation.py` con il use case `generate_bind_zone_file(input_value)`, che valida l'input apex, usa il profilo fisso `PUBLIC_SAFE_FIXED_DNS_PROFILE`, orchestra il renderer BIND e restituisce un esito strutturato con `zone_file_text` sul percorso di successo;
- aggiunto `tests/test_bind_zone_generation_use_case.py` con copertura esplicita del percorso applicativo di successo sul golden public-safe e del failure path con propagazione dell'`error_code` e assenza di testo renderizzato;
- aggiunto un test end-to-end su apex valido non-golden (`alpha-zone.example.org`) nel layer `application`, verificando che il generatore produca lo stesso contratto derivato già congelato nel renderer puro;
- estratto `tests/shared_bind_zone_assertions.py` come helper test-side condiviso, riusato da `tests/test_bind_zone_renderer.py` e `tests/test_bind_zone_generation_use_case.py` per evitare duplicazione letterale delle assertion e mantenere allineato il contratto verificato attraverso i due percorsi del core;
- verificate assenza di regressioni e qualità globale con `python -m pytest -q` → `42 passed` e `python -m pylint src tests` → `10.00/10`;
- estesa la copertura del use case `generate_bind_zone_file` con un failure path sintattico aggiuntivo su apex overlong, verificando la propagazione di `error_code="domain_too_long"` e l'assenza di testo renderizzato;
- estesa ulteriormente la copertura del use case `generate_bind_zone_file` con un failure path sintattico aggiuntivo su input vuoto, verificando la propagazione di `error_code="empty_input"` e l'assenza di testo renderizzato;
- estesa ulteriormente la copertura del use case `generate_bind_zone_file` con un failure path sintattico aggiuntivo su apex privo di dot, verificando la propagazione di `error_code="missing_dot"` e l'assenza di testo renderizzato;
- estesa ulteriormente la copertura del use case `generate_bind_zone_file` con un failure path sintattico aggiuntivo su apex con dot iniziale, verificando la propagazione di `error_code="leading_dot"` e l'assenza di testo renderizzato;
- avanzamento tecnico consolidato nei commit `641065e`, `514f278`, `43d7d37`, `2898fbb`, `6742c0e`, `97d3e83`, `ebe3221`, `558c533` ed `ef25219`.

**Nota di stato B2**
- il blocco non è ancora chiuso, perché pur esistendo ora sia il renderer minimo sia un primo boundary `application` con copertura estesa anche ai failure path sintattici `domain_too_long`, `empty_input`, `missing_dot` e `leading_dot`, mancano ancora ulteriori estensioni controllate della copertura, confronti più realistici e integrazioni verso superfici esterne;
- `B2` non è più da considerare solo un blocco di rendering isolato: esiste ora un primo contratto framework-agnostic end-to-end nel core, che parte dallo zone apex input, valida l'input e produce il testo BIND usando il profilo fisso public-safe, con resa derivata su apex non-golden difesa in modo coerente sia nel renderer sia nel use case applicativo tramite assertion condivise nel solo layer test;
- il prossimo passo corretto resta l'hardening controllato del generatore nel core, senza aprire nello stesso blocco scope su UI/web o refactor larghi.

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
