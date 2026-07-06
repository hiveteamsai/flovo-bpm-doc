# Model — RelatedForm (formlar arası ilişki)

> **Durum:** 🟢 TANIMLI
> **Eski karşılığı:** yok — **yeni model**.
> **Amaç:** Bir formu **başka bir formla ilişkilendirmek**. Bir kayıt birden çok forma bağlı olabilir; ilişki hangi
> **property** üzerinden kurulduğunu da taşır.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | İlişki kaydı ID'si. |
| `formId` | int | FK → Form.id | İlişkinin **işaret ettiği** (bağlanan) form. |
| `relatedFormId` | int | FK → Form.id | İlişkiyi **kuran** property'yi (`relatedPropertyId`) **içeren** form. |
| `relatedPropertyId` | int | FK → Property.id | İlişkiyi kuran property (Form List / Combobox). **`relatedFormId`'nin formu/servisi içinde yer alır.** |

## Alan semantiği (kural)
> **`relatedPropertyId`, `relatedFormId` id'li formun içinde yer alır.** Yani ilişkiyi kuran alan (Form List / Combobox),
> `relatedFormId`'nin **servisine** ait bir property'dir; bu property `formId`'deki formu işaret eder.
>
> Değişmez (invariant): `Property(relatedPropertyId).serviceId == Form(relatedFormId).serviceId`.

## Örnek (3 servis: **masraf formu** · **masraf** · **seyahat**)
- **masraf formu** içinde bir **Form List** alanı var; bu listeye **masraf** servisinin formları eklenir.
- **masraf** servisinde **seyahat** seçilen bir **Combobox** var.

| İlişkilendirme | `formId` | `relatedFormId` | `relatedPropertyId` | (property nerede) |
|---|---|---|---|---|
| masraf formu ↔ masraf | **masraf** id | **masraf formu** id | **Form List** id | Form List → *masraf formu* içinde |
| masraf ↔ seyahat | **seyahat** id | **masraf** id | **Combobox** id | Combobox → *masraf* içinde |

> Her iki satırda da `relatedPropertyId`, `relatedFormId`'nin formu içindeki alandır ve `formId`'deki formu işaret eder.

## İlişkiler
- **N – 1** → `Form` (`formId` = işaret edilen, `relatedFormId` = property'yi içeren), `Property` (`relatedPropertyId`).
- Form ↔ Form **N–N** köprü tablosu (property boyutuyla). Tek bir form birden çok `RelatedForm` kaydına bağlı olabilir
  (ör. bir masraf; masraf formuna, seyahate, avansa ayrı ayrı bağlanabilir).

*Oluşturma: 2026-07-06.*
