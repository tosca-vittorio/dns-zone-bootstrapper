# CHANGELOG

## Branch: [development]

### [Unreleased]
> Scope corrente: chiusura bootstrap repository/documentazione (`A0`), consolidamento di `B0` sulla validazione sintattica del dominio apex candidate, hardening progressivo di `B1` sul profilo DNS fisso public-safe versionabile, apertura minima di `B2` con primo renderer BIND verificato, hardening del contratto testuale tramite golden file esterno e placeholder derivati, introduzione del boundary applicativo minimo di generazione del file BIND, deduplicazione qualitativa delle assertion condivise tra renderer puro e use case applicativo e copertura di failure path applicativi aggiuntivi su input overlong, vuoto, privo di dot, con dot iniziale, con dot finale, con label vuota, con label non valida e su input non stringa, oltre a una copertura renderer-focused sul quoting dei record `TXT`, sulle annotazioni `cf_tags`, su un freeze esplicito della presenza, unicità e ordine dei section headers del renderer BIND, sull'assenza di annotazioni `cf_tags` per record senza stato proxy esplicito, sul failure path esplicito per `record_type` non supportato, sulla gestione strutturata del failure interno del renderer nel boundary `application` con `error_code="renderer_failure"`, sull'indipendenza del grouping delle sezioni rispetto all'ordine del profilo tramite test su record interleaved e fix runtime dedicato, sul riallineamento del contratto dichiarato del layer `application` ai failure strutturati su input non stringa già supportati a runtime, sull'hardening del failure translation boundary applicativo anche per `RuntimeError` interni del renderer e sul freeze esplicito del contratto di short-circuit applicativo che evita l'invocazione del renderer sui failure di validazione input, sul freeze esplicito del success-call contract del boundary `application`, che congela l'invocazione del renderer con `zone_apex` validato e `PUBLIC_SAFE_FIXED_DNS_PROFILE`, sul freeze esplicito dell'ordine relativo intra-sezione dei record dello stesso tipo nel renderer BIND, sul freeze esplicito dell'omissione delle sezioni vuote nel renderer BIND quando il profilo contiene solo un sottoinsieme dei record supportati, sul freeze esplicito dell'assenza di blank line spurie nel renderer BIND su output a sezione unica e sul freeze esplicito della separazione tramite esattamente una sola blank line tra sezioni popolate consecutive del renderer BIND.
> Ultimo consolidamento: apertura documentale di `B3` dopo audit read-only completato sul candidato v1, con timeline riallineata allo stato reale, quality gates globali già verdi (`67 passed`, `pylint 10.00/10`) e branch allineato a `origin/development`.

#### B3 — Test del generatore e preparazione fixture reali
> Ordinamento: `git log` (più recente → più vecchio) · principio truth-first: qui è riportato solo ciò che è consolidato a commit sul branch `development`.

- **`2ed6f52` — `docs(timeline): open B3 from completed read-only audit`**
  - **Type:** `docs` · **Categoria:** Owner docs / Timeline / B3 opening
  - **Cosa cambia:** aggiorna `docs/TIMELINE.md` aprendo operativamente `B3` sul piano documentale, registra l'audit read-only completato tra golden versionati, riferimento reale locale gitignored, snapshot normalizzato locale, profilo runtime, renderer e boundary `application`, e fissa come primo passo corretto la futura creazione di una fixture versionata, public-safe e realistic-backed sotto `tests/golden`.
  - **Impatto:** sposta il progetto fuori dalla sola preparazione teorica di `B3`, rende esplicito che il confronto realistico non ha evidenziato gap strutturali sul candidato v1 e prepara il primo avanzamento concreto del blocco senza toccare ancora runtime, UI/web o refactor larghi.
  - **Evidenze:** branch allineato a `origin/development`; commit `2ed6f52` pubblicato; `python -m pytest -q` → `67 passed`; `python -m pylint src tests` → `10.00/10`.

#### B2 — Renderer BIND zone file
> Ordinamento: `git log` (più recente → più vecchio) · principio truth-first: qui è riportato solo ciò che è consolidato a commit sul branch `development`.

