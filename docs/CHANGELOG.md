# CHANGELOG

## Branch: [development]

### [Unreleased]
> Scope corrente: **consolidato sul branch `development` il primo delta `M6` di hardening UI della demo web nel commit `af20290`; con il presente riallineamento truth-first risulta ora chiuso anche il relativo doc gate owner. Il backlog residuo non bloccante (`responsive refinement`, feedback utente ulteriori, `Docker/exportability`) resta classificato, ma non esiste ancora un freeze documentale separato `M6` consolidato a commit**

#### M6.1 — Primo delta di hardening UI della demo web

- **`af20290` — `feat(web): harden demo UI and align bootstrap contract`**
  - **Type:** CHANGED · **Categoria:** Web / Demo UI / Bootstrap contract
  - **Cosa cambia:** aggiorna `src/dns_zone_bootstrapper/interfaces/web/app.py` sostituendo la root HTML browser-default con una superficie web più solida e presentabile tramite CSS inline, layout a card, gerarchia tipografica più forte, hint di input più chiari e feedback errore strutturato; aggiorna inoltre `tests/test_bootstrap.py`, riallineando il contratto testuale della root alla nuova UI senza cambiare route, flusso `GET /generate`, validazione server-side o download diretto del `.txt`.
  - **Impatto:** apre di fatto `M6` sul primo delta UI non invasivo, rende la demo più difendibile per consegna e stakeholder senza introdurre nuove dipendenze, JavaScript, refactor architetturali o modifiche al core, e mantiene verdi i quality gates del repository.

##### Quality gates (snapshot corrente)
- `python -m pytest -q` → `79 passed`
- `python -m pylint src tests` → `10.00/10`
- Stato del blocco: **primo delta tecnico `M6` consolidato nel commit `af20290`; doc gate owner truth-first ora chiuso sul branch `development`; backlog residuo non bloccante classificato, ma nessun freeze documentale `M6` ancora consolidato nella storia Git**

#### M5 — Chiusura documentale essenziale e preparazione audit UI

- **`2642785` — `docs(project): close M5 and prepare UI audit gate`**
  - **Type:** CHANGED · **Categoria:** Owner docs / M5 / Transition gate
  - **Cosa cambia:** riallinea gli owner docs per chiudere formalmente `M5` come blocco documentale essenziale e per promuovere un audit conservativo della demo UI come passo corretto successivo, senza aprire ancora un hardening tecnico largo.
  - **Impatto:** completa la soglia di uscita documentale del blocco `M5`, impedisce derive premature su packaging o refinements non necessari e prepara in modo disciplinato l’ingresso del successivo delta UI minimale.

- **`e1aff03` — `docs(project): sync timeline and changelog after README strengthening`**
  - **Type:** CHANGED · **Categoria:** Owner docs / README / Timeline / Changelog
  - **Cosa cambia:** riallinea `docs/TIMELINE.md` e `docs/CHANGELOG.md` al rafforzamento già consolidato di `README.md`, mantenendo coerente il repository dopo il salto di qualità del documento di ingresso al prodotto.
  - **Impatto:** riduce il rischio di drift tra README e owner docs e rende più leggibile il passaggio dalla fase di freeze post-validazione alla chiusura formale di `M5`.

- **`339e4bb` — `docs(changelog): record post-validation documentation freeze`**
  - **Type:** CHANGED · **Categoria:** Changelog / Post-validation freeze
  - **Cosa cambia:** registra nel changelog la sequenza di freeze documentale successiva alla validazione tecnica del prodotto, mantenendo audit trail esplicito sul passaggio dal core funzionante alla documentazione essenziale.
  - **Impatto:** rende più leggibile la storia evolutiva del repository sul piano documentale e consolida il changelog come documento owner di tracciabilità, non solo come appendice dei commit tecnici.

