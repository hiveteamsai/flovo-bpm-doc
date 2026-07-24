# Flovo BPM — Açık Sorular / TODO (önceliklendirilmiş)

> Tüm tasarım dokümanlarındaki **açık kararlar/sorular** burada **tek yerde** ve **önceliklendirilmiş** toplanır.
> **Kural:** Açık sorular **yalnız bu dosyada** tutulur; diğer dokümanların "Açık Kararlar / Sorular" bölümleri **buraya
> işaretçi** verir (tutarsızlığı önlemek için). Her madde kaynağını `(<doküman> §..)` ile belirtir; çözülünce `[x]`.
>
> **Öncelik mantığı:** Tier 0 = bir kararla **birçok dokümanı** kapatan çapraz-kesen konular · Tier 1 = motor
> çekirdeği (mimari) · Tier 2 = özellik netleştirmeleri · Tier 3 = detay/sonraya.

---

## ⭐ Tier 0 — Çapraz-kesen kararlar (önce bunlar; bir karar → çok doküman)

- [x] **Kapsam kararı — servis-bazlı mı, paylaşımlı mı?** **ÇÖZÜLDÜ** (hiyerarşi ile): **organizasyon havuzu** =
  Translation / Style / Status / Action (organizasyona bağlı, tüm servislerde kullanılır); **servis-bazlı** =
  Property / ProcessViewProfile / ProcessStep / BusinessRule. _(action §3 · status §4 · work-rule §6 · view-profile §5)_
- [ ] **Genişletilebilirlik — sabit set mi, plugin/SDK ile eklenebilir mi?** Adım / aksiyon / alan setleri.
  _(process-step §4 · process-step-action §7 · properties §4)_
- [ ] **İki-katman sınırı** — **değer atama & karşılaştırma** hem süreç adımı hem iş kuralı olarak var. Sınır:
  iş kuralı = anlık form UX (frontend), adım = kalıcı/akış kararı (motor). Netleşince #Tier1 veri/motor ve
  tutarlılık kalemleri de oturur. _(flovo-bpm-engine §1.4/§12 · work-rule §6 · process-step §3.4/§3.13)_
  - **Not:** İş kuralı (`business-rule.md`) motordan bağımsız frontend'de çalıştığı için **en son** şekillenecek.

---

## 🏗️ Tier 1 — Motor çekirdeği (mimari)

- [ ] **Çalışma-zamanı mimarisi** — tek-süreç mi, kuyruk-tabanlı dağıtık worker mı? Orkestrasyon ↔ yürütme ayrımı;
  durum DB'de, kuyruk yalnız iş ID'leri, worker'lar durumsuz. _(flovo-bpm-engine §2.2 / §12)_
  - 🧱 **Tech-stack (kısmen kapandı):** dağıtım/ölçekleme kararı verildi — MVP **Core BPM monolith** → Hexagonal + **NATS kuyruk** +
    **durumsuz worker** + durum **Postgres/NATS**'ta (SOA-ready); motor-içi **orkestrasyon↔yürütme** ayrımı hâlâ açık. → [`tech-stack/`](./tech-stack/index.md) · [`research/tech-stack/tech_rating.md`](./research/tech-stack/tech_rating.md)