- **`07272ff` — `docs(timeline): close B2 and prepare B3 opening`**
  - **Type:** `docs` · **Categoria:** Owner docs / Timeline / Cycle transition
  - **Cosa cambia:** aggiorna `docs/TIMELINE.md` chiudendo formalmente `B2`, riallineando fase corrente, obiettivo immediato, ultimo consolidamento e nota di chiusura del blocco, e prepara `B3` come prossimo step operativo del core.
  - **Impatto:** impedisce ulteriore hardening marginale dentro `B2`, fissa documentalmente la soglia di uscita del blocco e rende `B3` il prossimo contenitore corretto per fixture e confronti più realistici, senza aprire nello stesso passaggio scope su UI/web o refactor larghi.
  - **Evidenze:** `python -m pytest -q` → `67 passed`; `python -m pylint src tests` → `10.00/10`; branch allineato a `origin/development`.

- **`2a9b10d` — `test(application): freeze golden renderer failure call contract`**
  - **Type:** `test` · **Categoria:** Application / Golden renderer failure-call contract freeze
  - **Cosa cambia:** irrigidisce `tests/test_bind_zone_generation_use_case.py` sul failure path golden di `generate_bind_zone_file("testdomain.com")`, congelando non solo il risultato strutturato di `renderer_failure` ma anche l'invocazione del renderer una sola volta con `zone_apex="testdomain.com"` e `profile=PUBLIC_SAFE_FIXED_DNS_PROFILE` quando `render_bind_zone_file(...)` fallisce con `ValueError`.
  - **Impatto:** rende `B2` più difendibile sul lato `application`, perché il percorso golden di failure non è più protetto soltanto sul risultato restituito ma anche sul contratto esplicito di orchestrazione verso il renderer, senza modificare il runtime del package e senza aprire nuovo scope su renderer runtime, CLI, web o fixture reali.
  - **Evidenze:** `python -m pytest -q tests/test_bind_zone_generation_use_case.py` → `19 passed`; `python -m pytest -q` → `67 passed`; `python -m pylint src tests` → `10.00/10`.

- **`8f8530d` — `test(application): freeze non-golden renderer failure call contract`**
  - **Type:** `test` · **Categoria:** Application / Non-golden renderer failure-call contract freeze
  - **Cosa cambia:** irrigidisce `tests/test_bind_zone_generation_use_case.py` sul failure path non-golden di `generate_bind_zone_file("alpha-zone.example.org")`, congelando non solo il risultato strutturato di `renderer_failure` ma anche l'invocazione del renderer una sola volta con `zone_apex="alpha-zone.example.org"` e `profile=PUBLIC_SAFE_FIXED_DNS_PROFILE` quando `render_bind_zone_file(...)` fallisce con `RuntimeError`.
  - **Impatto:** rende `B2` più difendibile sul lato `application`, perché il percorso non-golden di failure non è più protetto soltanto sul risultato restituito ma anche sul contratto esplicito di orchestrazione verso il renderer, senza modificare il runtime del package e senza aprire nuovo scope su renderer runtime, CLI, web o fixture reali.
  - **Evidenze:** `python -m pytest -q tests/test_bind_zone_generation_use_case.py` → `19 passed`; `python -m pytest -q` → `67 passed`; `python -m pylint src tests` → `10.00/10`.

- **`68e6690` — `test(application): freeze non-golden renderer failure boundary`**
  - **Type:** `test` · **Categoria:** Application / Non-golden renderer failure boundary freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato che, per `alpha-zone.example.org`, patcha `render_bind_zone_file(...)` con un `RuntimeError`, congela la traduzione strutturata in `error_code="renderer_failure"` e verifica la preservazione di `zone_apex="alpha-zone.example.org"` con `zone_file_text=None`.
  - **Impatto:** rende `B2` più difendibile sul lato `application`, perché il percorso non-golden viene ora protetto anche sul boundary di failure del renderer e non solo sul risultato di successo o sul contratto di orchestrazione, senza modificare il runtime del package e senza aprire nuovo scope su renderer runtime, CLI, web o fixture reali.
  - **Evidenze:** `python -m pytest -q tests/test_bind_zone_generation_use_case.py` → `19 passed`; `python -m pytest -q` → `67 passed`; `python -m pylint src tests` → `10.00/10`.

