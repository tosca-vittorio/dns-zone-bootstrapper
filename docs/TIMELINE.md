# TIMELINE

## Stato corrente del progetto

- Repo: `dns-zone-bootstrapper`
- Branch operativo: `development`
- Fase corrente: `A2`, `B1`, `B2`, `B3`, `B4`, `C0`, `C1` e `C2` chiusi e consolidati; blocco `Post-A2 / Post-C2` aperto in stato `🟡`; nessun blocco `D*` è stato ancora avviato.
- Baseline contrattuale v1: confermata con l'azienda
- Validazione empirica Cloudflare: import del file generato riuscito su zona pulita; primo failure su `www` ricondotto a collisione con record preesistenti nella zona target.
- Obiettivo immediato: avviare il primo micro-step del blocco documentale essenziale, partendo dal rafforzamento del `README.md` come documento di ingresso al prodotto, senza aprire ancora polish UI, Docker o hardening `D*` non prioritari.
- Valutazione congelata dello stato v1: il prodotto è coerente con la richiesta ricevuta, funziona nella sostanza della v1, il workflow `dominio -> file .txt -> import Cloudflare` è stato validato empiricamente e il lavoro svolto è da considerare positivo e tecnicamente difendibile.
- Gap principale congelato: il limite residuo non è il core applicativo ma la comprensibilità del prodotto per lettori/utenti terzi; il prossimo avanzamento corretto riguarda quindi chiarimento di contesto, utilità, workflow, lessico tecnico, perimetro v1, limiti e modalità d'uso.
- Regola documentale congelata: gli owner docs esistenti restano sufficienti come struttura di governo (`TIMELINE`, `CHANGELOG`, `ARCHITECTURE`, `ROADMAP`); il rafforzamento deve avvenire prima di tutto tramite ampliamento del `README.md` e, solo se realmente utile, tramite documenti di supporto non-owner dedicati alla guida utente o al deployment.
- Finestra di comunicazione verso l'azienda congelata: l'avviso/report di stato con demo v1 è considerato opportuno dopo la chiusura del blocco documentale essenziale, non dopo UI polish, CSS o Docker; questi restano incrementi successivi non bloccanti per la prima consegna.
- Sequenza prioritaria congelata post-validazione empirica:
  1. rafforzamento del `README.md` come documento di ingresso al prodotto;
  2. chiarimento architetturale e concettuale nei documenti owner già esistenti, dove necessario;
  3. introduzione di una guida d'uso dedicata per utente/demo/import Cloudflare, solo se il README non basta da solo;
  4. preparazione del testo/report di aggiornamento verso l'azienda con stato, demo e limiti attuali;
  5. audit conservativo di UI minimale difendibile;
  6. valutazione Docker/exportability come step successivo e non bloccante.
- Ultimo consolidamento post-validazione empirica: la suite `application` è ora isolata dal profilo locale gitignored tramite fixture autouse che forza `PUBLIC_SAFE_FIXED_DNS_PROFILE` nei test applicativi, eliminando il falso rosso osservato quando `local.dns_zone_profile` era presente nel workspace; hardening consolidato nel commit `4681df0` (`test(application): isolate public-safe runtime profile in application suite`) con quality gates globali verdi (`python -m pytest -q` → `78 passed`, `python -m pylint src tests` → `10.00/10`) su branch allineato a `origin/development`.
- Ultimo consolidamento `B4`: boundary runtime del profilo fisso consolidato nel commit `98ef332` (`feat(templates): add runtime fixed profile resolver`), con introduzione di `src/dns_zone_bootstrapper/templates/profile_resolver.py`, disaccoppiamento di `generate_bind_zone_file(...)` dal profilo versionato hardcoded, fallback sicuro a `PUBLIC_SAFE_FIXED_DNS_PROFILE`, supporto a override locale gitignored tramite `local.dns_zone_profile.ACTIVE_FIXED_DNS_PROFILE`, test dedicati in `tests/test_profile_resolver.py` e quality gates globali verdi (`python -m pytest -q` → `78 passed`, `python -m pylint src tests` → `10.00/10`) su branch allineato a `origin/development`.
- Ultimo consolidamento `C2`: chiusura tecnica del blocco consolidata nel commit `c432feb` (`feat(cli): add minimal web demo entrypoint`), con aggiunta del subcommand `dns-zone-cli web` come entrypoint minimale installato per avviare la demo FastAPI, estensione di `tests/test_bootstrap.py` sul nuovo boundary CLI/web e quality gates globali verdi (`python -m pytest -q` → `76 passed`, `python -m pylint src tests` → `10.00/10`) su branch allineato a `origin/development`.
- Ultimo consolidamento `C0`: primo incremento tecnico del `Cycle C` consolidato nel commit `a702f0b` (`feat(web): add minimal C0 web page`), con root `/` convertita in pagina HTML minimale, endpoint `/health` preservato, test bootstrap web dedicati aggiunti e quality gates globali verdi (`python -m pytest -q` → `73 passed`, `python -m pylint src tests` → `10.00/10`) su branch allineato a `origin/development`.
- Ultimo consolidamento `B3`: chiusura formale e documentale del blocco realistic-backed, a valle di tre incrementi tecnici consolidati (`d87feff`, `c98851b`, `6edb1e2`) e dell'audit read-only finale contro riferimento reale locale e snapshot normalizzato locale, con quality gates globali verdi (`python -m pytest -q` → `70 passed`, `python -m pylint src tests` → `10.00/10`) e branch allineato a `origin/development`.
- Ultimo consolidamento `B2`: chiusura formale e documentale del blocco, con renderer e boundary `application` difesi su success path e failure path sia golden sia non-golden, inclusi i rispettivi success-call e failure-call contract verso `render_bind_zone_file(...)`, quality gates globali verdi (`67 passed`, `pylint 10.00/10`) e repository allineato a `origin/development`.

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

