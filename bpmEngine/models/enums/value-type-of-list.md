# Enum — ValueTypeOfList

> **Kullanan model:** [`../service-settings/dto/business-rule/shared/business-rule-condition-compare-value.md`](../service-settings/dto/business-rule/shared/business-rule-condition-compare-value.md) — alan `valueTypeOfList`
> **Amaç:** Bir koşul karşılaştırmasında, **liste / çoklu-değer** üreten bir kontrolden **hangi alanın** okunacağını belirler.

## Nedir?
Bazı kontroller tek bir skaler yerine yapılı/çoklu değer üretir. Koşul tarafı bu tür bir alanı okuyorsa, bu enum
değerin **hangi parçasının** karşılaştırmaya gireceğini seçer.

## Değerler
| Değer | Okunan |
|---|---|
| `defaultValue` | Varsayılan değer. |
| `value` | Ham değer. |
| `display` | Görünen metin. |

## Notlar
- **Opsiyoneldir**; yalnız liste-tipli kontrollerde anlamlıdır, aksi halde alanın normal değeri okunur.
- **Kapsam-dışı bırakılan (masraf çekirdek modeli yok):** eski `expenseTypeId` · `expenseTypeName` · `categoryCode` (GroupByTax masraf kontrolüne özeldi) **taşınmadı** → [`../../todo.md`](../../todo.md) ("Kapsam-dışı varlıklar").

*Oluşturma: 2026-08-26.*
