# Property Settings — `userInfo` (User Info)

> **propertyType:** `userInfo` · **Kontrol:** **salt-okunur türetilmiş** alan; bir kullanıcının (varsayılan: giriş yapan kullanıcı) metadata'sını (ad-soyad · e-posta · departman · unvan · yönetici …) forma getirir. Flow Info'nun **kullanıcı karşılığı**. **Girdi değildir.**
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/user-info.md`](../../../processInstances/propertyValuesTemplates/user-info.md) (`reflectionMode`'a göre `snapshot`=dondurulmuş / `live`=okuma-anı) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.16 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `userInfoValue` | string (seçici) | **evet** | — | **Hangi kullanıcı bilgisinin** forma getirileceğini seçen anahtar — alanın **neyi göstereceğini** belirler (türetmenin girdisi; değer-materialize eden/projektör bununla `User`'ın hangi alanını okuyacağını bilir). Kullanıcı girdisi **değildir**. Aday katalog (eski koddan): `nameSurname` · `userId` · `mail` · `profession` · `department` · `additionalQualification` · `manager` (yönetici — `{userId, nameSurname}` referansı) · `costCenter` · `workerLevel` · `company` → **§Not** (henüz resmi enum değil). |

## 2. Çekirdek kolonda (settings'e girmez)
- **`reflectionMode`** ([`ReflectionMode`](../../../enums/reflection-mode.md)) — değerin **oluşturma-anı mı (dondurulmuş) yoksa güncel mi** getirileceğini belirler: `snapshot` (oluşturma anında `data`'ya kopyalanıp **dondurulur** — "o anki departman/unvan"; **userInfo varsayılanı**) · `live` (canlı — `data`'ya yazılmaz, okurken `User`'dan **güncel** getirilir; kullanıcı departmanı sonradan değişirse yeni değer görünür). `materialized` **geçerli değildir** (yalnız `parentProperty` — `User` bilgisi `AssociatedInstance` yayılım yolunda değildir). Motor/projektör okuduğundan **çekirdek kolonda** (§4). → [`../../../enums/reflection-mode.md`](../../../enums/reflection-mode.md).
- Değer-saklama/projeksiyon metadata'sı: `savePropertyToDb` · `projectToAttr` · `saveChangeLog` · `hasTranslation` (§1.3). `snapshot`'ta değer `data`'da olduğundan **InstanceAttr**'a projekte edilebilir; `live`'da `data`'da değer olmadığından **projekte edilmez** (rapor gerekiyorsa `User` join'i veya `snapshot`).
- `defaultValue` **kullanılmaz** — türetilmiş salt-okunur alan; başlangıç değeri yoktur.

## 3. Profil-bazlı
- Yok (`userInfo` için profil-özel ayar tanımlı değil; görünürlük genel profil alanıdır → [`../../view-profile-property.md`](../../view-profile-property.md)).

## 4. `reflectionMode` (türetme modu — çekirdek kolonda)
| `reflectionMode` | `data`'da | Getirilme | Kullanım |
|---|---|---|---|
| `snapshot` (**vars.**) | Anahtar **var**, değer taşır | Oluşturma anında kopyalanır + **dondurulur** | Kayıt **o anki** kullanıcı bilgisini korumalı (audit-dostu; departman/unvan sonradan değişse bile eski değer kalır). |
| `live` | Anahtar **bulunmaz** | Okuma-anı `User`'dan **güncel** | Her zaman **güncel** kullanıcı bilgisi gösterilecekse (Flow Info `live` gibi). |

> **Yönetici** gibi kullanıcıya atıf yapan bir alt-değer `string`/`LabeledValue` değil, kullanıcı-referans konvansiyonuyla **`{ userId, nameSurname }`** tutulur (→ değer şablonu §1).

## 5. JSON Schema (`settings`)
```json
{
  "$id": "property-settings/userInfo",
  "type": "object",
  "additionalProperties": false,
  "required": ["userInfoValue"],
  "properties": {
    "userInfoValue": { "type": "string" }
  }
}
```
> Not: `reflectionMode` **çekirdek kolon** olduğundan bu şemada **yer almaz**; şema yalnız `settings` JSONB'yi doğrular. `userInfoValue` **string seçici** olarak tutulur — somut değer kataloğu (yukarıdaki aday küme) henüz **resmi enum değildir**; kesinleşince `user-info-value.md` enum'una bağlanıp şemadaki tip `enum`'a daraltılabilir (→ [`../../../../todo.md`](../../../../todo.md), alan `settings` referans/enum kataloğu).

## 6. Örnek
```json
{ "userInfoValue": "department" }
```

*Oluşturma: 2026-08-28.*
