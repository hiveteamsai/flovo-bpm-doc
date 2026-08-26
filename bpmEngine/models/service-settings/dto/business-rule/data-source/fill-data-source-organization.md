# DTO — FillDataSourceOrganization

> **Tür:** DTO — **DB tablosu değildir.** `fillDataSource` aksiyon konfiginde (`fillDataSourceType == organizationData`),
> `BusinessRule.configuration` **JSONB** gövdesinde iç-içe yaşar.
> **Aile / davranış:** [`index.md`](../index.md) · [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3

## Nedir?
Bir seçim alanını **organizasyon master-verisinden** (departman, şirket, masraf merkezi, kullanıcı…) dolduran kaynağın ayarı.
Hangi veri (`organizationDataSourceType`), öğe alt-metni (`subTextType`) ve satır filtreleri (`parameters`) burada tanımlanır.

> **Örnek senaryo:** *"Masraf merkezi combosunu, formda seçili şirketin masraf merkezleriyle doldur; her öğenin altında kodu görünsün."*

## Alanlar
| Alan | Tip | Zorunlu | Açıklama |
|---|---|:---:|---|
| `organizationDataSourceType` | OrganizationDataSourceType | ✔ | Kaynak kurum verisi (→ [`../../../../enums/organization-data-source-type.md`](../../../../enums/organization-data-source-type.md)). |
| `subTextType` | SubTextType? | — | Liste öğelerinin **alt metni** (→ [`../../../../enums/sub-text-type.md`](../../../../enums/sub-text-type.md)). |
| `parameters` | List\<FillDataSourceParameter\> | — | Satır **filtreleri** (→ [`fill-data-source-parameter.md`](./fill-data-source-parameter.md)); boşsa tüm kayıtlar. |
| `companyId` | int? | — | Yalnız **`users`** kaynağında şirket filtresi (yalnız o şirkete bağlı kullanıcılar). |

## Örnek (JSON)
```jsonc
{
  "organizationDataSourceType": "costCenters",
  "subTextType": "code",
  "parameters": [
    { "parameter": "company", "value": { "valueAssignType": "propertyValue", "propertyValue": { "propertyId": 12 } } }
  ]
}
```
> `#SIRKET`'e (property 12) bağlı masraf merkezleri; öğe alt-metni = kod.

## Nasıl çalışır
- Kaynak listesi çekilir, `parameters` ile süzülür (tüm parametreler sağlanmalı), öğeler `{value, display, subText}` olarak üretilir.
- Kabul edilen filtreler `organizationDataSourceType`'a göre kısıtlıdır (→ enum "Seçilebilir filtreler").

## İlişkili
- Aksiyon konfigi: [`fill-data-source.md`](../actions/fill-data-source.md) · kullanıcı kaynağı: [`fill-data-source-user.md`](./fill-data-source-user.md)

## Notlar
- Eski adı `PropertyDataSourceFromOrganizationDataDto`. `ExpenseType`/`ExpenseCategory` kaynakları **taşınmadı** (masraf çekirdek modeli yok).

*Oluşturma: 2026-08-26.*