- [x] **Bulut + on-prem hibrit dağıtım — ÇÖZÜLDÜ (tech-stack):** **on-prem + Private Cloud ready** (K8s OpenShift + BYO + tek
  Helm umbrella); merkezi-kimlik çelişkisi **Keycloak AD/LDAP federasyonu** ile giderildi (müşterinin kendi AD/LDAP'ı; merkezi-cloud
  bağımlılığı yok). _(Kalan minör: saf-on-prem'de sosyal-login kapsamı.)_ → [`tech-stack/kubernetes-helm.md`](./tech-stack/kubernetes-helm.md) · [`tech-stack/keycloak.md`](./tech-stack/keycloak.md)
- [ ] **Veri modeli** — token-tabanlı (klasik BPMN) mı, koleksiyon-tabanlı (n8n) mı? Adımlar arası veri temsili/akışı,
  soy ağacı (lineage). _(flovo-bpm-engine §3 / §12)_
- [ ] **Kalıcılık & durum** — ne saklanır (süreç tanımı · instance/state · veri · dosya/binary); durum yaşam döngüsü
  (new/running/waiting/done); saklama/pruning. _(flovo-bpm-engine §8)_
  - 🧱 **Tech-stack:** kalıcılık **substratı** = PostgreSQL + **Partial Event Sourcing** (`workflow_events` append-only); *ne
    saklanır / yaşam döngüsü / pruning* tasarımı açık. → [`tech-stack/postgresql.md`](./tech-stack/postgresql.md)
- [ ] **Property value (form alan değerleri) depolaması** — `Instance`'un alan değerleri **nerede/nasıl** tutulacak: `Instance`
  modelinde mi, ayrı value tablo(lar)ında mı; tip-bazlı sütun mu, referans mı? Daha detaylı araştırma sonrası
  kararlaştırılacak; alan-düzeyi tanımlar ayrı **değer dokümantasyonunda** yapılacak.
  _(form-value-scenarios §5/§12 · models/processInstances/instance.md)_
  - Alt-sorular (form-value-scenarios §12): **(1)** EAV ↔ kolon ↔ JSON ↔ hibrit; **(2)** yansıma alanları A (kopya+senkron)
    ↔ B (on-read), snapshot ↔ canlı; **(3)** çeviri-bağımlı sorgu/indeksleme; **(4)** list-of-model (alt-servis) unnest /
    cross-form; **(5)** binary/dosya ayrımı; **(6)** value geçmişi/sürümleme; **(7)** instance/state serileştirme.
  - 📎 **Araştırma girdisi (değerlendirme bekliyor):** [`research/property-value-storage/`](./research/property-value-storage/index.md)
    — CQRS Projection · Outbox · Postgres/JSONB tabanlı bir mimari öneri (yukarıdaki alt-soruların çoğunu ele alıyor). Karara bağlanınca buraya işlenecek.
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
  _(process-step §4)_ · _(Processing'in ilerleme farkı **çözüldü**: frontende response döner ama beklemez, `default` ile ilerler → process-step §3.18)_
- [ ] **Form List / alt-servis yaşam döngüsü** — 3 dokümanda ortak: alt-servisin görüntülenecek alanları/seçilebilirliği
  view-profile ile nasıl; veri/`changeList`/parametre nasıl akar. _(properties §3.13 · process-step §4 · view-profile §5)_
- [x] **Alan-özel görünüm ayarlarının profil bazında yönetimi** — **KARAR (B2):** `ProcessViewProfilePropertySetting
  {viewProfilePropertyId, key, value}` (propertyType'a göre **dictionary**; katalog → `models/service-settings/view-profile-property.md`).
  Form List: `addNewEnabled`→**`activeStartActions`** (ProcessStepAction id listesi), `addFromExistingRecordsIsActive`→
  **`addFromExistingStatusIds`** (Status id listesi) profil'e taşındı; `selectedEnable`→**`selectableVisible`** (profil-bazlı;
  eski alan-düzeyi `selectableModeActive` **kaldırıldı**) + öneri `selectedEditable` (profil).
  **Kalan:** `reOrder`/`editOnlyOwnPosition` de profil-bazlı mı? _(view-profile §5 · properties §4)_
- [ ] **Form List ayarları gözden geçir** — `reOrder` · `parameterTransfer` · `propertyTransferParameters` ·
  `editOnlyOwnPosition` nasıl yönetilecek (profil-bazlı mı)? _(properties §4 / §3.13)_ · _(`addNewEnabled`→`activeStartActions`,
  `addFromExistingRecordsIsActive`→`addFromExistingStatusIds` (profil), `selectedEnable`→`selectableVisible` (profil): **çözüldü**.)_
- [ ] **Combobox/Radiobutton seçenek kaynağı** — statik (`propertyItems`) ↔ dinamik (`dataSource`) modeli ve iş kuralı
  `fillDataSource` ile ilişkisi; `fillDataSource` kaynak tipleri (Organization/User/API). _(properties §4 · work-rule §6)_
- [ ] **Timer üçlüsü** (Timer / Timer Start / Timer End) yaşam döngüsü ve bağlanması; global timer kayıtları?
  _(process-step §4)_
  - **Netleşen (v0.12):** `TimerCalculationType` + `ProcessStepTimerSettings` (çalışma/normal/sabit takvim blokları + timeout
    bildirimi) modellendi; **yaşam döngüsü/bağlanma** (`selectedTimerProcessStepId`, global timer kayıtları) hâlâ açık. _(process-step §3.7)_
- [ ] **Süreç Bitişi "önceki adıma taşıma"** — yeniden-açma (re-open) mı, ayrı akış mı? Denetim izine etkisi.
  _(process-step §4)_
- [ ] **Form yaşam döngüsü** — Instance Creator / Instance Deleter / Form Yönlendirme / Süreç Adımı Tetikleme; Parent Property
  ile birlikte. _(process-step §4)_
  - **Netleşen (v0.12):** **Instance Deleter** `deleteMode` (`InstanceDeleteMode`: `withRelated`/`unlinkRelated`) + **Instance Creator**
    temel ayar modeli tanımlandı; **Form Yönlendirme / Süreç Adımı Tetikleme** hâlâ açık. _(process-step §3.9/§3.15/§3.16)_
- [ ] **`default action` kavramı** — her adımda mı, yoksa yalnız HTTP Request(async)/Timer gibi adımlarda mı?
  _(process-step §4)_
- [ ] **Raporlama** ayrı özellik olarak nasıl modellenecek? _(view-profile §3 / §5)_
- [ ] **`changeViewProfile`** çalışma-zamanı profil değişiminin akış (motor) ile etkileşimi. _(view-profile §5)_
- [ ] **Customer API** — kimlik/yetki (token kapsam/süre/yenileme); webhook güvenliği (secret/imza) + **idempotency**;
  `POST /instances/search` sorgu dili; rate limit/sayfalama/hata sözleşmesi; request/response şemaları. _(flovo-customer-api §3)_
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
- [ ] **Processing'de "durum değişimi" alanı** nasıl tutulacak (Processing otomatik ilerlerken durumu neyle değiştirir).
  _(process-step §4 · sampleProcess)_
- [ ] **Kapsam-dışı varlıklar + Org ↔ BPM entegrasyonu** — ExpenseType / Currency / Tax modellensin mi;
  organizasyon ayarlarının BPM ile entegrasyon derinliği. _(Position/Staff modellendi → `position.md`.)_ _(index.md §4 · new-vs-current §14)_
- [ ] **ActionTransfer'e `user` alanı + API-başlatımlı `creatorUserId` tespiti** — `ActionTransfer` (parameters/changeList/
  action → process-step-action §2) modeline bir **user** property'si eklenmeli mi? **API ile başlatılan** süreçlerde **Instance
  Creator** (§3.12), kullanıcı olmadığından `Instance.creatorUserId`'yi **nasıl tespit edecek**? _(process-step-action §2 ·
  process-step §3.12 · models/processInstances/instance.md · `apiKeyId` açık sorusuyla bağlantılı)_