- **`13092db` — `docs(readme): strengthen product entry document`**
  - **Type:** CHANGED · **Categoria:** README / Product entry documentation
  - **Cosa cambia:** sostituisce il `README.md` precedente con una versione molto più forte come documento di ingresso al prodotto, introducendo sezioni dedicate a cos'è il progetto, perché esiste, stato attuale, workflow end-to-end, lessico minimo DNS/BIND/Cloudflare, perimetro v1, limiti correnti, avvio rapido, uso della demo e distinzione tra baseline public-safe versionata e override locale gitignored.
  - **Impatto:** riduce la dipendenza dalla storia del repository per capire il senso del prodotto, migliora nettamente la leggibilità per lettori terzi e rende più difendibile il blocco `M5`, perché il gap principale residuo viene affrontato nel punto corretto: il documento di ingresso.

- **`0b9d7ca` — `docs(timeline): open post-validation documentation and delivery freeze`**
  - **Type:** CHANGED · **Categoria:** Timeline / Roadmap / Strategic freeze
  - **Cosa cambia:** aggiorna `docs/TIMELINE.md` e `docs/ROADMAP.md` aprendo formalmente il blocco `Post-A2 / Post-C2`, classificando come gap prioritario la comprensibilità del prodotto e non più il core applicativo, attivando `M5` come milestone corrente e congelando la sequenza operativa post-validazione: rafforzamento `README.md`, eventuali chiarimenti mirati in `ARCHITECTURE.md`, eventuale guida utente dedicata, preparazione del report verso l'azienda, quindi solo dopo audit UI minimale e valutazione Docker/exportability.
  - **Impatto:** sposta ufficialmente il progetto dalla sola validazione tecnica alla fase di documentazione essenziale e preparazione consegna, impedisce derive premature su polish UI, Docker o hardening `D*` non prioritari e rende esplicito che la prima comunicazione verso l'azienda deve avvenire dopo la chiusura del blocco documentale essenziale, non dopo miglioramenti estetici o infrastrutturali.

##### Quality gates (snapshot corrente)
- `git status -sb` pulito su `development...origin/development` al consolidamento documentale di `M5`
- `python -m pytest -q` → `78 passed`
- `python -m pylint src tests` → `10.00/10`
- Stato del blocco: **`M5` chiusa e consolidata lato owner docs; il passo successivo corretto viene poi incanalato nell’audit UI minimale e nel primo delta `M6`**
#### Post-A2 / Post-C2 — Riallineamento del bootstrap dichiarato della demo

- **`b6f498e` — `fix(templates): load local override from working tree fallback`**
  - **Type:** FIXED · **Categoria:** Templates / Runtime profile resolution / Delivery bootstrap
  - **Cosa cambia:** aggiorna `src/dns_zone_bootstrapper/templates/profile_resolver.py` mantenendo come primo tentativo l'import standard di `local.dns_zone_profile`, ma introducendo un fallback esplicito al file gitignored `./local/dns_zone_profile.py` rispetto alla working tree corrente quando il top-level package `local` non è risolvibile nel contesto del console entrypoint installato; estende inoltre `tests/test_profile_resolver.py` per congelare sia il fallback public-safe in cwd isolata sia il caricamento dell'override locale direttamente dalla working tree.
  - **Impatto:** chiude il delta tecnico emerso durante l'audit di consegna, in cui il core e la web app avviata con `python -m uvicorn ...` producevano output concreto mentre `dns-zone-cli web` ricadeva ancora sul profilo public-safe placeholderizzato; il bootstrap dichiarato della demo risulta ora riallineato al comportamento atteso con override locale attivo, senza cambiare il contratto utente, il README o l'architettura AS-IS.

##### Quality gates (snapshot corrente)
- `python -m pytest -q tests/test_profile_resolver.py` → `3 passed`
- `python -m pylint src tests` → `10.00/10`
- smoke reale `dns-zone-cli web` + `curl -i "http://127.0.0.1:8000/generate?domain=testdomain.com"` con download `.txt` a valori concreti e non `__FIXED_*__`
- Stato del blocco: **bootstrap dichiarato della demo riallineato al runtime reale con override locale attivo; blocco successivo correttamente spostato sulla documentazione essenziale `M5`**

#### B4 — Runtime fixed profile resolution boundary
> Ordinamento: `git log` (più recente → più vecchio) · principio truth-first: qui è riportato solo ciò che è consolidato a commit sul branch `development`.

