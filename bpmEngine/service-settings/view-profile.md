# Flovo — Görüntüleme Profilleri (View Profiles) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR
> **Amaç:** Bir formun **farklı süreç adımlarında nasıl görüntüleneceğini** kontrol eden **görüntüleme profili**
> varlığını tanımlamak (alan görünürlüğü / düzenlenebilirliği / zorunluluğu / sırası).
> (Form alanları → `properties.md`; süreç adımları → `process-step.md`.)

---

## 0. View Profile Nedir?
Bir **görüntüleme profili (view profile)**, aynı formun **farklı süreç adımlarında / farklı kullanıcılara** nasıl
görüneceğini belirler: hangi alanlar **görünür**, hangileri **düzenlenebilir**, hangileri **zorunlu** ve hangi
**sırada**. Böylece tek form, farklı adımlarda farklı şekillerde sunulur (örn. talep eden için düzenlenebilir,
onaylayan için salt-okunur).

---

## 1. Profil Veri Modeli (`ProcessViewProfileDto`)
| Alan | Tip | Açıklama |
|---|---|---|
| `id` | int | Profil ID'si (primary key) |
| `serviceId` | int | Bağlı servis ID'si (servis-bazlı tanımlı) |
| `code` | string | Profil kodu (benzersiz) |
| `definition` | string | Profil adı |
| `isDefault` | bool | Varsayılan profil mi |
| `processViewProfileProperty` | List\<`ProcessViewProfilePropertyDto`\> | Profildeki **alan (property) yapılandırmaları** (§2) |

---

## 2. Profil Alan Yapısı (`ProcessViewProfilePropertyDto`)
Her profil, formun her alanını ayrı yapılandırır.

| Alan | Tip | Açıklama |
|---|---|---|
| `id` | int | Kayıt ID'si |
| `viewProfileId` | int | Bağlı profil ID'si |
| `propertyId` | int | Form alanı (property) ID'si |
| `visible` | bool | Alan görünür mü |
| `enabled` | bool | Alan düzenlenebilir mi |
| `required` | bool | Alan zorunlu mu |
| `order` | int | Sıralama (sürükle-bırak) |

> Bir alanın **görünür / düzenlenebilir / zorunlu** olması **burada** (profilde) tutulur; alanın kendi tanımında değil
> (→ `properties.md`). Yani: *alan = ne olduğu*, *profil = nerede nasıl göründüğü*.

---

## 3. Raporlama (kapsam dışı)
View Profile **yalnız formun adım-bazlı görünümünü** kontrol eder. **Raporlama ayrı bir özelliktir** (ayrı doküman/
yönetim ekranı olacak).

---

## 4. Çalışma Prensibi (runtime)
1. Her servis için bir veya birden fazla profil tanımlanır.
2. **`isDefault: true`** olan profil, süreç adımında profil belirtilmediğinde kullanılır.
3. Süreç adımına profil atanır (`processViewProfileId`).
4. Form açıldığında aktif adımın profili yüklenir:
   - `visible: false` → alan gizlenir
   - `enabled: false` → alan salt-okunur
   - `required: true` → alan zorunlu
   - alanlar `order` değerine göre sıralanır
5. Çalışma zamanında profil, iş kuralı **`ChangeViewProfile`** ile değiştirilebilir (→ `work-rule.md` §4).

---

## 5. Açık Kararlar / Sorular
> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(view-profile §..)`
> atfıyla bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

> **Çözülenler (yerel karar log'u):**
- [x] **Alan-özel görünüm ayarlarının profil bazında yönetimi** — **KARAR (B2):** tipe-özel, profil-bazlı ayarlar
      **`ProcessViewProfilePropertySetting {viewProfilePropertyId, key, value}`** ile tutulur (`propertyType`'a göre
      **dictionary**); `Property` varsayılanını profil düzeyinde ezer. Genel `visible/enabled/required/order` birinci
      sınıf kalır. Key kataloğu → `../models/service-settings/view-profile-property.md` (Form List: `activeStartActions`,
      `addFromExistingStatusIds`; öneri `selectedEditable`). `selectableModeActive` (tik modu) **alan-düzeyi** `Property`
      ayarıdır. _Örn._ *süreç başlatan* yeni form ekler
      ama *yönetici* ekleyemez; *yönetici* tik değiştirir, *başlatan* değiştiremez. **Kalan:** `reOrder`/`editOnlyOwnPosition`
      da profil-bazlı mı? (→ `../todo.md`)
- [x] Profiller **servis-bazlı** tanımlanır (bir servise ait — `serviceId`).

---

## 6. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-06-26.*
