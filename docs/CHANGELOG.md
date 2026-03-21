# CHANGELOG

## Branch: [development]

### [Unreleased]
> Scope corrente: chiusura bootstrap repository/documentazione (`A0`) e prima iterazione del core su `B0` con validazione sintattica iniziale del dominio apex candidate.

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

#### B0 — Validazione dominio apex (prima iterazione sintattica)
> Ordinamento: `git log` (più recente → più vecchio) · focus su primo avanzamento reale del core engine.

- **`4771e11` — `test(domain): cover remaining zone apex validation failures`**
  - **Type:** `test` · **Categoria:** Domain / Validation tests
  - **Cosa cambia:** completa la copertura del layer `domain` aggiungendo test espliciti per i failure mode `non_string_input` e `domain_too_long`, già supportati dalla validazione strutturata del dominio apex candidate.
  - **Impatto:** rende `B0` più difendibile e più completo sul piano dei test, senza modificare il comportamento del codice e senza aprire nuovo scope oltre la validazione sintattica corrente.
  - **Evidenze:** `pytest -q` → `26 passed`; `python -m pylint src tests` → `10.00/10`.

- **`f5f579d` — `feat(domain): add structured zone apex validation errors`**
  - **Type:** `feat` · **Categoria:** Domain / Validation
  - **Cosa cambia:** evolve la validazione del dominio apex da semplice predicato booleano a risultato strutturato con `error_code` deterministici per i principali failure mode sintattici, mantenendo un wrapper booleano compatibile e aggiornando i test del layer `domain` e del layer `application`.
  - **Impatto:** rende `B0` più robusto e più consumabile dalle future superfici applicative, perché l’esito della validazione non segnala più solo valido/non valido ma restituisce anche la motivazione sintetica dell’errore, senza ancora aprire scope su public suffix o registrable domain detection.
  - **Evidenze:** `pytest -q` → `24 passed`; `python -m pylint src tests` → `10.00/10`.

- **`18141f5` — `feat(application): add minimal zone apex validation use case`**
  - **Type:** `feat` · **Categoria:** Application / Use case
  - **Cosa cambia:** introduce il primo use case applicativo minimale per la validazione dello zone apex input, con risultato strutturato semplice e test dedicati nel layer `application`.
  - **Impatto:** rende `B0` più maturo trasformando la validazione da predicato domain isolato a primo contratto applicativo framework-agnostic, senza ancora aprire scope su public suffix, template DNS o superfici web.
  - **Evidenze:** `pytest -q` → `16 passed`; `python -m pylint src tests` → `10.00/10`.

- **`9670323` — `feat(domain): add initial apex domain candidate validator`**
  - **Type:** `feat` · **Categoria:** Domain / Validation
  - **Cosa cambia:** aggiunge il primo validatore sintattico del dominio apex candidate nel layer `domain` e introduce test automatici minimi per casi validi e non validi.
  - **Impatto:** apre formalmente `B0` con una prima regola forte framework-agnostic sull’input utente della v1, mantenendo però il perimetro conservativo: validazione sintattica DNS/hostname senza ancora risolvere public suffix o registrable domain reali.
  - **Evidenze:** `pytest -q` → `14 passed`; `python -m pylint src tests` → `10.00/10`.
