# Flovo BPM — Faz 2 (MVP-sonrası) Açık Konular / TODO

> **Kapsam:** MVP geliştirmesi **tamamlandıktan sonra** detaylandırılıp eklenecek özellikler. v0.47'de [`todo.md`](./todo.md)'den buraya taşındı;
> MVP kapsamı `todo.md`'de kalır ve oradaki "⏭️ Faz 2'ye taşınanlar" bölümü bu dosyaya işaretçi verir.
> **Kural:** `todo.md` ile aynı — açık sorular yalnız bu iki dosyada tutulur; tasarım dokümanları işaretçi verir. Her madde kaynağını
> `(<doküman> §..)` ile belirtir; çözülünce `[x]`. Bir konu **MVP'ye geri çekilirse** maddesi `todo.md`'ye taşınır (tek yerde tutulur).
> **"Faz" adlandırması — dikkat:** Buradaki Faz 2 = **MVP-sonrası özellik genişletmesi**. Motor geliştirme planındaki
> ([`../bpm-engine-build-plan.md`](../bpm-engine-build-plan.md)) **F1** (motor çalışır) / **F2** (frontend entegrasyonu) görev fazları **MVP'nin içindedir**;
> oradaki **F1.C.2 · F1.C.3 · F1.D.2 · F1.D.3 · F2.I.2 · F2.I.3** görevleri bu listeye bağlı olarak ⏭️ MVP-sonrası işaretlendi (F1.E.1 `ApiKey` yalnız iskelet).
> **Kural (v0.47):** Bu konulardaki mevcut model/doküman iskeletleri (ör. `service-trigger.md`, `scheduler-job.md`, Timer ayar modeli) **korunur**; MVP'de
> yalnız ayrıntılandırılmaz. MVP tasarımı bunlara **bağımlılık yaratmamalıdır**.

---
## 1. Yetkilendirme kapsamının detaylandırılması
- [ ] **Yetkilendirme (permissions) — açık kalanlar:** **(a)** `ProcessStepAction.authorizationLevel` (aksiyon-düzeyi sayısal
  yetki) yeni **org-bazlı** yetki modeliyle nasıl uyumlanır; **(b)** **impersonation** kapsamı/denetimi (kimin yerine
  geçilebilir; log/audit); **(c)** yetki setinin **genişletilebilirliği** (yeni yetki = Organization'a yeni `*UserGroupId`
  alanı mı, dinamik mi?); **(d)** admin-only yetki yapılandırması ↔ `OrganizationSettings` grubu erişim sınırı.
  _(permissions §5 · organization §5 · new-vs-current §14)_

## 2. Vekalet sistemi — `UserDelegate`
- [ ] **Vekalet (proxy / yetki verme) sistemi** — **görev-devri yerine** kalıcı vekalet: kullanıcılar başka kişilere vekalet verir;
  **vekil, vekaleti veren kişinin yerine geçerek onun adına işlem yapar** (aksiyon alabilenler kümesi atananın **aktif vekilleriyle**
  genişler). **Ayrıntı sonra** verilecek — model (**`UserDelegate`**: grantor/grantee/süre/kapsam — model adı **karar v0.47**) + kapsam (tüm servis ↔ servis-bazlı) +
  iz/log ("X adına Y") + grup görevlerini kapsama + zincir/tek-kademe kararları açık. _(process-step §3.15/§3.16 · instance-awaiting-user.md)_