### A2 — Setup laboratorio Cloudflare free + prove import/export — ✅
**Obiettivo**  
Creare un ambiente di verifica reale per:
- import manuale di zone file;
- export di zone file di riferimento;
- raccolta di fixture golden da usare nei test.

**Stato operativo**
- attivato e usato un laboratorio Cloudflare di verifica;
- generato localmente un file `.txt` BIND import-ready a partire dal runtime con override locale gitignored;
- osservato un primo failure sul record `www` in presenza di record preesistenti nella zona target, quindi classificato come conflitto ambientale e non come gap del generatore;
- ripetuto il test su una zona pulita con import Cloudflare riuscito.

**Evidenze correnti**
- `resolve_active_fixed_dns_profile()` ha caricato correttamente il profilo locale `ACTIVE_FIXED_DNS_PROFILE`;
- `generate_bind_zone_file("testdomain.com")` ha restituito `is_valid=True`, `error_code=None` e un file scritto localmente per il test di import;
- il file generato è risultato strutturalmente coerente con il riferimento reale locale, al netto del preambolo export Cloudflare e del record `SOA` fuori perimetro v1;
- log finale di import Cloudflare: `Success! We successfully imported your records.`

**Nota di chiusura A2**
- il workflow v1 `dominio -> file .txt -> import Cloudflare` risulta ora validato empiricamente;
- `A2` si considera chiuso sul piano sostanziale; eventuali export Cloudflare aggiuntivi o fixture golden ulteriori restano miglioramenti futuri e non prerequisiti bloccanti per la v1.

### A3 — Acquisizione e normalizzazione file di esempio — ✅
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

