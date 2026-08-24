# Değer Şablonu — `userInfo` (User Info)

> **Durum:** 🟢 OLGUN (v0.31)
> **Kapsam:** `userInfo` (salt-okunur kullanıcı metadata) değerinin **`InstanceValue.data` içindeki şekli** + fihrist yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.16 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **yansıma:** [`../../enums/reflection-mode.md`](../../enums/reflection-mode.md) · **değer modeli:** [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
`userInfoValue` ile seçilen kullanıcı bilgisi (ad/e-posta/departman/unvan/yönetici…). **Değerin oluşturma-anı mı (dondurulmuş)
yoksa güncel mi** gösterileceği **`reflectionMode`** ile seçilir (→ [`../../enums/reflection-mode.md`](../../enums/reflection-mode.md)):

| `reflectionMode` | `data`'da anahtar/değer | Nasıl |
|---|---|---|
| `snapshot` (**vars.**) | **Anahtar var + değer taşır** | **Oluşturma anında** kullanıcının o-anki bilgisi `data`'ya **kopyalanır + dondurulur** ("o anki departman/unvan"). |
| `live` | **Anahtar `data`'da HİÇ bulunmaz** | `data`'ya **yazılmaz** (anahtar dahi konmaz); okurken **User**'dan **güncel** getirilir — kullanıcı departmanı sonradan değişirse yeni değer görünür. Bu, "anahtar-her-zaman-bulunur" kuralının `text`'teki gibi **istisnasıdır** (değer okuma-anı join/referansla gelir, saklanmaz). |

Şekil, getirilen bilgiye göre (`snapshot`'ta `data`'da; `live`'da okuma sonucunda):
- **Skaler** (ad/e-posta): `string`
```json
{ "creatorDept": "Satınalma" }
```
- **Etiketli** (kod+ad taşıyan bilgi, ör. departman kodu): `LabeledValue` ([`labeled-value.md`](./labeled-value.md))
- **Kullanıcıya atıf yapan alt-değer** (ör. **yönetici**): `string`/`LabeledValue` **değil**, kullanıcı-referans konvansiyonuyla **`{ userId, nameSurname }`** (id + ad-soyad birlikte; → [`index.md`](./index.md) "Kullanıcı-referans konvansiyonu", Q11/Q13).
```json
{ "creatorManager": { "userId": 42, "nameSurname": "Ayşe Yılmaz" } }
```
- **Boş değer** (bilgi bulunamıyorsa — ör. departmansız/yöneticisiz kullanıcı): `data`'da anahtar **`null`** taşır (skaler boş-değer konvansiyonu). *(Yalnız `snapshot`'ta geçerli; `live`'da anahtar zaten bulunmaz.)*

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
- `userInfoValue` = hangi kullanıcı bilgisi (ad/e-posta/departman/unvan/yönetici…). **Yönetici** gibi kullanıcıya atıf yapan bir alt-değer, `{ userId, nameSurname }` konvansiyonuyla tutulur (bkz. §1).

*Oluşturma: 2026-08-06.*
