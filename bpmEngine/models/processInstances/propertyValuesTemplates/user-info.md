# Değer Şablonu — `userInfo` (User Info)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `userInfo` (salt-okunur kullanıcı metadata) değerinin **`InstanceValue.data` içindeki şekli** + fihrist yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.16 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md) · **yansıma:** [`../../enums/reflection-mode.md`](../../enums/reflection-mode.md) · **değer modeli:** [`../instance-attr.md`](../instance-attr.md).

## 1. JSONB değer şekli — `data["<code>"]`
**Snapshot (A) yansıma** — `userInfoValue` ile seçilen kullanıcı bilgisi **yazım anında `data`'ya kopyalanır ve dondurulur** ("o anki departman/unvan"). Şekil, getirilen bilgiye göre:

- **Skaler** (ad/e-posta): `string`
```json
{ "creatorDept": "Satınalma" }
```
- **Etiketli** (kod+ad taşıyan bilgi, ör. departman kodu): `LabeledValue` ([`labeled-value.md`](./labeled-value.md))

- Girdi değildir; kullanıcı düzenleyemez.

## 2. Projeksiyon — `projectToAttr=true`
| Şekil | Hedef | Kolon |
|---|---|---|
| Skaler | **InstanceAttr** | `textValue` (normal alan gibi) |
| Etiketli | **InstanceAttr** | `textValue`=`value` · `display` · `translationCode` |

## 3. Notlar
- **Snapshot** olduğu için sonradan kullanıcı departmanı değişse bile kayıt **eski değeri** korur (audit-dostu, ucuz) — Flow Info'nun **canlı** aksine.
- `userInfoValue` = hangi kullanıcı bilgisi (ad/e-posta/departman/unvan/yönetici…).

*Oluşturma: 2026-08-06.*
