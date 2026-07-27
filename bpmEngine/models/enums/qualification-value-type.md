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
- **Alan adı ayrıştırıldı (v0.18):** Bu enum `AdditionalQualification.`**`valueType`**'tır (**QualificationValueType**); süreç adımı **Değer Atama** alanı ise **`valueAssignType`** (tip **ValueAssignType** → [`value-assign-type.md`](./value-assign-type.md)). Alan adları **farklı** — çakışma yok.

*Oluşturma: 2026-07-10.*
