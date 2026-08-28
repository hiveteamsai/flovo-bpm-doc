# DTO — FillDataSource (aksiyon konfigi)

> **Tür:** DTO — **DB tablosu değildir.** `businessRuleActionType == fillDataSource` iken `BusinessRule.configuration` **JSONB** şeklidir.
> **Aile / davranış:** [`index.md`](../index.md) · [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3 · kaynak tipi → [`../../../../enums/fill-data-source-type.md`](../../../../enums/fill-data-source-type.md)

## Nedir?
Bir seçim alanının (combobox / radiobuttonList / Form List) **veri kaynağını** koşula göre **çalışma-zamanında** doldurur.
`fillDataSourceType` **ayrımlayıcısı** kaynağı seçer; yalnız o kaynağın **payload**'ı dolu olur (**discriminated union / oneOf**).

> **Örnek senaryo:** *"ŞİRKET seçilince MASRAF_MERKEZİ combosu, o şirketin masraf merkezleriyle dolsun."*

## Yapı (ayrımlayıcı + oneOf payload)
| Alan | Tip | Zorunlu | Açıklama |
|---|---|:---:|---|
| `propertyId` | int (FK → Property) | ✔ | Veri kaynağı **doldurulacak** alan (ortak; ayrımlayıcı dışı). |
| `fillDataSourceType` | FillDataSourceType | ✔ | **Ayrımlayıcı** — dolu payload'ı belirler. |
| `organizationData` | FillDataSourceOrganization | oneOf | Kurum master-verisi (→ [`fill-data-source-organization.md`](../data-source/fill-data-source-organization.md)). |
| `userData` | FillDataSourceUser | oneOf | Oturum kullanıcısının verisi (→ [`fill-data-source-user.md`](../data-source/fill-data-source-user.md)). |
| `serviceInstances` | AssignValueFromDataSet | oneOf | Başka servisin instance'ları (→ [`assign-value-from-dataset.md`](../data-source/assign-value-from-dataset.md)). |
| `httpRequest` | HTTP Request konfigi | oneOf | Dış-API — `process-step.md` HTTP Request altyapısı (→ [`../../../../../service-settings/process-step.md`](../../../../../service-settings/process-step.md) §3.2). |

> **oneOf kısıtı:** Yalnız `fillDataSourceType`'a karşılık gelen payload dolu olur.

## Örnek (JSON — organizationData)
```jsonc
{
  "propertyId": 30,                         // MASRAF_MERKEZI combosu
  "fillDataSourceType": "organizationData",
  "organizationData": {
    "organizationDataSourceType": "costCenters",
    "subTextType": "code",
    "parameters": [
      { "parameter": "company", "value": { "valueAssignType": "propertyValue", "propertyValue": { "propertyId": 12 } } }
    ]
  }
}
```

## Nasıl çalışır
- Koşul sağlanır **ve** `propertyId` doluysa çalışır; kaynak `fillDataSourceType` payload'ından çözülüp alana yazılır.
- Kaynak gerçekten değiştiyse **zincirleme** yeni bir kural turu tetiklenebilir.

## İlişkili / Notlar
- **SOLID:** `AssignValue` ile aynı discriminated-union konvansiyonu (ISP/OCP). **`companyId`** (users şirket filtresi) `FillDataSource`'tan çıkarılıp ait olduğu yere — `FillDataSourceOrganization`'a — taşındı (SRP).
- **Eski `FromEba` kaldırıldı** (→ `httpRequest`); eski **`FromDataSet`** → **`serviceInstances`**.

*Oluşturma: 2026-08-26 · Güncelleme: 2026-08-26 (SOLID — discriminated union; companyId→organizationData).*
