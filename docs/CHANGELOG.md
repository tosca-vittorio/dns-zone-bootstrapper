# CHANGELOG

## Branch: [development]

### [Unreleased]
> Scope corrente: chiusura bootstrap repository/documentazione (`A0`), consolidamento di `B0` sulla validazione sintattica del dominio apex candidate e apertura sostanziale di `B1` con prima baseline versionabile del profilo DNS fisso.

#### B1 — Modello record DNS e profilo template fisso (baseline iniziale)
> Ordinamento: `git log` (più recente → più vecchio) · principio truth-first: qui è riportato solo ciò che è consolidato a commit sul branch `development`.

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
