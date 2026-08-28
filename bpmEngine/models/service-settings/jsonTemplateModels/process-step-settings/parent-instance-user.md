# Process Step Settings — `parentInstanceUser` (Üst Form Kullanıcı)

> **stepType:** `parentInstanceUser` · **Adım:** Kullanıcı / Kullanıcı Grubu'na benzer **insan-görev** adımı; farkı: **atananları
> (aksiyon bekleyenler) ve görüntüleme profilini kendi ayarında tutmaz — bağlı olduğu üst formdan (parent instance) devralır.**
> Bir formun altında çalışan **alt-servisler** içindir: alt-servisi üst formla senkron ilerletmeden, üst formun **güncel** atananlarına/görünümüne **anlık bağlar**.
> **Davranış:** → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.22 · **Model (§3):** [`../../process-step.md`](../../process-step.md) §3.17 · **İndeks:** [`index.md`](./index.md).
> **Depolama:** `ProcessStep.settings` (JSONB), ayrımlayıcı `stepType`.

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `parentServiceId` | int | evet | — | İlişkiyi kuran alanın bulunduğu **üst formun servisi** (örn. *masraf formu*). Alt-servis kaydı bu servisteki üst forma bağlanır. |
| `associatedPropertyId` | int | evet | — | Üst formdaki **ilişki alanı** — yalnız `AssociatedInstance` bağı kuran alanlar (**Form List** veya `isAssociatedCombobox` **Combobox**) ve yalnız **bu servisi hedefleyenler** (Form List `childServiceId` = bu servis / Combobox `associatedServiceId` = bu servis). |

> **Bu adımda `processViewProfileId` ve aksiyon-bekleyen (atama) alanı YOKTUR** — ikisi de üst formdan **devralınır** (KARAR v0.32).
> Devralma **çalışma-zamanında** çözülür (kopyalanmaz):
> - **Üst form tespiti:** `AssociatedInstance` içinde `instanceId = <bu instance>` **ve** `associatedPropertyId = <settings.associatedPropertyId>`
>   olan kaydın **`associatedInstanceId`**'si üst formdur (ilişkiyi kuran alan üst formdadır).
> - **Görüntüleme profili:** üstün **aktif adım profilinin `code`**'una **eşleşen** alt-servis profili; aynı kodlu profil yoksa alt-servisin **`isDefault`** profili.
> - **Atananlar:** üst formun **güncel `InstanceAwaitingUser`** kümesi — **okuma-zamanında canlı** çözülür (kopyalanmaz).
>
> **Kenar durumlar (ÇÖZÜLDÜ v0.32):** üstte aksiyon alabilen **yoksa** (üst form bulunamadı/bağ kaldırılmış · üst **otomatik adımda** ·
> üst **Süreç Bitişi'nde**) → alt kayıt **herkese read-only** (profil: bulunamamada doğrudan `isDefault`); **birden fazla** üst → **ilk tespit edilen**.
> Detay → [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.22.

## 3. Ortak alanlar (settings'te değil — `ProcessStep` kolonu)
`code`·`stepType`·`definition`·`order`·`showInHistory`·`skip*`·`environmentRestriction` → [`../../process-step.md`](../../process-step.md) §1.

## 4. JSON Schema
```json
{
  "$id": "process-step-settings/parentInstanceUser",
  "type": "object",
  "additionalProperties": false,
  "required": ["parentServiceId", "associatedPropertyId"],
  "properties": {
    "parentServiceId":      { "type": "integer" },
    "associatedPropertyId": { "type": "integer" }
  }
}
```
> Not: `processViewProfileId` / atama alanı **şemada yoktur** (üstten devralınır). Referans id'ler (`parentServiceId`·`associatedPropertyId`)
> DB FK'si değil, **uygulama-katmanı** doğrulaması; ayrıca `associatedPropertyId` yalnız **bu servisi hedefleyen** ilişki alanları
> arasından seçilebilir (yukarıdaki filtre — uygulama-katmanı).

## 5. Örnek
```json
{
  "parentServiceId": 3,
  "associatedPropertyId": 88
}
```

*Oluşturma: 2026-08-28.*