## 3. Loglama — denetim izi · ayar-değişiklik logu · sistem logları
- [ ] **Denetim izi (audit) / loglama + dosya/binary depolama performansı** — **loglar nasıl ve nerede tutulacak**
  (workflow/form logları · **ayar değişiklik** logları · sistem logları); organizasyonlar **kendi loglarına** nasıl erişecek
  (izolasyon/yetki); saklama/pruning; mevcut "yavaş belge yükleme" şikâyetiyle doğrudan bağlı; KVKK. _(flovo-bpm-engine §8 / §12)_
  - 🧱 **Tech-stack (kısmen):** **dosya/binary depolama → MinIO** (URL-in-JSONB; "yavaş belge yükleme" çözülür) karara bağlandı;
    **loglama modeli** (nerede/erişim/pruning) hâlâ açık. → [`./tech-stack/minio.md`](./tech-stack/minio.md)
  - 📋 **Ayar değişiklik logu — tasarım planı hazır (v0.14), karar bekliyor:** sayfa bazlı denetim izi; tek generic tablo +
    JSONB delta + uygulama katmanı + append-only (`SettingsLog` · `SettingsLogBatch` · `SettingsLogBatchPage`); erişim/yetki
    mevcut `organizationSettings`/`serviceSettings` ikiliği + RLS ile çözülüyor. → [`./research/settings-log/index.md`](./research/settings-log/index.md)
    - **Ön koşul:** Customer API'de **ayar yazma / toplu senkron ucu yok** (bugün yalnız `GET /users/{userId}` · `GET /me`) —
      toplu güncelleme loglanmadan önce bu uç tasarlanmalı. _(flovo-customer-api §1)_
    - **Açık:** **saklama süresi / KVKK** (log kişisel veri + ham istek gövdesi içerir; "denetim kaydı silinmez" ↔ silme hakkı — **hukuki karar**) ·
      `requestBody` satır-içi ↔ MinIO **eşiği** · **`HttpMethod` enum'una `patch`** eklenmesi (Customer API zaten `PATCH` kullanıyor).
    - **Bölünmeli:** bu madde **üç** log sınıfını birlikte soruyor (workflow/form · **ayar** · sistem); üçü farklı doğada —
      ayar sınıfı bu planla kapanacak, **sistem logları** (Loki/OTel) için henüz **hiçbir karar yok**.
  - **Not:** Aynı maddedeki **dosya/binary depolama → MinIO** kararı **geçerli ve MVP'de** (→ `tech-stack/minio.md`); Faz 2'ye bırakılan yalnız **loglama** sınıflarıdır (workflow/form · ayar · sistem).

## 4. Toplu senkron ucu (organizasyon referans verisi)
- [ ] **Toplu senkron ucu** — organizasyon referans verisinin (kullanıcı/departman/pozisyon/şirket vb.) dış sistemden **toplu upsert**'i için Settings API ucu.
  **Ön koşul:** Customer API'de bugün **ayar yazma ucu yok** (yalnız `GET /users/{userId}` · `GET /me`); toplu güncelleme **loglanmadan** (→ §3 SettingsLog)
  önce bu uç tasarlanmalı. Ayrıca idempotency, kısmi hata sözleşmesi ve yetki granülaritesi Settings API ortak sözleşmeleriyle birlikte. _(settings-api §5–§9 · flovo-customer-api §1)_

## 5. `SchedulerJob` altyapı modeli
- [ ] **`SchedulerJob` altyapı modeli (erteleme)** — `...At` (`lastRunAt`/`createdAt`) ↔ `...Time` (`startTime`/`endTime`)
  **adlandırma birliği** + `category`/`status`/`triggeredBy` serbest-string alanlarının enum'a çekilip çekilmeyeceği +
  alan detayları. Altyapı-zamanlayıcı modeli olduğundan **sonraya** bırakıldı. _(models/organization-settings/scheduler-job.md)_
  - Motor planı görevi **F1.C.2** (`SchedulerJob` modelini tamamla) ⏭️ MVP-sonrası işaretlendi. _(../bpm-engine-build-plan.md §3 Grup C)_

## 6. Form List red-akışı bayrakları
- [ ] **Form List red-akışı bayrakları** — eski `isRejectReasonRequired` (red gerekçesi zorunlu) + `isReapprovalLockedAfterReject`
  (reddedilen satır yeniden onaya kapalı) yeni tasarımın settings/profil-bazlı katmanına **yerleştirilmedi** — karar gerek.
  _(jsonTemplateModels/property-settings/form-list.md)_

## 7. Flovo AI adımı ayarları
- [ ] **Flovo AI adım ayarları detayı** — `selectedAi` kanonik AI seti; `fileSourceType` (thumbnail/fileProperty) ayrı enum mü;
  AI'a-özel `aiSettings` şeması. _(process-step §3.2)_
  - Process-step `settings` şeması tarafı (v0.38): `selectedAi` kanonik set · `fileSourceType` enum · `aiSettings` per-AI şema. _(process-step-settings/flovo-ai.md)_

