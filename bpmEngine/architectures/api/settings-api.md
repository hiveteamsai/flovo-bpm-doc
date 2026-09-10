# Flovo Settings API — Tasarım-Zamanı Ayar CRUD'u

> **Durum:** 🟢 Tasarım (v0.39). **Amaç:** Bir tasarımcının (Form Designer / ayar ekranı) **servisleri ve ayarlarını**
> oluşturup düzenlediği **tasarım-zamanı (design-time) yönetim API'si.** Motor **runtime**'ının değil; **konfigürasyonun** CRUD'u.
>
> **Sınır (üç API'yi karıştırma):**
> - **Bu doküman** = tasarım-zamanı **ayar** CRUD'u (service/property/step/view-profile/business-rule + org ayarları).
> - **Runtime veri** (instance oku/yaz, webhook, dosya) = dış müşteri API'si → [`flovo-customer-api.md`](./flovo-customer-api.md).
> - **İş kuralı motoru** runtime uçları + kural CRUD'u → [`service-settings/business-rule-endpoints.md`](../../service-settings/business-rule-endpoints.md) (§7 CRUD bu dokümanın deseninin özel hâli).
>
> **Sözleşme kaynağı:** [`tech-stack/api-contract.md`](../../tech-stack/api-contract.md) (Protobuf → iç gRPC + dış grpc-gateway REST + OpenAPI).
> Aşağıdaki path'ler **dış REST** yüzeyidir (FE designer tüketir); iç modüller aynı proto'dan gRPC ile çağırır.

---

## 0. Ne zaman bu API?
Tasarımcı bir süreç kurarken/düzenlerken (→ [`flovo-bpm-engine.md`](../engine-core/flovo-bpm-engine.md) §2.1 tasarım-zamanı sırası). Yazılan
her şey **konfigürasyondur** (instance/veri değil); düşük hacim, **id ile** yüklenir, **RLS** ile kiracıya izole.

## 1. Ortak sözleşme
- **Kimlik:** `Authorization: Bearer <token>` (Keycloak OIDC); token'daki **`organizationId`** claim'i ile **PostgreSQL RLS**
  (Pattern B v2) → [`tech-stack/keycloak.md`](../../tech-stack/keycloak.md). Tasarım-zamanı yazma **yetki** gerektirir (admin/designer rolü;
  yetki modeli → [`organization-settings/permissions.md`](../../organization-settings/permissions.md)).
- **Protokol:** dış REST/JSON (grpc-gateway); iç gRPC. `Content-Type: application/json` · `Accept-Language` (çok-dilli metin).
- **Kaynak adları:** `code` **dış/iş kimliği**, `id` iç PK. **`Property.code` (ve `Service.code` …) immutable** — ilk instance
  oluştuktan sonra değişmez (dış API + JSONB anahtarı kimliği; → api-contract.md · property.md §1.1). Rename yalnız `translation`'da.
- **CRUD fiilleri (REST konvansiyonu):** `GET` (liste/tekil) · `POST` (oluştur) · `PUT` (tam güncelle) · `PATCH` (kısmi) ·
  `DELETE` (sil — **soft-delete**, `deleted=true`). Liste uçları **sayfalama/filtre** alır.
- **Hata sözleşmesi:** ortak standart (kod + mesaj + alan-bazlı doğrulama hataları) → todo (ortak hata sözleşmesi).
- **Geriye uyum:** proto WIRE_JSON breaking-check (api-contract.md) — kırıcı değişiklik CI'da engellenir.

## 2. Kaynak hiyerarşisi
```
Organization ─┬─ Solution ── Service ─┬─ Property ── PropertyItem
              │                        ├─ ProcessStep ── ProcessStepAction
              │                        ├─ ProcessViewProfile ── ProcessViewProfileProperty ── …PropertySetting
              │                        ├─ BusinessRule (→ business-rule-endpoints §7)
              │                        └─ ServiceTrigger
              └─ (organizasyon ayarları) Action · Status · Style · Translation · UserGroup · Company · Department · …
```
Path'ler bu ağaca göre **iç içe** (nested) verilir; her alt-kaynak üstünün `id`/`code`'uyla kapsamlanır.

## 3. Servis-ayarı kaynakları (design-time CRUD)

### 3.1 Solution
| Method | Path | Amaç |
|---|---|---|
| GET | `/solutions` | Organizasyonun çözümlerini listele |
| GET · POST | `/solutions` · `/solutions/{id}` | Oku / oluştur / güncelle / sil |
Model → [`models/service-settings/solution.md`](../../models/service-settings/solution.md).

### 3.2 Service
| Method | Path | Amaç |
|---|---|---|
| GET | `/solutions/{solutionId}/services` | Çözümün servisleri |
| POST | `/solutions/{solutionId}/services` | Servis oluştur (`code`·`definition`·`formType`) |
| GET · PUT · PATCH · DELETE | `/services/{id}` | Servis oku/güncelle/sil |
| GET | `/services/{id}/definition` | **Servisin TAM tanımı** (property+step+action+view-profile+rule+trigger tek pakette — designer yükleme + export) |
| PUT | `/services/{id}/definition` | **Toplu güncelle** (tüm servis tanımını bir dokümanla; §6) |
Model → [`models/service-settings/service.md`](../../models/service-settings/service.md). `formType`: form/parameter/eventForm.

### 3.3 Property (+ `settings` doğrulama)
| Method | Path | Amaç |
|---|---|---|
| GET | `/services/{serviceId}/properties` | Servisin alanları |
| POST | `/services/{serviceId}/properties` | Alan oluştur — `propertyType` + çekirdek alanlar + **`settings` (JSONB)** |
| GET · PUT · PATCH · DELETE | `/properties/{id}` | Alan oku/güncelle/sil |
| GET · POST | `/properties/{id}/items` | **PropertyItem** (statik seçenek) listele/ekle |
| PUT · DELETE | `/property-items/{id}` | Öğe güncelle/sil |
- **🟩 `settings` doğrulama kapısı (KARAR):** POST/PUT'ta `settings` JSONB'si, `propertyType`'a ait **JSON Schema** ile doğrulanır
  → [`models/service-settings/jsonTemplateModels/property-settings/`](../../models/service-settings/jsonTemplateModels/property-settings/index.md)
  (`<propertyType>.md`). Uymayan yazım **reddedilir** (`additionalProperties:false`). `settings` içi referans id'ler (`dataSourceId`…)
  ve çekirdek FK'ler (`associatedServiceId`/`childServiceId`…) **uygulama-katmanı** doğrulaması (§5).
- **`code` kilidi:** ilk instance sonrası `code` değişmez (draft penceresi → property.md §1.1).

### 3.4 ProcessStep + ProcessStepAction (+ `settings` doğrulama)
| Method | Path | Amaç |
|---|---|---|
| GET | `/services/{serviceId}/process-steps` | Servisin adımları |
| POST | `/services/{serviceId}/process-steps` | Adım oluştur — `stepType` + ortak alanlar + **`settings` (JSONB)** |
| GET · PUT · PATCH · DELETE | `/process-steps/{id}` | Adım oku/güncelle/sil |
| GET · POST | `/process-steps/{id}/actions` | **ProcessStepAction** (binding) listele/ekle — `Action` şablonu kopyalanır |
| PUT · DELETE | `/process-step-actions/{id}` | Aksiyon-binding güncelle/sil (`targetProcessStepId` = graf kenarı) |
- **🟩 `settings` doğrulama kapısı:** `settings`, `stepType`'a ait **JSON Schema** ile doğrulanır
  → [`models/service-settings/jsonTemplateModels/process-step-settings/`](../../models/service-settings/jsonTemplateModels/process-step-settings/index.md)
  (`<stepType>.md`). `settings` içi referans id'ler (`propertyId`/`userGroupId`/`targetProcessStepId`…) uygulama-katmanı doğrulaması (§5).
- **Graf bütünlüğü:** akış topolojisi `ProcessStepAction.targetProcessStepId`'de (settings'te değil); kenar hedefi aynı servis
  içinde olmalı (→ process-step.md §2).