- **`65b4692` — `test(application): freeze non-golden success call contract`**
  - **Type:** `test` · **Categoria:** Application / Non-golden success-call contract freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato che, per `alpha-zone.example.org`, patcha `render_bind_zone_file(...)`, congela la corretta invocazione del renderer con `zone_apex="alpha-zone.example.org"` e `profile=PUBLIC_SAFE_FIXED_DNS_PROFILE`, e verifica la propagazione del testo mocked nel `BindZoneFileGenerationResult` di successo.
  - **Impatto:** rende `B2` più difendibile sul lato `application`, perché il percorso non-golden non è più protetto soltanto sul risultato finale ma anche sul contratto esplicito di orchestrazione verso il renderer, senza modificare il runtime del package e senza aprire nuovo scope su renderer runtime, CLI, web o fixture reali.
  - **Evidenze:** `python -m pytest -q tests/test_bind_zone_generation_use_case.py` → `18 passed`; `python -m pytest -q` → `66 passed`; `python -m pylint src tests` → `10.00/10`.

- **`2338ad3` — `test(application): freeze full structured non-golden success result`**
  - **Type:** `test` · **Categoria:** Application / Structured non-golden success result freeze
  - **Cosa cambia:** aggiorna `tests/test_bind_zone_generation_use_case.py` irrigidendo il test sul percorso non-golden contro il golden dedicato `tests/golden/public_safe_candidate.alpha-zone-example-org.bind.txt`, che non verifica più soltanto `error_code`, `zone_apex` e `zone_file_text`, ma congela ora l'intero `BindZoneFileGenerationResult` di successo restituito da `generate_bind_zone_file("alpha-zone.example.org")`.
  - **Impatto:** rende `B2` più difendibile sul lato `application`, perché il boundary non-golden viene ora protetto sull'intera superficie del risultato strutturato e non solo su un sottoinsieme di campi, senza modificare il runtime del package e senza aprire nuovo scope su renderer runtime, CLI, web o fixture reali.
  - **Evidenze:** `python -m pytest -q tests/test_bind_zone_generation_use_case.py` → `17 passed`; `python -m pytest -q` → `65 passed`; `python -m pylint src tests` → `10.00/10`.

- **`f6538dc` — `test(application): freeze non-golden golden file output`**
  - **Type:** `test` · **Categoria:** Application / Non-golden golden file freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato che legge il golden file `tests/golden/public_safe_candidate.alpha-zone-example-org.bind.txt` e congela esplicitamente che `generate_bind_zone_file("alpha-zone.example.org")` restituisca nel boundary `application` esattamente il full-text atteso dal golden dedicato, oltre a verificare `error_code is None` e la preservazione di `zone_apex`.
  - **Impatto:** rende `B2` più difendibile sul lato `application`, perché il percorso non-golden non dipende più soltanto dal confronto di parità con il renderer puro ma è ora protetto anche da un freeze testuale completo diretto contro il golden dedicato, senza modificare il runtime del package e senza aprire nuovo scope su renderer runtime, CLI, web o fixture reali.
  - **Evidenze:** `python -m pytest -q tests/test_bind_zone_generation_use_case.py` → `17 passed`; `python -m pytest -q` → `65 passed`; `python -m pylint src tests` → `10.00/10`.

