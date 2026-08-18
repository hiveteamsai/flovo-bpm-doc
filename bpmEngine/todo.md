# Flovo BPM — Açık Sorular / TODO (önceliklendirilmiş)

> Tüm tasarım dokümanlarındaki **açık kararlar/sorular** burada **tek yerde** ve **önceliklendirilmiş** toplanır.
> **Kural:** Açık sorular **yalnız bu dosyada** tutulur; diğer dokümanların "Açık Kararlar / Sorular" bölümleri **buraya
> işaretçi** verir (tutarsızlığı önlemek için). Her madde kaynağını `(<doküman> §..)` ile belirtir; çözülünce `[x]`.
>
> **Öncelik mantığı:** Tier 0 = bir kararla **birçok dokümanı** kapatan çapraz-kesen konular · Tier 1 = motor
> çekirdeği (mimari) · Tier 2 = özellik netleştirmeleri · Tier 3 = detay/sonraya.

---

## ⭐ Tier 0 — Çapraz-kesen kararlar (önce bunlar; bir karar → çok doküman)

- [ ] **Genişletilebilirlik — sabit set mi, plugin/SDK ile eklenebilir mi?** Adım / aksiyon / alan setleri.
  _(process-step §4 · process-step-action §7 · properties §4)_
- [ ] **İki-katman sınırı** — **değer atama & karşılaştırma** hem süreç adımı hem iş kuralı olarak var. Sınır:
  iş kuralı = anlık form UX (frontend), adım = kalıcı/akış kararı (motor). Netleşince #Tier1 veri/motor ve
  tutarlılık kalemleri de oturur. _(flovo-bpm-engine §1.4/§12 · business-rule §6 · process-step §3.4/§3.13)_
  - **Not:** İş kuralı (`business-rule.md`) motordan bağımsız frontend'de çalıştığı için **en son** şekillenecek.

---

## 🏗️ Tier 1 — Motor çekirdeği (mimari)

- [ ] **Çalışma-zamanı mimarisi** — tek-süreç mi, kuyruk-tabanlı dağıtık worker mı? Orkestrasyon ↔ yürütme ayrımı;
  durum DB'de, kuyruk yalnız iş ID'leri, worker'lar durumsuz. _(flovo-bpm-engine §2.2 / §12)_
  - 🧱 **Tech-stack (kısmen kapandı):** dağıtım/ölçekleme kararı verildi — MVP **Core BPM monolith** → Hexagonal + **NATS kuyruk** +
    **durumsuz worker** + durum **Postgres/NATS**'ta (SOA-ready); motor-içi **orkestrasyon↔yürütme** ayrımı hâlâ açık. → [`tech-stack/`](./tech-stack/index.md) · [`research/tech-stack/tech_rating.md`](./research/tech-stack/tech_rating.md)
- [ ] **Veri modeli** — token-tabanlı (klasik BPMN) mı, koleksiyon-tabanlı (n8n) mı? Adımlar arası veri temsili/akışı,
  soy ağacı (lineage). _(flovo-bpm-engine §3 / §12)_
- [ ] **Kalıcılık & durum** — ne saklanır (süreç tanımı · instance/state · veri · dosya/binary); durum yaşam döngüsü
  (new/running/waiting/done); saklama/pruning. _(flovo-bpm-engine §8)_
  - 🧱 **Tech-stack:** kalıcılık **substratı** = PostgreSQL + **Partial Event Sourcing** (`workflow_events` append-only); *ne
    saklanır / yaşam döngüsü / pruning* tasarımı açık. → [`tech-stack/postgresql.md`](./tech-stack/postgresql.md)
