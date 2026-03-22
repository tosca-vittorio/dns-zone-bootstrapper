# CHANGELOG

## Branch: [development]

### [Unreleased]
> Scope corrente: chiusura bootstrap repository/documentazione (`A0`), consolidamento di `B0` sulla validazione sintattica del dominio apex candidate, hardening progressivo di `B1` sul profilo DNS fisso public-safe versionabile, apertura minima di `B2` con primo renderer BIND verificato, hardening del contratto testuale tramite golden file esterno e placeholder derivati, introduzione del boundary applicativo minimo di generazione del file BIND, deduplicazione qualitativa delle assertion condivise tra renderer puro e use case applicativo e copertura di failure path applicativi aggiuntivi su input overlong e vuoto.

#### B2 — Renderer BIND zone file (apertura minima)
> Ordinamento: `git log` (più recente → più vecchio) · principio truth-first: qui è riportato solo ciò che è consolidato a commit sul branch `development`.

- **`ebe3221` — `test(application): cover empty bind zone input failure`**
  - **Type:** `test` · **Categoria:** Application / Failure path coverage
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato su input apex vuoto, verificando nel use case `generate_bind_zone_file` la propagazione di `error_code="empty_input"` e l'assenza di `zone_file_text`.
  - **Impatto:** amplia ulteriormente la robustezza del boundary `application` sul failure path minimo più vicino all'input reale utente, senza modificare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `40 passed`; `python -m pylint src tests` → `10.00/10`.

- **`97d3e83` — `test(application): cover overlong bind zone input failure`**
  - **Type:** `test` · **Categoria:** Application / Failure path coverage
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato su input apex sintatticamente overlong, verificando nel use case `generate_bind_zone_file` la propagazione di `error_code="domain_too_long"` e l'assenza di `zone_file_text`.
  - **Impatto:** rende `B2` più solido sul boundary `application`, perché amplia la copertura dei failure path oltre il solo caso di `surrounding_whitespace` senza modificare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `39 passed`; `python -m pylint src tests` → `10.00/10`.

- **`6742c0e` — `test(application): share bind zone assertions across core paths`**
  - **Type:** `test` · **Categoria:** Application / Renderer shared assertions
  - **Cosa cambia:** introduce `tests/shared_bind_zone_assertions.py` e `tests/__init__.py`, riusa le stesse assertion sul rendering derivato in `tests/test_bind_zone_renderer.py` e `tests/test_bind_zone_generation_use_case.py`, e aggiunge nel layer `application` un test end-to-end su apex valido non-golden (`alpha-zone.example.org`).
  - **Impatto:** rende `B2` più solido e più pulito sul piano test-side, perché difende lo stesso contratto derivato lungo due percorsi del core senza duplicazione letterale e senza alterare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `38 passed`; `python -m pylint src tests` → `10.00/10`.

- **`2898fbb` — `feat(application): add fixed bind zone generation use case`**
  - **Type:** `feat` · **Categoria:** Application / BIND generation use case
  - **Cosa cambia:** introduce `src/dns_zone_bootstrapper/application/bind_zone_generation.py` con un use case framework-agnostic che parte dallo `zone_apex` input, riusa la validazione applicativa esistente, consuma il profilo fisso `PUBLIC_SAFE_FIXED_DNS_PROFILE`, invoca il renderer BIND e restituisce un risultato strutturato con `zone_file_text`; aggiunge inoltre `tests/test_bind_zone_generation_use_case.py` con copertura del caso di successo e del failure path con propagazione di `error_code`.
  - **Impatto:** rende `B2` più maturo trasformando il renderer da funzione core isolata a primo contratto applicativo di generazione end-to-end nel package, senza aprire ancora scope su CLI/web o su fixture reali.
  - **Evidenze:** `python -m pytest -q` → `37 passed`; `python -m pylint src tests` → `10.00/10`.