- **`98ef332` — `feat(templates): add runtime fixed profile resolver`**
  - **Type:** `feat` · **Categoria:** Templates / Application / Runtime profile resolution
  - **Cosa cambia:** introduce `src/dns_zone_bootstrapper/templates/profile_resolver.py` come boundary dedicato alla risoluzione del profilo fisso attivo; aggiorna `src/dns_zone_bootstrapper/application/bind_zone_generation.py`, che non dipende più direttamente da `PUBLIC_SAFE_FIXED_DNS_PROFILE` ma usa `resolve_active_fixed_dns_profile()`; aggiunge `tests/test_profile_resolver.py` per congelare sia il fallback al profilo public-safe sia l'uso di un eventuale override locale `local.dns_zone_profile.ACTIVE_FIXED_DNS_PROFILE`.
  - **Impatto:** elimina l'hardcode diretto del runtime sul solo profilo versionato public-safe, crea il gancio corretto per usare in locale valori fixed concreti senza versionare dati privati e prepara il passo successivo verso una generazione non placeholderizzata, mantenendo invariata la baseline safe del repository quando nessun override locale è presente.
  - **Evidenze:** `python -m pytest -q` → `78 passed`; `python -m pylint src tests` → `10.00/10`; commit `98ef332` pubblicato su `origin/development`.

#### C2 — Rifinitura demo web e packaging minimo
> Ordinamento: `git log` (più recente → più vecchio) · principio truth-first: qui è riportato solo ciò che è consolidato a commit sul branch `development`.

- **`c432feb` — `feat(cli): add minimal web demo entrypoint`**
  - **Type:** `feat` · **Categoria:** CLI / Minimal web demo packaging
  - **Cosa cambia:** aggiorna `src/dns_zone_bootstrapper/interfaces/cli/app.py` introducendo il subcommand `web`, che avvia la demo FastAPI tramite `uvicorn.run(...)` con entrypoint `dns_zone_bootstrapper.interfaces.web.app:app` e configurazione minima `127.0.0.1:8000`; estende inoltre `tests/test_bootstrap.py` con un test dedicato che congela il nuovo boundary CLI/web.
  - **Impatto:** chiude il gap minimo di packaging emerso in `C2`, perché la superficie installata del progetto non espone più soltanto `doctor` ma anche un entrypoint ergonomico per avviare la demo web locale, senza toccare core, renderer o web adapter.
  - **Evidenze:** `python -m pytest -q tests/test_bootstrap.py` → `10 passed`; `python -m pytest -q` → `76 passed`; `python -m pylint src tests` → `10.00/10`; commit `c432feb` pubblicato su `origin/development`.

- **`cb99280` — `feat(web): refresh demo copy for active generation flow`**
  - **Type:** `feat` · **Categoria:** Web / Demo copy alignment
  - **Cosa cambia:** aggiorna `src/dns_zone_bootstrapper/interfaces/web/app.py` riallineando la copy user-facing della root `/` allo stato reale della demo web, rimuovendo il riferimento ormai superato a `C0/C1` e dichiarando correttamente generazione e download diretto del file `.txt` già attivi. Aggiorna inoltre `tests/test_bootstrap.py`, rinominando il test della root e congelando il nuovo contratto testuale della pagina iniziale.
  - **Impatto:** apre tecnicamente `C2` con un primo delta piccolo, verificabile e non invasivo, migliora la coerenza della demo senza toccare core, route pubbliche o packaging e lascia ancora aperto il successivo lavoro minimo sul packaging.
  - **Evidenze:** `python -m pytest -q` → `75 passed`; `python -m pylint src tests` → `10.00/10`; commit `cb99280` pubblicato su `origin/development`.

#### C1 — Generazione e download del file
> Ordinamento: `git log` (più recente → più vecchio) · principio truth-first: qui è riportato solo ciò che è consolidato a commit sul branch `development`.

