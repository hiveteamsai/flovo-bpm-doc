# Flovo BPM — Açık Sorular / TODO (önceliklendirilmiş)

> Tüm tasarım dokümanlarındaki **açık kararlar/sorular** burada tek yerde ve **önceliklendirilmiş** toplanır.
> Kaynak dokümandaki madde çözüldükçe hem orada hem burada `[x]` işaretlenir.
>
> **Öncelik mantığı:** Tier 0 = bir kararla **birçok dokümanı** kapatan çapraz-kesen konular · Tier 1 = motor
> çekirdeği (mimari) · Tier 2 = özellik netleştirmeleri · Tier 3 = detay/sonraya.

---

## ⭐ Tier 0 — Çapraz-kesen kararlar (önce bunlar; bir karar → çok doküman)

- [x] **Kapsam kararı — servis-bazlı mı, paylaşımlı mı?** **ÇÖZÜLDÜ** (hiyerarşi ile): **organizasyon havuzu** =
  Translation / Style / Status / Action (organizasyona bağlı, tüm servislerde kullanılır); **servis-bazlı** =
  Property / ProcessViewProfile / ProcessStep / WorkRule. _(action §3 · status §4 · work-rule §6 · view-profile §5)_
- [ ] **Genişletilebilirlik — sabit set mi, plugin/SDK ile eklenebilir mi?** Adım / aksiyon / alan setleri.
  _(process-step §4 · process-step-action §7 · properties §4)_
- [ ] **İki-katman sınırı** — **değer atama & karşılaştırma** hem süreç adımı hem iş kuralı olarak var. Sınır:
  iş kuralı = anlık form UX (frontend), adım = kalıcı/akış kararı (motor). Netleşince #Tier1 veri/motor ve
  tutarlılık kalemleri de oturur. _(flovo-bpm-engine §1.4/§12 · work-rule §6 · process-step §3.4/§3.13)_
  - **Not:** İş kuralı (`work-rule.md`) motordan bağımsız frontend'de çalıştığı için **en son** şekillenecek.

---

## 🏗️ Tier 1 — Motor çekirdeği (mimari)

- [ ] **Çalışma-zamanı mimarisi** — tek-süreç mi, kuyruk-tabanlı dağıtık worker mı? Orkestrasyon ↔ yürütme ayrımı;
  durum DB'de, kuyruk yalnız iş ID'leri, worker'lar durumsuz. _(flovo-bpm-engine §2.2 / §12)_
- [ ] **Bulut + on-prem hibrit** dağıtım; on-prem ↔ merkezi kimlik/sosyal çelişkisi. _(flovo-bpm-engine §2.2 / §12)_
- [ ] **Veri modeli** — token-tabanlı (klasik BPMN) mı, koleksiyon-tabanlı (n8n) mı? Adımlar arası veri temsili/akışı,
  soy ağacı (lineage). _(flovo-bpm-engine §3 / §12)_
- [ ] **Kalıcılık & durum** — ne saklanır (süreç tanımı · instance/state · veri · dosya/binary); durum yaşam döngüsü
  (new/running/waiting/done); saklama/pruning. _(flovo-bpm-engine §8)_
- [ ] **Property value (form alan değerleri) depolaması** — `Form`'un alan değerleri **nerede/nasıl** tutulacak: `Form`
  modelinde mi, ayrı value tablo(lar)ında mı; tip-bazlı sütun mu, referans mı? Daha detaylı araştırma sonrası
  kararlaştırılacak; alan-düzeyi tanımlar ayrı **değer dokümantasyonunda** yapılacak.
  _(form-value-scenarios §12 · models/workFlows/form.md)_
- [ ] **Denetim izi (audit) + dosya/binary depolama performansı** — mevcut "yavaş belge yükleme" şikâyetiyle doğrudan
  bağlı; KVKK. _(flovo-bpm-engine §8 / §12)_
- [ ] **Güvenlik** — expression/kod değerlendirme **sandbox**'ı (sert sınır), credential şifreleme/paylaşım,
  riskli adımlar. _(flovo-bpm-engine §10 · process-step-action §5)_
- [ ] **Paralel dallanma / eşzamanlı kollar & join** var mı? Bir adım aynı anda birden çok sonraki adımı tetikler mi?
  Alt servisler (Form List) ana süreçle eşzamanlı mı yürür? _(flovo-bpm-engine §4.5)_
- [ ] **Olay/mesaj-tabanlı tetikleme** ve uyuyan sürecin uyandırılması; çok-örneklilikte "en-fazla-bir-kez"/lider
  seçimi. _(flovo-bpm-engine §5 / §6 / §12)_

---

## 🔧 Tier 2 — Özellik netleştirmeleri

