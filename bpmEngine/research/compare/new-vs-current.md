# Yeni Flovo BPM vs Mevcut (Eski) Flovo — Farklar

> **Amaç:** Mevcut (eski) Flovo BPM tarafı ile **yeni proje tasarımı** arasındaki farkları tek yerde toplamak —
> **neler eklendi, neler çıkarıldı, neler yeniden adlandırıldı / taşındı** — ve sonda **başarılı/başarısız değerlendirmesi.**
>
> **Kaynak:** Tasarım dokümanları (`../../flovo-bpm-engine.md`, `../../servis-ayarlari/*`, `../../genel-ayarlar/*`) ·
> Mevcut proje referansı → `../current-flovo-bpm-engine/`.
>
> **Not:** Bu **canlı özet**tir; her maddenin gerekçesi/detayı ilgili tasarım dosyasındadır. Çakışınca **ilgili doküman esastır.**

---

## 0. Özet — En Büyük Değişiklikler
| # | Değişiklik | Eski | Yeni |
|---|---|---|---|
| 1 | **Aksiyon seçimi + yönlendirme** | Örtük seçim + `targetProcessStepId` | **Aksiyon kodu** aksiyonu seçer (`default`/`onFail`/`true`-`false`/switch); **`targetProcessStepId` korunur** ve adıma yönlendirir |
| 2 | **Adımlar arası veri** | Örtük/server-driven | **Explicit `parameters` · `changeList` · `action`** modeli |
| 3 | **İş kuralı katmanı** | Motorla iç içe | **Frontend realtime katman**; motoru doğrudan etkilemez |
| 4 | **Renk/stil** | Statik Bootstrap (`actionType`) | **Dinamik Style** varlığı (ayrı yönetim) |
| 5 | **Aksiyon türleri** | İş-bazlı custom (`expform-*`, `new-instance*`...) | **Sade genel türler** (Manuel/withForm/Fotoğraf Çek/...) |
| 6 | **Aksiyon tanımı** | Tek DTO | **ActionDto = şablon** + adıma kopyalanan binding |
| 7 | **Adlandırma** | "field" | **"property"** (`...FieldId → ...PropertyId`) |
| 8 | **Raporlar** | View-profile içinde | **Ayrıldı** (ayrı özellik) |
| 9 | **Şişman modeller** | PropertyDto ~60 alan | **İnce çekirdek + tipe-özel ayar** |
| 10 | **Eba entegrasyonu** | Var (`ebaIntegratedFlovoApp`, `FromEba`) | **Tamamen kaldırıldı** |
| 11 | **Çeviri (i18n)** | Dağınık/örtük | **`code`-bazlı çeviri motoru** (ortak+organizasyon, `definition`=varsayılan dil) |
| 12 | **Organizasyon (kiracı)** | **Account** (`accountId`) + `solutionid` başlıkları | **Organization** (`organizationId`) varlığı (`defaultLang`, `idleTimeoutMinute`, `logoUrl`) |
| 13 | **Seçim öğesi** | `propertyItems` (değer=metin) | **`PropertyItem`** — `code` (çeviri) ile `value` **ayrıldı** |

---

## 1. Motor / Mimari (`../../flovo-bpm-engine.md`)
**➕ Eklendi**
- **Aksiyon-kodu tabanlı aksiyon seçimi:** adım sonucu → **kod** (`default`/`onFail`/`true`/`false`/switch) → o kodlu aksiyon; seçilen aksiyonun **`targetProcessStepId`**'si sonraki adıma yönlendirir.
- **`parameters` / `changeList` / `action`** veri aktarım modeli (niyetli/explicit).
- **changeList evrensel giriş kuralı:** her adım, işini yapmadan ÖNCE changeList'i forma uygular.
- **İki-katman ayrımı:** form-mantığı (frontend realtime) ↔ akış-mantığı (motor).
- **ActionDto = yeniden kullanılabilir aksiyon şablonu** kavramı.

