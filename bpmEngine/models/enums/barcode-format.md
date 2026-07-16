# Enum — BarcodeFormat

> **Kullanan model:** [`property.md`](../service-settings/property.md) — alan `barcodeFormat` (Barcode), tip **BarcodeFormat**
> **Amaç:** Barcode kontrolünün **tanıyacağı/tarayacağı barkod biçimini** belirler.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `aztec` | Aztec | 2B Aztec kodu. |
| `code39` | Code 39 | 1B Code 39 barkodu. |
| `code93` | Code 93 | 1B Code 93 barkodu. |
| `ean8` | EAN-8 | 8 haneli EAN ürün kodu. |
| `ean13` | EAN-13 | 13 haneli EAN ürün kodu. |
| `code128` | Code 128 | 1B Code 128 barkodu (yüksek yoğunluk). |
| `dataMatrix` | Data Matrix | 2B Data Matrix kodu. |
| `qr` | QR | 2B QR kodu. |
| `interleaved2of5` | Interleaved 2 of 5 | 1B ITF barkodu. |
| `pdf417` | PDF417 | 2B PDF417 kodu. |

## Notlar
- **Kaynak:** current Flovo `BarcodeFormat` enum'undan alındı →
  [`../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md`](../../research/current-flovo-bpm-engine/step-type-settings-and-enums.md) §6.
  (Önceki placeholder — "netleşecek" — kapandı.)

*Oluşturma: 2026-07-16.*
