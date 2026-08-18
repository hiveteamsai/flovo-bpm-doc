# Değer Şablonu — `userInfo` (User Info)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `userInfo` (salt-okunur kullanıcı metadata) değerinin **`InstanceValue.data` içindeki şekli** + fihrist yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.16 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **yansıma:** [`../../enums/reflection-mode.md`](../../enums/reflection-mode.md) · **değer modeli:** [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
`userInfoValue` ile seçilen kullanıcı bilgisi (ad/e-posta/departman/unvan/yönetici…). **Değerin oluşturma-anı mı (dondurulmuş)
yoksa güncel mi** gösterileceği **`reflectionMode`** ile seçilir (→ [`../../enums/reflection-mode.md`](../../enums/reflection-mode.md)):

| `reflectionMode` | `data`'da tutulur mu? | Nasıl |
|---|---|---|
| `snapshot` (**vars.**) | **Evet** | **Oluşturma anında** kullanıcının o-anki bilgisi `data`'ya **kopyalanır + dondurulur** ("o anki departman/unvan"). |
| `live` | **Hayır** | `data`'ya **yazılmaz**; okurken **User**'dan **güncel** getirilir (kullanıcı departmanı sonradan değişirse yeni değer görünür). |

Şekil, getirilen bilgiye göre (`snapshot`'ta `data`'da; `live`'da okuma sonucunda):
- **Skaler** (ad/e-posta): `string`
```json
{ "creatorDept": "Satınalma" }
```
- **Etiketli** (kod+ad taşıyan bilgi, ör. departman kodu): `LabeledValue` ([`labeled-value.md`](./labeled-value.md))

- Girdi değildir; kullanıcı düzenleyemez.

## 2. Projeksiyon — `projectToAttr=true`
| `reflectionMode` / Şekil | Hedef | Kolon |
|---|---|---|
| `snapshot` · Skaler | **InstanceAttr** | `textValue` (normal alan gibi) |
| `snapshot` · Etiketli | **InstanceAttr** | `textValue`=`value` · `display` · `translationCode` |
| `live` | **Yok** | `data`'da değer olmadığından projekte edilmez; rapor gerekiyorsa **User** join'i (veya `snapshot`'a geç). |

## 3. Notlar
- **`snapshot` (vars.)** sonradan kullanıcı departmanı değişse bile kayıt **eski değeri** korur (audit-dostu, ucuz); **`live`** her okumada **güncel**'i verir (Flow Info gibi). Seçim ayardan (`reflectionMode`) yapılır.
- **`materialized` geçerli değildir** (yalnız `parentProperty`): User bilgisi `AssociatedInstance` yayılım yolunda olmadığından otomatik-tazeleme yerine `live` kullanılır.
- `userInfoValue` = hangi kullanıcı bilgisi (ad/e-posta/departman/unvan/yönetici…).

*Oluşturma: 2026-08-06.*