**➖ Çıkarıldı / değişti**
- "Her şey backend / ince istemci" yaklaşımı yeniden değerlendirildi (iş kuralları frontend'e taşındı).

**↔ Korundu**
- Servis / Solution / **Organization** çok-kiracılık modeli (`organizationId`/`solutionid`/`ServiceId`) — model korundu, **Account → Organization** olarak yeniden adlandırıldı (`accountId`→`organizationId`).
- Tasarım-zamanı 6-alan sırası (property → profil → kural → aksiyon → durum → adım).
- Aksiyonun **`targetProcessStepId`**'si (aksiyon çalışınca hangi adıma ilerleneceği) — **korunur**; üstüne **aksiyon-kodu seçimi** formalize edildi.

---

## 2. Süreç Adımları (`../../servis-ayarlari/process-step.md`)
Mevcut **15 adım tipi** (biri, `atama`, enum'da tanımlı ama **kullanılmayan**) → yeni **19 adım** (korunan + yeni;
çıkarılan: **Adım İptali** · **Eba Entegre** · kullanılmayan **`atama`**).

**➕ Eklenen (mevcutta yok)**
- **Flovo AI** · **Switch** · **Processing** · **Form Creator** · **Form Silme** · **Form Yönlendirme** · **Süreç Adımı Tetikleme**

**➖ Çıkarılan**
- **Adım İptali** (`stepCancellation`) — kaldırıldı.
- **Eba Entegre** (`ebaIntegratedFlovoApp`) — kaldırıldı.
- **`atama`** — eski `ProcessStepType` enum'unda **tanımlı ama hiçbir yerde kullanılmayan / aktif olmayan** ölü bir değerdi
  (gerçek bir adım davranışı yoktu); bu yüzden yeni tasarıma **taşınmadı** (işlevsel bir kayıp değil).
  > ⚠️ Bu, form alanlarına **değer** yazan **Değer Atama** (`valueAssignment`) ile **karıştırılmamalı** — o ayrı ve **korunur** (aşağı bkz.).

**↔ Korunan (adım — dikkat)**
- **Değer Atama** (`valueAssignment`) → yeni **§3.4 Değer Atama** olarak **korunur** (property'ye / alt-servise değer atama).

**✏️ Yeniden adlandırılan**
- **Function → HTTP Request** (+ yeni `async` ayarı; query/template/header/body parametreleri explicit).

**🔧 Adım ortak yapısı (`ProcessStepDto`) değişiklikleri**
- **Kaldırıldı:** `selectModalItemDeactive`, `canSelectExpenses` → görüntüleme/seçim profili konusu (Form List).
- **Taşındı → Değer Atama:** `useRelatedService`, `relatedServiceId`, `targetInstancesFieldId` (→ `targetInstancesPropertyId`).
- **Değer Atama:** `valueType` değeri `FormValue` → **`PropertyValue`**; `targetFieldId`→`targetPropertyId`, `fieldId`→`propertyId`.

---

## 3. Aksiyonlar (`../../genel-ayarlar/action.md` + `../../servis-ayarlari/process-step-action.md`)
**➕ Eklendi**
- **ActionDto = aksiyon şablonu** (ayrı doküman); adıma eklenince `code`/`definition`/`icon`/`style`/`actionType` **kopyalanır**.
- **Sade actionType kataloğu:** **Manuel · withForm · Fotoğraf Çek · Dosya Seç · Barcode Tara · Webhook · Autoaction**.
- **withForm** (reasonRequired'ın yerini alır) · **Webhook** · **Autoaction** (yeni türler).
- **`parameters`/`changeList`/`action`** aktarım modeli.

**➖ Çıkarıldı**
- `reasonRequired` → **withForm** karşılıyor.
- **Custom per-job davranışları:** `fire-event`, `new-instance` / `-referenced` / `-other`, `take-photo`, `select-file`,
  `take-barcode`, `manuel-barcode-input`, `excel-export`, `expform-*`, `add-test-receipt` → genel türlere / başka mekanizmalara taşındı:
  - `new-instance*` → **Form Creator** adımı + **Form List** `addNewEnabled`
  - `expform-add-exist-expense` → **Form List** `addFromExistingRecordsIsActive`
  - `excel-export` → **raporlama** (ayrı özellik)
  - `add-test-receipt` → kaldırıldı

**✏️ Yeniden adlandırılan (DİKKAT — kavram takası)**
| Eski alan | Eski anlam | Yeni |
|---|---|---|
| `actionType` (ProcessActionDto) | renk/stil (success/danger…) | **`style`** (dinamik Style varlığı) |
| `action` (ProcessStepActionDto) | davranış (fire-event…) | **`actionType`** (tür: Manuel/withForm…) |

**↔ Korundu (binding'de):** **`targetProcessStepId`** (hedef adım), `changeStatusId`, `authorizationLevel`, `actionDisplayAuthorizedUserGroupId`, `showInHistory`, `environmentRestriction`.

---

## 4. Form Alanları (`../../servis-ayarlari/properties.md`)
Mevcut **30 ControlType** → yeni **19 alan** (16 founder + **3 mevcuttan korunan**; bazıları birleştirildi/çıkarıldı).

**➕ Eklendi**
- **İnce çekirdek + tipe-özel ayar** ayrımı (şişman ~60 alanlık `PropertyDto` sadeleştirildi).
- **`required`/`visible`/`enabled` property'den çıkarıldı → görüntüleme profiline** (alan = ne olduğu, profil = nasıl göründüğü).
- **User Info** alanı netleştirildi (Flow Info'dan ayrıldı).
- **`PropertyItem` modeli** (§2.6): `id` · `propertyId` · `value` · `code` · `definition`. **`value` ↔ `code` ayrıldı** —
  farklı comboboxlar aynı `value`'yu (0/1/2/3) kullanabildiği için **çeviri eşleşmesi `code` ile** yapılır; `(propertyId, value)` benzersiz.

**➖ Çıkarıldı**
- **DataGrid / DataGridControl** — kaldırıldı.
- **`ObjectAccessController` · `TableFieldDisplayController`** — kaldırıldı.
- **Property'den `style` alanı** — property'de style alanı yok; görünüm style ile değişmiyor.
- **`propertyName` · `label`** — `definition` ile duplicate; **binding key `code`** oldu.
- **`precition`** (Numeric) — `maxDecimalDigits` ile birleşti.

**↔ Mevcuttan korunan (ayarları belgelendi)**
- `GroupByTaxReceiptController` · `KeyValueListControl` · `ImageAreaSelector` (§3.17–§3.19) — davranış+ayarları kaynaktan çıkarıldı.

**✏️ Yeniden adlandırılan**
- **ModalList → Form List** (alt-servis alanı; **Combobox değil**).
- **`onAfterChange` → `saveAndRefreshOnAfterChange`** (anlam netleşti: değer değişince kaydet+formu yenile).
- **`maximumNumberDecimalDigits` → `maxDecimalDigits`** (Numeric; `precition` ile birleşik).

**🔗 Birleştirilen (alanın opsiyonu olarak)**
- `MaskedEntry` → **Textbox** (maske) · **`Entry` + `Editor` → Textbox** (`minLine`/`maxLine`; ayrı çok-satır alanı yok) ·
  `NumericUpDown` → **Numeric Textbox** · `MultiSelect` → **Combobox** · `DateTimePicker` → **Datepicker** ·
  `Photo` / `ImageList` → **File** · `DataGrid` görünümü → (kaldırıldı).

**🔧 Görünüm alanlarının kapsamı daraltıldı**
- `headerText` — artık **her alanda değil**; yalnız **pop-up açan alanlarda** (Combobox/Datepicker/Time Picker) pop-up başlığı.
- `fontSize`·`iconSize`·`isBold`·`textAlignment`·`stiky` — çekirdekten çıkıp **Text (statik başlık)** alanına özel oldu.

---

## 5. Görüntüleme Profilleri (`../../servis-ayarlari/view-profile.md`)
**➖ Çıkarıldı**
- **Raporlar ayrıldı:** `showOnDataGrid` + rapor objesi (`isUserReport`, `userGroupId`, `showAsManager`, `showToEveryone`).
- `ProcessViewProfilePropertyDto`'dan: `showOnListingPage`, `subFieldsViewProfiles`, `deletableStatuses`,
  `cardViewProfile`, `childFieldsProcessViewProfileFieldDtos`.

**✏️ Yeniden adlandırılan**
- `processViewProfileFields` → **`processViewProfileProperty`** · `ProcessViewProfileFieldDto` → **`ProcessViewProfilePropertyDto`** · `fieldId` → **`propertyId`**

---

## 6. İş Kuralları (`../../servis-ayarlari/work-rule.md`)
**🔧 Konumlandırma:** İş kuralları = **frontend realtime katman** (motoru doğrudan etkilemez) — netleştirildi.

**➖ Çıkarıldı:** `FromEba` (değer kaynağı) — Eba kaldırıldı.

**✏️ Yeniden adlandırılan**
| Eski | Yeni |
|---|---|
| `SetViewForFields` | `SetViewForProperties` |
| `AssignValueToField` | `AssignValueToProperty` |
| `AssignValueToPropertyField` | `AssignValueToPropertyAttribute` _(⚠️ teyit)_ |
| `FieldValue` / `FormValue` | `PropertyValue` |
| `Function` (değer kaynağı) | `HttpRequest` |

**↔ Korundu:** `ChangeViewProfile`, `ApplyValidation`, `ShowMessage`, `FillDataSource`, `SetStyle`, runtime tipleri (always/firstOpening/whenChanging), recursive koşullar.

---

## 7. Durumlar (`../../genel-ayarlar/status.md`)
**✏️ Yeniden adlandırılan:** `statusType` → **`style`** (yanlış adlandırılmıştı; aslında renk/görünüm).
**↔ Korundu:** `code`, `definition`, `icon`; aksiyonla durum değişimi (`changeStatusId`).

---

## 8. Stiller (`../../genel-ayarlar/style.md`) — YENİ KAVRAM
**➕ Eklendi:** **Dinamik Style yönetimi** — sistem stilleri (`organizationId=null`, read-only) + organizasyon stilleri (bg/font); **çapraz-kesen** (aksiyon ✓ · durum ✓ · alan ✓).
**➖ Değişti:** Statik Bootstrap renk sınıfları (`actionType`) → **dinamik Style varlığı** (referansla seçim).

---

## 9. Çeviri & Organizasyon (YENİ) — `../../genel-ayarlar/translation.md` · `../../genel-ayarlar/organization.md`
**➕ Çeviri motoru** (yeni yapı)
- **`code`-bazlı** çeviri: model `id`·`code`·`organizationId`·`tr`·`en`·`de`.
- **İki katman:** ortak (Flovo, `organizationId=null`, salt-okunur) + organizasyon çevirileri (kendi kayıtlarını günceller).
- **Çözümleme:** `definition` = organizasyonun `defaultLang` metni → dil eşleşince tabloya **gidilmez**; farklıysa
  `code`+`organizationId` (override) → `code`+`null` (ortak) → yoksa/boşsa **`definition`** fallback.

**➕ Organizasyon (tenant) varlığı**
- Model (başlangıç): `id`·`code`·`name`·`defaultLang`·`logoUrl`·`idleTimeoutMinute`.
- `code` benzersiz + dış referans anahtarı; `idleTimeoutMinute` (0=disable); `defaultLang` sabit dil seti (`tr`/`en`/`de`).

---

## 10. Genel Adlandırma Kuralı
- **field → property** (her yerde): `...FieldId` → `...PropertyId`, `fieldId`→`propertyId`, `FieldValue`/`FormValue`→`PropertyValue`.
- **Account → Organization**: `accountId`→`organizationId`, `accountUserGroup*`→`organizationUserGroup*`, `accountRestriction`→`organizationRestriction`.
- **function → HTTP Request** · **ModalList → Form List** · **statusType → style** · **(aksiyon) actionType → style** + **(aksiyon) action → actionType** · **onAfterChange → saveAndRefreshOnAfterChange**.

---

## 11. Başarılı / Başarısız Değerlendirme (mevcut projeye göre)

### ✅ Başarılı (mevcuda göre net iyileşme)
- **Açık veri sözleşmesi:** `parameters`/`changeList`/`action` ile adımlar arası akış **örtük server-driven**'dan çıkıp okunur/öngörülebilir hale geldi.
- **İki-katman ayrımı** (form-mantığı ↔ akış-mantığı): iş kuralları frontend realtime'a çekilerek motor sadeleşti; sorumluluklar netleşti.
- **ActionDto şablon + Style varlığı:** tekrar eden aksiyon/renk tanımları tek yerden yönetilir; statik Bootstrap bağımlılığı kalktı.
- **İnce çekirdek + tipe-özel ayar:** ~60 alanlık şişman `PropertyDto` sadeleşti; performans + self-servis kolaylaştı.
- **Ölü ağırlığın atılması:** Eba entegrasyonu, `add-test-receipt`, iş-bazlı custom aksiyonlar, çift ondalık alanı (`precition`) temizlendi.
- **i18n motoru:** `code`↔`definition` ayrımı + `definition`=varsayılan dil kısa-devresi hem tutarlı hem performanslı (çoğu kullanıcı sorgusuz).
- **Aksiyon-kodu + `targetProcessStepId` iki katmanı:** "hangi aksiyon" ile "hangi adım" ayrımı net formalize edildi.

### ⚠️ Başarısız / riskli / henüz eksik
- **Çıkarılan ama karşılığı netleşmemiş yetenekler:** view-profile'dan `subFieldsViewProfiles`/`cardViewProfile` kaldırıldı ama **Form List alt-servis görünümü** nasıl kurulacak açık.
- **`definition` = varsayılan dil kırılganlığı:** Bir organizasyon `defaultLang`'ini sonradan değiştirirse eski `definition`'lar yanlış dilde kalır; bu bir **veri-giriş kuralı** olarak garanti edilmeli (çeviri motorunun zayıf noktası).
- **Motor iç mekaniği hâlâ yazılmadı:** `flovo-bpm-engine.md`'de yürütme durumu/kalıcılık, bekleme-noktası serileştirme, hata katmanları, döngü/join **placeholder**; mevcut projede de netti değildi — devralınan boşluk.
- **`changeList` öğe yapısı belirsiz** (alan id + değer + tip?) — açık soru.
- **İsim çakışması:** `actionType` (ActionDto tür) ↔ WorkRule `actionType` (etki tipi) — ayrı varlıklar ama karışma riski.
- **ActionDto kopya ↔ canlı referans:** şablon değişince adımdaki kopyalar güncellensin mi — karar bekliyor.
- **İki-katman tekrarı:** değer atama & karşılaştırma hem adımda hem iş kuralında var — sınır netleşmeli.

---

## 12. Açık / Karara Bağlı Konular (özet)
- **Form List** alt-servis görüntülenecek alanları / seçilebilirliği view-profile ile nasıl ayarlanacak.
- **Şişman model** sadeleştirmesinde hangi alanlar çekirdek, hangileri tipe-özel.
- **`actionType` isim çakışması** (ActionDto ↔ WorkRule) — yeniden adlandırma opsiyonel.
- **ActionDto kopya ↔ canlı referans** senkronu.
- **Çeviri:** `definition`↔`defaultLang` tutarlılık garantisi; `du`→`de` gibi dil netliği.

---

*Güncelleme: 2026-07-01 · Tasarım dokümanları ile `../current-flovo-bpm-engine/` karşılaştırılarak derlendi.*