- [ ] **Alt-servis süreçlerinde `parentViewProfile` seçeneği** — Kullanıcı/Kullanıcı Grubu adımlarında `processViewProfileId`
  **statik** seçiliyor. Alt-servis olarak çalışan süreçlerde bunun yerine "**parent'ın view-profile'i ile aynı `code`'a sahip**
  view-profile'i kullan" gibi bir **parentViewProfile** seçeneği mi eklenmeli, yoksa farklı bir yöntemle mi ilerlenmeli?
  _(process-step §3.15/§3.16 · view-profile §5)_
- [ ] **Form List tik (seçim) davranışı** — formların yanındaki **tiklerde** yapılan değişiklikler **aksiyon tetikleyecek mi**?
  **Tik kaldırma nedeni** kullanıcıdan nasıl alınacak ve nasıl kaydedilecek? _(properties §3.13 Form List · `selectableVisible`/
  `selectedEditable` · view-profile §5)_
- [ ] **"Var olanlardan ekleme" filtreleri** — bugün yalnız **durum** (`addFromExistingStatusIds`) ile filtre var; ek olarak
  "yalnız **related-form** olanlar listelensin", "hangi **property** ile related olanlar listelensin" gibi seçenekler nasıl
  yönetilecek? _(view-profile §5 · properties §3.13 Form List · RelatedInstance)_
