# DNS Zone Bootstrapper

Prototipo Python per generare file di zona DNS in formato BIND, pronti per l'import su Cloudflare, a partire da un dominio in input e da un template DNS fisso derivato da un file reale di riferimento fornito dall'azienda, con focus iniziale su automazione orientata a mailcow.

## Fase corrente

Il progetto si trova in fase di bootstrap, freeze documentale e preparazione del core applicativo.

Il file reale di riferimento è stato ricevuto e il contratto v1 è stato chiarito con l'azienda.  
Per la prima versione, il comportamento atteso è il seguente:

- deliverable principale: pagina web;
- input utente: un solo dominio;
- altri valori del template: fissi per ora;
- output: file `.txt` pronto per l'import su Cloudflare;
- preview non necessaria;
- nessuna preferenza di stack imposta dall'azienda.

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
