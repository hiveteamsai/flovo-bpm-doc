# Flovo — İş Kuralları (Work Rules) Tasarımı

> **Durum:** 🟡 TASLAK — temel model tanımlı; detaylar sonra.
> **Amaç:** Form üzerinde **gerçek zamanlı (realtime) frontend davranışlarını** koşul-aksiyon tabanlı tanımlamak
> (alan göster/gizle, validasyon, değer atama, veri kaynağı doldurma, stil).
>
> **İlişki:** Alanlar → `properties.md` · Görüntüleme profilleri → `view-profile.md` · Stil → `../organization-settings/style.md` ·
> Süreç adımları/aksiyonlar → `process-step.md` / `process-step-action.md`.

---

## 0. Önemli — İş Kuralı ≠ BPM Motoru (katman ayrımı)
İş kuralları **frontend'de gerçek zamanlı çalışan işlerdir**; bu yüzden **BPM motorunu (flow/orkestrasyon) doğrudan
etkilemez.** İki **ayrı katman** vardır:

| Katman | Nerede çalışır | Ne yapar | Doküman |
|---|---|---|---|
| **Form-mantığı** = **İş Kuralları** | **Frontend, realtime** (form açıkken) | Açık formda anlık UX: alan göster/gizle, anlık validasyon, anlık değer/stil | **bu dosya** |
| **Akış-mantığı** = **BPM Motoru** | **Backend / motor** (adım geçişleri) | Süreç adımları arası ilerleme, aksiyon kodu yönlendirmesi, durum değişimi | `../flovo-bpm-engine.md` |

> İş kuralı, **kullanıcı form üzerinde gezinirken** (alan değiştirir, açar) tetiklenir ve **o anki formu** düzenler.
> Motorun adım-geçiş kararına karışmaz.

---

## 1. İş Kuralı Nedir?
Bir **iş kuralı (work rule)**, form üzerinde **koşul → aksiyon** tabanlı dinamik bir davranıştır. Belirli koşullar
sağlandığında **frontend'de anlık** olarak tetiklenir ve formu değiştirir: validasyon, değer atama, alan görünürlüğü,
veri kaynağı doldurma, stil vb.

---

## 2. Veri Modeli (`WorkRuleDto`)
| Alan | Tip | Açıklama |
|---|---|---|
| `id` | int | Kural ID'si |
| `organizationId` | int | Organizasyon ID'si (FK → `../organization-settings/organization.md` `id`) |
| `serviceId` | int | Servis ID'si |
| `code` | string | Kural kodu |
| `definition` | string | Kural adı/tanımı |
| `icon` | string | İkon |
| `environmentRestriction` | string | Ortam kısıtlaması |
| `actionType` | enum | Kural aksiyon tipi (§3) |
| `workRuleRuntimeType` | enum | Çalışma zamanı: `always` / `firstOpening` / `whenChanging` |
| `workRuleConditionType` | enum | Koşul birleştirme (VE/VEYA) |
| `workRuleConditions` | List | Koşul listesi (recursive) (§4) |
| `activeViewProfiles` | List\<int\> | Sadece bu görüntüleme profillerinde çalış (→ `view-profile.md`) |
| `shouldNotWorkInReadonlyMode` | bool | Salt-okunur modda çalışmasın |

---

## 3. Aksiyon Tipleri (`actionType`)
İş kuralı tetiklendiğinde **frontend'de** ne yapacağını belirler.

| Aksiyon | Ne yapar |
|---|---|
| `SetViewForProperties` | Hedef property'lerin `visible` / `enabled` / `required` durumunu ayarlar |
| `ChangeViewProfile` | Aktif görüntüleme profilini değiştirir (→ `view-profile.md`) |
| `ApplyValidation` | Koşullu validasyon; sağlanmazsa hata mesajı |
| `ShowMessage` | Kullanıcıya bilgi mesajı (başlık + içerik; dinamik değer) |
| `AssignValueToProperty` | Bir property'nin **değerine** değer atar (§3.1) |
| `FillDataSource` | Combobox / Form List gibi seçim alanlarının veri kaynağını doldurur |
| `AssignValueToPropertyAttribute` | Property'nin **değerine değil, bir niteliğine** (attribute) değer atar _(⚠️ isim teyit — §6)_ |
| `SetStyle` | Property/form'un **tekil görünüm niteliklerini** (örn. `fontSize`, `titleColor`) değiştirir. **`../organization-settings/style.md` Style varlığını seçmez** — daha spesifik, tekil nitelik değişimidir |