- [ ] **AI entegrasyon modeli** — deterministik "AI adımı" vs otonom "ajan"; takılabilir strateji (model/memory/araç);
  "herhangi bir adım = araç" + MCP? _(flovo-bpm-engine §11)_
- [ ] **Hata yönetimi** — her adımda `onFail` var mı/zorunlu mu; **retry** (deneme + bekleme); süreç-seviye global
  hata yakalayıcı; telafi/compensation; `action` zinciri **sonsuz döngü** koruması. _(flovo-bpm-engine §7 · process-step-action §7)_
- [ ] **İnsan-görev ailesi ortak modeli** — Kullanıcı / Kullanıcı Grubu / Processing için atama + bekleme.
  _(process-step §4)_ · _(Processing'in ilerleme farkı **çözüldü**: frontende response döner ama beklemez, `default` ile ilerler → process-step §3.18)_
- [ ] **Form List / alt-servis yaşam döngüsü** — 3 dokümanda ortak: alt-servisin görüntülenecek alanları/seçilebilirliği
  view-profile ile nasıl; veri/`changeList`/parametre nasıl akar. _(properties §3.13 · process-step §4 · view-profile §5)_
- [x] **Alan-özel görünüm ayarlarının profil bazında yönetimi** — **KARAR (B2):** `ProcessViewProfilePropertySetting
  {viewProfilePropertyId, key, value}` (propertyType'a göre **dictionary**; katalog → `models/service-settings/view-profile-property.md`).
  Form List: `addNewEnabled`→**`activeStartActions`** (ProcessStepAction id listesi), `addFromExistingRecordsIsActive`→
  **`addFromExistingStatusIds`** (Status id listesi) profil'e taşındı; `selectedEnable`→**`selectableModeActive`** (alan-düzeyi, `Property`).
  **Kalan:** `reOrder`/`editOnlyOwnPosition`/`selectedEditable` de profil-bazlı mı? _(view-profile §5 · properties §4)_
- [ ] **Form List ayarları gözden geçir** — `reOrder` · `parameterTransfer` · `propertyTransferParameters` ·
  `editOnlyOwnPosition` nasıl yönetilecek (profil-bazlı mı)? _(properties §4 / §3.13)_ · _(`addNewEnabled`→`activeStartActions`,
  `addFromExistingRecordsIsActive`→`addFromExistingStatusIds` (profil), `selectedEnable`→`selectableModeActive` (alan): **çözüldü**.)_
- [ ] **Combobox/Radiobutton seçenek kaynağı** — statik (`propertyItems`) ↔ dinamik (`dataSource`) modeli ve iş kuralı
  `FillDataSource` ile ilişkisi; `FillDataSource` kaynak tipleri (Organization/User/API). _(properties §4 · work-rule §6)_
- [ ] **Timer üçlüsü** (Timer / Timer Start / Timer End) yaşam döngüsü ve bağlanması; global timer kayıtları?
  _(process-step §4)_
- [ ] **Süreç Bitişi "önceki adıma taşıma"** — yeniden-açma (re-open) mı, ayrı akış mı? Denetim izine etkisi.
  _(process-step §4)_
- [ ] **Form yaşam döngüsü** — Form Creator / Form Silme / Form Yönlendirme / Süreç Adımı Tetikleme; Parent Property
  ile birlikte. _(process-step §4)_
- [ ] **`default action` kavramı** — her adımda mı, yoksa yalnız HTTP Request(async)/Timer gibi adımlarda mı?
  _(process-step §4)_
- [ ] **Raporlama** ayrı özellik olarak nasıl modellenecek? _(view-profile §3 / §5)_
- [ ] **`ChangeViewProfile`** çalışma-zamanı profil değişiminin akış (motor) ile etkileşimi. _(view-profile §5)_
- [ ] **Customer API** — kimlik/yetki (token kapsam/süre/yenileme); webhook güvenliği (secret/imza) + **idempotency**;
  `POST /forms/search` sorgu dili; rate limit/sayfalama/hata sözleşmesi; request/response şemaları. _(flovo-customer-api §3)_

---

## 🧩 Tier 3 — Detay / sonraya

- [ ] **`defaultAction` (bool) ↔ `default` (kod)** — ikisi de "varsayılan"ı işaret ediyor; nasıl birleşir?
  _(action §3 · process-step-action §7)_
- [x] **ActionDto: kopya ↔ canlı referans** — **ÇÖZÜLDÜ:** adıma eklenince alanlar **bir kez kopyalanır**, kopya **bağımsızdır**; Action değişince mevcut adım-aksiyonları güncellenmez (FK/canlı bağ yok). _(action §3)_
- [ ] **`actionDisplayType`** gözden geçir (`invisible`/`everywhere`/`onlyFormDetail`/`onlyFastApprove`). _(action §3)_
- [ ] **`withForm` formu** — serbest pop-up mu, formun bir görüntüleme profili mi? _(process-step-action §7)_
- [ ] **`changeList` öğe yapısı** (alan id + yeni değer + tip?) ve **`action` nesnesinin şekli**. _(process-step-action §7)_
- [ ] **`AssignValueToPropertyAttribute`** adı teyit. _(work-rule §6)_
- [ ] **İş kuralı performansı** — `always` kuralları yalnız ilgili property değişince (alan-bağımlı) tetiklensin mi?
  _(work-rule §6)_
- [ ] **Status: kategori/grup** — raporlama/filtreleme için `code`/`definition` yeterli mi, ayrı kategori boyutu gerekli mi?
  _(status §4)_ · _(icon/definition rengi = `styleId`.`fontColor` — **çözüldü**.)_
- [ ] **Style kapsamı** — yalnız bg+font mı, daha fazlası mı (fontSize/isBold/border/iconColor)? Tema/dark mode; bg/font
  **kontrast** kontrolü. _(style §4)_
- [ ] **Çeviri** — ortak (`null`) kayıt sonradan güncellenince, onu **ezmiş** organizasyon kayıtları etkilenmemeli (teyit).
  _(translation §5)_
- [ ] **`idleTimeoutMinute`** alt/üst sınır; oturum kilitlenince davranış (yeniden giriş mi, yalnız parola mı)?
  Organization sonraki alanlar: plan/abonelik, timezone, para birimi, bölge, güvenlik. _(organization §4)_

---

## 🆕 Bu oturumda eklenen açık sorular

- [ ] **`dataSource` alan adı çift anlamlı** — Combobox/Radiobutton'da dinamik veri kaynağı (§2.4), Image Area
  Selector'da statik nokta listesi (`code`·`x`·`y`·`isSelected`, §3.19). Ayrıştırılsın/yeniden adlandırılsın mı?
  _(properties §4)_
- [ ] **Customer API dış referans anahtarı** — API'de kiracı `organizationId` (int) mi, `organizationCode` (string) mi
  ile belirtilmeli? (organization §2 dış referanslarda `code` diyor.) _(flovo-customer-api §3)_
- [ ] **`apiKeyId` içeriği/adı (Customer API kimliği)** — Customer API ile oluşturulan kayıtlarda oluşturan **User**
  olmadığından işlemi kimin yaptığını kaydetmek için `apiKeyId` alanları var (`WorkFlow.createdByApiKeyId`,
  `ProcessStepExecution.atApiKeyId`). **Ad geçici**; içine gelecek veri Customer API **erişim mekanizması** kesinleşince
  doğrulanacak. _(flovo-customer-api §3 · models/workFlows/work-flow.md · process-step-execution.md)_
- [ ] **Webhook/Triggered süreç adımı türü (yeni)** — Webhook bugün bir **aksiyon** olarak modelli; ama `ProcessStepExecution`
  `processStepId` gerektirdiğinden, süreçten bağımsız **child süreçte** dışarıdan (API) tetiklenen webhook aksiyonu bir
  process-step'e bağlı olmadığı için **kayıt doğru atılamıyor**. **Öneri:** yeni adım türü (**Webhook** *veya* **Triggered** —
  biri seçilecek); API ile *aksiyon* değil **bu adım** tetiklensin; webhook'u tutan adımdaki aksiyon **`default`**'a dönüşüp bu
  yeni adıma bağlansın. **Karar sonraya.** _(process-step §4 · process-step-action §3.6 · sampleProcess/createPdfAsync ·
  models/workFlows/process-step-execution.md)_
- [ ] **Grup onayı: `groupApproval` (adım) ↔ `groupApprovalRequired` (UserGroup) ilişkisi** — eşik (**hepsi/biri**) adım-düzeyi
  `groupApproval`'da (process-step §3.16), "grup onayı gerekli mi" ise `UserGroup.groupApprovalRequired` (bool) alanında. İki alanın
  yakın adı + kapsam örtüşmesi netleştirilmeli (eşiğin ve gerekliliğin tek sahibi kim; opsiyon seti hepsi/biri). _(process-step §3.16 ·
  models/organization-settings/user-group.md · models/workFlows/user-group-approved-user.md)_
- [ ] **Form validasyon durumu — `Form.validated` (bool) mü, `FormValidation` tablosu mu?** Workflow'dan validasyonları **sürekli
  tekrar yapmamak** ve **iş kuralı** (WorkRule `ApplyValidation`) ile oluşturulan validasyonlarla **tutarsızlık yaşamamak** için:
  `Form` modeline **`validated` (bool)** alanı mı eklenmeli, yoksa ayrı bir **`FormValidation`** tablosu mu oluşturulmalı? Karar
  sonraya. _(models/workFlows/form.md · work-rule.md `ApplyValidation` · flovo-bpm-engine.md)_
- [x] **Solution & Service modellendi** — hiyerarşi `Organization → Solution → Service` netleşti; `models/service-settings/solution.md`
  ve `models/service-settings/service.md` oluşturuldu. Alan ayrıntıları (ikon/versiyon/yetki vb.) daha sonra detaylandırılacak.

### 🔎 Tutarlılık denetiminden (2026-07-02)
- [ ] **`skipWithThisActionId` referansı** — atlamayı tetikleyen aksiyon: action `code` mi, `ProcessStepAction` mı,
  Action şablonu mu? (Action'a **canlı FK yok** ilkesiyle uyumlu olmalı; şu an models'ta belirsiz.) _(process-step §2)_
- [ ] **Bildirim dil kapsamı** — bildirim başlık/mesajı bugün **TR/EN**; sabit dil seti **tr/en/de** ve kayıt-başına-dil
  ilkesiyle hizalanmalı mı (**de eksik**)? _(process-step §3.6 · flovo-bpm-engine §8)_
- [ ] **`ProcessStep`/`WorkRule` denormalize `organizationId`** — asıl kapsayıcı `serviceId`; kiracı için ayrıca
  `organizationId` tutulsun mu, yoksa `service → solution → org` üzerinden mi? _(models)_

---

## ✅ Bu oturumda çözülen tutarsızlıklar (log)

- **Kimlik tipi:** `organizationId` her yerde **int** (eski app'teki `accountId` = yeni `organizationCode`'a denk).
  `string` tipler int'e çevrildi.
- **Style ↔ alan:** Form alanları `style.md` Style varlığını **kullanmaz**; iş kuralı `SetStyle` yalnız tekil görünüm
  niteliğini (fontSize/titleColor) değiştirir. Style tüketicileri = aksiyon + durum.
- **Değer Atama:** `valueType`'a `FromCalculation` (+ `expression`) eklendi (özetteki "hesaplayarak" ile hizalandı).
- **Processing:** frontende form/response döner ama beklemez → `default` ile otomatik ilerler (yeniden sınıflandırıldı).
- **View-profile + diğer modeller:** eksik primary/secondary key'ler eklendi (`id`, `serviceId`, `processStepId`);
  alan-referansları `...Id` (FK) yapıldı (`processViewProfileId`, `organizationUserGroupIds`, `styleId`).
- **PK adı:** modelin birincil anahtarı `id` (property'de `propertyId`→`id`).
- **İnsan-tetikli aksiyonlar:** manuel/withForm'a ek Fotoğraf Çek/Dosya Seç/Barcode Tara da eklendi.
- **Yazım/casing:** `trealingView`→`trailingView`, `criteritionType`→`criterionType`, `solutionid`/`ServiceId`→`solutionId`/`serviceId`.
- **Hiyerarşi tanımlandı:** `Organization → Solution → Service → {Property · ProcessViewProfile · ProcessStep · WorkRule}`;
  `ProcessStepAction → ProcessStep`; **Action/Status/Style/Translation → Organization** (havuz). `models/` klasörü ve
  `organization-settings/action.md`·`status.md` buna göre revize edildi (Action/Status `serviceId`→`organizationId`).
- **Translation kayıt-başına-dil:** `tr`/`en`/`de` kolonları kaldırıldı → **`languageCode` + `definition`** eklendi;
  benzersizlik `(organizationId, code, languageCode)`; çözümleme `code` + `languageCode` + `organizationId` ile.
- **Action → ProcessStepAction bağımsız kopya:** `actionId` FK **kaldırıldı**; alanlar oluşturmada **bir kez** kopyalanır,
  iki taraf birbirini etkilemez (Action değişince mevcut binding'ler güncellenmez).
- **Profil-bazlı alan override'ı (B2):** `ProcessViewProfilePropertySetting {viewProfilePropertyId, key, value}` eklendi
  (propertyType'a göre dictionary). Form List ayarları Property'den profile taşındı: `addNewEnabled`→`activeStartActions`
  (ProcessStepAction id listesi), `addFromExistingRecordsIsActive`→`addFromExistingStatusIds` (Status id listesi). Ayrıca
  `selectedEnable`→`selectableModeActive` olarak **alan-düzeyine** (Form List, `Property`) taşındı.
- **Dokümanlar senkronlandı + tutarlılık denetimi:** `research/compare/new-vs-current.md` bu oturumun tüm kararlarıyla
  güncellendi; `CLAUDE.md`/`README.md` indekslerine `models/` + `todo.md` eklendi. Bağımsız denetim düzeltmeleri:
  README (style alanları), Processing taksonomisi (otomatik), `process-step-action`/`flovo-bpm-engine` `style`→`styleId`,
  `skipWithThisActionId` "FK → Action" kaldırıldı (belirsiz olarak işaretlendi), Customer API başlığı "geçici" notu.

---

*Oluşturma: 2026-07-02.*