- **`89a92ae` — `test(renderer): freeze derived-token-only non-golden golden delta`**
  - **Type:** `test` · **Categoria:** Renderer / Golden delta invariance freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_renderer.py` con un test dedicato che legge i due golden file `tests/golden/public_safe_candidate.bind.txt` e `tests/golden/public_safe_candidate.alpha-zone-example-org.bind.txt`, congela l'assenza dei token dell'uno nel testo dell'altro e verifica che, dopo la normalizzazione dei soli token derivati attesi dell'apex (`alpha-zone.example.org.` → `testdomain.com.` e `alpha-zone-example-org` → `testdomain-com`), i due file coincidano byte-for-byte.
  - **Impatto:** formalizza in modo esplicito l'audit read-only sul delta tra golden baseline e golden non-golden del renderer puro, rendendo `B2` più difendibile contro derive strutturali silenziose nel full-text e congelando che il differenziale ammesso resti confinato ai soli derivati dell'apex, senza modificare il runtime del package e senza aprire nuovo scope su `application`, CLI, web o fixture reali.
  - **Evidenze:** `python -m pytest -q` → `64 passed`; `python -m pylint src tests` → `10.00/10`.

- **`f8c8331` — `test(renderer): freeze non-golden full-text golden output`**
  - **Type:** `test` · **Categoria:** Renderer / Non-golden full-text golden freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_renderer.py` con un test dedicato che confronta l'output completo di `render_bind_zone_file(...)` per `alpha-zone.example.org` con un nuovo golden file dedicato `tests/golden/public_safe_candidate.alpha-zone-example-org.bind.txt`, introducendo così un freeze full-text indipendente del percorso non-golden del renderer puro.
  - **Impatto:** rende più difendibile `B2` sul lato renderer, perché il percorso non-golden non dipende più soltanto da assertion condivise di sottoinsieme o da confronti mediati dal boundary `application`, senza modificare il runtime del package e senza aprire nuovo scope su CLI, web o fixture reali esterne.
  - **Evidenze:** `python -m pytest -q` → `63 passed`; `python -m pylint src tests` → `10.00/10`.

- **`895e161` — `test(application): freeze non-golden full-text renderer parity`**
  - **Type:** `test` · **Categoria:** Application / Non-golden full-text parity freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato che, per `alpha-zone.example.org`, confronta il `zone_file_text` prodotto da `generate_bind_zone_file(...)` con il testo completo restituito dal renderer puro `render_bind_zone_file(...)` invocato con `PUBLIC_SAFE_FIXED_DNS_PROFILE`.
  - **Impatto:** rende più difendibile il boundary `application` sul percorso non-golden, perché aggiunge un freeze esplicito di coerenza full-text cross-layer e non lascia più quel percorso coperto soltanto da assertion condivise su un sottoinsieme del contratto, senza modificare il runtime del package e senza aprire nuovo scope su CLI, web o fixture reali.
  - **Evidenze:** `python -m pytest -q` → `62 passed`; `python -m pylint src tests` → `10.00/10`.

- **`5a52bc4` — `test(renderer): harden shared non-golden rendering contract`**
  - **Type:** `test` · **Categoria:** Renderer / Application / Shared non-golden contract hardening
  - **Cosa cambia:** irrigidisce `tests/shared_bind_zone_assertions.py`, che non congela più solo tre linee `CNAME` derivate e l'assenza di newline finale, ma anche presenza, unicità e ordine dei section headers `A`, `CNAME`, `MX`, `SRV`, `TXT`, un insieme rappresentativo cross-section di linee renderizzate per `alpha-zone.example.org` e l'assenza di placeholder raw residui `{apex}`, `{apex_fqdn}`, `{apex_slug}`; il contratto resta condiviso e riusato sia dal renderer puro sia dal use case `application`.
  - **Impatto:** rende più difendibile il contratto condiviso non-golden del core, perché riduce il rischio che una regressione coerente tra renderer e boundary `application` passi ancora attraverso assertion troppo deboli, senza modificare il runtime del package e senza aprire nuovo scope su CLI, web o fixture reali.
  - **Evidenze:** `python -m pytest -q` → `61 passed`; `python -m pylint src tests` → `10.00/10`.

