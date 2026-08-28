# Property Settings — `flowInfo` (Flow Info)

> **propertyType:** `flowInfo` · **Kontrol:** **salt-okunur türetilmiş** alan; akışın (Instance) kendi metadata'sını (durum · oluşturulma tarihi · oluşturan kullanıcı …) forma getirir. **Girdi değildir.**
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/flow-info.md`](../../../processInstances/propertyValuesTemplates/flow-info.md) (`reflectionMode`'a göre `live`=okuma-anı / `snapshot`=dondurulmuş) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.14 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `flowInfoValue` | string (seçici) | **evet** | — | **Hangi akış (Instance) bilgisinin** forma getirileceğini seçen anahtar — alanın **neyi göstereceğini** belirler (türetmenin girdisi; değer-materialize eden/projektör bununla hangi `Instance` kolonu/join'i okuyacağını bilir). Kullanıcı girdisi **değildir**. Değer şablonunun tanıdığı çekirdek küme: `status` (güncel durum) · `createdDate` (oluşturulma tarihi) · `creatorUser` (oluşturan kullanıcı). Geniş katalog (eski koddan aday) ayrıca `instanceId` · `parentInstanceId` · `parentStatus` · `personToApprove` · `mainAccount` · `lastActionReason` içerir → **§Not** (henüz resmi enum değil). |

## 2. Çekirdek kolonda (settings'e girmez)
- **`reflectionMode`** ([`ReflectionMode`](../../../enums/reflection-mode.md)) — değerin **oluşturma-anı mı (dondurulmuş) yoksa güncel mi** getirileceğini belirler: `live` (canlı — `data`'ya yazılmaz, okurken `Instance` kolonlarından/join ile **güncel** getirilir; **flowInfo varsayılanı**) · `snapshot` (oluşturma anında `data`'ya kopyalanıp **dondurulur**). `materialized` **geçerli değildir** (yalnız `parentProperty` — akış kolonları `AssociatedInstance` yayılım yolunda değildir). Motor/projektör okuduğundan **çekirdek kolonda** (§4). → [`../../../enums/reflection-mode.md`](../../../enums/reflection-mode.md).
- Değer-saklama/projeksiyon metadata'sı: `savePropertyToDb` · `projectToAttr` · `saveChangeLog` · `hasTranslation` (§1.3). `live`'da `data`'da değer olmadığından **fihrist üretilmez**; rapor/filtre doğrudan `Instance` kolonlarından (durum → `Instance.statusId`, tarih/oluşturan → `Instance.createdDate`/`creatorUserId`).
- `defaultValue` **kullanılmaz** — türetilmiş salt-okunur alan; başlangıç değeri yoktur.

## 3. Profil-bazlı
- Yok (`flowInfo` için profil-özel ayar tanımlı değil; görünürlük genel profil alanıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. `reflectionMode` (türetme modu — çekirdek kolonda)
| `reflectionMode` | `data`'da | Getirilme | Kullanım |
|---|---|---|---|
| `live` (**vars.**) | Anahtar **bulunmaz** | Okuma-anı `Instance` kolonundan/join ile **güncel** | Sürekli değişen ama yalnız **gösterilecek** değer (özellikle **status**); rapor `Instance` kolonundan. |
| `snapshot` | Anahtar **var**, değer taşır | Oluşturma anında kopyalanır + **dondurulur** | "Oluşturma-anı" değeri (ör. başlangıç durumu) denetim/rapor için gerekince. |

> `createdDate`/`creatorUser` zaten değişmez → onlarda `live`↔`snapshot` farkı yoktur; fark esas **status**'ta anlamlıdır.

## 5. JSON Schema (`settings`)
```json
{
  "$id": "property-settings/flowInfo",
  "type": "object",
  "additionalProperties": false,
  "required": ["flowInfoValue"],
  "properties": {
    "flowInfoValue": { "type": "string" }
  }
}
```
> Not: `reflectionMode` **çekirdek kolon** olduğundan bu şemada **yer almaz**; şema yalnız `settings` JSONB'yi doğrular. `flowInfoValue` **string seçici** olarak tutulur — somut değer kataloğu (yukarıdaki geniş küme) henüz **resmi enum değildir**; kesinleşince `flow-info-value.md` enum'una bağlanıp şemadaki tip `enum`'a daraltılabilir (→ [`../../../../todo.md`](../../../../todo.md), alan `settings` referans/enum kataloğu).

## 6. Örnek
```json
{ "flowInfoValue": "status" }
```

*Oluşturma: 2026-08-28.*
