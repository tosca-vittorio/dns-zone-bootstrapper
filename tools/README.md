# Tools — cleanup_runtime_artifacts.py

Questo repository include il tool `tools/cleanup_runtime_artifacts.py` per la pulizia **conservativa** degli artefatti runtime repo-locali.

## Obiettivo

Ridurre rumore locale e residui di esecuzione mantenendo un comportamento:

- **safe by default**
- **evidence-first**
- coerente con un repository **Python-first**
- compatibile con l’ambiente reale del progetto su Windows / Git Bash / venv locale

Il tool è pensato per rimuovere solo artefatti rigenerabili, senza toccare per default boundary protetti o directory locali sensibili.

---

## Boundary e principi di sicurezza

Per default il tool:

- opera dalla root reale del repository, derivata dalla posizione del file
- verifica la presenza dei marker minimi della repo:
  - `README.md`
  - `pyproject.toml`
  - `src`
- protegge sempre:
  - `.git/`
  - `tmp/`
- esclude per default gli ambienti virtuali:
  - `.venv/`
  - `venv/`
  - `env/`
  - `ENV/`

Questo evita cancellazioni accidentali fuori perimetro e preserva il boundary canonico del progetto.

---

## Cosa pulisce di default

Senza flag opt-in, il tool considera solo artefatti runtime **repo-locali** fuori da `.git/`, `tmp/` e venv.

### Directory artifacts
- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- `htmlcov/`
- `.tox/`
- `.nox/`
- `build/`
- `dist/`
- `*.egg-info/`

### Compiled Python files
- `*.pyc`
- `*.pyo`

### Coverage files
- `.coverage`
- `.coverage.*`
- `coverage.xml`

---

## Cosa NON pulisce di default

Per ridurre il rischio operativo, il tool non tocca automaticamente:

- `.git/`
- `tmp/`
- `.venv/`, `venv/`, `env/`, `ENV/`

In particolare, `tmp/` è un boundary protetto del repository e non rientra nella pulizia standard.

---

## Modalità d’uso

### Dry-run
Mostra cosa verrebbe rimosso senza cancellare nulla.

```bash
python tools/cleanup_runtime_artifacts.py
```

### Apply reale

Applica la rimozione dei target trovati.

```bash
python tools/cleanup_runtime_artifacts.py --apply
```

### Verbose

Mostra in output i singoli path coinvolti.

```bash
python tools/cleanup_runtime_artifacts.py --verbose
python tools/cleanup_runtime_artifacts.py --apply --verbose
```

---

## Opt-in disponibili

### `--include-venv`

Abilita la pulizia **soft** dentro gli ambienti virtuali.

Quando questo flag è attivo, nella venv vengono considerati **solo**:

* `__pycache__/`
* `*.pyc`
* `*.pyo`

Non vengono invece promossi dentro la venv altri target repo-level come:

* `build/`
* `dist/`
* `htmlcov/`
* `.coverage`
* `.pytest_cache`
* `*.egg-info`

Esempio:

```bash
python tools/cleanup_runtime_artifacts.py --include-venv
python tools/cleanup_runtime_artifacts.py --include-venv --apply
```

### `--skip-root-guard`

Disabilita il controllo dei marker di root.

Uso sconsigliato, da riservare solo a casi eccezionali di debugging controllato.

```bash
python tools/cleanup_runtime_artifacts.py --skip-root-guard
```

---

## Output atteso

Il tool stampa sempre:

* versione dello script
* modalità (`DRY-RUN` oppure `APPLY`)
* `repo_root`
* stato di `include_venv`

Quando trova target, li raggruppa in sezioni:

* `1) Directory artifacts`
* `2) Compiled Python files`
* `3) Coverage files`

Per ogni sezione mostra il numero di item rilevati.
In dry-run mostra anche i path previsti in rimozione.
In apply stampa il riepilogo finale con:

* `items_removed_or_proposed=N`

Se non trova nulla, restituisce:

```text
No cleanup targets found inside repo-owned boundaries.
```

---

## Workflow consigliato

Prima:

```bash
git status -sb
python tools/cleanup_runtime_artifacts.py
```

Applicazione reale:

```bash
python tools/cleanup_runtime_artifacts.py --apply
```

Verifica finale:

```bash
python tools/cleanup_runtime_artifacts.py
git status -sb
```

---

## Failure mode / note operative

### File lock su Windows

Se un file o una directory sono in uso, la rimozione può fallire con warning esplicito.
In quel caso il tool non nasconde il problema: lo espone e termina con codice non nullo se restano failure.

### Nessun target trovato

È uno stato valido e desiderabile quando la working tree è già pulita rispetto agli artefatti runtime repo-locali.

### Venv molto grande

Con `--include-venv` il numero di target può essere elevato. È normale: la pulizia resta comunque limitata ai soli `__pycache__/`, `*.pyc`, `*.pyo`.

---

## File location

* Script canonico: `tools/cleanup_runtime_artifacts.py`
* Documentazione tool: `tools/README.md`