- **`ce15d46` — `test(renderer): freeze multi-section blank-line separation`**
  - **Type:** `test` · **Categoria:** Renderer / Multi-section blank-line separation contract freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_renderer.py` con un test dedicato che congela esplicitamente, nel renderer BIND, la separazione tramite esattamente una sola blank line tra sezioni popolate consecutive, verificando il comportamento su un profilo multi-section parziale `A`/`MX`/`TXT`.
  - **Impatto:** rende il renderer più difendibile sul piano contrattuale, perché la separazione tra sezioni consecutive popolate non resta più solo implicita nel golden file completo o in assunzioni indirette di altri test ma viene protetta da un test mirato e focalizzato, senza aprire nuovo scope su `application`, `domain`, CLI o web.
  - **Evidenze:** `python -m pytest -q tests/test_bind_zone_renderer.py` → `12 passed`.

- **`110febe` — `test(renderer): freeze single-section blank-line contract`**
  - **Type:** `test` · **Categoria:** Renderer / Single-section blank-line contract freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_renderer.py` con un test dedicato che congela esplicitamente, nel renderer BIND, l'assenza di newline iniziale, newline finale e blank line spurie quando l'output contiene una sola sezione `TXT`.
  - **Impatto:** rende il renderer più difendibile sul piano contrattuale, perché la pulizia strutturale minima dell'output su profili a sezione unica non resta più solo implicita nell'implementazione corrente ma viene protetta da un test mirato, senza aprire nuovo scope su `application`, `domain`, CLI o web.
  - **Evidenze:** `python -m pytest -q` → `60 passed`; `python -m pylint src tests` → `10.00/10`.

- **`666efe7` — `test(renderer): freeze empty section omission`**
  - **Type:** `test` · **Categoria:** Renderer / Empty section omission contract freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_renderer.py` con un test dedicato che congela esplicitamente, nel renderer BIND, l'omissione delle sezioni vuote quando il profilo contiene solo un sottoinsieme dei record supportati, verificando l'emissione delle sole sezioni presenti in un profilo parziale `A`/`TXT`.
  - **Impatto:** rende il renderer più difendibile sul piano contrattuale, perché l'assenza di header vuoti e di sezioni non presenti nel profilo non resta più solo implicita nell'implementazione corrente ma viene protetta da un test mirato, senza aprire nuovo scope su `application`, `domain`, CLI o web.
  - **Evidenze:** `python -m pytest -q` → `59 passed`; `python -m pylint src tests` → `10.00/10`.

- **`2b0c015` — `test(renderer): freeze intra-section relative order`**
  - **Type:** `test` · **Categoria:** Renderer / Intra-section ordering contract freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_renderer.py` con un test dedicato che congela esplicitamente, nel renderer BIND, la preservazione dell'ordine relativo di input dei record dello stesso tipo all'interno della sezione `CNAME`, anche in presenza di profilo interleaved.
  - **Impatto:** rende il renderer più difendibile sul piano contrattuale, perché l'ordine intra-sezione non resta più solo implicito nell'implementazione corrente ma viene protetto da un test mirato, senza aprire nuovo scope su `application`, `domain`, CLI o web.
  - **Evidenze:** `python -m pytest -q` → `58 passed`; `python -m pylint src tests` → `10.00/10`.

- **`1857c1d` — `test(application): freeze renderer success-call contract`**
  - **Type:** `test` · **Categoria:** Application / Success-call contract freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato che congela esplicitamente il percorso di successo del boundary `application`, verificando che `generate_bind_zone_file(...)` invochi `render_bind_zone_file(...)` una sola volta con `zone_apex` validato e `profile=PUBLIC_SAFE_FIXED_DNS_PROFILE`, e che propaghi nel risultato strutturato il testo ritornato dal renderer.
  - **Impatto:** rende il boundary `application` più difendibile sul piano contrattuale, perché l'orchestrazione del success path non resta più solo implicita nell'output end-to-end ma viene protetta da un test esplicito e mirato, senza aprire nuovo scope su `domain`, renderer, CLI o web.
  - **Evidenze:** `python -m pytest -q` → `57 passed`; `python -m pylint src tests` → `10.00/10`.