- **`43d7d37` — `test(renderers): cover derived placeholder rendering`**
  - **Type:** `test` · **Categoria:** Renderers / Derived placeholder coverage
  - **Cosa cambia:** estende `tests/test_bind_zone_renderer.py` con un test dedicato su un apex diverso dal golden corrente (`alpha-zone.example.org`), congelando la resa di `apex_slug`, `apex_fqdn` e l'assenza di newline finale nel testo generato.
  - **Impatto:** rende `B2` più difendibile contro drift silenziosi nella logica di rendering dei placeholder derivati, senza modificare il comportamento runtime del renderer.
  - **Evidenze:** `python -m pytest -q` → `35 passed`; `python -m pylint src tests` → `10.00/10`.

- **`514f278` — `test(renderers): externalize public-safe BIND golden output`**
  - **Type:** `test` · **Categoria:** Renderers / Golden contract
  - **Cosa cambia:** introduce `tests/golden/public_safe_candidate.bind.txt` come golden file public-safe del renderer BIND e alleggerisce `tests/test_bind_zone_renderer.py`, che ora legge l'expected esterno invece di mantenere il contratto testuale inline.
  - **Impatto:** rende il confronto del testo generato più auditabile, manutenibile e pronto a futuri confronti golden senza modificare il comportamento runtime del renderer.
  - **Evidenze:** `python -m pytest -q` → `34 passed`; `python -m pylint src tests` → `10.00/10`.

- **`641065e` — `feat(renderers): add minimal BIND zone file renderer`**
  - **Type:** `feat` · **Categoria:** Renderers / BIND zone file
  - **Cosa cambia:** introduce `src/dns_zone_bootstrapper/renderers/bind_zone_renderer.py` con una funzione pura che renderizza il profilo DNS fisso a testo BIND a partire da `zone_apex` e `FixedDnsProfile`, gestendo owner FQDN, risoluzione placeholder, quoting dei record `TXT`, annotazioni opzionali `cf_tags` e raggruppamento per tipo record; aggiunge inoltre `tests/test_bind_zone_renderer.py` con un contratto testuale esplicito sul profilo `PUBLIC_SAFE_FIXED_DNS_PROFILE`.
  - **Impatto:** apre sostanzialmente `B2` con un primo contratto di rendering framework-agnostic, separato da CLI/web/application, e prepara il terreno a successivi test golden o confronti più realistici senza reintrodurre dipendenze runtime dagli asset privati locali.
  - **Evidenze:** `python -m pytest -q` → `34 passed`; `python -m pylint src tests` → `10.00/10`.

#### B1 — Modello record DNS e profilo template fisso (baseline iniziale)
> Ordinamento: `git log` (più recente → più vecchio) · principio truth-first: qui è riportato solo ciò che è consolidato a commit sul branch `development`.

- **`1411bea` — `refactor(templates): formalize semantic rdata template metadata`**
  - **Type:** `refactor` · **Categoria:** Templates / Semantic RDATA metadata
  - **Cosa cambia:** introduce nel model layer un value object dedicato per il `rdata`, formalizzando in modo esplicito metadata semantici (`kind`) e template string (`template`) del payload DNS e aggiornando il profilo `public_safe_candidate` di conseguenza, con test dedicato sul freeze della superficie `rdata_kind`.
  - **Impatto:** riduce la dipendenza da logica implicita “stringly-typed” nella lettura del profilo `B1`, rende il modello più coerente e prepara meglio il terreno al futuro renderer senza aprire ancora `B2`.
  - **Evidenze:** `pytest -q` → `33 passed`; `python -m pylint src tests` → `10.00/10`.

- **`afdf577` — `refactor(templates): narrow fixed profile model vocabularies`**
  - **Type:** `refactor` · **Categoria:** Templates / Model vocabulary narrowing
  - **Cosa cambia:** restringe nel file `profile_model.py` il vocabolario del model layer introducendo alias tipizzati dedicati per `RecordClass` e `ManualFlag`, sostituendo i campi generici `str` in `DnsRecordTemplate`.
  - **Impatto:** porta nel modello centrale due invarianti già veri nel profilo `B1` corrente e già protetti dai test, riducendo la superficie di drift silenzioso prima dell’apertura del renderer senza modificare il comportamento runtime del profilo public-safe.
  - **Evidenze:** `pytest -q` → `32 passed`; `python -m pylint src tests` → `10.00/10`.

