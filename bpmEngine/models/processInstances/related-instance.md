# Model — RelatedInstance (formlar arası ilişki)

> **Durum:** 🟢 TANIMLI
> **Eski karşılığı:** yok — **yeni model**.
> **Amaç:** Bir formu **başka bir formla ilişkilendirmek**. Bir kayıt birden çok forma bağlı olabilir; ilişki hangi
> **property** üzerinden kurulduğunu da taşır.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | İlişki kaydı ID'si. |
| `instanceId` | int | FK → Instance.id | İlişkinin **işaret ettiği** (bağlanan) form. |
| `relatedInstanceId` | int | FK → Instance.id | İlişkiyi **kuran** property'yi (`relatedPropertyId`) **içeren** form. |
| `relatedPropertyId` | int | FK → Property.id | İlişkiyi kuran property (Form List / Combobox). **`relatedInstanceId`'nin formu/servisi içinde yer alır.** |

## Alan semantiği (kural)
> **`relatedPropertyId`, `relatedInstanceId` id'li formun içinde yer alır.** Yani ilişkiyi kuran alan (Form List / Combobox),
> `relatedInstanceId`'nin **servisine** ait bir property'dir; bu property `instanceId`'deki formu işaret eder.
>
> Değişmez (invariant): `Property(relatedPropertyId).serviceId == Instance(relatedInstanceId).serviceId`.

## Örnek (3 servis: **masraf formu** · **masraf** · **seyahat**)
- **masraf formu** içinde bir **Form List** alanı var; bu listeye **masraf** servisinin formları eklenir.
- **masraf** servisinde **seyahat** seçilen bir **Combobox** var.

| İlişkilendirme | `instanceId` | `relatedInstanceId` | `relatedPropertyId` | (property nerede) |
|---|---|---|---|---|
| masraf formu ↔ masraf | **masraf** id | **masraf formu** id | **Form List** id | Form List → *masraf formu* içinde |
| masraf ↔ seyahat | **seyahat** id | **masraf** id | **Combobox** id | Combobox → *masraf* içinde |

> Her iki satırda da `relatedPropertyId`, `relatedInstanceId`'nin formu içindeki alandır ve `instanceId`'deki formu işaret eder.

## İlişkiler
- **N – 1** → `Instance` (`instanceId` = işaret edilen, `relatedInstanceId` = property'yi içeren), `Property` (`relatedPropertyId`).
- Instance ↔ Instance **N–N** köprü tablosu (property boyutuyla). Tek bir Instance birden çok `RelatedInstance` kaydına bağlı olabilir
  (ör. bir masraf; masraf formuna, seyahate, avansa ayrı ayrı bağlanabilir).

*Oluşturma: 2026-07-06.*