### B2 — Renderer BIND zone file — ✅
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
- irrigidito ulteriormente `tests/shared_bind_zone_assertions.py` come contratto condiviso non-golden tra renderer puro e boundary `application`, congelando in modo più esplicito la presenza, unicità e ordine dei section headers `A`, `CNAME`, `MX`, `SRV`, `TXT`, un insieme rappresentativo cross-section di linee renderizzate per `alpha-zone.example.org`, l'assenza di placeholder raw residui `{apex}`, `{apex_fqdn}`, `{apex_slug}` e l'assenza di newline finale, mantenendo il tutto confinato al solo layer test-side condiviso;
- aggiunto un test dedicato nel layer `application` che congela esplicitamente, per l'apex valido non-golden `alpha-zone.example.org`, la parità full-text tra `generate_bind_zone_file(...)` e `render_bind_zone_file(...)` invocato con `PUBLIC_SAFE_FIXED_DNS_PROFILE`, così da non limitare più il percorso applicativo non-golden al solo subset contract condiviso;
- aggiunto un test dedicato nel layer `application` che congela esplicitamente, per l'apex valido non-golden `alpha-zone.example.org`, il confronto diretto tra `generate_bind_zone_file(...)` e il golden file dedicato `tests/golden/public_safe_candidate.alpha-zone-example-org.bind.txt`, così da rendere il boundary `application` difeso anche contro il golden testuale completo del percorso non-golden e non solo tramite parità con il renderer puro;
- irrigidito il test dedicato nel layer `application` sul percorso non-golden `alpha-zone.example.org`, passando da assertion parziali su `error_code`, `zone_apex` e `zone_file_text` al freeze dell'intero `BindZoneFileGenerationResult` di successo contro il golden dedicato, così da rendere più esplicito e completo il contratto strutturato del boundary `application`;
- aggiunto un test dedicato nel layer `application` che congela esplicitamente, per l'apex valido non-golden `alpha-zone.example.org`, il success-call contract del boundary, verificando che `generate_bind_zone_file(...)` invochi `render_bind_zone_file(...)` con `zone_apex="alpha-zone.example.org"` e `profile=PUBLIC_SAFE_FIXED_DNS_PROFILE`, e che propaghi nel risultato strutturato il testo di successo restituito dal renderer;
- aggiunto un test dedicato nel layer `application` che congela esplicitamente, per l'apex valido non-golden `alpha-zone.example.org`, il renderer failure boundary, verificando che un `RuntimeError` interno di `render_bind_zone_file(...)` venga tradotto in `error_code="renderer_failure"` con `zone_apex="alpha-zone.example.org"` preservato e `zone_file_text=None`;
- irrigidito ulteriormente il test dedicato nel layer `application` sul failure path golden `testdomain.com`, congelando anche il failure-call contract verso `render_bind_zone_file(...)`, cioè l'invocazione una sola volta con `zone_apex="testdomain.com"` e `profile=PUBLIC_SAFE_FIXED_DNS_PROFILE` anche quando il renderer fallisce con `ValueError`;
- irrigidito ulteriormente il test dedicato nel layer `application` sul failure path non-golden `alpha-zone.example.org`, congelando anche il failure-call contract verso `render_bind_zone_file(...)`, cioè l'invocazione una sola volta con `zone_apex="alpha-zone.example.org"` e `profile=PUBLIC_SAFE_FIXED_DNS_PROFILE` anche quando il renderer fallisce con `RuntimeError`;
- aggiunto un golden file dedicato `tests/golden/public_safe_candidate.alpha-zone-example-org.bind.txt` e un test dedicato nel layer `renderer` che congela esplicitamente, per l'apex valido non-golden `alpha-zone.example.org`, il full-text prodotto da `render_bind_zone_file(...)`, così da rendere indipendente dal boundary `application` anche il freeze testuale completo del percorso non-golden del renderer puro;
- aggiunto un test dedicato nel layer `renderer` che formalizza l'audit comparativo tra il golden baseline `tests/golden/public_safe_candidate.bind.txt` e il golden non-golden `tests/golden/public_safe_candidate.alpha-zone-example-org.bind.txt`, congelando che, dopo la normalizzazione dei soli token derivati attesi dell'apex (`alpha-zone.example.org.` → `testdomain.com.` e `alpha-zone-example-org` → `testdomain-com`), i due file coincidano byte-for-byte senza derive strutturali residue;
- estesa la copertura del use case `generate_bind_zone_file` con un failure path sintattico aggiuntivo su apex overlong, verificando la propagazione di `error_code="domain_too_long"` e l'assenza di testo renderizzato;
- estesa ulteriormente la copertura del use case `generate_bind_zone_file` con un failure path sintattico aggiuntivo su input vuoto, verificando la propagazione di `error_code="empty_input"` e l'assenza di testo renderizzato;
- estesa ulteriormente la copertura del use case `generate_bind_zone_file` con un failure path sintattico aggiuntivo su apex privo di dot, verificando la propagazione di `error_code="missing_dot"` e l'assenza di testo renderizzato;
- estesa ulteriormente la copertura del use case `generate_bind_zone_file` con un failure path sintattico aggiuntivo su apex con dot iniziale, verificando la propagazione di `error_code="leading_dot"` e l'assenza di testo renderizzato;
- estesa ulteriormente la copertura del use case `generate_bind_zone_file` con un failure path sintattico aggiuntivo su apex con dot finale, verificando la propagazione di `error_code="trailing_dot"` e l'assenza di testo renderizzato;
- estesa ulteriormente la copertura del use case `generate_bind_zone_file` con un failure path sintattico aggiuntivo su apex con label vuota, verificando la propagazione di `error_code="empty_label"` e l'assenza di testo renderizzato;
- estesa ulteriormente la copertura del use case `generate_bind_zone_file` con un failure path sintattico aggiuntivo su apex con label non valida, verificando la propagazione di `error_code="invalid_label"` e l'assenza di testo renderizzato;
- estesa ulteriormente la copertura del use case `generate_bind_zone_file` con un failure path sintattico aggiuntivo su input apex non stringa, verificando la propagazione di `error_code="non_string_input"` e l'assenza di testo renderizzato;
- estesa la copertura del renderer BIND con un test mirato sul quoting dei record `TXT`, verificando esplicitamente che l'output renderizzato mantenga il payload tra doppi apici per record testuali rappresentativi del profilo public-safe;
- estesa la copertura del renderer BIND con un test mirato sulle annotazioni `cf_tags`, verificando esplicitamente la resa di record sia `cf-proxied:true` sia `cf-proxied:false` nell'output renderizzato del profilo public-safe;
- aggiunto un test esplicito che congela presenza, unicità e ordine dei section headers `A`, `CNAME`, `MX`, `SRV` e `TXT` nell'output BIND del profilo public-safe, rendendo esplicito il contratto corrente dei blocchi sezione del renderer;
- aggiunto un test esplicito che congela l'assenza delle annotazioni `cf_tags` per record del profilo public-safe privi di stato proxy esplicito (`cf_proxied is None`), rendendo più completo il contratto corrente del renderer sulle annotazioni Cloudflare;
- reso esplicito nel renderer BIND il failure path per `record_type` non supportato, sostituendo il `KeyError` implicito sul mapping delle sezioni con un `ValueError` deterministico e aggiungendo un test dedicato che congela il comportamento su un record artificiale con tipo non supportato (`AAAA`);
- irrigidito il boundary `application` del use case `generate_bind_zone_file`, che ora intercetta i failure interni del renderer e restituisce un esito strutturato con `error_code="renderer_failure"`, `zone_file_text=None` e `zone_apex` preservato quando l'input è valido; aggiunto inoltre un test dedicato che forza il renderer a fallire e congela il nuovo comportamento del use case;
- reso il grouping delle sezioni del renderer BIND indipendente dall'ordine di `profile.records`, introducendo un test dedicato su record interleaved che congela unicità delle sezioni e ordine canonico `A`, `CNAME`, `MX`, `SRV`, `TXT` anche quando i record in input non sono contigui per tipo;
- riallineato il contratto dichiarato del layer `application` al comportamento runtime già supportato sui failure strutturati di input non stringa, tipizzando `input_value` come `object` nei result object e nelle firme di `validate_zone_apex_input(...)` e `generate_bind_zone_file(...)`, e aggiungendo un test dedicato sul validation use case per `non_string_input`;
- irrigidito ulteriormente il boundary `application` di `generate_bind_zone_file(...)`, traducendo in `error_code="renderer_failure"` non solo `ValueError` ma anche `RuntimeError` interni del renderer e aggiungendo un test dedicato che congela il caso di failure renderer non-`ValueError`;
- aggiunto un test dedicato che congela esplicitamente il contratto di short-circuit del boundary `application`, verificando che `generate_bind_zone_file(...)` restituisca il failure strutturato e non invochi `render_bind_zone_file(...)` quando la validazione dell'input fallisce;
- aggiunto un test dedicato che congela esplicitamente il success-call contract del boundary `application`, verificando che `generate_bind_zone_file(...)` invochi `render_bind_zone_file(...)` con `zone_apex` validato e `profile=PUBLIC_SAFE_FIXED_DNS_PROFILE`, e che propaghi nel risultato strutturato il testo ritornato dal renderer;
- aggiunto un test dedicato che congela esplicitamente, nel renderer BIND, la preservazione dell'ordine relativo di input dei record dello stesso tipo all'interno della sezione `CNAME`, anche in presenza di profilo interleaved;
- aggiunto un test dedicato che congela esplicitamente, nel renderer BIND, l'omissione delle sezioni vuote quando il profilo contiene solo un sottoinsieme dei record supportati, verificando l'emissione delle sole sezioni presenti in un profilo parziale `A`/`TXT`;
- aggiunto un test dedicato che congela esplicitamente, nel renderer BIND, l'assenza di newline iniziale, newline finale e blank line spurie quando l'output contiene una sola sezione `TXT`;
- aggiunto un test dedicato che congela esplicitamente, nel renderer BIND, la separazione tramite esattamente una sola blank line tra sezioni popolate consecutive, verificando il comportamento su un profilo multi-section parziale `A`/`MX`/`TXT`;
- avanzamento aggiuntivo consolidato a commit nel branch `development` con `68e6690` (`test(application): freeze non-golden renderer failure boundary`);
- avanzamento aggiuntivo consolidato a commit nel branch `development` con `8f8530d` (`test(application): freeze non-golden renderer failure call contract`);
- avanzamento aggiuntivo consolidato a commit nel branch `development` con `2a9b10d` (`test(application): freeze golden renderer failure call contract`);

