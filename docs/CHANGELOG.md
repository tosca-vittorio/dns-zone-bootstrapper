# CHANGELOG

## Branch: [development]

### [Unreleased]
- Bootstrap del repository per il progetto `dns-zone-bootstrapper`.
- Inizializzazione dei documenti owner (`TIMELINE.md`, `ROADMAP.md`, `ARCHITECTURE.md`, `CHANGELOG.md`).
- Definizione della baseline Python-first con package `src/`, superfici tecniche minime e verifiche locali iniziali.
- Promozione di `TIMELINE.md` a documento operativo centrale, senza dipendere da un backlog separato esterno.
- Ricezione del file reale di riferimento fornito dall'azienda e congelamento del contratto v1 della task.
- Conferma dei vincoli v1:
  - deliverable principale = pagina web;
  - input utente = solo dominio;
  - valori restanti = fissi per ora;
  - output = file `.txt` pronto per import Cloudflare;
  - preview non necessaria;
  - nessuna preferenza di stack imposta dall'azienda.
- Ricollocazione del file reale di riferimento in area locale privata gitignored (`samples/private/company_reference/`) per evitare tracciamento grezzo nel repository.
- Riallineamento di `README.md`, `ROADMAP.md`, `TIMELINE.md` e `ARCHITECTURE.md` al nuovo stato del progetto.
- Decisione di governance: `pylint` promosso a quality gate della baseline dev del progetto.
- Decisione di governance: `requirements.txt` mantenuto come freeze operativo versionato, da aggiornare solo a checkpoint significativi dell'ambiente.
- Verificato il baseline dev environment tramite `python -m pip install -e ".[dev]"`.
- Eseguiti con esito verde i quality gate iniziali: `pytest` (`4 passed`) e `pylint` (`10.00/10` su `src` e `tests`).
- Creata e verificata `.venv` locale pulita come baseline isolata del progetto.
- Rigenerato `requirements.txt` dalla `.venv` pulita, eliminando il freeze non affidabile derivato dal Python globale.