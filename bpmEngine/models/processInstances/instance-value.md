# Model — InstanceValue (form değer tapusu / kaynak-hakikat)

> **Durum:** 🟡 TASLAK — değer-saklama mimarisinden türetildi (→ `../../research/property-value-storage/form-deger-saklama-v2.html`); alanlar gözden geçirilecek.
> **Yeni model.**
> **Amaç:** Bir `Instance`'ın **tüm alan değerleri** tek **JSONB** kutuda (`data`). Sistemin **tek gerçek kaynağıdır**
> (tapu): kullanıcı formunu buradan görür, motor tek-kayıt okuması burayı okur. Fihristler (`InstanceAttr`/`InstanceListItem`)
> bundan **yeniden üretilebilir**; bu model onlardan üretilmez.

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `instanceId` | int | PK · FK → Instance.id | Hangi form. `Instance` ile **1–1** (PK aynı zamanda FK). |
| `organizationId` | int | (denormalize) | Kiracı kimliği — **RLS/tenant izolasyonu** + partition için `Instance`'tan denormalize edilir. |
| `serviceId` | int | **PK** · FK → Service.id | Hangi servis — **partition (HASH)** + sorgu pruning. **PK'ye dâhildir:** partition kolonu PK'de olmalı (HASH partition gereği); ayrıca `InstanceAttr`/`InstanceListItem` ile simetri + **servis-kapsamlı join'siz** sorgu. |
| `data` | jsonb | — | **Tüm alan değerleri — `code`-keyed** (JSON anahtarı = `Property.code`, id değil). API, iş kuralı ve custom code aynı dili konuşur. Etiketli seçimler `LabeledValue` şekliyle (`{value, display, translationCode}`) yazılır → [`labeled-value.md`](./propertyValuesTemplates/labeled-value.md). |
| `version` | int | — | Her update'te **+1**; projektör **idempotency** anahtarı (`event.version <= last_projected_version → skip`). |
| `createdDate` | datetime | — | Oluşturulma zamanı. |
| `updatedDate` | datetime | — | Son güncelleme zamanı. |

> **Birincil anahtar:** `(instanceId, serviceId)`. `instanceId` tek başına da benzersizdir (Instance ile **1–1**); `serviceId`
> **partition kolonu** olduğundan PK'ye dâhil edilir (`InstanceAttr`/`InstanceListItem` PK deseniyle simetri).

## İlişkiler
- **1 – 1** ↔ `Instance` (`instanceId` — PK'nin parçası, aynı zamanda FK).
- **N – 1** → `Service` (`serviceId`).
- **1 – N** → `InstanceAttr` · `InstanceListItem` · `InstanceValueChange` · `InstanceValueOutbox` (hepsi `instanceId` ile;
  fihrist/olay/geçmiş kayıtları bu tapudan türetilir/beslenir).

## Notlar / açık noktalar
- **Kaynak vs fihrist (mimari sözleşme):** `InstanceValue.data` **tek gerçek kaynaktır**. `InstanceAttr`/`InstanceListItem`
  **projeksiyondur** — silinseler bile bu `data`'dan bit-bit aynı yeniden üretilir; içlerinde "başka yerde olmayan" bilgi
  yoktur. **Detay/form ekranı asla fihriste bakmaz** → projeksiyon gecikmesi (eventual consistency) formu bozamaz.
- **Yazım = tek atomik TX:** `UPDATE InstanceValue (data, version+1, updatedDate)` ile `INSERT InstanceValueOutbox`
  **aynı DB transaction'ında** yazılır (biri yazılır diğeri yazılmaz durumu imkânsız). `saveChangeLog=true` alanlar için
  aynı TX'te `InstanceValueChange` de yazılır. Arka planda: Outbox → NATS → generic projektör (tam-yansıtma, delta değil).
- **Anahtar konvansiyonu (KARAR):** Değer saklayan her alan `data`'da **`Property.code`** anahtarıyla temsil edilir ve **anahtar
  her zaman bulunur** (anahtarlar **daima** `code`; id değil). Boş değer **anahtar yokluğuyla değil**, değerin **`null`** (skaler) /
  **`[]`** (liste) olmasıyla gösterilir. **İstisna — `data`'ya hiç yazmayan alanlar:** `text` (statik label) · **`live`** yansımalar
  (`flowInfo`/`userInfo`/`parentProperty`) · **`savePropertyToDb=false`** (geçici/backing alan) → bunların anahtarı olmaz.
- **Ortak değer dili (koleksiyon-tabanlı motor):** `data`'daki değer-modeli (code-keyed + `propertyValuesTemplates` şekilleri +
  `LabeledValue`), aksiyon veri-aktarımındaki **`changeList`/`parameters`** ile **aynıdır**. `changeList` = obje-map
  `{ Property.code: value }` → forma **doğrudan JSONB merge** (`data = data || changeList`); `parameters` = aynı değer şekli,
  **serbest anahtar**, forma yazılmaz. Bu sayede değer adım↔adım↔form arasında **kayıpsız** akar. → `../../flovo-bpm-engine.md` §3 ·
  `../../service-settings/process-step-action.md` §2.2.
- **`data` küçük tutulur:** JSONB update = satırın **tümünün** yeniden yazılması (MVCC). Bu yüzden dosya/binary
  **JSONB'ye gömülmez** — MinIO'ya konur, `data`'da yalnız URL/object key durur (→ `tech-stack/minio.md`).
- **`status` `data`'da değildir:** formun canlı durumu `Instance.statusId` **kolonundadır** (her onayda tüm `data` yeniden
  yazılmasın + rapor bayatlamasın diye). Aynı şekilde `creatorUserId`/`createdDate` = `Instance` kolonları.
- **`eventForm` tipi serviste `InstanceValue` oluşmaz** (o serviste `Instance` de oluşmaz; değerler `parameters` ile geçici
  taşınır → `../service-settings/service.md` `formType`).
- **Kaynak mimari:** → `../../research/property-value-storage/form-deger-saklama-v2.html` (§3 sözleşme · §6.2 · §8 yazma · §19 outbox).

*Oluşturma: 2026-08-04.*
