# Flovo BPM — Açık Sorular / TODO (önceliklendirilmiş)

> Tüm tasarım dokümanlarındaki **açık kararlar/sorular** burada **tek yerde** ve **önceliklendirilmiş** toplanır.
> **Kural:** Açık sorular **yalnız bu dosyada** tutulur; diğer dokümanların "Açık Kararlar / Sorular" bölümleri **buraya
> işaretçi** verir (tutarsızlığı önlemek için). Her madde kaynağını `(<doküman> §..)` ile belirtir; çözülünce `[x]`.
>
> **Öncelik mantığı:** Tier 0 = bir kararla **birçok dokümanı** kapatan çapraz-kesen konular · Tier 1 = motor
> çekirdeği (mimari) · Tier 2 = özellik netleştirmeleri · Tier 3 = detay/sonraya · ⏭️ **Faz 2 = MVP-sonrası** — ayrı dosya
> [`todo-phase2.md`](./todo-phase2.md) (bu dosya yalnız **MVP** kapsamını tutar).

---

## ⏭️ Faz 2'ye (MVP-sonrası) taşınanlar → [`todo-phase2.md`](./todo-phase2.md)
> **v0.47 kararı:** aşağıdaki konular MVP geliştirmesinden **sonra** detaylandırılıp eklenecek; ayrıntı/alt sorular ayrı dosyada.
> Tasarım dokümanlarındaki eski `todo.md` işaretçileri bu satır üzerinden çözülür; bir konu MVP'ye geri çekilirse maddesi buraya taşınır.
- ⏭️ **Yetkilendirme kapsamının detaylandırılması** (§1) · **Vekalet sistemi `UserDelegate`** (§2) · **Loglama** — denetim izi / ayar-değişiklik / sistem
  logları (§3) · **Toplu senkron ucu** (§4) · **`SchedulerJob`** (§5) · **Form List red-akışı bayrakları** (§6) · **Flovo AI adım ayarları** (§7) ·
  **`triggerProcessStep` / `formRedirect` adımları** (§8) · **Timer üçlüsü** (§9) · **ServiceTrigger kenar durumları** (§10) · **View profile / Form List
  tik değişim olayları** (§11 — ServiceTrigger ile birlikte) · **Servis template & JSON** (§12) · **Customer API** (§13 — O6 dış referans anahtarı · `apiKeyId` dahil).

---

## ⭐ Tier 0 — Çapraz-kesen kararlar (önce bunlar; bir karar → çok doküman)

_(açık madde yok — kapananlar alt bölümde: ✅ → 📦 konsolide edilen çözülmüş maddeler)_

---

## 🏗️ Tier 1 — Motor çekirdeği (mimari)

- [ ] **Çalışma-zamanı mimarisi** — tek-süreç mi, kuyruk-tabanlı dağıtık worker mı? Orkestrasyon ↔ yürütme ayrımı;
  durum DB'de, kuyruk yalnız iş ID'leri, worker'lar durumsuz. _(flovo-bpm-engine §2.2 / §12)_
  - 🧱 **Tech-stack:** MVP **Core BPM monolith** → Hexagonal + **NATS kuyruk** + **durumsuz worker** + durum **Postgres/NATS**'ta
    (SOA-ready). → [`tech-stack/`](./tech-stack/index.md) · [`./research/tech-stack/tech_rating.md`](./research/tech-stack/tech_rating.md)
  - **Motor-içi orkestrasyon↔yürütme — ÇÖZÜLDÜ (v0.40):** senkron §4.4 döngüsü → **event-driven state machine**
    (worker/orkestratör/scheduler · `workflow_events` Partial Event Sourcing · suspend/resume · `executionState`) →
    [`engine-runtime.md`](./engine-runtime.md). **Kalan:** `workflow_events`/`workflow_projection` **model dosyaları** · scheduler
    **lider-seçim** mekanizması (NATS KV ↔ Postgres advisory lock) · retry politika değerleri + **global hata yakalayıcı** +
    compensation · **fork/join** (ertelendi) · `workflow_events` **pruning/KVKK** · optimistic-concurrency çakışma UX'i. _(engine-runtime §11)_
- [ ] **Veri modeli** — **temsil/akış ÇÖZÜLDÜ (v0.30): koleksiyon-tabanlı.** Adımlar arası veri, `InstanceValue` ile **ortak
  değer-modeli** (`propertyValuesTemplates` + `LabeledValue`) taşıyan bir **değer koleksiyonu** olarak aksiyonla **açıkça** akar:
  `changeList` = obje-map `{ Property.code: value }` → forma **doğrudan JSONB merge**; `parameters` = aynı değer şekli + **serbest
  anahtar** (forma yazılmaz). Alan değeri model/dizi ise **tüm değer komple** taşınır (kısmi patch yok). _(→ flovo-bpm-engine §3 ·
  process-step-action §2.2)_
  - **Açık kalan:** **soy ağacı (lineage)** ayrıntısı (n8n `pairedItem` muadili) + **çok-kayıt iterasyonu / loop / join**
    (item-dizisi otomatik fan-out) — bu karar **temsili** çözer, **iterasyon semantiğini değil** → "Paralel dallanma" maddesi. _(flovo-bpm-engine §3 / §4.5 / §12)_
- [ ] **Kalıcılık & durum** — ne saklanır (süreç tanımı · instance/state · veri · dosya/binary); durum yaşam döngüsü
  (new/running/waiting/done); saklama/pruning. _(flovo-bpm-engine §8)_
  - 🧱 **Tech-stack:** kalıcılık **substratı** = PostgreSQL + **Partial Event Sourcing** (`workflow_events` append-only); *ne
    saklanır / yaşam döngüsü / pruning* tasarımı açık. → [`./tech-stack/postgresql.md`](./tech-stack/postgresql.md)
