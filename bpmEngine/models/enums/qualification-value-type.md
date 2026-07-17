# Enum — QualificationValueType

> **Kullanan model:** [`additional-qualification.md`](../organization-settings/additional-qualification.md) — alan `valueType`, tip **QualificationValueType**
> **Amaç:** Ek niteliğin **değer tipini** belirler; değerin `...QualificationValue` modelinde **hangi typed sütuna** yazılacağını seçer.

## Değerler
| Index | Değer | Depolanan sütun | Ne için |
|---|---|---|---|
| 0 | `string` | `stringValue` (string) | Serbest metin nitelik. |
| 1 | `double` | `doubleValue` (double) | Sayısal nitelik. |
| 2 | `dateTime` | `datetimeValue` (datetime) | Tarih/zaman nitelik. |
| 3 | `combobox` | `comboboxItemId` + kopya `comboboxTranslationCode` / `comboboxDefinition` | Önceden tanımlı seçeneklerden seçim (→ `QualificationItem`). |

## Notlar
- **⚠️ Alan adı çakışması:** Bu enum `AdditionalQualification.valueType`'tır (**QualificationValueType**); süreç adımı **Değer Atama**'daki `valueType` ise [`value-assign-type.md`](./value-assign-type.md)'dir (**ValueAssignType** — farklı enum).

*Oluşturma: 2026-07-10.*
