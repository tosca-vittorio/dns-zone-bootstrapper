# DNS Zone Bootstrapper

Prototipo Python per generare file di zona DNS in formato BIND, pronti per l'import su Cloudflare, a partire da un dominio in input e da un template DNS fisso derivato da un file reale di riferimento, con focus iniziale su automazione orientata.

## Fase corrente

Il progetto ha chiuso il core engine fino a `B3` e ha consolidato il primo incremento tecnico del `Cycle C` con una pagina web minimale su FastAPI, pronta al successivo collegamento del generatore nel blocco `C1`.

Il file reale di riferimento è stato ricevuto e il contratto v1 è stato chiarito.  
Per la prima versione, il comportamento atteso è il seguente:

- deliverable principale: pagina web;
- input utente: un solo dominio;
- altri valori del template: fissi per ora;
- output: file `.txt` pronto per l'import su Cloudflare;
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
python -m uvicorn dns_zone_bootstrapper.interfaces.web.app:app --reload
```

## Direzione architetturale corrente

* core Python-first;
* logica applicativa riusabile e indipendente dall'interfaccia;
* pagina web come superficie principale della v1;
* CLI mantenuta solo come supporto tecnico interno;
* template DNS trattato come profilo fisso interno, pronto a futura estensione senza riscrivere il nucleo del progetto.