- aggiornate le evidenze globali al checkpoint più recente del freeze application-side sul renderer failure boundary non-golden: `python -m pytest -q` → `67 passed` e `python -m pylint src tests` → `10.00/10`;
- avanzamento tecnico consolidato nei commit `e56afef`, `66f8c3d`, `4733c97`, `85203cf`, `5cf0c05`, `bff112d`, `1840aab`, `bc4f648`, `641065e`, `514f278`, `43d7d37`, `2898fbb`, `6742c0e`, `97d3e83`, `ebe3221`, `558c533`, `ef25219`, `ca8e2e0`, `9b2957d`, `7aad215`, `afa92bd`, `9c5910b` e `f97cd44`, oltre ai freeze contrattuali consolidati nei commit `1857c1d`, `2b0c015`, `666efe7`, `110febe` e `ce15d46`.

**Nota di chiusura B2**
- `B2` non è più da considerare solo un blocco di rendering isolato: esiste ora un primo contratto framework-agnostic end-to-end nel core, che parte dallo zone apex input, valida l'input e produce il testo BIND usando il profilo fisso public-safe, con resa derivata su apex non-golden difesa in modo coerente sia nel renderer sia nel use case applicativo tramite assertion condivise nel solo layer test, con copertura esplicita anche del quoting dei record `TXT`, delle annotazioni `cf_tags`, della presenza, unicità e ordine dei section headers, dell'assenza di annotazioni `cf_tags` per record senza stato proxy esplicito, del failure path deterministico per `record_type` non supportato nel renderer, della conversione strutturata dei failure interni del renderer in `error_code="renderer_failure"` nel boundary `application`, dell'indipendenza del grouping delle sezioni rispetto all'ordine dei record in input, della coerenza tra type surface dichiarata e failure strutturati già supportati su input non stringa e dell'hardening esplicito del failure translation boundary anche per `RuntimeError` interni del renderer e del freeze esplicito del success-call contract del boundary `application`, che rende non più solo implicita l'orchestrazione del percorso di successo, oltre al freeze esplicito dell'ordine relativo intra-sezione dei record dello stesso tipo nel renderer, dell'omissione esplicita delle sezioni vuote per profili parziali, dell'assenza di blank line spurie su output a sezione unica e della separazione esplicita tramite una sola blank line tra sezioni popolate consecutive.
- la DoD sostanziale del blocco risulta soddisfatta sul repository reale;
- il renderer BIND minimale è presente, versionato e difeso da golden baseline, golden non-golden, contratti strutturali e test mirati su placeholder derivati, grouping, ordine, blank lines, TXT quoting, `cf_tags` e failure contract per `record_type` non supportato;
- il boundary `application` è presente, versionato e difeso su success path e failure path, sia golden sia non-golden, con freeze esplicito dei contratti di orchestrazione verso il renderer nei percorsi di successo e di failure;
- il confronto realistico read-only con il file di riferimento non ha evidenziato gap strutturali tali da giustificare ulteriore hardening immediato dentro `B2`;
- `B2` si considera chiuso; il passo successivo corretto è `B3`, dedicato alla protezione del generatore con fixture e confronti più realistici, senza aprire nello stesso blocco scope su UI/web.