- **`7562486` — `feat(web): add C1 generation and download flow`**
  - **Type:** `feat` · **Categoria:** Web / Generation + direct download flow
  - **Cosa cambia:** aggiorna `src/dns_zone_bootstrapper/interfaces/web/app.py` introducendo la route `GET /generate`, collegata al use case `generate_bind_zone_file(...)`; abilita il form della root `/`, aggiunge rendering HTML del failure path con messaggi user-facing derivati dagli `error_code` strutturati e restituisce sul success path il file BIND come `text/plain` con `Content-Disposition` per il download diretto. Estende inoltre `tests/test_bootstrap.py` per coprire entrypoint `C1`, failure path HTML, success path di download e presenza della route `/generate`.
  - **Impatto:** chiude il perimetro minimo di `C1` senza introdurre nuove dipendenze o duplicazione della logica di generazione fuori dal core, rende la v1 realmente usabile end-to-end da pagina web e prepara il terreno al successivo blocco `C2` di rifinitura demo e packaging.
  - **Evidenze:** `python -m pytest -q` → `75 passed`; `python -m pylint src tests` → `10.00/10`; commit `7562486` pubblicato su `origin/development`.

- **`288a0b5` — `docs(project): close C0 and prepare C1`**
  - **Type:** `docs` · **Categoria:** Owner docs / C0 closure + C1 preparation
  - **Cosa cambia:** aggiorna `README.md`, `docs/TIMELINE.md` e `docs/CHANGELOG.md` riallineando lo stato del progetto alla chiusura di `C0` e promuovendo `C1` a prossimo blocco operativo del `Cycle C`.
  - **Impatto:** chiude formalmente il doc gate di `C0`, impedisce che la timeline resti ferma alla sola pagina minimale e prepara correttamente il repository al successivo incremento tecnico sulla generazione e sul download diretto del file.
  - **Evidenze:** commit `288a0b5` pubblicato su `origin/development`; branch allineato; nessuna modifica runtime in quel passaggio.

#### C0 — Pagina web minimale
> Ordinamento: `git log` (più recente → più vecchio) · principio truth-first: qui è riportato solo ciò che è consolidato a commit sul branch `development`.

- **`a702f0b` — `feat(web): add minimal C0 web page`**
  - **Type:** `feat` · **Categoria:** Web / Minimal HTML delivery surface
  - **Cosa cambia:** aggiorna `src/dns_zone_bootstrapper/interfaces/web/app.py` sostituendo la root `/` JSON con una pagina HTML minimale in italiano, contenente titolo, descrizione sintetica, un solo input `Dominio apex` e una CTA disabilitata che esplicita il demandare generazione/download al blocco `C1`; estende inoltre `tests/test_bootstrap.py` con test dedicati sul contratto minimo della superficie web (`root`, `health`, route pubbliche minime).
  - **Impatto:** apre realmente il `Cycle C` sul piano tecnico senza introdurre nuove dipendenze o collegamenti prematuri al generatore, rende la v1 visibile attraverso una pagina web coerente con i vincoli minimi concordati e mantiene separato il successivo lavoro di generazione/download nel blocco `C1`.
  - **Evidenze:** `python -m pytest -q` → `73 passed`; `python -m pylint src tests` → `10.00/10`; commit `a702f0b` pubblicato su `origin/development`.

- **`bb852a8` — `docs(timeline): open C0 minimal web page cycle`**
  - **Type:** `docs` · **Categoria:** Owner docs / Timeline / C0 opening
  - **Cosa cambia:** aggiorna `docs/TIMELINE.md` aprendo formalmente `C0` come primo blocco operativo del `Cycle C`, classificando truth-first che il gap reale residuo non era più nel core ma nella delivery surface web minimale.
  - **Impatto:** sposta formalmente il progetto fuori dalla sola chiusura di `B3` e rende `C0` il contenitore corretto per la prima superficie web della v1, senza aprire nello stesso passaggio `C1`, refactor larghi o hardening.
  - **Evidenze:** commit `bb852a8` pubblicato su `origin/development`; branch allineato; nessuna modifica runtime in quel passaggio.

