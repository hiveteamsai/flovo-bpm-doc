# Model — InstanceListItem (liste kalemleri fihristi / projeksiyon)

> **Durum:** 🟡 TASLAK — değer-saklama mimarisinden türetildi (→ `../../research/property-value-storage/form-deger-saklama-v2.html`); alanlar gözden geçirilecek.
> **Yeni model.**
> **Amaç:** "Liste içinde obje" tipi alanlar (`groupByTax`, `keyValueList` gibi **aynı JSON içindeki** kalemler) için
> rapor/filtre/toplam fihristi. Her kalemin her alt-alanı **ayrı satır**. `InstanceValue.data` içindeki diziden **türetilir**;
> yeniden üretilebilir projeksiyondur.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `instanceId` | int | PK · FK → Instance.id | Kimlik. |
| `serviceId` | int | PK · FK → Service.id | Kimlik + izolasyon/partition. |
| `organizationId` | int | (denormalize) | Kiracı — RLS/tenant izolasyonu. |
| `listCode` | string | PK | Hangi liste property'si (`Property.code`, ör. `groupByTax`). **`code`-keyed**. |
| `itemIndex` | int | PK | Listedeki kaçıncı kalem (0, 1, 2…). |
| `attrCode` | string | PK | Kalemin alt-alanı (`vergiOrani`, `tutar`…). **`code`-keyed**. |
| `numValue` | numeric? | — | Sayısal alt-alan değeri. |
| `textValue` | string? | — | Metin / seçim kodu. |
| `dateValue` | datetime? | — | Tarih. |
| `boolValue` | bool? | — | Bool. |
| `display` | string? | — | Etiketli alt-alan **görünen adı** (`LabeledValue.display` — org varsayılan dili, `PropertyItem.definition`'dan; kullanıcı dili aynıysa join'siz doğrudan kullanılır); yoksa null. |
| `translationCode` | string? | — | `PropertyItem.translationCode`'dan; dil uyuşmazlığında doğru dil Translation'dan getirilir; yoksa null (→ okuma kuralı: [`labeled-value.md`](./propertyValuesTemplates/labeled-value.md)). |

> **Birincil anahtar:** `(instanceId, serviceId, listCode, itemIndex, attrCode)`. Tek **generic** tablo tüm liste
> kontrollerini karşılar — her liste tipi için ayrı tablo **yok**.

## İlişkiler
- **N – 1** → `Instance` (`instanceId`), `Service` (`serviceId`).
- **Türetilir** ← `InstanceValue.data` (liste-of-model alanları; `Property.projectToAttr=true`).

## Notlar / açık noktalar
- **`InstanceListItem` ≠ Form List:** Bu tablo **aynı JSON içindeki** kalemler içindir (liste-of-model). **Form List** ise
  alt-servis kayıtları **ayrı `Instance`**'lardır ve ilişki [`associated-instance.md`](./associated-instance.md)'de tutulur —
  child form'lar buraya **yazılmaz**.
- **Kalemi tek satır isteyen rapor** (`giderTuru | vergiOrani | tutar`): `(instanceId, itemIndex)` üzerinde **pivot** yapılır;
  sayısal sıra `numValue` index'inden gelir.
- **Tam-yansıtma:** kalem eklen/çıkarılınca projektör o instance'ın ListItem satırlarını **siler → yeniden yazar** (delta değil).
- **Kaynak mimari:** → `../../research/property-value-storage/form-deger-saklama-v2.html` (§6.4 · §9.4 · §15 Form List ayrımı).

*Oluşturma: 2026-08-04.*
