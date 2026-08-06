# Değer Şablonu — `flowInfo` (Flow Info)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `flowInfo` (salt-okunur akış metadata) değerinin **`InstanceValue.data` içindeki şekli** + fihrist yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.14 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **kaynak:** [`../instance.md`](../instance.md) · **yansıma:** [`../../enums/reflection-mode.md`](../../enums/reflection-mode.md).

## 1. JSONB değer şekli — `data["<code>"]`
**Canlı (B) yansıma — `data`'ya YAZILMAZ.** Değer, `flowInfoValue` ile seçilen akış bilgisidir ve **`Instance` kolonlarından / join'den** okunur (kopya tutulmaz):

| `flowInfoValue` | Kaynak |
|---|---|
| durum (status) | `Instance.statusId` (→ `Status`) |
| oluşturulma tarihi | `Instance.createdDate` |
| oluşturan kullanıcı | `Instance.creatorUserId` (→ `User`) |

- Girdi değildir; **sürekli değişebilir** (özellikle status).

## 2. Projeksiyon — `projectToAttr`
- **Fihrist üretilmez** (değer `data`'da yok). Rapor/filtre doğrudan **`Instance` kolonlarından**:
  - durum filtresi → `Instance.statusId` (indeksli kolon, `InstanceAttr` değil).
  - tarih/oluşturan → `Instance.createdDate` / `creatorUserId`.

## 3. Notlar
- **Neden canlı + kolon:** status sık değişir; `data`'ya yazılsa her değişimde tüm `InstanceValue` yeniden yazılır (MVCC) + rapor bayatlar. Bu yüzden `Instance.statusId` **ayrı indeksli kolondur** (→ [`../instance.md`](../instance.md)).
- Kullanıcı bilgisi karşılığı **snapshot**'tır → [`user-info.md`](./user-info.md) (Flow Info canlı, User Info dondurulmuş).

*Oluşturma: 2026-08-06.*
