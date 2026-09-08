# Property Settings — `flowInfo` (Flow Info)

> **propertyType:** `flowInfo` · **Kontrol:** **salt-okunur türetilmiş** alan; akışın (Instance) kendi metadata'sını (durum · oluşturulma tarihi · oluşturan kullanıcı …) forma getirir. **Girdi değildir.**
> **Değer şekli:** → [`../../../processInstances/propertyValuesTemplates/flow-info.md`](../../../processInstances/propertyValuesTemplates/flow-info.md) (`reflectionMode`'a göre `live`=okuma-anı / `snapshot`=dondurulmuş) ·
> **Davranış:** → [`../../../../service-settings/properties.md`](../../../../service-settings/properties.md) §3.14 · **Çekirdek model:** [`../../property.md`](../../property.md) · **İndeks:** [`index.md`](./index.md).

## 1. `settings` (JSONB) — tipe-özel ayarlar
| Alan | Tip | Zorunlu | Varsayılan | Açıklama / kısıt |
|---|---|---|---|---|
| `flowInfoValue` | string (seçici) | **evet** | — | **Hangi akış (Instance) bilgisinin** forma getirileceğini seçen anahtar — alanın **neyi göstereceğini** belirler (türetmenin girdisi; değer-materialize eden/projektör bununla hangi `Instance` kolonu/join'i okuyacağını bilir). Kullanıcı girdisi **değildir**. Değer şablonunun tanıdığı çekirdek küme: `status` (güncel durum) · `createdDate` (oluşturulma tarihi) · `creatorUser` (oluşturan kullanıcı). Geniş katalog adayları: `instanceId` · `parentInstanceId` · `parentStatus` · `personToApprove` — katalog **`flow-info-value.md` enum'una** çekilecek (→ §5 not). **`mainAccount` ve `lastActionReason` katalogda yoktur** (KARAR v0.46 → §7). |

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

## 7. Kararlar (v0.46) — `mainAccount` ve `lastActionReason` katalog-dışı
**`lastActionReason` flowInfo değildir — bilinçli olarak yoktur.** Aksiyon gerekçesi bir akış metadata'sı değil, **form verisidir**; motor için
özel bir mekanizma (kanonik "gerekçe" kolonu, "gerekçe zorunlu" bayrağı, flowInfo anahtarı) gerektirmez. Tamamen **no-code** kurulur:
1. Aksiyon türü **`eventForm`** (→ [`../../../../service-settings/process-step-action.md`](../../../../service-settings/process-step-action.md) §3.2):
   kullanıcı reddederken/geri gönderirken pop-up'ta gerekçeyi girer; değer **`ActionTransfer.parameters`** ile hedef adıma taşınır
   (zorunluluk, `eventForm` servisindeki alanın kendi zorunluluk ayarıyla sağlanır).
2. Hedef adım **Değer Atama** (→ [`../../../../service-settings/process-step.md`](../../../../service-settings/process-step.md) §3.4): gelen parametreyi
   formdaki **istenen alana** (örn. `rejectReason` text property) yazar.
3. Gerekçe artık **normal bir form alanıdır**: `InstanceValue.data`'da saklanır, `projectToAttr` ile fihriste girer; rapor/filtre/iş kuralı/görünüm
   profili bu alan üzerinden çalışır. Hangi aksiyonda girildiği gerekirse `ProcessStepInstance.processStepActionParameter`'dan (aksiyon paketi) izlenir.
> Örnek: [`../../../../sampleProcess/referred/referred.md`](../../../../sampleProcess/referred/referred.md) — `Yönlendir` (eventForm) →
> `parameters: { transferUser }` → `atama` (Değer Atama) → "Yönlendirilen Kullanıcı" alanı; "Geri Gönder / Reddet" gerekçesi için aynı desen.
> Değer Atama'nın gelen `parameters`'ı **hangi kaynak türüyle** okuduğu (`ValueAssignType` Değer Atama alt-kümesinde parametre kaynağı tanımlı değil)
> → [`../../../../todo.md`](../../../../todo.md) açık sorusu.

**`mainAccount` katalogdan düşürüldü.** Yeni modelde bir Instance'ın "hesap" düzeyinde okunacak bir kaynağı yoktur: kiracı
**`Instance.organizationId`**'dir (RLS/tenant izolasyonu — formu gören herkes zaten aynı organizasyondadır, gösterilecek bilgi değildir); şirket ise
**kullanıcıya** bağlıdır (`User.companyIds` → **`userInfo`** tipi, `company` anahtarı → [`user-info.md`](./user-info.md)). Akış bilgisi olarak
karşılığı bulunmadığından `flow-info-value.md` enum'una **alınmaz**.

*Oluşturma: 2026-08-28. Güncelleme: 2026-09-08 (v0.46) — §7 kararlar: `mainAccount` · `lastActionReason` katalog-dışı (gerekçe = eventForm → Değer Atama → form alanı).*