- **`e56afef` — `test(application): freeze short-circuit on validation failure`**
  - **Type:** `test` · **Categoria:** Application / Short-circuit contract freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato che forza un failure di validazione (`surrounding_whitespace`) e congela esplicitamente che `generate_bind_zone_file(...)` restituisca il failure strutturato senza invocare `render_bind_zone_file(...)`.
  - **Impatto:** rende il boundary `application` più difendibile sul piano contrattuale, perché il non-invocare il renderer in presenza di input invalido non resta più solo implicito nell'implementazione corrente ma viene protetto da un test esplicito e mirato, senza aprire nuovo scope su `domain`, renderer, CLI o web.
  - **Evidenze:** `python -m pytest -q` → `56 passed`; `python -m pylint src tests` → `10.00/10`.

- **`66f8c3d` — `fix(application): harden renderer failure translation boundary`**
  - **Type:** `fix` · **Categoria:** Application / Renderer failure translation hardening
  - **Cosa cambia:** aggiorna `src/dns_zone_bootstrapper/application/bind_zone_generation.py` facendo sì che `generate_bind_zone_file(...)` traduca in `error_code="renderer_failure"` non solo `ValueError` ma anche `RuntimeError` interni del renderer; estende inoltre `tests/test_bind_zone_generation_use_case.py` con un test dedicato che congela esplicitamente il caso di failure renderer non-`ValueError`.
  - **Impatto:** rende il boundary `application` più robusto e più esplicito sul piano contrattuale, perché la traduzione dei failure interni del renderer non dipende più solo dal caso `ValueError` già coperto in precedenza, senza aprire nuovo scope su `domain`, renderer, CLI o web.
  - **Evidenze:** `python -m pytest -q` → `55 passed`; `python -m pylint src tests` → `10.00/10`.

- **`4733c97` — `fix(application): align input contract with structured non string failures`**
  - **Type:** `fix` · **Categoria:** Application / Contract surface alignment
  - **Cosa cambia:** aggiorna `src/dns_zone_bootstrapper/application/zone_apex_validation.py` e `src/dns_zone_bootstrapper/application/bind_zone_generation.py` riallineando `input_value` da `str` a `object` nei result object e nelle firme dei use case `validate_zone_apex_input(...)` e `generate_bind_zone_file(...)`, così da rendere il contratto dichiarato coerente con i failure strutturati su input non stringa già supportati dal runtime; estende inoltre `tests/test_zone_apex_validation_use_case.py` con un test dedicato che congela `non_string_input` anche sul boundary applicativo minimale di validazione.
  - **Impatto:** rende il boundary `application` più coerente e più leggibile sul piano contrattuale, perché la type surface esposta non dichiara più un input artificialmente ristretto rispetto al comportamento reale già supportato sui failure strutturati, senza aprire nuovo scope su `domain`, renderer, CLI o web.
  - **Evidenze:** `python -m pytest -q` → `54 passed`; `python -m pylint src tests` → `10.00/10`.

- **`85203cf` — `fix(renderer): group bind sections independently from profile order`**
  - **Type:** `fix` · **Categoria:** Renderer / Section grouping hardening
  - **Cosa cambia:** aggiorna `src/dns_zone_bootstrapper/renderers/bind_zone_renderer.py` affinché il renderer BIND raccolga prima i record per tipo supportato e poi li emetta nell'ordine canonico delle sezioni `A`, `CNAME`, `MX`, `SRV`, `TXT`, rendendo così il grouping indipendente dall'ordine di `profile.records`; estende inoltre `tests/test_bind_zone_renderer.py` con un test dedicato su profilo artificiale con record interleaved che congela unicità delle sezioni e ordering canonico anche quando i record in input non sono contigui per tipo.
  - **Impatto:** rende il contratto del renderer più robusto e più esplicito, perché l'apertura delle sezioni non dipende più implicitamente dall'ordine corrente del profilo public-safe ma da una logica interna deterministica del renderer, senza aprire nuovo scope su `application`, CLI o web.
  - **Evidenze:** `python -m pytest -q` → `53 passed`; `python -m pylint src tests` → `10.00/10`.

