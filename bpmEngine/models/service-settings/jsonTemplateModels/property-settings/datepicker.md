# Property Settings — `datepicker` (Datepicker)

> **propertyType:** `datepicker` · **Kontrol:** takvimden **tek bir gün** seçtiren alan; değer sadece-tarih (saat taşımaz).
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/datepicker.md`](../../../processInstances/propertyValuesTemplates/datepicker.md) (ISO `YYYY-MM-DD` `string`, saat **yok**) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.4 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `minimumDate` | string? (`YYYY-MM-DD`) | hayır | `null` | Seçilebilir **en erken takvim günü**; takvimde bundan öncesi kapatılır (geçmiş/gelecek sınırlama). `null` = alt sınır yok. Değer sadece-tarih olduğundan sınır da takvim günüdür (saat/tz yok → değer şablonu §1). |
| `maximumDate` | string? (`YYYY-MM-DD`) | hayır | `null` | Seçilebilir **en geç takvim günü**; sonrası kapatılır. `null` = üst sınır yok. Verilirse `maximumDate ≥ minimumDate`. |
| `setAsToday` | bool | hayır | `false` | Alan ilk açıldığında **bugünün tarihini** varsayılan olarak yazsın mı — sabit tasarım-zamanı `defaultValue` yerine **çalışma-anı "bugün"** koyar. |
| `headerText` | string? | hayır | `null` | Takvim **pop-up başlığı** — yalnız pop-up açan alanlarda görünür (§2.2 notu). |

## 2. Çekirdek kolonda (settings'e girmez)
- `defaultValue` (string, `YYYY-MM-DD`) — tasarım-zamanı **başlangıç tarihi** (§1.3). `setAsToday=true` iken çalışma-anı "bugün" bunu geçersiz kılar.
- `format` (string) — takvim/gösterim **formatı** (ör. `dd.MM.yyyy`); yalnız **sunumdadır**, saklanan değer kanonik `YYYY-MM-DD`'dir (değer şablonu §1). `hint`/`helperText` yardım metinleri (§1.2).
- Değer-saklama/projeksiyon metadata'sı: `savePropertyToDb` · `projectToAttr` (`true` → **InstanceAttr.dateValue**, takvim tarihi; aralık/sıralama btree) · `saveChangeLog` (§1.3).

## 3. Profil-bazlı
- Yok (`datepicker` için profil-özel ayar tanımlı değil; görünür/düzenlenebilir/zorunlu genel profil alanlarıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. JSON Schema
```json
{
  "$id": "property-settings/datepicker",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "minimumDate": { "type": ["string", "null"], "format": "date", "default": null },
    "maximumDate": { "type": ["string", "null"], "format": "date", "default": null },
    "setAsToday":  { "type": "boolean", "default": false },
    "headerText":  { "type": ["string", "null"], "default": null }
  }
}
```
> Not: `maximumDate ≥ minimumDate` çapraz-kısıtı ve `setAsToday=true` ↔ `defaultValue` etkileşimi JSON Schema ile ifade edilemez → **uygulama-katmanı** doğrulaması. `defaultValue`/`format` **çekirdek kolon** olduğundan bu şemada **yer almaz**.

## 5. Örnek
```json
{ "minimumDate": "2026-01-01", "maximumDate": null, "setAsToday": true, "headerText": "Fatura tarihi seçin" }
```

*Oluşturma: 2026-08-28.*