- [ ] **Alt süreç ProcessInstance'ları ayrı tabloda mı?** — Bağımsız alt süreçler (`parentProcessInstanceId`) ana `ProcessInstance` tablosunda mı,
  yoksa **ayrı bir tablo/sayfa**da mı tutulmalı? Fayda/eksi (izolasyon · sorgu maliyeti · raporlama · listeleme). _(models/
  processInstances/process-instance.md · process-step §3.20)_
- [ ] **Ortamlar arası değişiklik aktarımı (promote/rollback)** — bir ortamda yapılan değişiklikleri **canlıya aktarma** ve
  **geri alma** yöntemi; ortamlar arası **pull-request** benzeri bir yapı nasıl kurulabilir? _(→ Tier 1 "Ortam (environment) modeli")_
- [ ] **Servis template & JSON ile servis oluşturma** — servisler **template** olarak nasıl oluşturulacak; template ile servis
  üretimi nasıl olacak; **n8n gibi JSON template** export/import ile mi; **ilişkili servisler toplu** mı oluşturulacak?
  _(models/service-settings/service.md · solution.md · research/n8n)_

---

## 🧩 Tier 3 — Detay / sonraya

- [ ] **`defaultAction` (bool) ↔ `default` (kod)** — ikisi de "varsayılan"ı işaret ediyor; nasıl birleşir?
  _(action §3 · process-step-action §7)_
- [x] **ActionDto: kopya ↔ canlı referans** — **ÇÖZÜLDÜ:** adıma eklenince alanlar **bir kez kopyalanır**, kopya **bağımsızdır**; Action değişince mevcut adım-aksiyonları güncellenmez (FK/canlı bağ yok). _(action §3)_
- [ ] **`actionDisplayType`** gözden geçir (`invisible`/`everywhere`/`onlyFormDetail`/`onlyFastApprove`). _(action §3)_
- [x] **`eventForm` formu** — **ÇÖZÜLDÜ:** `formType = eventForm` olan servisin **görüntüleme profilidir**; aksiyon alınırken seçili profildeki alanlar **pop-up** olur, sonuç **`parameters`** ile taşınır (`Instance`/akış yok). _(process-step-action §3.2 · models/service-settings/service.md)_
- [ ] **`changeList` öğe yapısı** (alan id + yeni değer + tip?) ve **`action` nesnesinin şekli**. _(process-step-action §7)_
- [ ] **`assignValueToPropertyAttribute`** adı teyit. _(work-rule §6)_
- [ ] **İş kuralı performansı** — `always` kuralları yalnız ilgili property değişince (alan-bağımlı) tetiklensin mi?
  _(work-rule §6)_
- [ ] **Status: kategori/grup** — raporlama/filtreleme için `code`/`definition` yeterli mi, ayrı kategori boyutu gerekli mi?
  _(status §4)_ · _(icon/definition rengi = `styleId`.`fontColor` — **çözüldü**.)_
- [ ] **Style kapsamı** — yalnız bg+font mı, daha fazlası mı (fontSize/isBold/border/iconColor)? Tema/dark mode; bg/font
  **kontrast** kontrolü. _(style §4)_
- [ ] **Çeviri** — ortak (`null`) kayıt sonradan güncellenince, onu **ezmiş** organizasyon kayıtları etkilenmemeli (teyit).
  _(translation §5)_
- [ ] **`translationCode` ad-uzayı kuralı** — anahtar **serbest metin**; değeri **kim üretir**? (a) kullanıcı serbest girer,
  (b) `<varlık>.<code>` (örn. `department.01`) **otomatik** üretilir, (c) hibrit (öneri + düzenlenebilir). Bağlı sorular:
  iş `code`'u değişince anahtar ne olur (sabit kalır / birlikte değişir); iki kaydın **kasıtlı aynı anahtarı** paylaşması
  serbest mi; anahtar için benzersizlik kısıtı olmalı mı (şu an **yok** — çakışma artık **mümkün ama kasıtlı**).
  _(translation §3.1 · models/index.md Notlar)_
- [x] **Çeviri eşleşme anahtarı — ÇÖZÜLDÜ (v0.13):** Çeviri, modellerin **iş kodu (`code`)** üzerinden yapılıyordu; `code`
  **model-içi** benzersiz, çeviri ad-uzayı ise **organizasyon geneli** ve varlık ayrımı yok → Departman `"01"` ile Şirket `"01"`
  **aynı çeviri satırına çakışıyordu**. Çözüm: **23 model/alt-modele ayrı, nullable `translationCode`**
  (`Model.translationCode → Translation.code`); **`null` = çeviri es geçilir → `definition`** (opt-in).
  _(translation §3/§3.1 · models/index.md · new-vs-current §0/§9)_