## 8. `triggerProcessStep` (Süreç Adımı Tetikleme) · `formRedirect` (Form Yönlendirme) süreç adımları
- [ ] **`triggerProcessStep` / `formRedirect` adım ayarları** — henüz modellenmedi (ayarsız grup §3.16). _(process-step §3.16)_
  - Process-step `settings` şeması tarafı (v0.38): `triggerProcessStep` / `formRedirect` **`settings` şeması** hâlâ modellenmedi (aday kavramlar şema-dışı işaretli).
    _(process-step-settings/trigger-process-step.md · form-redirect.md · process-step §3.16)_
  - Form yaşam döngüsü tarafı (v0.12): **Form Yönlendirme / Süreç Adımı Tetikleme** davranışı açık. _(process-step §3.15/§3.16 · §4)_
  - Motor planı görevleri **F1.D.2** (`triggerProcessStep` settings + yürütme) · **F1.D.3** (`formRedirect`) ⏭️ MVP-sonrası işaretlendi. _(../bpm-engine-build-plan.md §3 Grup D)_

## 9. Timer süreç adımı üçlüsü (Timer / Timer Start / Timer End)
- [ ] **Timer üçlüsü** (Timer / Timer Start / Timer End) yaşam döngüsü ve bağlanması; global timer kayıtları?
  _(process-step §4)_
  - **Netleşen (v0.12):** `TimerCalculationType` + `ProcessStepTimerSettings` (çalışma/normal/sabit takvim blokları + timeout
    bildirimi) modellendi; **yaşam döngüsü/bağlanma** (`selectedTimerProcessStepId`, global timer kayıtları) hâlâ açık. _(process-step §3.7)_

