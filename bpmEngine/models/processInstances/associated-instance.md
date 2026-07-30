# Model — AssociatedInstance (formlar arası ilişki)

> **Durum:** 🟢 TANIMLI
> **Yeni model.**
> **Amaç:** Bir formu **başka bir formla ilişkilendirmek**. Bir kayıt birden çok forma bağlı olabilir; ilişki hangi
> **property** üzerinden kurulduğunu da taşır.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | İlişki kaydı ID'si. |
| `instanceId` | int | FK → Instance.id | İlişkinin **işaret ettiği** (bağlanan) form. |
| `associatedInstanceId` | int | FK → Instance.id | İlişkiyi **kuran** property'yi (`associatedPropertyId`) **içeren** form. |
| `associatedPropertyId` | int | FK → Property.id | İlişkiyi kuran property (Form List / Combobox). **`associatedInstanceId`'nin formu/servisi içinde yer alır.** |

## Alan semantiği (kural)
> **`associatedPropertyId`, `associatedInstanceId` id'li formun içinde yer alır.** Yani ilişkiyi kuran alan (Form List / Combobox),
> `associatedInstanceId`'nin **servisine** ait bir property'dir; bu property `instanceId`'deki formu işaret eder.
>
> Değişmez (invariant): `Property(associatedPropertyId).serviceId == Instance(associatedInstanceId).serviceId`.

## Örnek (3 servis: **masraf formu** · **masraf** · **seyahat**)
- **masraf formu** içinde bir **Form List** alanı var; bu listeye **masraf** servisinin formları eklenir.
- **masraf** servisinde **seyahat** seçilen bir **Combobox** var.

| İlişkilendirme | `instanceId` | `associatedInstanceId` | `associatedPropertyId` | (property nerede) |
|---|---|---|---|---|
| masraf formu ↔ masraf | **masraf** id | **masraf formu** id | **Form List** id | Form List → *masraf formu* içinde |
| masraf ↔ seyahat | **seyahat** id | **masraf** id | **Combobox** id | Combobox → *masraf* içinde |

> Her iki satırda da `associatedPropertyId`, `associatedInstanceId`'nin formu içindeki alandır ve `instanceId`'deki formu işaret eder.

> **İlişki kaydı ne zaman düşer?**
> - **Combobox** için: yalnız property'nin `isAssociatedCombobox=true` (ve `associatedServiceId` dolu) olması hâlinde —
>   alanın `propertyValue`'su değiştikçe, seçilen instance için bir `AssociatedInstance` kaydı yazılır
>   (→ [`../service-settings/property.md`](../service-settings/property.md) §2 · `../../service-settings/properties.md` §3.3).
> - **Form List** için: ilişki, alt-servis kaydının listeye **eklenmesiyle** kurulur.

> **Ters arama tüketicisi — Üst Form Kullanıcı adımı (§3.22):** Bir alt-servis kaydı, üst formunu bu tablodan **ters
> aramayla** bulur: `instanceId = <alt-servis kaydı>` **ve** `associatedPropertyId = <ilişki alanı>` → **`associatedInstanceId`
> = üst form**. Böylece alt-servis, üst formun güncel atananlarını/görünümünü devralır
> (→ [`../../service-settings/process-step.md`](../../service-settings/process-step.md) §3.22).

> **Yazım-yolu tüketicisi — ServiceTrigger (`whenAddedAssociate`/`whenRemoveAssociate`):** Bu tabloya **AddOrUpdate/silme**
> yapılırken, **`associatedPropertyId == ServiceTrigger.targetPropertyId`** olan (ve tipi eşleşen aktif) trigger'lar taranıp
> ateşlenir; **parametre kaynağı = `associatedInstanceId`** (ilişki alanını içeren üst form), **yürütme hedefi = `instanceId`**
> (işaret edilen form; `targetService`'teki **mevcut** instance — alt süreç bunun üzerinde koşar, yeni instance oluşmaz).
> Tespit **DB güncelleme katmanında, çekirdek (core)** olarak yapılır — böylece ilişki kuran her yerde ayrıca tekrarlanmaz
> (→ [`../service-settings/service-trigger.md`](../service-settings/service-trigger.md)).

## İlişkiler
- **N – 1** → `Instance` (`instanceId` = işaret edilen, `associatedInstanceId` = property'yi içeren), `Property` (`associatedPropertyId`).
- Instance ↔ Instance **N–N** köprü tablosu (property boyutuyla). Tek bir Instance birden çok `AssociatedInstance` kaydına bağlı olabilir
  (ör. bir masraf; masraf formuna, seyahate, avansa ayrı ayrı bağlanabilir).

*Oluşturma: 2026-07-06.*