- **`532487a` — `test(templates): freeze public-safe fixed rdata surface`**
  - **Type:** `test` · **Categoria:** Templates / Fixed RDATA contract freeze
  - **Cosa cambia:** aggiunge un test esplicito che congela la superficie `rdata_template` fixed-only non derivata dal dominio nel profilo `public_safe_candidate`, verificando i valori fissi correnti di record `A`, `CNAME`, `MX`, `SRV` e `TXT`.
  - **Impatto:** rende `B1` più difendibile contro drift silenziosi nei valori fissi del profilo prima dell'apertura del renderer, senza modificare il runtime del package.
  - **Evidenze:** `pytest -q` → `32 passed`; `python -m pylint src tests` → `10.00/10`.

- **`c4a31b6` — `test(templates): freeze public-safe placeholder surface`**
  - **Type:** `test` · **Categoria:** Templates / Placeholder contract freeze
  - **Cosa cambia:** aggiunge un test esplicito che congela la superficie placeholder ammessa nel profilo `public_safe_candidate`, verificando i soli casi attesi sui record `brevo1._domainkey`, `brevo2._domainkey` e `www`, oltre all'assenza di `{apex}` nei `rdata_template`.
  - **Impatto:** rende `B1` più difendibile contro drift silenziosi nella semantica dei placeholder prima dell'apertura del renderer, senza modificare il runtime del package.
  - **Evidenze:** `pytest -q` → `31 passed`; `python -m pylint src tests` → `10.00/10`.

- **`87a1e67` — `test(templates): freeze public-safe profile contract`**
  - **Type:** `test` · **Categoria:** Templates / Contract freeze
  - **Cosa cambia:** aggiunge un test esplicito che congela l'inventario record, l'ordine corrente, i flag `cf_proxied` e l'unicità del record TXT con `manual_flag` nel profilo `public_safe_candidate`.
  - **Impatto:** rende `B1` più auditabile e riduce il rischio di drift silenzioso del contratto del profilo prima della successiva formalizzazione tecnica, senza modificare il runtime del package.
  - **Evidenze:** `pytest -q` → `30 passed`; `python -m pylint src tests` → `10.00/10`.

- **`43c3c3b` — `fix(templates): align public-safe profile naming to reference template`**
  - **Type:** `fix` · **Categoria:** Templates / Profile semantic alignment
  - **Cosa cambia:** riallinea nel profilo `public_safe_candidate` il naming dei selector DKIM da `provider1/provider2` a `brevo1/brevo2` e il prefisso del record TXT token-like da `verification-code:` a `brevo-code:`, aggiornando di conseguenza i test associati.
  - **Impatto:** rende la baseline runtime di `B1` più fedele al template fisso reale senza reintrodurre valori privati o dipendenze da snapshot locali; resta invariata la natura public-safe e versionabile del profilo.
  - **Evidenze:** `pytest -q` → `29 passed`; `python -m pylint src tests` → `10.00/10`.

- **`cf943e6` — `feat(templates): add public-safe fixed DNS profile baseline`**
  - **Type:** `feat` · **Categoria:** Templates / Profile model
  - **Cosa cambia:** introduce `profile_model.py` con i data model versionabili per record e profilo DNS fisso, aggiunge `public_safe_candidate.py` come primo profilo public-safe sanificato e aggiunge `tests/test_public_safe_candidate_profile.py` per verificare shape minima, assenza di `SOA` e placeholder derivati dal dominio.
  - **Impatto:** apre realmente `B1` con una baseline code-only difendibile, separa il profilo fisso dal materiale privato locale e prepara il terreno per renderer e formalizzazione successiva del template senza dipendenze runtime da snapshot gitignored.
  - **Evidenze:** `pytest -q` → `29 passed`; `python -m pylint src tests` → `10.00/10`.

