# DTO — FillDataSourceUser

> **Tür:** DTO — **DB tablosu değildir.** `fillDataSource` aksiyon konfiginde (`fillDataSourceType == userData`),
> `BusinessRule.configuration` **JSONB** gövdesinde iç-içe yaşar.
> **Aile / davranış:** [`index.md`](../index.md) · [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3

## Nedir?
Bir seçim alanını **oturum kullanıcısının** verisinden (kredi kartı / şirket / masraf merkezi) dolduran kaynağın ayarı.
Yapısı `FillDataSourceOrganization` ile aynıdır; yalnız kaynak **kullanıcıya özeldir**.

> **Örnek senaryo:** *"Kart alanını, oturum kullanıcısının aktif kredi kartlarıyla doldur."*

## Alanlar
| Alan | Tip | Zorunlu | Açıklama |
|---|---|:---:|---|
| `userDataSourceType` | UserDataSourceType | ✔ | Kullanıcının hangi verisi (`creditCards`/`companies`/`costCenters` → [`../../../../enums/user-data-source-type.md`](../../../../enums/user-data-source-type.md)). |
| `subTextType` | SubTextType? | — | Liste öğelerinin **alt metni** (→ [`../../../../enums/sub-text-type.md`](../../../../enums/sub-text-type.md)). |
| `parameters` | List\<FillDataSourceParameter\> | — | Satır **filtreleri** (→ [`fill-data-source-parameter.md`](./fill-data-source-parameter.md)); boşsa tüm kayıtlar. |

## Örnek (JSON)
```jsonc
{
  "userDataSourceType": "creditCards",
  "subTextType": "code"
}
```

## Nasıl çalışır
- `creditCards`: yalnız **`active`** kartlar; **tek kart** varsa veya bir kart **seçili** işaretliyse otomatik seçili gelir.
- `parameters` verilirse kayıtlar `FillDataSourceParameter` ile süzülür (kaynak kullanıcının verisi olsa da aynı filtre modeli).

## İlişkili
- Aksiyon konfigi: [`fill-data-source.md`](../actions/fill-data-source.md) · organizasyon kaynağı: [`fill-data-source-organization.md`](./fill-data-source-organization.md)

## Notlar
- Eski adı `PropertyDataSourceFromUserDataDto`. Kaynak, **oturum kullanıcısına** özeldir (organizasyon geneli değil — o `organizationData`).

*Oluşturma: 2026-08-26.*