- [ ] **Property value (form alan değerleri) depolaması — MODEL KATMANI İŞLENDİ (2026-08-04); operasyonel kararlar açık.**
  Değerler `Instance`'ta değil, **`InstanceValue.data` (JSONB, code-keyed)** kaynak-hakikatinde; fihristler `InstanceAttr`/
  `InstanceListItem` projeksiyonu (CQRS + Outbox + NATS). Model dosyaları `models/processInstances/` altında oluşturuldu
  (InstanceValue · InstanceAttr · InstanceListItem · InstanceValueOutbox · InstanceValueChange · LabeledValue);
  `Property` += `projectToAttr`/`hasTranslation`/`reflectionMode`/`reflectionPropagation`/`isReflectionSource` + `code` immutable; **ReflectionMode** + **ReflectionPropagation** enum'ları eklendi.
  _(→ v0.26 · models/processInstances/index.md · research/property-value-storage/index.md 🟢)_
  - **7 alt-sorunun (form-value-scenarios §12) karşılığı:** **(1)** hibrit — JSONB kaynak + tipli projeksiyon; **(2)** yansıma
    `reflectionMode` (snapshot/live/materialized=A′) + `reflectionPropagation` (async/sync); yayılım `AssociatedInstance` + `Property` metadata ile (ayrı tablo yok); **(3)** çeviri — `LabeledValue` + `Attr.display`/
    `translationCode`; **(4)** list-of-model → `InstanceListItem`, Form List → `AssociatedInstance`; **(5)** binary → MinIO URL
    (JSONB'de değil); **(6)** value geçmişi → `InstanceValueChange` (append-only); **(7)** durum → `Instance.statusId` kolonu.
  - **Açık kalan operasyonel kararlar:** **rollup/denormalize dashboard projeksiyonu** (ağır cross-form toplam) · **yansıma
    yayılım (A′) sınırları** (derinlik/döngü — motor **O3** ile ortak) · **retention/pruning + KVKK** (outbox işlenmiş olay ·
    `InstanceValueChange` saklama) · **davranış-dokümanı entegrasyonu** (`service-settings/properties.md` · `flovo-bpm-engine.md`
    yazma/okuma yolu · JSON Schema kapı doğrulama) · GIN/tipli index stratejisi (araştırma dokümanında, kesinleşecek).
  - ✅ **`ReflectionLink` yapısı gözden geçirildi → tablo KALDIRILDI (v0.27):** instance-seviyesi bağ tablosu `AssociatedInstance`'ı
    kopyalıyordu (redundant + staleness). Yeni tasarım: **eşleme `Property.refPropertyId`/`code`** (mevcut) + **instance çözümü
    `AssociatedInstance` ters araması**; ayarlanabilir **`reflectionPropagation` (async vars. / sync guardrail'li)**; outbox +=
    `changedPropertyCodes`/`hopCount`; kaynak alanda `isReflectionSource` hızlı-çıkış bayrağı. → [`models/processInstances/reflection-propagation.md`](./models/processInstances/reflection-propagation.md).
    - ✅ **Referans kapsamı çözüldü (v0.28):** kenarlar **daima doğrudan üst** (tek-hop); **ata** referansı ayrı/non-adjacent
      mekanizma **değil** — ya **röle zinciri** (ara form ata alanını kendi `parentProperty`'si olarak yeniden yayınlar → §4
      kaskadı hop-hop indirir; materialized, sorgulanabilir) ya da **`live`** okuma-anı zincir join (yalnız gösterim). Edge-cache
      ve recursive reverse-join **reddedildi**. → [`reflection-propagation.md` §9](./models/processInstances/reflection-propagation.md).
    - 🔶 **Açık kalan (yalnız sayısal eşikler):** **A′ derinlik/döngü limiti** (motor **O3**) + **`sync` fan-out eşiği** değeri kesinleşecek.
  - 📐 **Tip-bazlı değer şablonları → [`models/processInstances/propertyValuesTemplates/`](./models/processInstances/propertyValuesTemplates/index.md)** (18 tip + core
    `labeled-value.md`). Her `propertyType` için `data` JSONB şekli + `projectToAttr` projeksiyon eşlemesi. **Q1–Q11, Q13 kullanıcı
    kararlarıyla çözüldü** (combobox `value`/id-iki-kolon · groupByTax şema+türetilmiş toplam · formList `AssociatedInstance`-senkron +
    durum→ListItem + `rejectedBy` user-obj · mapViewer `address`→Attr · timePicker `textValue` · phone maskeli · file her-zaman-dizi +
    `fileInfo`{user-obj,date,location-str} · **kullanıcı-referans konvansiyonu** `{userId,nameSurname}`). **Q12 çözüldü:** `InstanceListItem.attrCode`
    = nesne kaleminde **alt-alan adı**, tek atomik değerde sabit **`"value"`**. **Q1–Q13 kapandı**; şablonlar 🟡 TASLAK (ince ayar kullanıcı iterasyonuyla).
  - 📎 **Kaynak/mimari referans:** [`research/property-value-storage/`](./research/property-value-storage/index.md) —
    [`form-deger-saklama-v2.html`](./research/property-value-storage/form-deger-saklama-v2.html) (A'dan Z'ye). _(İsim uyumlaması models/ tarafında yapıldı: `controlTypeId`→`propertyType` · `RelatedInstance`→`AssociatedInstance` · `Instance.delete`→`deleted`.)_
  - 🧱 **Tech-stack:** depolama **substratı** karara bağlandı — PostgreSQL/JSONB · **NATS JetStream** (outbox omurgası) · MinIO
    (binary) · Go (projektör); bu, `form_attr` değerlendirmesindeki **S2/D9 "NATS stack açık" notunu kapatır**. Depolama **MODELİ**
    hâlâ karara bağlanacak. → [`tech-stack/index.md`](./tech-stack/index.md)
- [ ] **Denetim izi (audit) / loglama + dosya/binary depolama performansı** — **loglar nasıl ve nerede tutulacak**
  (workflow/form logları · **ayar değişiklik** logları · sistem logları); organizasyonlar **kendi loglarına** nasıl erişecek
  (izolasyon/yetki); saklama/pruning; mevcut "yavaş belge yükleme" şikâyetiyle doğrudan bağlı; KVKK. _(flovo-bpm-engine §8 / §12)_
  - 🧱 **Tech-stack (kısmen):** **dosya/binary depolama → MinIO** (URL-in-JSONB; "yavaş belge yükleme" çözülür) karara bağlandı;
    **loglama modeli** (nerede/erişim/pruning) hâlâ açık. → [`tech-stack/minio.md`](./tech-stack/minio.md)
  - 📋 **Ayar değişiklik logu — tasarım planı hazır (v0.14), karar bekliyor:** sayfa bazlı denetim izi; tek generic tablo +
    JSONB delta + uygulama katmanı + append-only (`SettingsLog` · `SettingsLogBatch` · `SettingsLogBatchPage`); erişim/yetki
    mevcut `organizationSettings`/`serviceSettings` ikiliği + RLS ile çözülüyor. → [`research/settings-log/index.md`](./research/settings-log/index.md)
    - **Ön koşul:** Customer API'de **ayar yazma / toplu senkron ucu yok** (bugün yalnız `GET /users/{userId}` · `GET /me`) —
      toplu güncelleme loglanmadan önce bu uç tasarlanmalı. _(flovo-customer-api §1)_
    - **Açık:** **saklama süresi / KVKK** (log kişisel veri + ham istek gövdesi içerir; "denetim kaydı silinmez" ↔ silme hakkı — **hukuki karar**) ·
      `requestBody` satır-içi ↔ MinIO **eşiği** · **`HttpMethod` enum'una `patch`** eklenmesi (Customer API zaten `PATCH` kullanıyor).
    - **Bölünmeli:** bu madde **üç** log sınıfını birlikte soruyor (workflow/form · **ayar** · sistem); üçü farklı doğada —
      ayar sınıfı bu planla kapanacak, **sistem logları** (Loki/OTel) için henüz **hiçbir karar yok**.
- [ ] **Ortam (environment) modeli** — **parent-child env** yapısı kurulacak mı? Her ortamın **formları ayrı mı**? Geliştirmeyi
  bir ortamda yapıp **canlı ortamda oluşturulmuş formları görüntüleme** senaryosu nasıl çözülecek? _(environmentRestriction
  alanları: process-step §2 / action · flovo-bpm-engine §8)_
  - **`environmentRestriction` alan formatı** (enum mu, string mi, kapsam) bu modelle birlikte netleşecek — şimdilik **ertelendi**.
    _([`research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](./research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §8)_
- [ ] **Güvenlik** — expression/kod değerlendirme **sandbox**'ı (sert sınır), credential şifreleme/paylaşım,
  riskli adımlar. _(flovo-bpm-engine §10 · process-step-action §5)_
- [ ] **Paralel dallanma / eşzamanlı kollar & join** var mı? Bir adım aynı anda birden çok sonraki adımı tetikler mi?
  Alt servisler (Form List) ana süreçle eşzamanlı mı yürür? _(flovo-bpm-engine §4.5)_
- [ ] **Olay/mesaj-tabanlı tetikleme** ve uyuyan sürecin uyandırılması; çok-örneklilikte "en-fazla-bir-kez"/lider
  seçimi. _(flovo-bpm-engine §5 / §6 / §12)_
  - 🧱 **Tech-stack:** mesaj/olay **omurgası** = **NATS JetStream** (durable consumer + `Nats-Msg-Id` idempotency → "en-fazla-bir-kez");
    BPM-düzeyi *uyandırma / lider-seçimi* tasarımı açık. → [`tech-stack/nats-jetstream.md`](./tech-stack/nats-jetstream.md)

---

## 🔧 Tier 2 — Özellik netleştirmeleri

- [ ] **AI entegrasyon modeli** — deterministik "AI adımı" vs otonom "ajan"; takılabilir strateji (model/memory/araç);
  "herhangi bir adım = araç" + MCP? _(flovo-bpm-engine §11)_
  - 🧱 **Tech-stack:** AI **substratı** = **Python AI Service** (🟡 post-MVP) + **pgvector**; entegrasyon **MODELİ** açık. → [`tech-stack/python-ai-service.md`](./tech-stack/python-ai-service.md)
- [ ] **Hata yönetimi** — her adımda `onFail` var mı/zorunlu mu; **retry** (deneme + bekleme); süreç-seviye global
  hata yakalayıcı; telafi/compensation; `action` zinciri **sonsuz döngü** koruması. _(flovo-bpm-engine §7 · process-step-action §7)_
- [ ] **İnsan-görev ailesi ortak modeli** — Kullanıcı / Kullanıcı Grubu / Processing için atama + bekleme.
  _(process-step §4)_ · _(Processing'in ilerleme farkı **çözüldü**: `default` kodlu `autoAction` varsa otomatik ilerler, yoksa bekler → process-step §3.18)_
- [ ] **Üst Form Kullanıcı (§3.22) — kenar durumlar** — alt-servisin üst formun atananlarını/görünümünü devraldığı yeni
  adım (Parent Instance User) çekirdeği tanımlandı; **açık kalan:** (a) üst form **bulunamazsa** (bağ yok/kaldırılmış)
  davranış; (b) üst form **otomatik adımda** olup aksiyon bekleyeni yokken görünüm/atanan; (c) **birden fazla** üst form
  eşleşirse ayrıştırma kuralı; (d) üst form **Süreç Bitişi**'ne ulaşınca alt-servisin yaşam döngüsü; (e) atananların
  **kopyalanması vs okuma-zamanı** çözümü (öneri: anlık). _(process-step §3.22 · flovo-bpm-engine §4.3 · AssociatedInstance)_
- [ ] **Form List ayarları gözden geçir** — `reOrder` · `parameterTransfer` · `propertyTransferParameters` ·
  `editOnlyOwnPosition` nasıl yönetilecek (profil-bazlı mı)? _(properties §4 / §3.13)_ · _(`addNewEnabled`→`activeStartActions`,
  `addFromExistingRecordsIsActive`→`addFromExistingStatusIds` (profil), `selectedEnable`→`selectableVisible` (profil): **çözüldü**.)_
- [ ] **Timer üçlüsü** (Timer / Timer Start / Timer End) yaşam döngüsü ve bağlanması; global timer kayıtları?
  _(process-step §4)_
  - **Netleşen (v0.12):** `TimerCalculationType` + `ProcessStepTimerSettings` (çalışma/normal/sabit takvim blokları + timeout
    bildirimi) modellendi; **yaşam döngüsü/bağlanma** (`selectedTimerProcessStepId`, global timer kayıtları) hâlâ açık. _(process-step §3.7)_
- [ ] **Form yaşam döngüsü** — Instance Creator / Instance Deleter / Form Yönlendirme / Süreç Adımı Tetikleme; Parent Property
  ile birlikte. _(process-step §4)_
  - **Netleşen (v0.12):** **Instance Deleter** `deleteMode` (`InstanceDeleteMode`: `withRelated`/`unlinkRelated`) + **Instance Creator**
    temel ayar modeli tanımlandı; **Form Yönlendirme / Süreç Adımı Tetikleme** hâlâ açık. _(process-step §3.9/§3.15/§3.16)_
- [ ] **ServiceTrigger — kalan kenar durumlar** _(models/service-settings/service-trigger.md · enums/service-trigger-type.md)_.
  Model **inşa edildi ve olgunlaştırıldı** (v0.23): `serviceTriggerType` (`timer`/`whenAddedAssociate`/`whenRemoveAssociate`) ·
  `cronExpression` (timer) · `targetPropertyId` (associate) · `targetServiceId` · `targetStarterProcessStepId` (`subProcessStart`) ·
  `async` · `parameters` (DynamicParameter[]) + kimlik/yaşam-döngüsü alanları (`code`/`definition`/`order`/`active`/`deleted`).
  - **Çözülen (v0.23):** associate **tespiti** = `AssociatedInstance` yazımında (DB katmanı, **çekirdek**; ayrı yerlerde
    tekrarlanmaz) · associate **filtresi** = `targetPropertyId` (`associatedPropertyId == targetPropertyId` → kaynak =
    `associatedInstanceId`; "hangi taraf" belirsizliği kapandı) · **`timer`** = `cronExpression` + **`processStart`**
    (alt süreç değil; her cron tetiğinde **yeni bağımsız ana süreç**, servis-global, kaynak instance yok) · associate →
    `subProcessStart` · **`async=false`** = başlatılan süreç **Süreç Bitişi'ne** ulaşana kadar bekler, `async=true` = beklenmez ·
    **karşı-instance parametresi gereksiz** · kimlik/yaşam-döngüsü alanları eklendi · **`triggerProcessStep` ile sınır**
    (triggerProcessStep = akış-üzeri adım, girince alt süreç/aksiyon tetikler ↔ ServiceTrigger = akış-dışı otomatik olay/cron).
  - **Çözülen (v0.24, expenseAndCreditCard örneğiyle):** **kaynak ↔ hedef ayrımı** — `parameters` **kaynağı = `associatedInstanceId`**
    (üst form); **yürütme hedefi = `instanceId`** (targetService'teki **mevcut** instance). Associate alt süreci **yeni Instance (form kaydı)
    oluşturmaz**; hedef instance için **yeni bir alt-`ProcessInstance`** olarak koşar — **`parentProcessInstanceId` = hedef
    instance'ın ana `ProcessInstance`'ı** (tetikleyen `associatedInstanceId` değil); instance'a bağ bu zincirle **dolaylı**
    (statü okur, `triggerProcessStep` ile ana-akış aksiyonu tetikler). Önceki "parent=associatedInstanceId" ifadesi düzeltildi.
  - **Çözülen (v0.25):** **hedef servis ↔ hedef alan invariant'ı** (`targetServiceId == targetPropertyId'nin childServiceId/associatedServiceId`'si;
    kaydetme-anı doğrulaması) · **`async` bekleme yeri** (bekleme, ilişki değişikliğini/`AssociatedInstance` yazımını yapan **tetikleme noktasında**
    yapılır) · **`subProcessStart` tetikleme kataloğuna ServiceTrigger (associate) eklendi** (process-step §3.20/§3.16).
  - **Açık kalan:** **(1) `timer` saat dilimi/DST** — cron'un değerlendirileceği saat dilimi (Organization timezone alanı henüz
    açık) + DST geçişleri; **(2) döngü koruması** — A→B→A tetikleme recursion'ı (derinlik/çevrim sınırı) _(tasarım-zamanı önleme
    örneği: `isAssociatedCombobox=false` geri-referans — `sampleProcess/expenseAndCreditCard/creditCardStatementLine.md`; motor-düzeyi
    güvenlik ağı açık)_; **(3) `async` kaskad kompozisyonu** — üst üste `async=false` senkron derinlik yaratır; seviyeler boyunca
    async + işlem/derinlik sınırı (Senaryo 5 kaskadı); **(4) `triggerProcessStep` → ilişkili instance (associatedInstance) tetikleme** —
    Süreç Adımı Tetikleme adımı, ilişkili instanceların **alt sürecini/aksiyonunu** tetikleyebilir; hangi associatedInstance'ların
    seçileceği (ilişki alanı/yön) + ayar detayları **tanımlanacak** (process-step §3.5/§3.20). _(Not: "alt sürecin mevcut-instance
    mekaniği" → **ÇÖZÜLDÜ v0.25**: yeni alt-`ProcessInstance`, `parentProcessInstanceId`=hedef instance'ın anası; `ProcessInstance`'a `instance` alanı eklenmez.)_
- [ ] **Raporlama** ayrı özellik olarak nasıl modellenecek? _(view-profile §3 / §5)_
- [ ] **Customer API** — kimlik/yetki (token kapsam/süre/yenileme); webhook güvenliği (secret/imza) + **idempotency**;
  `POST /instances/search` sorgu dili; rate limit/sayfalama/hata sözleşmesi; request/response şemaları. _(flovo-customer-api §3)_
  - **Dış referans anahtarı — statü çelişkisi (O6):** `flovo-customer-api.md` header'da `organizationId` kullanıp konuyu **açık**
    sayıyor; `organization.md`/`models/index.md` ise **`organizationCode` (string) kararlaştırıldı** diyor. **Customer API detaylanınca
    tek statüye** bağlanacak (o zamana dek atlandı).
  - 🧱 **Tech-stack (kısmen):** kimlik = **Keycloak** (token) · sözleşme/şema = **OpenAPI** (api-contract) · idempotency deseni =
    **NATS**; API'nin kendi tasarımı (search sorgu dili, rate limit, webhook imza) açık. → [`tech-stack/keycloak.md`](./tech-stack/keycloak.md) · [`tech-stack/api-contract.md`](./tech-stack/api-contract.md)
- [ ] **Yetkilendirme (permissions) — açık kalanlar:** **(a)** `ProcessStepAction.authorizationLevel` (aksiyon-düzeyi sayısal
  yetki) yeni **org-bazlı** yetki modeliyle nasıl uyumlanır; **(b)** **impersonation** kapsamı/denetimi (kimin yerine
  geçilebilir; log/audit); **(c)** yetki setinin **genişletilebilirliği** (yeni yetki = Organization'a yeni `*UserGroupId`
  alanı mı, dinamik mi?); **(d)** admin-only yetki yapılandırması ↔ `OrganizationSettings` grubu erişim sınırı.
  _(permissions §5 · organization §5 · new-vs-current §14)_
- [ ] **Aksiyon parametrelerinde ifade/kod desteği** — parametreler ne kadar "ifade" (expression/kod) destekleyecek
  (no-code ↔ pro-code dengesi); ifade motoru + veri eşleme (sürükle-bırak) + koşullu çalışma kapsamı. _(process-step-action §5 / §7)_
- [ ] **Çekirdek ↔ tipe-özel alan ayrımı nihai mi** — hangi alanlar `Property` çekirdeğinde, hangileri tipe-özel ayar;
  şişman modelin sadeleştirme sınırı. _(properties §4 · new-vs-current §14)_
- [ ] **Kapsam-dışı varlıklar + Org ↔ BPM entegrasyonu** — ExpenseType / Currency / Tax modellensin mi;
  organizasyon ayarlarının BPM ile entegrasyon derinliği. _(Position/Staff modellendi → `position.md`.)_ _(index.md §4 · new-vs-current §14)_
- [ ] **ActionTransfer'e `user` alanı** — `ActionTransfer` (parameters/changeList/action → process-step-action §2) modeline
  bir **user** property'si eklenmeli mi (aksiyon/parametre verisinden `Instance.creatorUserId`'yi **isteğe bağlı** set etmek için)?
  _(process-step-action §2 · process-step §3.12 · `apiKeyId` açık sorusuyla bağlantılı)_
  - **Netleşen (v0.17):** "`form` tipinde `creatorUserId` **zorunlu dolu**" kuralı **kaldırıldı** — süreç **API/webhook ile**
    (tek oluşturan kullanıcı olmadan, ör. gruba yönlendirilerek → `sampleProcess/referred`) başlatılabildiğinden
    `creatorUserId` **null olabilir**; başlatan **`ProcessInstance.createdByApiKeyId`** ile izlenir. Açık kalan: yalnız
    ActionTransfer.user ile creatorUserId'nin **opsiyonel atanması**.
- [ ] **Form List tik (seçim) davranışı** — formların yanındaki **tiklerde** yapılan değişiklikler **aksiyon tetikleyecek mi**?
  **Tik kaldırma nedeni** kullanıcıdan nasıl alınacak ve nasıl kaydedilecek? _(properties §3.13 Form List · `selectableVisible`/
  `selectedEditable` · view-profile §5)_
- [ ] **"Var olanlardan ekleme" filtreleri** — bugün yalnız **durum** (`addFromExistingStatusIds`) ile filtre var; ek olarak
  "yalnız **related-form** olanlar listelensin", "hangi **property** ile related olanlar listelensin" gibi seçenekler nasıl
  yönetilecek? _(view-profile §5 · properties §3.13 Form List · AssociatedInstance)_
- [ ] **Ortamlar arası değişiklik aktarımı (promote/rollback)** — bir ortamda yapılan değişiklikleri **canlıya aktarma** ve
  **geri alma** yöntemi; ortamlar arası **pull-request** benzeri bir yapı nasıl kurulabilir? _(→ Tier 1 "Ortam (environment) modeli")_
- [ ] **Servis template & JSON ile servis oluşturma** — servisler **template** olarak nasıl oluşturulacak; template ile servis
  üretimi nasıl olacak; **n8n gibi JSON template** export/import ile mi; **ilişkili servisler toplu** mı oluşturulacak?
  _(models/service-settings/service.md · solution.md · research/n8n)_

---

## 🧩 Tier 3 — Detay / sonraya

- [ ] **`actionDisplayType`** gözden geçir (`invisible`/`everywhere`/`onlyFormDetail`/`onlyFastApprove`). _(action §3)_
- [ ] **`changeList` öğe yapısı** (alan id + yeni değer + tip?) ve **`action` nesnesinin şekli**. _(process-step-action §7)_
- [ ] **İş kuralı performansı** — `always` kuralları yalnız ilgili property değişince (alan-bağımlı) tetiklensin mi?
  _(business-rule §6)_
- [ ] **Status: kategori/grup** — raporlama/filtreleme için `code`/`definition` yeterli mi, ayrı kategori boyutu gerekli mi?
  _(status §4)_ · _(icon/definition rengi = `styleId`.`fontColor` — **çözüldü**.)_
- [ ] **Çeviri** — ortak (`null`) kayıt sonradan güncellenince, onu **ezmiş** organizasyon kayıtları etkilenmemeli (teyit).
  _(translation §5)_
- [ ] **`idleTimeoutMinute` alt/üst sınır** + Organization sonraki alanlar (plan/abonelik, timezone, para birimi, bölge,
  güvenlik). _(Kilit davranışı **çözüldü** (v0.18): kilitlenince yeniden giriş/login gerekir → log.)_ _(organization §4)_
- [ ] **Örnekler arası aksiyon kodu adlandırma tutarlılığı** — sampleProcess örneklerinde kod adları (`default` vb.) tutarlı
  tutulmalı (doc-hygiene). _(sampleProcess)_
- [ ] **Aksiyonlarda swipe item** — process-step-action'lar için görünüm (`styleId`/`actionDisplayType`) yerine ya da ek olarak
  **swipe item** (kaydırmalı aksiyon) eklenmeli mi? _(process-step-action §4 · action §3 `actionDisplayType`)_

---

## 🆕 Bu oturumda eklenen açık sorular

- [x] **Customer API dış referans anahtarı (O6) — Tier 2'ye konsolide edildi:** aynı soru Tier 2 "Customer API" alt-maddesinde
  (**O6**, `organizationId` int ↔ `organizationCode` string) izleniyor; mükerrer kayıt kaldırıldı.
- [ ] **`apiKeyId` içeriği/adı (Customer API kimliği)** — Customer API ile oluşturulan kayıtlarda oluşturan **User**
  olmadığından işlemi kimin yaptığını kaydetmek için `apiKeyId` alanları var (`ProcessInstance.createdByApiKeyId`,
  `ProcessStepInstance.atApiKeyId`). **Ad geçici**; içine gelecek veri Customer API **erişim mekanizması** kesinleşince
  doğrulanacak. _(flovo-customer-api §3 · models/processInstances/process-instance.md · process-step-instance.md)_
- [ ] **Form validasyon durumu — `Instance.validated` (bool) mü, `FormValidation` tablosu mu?** İş akışından validasyonları **sürekli
  tekrar yapmamak** ve **iş kuralı** (BusinessRule `applyValidation`) ile oluşturulan validasyonlarla **tutarsızlık yaşamamak** için:
  `Instance` modeline **`validated` (bool)** alanı mı eklenmeli, yoksa ayrı bir **`FormValidation`** tablosu mu oluşturulmalı? Karar
  sonraya. _(models/processInstances/instance.md · business-rule.md `applyValidation` · flovo-bpm-engine.md)_

### 🔎 Tutarlılık denetiminden (2026-07-02)
- [ ] **`ProcessStep`/`BusinessRule` denormalize `organizationId`** — asıl kapsayıcı `serviceId`; kiracı için ayrıca
  `organizationId` tutulsun mu, yoksa `service → solution → org` üzerinden mi? _(models)_

### 🔧 v0.12 — Adım tipe-özel ayar modellemesinden (2026-07-16)
- [ ] **Flovo AI adım ayarları detayı** — `selectedAi` kanonik AI seti; `fileSourceType` (thumbnail/fileProperty) ayrı enum mü;
  AI'a-özel `aiSettings` şeması. _(process-step §3.2)_
- [ ] **Adım `settings` JSONB doğrulama & referans bütünlüğü** — tip-başına **JSON Schema**; `settings` içindeki referans id'lerin
  (`propertyId`/`userGroupId`/`selectedTimerProcessStepId`…) **uygulama-katmanı** doğrulaması + **silme koruması**. _(process-step §2)_
- [ ] **`triggerProcessStep` / `formRedirect` adım ayarları** — henüz modellenmedi (ayarsız grup §3.16). _(process-step §3.16)_
- [ ] **`DynamicParameter.value` şekli** — değer-kaynağı (**ValueAssignType**: sabit/hesaplama/form property) + değerin JSONB
  temsili (iş-kuralı `AssignValueToFieldDto` muadili). _(process-step §3.1/§3.6)_

---

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
  (profil). _(Açık kalan `reOrder`/`editOnlyOwnPosition` profil-bazlılığı → Tier 2 "Form List ayarları gözden geçir".)_
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
- **Kapsam kararı — servis-bazlı mı, paylaşımlı mı? (ÇÖZÜLDÜ):** hiyerarşi ile — **organizasyon havuzu** = Translation / Style /
  Status / Action (organizasyona bağlı, tüm servislerde); **servis-bazlı** = Property / ProcessViewProfile / ProcessStep /
  BusinessRule. _(action §3 · status §4 · business-rule §6 · view-profile §5)_
- **Bulut + on-prem hibrit dağıtım (ÇÖZÜLDÜ — tech-stack):** **on-prem + Private Cloud ready** (K8s OpenShift + BYO + tek Helm
  umbrella); merkezi-kimlik çelişkisi **Keycloak AD/LDAP federasyonu** ile giderildi. Kalan minör: saf-on-prem'de sosyal-login
  kapsamı. → [`tech-stack/kubernetes-helm.md`](./tech-stack/kubernetes-helm.md) · [`tech-stack/keycloak.md`](./tech-stack/keycloak.md)
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