- [ ] **`idleTimeoutMinute`** alt/üst sınır; oturum kilitlenince davranış (yeniden giriş mi, yalnız parola mı)?
  Organization sonraki alanlar: plan/abonelik, timezone, para birimi, bölge, güvenlik. _(organization §4)_
- [x] **`actionType` isim çakışması — ÇÖZÜLDÜ (v0.7):** BusinessRule alanı `actionType` → **`businessRuleActionType`**
  olarak yeniden adlandırıldı; **`Action.actionType`** aynen kaldı. _(business-rule.md · index.md Notlar · business-rule-action-type.md)_
- [ ] **`valueType` isim çakışması** — AdditionalQualification `valueType` (**QualificationValueType**: string/double/dateTime/combobox)
  ↔ süreç adımı Değer Atama `valueType` (**ValueAssignType**: değer kaynağı) aynı ada sahip; ayrı enum'lardır, yeniden
  adlandırma (opsiyonel). _(models/enums/index.md Notlar · additional-qualification · process-step §3.4)_
- [ ] **Çeviri `definition` ↔ `defaultLang` tutarlılığı** — organizasyon `defaultLang`'ini sonradan değiştirirse eski
  `definition` metinleri **yanlış dilde** kalır; veri-giriş kuralı ile garanti edilmeli. (Yukarıdaki "ezmiş kayıt teyidi"nden ayrı.)
  _(new-vs-current §13/§14 · translation §5)_
- [ ] **Örnekler arası aksiyon kodu adlandırma tutarlılığı** — sampleProcess örneklerinde kod adları (`default` vb.) tutarlı
  tutulmalı (doc-hygiene). _(sampleProcess)_
- [ ] **Aksiyonlarda swipe item** — process-step-action'lar için görünüm (`styleId`/`actionDisplayType`) yerine ya da ek olarak
  **swipe item** (kaydırmalı aksiyon) eklenmeli mi? _(process-step-action §4 · action §3 `actionDisplayType`)_

---

## 🆕 Bu oturumda eklenen açık sorular

- [ ] **`dataSource` alan adı çift anlamlı** — Combobox/Radiobutton'da dinamik veri kaynağı (§2.4), Image Area
  Selector'da statik nokta listesi (`code`·`x`·`y`·`isSelected`, §3.19). Ayrıştırılsın/yeniden adlandırılsın mı?
  _(properties §4)_
- [ ] **Customer API dış referans anahtarı** — API'de kiracı `organizationId` (int) mi, `organizationCode` (string) mi
  ile belirtilmeli? (organization §2 dış referanslarda `code` diyor.) _(flovo-customer-api §3)_
- [ ] **`apiKeyId` içeriği/adı (Customer API kimliği)** — Customer API ile oluşturulan kayıtlarda oluşturan **User**
  olmadığından işlemi kimin yaptığını kaydetmek için `apiKeyId` alanları var (`ProcessInstance.createdByApiKeyId`,
  `ProcessStepInstance.atApiKeyId`). **Ad geçici**; içine gelecek veri Customer API **erişim mekanizması** kesinleşince
  doğrulanacak. _(flovo-customer-api §3 · models/processInstances/process-instance.md · process-step-instance.md)_
- [x] **Alt Süreç Başlangıcı adım türü — ÇÖZÜLDÜ** (eski "Webhook/Triggered" açık sorusu): Bağımsız alt süreçlerin **giriş
  düğümü** için yeni **Alt Süreç Başlangıcı** adım türü eklendi (process-step §3.20). Webhook **ve** Süreç Adımı Tetikleme
  ile tetiklenir; webhook'u tutan aksiyon bu adıma bağlı **`default`**'a dönüşür; Alt Süreç Başlangıcı bir süreç adımı
  olduğundan `ProcessStepInstance.processStepId` doğru atılır. Ana süreç içi API ilerlemesi için **Webhook aksiyonu**
  (process-step-action §3.6) kullanımı korunur. _(process-step §3.20/§4 · sampleProcess/createPdfAsync ·
  models/processInstances/process-step-instance.md)_
