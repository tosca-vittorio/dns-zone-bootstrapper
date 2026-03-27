# DNS Zone Bootstrapper

Prototipo Python per generare file di zona DNS in formato BIND, orientati al workflow di import su Cloudflare, a partire da un dominio in input e da un template DNS fisso derivato da un file reale di riferimento, con focus iniziale su automazione orientata.

## Fase corrente

Il progetto ha chiuso il core engine fino a `B4` e ha già consolidato il `Cycle C` fino a `C2`, con demo web minimale FastAPI attiva, flusso di generazione/download del file `.txt` disponibile e packaging minimo locale tramite subcommand `dns-zone-cli web`.

L'ultimo consolidamento tecnico (`98ef332`) ha introdotto un boundary runtime per la risoluzione del profilo DNS fisso: `generate_bind_zone_file(...)` non dipende più direttamente dal solo profilo versionato public-safe, ma usa `resolve_active_fixed_dns_profile()`.

Il comportamento runtime attuale è ora il seguente:

- se non esiste alcun override locale gitignored, il runtime usa `PUBLIC_SAFE_FIXED_DNS_PROFILE`;
- se esiste `local.dns_zone_profile` con `ACTIVE_FIXED_DNS_PROFILE`, il runtime usa quel profilo locale come sorgente dei valori fixed concreti;
- il repository versionato resta quindi public-safe per default, mentre i valori operativi concreti possono vivere fuori dal versionamento.

Il file reale di riferimento è stato ricevuto e il contratto v1 è stato chiarito.
Per la prima versione, il comportamento atteso resta il seguente:

- deliverable principale: pagina web;
- input utente: un solo dominio;
- altri valori del template: fissi per ora;
- output target: file `.txt` candidato al workflow di import Cloudflare;
- preview non necessaria;
- nessuna preferenza di stack imposta.

## Obiettivi del prototipo

- validare un dominio apex come input minimo;
- applicare un template DNS fisso derivato dal caso reale;
- generare un file di zona BIND compatibile con l'import Cloudflare;
- esporre il core tramite una pagina web minimale;
- mantenere il nucleo del progetto riusabile per future estensioni.

## Struttura del repository

```text
docs/                          documenti owner
src/dns_zone_bootstrapper/     codice applicativo
tests/                         test e fixture golden
```

## Bootstrap locale

```bash
python -m pip install -e ".[dev]"
pytest -q
dns-zone-cli doctor
dns-zone-cli web
# alternativa tecnica equivalente:
python -m uvicorn dns_zone_bootstrapper.interfaces.web.app:app --reload
```

## Direzione architetturale corrente

* core Python-first;
* logica applicativa riusabile e indipendente dall'interfaccia;
* pagina web come superficie principale della v1;
* CLI mantenuta solo come supporto tecnico interno;
* template DNS trattato come profilo fisso interno, pronto a futura estensione senza riscrivere il nucleo del progetto.