### B3 — Test del generatore e preparazione fixture reali — ✅
**Obiettivo**
Proteggere il comportamento del generatore tramite test automatici e preparare l'ingresso di fixture realistiche versionabili, senza dipendere direttamente dagli artefatti privati gitignored.

**Dipendenze**
- file reale di riferimento già acquisito;
- snapshot normalizzato locale del riferimento reale già disponibile;
- eventuale laboratorio Cloudflare per export/import di verifica.

**Stato operativo**
- completato audit read-only tra golden public-safe versionato, file reale locale gitignored, snapshot normalizzato locale, profilo runtime `public_safe_candidate`, renderer e boundary `application`;
- confermata parità strutturale e d'ordine del candidato v1 rispetto al riferimento reale, al netto del solo `SOA` presente nell'export reale e già fuori perimetro runtime/versionato;
- confermato allineamento tra profilo runtime versionato e snapshot normalizzato su inventario, ordine, `cf_proxied`, `manual_flag` e `rdata_kind`;
- verificato che `samples/private/` è gitignored e che le fixture realistiche locali non sono referenziate dai test versionati del repository;
- identificato come primo passo corretto di `B3` la creazione di una fixture versionata, public-safe e realistic-backed sotto `tests/golden`, da usare come ponte verso il primo test snapshot-backed del generatore nel layer `application`.
- introdotta la prima fixture versionata, public-safe e realistic-backed in `tests/golden/public_safe_candidate.testdomain-com.bind.txt`, derivata dal riferimento reale auditato, strutturalmente allineata al candidato v1, senza SOA e con delta confinato ai soli valori sanitizzati rispetto al riferimento reale;
- aggiunto in `tests/test_bind_zone_generation_use_case.py` un primo test snapshot-backed nel layer `application` che congela il delta ammesso rispetto alla fixture realistic-backed tramite normalizzazione esplicita dei soli valori sanitizzati/public-safe verso la baseline runtime corrente, senza modificare il runtime del profilo o del renderer;
- esteso in `tests/test_bind_zone_renderer.py` anche il freeze realistic-backed sul layer `renderer` per `testdomain.com` contro la stessa fixture versionata, e successivamente estratto in `tests/shared_bind_zone_assertions.py` l'helper condiviso `load_normalized_realistic_testdomain_golden(...)`, riusato da renderer e `application` per deduplicare la normalizzazione test-side senza modificare runtime, renderer o fixture;
- aggiunto `tests/test_shared_bind_zone_assertions.py` con un test dedicato che congela il comportamento del helper shared realistic-backed, verificando la presenza dei soli frammenti sanitizzati attesi nel raw realistic-backed, la loro assenza nel testo normalizzato e la parità byte-for-byte del risultato normalizzato con il golden baseline public-safe.
- completato audit read-only finale contro `samples/private/company_reference/testdomain.com.txt` e `samples/private/company_reference/testdomain.profile.snapshot.json`, con conferma che la fixture versionata `tests/golden/public_safe_candidate.testdomain-com.bind.txt` conserva ordine e struttura del candidato v1, esclude solo il record `SOA` export-only e differisce dal riferimento reale soltanto per sanitizzazione public-safe e normalizzazione del whitespace.

