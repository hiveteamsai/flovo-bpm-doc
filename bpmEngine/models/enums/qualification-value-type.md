# Enum — QualificationValueType (AdditionalQualification)

> **Kullanan model:** [`additional-qualification.md`](../organization-settings/additional-qualification.md) (`valueType`)
> **Amaç:** Ek niteliğin **değer tipini** belirler; değerin `...QualificationValue` modelinde **hangi typed sütuna** yazılacağını seçer.

## Değerler
| Index | Değer | Depolanan sütun | Ne için |
|---|---|---|---|
| 0 | `String` | `stringValue` (string) | Serbest metin nitelik. |
| 1 | `Double` | `doubleValue` (double) | Sayısal nitelik. |
| 2 | `DateTime` | `datetimeValue` (datetime) | Tarih/zaman nitelik. |
| 3 | `Combobox` | `comboboxItemId` + kopya `comboboxCode` / `comboboxDefinition` | Önceden tanımlı seçeneklerden seçim (→ `QualificationItem`). |

## Notlar
- **⚠️ Alan adı çakışması:** Bu enum `AdditionalQualification.valueType`'tır; süreç adımı **Değer Atama**'daki `valueType` ise [`value-assign-type.md`](./value-assign-type.md)'dir (farklı enum).

*Oluşturma: 2026-07-10.*