- **`a62470e` — `docs(timeline): close B0 and prepare B1 opening`**
  - **Type:** `docs` · **Categoria:** Owner docs / Timeline
  - **Cosa cambia:** aggiorna `TIMELINE.md` chiudendo formalmente `B0` e preparando l’apertura operativa di `B1`, senza introdurre nuove modifiche di codice.
  - **Impatto:** consolida documentalmente la chiusura del blocco di validazione del dominio apex e crea il ponte formale verso la successiva baseline del profilo DNS fisso.
  - **Evidenze:** owner docs riallineati allo stato reale del branch nel checkpoint precedente a `cf943e6`; nessuna modifica al codice.

#### B0 — Validazione dominio apex (prima iterazione sintattica)
> Ordinamento: `git log` (più recente → più vecchio) · focus su primo avanzamento reale del core engine.

- **`bf8dc43` — `docs(project): record remaining B0 validation failure coverage`**
  - **Type:** `docs` · **Categoria:** Owner docs / B0 coverage
  - **Cosa cambia:** aggiorna i documenti owner registrando il completamento della copertura residua dei failure mode sintattici del dominio apex candidate, inclusi `non_string_input` e `domain_too_long`.
  - **Impatto:** rende `B0` più auditabile e allinea la documentazione al checkpoint in cui la copertura dei failure mode principali risulta sostanzialmente completata.
  - **Evidenze:** owner docs riallineati al checkpoint reale successivo a `4771e11`; nessuna modifica al codice.

- **`4771e11` — `test(domain): cover remaining zone apex validation failures`**
  - **Type:** `test` · **Categoria:** Domain / Validation tests
  - **Cosa cambia:** completa la copertura del layer `domain` aggiungendo test espliciti per i failure mode `non_string_input` e `domain_too_long`, già supportati dalla validazione strutturata del dominio apex candidate.
  - **Impatto:** rende `B0` più difendibile e più completo sul piano dei test, senza modificare il comportamento del codice e senza aprire nuovo scope oltre la validazione sintattica corrente.
  - **Evidenze:** `pytest -q` → `26 passed`; `python -m pylint src tests` → `10.00/10`.

- **`6d94090` — `docs(project): record structured B0 validation errors`**
  - **Type:** `docs` · **Categoria:** Owner docs / B0 error model
  - **Cosa cambia:** aggiorna i documenti owner per registrare l’introduzione di `error_code` strutturati nel layer `domain` e la loro propagazione nel layer `application`.
  - **Impatto:** rende esplicito sul piano documentale il passaggio da validazione booleana a risultato strutturato, migliorando la tracciabilità del blocco `B0`.
  - **Evidenze:** owner docs riallineati al checkpoint reale successivo a `f5f579d`; nessuna modifica al codice.

- **`f5f579d` — `feat(domain): add structured zone apex validation errors`**
  - **Type:** `feat` · **Categoria:** Domain / Validation
  - **Cosa cambia:** evolve la validazione del dominio apex da semplice predicato booleano a risultato strutturato con `error_code` deterministici per i principali failure mode sintattici, mantenendo un wrapper booleano compatibile e aggiornando i test del layer `domain` e del layer `application`.
  - **Impatto:** rende `B0` più robusto e più consumabile dalle future superfici applicative, perché l’esito della validazione non segnala più solo valido/non valido ma restituisce anche la motivazione sintetica dell’errore, senza ancora aprire scope su public suffix o registrable domain detection.
  - **Evidenze:** `pytest -q` → `24 passed`; `python -m pylint src tests` → `10.00/10`.

- **`f2b2705` — `docs(project): record B0 application validation progress`**
  - **Type:** `docs` · **Categoria:** Owner docs / B0 application
  - **Cosa cambia:** aggiorna i documenti owner registrando l’introduzione del primo use case applicativo minimale per la validazione dello zone apex input e il relativo avanzamento del blocco `B0`.
  - **Impatto:** allinea la documentazione all’espansione del core dal solo layer `domain` al primo contratto `application`, senza aprire ancora scope su template DNS o superfici web.
  - **Evidenze:** owner docs riallineati al checkpoint reale successivo a `18141f5`; nessuna modifica al codice.

