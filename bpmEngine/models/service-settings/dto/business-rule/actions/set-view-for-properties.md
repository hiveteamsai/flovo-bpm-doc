# DTO — SetViewForProperties (aksiyon konfigi)

> **Tür:** DTO — **DB tablosu değildir.** `BusinessRule.configuration` **JSONB** gövdesinde yaşar.
> **Aktif olduğu tip:** `businessRuleActionType == setViewForProperties`.
> **Aile / davranış:** [`index.md`](../index.md) · [`../../../../../service-settings/business-rule.md`](../../../../../service-settings/business-rule.md) §3

## Nedir?
Bir kuralın koşulu **sağlandığında** (ya da **sağlanmadığında**) **bir veya birden çok alanın** görünürlüğünü,
düzenlenebilirliğini ve zorunluluğunu **anlık** değiştiren aksiyonun ayarıdır.

> **Örnek senaryo:** *"Talep tipi **Avans** ise AÇIKLAMA alanı **görünür + zorunlu** olsun; değilse **gizlensin**."*
> Tek kuralla birden çok alan yönetilebilir.

## Alanlar
| Alan | Tip | Zorunlu | Açıklama |
|---|---|:---:|---|
| `properties` | List\<SetViewForPropertyItem\> | ✔ | Görünümü yönetilecek alanların listesi (aşağıda). |

**`SetViewForPropertyItem`** — listedeki her alan için:

| Alan | Tip | Zorunlu | Açıklama |
|---|---|:---:|---|
| `propertyId` | int (FK → Property) | ✔ | Hedef alan. |
| `providedAppearance` | PropertyAppearance | ✔ | Koşul **sağlanınca** uygulanacak görünüm (`visible`/`enabled`/`required`). |
| `notProvidedAppearance` | PropertyAppearance | — | Koşul **sağlanmayınca** uygulanacak görünüm. |
| `notProvidedDeactive` | bool | — | `true` ise koşul sağlanmadığında alana **hiç dokunulmaz** (mevcut görünüm korunur). |

## Örnek (JSON)
```jsonc
{
  "properties": [
    {
      "propertyId": 42,                                              // AÇIKLAMA alanı
      "providedAppearance":    { "visible": true,  "enabled": true,  "required": true  },
      "notProvidedAppearance": { "visible": false, "enabled": false, "required": false },
      "notProvidedDeactive": false
    }
  ]
}
```
> Koşul sağlanınca AÇIKLAMA **görünür + zorunlu**; sağlanmayınca **gizli**.

## Nasıl çalışır
- **Koşul sağlandı** → her alana `providedAppearance` uygulanır.
- **Koşul sağlanmadı** → `notProvidedAppearance` uygulanır; ancak `notProvidedDeactive == true` ise alan **atlanır** (dokunulmaz).
- **Salt-okunur modda** `enabled` her durumda **`false`**'a zorlanır (görünürlük/zorunluluk kuraldan gelir; düzenlenebilirlik açılmaz).

## İlişkili
- Görünüm bayrakları → [`property-appearance.md`](../shared/property-appearance.md) (`PropertyAppearance`)
- Alanın **varsayılan** (form-düzeyi) görünümü → [`../../../view-profile-property.md`](../../../view-profile-property.md) *(bu aksiyon onun koşullu anlık override'ıdır)*

## Notlar
- Eski DataGrid `childField` hedefleme **taşınmadı** (DataGrid kaldırıldı → [`../../../../../research/compare/new-vs-current-names.md`](../../../../../research/compare/new-vs-current-names.md) §6).

*Oluşturma: 2026-08-26.*
