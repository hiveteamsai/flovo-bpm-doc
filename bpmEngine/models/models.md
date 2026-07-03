# Flovo BPM — Veri Modelleri (Şema Referansı)

> **Durum:** 🟡 TASLAK — mevcut tasarım dokümanlarından **ilk çıkarım**; alanlar/tipler gözden geçirilecek.
> **Amaç:** Tüm veri modellerinin **tek yerde** kısa tanımı + **birbirleriyle ilişkileri**. Her modelin **alan-düzeyi
> ayrıntısı** kendi dosyasındadır. Bu klasör **veri modeli/şema** odaklıdır; **davranış/kullanım** özellik
> dokümanlarındadır (`genel-ayarlar/`, `servis-ayarlari/`, `flovo-bpm-engine.md`).
>
> **Anahtar kuralı:** Her modelin birincil anahtarı **`id`** (int). Yabancı anahtarlar **`...Id`** (örn. `serviceId`,
> `styleId`). Kiracı kimliği **`organizationId`** (int); dış referanslarda **`organizationCode`** (string) kullanılır.

---

## 0. Hiyerarşi (özet)

**`Organization → Solution → Service → {Property · ProcessViewProfile · ProcessStep · WorkRule}`**

- **Organization** = kiracının kendisi.
- **Solution** = organizasyona bağlı; **servisleri gruplayan** tanım. Bir organizasyonda birden çok solution olabilir.
- **Service** = bir solution altında oluşturulur; **kendi ayarlarını** (property/görüntüleme profili/süreç adımı/iş
  kuralı) barındırır.
- **Organizasyon havuzu** (`Translation`, `Style`, `Status`, `Action`) = organizasyona bağlıdır; o organizasyonun
  **tüm servislerinde** kullanılabilir.
- **ProcessStepAction** = bir **ProcessStep**'e bağlıdır.

---

## 1. Modeller (dizin)

### Kiracı & hiyerarşi
| Model | Dosya | Kısa açıklama |
|---|---|---|
| **Organization** | [`organization.md`](./organization.md) | Kiracı (tenant). En üst kapsayıcı. |
| **Solution** | [`solution.md`](./solution.md) | Servisleri gruplayan tanım (organizasyona bağlı). |
| **Service** | [`service.md`](./service.md) | İş sürecinin/formun tamamı (solution altında). |

### Organizasyon havuzu (organizasyona bağlı — servislerde kullanılır)
| Model | Dosya | Kısa açıklama |
|---|---|---|
| **Translation** | [`translation.md`](./translation.md) | `code`-bazlı çok dilli metinler (ortak + organizasyon). |
| **Style** | [`style.md`](./style.md) | Renk/görünüm varlığı (bg + font). |
| **Status** | [`status.md`](./status.md) | Kaydın aşaması (etiket). |
| **Action** | [`action.md`](./action.md) | Aksiyon **şablonu** (ActionDto); adıma eklenince kopyalanır. |

### Servise bağlı (bir servise/forma ait)
| Model | Dosya | Kısa açıklama |
|---|---|---|
| **Property** | [`property.md`](./property.md) | Form alanı (kontrol tipiyle render edilir). |
| **PropertyItem** | [`property-item.md`](./property-item.md) | Seçim alanının statik seçeneği. |
| **ProcessViewProfile** | [`view-profile.md`](./view-profile.md) | Formun adım-bazlı görünümü. |
| **ProcessViewProfileProperty** | [`view-profile-property.md`](./view-profile-property.md) | Profildeki tek alan yapılandırması. |
| **ProcessViewProfilePropertySetting** | [`view-profile-property-setting.md`](./view-profile-property-setting.md) | Alanın profil-bazlı tipe-özel override'ı (key/value). |
| **ProcessStep** | [`process-step.md`](./process-step.md) | Süreç adımı (akıştaki düğüm). |
| **ProcessStepAction** | [`process-step-action.md`](./process-step-action.md) | Aksiyonun adıma bağlanması (binding). |
| **WorkRule** | [`work-rule.md`](./work-rule.md) | Frontend realtime form davranışı. 🟡 en son şekillenecek. |
| **WorkRuleCondition** | [`work-rule-condition.md`](./work-rule-condition.md) | İş kuralı koşulu (recursive). 🟡 en son. |

---

## 2. İlişki Haritası

```
Organization (id)
 ├─< Solution (organizationId)
 │    └─< Service (solutionId)
 │         ├─< Property             (serviceId) ──< PropertyItem  (propertyId; (propertyId,value) benzersiz)
 │         ├─< ProcessViewProfile   (serviceId)
 │         │        └─< ProcessViewProfileProperty (viewProfileId, propertyId → Property)
 │         │                 └─< ProcessViewProfilePropertySetting (viewProfilePropertyId; key/value — propertyType'a göre)
 │         ├─< ProcessStep          (serviceId; +organizationId = izolasyon)
 │         │        └─< ProcessStepAction (processStepId,
 │         │                               targetProcessStepId → ProcessStep,
 │         │                               changeStatusId      → Status)
 │         └─< WorkRule             (serviceId; +organizationId = izolasyon)
 │                  └─< WorkRuleCondition (workRuleId, recursive)
 │
 └── Organizasyon havuzu (organizationId) — servis modellerinde kullanılır:
      ├─< Translation (null = ortak/Flovo)
      ├─< Style       (null = sistem) ─────> Action.styleId · Status.styleId
      ├─< Action                     ┄┄┄┄> (ProcessStepAction'a bir kez kopyalanır — canlı FK yok)
      └─< Status                     ─────> ProcessStepAction.changeStatusId
```