**Evidenze correnti**
- `git status` → `nothing to commit, working tree clean`;
- `git status -sb` → `## development...origin/development`;
- `python -m pytest -q` → `70 passed`;
- `python -m pylint src tests` → `10.00/10`;
- primo avanzamento tecnico `B3` consolidato nel commit `d87feff` (`test(application): freeze realistic-backed testdomain golden delta`);
- secondo avanzamento tecnico `B3` consolidato nel commit `c98851b` (`test(bind): share realistic-backed golden normalization helper`);
- terzo avanzamento tecnico `B3` consolidato nel commit `6edb1e2` (`test(bind): freeze shared realistic-backed normalization helper`);
- `samples/private/company_reference/testdomain.profile.snapshot.json` → `record_lines=14`, `excluded_record_lines=1`, `v1_candidate_record_lines=13`;
- `diff -u samples/private/company_reference/testdomain.com.txt tests/golden/public_safe_candidate.testdomain-com.bind.txt` → delta confinato a header/export comments + `SOA` escluso, sanitizzazione public-safe dei valori sensibili e normalizzazione del whitespace;
- `git status -sb` post-push → `## development...origin/development`;
- audit read-only completato: delta residuo confinato a `SOA` extra nel riferimento reale e a valori sanitizzati/public-safe rispetto ai valori reali; nessun gap strutturale emerso sul candidato v1.
- isolamento test-side della suite `application` dal profilo locale gitignored consolidato nel commit `4681df0` (`test(application): isolate public-safe runtime profile in application suite`), così da preservare i golden e i call contract versionati anche quando `local.dns_zone_profile` è presente nel workspace.

### B4 — Runtime fixed profile resolution boundary — ✅
**Obiettivo**
Introdurre un boundary runtime che permetta al generatore di usare, quando disponibile, un profilo fixed locale gitignored con valori concreti, senza rompere la baseline public-safe versionata del repository.

**Stato operativo**
- introdotto `src/dns_zone_bootstrapper/templates/profile_resolver.py` come boundary dedicato alla risoluzione del profilo fisso attivo a runtime;
- `generate_bind_zone_file(...)` non dipende più direttamente da `PUBLIC_SAFE_FIXED_DNS_PROFILE`, ma usa ora `resolve_active_fixed_dns_profile()`;
- il resolver prova a usare `local.dns_zone_profile.ACTIVE_FIXED_DNS_PROFILE` quando presente;
- in assenza del modulo locale, il runtime ricade in modo deterministico sul profilo versionato public-safe;
- aggiunti `tests/test_profile_resolver.py` per congelare sia il fallback al profilo public-safe sia l'uso dell'override locale.

**Evidenze correnti**
- `git status` → `nothing to commit, working tree clean`;
- `git status -sb` → `## development...origin/development`;
- `python -m pytest -q` → `78 passed`;
- `python -m pylint src tests` → `10.00/10`;
- avanzamento tecnico consolidato nel commit `98ef332` (`feat(templates): add runtime fixed profile resolver`).

**Nota di chiusura B4**
- il repository dispone ora del gancio architetturale corretto per separare baseline runtime public-safe e valori fixed concreti non versionati;
- il passo successivo corretto non è un refactor largo né un blocco `D*`, ma l'introduzione di un primo `ACTIVE_FIXED_DNS_PROFILE` locale gitignored e la successiva verifica del file generato con valori concreti.

---

## Cycle C — Delivery surfaces

### C0 — Pagina web minimale — ✅
**Obiettivo**
Esporre il core tramite una pagina web minimale coerente con la richiesta iniziale.