#### B3 — Test del generatore e preparazione fixture reali
> Ordinamento: `git log` (più recente → più vecchio) · principio truth-first: qui è riportato solo ciò che è consolidato a commit sul branch `development`.

- **`6edb1e2` — `test(bind): freeze shared realistic-backed normalization helper`**
  - **Type:** `test` · **Categoria:** Shared test helpers / Realistic-backed normalization contract freeze
  - **Cosa cambia:** introduce `tests/test_shared_bind_zone_assertions.py` con un test dedicato a `load_normalized_realistic_testdomain_golden(...)`, verificando che il raw realistic-backed contenga i soli frammenti sanitizzati attesi, che tali frammenti scompaiano nel testo normalizzato, che compaiano i corrispondenti placeholder public-safe e che il risultato normalizzato coincida byte-for-byte con `tests/golden/public_safe_candidate.bind.txt`.
  - **Impatto:** rende il perimetro `B3` più difendibile perché il helper condiviso, già riusato da renderer e `application`, non resta più protetto solo indirettamente dai test dei due layer ma viene ora congelato anche come responsabilità autonoma, senza modificare runtime, fixture o confini architetturali.
  - **Evidenze:** `python -m pytest -q tests/test_shared_bind_zone_assertions.py` → `1 passed`; `python -m pytest -q` → `70 passed`; `python -m pylint src tests` → `10.00/10`; commit `6edb1e2` pubblicato su `origin/development`.

- **`c98851b` — `test(bind): share realistic-backed golden normalization helper`**
  - **Type:** `test` · **Categoria:** Renderer / Application / Realistic-backed normalization dedup + renderer freeze
  - **Cosa cambia:** estende `tests/test_bind_zone_renderer.py` con un freeze realistic-backed per `testdomain.com` allineato alla fixture versionata `tests/golden/public_safe_candidate.testdomain-com.bind.txt` e introduce in `tests/shared_bind_zone_assertions.py` la helper `load_normalized_realistic_testdomain_golden(...)`, poi riusata anche da `tests/test_bind_zone_generation_use_case.py` per deduplicare la normalizzazione condivisa verso la baseline runtime public-safe.
  - **Impatto:** completa il secondo ponte tecnico di `B3` lato test senza toccare runtime o fixture, difende la stessa delta policy realistic-backed sia nel renderer puro sia nel boundary `application` e ripristina il quality gate `pylint` eliminando il `duplicate-code` introdotto dal freeze renderer-side iniziale.
  - **Evidenze:** `python -m pytest -q tests/test_bind_zone_generation_use_case.py tests/test_bind_zone_renderer.py` → `35 passed`; `python -m pytest -q` → `69 passed`; `python -m pylint src tests` → `10.00/10`; commit `c98851b` pubblicato su `origin/development`.

- **`d87feff` — `test(application): freeze realistic-backed testdomain golden delta`**
  - **Type:** `test` · **Categoria:** Application / Realistic-backed golden delta freeze
  - **Cosa cambia:** introduce `tests/golden/public_safe_candidate.testdomain-com.bind.txt` come prima fixture versionata, public-safe e realistic-backed derivata dal riferimento reale auditato per `testdomain.com`, ed estende `tests/test_bind_zone_generation_use_case.py` con un test dedicato che congela nel layer `application` il delta ammesso rispetto a tale fixture tramite normalizzazione esplicita dei soli valori sanitizzati/public-safe verso la baseline runtime corrente.
  - **Impatto:** apre realmente `B3` sul piano tecnico senza forzare modifiche premature al runtime, protegge il generatore con un primo ponte snapshot-backed più realistico del golden baseline puro e formalizza che il differenziale atteso rispetto al riferimento realistico resti confinato ai soli valori sanitizzati/public-safe, lasciando invariati struttura, ordine e perimetro v1 del core.
  - **Evidenze:** `python -m pytest -q tests/test_bind_zone_generation_use_case.py -k realistic` → `1 passed, 19 deselected`; `python -m pytest -q` → `68 passed`; `python -m pylint src tests` → `10.00/10`; commit `d87feff` pubblicato su `origin/development`.

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
