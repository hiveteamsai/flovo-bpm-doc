# Model — InstanceValueOutbox (değer-değişim olay kuyruğu)

> **Durum:** 🟡 TASLAK — değer-saklama mimarisinden türetildi (→ `../../research/property-value-storage/form-deger-saklama-v2.html`); alanlar gözden geçirilecek.
> **Yeni model.**
> **Amaç:** `InstanceValue` güncellendiğinde **aynı transaction'da** yazılan "işlenecek olay" kaydı (Outbox pattern). Relay
> bu tablodan işlenmemiş olayları okuyup **NATS JetStream**'e yayınlar; generic projektör fihristleri (`InstanceAttr`/
> `InstanceListItem`) günceller. **DB trigger yerine** outbox seçildi (yazma yolu şişmesin, hata kaydı geri almasın).

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Olay kimliği. Yayında **NATS `Nats-Msg-Id`** (idempotency/dedup anahtarı) olarak kullanılır. |
| `instanceId` | int | FK → Instance.id | Hangi form değişti. |
| `serviceId` | int | FK → Service.id | Hangi servis (projektör metadata seçimi + izolasyon). |
| `organizationId` | int | (denormalize) | Kiracı — RLS/tenant izolasyonu. |
| `version` | int | — | Değişimin `InstanceValue.version`'ı — **projektör idempotency** (`version <= last_projected_version → skip`). |
| `changedPropertyCodes` | string[] | — | **Delta** — bu olayda değişen alan `code`'ları. Projektör yalnız bunları yeniden yansıtır; **yansıma yayılımı** (A′) yalnız bu kodlardan **kaynak (`isReflectionSource`) olanlar** için tetiklenir (gereksiz fan-out önlenir). Boş/atlanırsa tüm alanlar (full-reflection) fallback. |
| `hopCount` | int | — | **Yansıma kaskad derinliği** (varsayılan `0`; her A′ tazeleme adımında +1). `hopCount > limit → düş` (**derinlik limiti**) + **döngü koruması** (motor **O3**). → [`reflection-propagation.md`](./reflection-propagation.md). |
| `occurredDate` | datetime | — | Olay zamanı. |
| `processedDate` | datetime? | — | İşlenme zamanı; **null = henüz işlenmedi** (relay bunları tarar). |

## İlişkiler
- **N – 1** → `Instance` (`instanceId`), `Service` (`serviceId`).
- **Beslenir** ← `InstanceValue` güncellemesi (aynı TX).

## Notlar / açık noktalar
- **Atomiklik:** `UPDATE InstanceValue` + `INSERT InstanceValueOutbox` **tek DB transaction** — "biri yazıldı diğeri yazılmadı"
  durumu imkânsız. Kayıt = **2 küçük yazma**; asıl projeksiyon işi arka planda.
- **`metadataVersion` yok:** Olayda `instanceId` + `version` (+ `serviceId`) yeter; projektör yansıtırken **güncel `Property`**
  tanımından `projectToAttr`/tip okur (kod ne kadar eski olay gelirse gelsin güncel metadata'ya göre yansıtır).
- **İki tüketici:** (1) **generic projector** → `InstanceAttr`/`InstanceListItem` fihristini yansıtır; (2) **reflection-propagation consumer** → `changedPropertyCodes` içinde `isReflectionSource` alan varsa `AssociatedInstance`'tan child'ları bulup A′ kopyalarını tazeler (→ [`reflection-propagation.md`](./reflection-propagation.md)). `hopCount` kaskad/döngü sınırını taşır.
- **Dayanıklılık:** NATS düşse Outbox **birikir**, relay tekrar dener; kaynak TX zaten tamamdır (veri kaybı yok).
- **Saklama:** işlenmiş (`processedDate` dolu) olaylar periyodik **pruning** ile temizlenir (retention politikası → `../../todo.md`).
- **Kaynak mimari:** → `../../research/property-value-storage/form-deger-saklama-v2.html` (§6.5 · §19 outbox · §20 projektör).

*Oluşturma: 2026-08-04.*