**Stato operativo**
- il web adapter `FastAPI` espone ora una root `/` HTML minimale in italiano al posto del precedente bootstrap JSON;
- la pagina mostra titolo, descrizione sintetica, un solo input `Dominio apex` e una CTA disabilitata che esplicita la successiva attivazione del download in `C1`;
- l'endpoint `/health` resta invariato come superficie tecnica minima;
- `tests/test_bootstrap.py` è stato esteso per congelare il contratto minimo della superficie web su contenuto HTML, payload health e route pubbliche minime.

**Evidenze correnti**
- `python -m pytest -q` → `73 passed`;
- `python -m pylint src tests` → `10.00/10`;
- avanzamento tecnico consolidato nel commit `a702f0b` (`feat(web): add minimal C0 web page`).

**Nota di chiusura C0**
- la pagina web minimale della v1 è ora presente, versionata e difesa da test bootstrap dedicati;
- il collegamento del form al generatore BIND e il download diretto del file `.txt` restano correttamente demandati a `C1`.

### C1 — Generazione e download del file — ✅
**Obiettivo**
Permettere l'inserimento del dominio e il download diretto del file `.txt` generato.

**Stato operativo**
- la root `/` espone ora un form attivo con `action="/generate"` e bottone abilitato per l'avvio del flusso web minimale della v1;
- la route `GET /generate` integra il use case framework-agnostic `generate_bind_zone_file(...)` senza introdurre nuove dipendenze o logica duplicata fuori dal core;
- sul success path viene restituito il file BIND come `text/plain` con header `Content-Disposition` orientato al download diretto;
- sul failure path il web adapter restituisce una pagina HTML con messaggio di errore user-facing derivato dagli `error_code` strutturati del boundary applicativo, preservando la superficie minima della demo;
- `tests/test_bootstrap.py` è stato esteso per congelare l'entrypoint `C1`, il failure path HTML su input invalido, il success path di download e la presenza della route pubblica `/generate`.

**Evidenze correnti**
- `python -m pytest -q` → `75 passed`;
- `python -m pylint src tests` → `10.00/10`;
- avanzamento tecnico consolidato nel commit `7562486` (`feat(web): add C1 generation and download flow`).

**Nota di chiusura C1**
- la superficie web della v1 consente ora sia l'inserimento del dominio sia il download diretto del file `.txt` generato;
- il prossimo step corretto del `Cycle C` è `C2`, dedicato alla rifinitura della demo web e al packaging minimo.

### C2 — Rifinitura demo web e packaging minimo — ✅
**Obiettivo**
Rifinire in modo conservativo la demo web esistente e preparare un packaging minimo di esecuzione, senza toccare il core applicativo.

**Stato operativo**
- `C2` è stato completato con due micro-step conservativi e verificabili, senza toccare il core applicativo;
- nel primo micro-step la root `/` è stata riallineata allo stato reale della demo web, eliminando la copy obsoleta che descriveva `C1` come ancora "in apertura";
- nel secondo micro-step la superficie installata del progetto espone ora il subcommand `dns-zone-cli web`, che avvia localmente la demo FastAPI tramite `uvicorn` con configurazione minima deterministica;
- `tests/test_bootstrap.py` è stato esteso sia sul contratto testuale della root sia sul nuovo boundary CLI/web minimale, mantenendo invariati renderer, template, use case applicativi e route pubbliche già consolidate.

**Evidenze correnti**
- `python -m pytest -q` → `76 passed`;
- `python -m pylint src tests` → `10.00/10`;
- primo avanzamento tecnico `C2` consolidato nel commit `cb99280` (`feat(web): refresh demo copy for active generation flow`);
- secondo avanzamento tecnico `C2` consolidato nel commit `c432feb` (`feat(cli): add minimal web demo entrypoint`).

**Nota di chiusura C2**
- la demo web minima della v1 è ora rifinita sia sul piano della comunicazione user-facing sia su quello del packaging minimo di avvio locale;
- la DoD sostanziale del blocco risulta soddisfatta sul repository reale e `C2` si considera chiuso; l'eventuale blocco successivo dovrà essere determinato separatamente con un nuovo audit conservativo.


### Post-A2 / Post-C2 — Freeze strategico, documentazione essenziale e preparazione consegna — 🟡
**Obiettivo**
Congelare il significato del prodotto, il suo posizionamento operativo e la sequenza corretta dei prossimi blocchi, così da evitare derive premature su UI polish, Docker o hardening non prioritari.