### 3.1 — `AssignValueToProperty` değer kaynakları (`ValueAssignType`)
`FixedValue` (sabit) · `PropertyValue` (başka bir property'nin değeri) · `FromCalculation` (expression) ·
`FromDataSet` (veri setinden) · `Search` (arama) · `HttpRequest` (HTTP Request çağrısı ile → `process-step.md` §3.2).

---

## 4. Koşul Yapısı (`WorkRuleConditionDto`)
Her koşul iki değerin bir **operatörle** karşılaştırılmasıdır; koşullar **iç içe** (recursive) gruplanabilir (VE/VEYA).

| Alan | Açıklama |
|---|---|
| `referenceValue` | Referans değer (sol taraf) — tip: `WorkRuleConditionCompareType` |
| `valueToCompare` | Karşılaştırılacak değer (sağ taraf) |
| `criterionType` | Operatör (=, !=, boş, boş değil, >, >=, <, <=, başlar, biter, içerir, içermez) |
| `isConditionList` | İç içe koşul grubu mu |
| `workRuleConditionType` | Alt grup birleştirme (VE/VEYA) |
| `workRuleConditions` | İç içe koşullar (recursive) |

**Karşılaştırma değer tipleri (`WorkRuleConditionCompareType`):** `PropertyValue` · `ViewProfile` (aktif görüntüleme
profili) · `FixedValue` · `FromCalculate` (expression).

---

## 5. Çalışma Prensibi (frontend realtime)
1. **Form açılır** veya **bir property değişir** (frontend olayı).
2. `workRuleRuntimeType` kontrolü: `always` (açılış + her değişiklik) / `firstOpening` (yalnız açılış) /
   `whenChanging` (yalnız değişimde).
3. `shouldNotWorkInReadonlyMode` → salt-okunur modda atlanır.
4. `activeViewProfiles` doluysa, **aktif profil** listede mi kontrol edilir.
5. Koşullar **recursive** değerlendirilir (VE/VEYA).
6. Koşul **TRUE** → ilgili `actionType` **frontend'de anlık** çalışır; **FALSE** → çalışmaz.

> Tümü **istemci tarafında**, motoru beklemeden olur — anlık UX içindir. Kalıcı/akış kararları motorun işidir (§0).

---

## 6. Açık Kararlar / Sorular
- [ ] **İki-katman sınırı:** **değer atama** ve **karşılaştırma** hem **süreç adımı** (`process-step.md` §3.4 / §3.13)
      hem **iş kuralı** olarak var. Sınır net mi? Öneri: iş kuralı = **anlık form UX**, adım = **kalıcı/akış** kararı.
- [ ] **`AssignValueToPropertyAttribute`** adı teyit — "property'nin niteliğine değer atama" doğru karşılık mı?
- [x] **`SetStyle`** `style.md` Style varlığını **seçmez**; yalnız tekil görünüm niteliklerini (`fontSize`, `titleColor` vb.) değiştirir. _(Detay, iş kuralı en son şekillenince netleşecek → §7.)_
- [ ] **`FillDataSource`** kaynak tipleri (Organization Data / User Data / API) nasıl modellenecek?
- [ ] **Performans:** `always` kuralları her değişiklikte değil, **alan-bağımlı** (yalnız ilgili property değişince) tetiklensin mi?
- [x] İş kuralları **servis-bazlı** tanımlanır (bir servise ait — `serviceId`).

---

## 7. Notlar / Ham Düşünceler
> _(Bu dosya şimdilik **taslak**; detaylandırma sonra.)_

---

*Oluşturma: 2026-06-30.*