### 3.5 ProcessViewProfile (+ property + setting)
| Method | Path | Amaç |
|---|---|---|
| GET · POST | `/services/{serviceId}/view-profiles` | Görüntüleme profilleri |
| GET · PUT · DELETE | `/view-profiles/{id}` | Profil oku/güncelle/sil |
| PUT | `/view-profiles/{id}/properties` | Profildeki alan ayarları (görünür/düzenlenebilir/zorunlu/sıra) — toplu |
| PUT | `/view-profile-properties/{id}/settings` | Alan **profil-bazlı override** (`ProcessViewProfilePropertySetting` key/value) |
Model → [`models/service-settings/view-profile.md`](../../models/service-settings/view-profile.md) ailesi.

### 3.6 BusinessRule · ServiceTrigger
| Method | Path | Amaç |
|---|---|---|
| — | `/services/{serviceId}/business-rules` (CRUD) | **İş kuralı CRUD** → mevcut [`service-settings/business-rule-endpoints.md`](../../service-settings/business-rule-endpoints.md) §7 (bu desenle aynı; `configuration` JSONB `businessRuleActionType` şemasıyla doğrulanır) |
| GET · POST | `/services/{serviceId}/service-triggers` | **ServiceTrigger** (olay/zaman tetikleyici) |
| GET · PUT · DELETE | `/service-triggers/{id}` | Tetikleyici oku/güncelle/sil (`serviceTriggerType` + invariant'lar → service-trigger.md) |

## 4. Organizasyon-ayarı kaynakları (design-time CRUD)
Servise değil **organizasyona** bağlı, servisler-arası paylaşılan ayarlar (→ [`organization-settings/index.md`](../../organization-settings/index.md)).
Aynı CRUD deseni (`GET/POST/PUT/DELETE`, RLS, soft-delete).

| Kaynak | Path kökü | Model |
|---|---|---|
| **Action** (aksiyon şablonu) | `/organization/actions` | action.md (`actionType`·`styleId`·…) |
| **Status** (durum) | `/organization/statuses` | status.md (`styleId`) |
| **Style** (stil) | `/organization/styles` | style.md (`bgColor`/`fontColor`) |
| **Translation** (çeviri) | `/organization/translations` | translation.md (`code`+`languageCode`) |
| **UserGroup** | `/organization/user-groups` | user-group.md |
| **Referans veriler** | `/organization/{companies\|departments\|cost-centers\|professions\|positions\|worker-levels\|credit-cards\|working-schedules\|vacation-days}` | ilgili org-settings modeli |

> **Not:** Bu org-veri uçlarının **okuma (GET)** tarafı iş kuralı motorunun `organizationData` kaynağıyla ortaktır
> (→ business-rule-endpoints §3); burada **yazma (POST/PUT/DELETE)** tarafı eklenir (tasarım-zamanı). `synchronizationStatus`
> (→ [`models/enums/sync-status.md`](../../models/enums/sync-status.md)) harici ERP senkronunu izler; **toplu senkron ucu** → §6.

## 5. `settings` doğrulama & referans bütünlüğü (çapraz-kesen)
- **Şekil (JSON Schema):** `Property.settings` / `ProcessStep.settings` her yazımda **ayrımlayıcıya** (`propertyType`/`stepType`)
  ait JSON Schema ile doğrulanır (§3.3/§3.4); `additionalProperties:false` → bilinmeyen anahtar reddedilir. `configuration` (BusinessRule)
  aynı şekilde `businessRuleActionType` şemasıyla.
- **Referans bütünlüğü (uygulama-katmanı):** `settings`/`configuration` içindeki **mantıksal id'ler** DB FK'si değildir; kaydetme
  anında "hedef var mı + aynı servis/kapsam mı" denetlenir. **Silme koruması:** bir Property/Step/Status/Action silinmeden önce
  "buna referans veren ayar var mı?" taranır (→ todo "settings referans bütünlüğü").
- **`code` immutability:** instance oluştuktan sonra `code` kilitlenir (draft penceresi dışında rename yok).

## 6. Toplu işlemler & taşıma
- **Servis tanımı export/import:** `GET/PUT /services/{id}/definition` — bir servisin **tüm ayarını** tek dokümanla taşır (yedek,
  şablon, ortamlar-arası kopya). Ortamlar-arası akış **ortam (env) modeline** bağlı (→ todo "Ortam modeli").
- **Toplu senkron (org referans verisi):** harici ERP'den `company/department/user…` **toplu upsert** ucu — bugünkü Customer API'de
  **yok** (todo ön-koşulu); tasarım/senkron katmanı olarak buraya eklenir; her kaydın `synchronizationStatus`'u güncellenir.

## 7. Draft / yayınlama & versiyonlama (pilotta inşa edildi)
> **Durum:** 🟢 Pilotta inşa edildi (v0.41-1) → [`implementation-status.md`](../../implementation-status.md); model →
> [`models/service-settings/service.md`](../../models/service-settings/service.md) "Versiyonlama & yayınlama".

- **Akış = `draft → publish`:** Designer değişiklikleri doğrudan canlıya gitmez → `Service.hasUnpublishedChanges = true`. **Publish**,
  taslağı yeni bir **versiyon** olarak sabitler (`currentVersion`↑ · `lastPublishedAt` · `ServiceVersion` snapshot; `hasUnpublishedChanges=false`).
- **Versiyonlama:** çalışan instance'lar **başlatıldıkları versiyonun** tanımını kullanır (yayın eski instance'ları etkilemez).
- **Kod kilidi:** yayınlanan kaynağın `code`'u kilitlenir (§5).
- **Arşivleme:** servis soft-arşivlenir (`archivedAt`/`archivedBy`); **`ArchivedChecker`** arşivli parent altındaki property/view-profile/
  service/publish **yazma yollarını** `FailedPrecondition` ile reddeder; `archiveFilter` (active/archived/all).
- 🟦 **Kalan açık:** **ortamlar-arası (env) kopya/promote** + `ServiceVersion` **snapshot içeriği** → todo ("Ortam modeli"). Not:
  versiyonlama/arşivleme pilotta **ortam modelinden bağımsız** inşa edildi.

## 8. Denetim / loglama (açık)
- 🟦 **AÇIK:** Ayar-değişiklik **denetim izi** (kim, ne, ne zaman) — plan hazır (`SettingsLog`/`SettingsLogBatch` →
  [`research/settings-log/index.md`](../../research/settings-log/index.md)), karar bekliyor; KVKK/saklama → todo.

## 9. Açık noktalar (→ [`todo.md`](../../todo.md))
Ortak **hata sözleşmesi** · **ortamlar-arası kopya/promote** (env modeli — *draft/publish + versiyonlama + arşivleme pilotta inşa edildi
→ §7*) · **toplu senkron** ucu (Customer API ön-koşulu) · ayar-değişiklik **loglama** (SettingsLog) · `settings` **referans bütünlüğü +
silme koruması** kesin kuralları · yetki granülaritesi (hangi rol hangi kaynağı yazar).

---

*Oluşturma: 2026-08-28.*
