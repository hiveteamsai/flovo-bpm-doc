# Değer Şablonları (Property tipine göre) — İndeks

> **Durum:** 🟡 TASLAK — ilk çıkarım; her tip ayrı ayrı düzenlenecek.
> **Amaç:** Her `propertyType` için, o alanın değerinin **`InstanceValue.data` (JSONB) içinde hangi şekille (model) tutulacağı**
> ve **`projectToAttr=true`** iken **hangi fihrist tablosuna** (`InstanceAttr` / `InstanceListItem`) **nasıl** yansıyacağı
> tek tek tanımlanır. Bu klasör, değer-saklama modellerinin (`../instance-value.md` · `../instance-attr.md` ·
> `../instance-list-item.md`) **tip-bazlı somut şekil kataloğudur**.
>
> **Alan tanımı/davranış (kaynak):** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3 ·
> **çekirdek model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **tip listesi:** [`../../enums/property-type.md`](../../enums/property-type.md).

## Ortak çekirdek şekiller
| Döküman | Rol |
|---|---|
| [`labeled-value.md`](./labeled-value.md) | **Core değer şekli** — bazı property'lerin `value`'sunu saran `{value, display, translationCode}` (combobox/radio/liste value…). Tablo değil; JSONB'ye gömülü + Attr'a açılır. |

## Değer şablonları (18 tip)

### Skaler (→ `InstanceAttr`, tek satır/tek tipli kolon)
| Tip | Döküman | JSONB şekli | Attr kolonu |
|---|---|---|---|
| `textbox` | [`textbox.md`](./textbox.md) | `string` | `textValue` |
| `numericTextbox` | [`numeric-textbox.md`](./numeric-textbox.md) | `number` | `numValue` |
| `datepicker` | [`datepicker.md`](./datepicker.md) | ISO tarih `string` | `dateValue` |
| `timePicker` | [`time-picker.md`](./time-picker.md) | `"HH:mm"` `string` | `textValue` |
| `checkbox` | [`checkbox.md`](./checkbox.md) | `bool` | `boolValue` |
| `barcode` | [`barcode.md`](./barcode.md) | `string` | `textValue` |
| `phone` | [`phone.md`](./phone.md) | `{countryCode, number}` obje | `textValue` (birleşik) |

### Etiketli seçim (→ `LabeledValue`; `InstanceAttr` veya çoklu ise `InstanceListItem`)
| Tip | Döküman | JSONB şekli | Projeksiyon |
|---|---|---|---|
| `combobox` | [`combobox.md`](./combobox.md) | `LabeledValue` / dizi / ilişkili=id | Attr veya ListItem / AssociatedInstance |
| `radiobuttonList` | [`radiobutton-list.md`](./radiobutton-list.md) | `LabeledValue` | Attr (textValue+display+translationCode) |

### Liste-of-model (→ `InstanceListItem`, kalem-bazlı)
| Tip | Döküman | JSONB şekli | Projeksiyon |
|---|---|---|---|
| `groupByTaxReceipt` | [`group-by-tax-receipt.md`](./group-by-tax-receipt.md) | obje dizisi (kalem) | ListItem (kalem × alt-alan) |
| `keyValueList` | [`key-value-list.md`](./key-value-list.md) | `{key,value}` dizisi | ListItem |

### Yapısal / dosya / ilişkisel
| Tip | Döküman | JSONB şekli | Projeksiyon |
|---|---|---|---|
| `mapViewer` | [`map-viewer.md`](./map-viewer.md) | `{lat,lng,address}` obje | `address`→Attr.textValue; `lat`/`lng`→data (GIN/PostGIS) |
| `file` | [`file.md`](./file.md) | **list-of-model** (`url`+`fileInfo{user,date,location}`) — hep dizi | genelde yok; gerekirse ListItem |
| `formList` | [`form-list.md`](./form-list.md) | **list-of-model** (`instanceId`+`status`+`rejectedBy`+`rejectedDate`+`rejectedByReason`) | child değeri + `AssociatedInstance` (**senkron**); satır durumu → `InstanceListItem` |

### Yansıma & statik (yazılmaz veya reflectionMode'a bağlı)
| Tip | Döküman | JSONB şekli | Projeksiyon |
|---|---|---|---|
| `userInfo` | [`user-info.md`](./user-info.md) | snapshot skaler/labeled | Attr (normal alan gibi) |
| `parentProperty` | [`parent-property.md`](./parent-property.md) | `reflectionMode`'a göre | snapshot/materialized → Attr; live → yok |
| `flowInfo` | [`flow-info.md`](./flow-info.md) | **yazılmaz** (canlı) | yok — `Instance` kolonları / join |
| `text` | [`text.md`](./text.md) | **yok** (statik label) | yok |

## Notlar
- **Şekil ↔ projeksiyon eşlemesi** araştırma kaynağındaki değer-şekilleri tablosuna dayanır → [`../../../research/property-value-storage/form-deger-saklama-v2.html`](../../../research/property-value-storage/form-deger-saklama-v2.html) §7.
- **`projectToAttr=false`** ise (hangi tip olursa olsun) değer yalnız `InstanceValue.data`'da kalır; eşitlik sorgusu için `data` üzerindeki **GIN** yeterlidir (fihrist üretilmez).
- **Etiketli değerlerde** `display`/`translationCode` çözümü → [`labeled-value.md`](./labeled-value.md) "Okuma kuralı".
- **Kullanıcı-referans konvansiyonu (Q11/Q13):** Değer içinde bir kullanıcıya atıf, **`{ userId: int, nameSurname: string }`** objesiyle yapılır (id + ad-soyad **birlikte**). Fihriste: `numValue`=userId · `textValue`=nameSurname. Kullananlar: `file.fileInfo.user`, `formList.rejectedBy`.
- **`InstanceListItem.attrCode` konvansiyonu (Q12):** Liste kalemi bir **nesne** ise `attrCode` = **alt-alan adı** (`expenseType`/`key`/`url`/`instanceId`/`status`…). Kalem **tek atomik değer** ise (adlı alt-alanı / kendi `value` kodu **yok**; ör. multi-select combobox'ın LabeledValue'su) `attrCode` = sabit **`"value"`**.

*Oluşturma: 2026-08-06.*