- [x] **Alt süreç yürütmesinin runtime temsili — ÇÖZÜLDÜ:** Bağımsız alt süreç tetiklenince **ayrı, yeni bir `ProcessInstance`** oluşur;
  **`ProcessInstance.parentProcessInstanceId`** = tetikleyen ana sürecin `ProcessInstance` id'si (ana süreçlerde null). _(process-step §3.20/§4 ·
  models/processInstances/process-instance.md · process-step-instance.md · index.md)_
- [ ] **Grup onayı: `groupApproval` (adım) ↔ `groupApprovalRequired` (UserGroup) ilişkisi** — eşik (**hepsi/biri**) adım-düzeyi
  `groupApproval`'da (process-step §3.16), "grup onayı gerekli mi" ise `UserGroup.groupApprovalRequired` (bool) alanında. İki alanın
  yakın adı + kapsam örtüşmesi netleştirilmeli (eşiğin ve gerekliliğin tek sahibi kim; opsiyon seti hepsi/biri). _(process-step §3.16 ·
  models/organization-settings/user-group.md · models/processInstances/user-group-approved-user.md)_
  - **Netleşen:** adım-düzeyi `groupApproval` **bool** kalır — `true`: aksiyon alabilen **tüm** kullanıcılar onaylayınca ilerler,
    `false`: **bir** kişinin onayı yeterli. Açık kalan: `UserGroup.groupApprovalRequired` ile sahiplik/örtüşme.
    _([`research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](./research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §3)_
- [ ] **Form validasyon durumu — `Instance.validated` (bool) mü, `FormValidation` tablosu mu?** İş akışından validasyonları **sürekli
  tekrar yapmamak** ve **iş kuralı** (BusinessRule `applyValidation`) ile oluşturulan validasyonlarla **tutarsızlık yaşamamak** için:
  `Instance` modeline **`validated` (bool)** alanı mı eklenmeli, yoksa ayrı bir **`FormValidation`** tablosu mu oluşturulmalı? Karar
  sonraya. _(models/processInstances/instance.md · business-rule.md `applyValidation` · flovo-bpm-engine.md)_
- [x] **Solution & Service modellendi** — hiyerarşi `Organization → Solution → Service` netleşti; `models/service-settings/solution.md`
  ve `models/service-settings/service.md` oluşturuldu. Alan ayrıntıları (ikon/versiyon/yetki vb.) daha sonra detaylandırılacak.

### 🔎 Tutarlılık denetiminden (2026-07-02)
- [ ] **`skipWithThisActionId` referansı** — atlamayı tetikleyen aksiyon: action `code` mi, `ProcessStepAction` mı,
  Action şablonu mu? (Action'a **canlı FK yok** ilkesiyle uyumlu olmalı; şu an models'ta belirsiz.) _(process-step §2)_
- [x] **Bildirim dil kapsamı — ÇÖZÜLDÜ (dinamik dil listesi):** bildirim başlık/mesajı sabit TR/EN alan çiftleri yerine
  **dinamik `{ languageCode, text }` listesi**ne dönüştürüldü; sabit dil setine (tr/en/de) bağlı kalmadan kayıt-başına-dil
  genişler. _(process-step §3.6 · [`research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](./research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §4)_
- [ ] **`ProcessStep`/`BusinessRule` denormalize `organizationId`** — asıl kapsayıcı `serviceId`; kiracı için ayrıca
  `organizationId` tutulsun mu, yoksa `service → solution → org` üzerinden mi? _(models)_

### 🔧 v0.12 — Adım tipe-özel ayar modellemesinden (2026-07-16)
- [ ] **Flovo AI adım ayarları detayı** — `selectedAi` kanonik AI seti; `fileSourceType` (thumbnail/fileProperty) ayrı enum mü;
  AI'a-özel `aiSettings` şeması. _(process-step §3.2)_
- [ ] **Adım `settings` JSONB doğrulama & referans bütünlüğü** — tip-başına **JSON Schema**; `settings` içindeki referans id'lerin
  (`propertyId`/`organizationUserGroupId`/`selectedTimerProcessStepId`…) **uygulama-katmanı** doğrulaması + **silme koruması**. _(process-step §2)_
- [ ] **`triggerProcessStep` / `formRedirect` adım ayarları** — henüz modellenmedi (ayarsız grup §3.16). _(process-step §3.16)_
- [ ] **`DynamicParameter.value` şekli** — değer-kaynağı (**ValueAssignType**: sabit/hesaplama/form property) + değerin JSONB
  temsili (iş-kuralı `AssignValueToFieldDto` muadili). _(process-step §3.1/§3.6)_

### 🔎 v0.15 — Proje incelemesinden (2026-07-24)
- [ ] **Süreç başlatma kısıtı (`ProcessStepProcessStartSettings.userGroupId`) — davranış tarafı incelenecek.** Modelde
  başlatmayı **hangi kullanıcı grubunun** yapabileceği tanımlı (`userGroupId`: **null** → herkes, **dolu** → yalnız o grup →
  `models/service-settings/process-step.md` §3.14); ancak **davranış** dokümanı Süreç Başlangıcı'nı (§3.1) yalnız *nasıl*
  tetiklendiği (manuel/webhook) üzerinden anlatıyor, **kim başlatabilir** kısıtından söz etmiyor. Kısıtın kapsamı gözden
  geçirilip (grup dışı kullanıcı başlangıç aksiyonlarını **görür mü**, yalnız tetikleyemez mi? webhook/Customer API
  tetiklemesinde grup kısıtı nasıl uygulanır?) sonuç **davranış §3.1'e** yazılacak. _(process-step §3.1 · models §3.14)_
- [ ] **`Instance.delete` alan adı ↔ `deleted` tutarsızlığı — tek isme sabitlenecek (kontrol bekliyor).** Runtime
  `Instance` modelinde soft-delete alanı **`delete`** adında (`models/processInstances/instance.md` alan tablosu + "`delete`
  alanı içeren tüm modeller" notu); fakat onu **set eden/anan her yer `deleted`** diyor: Instance Deleter adımı
  (`models/service-settings/process-step.md` §3.15 `deleted = true`), **InstanceDeleteMode** ve **ProcessStepType** enum'ları,
  ayar logu tasarımı, hatta `sampleProcess/expense` ("`deleted` durumuna çekilir"). Ayrıca **tüm organizasyon-ayar
  modelleri** soft-delete için **`deleted`** kullanıyor (`delete` kullanan başka model yok). **Detay/karar:** kanonik isim
  **`deleted`** olmalı (hem tutarlılık hem `delete`'in SQL'de ayrılmış sözcük olması nedeniyle); değişiklik `instance.md`
  alan adı + "`delete` alanı içeren tüm modeller" notunu kapsar. **Kontrol:** başka `delete` (soft-delete) kullanan yer
  kalmadığı doğrulanıp tek seferde `deleted`'e çevrilecek. _(models/processInstances/instance.md · process-step §3.15 ·
  enums/instance-delete-mode.md · enums/process-step-type.md · research/settings-log)_

---

## ✅ Bu oturumda çözülen tutarsızlıklar (log)

- **Kimlik tipi:** `organizationId` her yerde **int** (eski app'teki `accountId` = yeni `organizationCode`'a denk).
  `string` tipler int'e çevrildi.
- **Style ↔ alan:** Form alanları `style.md` Style varlığını **kullanmaz**; iş kuralı `setStyle` yalnız tekil görünüm
  niteliğini (fontSize/titleColor) değiştirir. Style tüketicileri = aksiyon + durum.
- **Değer Atama:** `valueType`'a `fromCalculation` (+ `expression`) eklendi (özetteki "hesaplayarak" ile hizalandı).
- **Processing:** frontende form/response döner ama beklemez → `default` ile otomatik ilerler (yeniden sınıflandırıldı).
- **View-profile + diğer modeller:** eksik primary/secondary key'ler eklendi (`id`, `serviceId`, `processStepId`);
  alan-referansları `...Id` (FK) yapıldı (`processViewProfileId`, `organizationUserGroupIds`, `styleId`).
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
  (propertyType'a göre dictionary). Form List ayarları Property'den profile taşındı: `addNewEnabled`→`activeStartActions`
  (ProcessStepAction id listesi), `addFromExistingRecordsIsActive`→`addFromExistingStatusIds` (Status id listesi). Ayrıca
  `selectedEnable`→`selectableVisible` olarak **profil-bazına** (Form List, `ProcessViewProfilePropertySetting`) taşındı.
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