- **`5cf0c05` — `test(application): harden bind zone renderer failure handling`**
  - **Type:** `test` · **Categoria:** Application / Renderer failure contract hardening
  - **Cosa cambia:** irrigidisce `src/dns_zone_bootstrapper/application/bind_zone_generation.py` facendo sì che il use case `generate_bind_zone_file` intercetti i failure interni del renderer e restituisca un esito strutturato con `error_code="renderer_failure"`, `zone_file_text=None` e `zone_apex` preservato quando l'input è valido; estende inoltre `tests/test_bind_zone_generation_use_case.py` con un test dedicato che forza il renderer a fallire e congela il nuovo comportamento.
  - **Impatto:** rende il boundary `application` più robusto e più leggibile sul piano contrattuale, perché un fallimento interno del renderer non propaga più un'eccezione grezza verso l'esterno ma viene trasformato in un risultato strutturato coerente con gli altri failure path del use case, senza aprire ancora scope su CLI, web o fixture reali.
  - **Evidenze:** `python -m pytest -q` → `52 passed`; `python -m pylint src tests` → `10.00/10`.

- **`bff112d` — `test(renderer): harden unsupported bind record type failure`**
  - **Type:** `test` · **Categoria:** Renderer / Failure contract hardening
  - **Cosa cambia:** rende esplicito nel renderer BIND il failure path per `record_type` non supportato introducendo un `ValueError` deterministico al posto del precedente `KeyError` implicito sul mapping `_SECTION_TITLES`, ed estende `tests/test_bind_zone_renderer.py` con un test dedicato che congela il comportamento su un record artificiale con tipo `AAAA`.
  - **Impatto:** rende il contratto del renderer più difendibile e più leggibile sul piano semantico, perché in caso di profilo malformato o futuro drift fuori vocabolario il fallimento non dipende più da un errore accidentale di lookup ma da un errore esplicito e intenzionale, senza aprire nuovo scope su `application`, CLI o web.
  - **Evidenze:** `python -m pytest -q` → `51 passed`; `python -m pylint src tests` → `10.00/10`.

- **`1840aab` — `test(renderer): cover missing cf tags bind zone output`**
  - **Type:** `test` · **Categoria:** Renderer / Cloudflare annotation contract coverage
  - **Cosa cambia:** estende `tests/test_bind_zone_renderer.py` con un test dedicato che verifica esplicitamente l'assenza di annotazioni `cf_tags` nell'output BIND per record del profilo public-safe privi di stato proxy esplicito, coprendo casi rappresentativi come `MX` e `TXT`.
  - **Impatto:** rende più completo e più difendibile il contratto del renderer sulle annotazioni Cloudflare, perché congela non solo i casi `cf-proxied:true/false` ma anche l'omissione corretta delle annotazioni quando il proxy state non è definito, senza modificare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `50 passed`; `python -m pylint src tests` → `10.00/10`.

