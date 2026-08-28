# Enum — OrganizationParameter

> **Kullanan model:** [`../service-settings/jsonTemplateModels/business-rule/data-source/fill-data-source-parameter.md`](../service-settings/jsonTemplateModels/business-rule/data-source/fill-data-source-parameter.md) — alan `parameter`
> **Amaç:** `fillDataSource` (`organizationData`/`userData`) kaynağında, bir kurum/kullanıcı kaydından **hangi alanın okunup** filtreye sokulacağını belirler.

## Nedir?
Kurum master-verisi ya da kullanıcı verisi listesi doldurulurken, kayıtları **süzmek** için o kayıttan okunacak alanı seçer.
Örneğin *"Masraf merkezi listesini, formda seçili **şirketin** masraf merkezleriyle doldur"* → parametre `company`.

## Değerler
| Değer | Kayıttan okunan |
|---|---|
| `company` | Şirket kodu. |
| `name` | Ad / tanım. |
| `code` | Kod. |
| `userCode` | Kullanıcı kodu. |
| `additionalQualification` | Ek nitelik değeri (**hangi** nitelik → `fill-data-source-parameter.md` `additionalQualificationCode`). |
| `professionCode` | Unvan kodu. |

## Notlar
- Her `OrganizationDataSourceType` yalnız **belirli** parametreleri kabul eder (→ [`organization-data-source-type.md`](./organization-data-source-type.md) "Seçilebilir filtreler").

*Oluşturma: 2026-08-26.*