---

## 3. İlişki Tablosu

| Kaynak | Alan | Hedef | Kardinalite | Not |
|---|---|---|---|---|
| Solution | `organizationId` | Organization.id | N–1 | |
| Service | `solutionId` | Solution.id | N–1 | organizasyon dolaylı (solution üzerinden) |
| Translation | `organizationId` | Organization.id | N–1 | `null` = ortak (Flovo) |
| Style | `organizationId` | Organization.id | N–1 | `null` = sistem stili (salt-okunur) |
| Action | `organizationId` | Organization.id | N–1 | organizasyon havuzu |
| Action | `styleId` | Style.id | N–1 | |
| Status | `organizationId` | Organization.id | N–1 | organizasyon havuzu |
| Status | `styleId` | Style.id | N–1 | |
| Property | `serviceId` | Service.id | N–1 | |
| PropertyItem | `propertyId` | Property.id | N–1 | `(propertyId, value)` benzersiz |
| ProcessViewProfile | `serviceId` | Service.id | N–1 | |
| ProcessViewProfileProperty | `viewProfileId` | ProcessViewProfile.id | N–1 | |
| ProcessViewProfileProperty | `propertyId` | Property.id | N–1 | |
| ProcessViewProfilePropertySetting | `viewProfilePropertyId` | ProcessViewProfileProperty.id | N–1 | profil-bazlı alan override (key/value) |
| ProcessStep | `serviceId` | Service.id | N–1 | asıl kapsayıcı |
| ProcessStep | `organizationId` | Organization.id | N–1 | kiracı/izolasyon (denormalize) |
| ProcessStepAction | `processStepId` | ProcessStep.id | N–1 | binding'in ait olduğu adım |
| ProcessStepAction | `targetProcessStepId` | ProcessStep.id | N–1 | ilerlenecek hedef adım |
| ProcessStepAction | `changeStatusId` | Status.id | N–1 | aksiyon sonrası durum |
| WorkRule | `serviceId` | Service.id | N–1 | asıl kapsayıcı |
| WorkRule | `organizationId` | Organization.id | N–1 | kiracı/izolasyon (denormalize) |
| WorkRule | `activeViewProfiles` | ProcessViewProfile.id | N–N | yalnız bu profillerde çalış |
| WorkRuleCondition | `workRuleId` | WorkRule.id | N–1 | |
| WorkRuleCondition | `parentConditionId` | WorkRuleCondition.id | N–1 | iç içe (recursive) |
| Translation | `code` | (kod eşleşmesi) | — | FK değil; `code` + `languageCode` + `organizationId` ile çözülür |

---

## 4. Henüz modellenmemiş / referans verilen varlıklar (açık)

| Varlık | Nerede geçiyor | Not |
|---|---|---|
| **Form / Instance** (çalıştırma kaydı) | `formId` (Customer API), süreç state | Doldurulmuş form + süreç örneği (runtime durum). |
| **User** | atama, bildirim | Kullanıcı modeli ayrıca ele alınacak. |
| **UserGroup** | `organizationUserGroupId`, `actionDisplayAuthorizedUserGroupId` | Kullanıcı grubu. |

---

## 5. Notlar
- **Enum'lar** ilgili model dosyasında listelenir (`actionType`, `controlTypeId`, `workRuleRuntimeType`, `criterionType`, `valueType`...).
- **Organizasyon havuzu** (Translation/Style/Status/Action) `genel-ayarlar/`'a; **servise bağlı** modeller `servis-ayarlari/`'ya karşılık gelir.
- **ProcessStep / WorkRule** asıl kapsayıcısı **Service**'tir; `organizationId` kiracı izolasyonu için denormalize edilmiş referanstır (gözden geçirilebilir → `../todo.md`).
- **Style tüketicileri:** yalnız **Action** ve **Status** (`styleId`). Form alanları bu Style varlığını kullanmaz.
- **Action → ProcessStepAction:** canlı bağ (FK) **yoktur**. Adıma aksiyon eklenirken Action alanları
  (`code`/`definition`/`icon`/`styleId`/`actionType`) **bir kez kopyalanır**; sonrasında iki taraf **bağımsızdır**
  (Action değişince mevcut binding'ler güncellenmez). Bu yüzden `ProcessStepAction`'da `actionId` **tutulmaz**.
- **Profil-bazlı alan override'ı:** `ProcessViewProfilePropertySetting` (`viewProfilePropertyId` + `key`/`value`),
  `propertyType`'a göre yorumlanan bir **dictionary**'dir; `Property` varsayılanını profil düzeyinde ezer (Form List:
  `activeStartActions`, `addFromExistingStatusIds`). Key kataloğu → `view-profile-property.md`.
- **WorkRule / WorkRuleCondition** frontend'de çalışır; **en son** kesinleşecek (→ `../todo.md`).

---

*Oluşturma: 2026-07-02.*