## 10. ServiceTrigger — kalan kenar durumlar
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
  - **Açık kalan:** **(1) `timer` DST kenar durumları** — cron değerlendirmesinde DST geçişleri (saat dilimi **ayrı açık konu değil** —
    v0.33: Organization'a org-bazlı timezone alanı **planlanmıyor**; cron sabit/varsayılan konvansiyona göre değerlendirilir); **(2) döngü koruması** — A→B→A tetikleme recursion'ı (derinlik/çevrim sınırı) _(tasarım-zamanı önleme
    örneği: `isAssociatedCombobox=false` geri-referans — `sampleProcess/expenseAndCreditCard/creditCardStatementLine.md`; motor-düzeyi
    güvenlik ağı açık)_; **(3) `async` kaskad kompozisyonu** — üst üste `async=false` senkron derinlik yaratır; seviyeler boyunca
    async + işlem/derinlik sınırı (Senaryo 5 kaskadı); **(4) `triggerProcessStep` → ilişkili instance (associatedInstance) tetikleme** —
    Süreç Adımı Tetikleme adımı, ilişkili instanceların **alt sürecini/aksiyonunu** tetikleyebilir; hangi associatedInstance'ların
    seçileceği (ilişki alanı/yön) + ayar detayları **tanımlanacak** (process-step §3.5/§3.20). _(Not: "alt sürecin mevcut-instance
    mekaniği" → **ÇÖZÜLDÜ v0.25**: yeni alt-`ProcessInstance`, `parentProcessInstanceId`=hedef instance'ın anası; `ProcessInstance`'a `instance` alanı eklenmez.)_
  - Motor planı görevi **F1.C.3** (trigger döngü koruması · `async` kaskad sınırı · timer DST) ⏭️ MVP-sonrası işaretlendi. _(../bpm-engine-build-plan.md §3 Grup C)_

## 11. View profile / Form List tik değişim olayları
- [ ] **Form List tik (seçim) davranışı** — formların yanındaki **tiklerde** yapılan değişiklikler **aksiyon tetikleyecek mi**?
  **Tik kaldırma nedeni** kullanıcıdan nasıl alınacak ve nasıl kaydedilecek? _(properties §3.13 Form List · `selectableVisible`/
  `selectedEditable` · view-profile §5)_
  - **Yürütme notu (v0.47):** Tik değişim olayları **ServiceTrigger ile birlikte** ele alınacak (→ §10) — tik ekleme/kaldırma, `AssociatedInstance` yazımı üzerinden `whenAddedAssociate`/`whenRemoveAssociate` tetikleyicileriyle aynı olay yoluna oturur.

## 12. Servis template & JSON ile servis oluşturma
- [ ] **Servis template & JSON ile servis oluşturma** — servisler **template** olarak nasıl oluşturulacak; template ile servis
  üretimi nasıl olacak; **n8n gibi JSON template** export/import ile mi; **ilişkili servisler toplu** mı oluşturulacak?
  _(models/service-settings/service.md · solution.md · research/n8n)_

## 13. Customer API (custom code için dış API)
- [ ] **Customer API** — kimlik/yetki (token kapsam/süre/yenileme); webhook güvenliği (secret/imza) + **idempotency**;
  `POST /instances/search` sorgu dili; rate limit/sayfalama/hata sözleşmesi; request/response şemaları. _(flovo-customer-api §3)_
  - **Dış referans anahtarı — statü çelişkisi (O6):** `flovo-customer-api.md` header'da `organizationId` kullanıp konuyu **açık**
    sayıyor; `organization.md`/`models/index.md` ise **`organizationCode` (string) kararlaştırıldı** diyor. **Customer API detaylanınca
    tek statüye** bağlanacak (o zamana dek atlandı).
  - 🧱 **Tech-stack (kısmen):** kimlik = **Keycloak** (token) · sözleşme/şema = **OpenAPI** (api-contract) · idempotency deseni =
    **NATS**; API'nin kendi tasarımı (search sorgu dili, rate limit, webhook imza) açık. → [`./tech-stack/keycloak.md`](./tech-stack/keycloak.md) · [`./tech-stack/api-contract.md`](./tech-stack/api-contract.md)
- [ ] **`apiKeyId` içeriği/adı (Customer API kimliği)** — Customer API ile oluşturulan kayıtlarda oluşturan **User**
  olmadığından işlemi kimin yaptığını kaydetmek için `apiKeyId` alanları var (`ProcessInstance.createdByApiKeyId`,
  `ProcessStepInstance.atApiKeyId`). **Ad geçici**; içine gelecek veri Customer API **erişim mekanizması** kesinleşince
  doğrulanacak. _(flovo-customer-api §3 · models/processInstances/process-instance.md · process-step-instance.md)_
  - **Bağlantılar:** toplu senkron ucu (§4) bu API'nin yazma yüzeyine bağlı · `ApiKey` modeli MVP'de yalnız **iskelet** (3 FK'yi bağlar; motor planı F1.E.1),
    detay burada · motor planı **F2.I.2** (request/response şemaları) ve **F2.I.3** (search sorgu dili hizalama) ⏭️ işaretlendi ·
    doküman [`flovo-customer-api.md`](./architectures/api/flovo-customer-api.md) (🟡 TASLAK) MVP-sonrası olarak işaretlendi.
  - **MVP'de kalan (Customer API değildir):** frontend'in kullandığı **motor runtime uçları** — `POST /instances/{id}/actions/{code}` (F1.E.3) · `GET /instances/{id}` (F2.G.2) ·
    servis instance listesi (F2.G.3) · iş kuralı instance-fetch ucu (`business-rule-endpoints.md`).
  - **Açık (kapsam, v0.47):** Webhook aksiyonunun **dış tetikleme ucu** (`process-step-action` §3.6; örnek `sampleProcess/createPdfAsync`) Customer API yüzeyinde
    tanımlı. MVP'de dış sistemden tetikleme gerekiyorsa **minimal bir iç uç** mu kalır, yoksa webhook tetikleme de bütünüyle Faz 2'ye mi kayar? → kullanıcı kararı.

---

*Oluşturma: 2026-09-08 (v0.47) — `todo.md`'den taşındı. Güncelleme: §13 Customer API (aynı gün, ikinci karar).*
