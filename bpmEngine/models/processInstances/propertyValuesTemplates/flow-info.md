# Değer Şablonu — `flowInfo` (Flow Info)

> **Durum:** 🟢 OLGUN (v0.31)
> **Kapsam:** `flowInfo` (salt-okunur akış metadata) değerinin **`InstanceValue.data` içindeki şekli** + fihrist yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.14 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **kaynak:** [`../instance.md`](../instance.md) · **yansıma:** [`../../enums/reflection-mode.md`](../../enums/reflection-mode.md).

## 1. JSONB değer şekli — `data["<code>"]`
Değer, `flowInfoValue` ile seçilen akış bilgisidir. **Oluşturma-anı mı (dondurulmuş) yoksa güncel mi** gösterileceği
**`reflectionMode`** ile seçilir (→ [`../../enums/reflection-mode.md`](../../enums/reflection-mode.md)):

| `reflectionMode` | `data`'da anahtar/değer | Nasıl |
|---|---|---|
| `live` (**vars.**) | **Anahtar `data`'da HİÇ bulunmaz** | `data`'ya **yazılmaz** (anahtar dahi konmaz); **`Instance` kolonlarından / join'den** **güncel** okunur (kopya tutulmaz). "Anahtar-her-zaman-bulunur" kuralının `text`'teki gibi **istisnasıdır** (değer okuma-anı gelir, saklanmaz). |
| `snapshot` | **Anahtar var + değer taşır** | **Oluşturma anındaki** değer `data`'ya **kopyalanır + dondurulur** (ör. "başlangıç durumu"). |

**Kaynak/şekil** (`live`'da okuma kaynağı; `snapshot`'ta `data`'daki şekil):

| `flowInfoValue` | Kaynak (`live`) | Şekil (`snapshot`) |
|---|---|---|
| durum (status) | `Instance.statusId` (→ `Status`) | `LabeledValue` (status `value`+`display`+`translationCode`) |
| oluşturulma tarihi | `Instance.createdDate` | ISO tarih `string` |
| oluşturan kullanıcı | `Instance.creatorUserId` (→ `User`) | `{ userId, nameSurname }` (kullanıcı-referans konvansiyonu) |

- Girdi değildir. `live`'da **sürekli değişebilir** (özellikle status); `snapshot`'ta sabittir.
- **Boş değer** (bilgi bulunamıyorsa — ör. henüz atanmamış durum/oluşturan): `snapshot`'ta anahtar **`null`** taşır (skaler boş-değer konvansiyonu); `live`'da anahtar zaten `data`'da bulunmaz.

## 2. Projeksiyon — `projectToAttr`
| `reflectionMode` | Projeksiyon |
|---|---|
| `live` (**vars.**) | **Fihrist üretilmez** (değer `data`'da yok). Rapor/filtre doğrudan **`Instance` kolonlarından**: durum → `Instance.statusId` (indeksli kolon, `InstanceAttr` değil) · tarih/oluşturan → `Instance.createdDate`/`creatorUserId`. |
| `snapshot` | **InstanceAttr** — donmuş değerin tipiyle: status→`textValue`=`value`+`display`+`translationCode` · tarih→`dateValue` · kullanıcı→`numValue`=userId+`textValue`=nameSurname. |

## 3. Notlar
- **Neden `live` varsayılan + kolon:** status sık değişir; `data`'ya yazılsa her değişimde tüm `InstanceValue` yeniden yazılır (MVCC) + rapor bayatlar. Bu yüzden `Instance.statusId` **ayrı indeksli kolondur** (→ [`../instance.md`](../instance.md)). Güncel-durum gösterimi için `live` doğal seçimdir.
- **`snapshot`** yalnız "oluşturma-anı değerini dondur" gerektiğinde bilinçli seçilir (ör. başlangıç durumu/oluşturan denetimi). `createdDate`/`creatorUser` zaten değişmediğinden onlarda `live`↔`snapshot` farkı yoktur; fark esas **status**'ta anlamlıdır.
- **`materialized` geçerli değildir** (yalnız `parentProperty`).
- Kullanıcı-metadata karşılığı → [`user-info.md`](./user-info.md) (ikisi de aynı `reflectionMode` ile snapshot↔live seçer; varsayılanları farklı: userInfo `snapshot`, flowInfo `live`).

*Oluşturma: 2026-08-06.*