- [ ] **Ortam (environment) modeli** — **parent-child env** yapısı kurulacak mı? Her ortamın **formları ayrı mı**? Geliştirmeyi
  bir ortamda yapıp **canlı ortamda oluşturulmuş formları görüntüleme** senaryosu nasıl çözülecek? _(environmentRestriction
  alanları: process-step §2 / action · flovo-bpm-engine §8)_
  - **`environmentRestriction` alan formatı** (enum mu, string mi, kapsam) bu modelle birlikte netleşecek — şimdilik **ertelendi**.
    _([`./research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](./research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §8)_
  - **Not (v0.41-1):** servis **versiyonlama/draft-publish + arşivleme** pilotta **ortam modelinden bağımsız** inşa edildi;
    env katmanı geldiğinde ortamlar-arası **kopya/promote** bunun üstüne oturur (versiyonlamayı env'e bağlama varsayımı gevşedi).
    → [`implementation-status.md`](./implementation-status.md).
- [ ] **Güvenlik** — expression/kod değerlendirme **sandbox**'ı (sert sınır), credential şifreleme/paylaşım,
  riskli adımlar. _(flovo-bpm-engine §10 · process-step-action §5)_
- [ ] **Paralel dallanma / eşzamanlı kollar & join** var mı? Bir adım aynı anda birden çok sonraki adımı tetikler mi?
  Alt servisler (Form List) ana süreçle eşzamanlı mı yürür? _(flovo-bpm-engine §4.5)_
- [ ] **Olay/mesaj-tabanlı tetikleme** ve uyuyan sürecin uyandırılması; çok-örneklilikte "en-fazla-bir-kez"/lider
  seçimi. _(flovo-bpm-engine §5 / §6 / §12)_
  - 🧱 **Tech-stack:** mesaj/olay **omurgası** = **NATS JetStream** (durable consumer + `Nats-Msg-Id` idempotency → "en-fazla-bir-kez");
    BPM-düzeyi *uyandırma / lider-seçimi* tasarımı açık. → [`./tech-stack/nats-jetstream.md`](./tech-stack/nats-jetstream.md)

---

## 🔧 Tier 2 — Özellik netleştirmeleri

- [ ] **AI entegrasyon modeli** — deterministik "AI adımı" vs otonom "ajan"; takılabilir strateji (model/memory/araç);
  "herhangi bir adım = araç" + MCP? _(flovo-bpm-engine §11)_
  - 🧱 **Tech-stack:** AI **substratı** = **Python AI Service** (🟡 post-MVP) + **pgvector**; entegrasyon **MODELİ** açık. → [`./tech-stack/python-ai-service.md`](./tech-stack/python-ai-service.md)
- [ ] **Settings API (tasarım-zamanı ayar CRUD) — açık noktalar** — yüzey tasarlandı ([`settings-api.md`](./settings-api.md)); kalan:
  **ortak hata sözleşmesi** · **ortamlar-arası (env) kopya/promote** · `settings`/`configuration` **referans bütünlüğü +
  silme koruması** kesin kuralları · **yetki granülaritesi** (hangi rol hangi kaynağı yazar). _(settings-api §5–§9)_ ⏭️ Toplu senkron ucu + ayar-değişiklik loglama → **Faz 2** ([`todo-phase2.md`](./todo-phase2.md) §3–§4).
  - **Pilotta inşa edildi (v0.41-1):** **draft/publish + servis versiyonlama** (`ServiceVersion` · `currentVersion` ·
    `hasUnpublishedChanges` · `lastPublishedAt` + code-lock) ve **süreç arşivleme** (`archivedAt`/`archivedBy` + `ArchivedChecker`
    cross-domain guard + `archiveFilter`) — **ortam modelinden bağımsız**. → [`implementation-status.md`](./implementation-status.md) ·
    `models/service-settings/service.md`. **Kalan:** `ServiceVersion` **snapshot içeriği** + ortamlar-arası kopya.
- [ ] **Hata yönetimi** — her adımda `onFail` var mı/zorunlu mu; **retry** (deneme + bekleme); süreç-seviye global
  hata yakalayıcı; telafi/compensation; `action` zinciri **sonsuz döngü** koruması. _(flovo-bpm-engine §7 · process-step-action §7)_
- [ ] **Form yaşam döngüsü** — Instance Creator / Instance Deleter; Parent Property ile birlikte. _(process-step §4)_
  - **Netleşen (v0.12):** **Instance Deleter** `deleteMode` (`InstanceDeleteMode`: `withRelated`/`unlinkRelated`) + **Instance Creator**
    temel ayar modeli tanımlandı. **Form Yönlendirme / Süreç Adımı Tetikleme** ⏭️ **Faz 2** ([`todo-phase2.md`](./todo-phase2.md) §8). _(process-step §3.9)_
- [ ] **Raporlama** ayrı özellik olarak nasıl modellenecek? _(view-profile §3 / §5)_
- [ ] **Aksiyon parametrelerinde ifade/kod desteği** — parametreler ne kadar "ifade" (expression/kod) destekleyecek
  (no-code ↔ pro-code dengesi); ifade motoru + veri eşleme (sürükle-bırak) + koşullu çalışma kapsamı. _(process-step-action §5 / §7)_
- [ ] **Kapsam-dışı varlıklar + Org ↔ BPM entegrasyonu** — ExpenseType modellensin mi; organizasyon ayarlarının BPM ile entegrasyon derinliği.
  ⏸️ **Currency / Tax → askıya alındı (KARAR v0.47): yeni projede kullanılmayacak, modellenmez.** _(Position/Staff modellendi → `position.md`.)_ _(index.md §4 · new-vs-current §14)_
  - **Bağımlı kararlar (v0.47, Tax/Currency askıya alınınca):** **`groupByTaxReceipt`** alan tipi vergi-oranı listesini org Tax ayarından alıyordu → alan tipi de
    **askıya mı alınır** (`PropertyType` enum'undan düşer, settings/değer şablonu dosyaları arşivlenir) yoksa `taxRate` **serbest sayı** olarak kalıp alan tipi korunur mu? ·
    ifade kataloğundaki **`getExchange`** (döviz kuru, async) **katalog-dışı adayı**. _(property-settings/group-by-tax-receipt.md · enums/property-type.md · business-rule-engine §9 katalog)_
- [ ] **ActionTransfer'e `user` alanı** — `ActionTransfer` (DTO → `models/service-settings/jsonTemplateModels/action-transfer.md`;
  parameters/changeList/action → process-step-action §2) modeline bir **user** property'si eklenmeli mi (aksiyon/parametre
  verisinden `Instance.creatorUserId`'yi **isteğe bağlı** set etmek için)?
  _(process-step-action §2 · process-step §3.12 · `apiKeyId` açık sorusuyla bağlantılı → ⏭️ [`todo-phase2.md`](./todo-phase2.md) §13)_
  - **Netleşen (v0.17):** "`form` tipinde `creatorUserId` **zorunlu dolu**" kuralı **kaldırıldı** — süreç **API/webhook ile**
    (tek oluşturan kullanıcı olmadan, ör. gruba yönlendirilerek → `sampleProcess/referred`) başlatılabildiğinden
    `creatorUserId` **null olabilir**; başlatan **`ProcessInstance.createdByApiKeyId`** ile izlenir. Açık kalan: yalnız
    ActionTransfer.user ile creatorUserId'nin **opsiyonel atanması**.
- [ ] **"Var olanlardan ekleme" filtreleri** — bugün yalnız **durum** (`addFromExistingStatusIds`) ile filtre var; ek olarak
  "yalnız **related-form** olanlar listelensin", "hangi **property** ile related olanlar listelensin" gibi seçenekler nasıl
  yönetilecek? _(view-profile §5 · properties §3.13 Form List · AssociatedInstance)_
- [ ] **Ortamlar arası değişiklik aktarımı (promote/rollback)** — bir ortamda yapılan değişiklikleri **canlıya aktarma** ve
  **geri alma** yöntemi; ortamlar arası **pull-request** benzeri bir yapı nasıl kurulabilir? _(→ Tier 1 "Ortam (environment) modeli")_
- [ ] **İş kuralı — açık detaylar** (v0.34'te model iskeleti kuruldu: `BusinessRule.configuration` JSONB + `jsonTemplateModels/business-rule/`
  aksiyon konfig ailesi). Kalan açık noktalar:
  - **İfade dilinin somut seçimi** — sandbox'lı standart dil (**JSONLogic ↔ CEL**) + fonksiyon **katalog kapsamı**; **tam-frontend**
    kararı gereği dil **çok-client portlanabilir** olmalı (Dart+JS portu). _(business-rule §5 · Tier 0 Güvenlik sandbox)_
    - **Çok-dilli ifade — ÇÖZÜLDÜ (v0.34):** `fromCalculation` = `expression` (default) + `localizedExpressions [{languageCode, expression}]`;
      eksik dilde default. Sabit TR/EN kısıtı kalktı (→ `jsonTemplateModels/business-rule/shared/assign-value.md`). İfade dilinin **kendi** seçimi (JSONLogic/CEL) açık kalır.
  - **`fillDataSource` `organizationData` MODELLENDİ (v0.34, gerçek koddan):** `OrganizationDataSourceType` (10) + `OrganizationParameter` +
    `SubTextType` + `FillDataSourceOrganization`/`FillDataSourceParameter` oluşturuldu. **Açık:** masraf varlıkları (ExpenseType/ExpenseCategory)
    + `ValueTypeOfList` masraf değerleri (expenseType*/categoryCode) **kapsam-dışı** (masraf çekirdek modeli yok) → "Kapsam-dışı varlıklar".
  - **Lazy dataset runtime API sözleşmesi** — `serviceInstances` çalışma-anı fetch request/response (eski `GetWorkRuleDataSet*`/`DataSetDto`)
    = runtime API tasarımı (Customer API ⏭️ Faz 2; iş kuralının instance-fetch ucu MVP'de **motor/frontend API'sinde** kalır); iş-kuralı-tanımı değil, ayrı ele alınacak. _(jsonTemplateModels/business-rule/assign-value-from-dataset.md)_
  - **`search` değer kaynağı** davranışı (arama bağlamı). _(jsonTemplateModels/business-rule/assign-value.md)_
  - **`setStyle` `style` objesi** şeması (tekil görünüm nitelikleri: fontSize/titleColor…). _(jsonTemplateModels/business-rule/set-style.md)_
  - **`showMessage` "bir kez göster"** mekanizması. _(jsonTemplateModels/business-rule/show-message.md)_
  - **Döngü/derinlik limiti + hata görünürlüğü** — v0.34 düzeltme kapsamına **alınmadı** (eski dolaylı-durma + sessiz-yut korunur);
    sonra değerlendirilecek. _(business-rule §5 · Tier 2 "Hata yönetimi")_
  - **`ValueTypeOfList` / `IsActiveKkegAttachment`** (masraf/KKEG-niş) — şimdilik **dışta**; ihtiyaç doğarsa değerlendirilir.
  - **[eski-kod doğrulama, v0.34 — kritik değil, sonra bakılacak]** eski `WorkRule` model+motor taramasından (`Pratico.Apps`) çıkan açık noktalar:
    - **`any`/`every` karşılaştırma EKSİK** — eski `CriteritionType` idx 12-13 (çoklu-değer: virgüllü parçalardan **herhangi biri**/**hepsi** sol değerde geçiyorsa). `criterion-type.md`'ye `containsAny`/`containsAll` eklenebilir. _(criterion-type.md)_
    - **`httpRequest` iş-kuralı şeması** — eski `AssignValueFromFunctionDto` (`metod`/`url`/`responseParameter` + query/header/body/template grupları) → yeni'de process-step'e delege; grup ayrımı `DynamicParameter`'da netleşmeli (`DynamicParameter.value` maddesiyle bağlı). _(shared/assign-value.md)_
    - **`shouldNotWorkInReadonlyMode`** — eski motorda **ölü alan** (hiç okunmuyor); yeni motorda anlamlı kılınmalı mı yoksa çıkarılmalı mı? _(business-rule.md)_
    - **compare-value `fromCalculation` tutarlılık** — koşul tarafı sade `{expression}`; `AssignValue` ile tutarlı `localizedExpressions` eklensin mi? _(shared/business-rule-condition-compare-value.md)_
    - **İş kuralı davranış spesifikasyonu (motor)** — koşul tip-semantiği (string/num/date **sol-operanddan** · boş-tarih=`year==1` · TR-sayı formatı · ModalList/RadioButton/FileControl/DataGrid özel); `formListRowCondition` hep **OR**; **global kill-switch** (org/network hatası tüm kuralları durdurur) + cascade **döngü/derinlik limiti** → Tier 2 "Hata yönetimi". _(business-rule.md davranış)_
  - **[kodlanabilirlik gap → KARARLAR v0.35]** **ÇÖZÜLDÜ:** **ifade dili = JSONLogic** (+ custom operator katalog · veri-only sandbox ·
    async sarmalayıcı) · **`compareValues`** = **`propertyType`-güdümlü** + `containsAny`/`containsAll` (çoklu-değer) · **koşul depolama =
    gömülü JSONB** (ayrı tablo değil) · **`httpRequest` çıkarım** = **nokta-yolu** (`data.items.0.code`) · **`prepareEngine` = hibrit**
    ön-yükleme (cache-sync + lazy) · **`shouldNotWorkInReadonlyMode`** = motor uygular. _(business-rule-engine §3/§6/§7/§9 · business-rule-condition.md)_
    - **Kalan açık:** ifade **katalog kesin kapsamı + operatör imzaları** · **`environmentRestriction`** (geçerli değerler → ortam modeli) ·
      hata görünürlüğü + veri-hatası davranışı · cascade **döngü/derinlik limiti** · `search` değer kaynağı · `setStyle` `style` şeması ·
      `httpRequest` alan-yolu **JSONPath'e genişletme**. _(business-rule-engine §11)_
    - **Not (v0.43, S4 paritesi):** ifade dili + operatör kataloğu **çapraz-katman ORTAK** olmalı — aynı fonksiyon/operatör motor (Go) ve
      frontend (JS+Dart) için **aynı çıktıyı** üretir; katalog kesin kapsamı bu parite gereğiyle tanımlanacak (yalnız iş kuralı değil,
      **Değer Atama `fromCalculation` + Karşılaştırma** adımlarını da kapsar).

---

## 🧩 Tier 3 — Detay / sonraya

- [ ] **`actionDisplayType`** gözden geçir (`invisible`/`everywhere`/`onlyFormDetail`/`onlyFastApprove`). _(action §3)_
- [ ] **İş kuralı performansı** — `always` kuralları yalnız ilgili property değişince (alan-bağımlı) tetiklensin mi?
  _(business-rule §6)_
- [ ] **Property `settings` şeması — tip-başına şemalardan açık alan kararları (v0.37):**
  - `flowInfoValue` / `userInfoValue` **değer kataloğu enum'a çekilsin mi** — şu an `settings`'te `string` seçici. **Karar: evet** —
    `flow-info-value.md` / `user-info-value.md` enum dosyaları + koşullu `settings` alanları **harici analiz PR'ı** ile geliyor (review bekliyor).
    ✅ v0.46: `mainAccount` ve `lastActionReason` **katalog-dışı** (gerekçe = eventForm parametresi → Değer Atama → form alanı; flowInfo değil). **Kalan:** enum dosyalarının repoya girmesi + §5 şemalarının `string` → `enum`'a daraltılması.
    _(jsonTemplateModels/property-settings/flow-info.md §7 · user-info.md)_
  - **Form List red-akışı bayrakları** ⏭️ **Faz 2** → [`todo-phase2.md`](./todo-phase2.md) §6.
  - **`groupByTaxReceipt` eski-kod ayar adayları** — `isLineAddActive`/`isLineReduceActive`/`isTaxEditable`/`isManuelTax`/
    `kkegExpenseTypeId`/`multiKkegActive` kapsam-dışı bırakıldı; `settings` adayı mı? ⏸️ **Tax askıya alındı (v0.47)** → alan tipinin kaderiyle birlikte
    karar (Tier 2 "Kapsam-dışı varlıklar" bağımlı kararlar). _(jsonTemplateModels/property-settings/group-by-tax-receipt.md)_
- [ ] **Process step `settings` şeması — tip-başına şemalardan açık alan kararları (v0.38):**
  - **`comparison` değer-kaynağı** — `referenceValue`/`valueToCompare` **ValueAssignType** (fixed/property/calc) mı yoksa iş kuralıyla
    ortak **`BusinessRuleConditionCompareValue`** (`viewProfile` kaynağı dahil) mı olacak? Karşılaştırma adımı viewProfile'ı destekleyecekse
    ikincisine geçmeli. _(jsonTemplateModels/process-step-settings/comparison.md)_
    - **→ Yön ÇÖZÜLDÜ (v0.43, S4 paritesi):** ortak **`BusinessRuleConditionCompareValue`** (`viewProfile` dâhil) — compareType iş
      kuralıyla **birebir aynı** çalışacağından. **Kalan:** şema hizalama detayı (comparison.md güncellemesi).
  - **`comparison` nested grup birleştiricisi** — `ComparisonCondition.children` alt-gruplarının kendi `and`/`or` birleştiricisi yok
    (yalnız kök `conditionType`); iş kuralı koşul ağacıyla hizalanmalı mı? _(process-step-settings/comparison.md)_
  - **`instanceCreator`** init-değer eşleme detayı (§3.9 "sonra genişletilecek"). _(process-step-settings/instance-creator.md)_
  - `triggerProcessStep` / `formRedirect` `settings` şeması · `flovoAi` ayarları ⏭️ **Faz 2** → [`todo-phase2.md`](./todo-phase2.md) §7–§8.

---

## 🆕 Bu oturumda eklenen açık sorular


### 🔎 Tutarlılık denetiminden (2026-07-02)
- [ ] **`ProcessStep`/`BusinessRule` denormalize `organizationId`** — asıl kapsayıcı `serviceId`; kiracı için ayrıca
  `organizationId` tutulsun mu, yoksa `service → solution → org` üzerinden mi? _(models)_

### 🔧 v0.12 — Adım tipe-özel ayar modellemesinden (2026-07-16)
- [ ] **Adım `settings` JSONB doğrulama & referans bütünlüğü** — tip-başına **JSON Schema**; `settings` içindeki referans id'lerin
  (`propertyId`/`userGroupId`/`selectedTimerProcessStepId`…) **uygulama-katmanı** doğrulaması + **silme koruması**. _(process-step §2)_
- [ ] **`DynamicParameter.value` şekli** — değer-kaynağı (**ValueAssignType**: sabit/hesaplama/form property) + değerin JSONB
  temsili (iş-kuralı `AssignValueToFieldDto` muadili). _(process-step §3.1/§3.6)_

---
- [ ] **Değer Atama — gelen `parameters`'tan değer atama kaynağı (v0.46)** — eventForm pop-up parametresini form alanına yazma deseni
  (`referred`: `transferUser` → "Yönlendirilen Kullanıcı"; red gerekçesi için aynı desen — flowInfo `lastActionReason` bu yüzden yok) kullanılıyor,
  fakat `ValueAssignType`'ın Değer Atama alt-kümesi (`fixedValue`/`propertyValue`/`fromCalculation`) **parametre kaynağı** içermiyor ve ifade
  kataloğunda `parameters` erişimi tanımlı değil. Seçenek: **(a)** enum'a `parameterValue` + `parameterKey` ayarı (yalnız Değer Atama'da geçerli) ·
  **(b)** `fromCalculation` ifadesine `parameters` bağlamı. Ayrıca "forma yazılınca parametre ileri taşınmaz (tüketilir)" kuralı (`referred.md` §4)
  `mergeParameter`/§2 ile netleştirilmeli. _(process-step.md §3.4 · process-step-settings/value-assignment.md · enums/value-assign-type.md · process-step-action.md §2)_

## ✅ Bu oturumda çözülen tutarsızlıklar (log)

> **Not (v0.22):** **Commit-bazında (v0.18+) çözülen soruların DETAYI** (cevap + geliştirme + dosya listesi) artık todo'da
> **tutulmaz**; ilgili **`commitNotes/v0-X.md`** dosyasının "✅ Çözülen açık sorular" bölümündedir (todo'yu sadeleştirmek için):
> v0.18 → [`../commitNotes/v0-18.md`](../commitNotes/v0-18.md) · v0.20 → [`../commitNotes/v0-20.md`](../commitNotes/v0-20.md) ·
> v0.21 → [`../commitNotes/v0-21.md`](../commitNotes/v0-21.md). Aşağıdaki **genel log** + **📦 konsolide liste** (sürüm-öncesi /
> çapraz kararların özeti) todo'da kalır; **bundan sonraki** çözülenler yalnız ilgili commit-notunda toplanır.

- **Kimlik tipi:** `organizationId` her yerde **int** (eski app'teki `accountId` = yeni `organizationCode`'a denk).
  `string` tipler int'e çevrildi.
- **Style ↔ alan:** Form alanları `style.md` Style varlığını **kullanmaz**; iş kuralı `setStyle` yalnız tekil görünüm
  niteliğini (fontSize/titleColor) değiştirir. Style tüketicileri = aksiyon + durum.
- **Değer Atama:** `valueAssignType`'a `fromCalculation` (+ `expression`) eklendi (özetteki "hesaplayarak" ile hizalandı). _(alan v0.18'de `valueType`→`valueAssignType` olarak ayrıştırıldı)_
- **Processing:** frontende form/response döner; **`default` kodlu `autoAction` varsa** otomatik ilerler, **yoksa bekler** (opsiyonel otomatik ilerleme; yeniden sınıflandırıldı).
- **View-profile + diğer modeller:** eksik primary/secondary key'ler eklendi (`id`, `serviceId`, `processStepId`);
  alan-referansları `...Id` (FK) yapıldı (`processViewProfileId`, `userGroupIds`, `styleId`).
- **PK adı:** modelin birincil anahtarı `id` (property'de `propertyId`→`id`).
- **İnsan-tetikli aksiyonlar:** `manual`/`eventForm`'a ek `takePhoto`/`selectFile`/`scanBarcode` da eklendi.
- **Yazım/casing:** `trealingView`→`trailingView`, `criteritionType`→`criterionType`, `solutionid`/`ServiceId`→`solutionId`/`serviceId`.
- **Hiyerarşi tanımlandı:** `Organization → Solution → Service → {Property · ProcessViewProfile · ProcessStep · BusinessRule}`;
  `ProcessStepAction → ProcessStep`; **Action/Status/Style/Translation → Organization** (havuz). `models/` klasörü ve
  `organization-settings/action.md`·`status.md` buna göre revize edildi (Action/Status `serviceId`→`organizationId`).
- **Translation kayıt-başına-dil:** `tr`/`en`/`de` kolonları kaldırıldı → **`languageCode` + `definition`** eklendi;
  benzersizlik `(organizationId, code, languageCode)`; çözümleme `code` + `languageCode` + `organizationId` ile.
- **Action → ProcessStepAction bağımsız kopya:** `actionId` FK **kaldırıldı**; alanlar oluşturmada **bir kez** kopyalanır,
  iki taraf birbirini etkilemez (Action değişince mevcut binding'ler güncellenmez).
- **Profil-bazlı alan override'ı (B2):** `ProcessViewProfilePropertySetting {viewProfilePropertyId, key, value}` eklendi
  (propertyType'a göre dictionary; katalog → `models/service-settings/view-profile-property.md`). Form List ayarları Property'den
  profile taşındı: `addNewEnabled`→`activeStartActions` (ProcessStepAction id listesi), `addFromExistingRecordsIsActive`→
  `addFromExistingStatusIds` (Status id listesi). Ayrıca `selectedEnable`→`selectableVisible` olarak **profil-bazına** (Form List,
  `ProcessViewProfilePropertySetting`) taşındı; eski alan-düzeyi `selectableModeActive` **kaldırıldı**, öneri `selectedEditable`
  (profil). _(`reOrder` + mapViewer `editOnlyOwnPosition` profil-bazlılığı **ÇÖZÜLDÜ v0.33**; `parameterTransfer`/`propertyTransferParameters` **kaldırıldı** → `parentProperty`.)_
- **Dokümanlar senkronlandı + tutarlılık denetimi:** `research/compare/new-vs-current.md` bu oturumun tüm kararlarıyla
  güncellendi; `CLAUDE.md`/`index.md` indekslerine `models/` + `todo.md` eklendi. Bağımsız denetim düzeltmeleri:
  README (style alanları), Processing taksonomisi (otomatik), `process-step-action`/`flovo-bpm-engine` `style`→`styleId`,
  `skipWithThisActionId` "FK → Action" kaldırıldı (belirsiz olarak işaretlendi), Customer API başlığı "geçici" notu.
- **Açık soru merkezileştirme (2026-07-07):** Tüm dokümanlar denetlendi; dağınık açık sorular burada toplandı. **Eklenen**
  (todo'da yoktu): yetkilendirme 4-madde (authorizationLevel uyumu · impersonation kapsamı · yetki genişletilebilirliği ·
  admin-only ↔ OrganizationSettings sınırı), aksiyon parametre ifade/kod desteği, çekirdek↔tipe-özel ayrım, Processing durum
  değişimi, kapsam-dışı varlıklar (ExpenseType/Currency/Position/Tax), `actionType` isim çakışması, çeviri `definition`↔`defaultLang`,
  aksiyon kodu adlandırma tutarlılığı; property-value 7 alt-sorusu (form-value-scenarios §12) umbrella altında sayıldı. Diğer
  dokümanların "Açık Kararlar / Sorular" bölümleri **todo.md işaretçisine** çevrildi. `style.md` "Style tüketicisi: adım?" **çözüldü**
  (tüketici = Action + Status; alanlar Style kullanmaz).
- **Adım tipe-özel ayarlar → JSONB `settings` (KARAR, v0.12):** `ProcessStep.settings` JSONB kolonunda **gömülü** (ayrı alt-tablo
  yok); ayrımlayıcı `stepType` (ProcessStepType); tip-tip ayar modelleri process-step §3. Model §2'deki "ayrı alt-model mi gömülü mü"
  açık notu **kapandı**; referans bütünlüğü uygulama-katmanında (tip-başına JSON Schema).
- **Adım-tipi enum ailesi + alan rename'leri (v0.12):** 11 yeni enum (ProcessStepType · HttpMethod · ProcessStepUserType ·
  ProcessStepUserGroupType · NotificationChannel · NotificationRecipientType · NotificationUserType · TimerCalculationType ·
  WorkTimeSelection · TimeAdjustmentOption · InstanceDeleteMode) + KeyboardType/BarcodeFormat dolduruldu; NotificationUserGroupType
  **foldlandı**. Rename: `stableUserId→fixedUserId` · `resource→endpoint` · `method→HttpMethod` · `WorkStyle→TimerCalculationType` ·
  `HttpRequestParameter→DynamicParameter` · `dynamicUserListFieldId→dynamicUserListPropertyId`; kaldırıldı: `returns`, Switch `cases`,
  userType `managerChain`/`managerByTitle`. Davranış dokümanı senkronlandı; `research/compare/*` güncellendi.
- **Çeviri anahtarı ayrıldı → `translationCode` (KARAR, v0.13):** Çeviri eşleşmesi modellerin **iş kodu (`code`)** üzerinden
  yapılıyordu; `code` **model-içi**, çeviri ad-uzayı **organizasyon geneli** ve varlık-ayrımsız olduğundan Departman `"01"` ↔
  Şirket `"01"` **aynı çeviri satırına çakışıyordu**. **23 model/alt-modele** ayrı **nullable `translationCode`** eklendi
  (`Model.translationCode → Translation.code`); **`null` = çeviri es geçilir → `definition`** (opt-in). Emsal: `PropertyItem`
  (`code ≠ value`) — standart tüm modellere yayıldı. Rename: `PropertyItem.code`/`QualificationItem.code` → `translationCode`;
  `comboboxCode` → `comboboxTranslationCode`. **VacationDay** anahtarsızdı (hiç çevrilemiyordu) — boşluk kapandı.
  Motor `translation.md §3/§3.1`'e işlendi; ad-uzayı kuralı **açık** kaldı.

### 📦 Tier listelerinden konsolide edilen çözülmüş maddeler
> `[x]` işaretli çözülmüş maddeler Tier 0–3 / "eklenen açık sorular" listelerinden buraya taşındı (açık listelerde artık yalnız
> `[ ]` kalır). _(Zaten yukarıdaki log'da özeti bulunanlar tekrar edilmedi: **Profil-bazlı alan override'ı (B2)** ·
> **Action→ProcessStepAction bağımsız kopya** · **Çeviri anahtarı `translationCode` (v0.13)**.)_
- **Genişletilebilirlik — sabit set mi, plugin/SDK mı? (ÇÖZÜLDÜ — v0.30):** Adım / aksiyon / alan tipleri **sabit, kapalı
  bir settir**; plugin/SDK ile üçüncü-taraf yeni tip **eklenemez**. Tüm tipler ve bunların motordaki yürütme davranışı **Flovo
  tarafından** geliştirilir/bakılır; yeni ihtiyaç = **çekirdek motor geliştirmesi** (harici genişletme noktası yok).
  _(process-step §1/§4 · process-step-action §3/§7 · properties §3/§4)_
- **Kapsam kararı — servis-bazlı mı, paylaşımlı mı? (ÇÖZÜLDÜ):** hiyerarşi ile — **organizasyon havuzu** = Translation / Style /
  Status / Action (organizasyona bağlı, tüm servislerde); **servis-bazlı** = Property / ProcessViewProfile / ProcessStep /
  BusinessRule. _(action §3 · status §4 · business-rule §6 · view-profile §5)_
- **Bulut + on-prem hibrit dağıtım (ÇÖZÜLDÜ — tech-stack):** **on-prem + Private Cloud ready** (K8s OpenShift + BYO + tek Helm
  umbrella); merkezi-kimlik çelişkisi **Keycloak AD/LDAP federasyonu** ile giderildi. Kalan minör: saf-on-prem'de sosyal-login
  kapsamı. → [`./tech-stack/kubernetes-helm.md`](./tech-stack/kubernetes-helm.md) · [`./tech-stack/keycloak.md`](./tech-stack/keycloak.md)
- **`eventForm` formu (ÇÖZÜLDÜ):** `formType = eventForm` servisinin **görüntüleme profilidir**; aksiyon alınırken seçili
  profildeki alanlar **pop-up** olur, sonuç **`parameters`** ile taşınır (`Instance`/akış yok). _(process-step-action §3.2 ·
  models/service-settings/service.md)_
- **`actionType` isim çakışması (ÇÖZÜLDÜ — v0.7):** BusinessRule alanı `actionType` → **`businessRuleActionType`**;
  **`Action.actionType`** aynen kaldı. _(business-rule.md · index.md Notlar · business-rule-action-type.md)_
- **Alt Süreç Başlangıcı adım türü (ÇÖZÜLDÜ):** Bağımsız alt süreçlerin **giriş düğümü** için yeni adım türü (process-step
  §3.20); webhook **ve** Süreç Adımı Tetikleme ile tetiklenir; webhook'u tutan aksiyon bu adıma bağlı **`default`**'a dönüşür;
  `ProcessStepInstance.processStepId` doğru atılır. _(process-step §3.20/§4 · sampleProcess/createPdfAsync)_
- **Alt süreç yürütmesinin runtime temsili (ÇÖZÜLDÜ):** Alt süreç tetiklenince **ayrı, yeni bir `ProcessInstance`** oluşur (yeni **Instance/form kaydı** oluşmaz);
  **`parentProcessInstanceId`** = alt sürecin koştuğu **hedef/host instance'ın ana süreci** (**tetikleyen** değil; ana süreçlerde null);
  instance'a bağ bu zincirle **dolaylı** (`ProcessInstance`'a `instance` alanı eklenmez). _(process-step §3.20/§4 ·
  models/processInstances/process-instance.md · service-trigger.md)_
- **Solution & Service modellendi (ÇÖZÜLDÜ):** hiyerarşi `Organization → Solution → Service` netleşti;
  `models/service-settings/solution.md` + `service.md` oluşturuldu (alan ayrıntıları — ikon/versiyon/yetki — sonra).
- **Bildirim dil kapsamı (ÇÖZÜLDÜ — dinamik dil listesi):** bildirim başlık/mesajı sabit TR/EN yerine **dinamik
  `{ languageCode, text }` listesi**; sabit dil setine bağlı kalmadan kayıt-başına-dil genişler. _(process-step §3.6)_
- **Property value (form alan değerleri) depolaması (ÇÖZÜLDÜ — v0.26 model + v0.31 operasyonel):** değerler `InstanceValue.data`
  (JSONB, code-keyed) kaynak-hakikati; fihrist `InstanceAttr`/`InstanceListItem` projeksiyonu (CQRS+Outbox+NATS); yansıma A′ =
  **3 hop / 20 fan-out**; tip şablonları 🟢; **rollup post-MVP**, **retention manuel**; GIN(data)+tipli B-tree(Attr) index. Detay →
  `commitNotes/v0-26`·`v0-31` · `models/processInstances/index.md` · `reflection-propagation.md`.
- **İnsan-görev ailesi ortak modeli (ÇÖZÜLDÜ — v0.32):** Kullanıcı / Kullanıcı Grubu / Üst Form Kullanıcı / Processing **ortak iskelet**
  (adım tipleri ayrı); grup-onay yok · dinamik üyelik · atama-hata fallback · eskalasyon=timeout-hedefi · görev-devri yok→**vekalet** (açık).
  Detay → `commitNotes/v0-32` · `flovo-bpm-engine §4.3/§6.2`.
- **Üst Form Kullanıcı (§3.22) kenar durumlar (ÇÖZÜLDÜ — v0.32):** üstte aksiyon alan yoksa alt kayıt **read-only** · birden fazla üst →
  **ilk tespit** · atananlar kopyalanmaz, **canlı** okunur. Detay → `commitNotes/v0-32` · `process-step §3.22`.
- **`parentProperty` kopyalama anı (ÇÖZÜLDÜ — v0.45):** `snapshot`/`materialized` kopyası **ilişki kurulduğu anda** (`AssociatedInstance` insert)
  üstten alınır, bağ **kaldırılınca `null`**; instance oluşturma anına bağlı değil; `live`'da işlem yok. **Ek kararlar (aynı sürüm):** birden fazla üst
  instance → **birincil üst = en erken bağ** (§3.22 ile aynı) · Designer: bağlayan alan yalnız Form List / tek-seçimli ilişkili Combobox ·
  `parentPropertyId` = **bağlayan alan**, `refPropertyId` = **üst servisteki yansıtılan alan**, `relatedPropertyIds` **kaldırıldı** (eski uygulamada **DataGrid alt-alan/kolon listesi**ydi — `relatedPropertyDtos` ile çift; DataGrid yeni tasarımda yok) ·
  faz: `snapshot`/`live` Motor Faz 1, `materialized` **F1.A.4** ile (öncesinde reddedilir); örnek süreçte alan bazında mod atandı.
  Detay → `commitNotes/v0-45` · `models/processInstances/reflection-propagation.md §3a/§10`.
- **Çekirdek ↔ tipe-özel alan ayrımı (ÇÖZÜLDÜ — v0.31):** tipe-özel ayarlar `Property.settings` **JSONB** (tip-başına JSON Schema);
  ilişkisel-okunan metadata **kolonda** kalır. Detay → `commitNotes/v0-31` · `models/service-settings/property.md §2`.
- **Status: kategori/grup (ÇÖZÜLDÜ — v0.33): gerek yok** — `code`/`definition` yeterli; ayrı kategori/grup boyutu eklenmez. _(status §4)_
- **Çeviri: ortak (null) kaydın sonradan güncellenmesi (ÇÖZÜLDÜ — v0.33):** rutin akış değil; override ayrı satır → **etkilenmez**;
  nadir ihtiyaçta vaka-bazlı **manuel** güncelleme (otomatik kaskad/koruma yok). _(translation §5)_
- **`idleTimeoutMinute` alt/üst sınır (ÇÖZÜLDÜ — v0.33): sınır yok** — `0`=disable, `>0`= organizasyonca belirlenen dakika → **logout**.
  **timezone** ayrı açık konu değil (org timezone alanı planlanmıyor); diğer Organization alanları ihtiyaç anında eklenir. _(organization §4)_
- **Örnekler arası aksiyon kodu adlandırma tutarlılığı (İZLENMEZ — v0.33):** örnek-düzeyi doc-hygiene todo'da tutulmaz; örnekler
  dökümanlar tamamlanınca **baştan eksiksiz** yeniden oluşturulur. _(sampleProcess/index.md)_
- **Aksiyonlarda swipe item (ÇÖZÜLDÜ — v0.33):** ayrı görünüm ayarı değil; `ActionType`'a **`delete`** eklendi (aksiyon → form UI'dan
  kalkar; card'da **swipe item**); `actionDisplayType` değişmedi. _(process-step-action §3.8 · action-type.md)_
- **Customer API dış referans anahtarı (O6) (KONSOLİDE):** ⏭️ Faz 2 — [`todo-phase2.md`](./todo-phase2.md) §13 "Customer API" alt-maddesinde izleniyor (`organizationId` int ↔
  `organizationCode` string); Customer API detaylanınca tek statüye bağlanacak. _(flovo-customer-api §3)_
- **Form validasyon durumu (ÇÖZÜLDÜ — v0.31): `Instance.validated` (bool)** — ayrı `FormValidation` tablosu yok; değer/iş-kuralı
  değişiminde `false`'a döner. _(models/processInstances/instance.md)_
- **Form List ayarları gözden geçir (ÇÖZÜLDÜ — v0.33):** `reOrder` → **profil-bazlı** (view-profile-property); `editOnlyOwnPosition`
  (mapViewer alanı) → **profil-bazlı**; `parameterTransfer`/`propertyTransferParameters` → **tamamen kaldırıldı** (ana↔alt akış artık
  `parentProperty`). _(properties §3.12/§3.13 · view-profile-property.md · form-list.md)_
- **`ActionTransfer` DTO + `action`/`changeList` şekli (ÇÖZÜLDÜ):** `ActionTransfer` **DTO** olarak `models/service-settings/jsonTemplateModels/`
  altına alındı; `action` = **`string?`** (aksiyon kodu; doluysa aynı `code`'lu aksiyon, boş/null → **`default`**) — v0.33;
  `changeList` = **obje-map** `{ Property.code: value }` — v0.30. **Açık kalan:** `ActionTransfer.user` alanı (ayrı madde). _(jsonTemplateModels/action-transfer.md · process-step-action §2/§2.2)_
- **İki-katman sınırı — ÇÖZÜLDÜ (v0.43)** — **değer atama & karşılaştırma** hem süreç adımı hem iş kuralı olarak var; sınır _(← Tier 0)_
  kararları (detay → `business-rule.md` §0.1 · `commitNotes/v0-43.md`):
  - **(S1) Kısıt yok:** no-code platform; bir iş **ikisinde de** ayarlandıysa **ikisi de çalışır** (kombinasyon = tasarımcı senaryosu).
  - **(S2) Değer akışı & bütünlük:** iş kuralı değeri **`changeList` → kaydedilir** (`InstanceValue`); motor adımları **DB'deki kayıtlı
    güncel veriyle** işler (geçici frontend değerine bakmaz). → flovo-bpm-engine §3.1.
  - **(S3) API/webhook başlatma:** frontend'den geçmeyen instance'da iş kuralı **koşmaz** → telafi eden motor adımlarını kurmak
    **süreç tasarımcısının sorumluluğunda** (BPM aracı; senaryo tasarımcıya ait).
  - **(S4) Parite:** iş kuralı ↔ süreç adımı **fonksiyon/operatör + ifade dili hizalı, aynı girdi=aynı çıktı** (backend Go ↔ frontend
    JS+Dart); **Karşılaştırma adımı** `compareType`/operatörleri iş kuralı koşullarıyla **birebir aynı** (→ Tier 3 comparison değer-kaynağı ortak modele hizalanır).
  - **(S5) atlandı** — öncelik/çelişme ayrı açık konu değil.
  - **(S6) Form List:** iş kuralı Form List'ten **okuyup hesaplar**; **toplu alt-servis yazımı yalnız motor Değer Atama adımı** (§3.4).
  _(flovo-bpm-engine §1.4/§3.1 · business-rule §0.1 · process-step §3.4/§3.13)_
