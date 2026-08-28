# Enum — PropertyAttributeType

> **Kullanan model:** [`../service-settings/jsonTemplateModels/business-rule/actions/assign-value-to-property-attribute.md`](../service-settings/jsonTemplateModels/business-rule/actions/assign-value-to-property-attribute.md) — alan `propertyAttributeType`
> **Amaç:** İş kuralı **`assignValueToPropertyAttribute`** aksiyonunun, bir alanın **hangi meta-özniteliğine** değer yazacağını belirler.
> **Davranış/kullanım:** → [`../../service-settings/business-rule.md`](../../service-settings/business-rule.md) §3

> ⚠️ **Bu enum kontrol tipi DEĞİLDİR.** Alanın **kontrol tipi** → [`property-type.md`](./property-type.md) (**PropertyType**). Bu enum,
> alanın **değerine değil**, bir **öznitelik/metadata**'sına (ör. seçilebilir tarih aralığı, yardımcı metin) yazan aksiyonun hedefidir.

## Değerler
| Değer | Anlam | Geçerli kontrol tipi |
|---|---|---|
| `minDate` | Seçilebilir **minimum tarih**. | `datepicker` |
| `maxDate` | Seçilebilir **maksimum tarih**. | `datepicker` |
| `helperText` | Alanın **yardımcı metni**. | Tüm alanlar |
| `sideText` | Alanın **yan metni** (birim/etiket). | `textbox` · `numericTextbox` |
| `addNewEnabled` | **Yeni satır ekleme** izni. | `formList` |

## Notlar
- Örnek: `BITIS_TARIHI` alanının `minDate` özniteliğine `#BASLANGIC_TARIHI` değerini yazmak → bitiş, başlangıçtan önce seçilemez.
- **Eski `IsActiveKkegAttachment`** (KKEG / masraf-vergi kavramı) **taşınmadı** — yeni motorda masraf çekirdek modeli yok.

*Oluşturma: 2026-08-26.*