- **`bc4f648` — `test(renderer): freeze bind section header order`**
  - **Type:** `test` · **Categoria:** Renderer / Section header contract freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_renderer.py` con un test dedicato che congela esplicitamente presenza, unicità e ordine dei section headers `A`, `CNAME`, `MX`, `SRV` e `TXT` nell'output BIND del profilo public-safe.
  - **Impatto:** rende più esplicito e più difendibile il contratto corrente del renderer sui blocchi sezione dell'output, riducendo il rischio di drift silenzioso su headers e ordering senza modificare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `49 passed`; `python -m pylint src tests` → `10.00/10`.

- **`f97cd44` — `test(renderer): cover cf tags bind zone annotations`**
  - **Type:** `test` · **Categoria:** Renderer / Contract coverage
  - **Cosa cambia:** estende `tests/test_bind_zone_renderer.py` con un test mirato che verifica esplicitamente la resa delle annotazioni `cf_tags` nell'output BIND renderizzato, coprendo sia il caso `cf-proxied:true` sia il caso `cf-proxied:false`.
  - **Impatto:** rafforza ulteriormente il contratto del renderer su una parte semantica load-bearing dell'output emesso, senza modificare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `48 passed`; `python -m pylint src tests` → `10.00/10`.

- **`9c5910b` — `test(renderer): cover txt quoting bind zone output`**
  - **Type:** `test` · **Categoria:** Renderer / Contract coverage
  - **Cosa cambia:** estende `tests/test_bind_zone_renderer.py` con un test mirato che verifica esplicitamente il quoting dei payload `TXT` nell'output BIND renderizzato per record testuali rappresentativi del profilo public-safe.
  - **Impatto:** rafforza il contratto del renderer sul trattamento dei record `TXT`, isolando un aspetto semantico importante del formato emesso senza modificare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `47 passed`; `python -m pylint src tests` → `10.00/10`.

- **`afa92bd` — `test(application): cover non string bind zone input failure`**
  - **Type:** `test` · **Categoria:** Application / Failure path coverage
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato su input apex non stringa, verificando nel use case `generate_bind_zone_file` la propagazione di `error_code="non_string_input"` e l'assenza di `zone_file_text`.
  - **Impatto:** amplia ulteriormente la robustezza del boundary `application` coprendo anche il caso di input non conforme al contratto atteso, senza modificare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `46 passed`; `python -m pylint src tests` → `10.00/10`.

- **`7aad215` — `test(application): cover invalid label bind zone input failure`**
  - **Type:** `test` · **Categoria:** Application / Failure path coverage
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato su apex con label non valida, verificando nel use case `generate_bind_zone_file` la propagazione di `error_code="invalid_label"` e l'assenza di `zone_file_text`.
  - **Impatto:** amplia ulteriormente la robustezza del boundary `application` su un failure path sintattico realistico e coerente con la validazione strutturata del layer `domain`, senza modificare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `45 passed`; `python -m pylint src tests` → `10.00/10`.

- **`9b2957d` — `test(application): cover empty label bind zone input failure`**
  - **Type:** `test` · **Categoria:** Application / Failure path coverage
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato su apex con label vuota, verificando nel use case `generate_bind_zone_file` la propagazione di `error_code="empty_label"` e l'assenza di `zone_file_text`.
  - **Impatto:** amplia ulteriormente la robustezza del boundary `application` su un failure path sintattico realistico e coerente con la validazione strutturata del layer `domain`, senza modificare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `44 passed`; `python -m pylint src tests` → `10.00/10`.

- **`ca8e2e0` — `test(application): cover trailing dot bind zone input failure`**
  - **Type:** `test` · **Categoria:** Application / Failure path coverage
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato su apex con dot finale, verificando nel use case `generate_bind_zone_file` la propagazione di `error_code="trailing_dot"` e l'assenza di `zone_file_text`.
  - **Impatto:** amplia ulteriormente la robustezza del boundary `application` su un failure path sintattico realistico e strettamente complementare a `leading_dot`, senza modificare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `43 passed`; `python -m pylint src tests` → `10.00/10`.

- **`ef25219` — `test(application): cover leading dot bind zone input failure`**
  - **Type:** `test` · **Categoria:** Application / Failure path coverage
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato su apex con dot iniziale, verificando nel use case `generate_bind_zone_file` la propagazione di `error_code="leading_dot"` e l'assenza di `zone_file_text`.
  - **Impatto:** amplia ulteriormente la robustezza del boundary `application` su un failure path sintattico realistico e vicino agli errori di input utente, senza modificare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `42 passed`; `python -m pylint src tests` → `10.00/10`.

- **`558c533` — `test(application): cover missing dot bind zone input failure`**
  - **Type:** `test` · **Categoria:** Application / Failure path coverage
  - **Cosa cambia:** estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato su apex privo di dot, verificando nel use case `generate_bind_zone_file` la propagazione di `error_code="missing_dot"` e l'assenza di `zone_file_text`.
  - **Impatto:** amplia ulteriormente la robustezza del boundary `application` su un failure path sintattico realistico e frequente dell'input utente, senza modificare il runtime del package.
  - **Evidenze:** `python -m pytest -q` → `41 passed`; `python -m pylint src tests` → `10.00/10`.

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