- **`18141f5` — `feat(application): add minimal zone apex validation use case`**
  - **Type:** `feat` · **Categoria:** Application / Use case
  - **Cosa cambia:** introduce il primo use case applicativo minimale per la validazione dello zone apex input, con risultato strutturato semplice e test dedicati nel layer `application`.
  - **Impatto:** rende `B0` più maturo trasformando la validazione da predicato domain isolato a primo contratto applicativo framework-agnostic, senza ancora aprire scope su public suffix, template DNS o superfici web.
  - **Evidenze:** `pytest -q` → `16 passed`; `python -m pylint src tests` → `10.00/10`.

- **`1dd9442` — `docs(project): record B0 initial domain validation progress`**
  - **Type:** `docs` · **Categoria:** Owner docs / B0 baseline
  - **Cosa cambia:** aggiorna i documenti owner registrando la prima apertura operativa di `B0` dopo l’introduzione del validatore sintattico iniziale del dominio apex candidate.
  - **Impatto:** formalizza documentalmente l’avvio del core engine sul dominio apex e allinea i documenti al primo baseline tecnico del blocco.
  - **Evidenze:** owner docs riallineati al checkpoint reale successivo a `9670323`; nessuna modifica al codice.

- **`9670323` — `feat(domain): add initial apex domain candidate validator`**
  - **Type:** `feat` · **Categoria:** Domain / Validation
  - **Cosa cambia:** aggiunge il primo validatore sintattico del dominio apex candidate nel layer `domain` e introduce test automatici minimi per casi validi e non validi.
  - **Impatto:** apre formalmente `B0` con una prima regola forte framework-agnostic sull’input utente della v1, mantenendo però il perimetro conservativo: validazione sintattica DNS/hostname senza ancora risolvere public suffix o registrable domain reali.
  - **Evidenze:** `pytest -q` → `14 passed`; `python -m pylint src tests` → `10.00/10`.

#### A0 — Bootstrap repository, baseline qualità e chiusura documentale
> Ordinamento: `git log` (più recente → più vecchio) · principio truth-first: qui è riportato solo ciò che è consolidato a commit sul branch `development`.

- **`a0787f4` — `docs(project): sync owner docs and README after bootstrap closure`**
  - **Type:** `docs` · **Categoria:** Owner docs / Governance
  - **Cosa cambia:** riallinea `README.md`, `TIMELINE.md`, `ROADMAP.md`, `ARCHITECTURE.md` e `CHANGELOG.md` alla baseline reale del progetto dopo la chiusura del bootstrap, congelando il contratto v1, la direzione Python-first/web-first e la chiusura sostanziale di `A0`.
  - **Impatto:** rende i documenti owner coerenti con lo stato reale del repository e trasforma `A0` in un blocco difendibile sia tecnicamente sia documentalmente.

- **`64278ee` — `feat(bootstrap): add python package skeleton and quality baseline`**
  - **Type:** `feat` · **Categoria:** Bootstrap / Baseline tecnica
  - **Cosa cambia:** introduce lo skeleton Python del progetto, la struttura `src/`, i package base, gli entrypoint tecnici iniziali, i test bootstrap, `.gitignore`, `pyproject.toml` e `requirements.txt` come freeze operativo.
  - **Impatto:** crea la baseline tecnica minima del repository, abilita i quality gate iniziali e rende il progetto realmente eseguibile e verificabile in locale.

**Snapshot quality gate consolidato del bootstrap**
- `.venv` locale pulita creata e verificata;
- `python -m pip install -e ".[dev]"` eseguito con successo;
- `pytest -q` → `4 passed`;
- `python -m pylint src` → `10.00/10`;
- `python -m pylint tests` → `10.00/10`;
- `requirements.txt` rigenerato dalla `.venv` pulita, eliminando il freeze non affidabile derivato dal Python globale.
