# DTO — AssignValueFromDataSetParameter

> **Tür:** **DTO** — **DB tablosu değildir.** [`assign-value-from-dataset.md`](./assign-value-from-dataset.md) içindeki bir **satır filtresi**;
> `BusinessRule.configuration` **JSONB** gövdesinde iç-içe yaşar.
> **Amaç:** Kaynak servisin bir **kolonunu**, formdan/sabitten çözülen bir **değerle** karşılaştırarak kayıtları filtreler.

## Alanlar
| Alan | Tip | Ne için |
|---|---|---|
| `parameterPropertyId` | int (FK → Property) | Kaynak servisteki **filtre kolonu**. |
| `value` | AssignValue | Karşılaştırılacak **değer** (formdan / sabitten / hesaplamadan → [`assign-value.md`](../shared/assign-value.md)). |
| `criterionType` | CriterionType? | Operatör (→ [`../../../../enums/criterion-type.md`](../../../../enums/criterion-type.md)); **`null` → `equals`**. |
| `changeToCompare` | bool | `true` ise operatörün **sol/sağ** tarafları yer değiştirir (ör. "satır değeri, form değerini içersin"). |

## Notlar
- Bir sorgudaki **tüm** parametreler sağlanmalıdır (VE mantığı); parametre listesi **boş** ise "filtre yok" → tüm kayıtlar.

*Oluşturma: 2026-08-26.*