**Valutazione congelata**
- il prodotto è da considerare funzionante e coerente con la richiesta chiarita per la v1;
- la richiesta sostanziale risulta soddisfatta: input unico `dominio`, valori fixed, output `.txt` orientato all'import Cloudflare e superficie principale web;
- il risultato principale già validato non è un semplice file generato, ma un artefatto DNS deterministico, riproducibile e importabile che riduce lavoro manuale e rischio operativo;
- il lavoro svolto fino a questo punto è valutato positivamente, ma la difendibilità del progetto non è ancora massima finché il prodotto non risulta comprensibile a terzi anche sul piano documentale.

**Decisioni congelate**
- non aprire automaticamente `D0`, `D1`, `D2` o altri hardening generici come prossimo passo;
- non introdurre nuovi owner docs se non strettamente necessario;
- usare il `README.md` come punto di ingresso principale per spiegare senso del prodotto, contesto, utilità, workflow, lessico di base e perimetro v1;
- usare `ARCHITECTURE.md` per chiarimenti strutturali e tecnici del funzionamento del software, senza trasformarlo in guida utente;
- introdurre un documento di supporto tipo guida utente solo se emerge un bisogno reale non assorbibile in modo pulito dal `README.md`;
- mantenere UI polish e Docker fuori dal perimetro essenziale della prima consegna.

**Contenuti documentali da assorbire nel blocco essenziale**
- spiegazione di cosa risolve il prodotto e perché esiste;
- spiegazione di concetti minimi necessari per capire il dominio (`BIND`, zone file, zona apex, import Cloudflare, record DNS rilevanti);
- spiegazione del workflow reale del software e del rapporto tra template, rendering, import Cloudflare e profili fixed;
- spiegazione della distinzione tra baseline public-safe versionata e override locale gitignored;
- esplicitazione di ciò che la v1 fa e di ciò che non fa ancora;
- guida pratica all'uso per demo, generazione file e interpretazione dei conflitti più comuni.

**Sequenza operativa congelata**
1. blocco documentale essenziale sul `README.md`;
2. eventuale riallineamento mirato di `ARCHITECTURE.md` ai chiarimenti concettuali/tecnici necessari;
3. eventuale guida utente dedicata, solo se la densità del `README.md` diventasse eccessiva;
4. solo dopo questi punti, preparazione del messaggio/report verso l'azienda con stato attuale, validazione ottenuta, demo disponibile e limiti residui;
5. successivamente audit su UI minimale difendibile;
6. successivamente valutazione Docker/exportability.


**Deliverable essenziali del blocco documentale**
- `README.md` rafforzato come documento di ingresso, comprensibile anche a chi non conosce il progetto o il dominio DNS;
- chiarimenti mirati in `ARCHITECTURE.md` su concetti, flusso software e boundary principali;
- eventuale guida pratica dedicata (`docs/guides/USER_GUIDE.md` oppure documento equivalente) solo se necessaria per non sovraccaricare il `README.md`;
- base già pronta dei punti da riportare nel futuro messaggio/report verso l'azienda.

**Criterio di uscita del blocco documentale essenziale**
- un lettore nuovo deve poter capire cos'è il prodotto, a cosa serve, cosa prende in input, cosa produce in output e quali limiti ha la v1;
- deve risultare chiara la differenza tra profilo public-safe versionato e profilo locale gitignored;
- deve risultare chiaro il rapporto tra template fisso, rendering BIND, demo web e import Cloudflare;
- deve essere pronta la base informativa minima per una comunicazione aziendale pulita, senza dipendere ancora da CSS, polish UI o Docker.

**Backlog non bloccante già classificato**
- polish UI con CSS, responsive, gerarchia visiva e feedback utente migliori;
- Docker/exportability e relativi documenti di deployment;
- eventuali affinamenti estetici o infrastrutturali ulteriori non necessari per la prima comunicazione/consegna.

**Gate di comunicazione**
- la comunicazione è ritenuta opportuna dopo il completamento del blocco documentale essenziale;
- il contenuto atteso del futuro report dovrà includere almeno: stato v1, coerenza rispetto alla richiesta, validazione empirica Cloudflare, disponibilità demo web, limiti attuali e distinzione tra miglioramenti essenziali e miglioramenti non bloccanti;
- UI styles, polish grafico, responsive refinement e Docker non devono bloccare la prima comunicazione/consegna se il blocco documentale essenziale è chiuso e la demo resta verificata.

**Nota operativa**
- il rischio maggiore attuale non è una regressione del core, ma il fatto che il prodotto possa risultare poco leggibile o poco spiegato a chi non ha seguito la storia del repository;
- per questo il prossimo blocco corretto è documentale e non estetico/infrastrutturale.
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
Preparare una demo presentabile e riproducibile.

### D3 — Eventuale import diretto via API come extra — ⬜
**Obiettivo**  
Valutare come estensione futura l'import assistito o diretto verso Cloudflare.
