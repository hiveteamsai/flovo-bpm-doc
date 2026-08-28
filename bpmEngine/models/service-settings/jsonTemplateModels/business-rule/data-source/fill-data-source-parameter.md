# DTO — FillDataSourceParameter

> **Tür:** DTO — **DB tablosu değildir.** `fillDataSource` `organizationData`/`userData` kaynağının içinde,
> `BusinessRule.configuration` **JSONB** gövdesinde iç-içe yaşar.
> **Aile / davranış:** [`index.md`](../index.md) · [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3

## Nedir?
Kurum ya da kullanıcı verisi listesi doldurulurken kayıtları **süzen tek filtre**. Kaynak kaydın bir alanını
(`OrganizationParameter`), formdan/sabitten çözülen bir değerle karşılaştırır.

> **Örnek senaryo:** *"Masraf merkezi listesini yalnız formdaki `#SIRKET` alanına eşit **şirket** kayıtlarıyla doldur."*
> → `parameter = company`, `value = #SIRKET`.

## Alanlar
| Alan | Tip | Zorunlu | Açıklama |
|---|---|:---:|---|
| `parameter` | OrganizationParameter | ✔ | Kayıttan okunacak filtre alanı (`company`/`name`/`code`/`userCode`/`additionalQualification`/`professionCode` → [`../../../../enums/organization-parameter.md`](../../../../enums/organization-parameter.md)). |
| `value` | AssignValue | ✔ | Karşılaştırılacak değer (formdan/sabitten → [`assign-value.md`](../shared/assign-value.md)). |
| `criterionType` | CriterionType? | — | Operatör (→ [`../../../../enums/criterion-type.md`](../../../../enums/criterion-type.md)); **`null` → `equals`**. |
| `changeToCompare` | bool | — | `true` ise operatörün **sol/sağ** tarafları yer değiştirir. |
| `additionalQualificationCode` | string? | — | `parameter == additionalQualification` iken **hangi** ek niteliğin okunacağı. |

## Örnek (JSON)
```jsonc
{
  "parameter": "company",
  "value": { "valueAssignType": "propertyValue", "propertyValue": { "propertyId": 12 } },  // #SIRKET
  "criterionType": null,          // → equals
  "changeToCompare": false
}
```

## Nasıl çalışır
- Bir kaynağın **tüm** parametreleri sağlanmalıdır (VE mantığı).
- Parametre listesi **boş** ise "filtre yok" → tüm kayıtlar listelenir.

## İlişkili
- Kaynak konfigleri: [`fill-data-source-organization.md`](./fill-data-source-organization.md) · [`fill-data-source-user.md`](./fill-data-source-user.md)

## Notlar
- Eski adı `FillDataSoruceOrganizationParameter` (yazım hatası + yalnız "Organization" çağrışımı) → yeni motorda **org ve user** kaynaklarının **ortak** parametresi: `FillDataSourceParameter`.

*Oluşturma: 2026-08-26.*
