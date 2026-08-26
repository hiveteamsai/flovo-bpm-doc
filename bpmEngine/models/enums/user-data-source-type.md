# Enum — UserDataSourceType

> **Kullanan model:** [`../service-settings/dto/business-rule/data-source/fill-data-source-user.md`](../service-settings/dto/business-rule/data-source/fill-data-source-user.md) — alan `userDataSourceType`
> **Amaç:** İş kuralı `fillDataSource` **`userData`** kaynağında, **oturum kullanıcısının** hangi verisinin listeleneceğini belirler.
> **Davranış/kullanım:** → [`../../service-settings/business-rule.md`](../../service-settings/business-rule.md) §3

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `creditCards` | Kullanıcının kredi kartları. | Kart seçimi. `active` kartlar; **tek kart** varsa veya bir kart **seçili** işaretliyse otomatik seçilir. |
| `companies` | Kullanıcının şirketleri. | Şirket seçimi. |
| `costCenters` | Kullanıcının masraf merkezleri. | Masraf merkezi seçimi. |

## Notlar
- Kaynak, **oturum kullanıcısına** özeldir (organizasyon geneli değil — o `organizationData`).

*Oluşturma: 2026-08-26.*
