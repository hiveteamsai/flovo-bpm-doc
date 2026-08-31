# Flovo BPM Motoru — Runtime Verisi Saklama · Pruning · KVKK (workflow_events ve motor tabloları)

> **Durum:** 📝 TASLAK v0.44 — **onay bekliyor**. Karar **R16**, açık sorular **Q18–Q19** → [`engine-runtime-plan.md`](./engine-runtime-plan.md).
> **Kapsam:** [`engine-runtime.md`](./engine-runtime.md) §9 "pruning/saklama" açık notu; `flovo-bpm-engine.md` §8 saklama; **motor runtime tablolarının** yaşam döngüsü:
> `workflow_events` · `workflow_projection` · `workflow_timer` · `ProcessStepInstance` · `InstanceValueOutbox`. **Kapsam dışı (ayrı konular):** form değeri
> (`InstanceValue`/`InstanceValueChange` — "retention manuel" v0.31) · **ayar değişiklik logu** (`research/settings-log/`) · sistem logları (Loki/OTel).
> Bu doküman **teknik mekanizmayı** tanımlar; **süreler ve silme-hakkı politikası hukuki karardır** (Q18/Q19) — burada yalnız **varsayılan öneri** verilir.

---

## 0. İlke
**Denetim izi silinmez, kişi anonimleştirilir; veri katmanlar arasında yaşlanır, satır-satır silinmez.** `workflow_events` **aylık partition**'lıdır: sıcak →
soğuk → arşiv (dışa aktarım) → drop. KVKK "silme/anonimleştirme" talebi olay satırını **silmez**; kişiyi işaret eden **kolonları ve payload yollarını**
bir **tombstone** kullanıcıya çevirir (`pseudonymization`) — süreç geçmişi ("bir yönetici onayladı") korunur, kimlik gider.

## 1. Veri sınıfları (motor runtime)
| Tablo | Rol | Kişisel veri | Yeniden kurulabilir mi | Saklama sınıfı |
|---|---|---|---|---|
| [`workflow_events`](./models/processInstances/workflow-event.md) | **kaynak-hakikat** (audit + replay) | `actor*` kolonları · `payload` içinde user-ref (`{userId, nameSurname}`) · `awaiting[].userId` | — (kaynak) | **A — uzun** (yasal denetim) |
| [`workflow_projection`](./models/processInstances/workflow-projection.md) | türetilmiş imleç | dolaylı (yok) | evet (replay) | **B — süreç yaşadığı sürece**; `done`/`cancelled` + 90 gün sonra silinebilir (liste ihtiyacı `ProcessInstance.executionState`'ten) |
| [`workflow_timer`](./models/processInstances/workflow-timer.md) | uyandırma kaydı | yok | evet (armed set replay) | **C — kısa**: `fired`/`cancelled` 30 gün |
| `ProcessStepInstance` | adım çalıştırma kaydı (iş + motor alanları) | `atUserId` · `atDelegateUserId` | motor alanları evet; `instanceId` bağı **iş verisi** | **A** (form tarihçesi kullanıcıya gösterilir — `showInHistory`) |
| `InstanceAwaitingUser` | canlı bekleyen seti | `userId` | evet | **yaşam = bekleme**; süreç ilerleyince zaten silinir |
| `InstanceValueOutbox` | değer-değişim outbox | yok | — | **C**: `processedDate` dolu > 7 gün → sil |

## 2. Yaşam döngüsü katmanları — `workflow_events` (öneri — Q18)
| Katman | Tanım | Nerede | Süre (varsayılan öneri) | Erişim |
|---|---|---|---|---|
| **Sıcak** | aktif + yakın tarihte biten süreçlerin olayları | ana tablo (aylık partition, tüm indeksler) | partition ayı + **3 ay** | motor + UI tarihçe (anlık) |
| **Soğuk** | biten süreçler; sorgu nadir | aynı DB, partition **detach** → `workflow_events_cold` (yalnız PK + `(organizationId, occurredAt)` indeksi; `pg_squeeze`/cluster) | **+ 21 ay** (toplam 24 ay DB'de) | tarihçe (yavaş kabul) · rapor |
| **Arşiv** | yasal saklama | **MinIO** — org-bazlı bucket, ay-bazlı **JSONL.gz** (+ şema sürümü) `archive/{orgCode}/workflow_events/{yyyy-mm}.jsonl.gz` | **10 yıl** (TTK 82 ticari defter/belge saklama süresine hizalı — **hukuk teyidi** Q18) | talep üzerine (denetim), UI'dan değil |
| **Drop** | süre dolunca | partition `DROP` · arşiv objesi **object-lock** süresi bitince silinir | — | — |

- **Aktif süreçler asla düşmez:** partition detach **koşullu** — partition'daki tüm `processInstanceId`'ler `done`/`cancelled` değilse (`failed` **aktif** sayılır)
  o partition **bekletilir** (uzun yaşayan süreçler için; tipik süreç günler-haftalar sürer).
- **Org-bazlı politika (öneri):** `Organization.retentionPolicy { hotMonths, coldMonths, archiveYears }` — null → sistem varsayılanı. On-prem müşteride
  arşiv hedefi kendi MinIO'su. _(Model alanı **onaydan sonra** eklenir → Q18.)_

## 3. Mekanizma
1. **Partition:** `workflow_events` `RANGE (occurredAt)` **aylık**; yeni partition **2 ay önceden** otomatik (housekeeping — scheduler §7). Değer tabloları `HASH(service_id)`
   kalır; olay tablosunun **zamanla yaşlanan** doğası RANGE'i gerektirir (Q2).
2. **Sıcak → soğuk:** aylık job: uygun partition'ı `DETACH` → `ATTACH` soğuk tabloya (veri kopyalanmaz, metadata işlemi); gereksiz indeksler düşer.
3. **Soğuk → arşiv:** `COPY (SELECT … ORDER BY processInstanceId, version) TO STDOUT` → JSONL.gz → MinIO (`PUT` + object-lock **compliance** modu — arşiv değiştirilemez);
   **checksum** manifest'e yazılır; başarı → partition `DROP`.
4. **Replay uyumu:** arşiv dosyası `WorkflowEvent` şemasıyla **1:1** (şema sürümü manifest'te) → gerekirse geri yükle + replay.
5. **Projeksiyon temizliği:** `workflow_projection` — `executionState IN (done, cancelled) AND updatedAt < now() - 90d` → sil (liste `ProcessInstance.executionState` kopyasından).
6. **Silme yok, drop var:** `workflow_events` üzerinde satır `DELETE` **hiçbir zaman** çalışmaz (append-only garantisi + vacuum yükü yok).

## 4. KVKK — silme/anonimleştirme hakkı ↔ denetim izi (Q19 — hukuki)
### 4.1 Gerilim
Denetim kaydı "**kim** onayladı" bilgisini taşır (kişisel veri). Kişi silme hakkı kullanırsa: kaydı **silmek** denetim bütünlüğünü bozar; **tutmak** hakkı ihlal eder.
Yerleşik çözüm: **pseudonymization** — kayıt kalır, kimlik **geri döndürülemez** biçimde tombstone'a bağlanır. Hukuki dayanak (KVKK m.7 · saklama yükümlülükleri) **hukuk kararı**.

### 4.2 Teknik tasarım (R16)
- **Tombstone kullanıcı:** organizasyon başına sistem `User` kaydı `deletedUser` (ad "Silinmiş Kullanıcı"); FK'ler kırılmaz.
- **Hedefler (kişi = `userId`):**
  | Tablo | Kolon / yol | İşlem |
  |---|---|---|
  | `workflow_events` | `actorUserId` · `actorDelegateUserId` | `= tombstone` |
  | `workflow_events.payload` | tip-başına **kişisel yol listesi**: `actionTransfer.parameters.<user-ref>` (`{userId, nameSurname}`) · `awaiting[].userId` · `skippedForUserId` · `stepFailed.detail` (serbest metin → **boşaltılır**) | `jsonb_set` ile tombstone/`null` |
  | `ProcessStepInstance` | `atUserId` · `atDelegateUserId` | `= tombstone` |
  | `ProcessInstance` | `createdByUserId` | `= tombstone` |
  | `InstanceValue.data` / `InstanceAttr` (user-ref alanlar) | ilgili `Property` alanları | **ayrı konu** (form verisi — "retention manuel" v0.31; ama aynı talebin parçası) |
  | Arşiv (MinIO) | JSONL objeleri | object-lock nedeniyle **değiştirilemez** → **anonimleştirme kaydı** (`kvkk_erasure_log`: `userId → tombstone, tarih`) tutulur; arşiv okunurken **maskeleme uygulanır** (read-time redaction) |
- **İşlem:** `POST /organizations/{org}/kvkk/erasure { userId }` (admin; permissions) → tek job, tüm hedefler; sonuç raporu (kaç satır) → `SettingsLog`.
- **Append-only istisnası:** `workflow_events` üzerindeki **tek UPDATE yolu** budur (+ `publishedAt`); trigger ile başka kolon güncellemesi **engellenir**.
- **`nameSurname` snapshot'ları:** `ActionTransfer` içindeki user-ref değerleri isim taşır → payload yollarında listelenmesi **zorunlu** (aksi hâlde kaçak kişisel veri).

### 4.3 Kişisel veriyi baştan azaltma (tasarım kuralı)
- `stepFailed.payload.detail` **ham response gövdesi taşımaz** (özet ≤ 2 KB, PII-siz); ham gövde gerekiyorsa MinIO'ya, **kısa retention** ile (Q3).
- `suspended.payload.awaiting` yalnız **id** taşır (isim yok); isim okuma-zamanında çözülür.

## 5. Erişim / izolasyon
- Tüm katmanlar `organizationId` + RLS (soğuk tablo dâhil); arşiv bucket **org-başına** (MinIO bucket-per-tenant → `tech-stack/minio.md`).
- Organizasyon **kendi** olay geçmişini UI'dan (sıcak+soğuk) görür; arşive erişim **talep-bazlı** (denetim), sistem yöneticisi aracılığıyla.
- Silme-hakkı işlemi yalnız **organizasyon admin yetkisi** ile (permissions → Q12 ile birlikte).

## 6. Diğer runtime tabloları — kısa saklama
| Tablo | Kural | Job |
|---|---|---|
| `workflow_timer` | `status IN (fired, cancelled) AND coalesce(firedAt, cancelledAt) < now() - 30d` → `DELETE` | günlük |
| `InstanceValueOutbox` | `processedDate < now() - 7d` → `DELETE` | günlük (todo'daki açık "retention" burada kapanır — öneri) |
| `workflow_projection` | §3.5 | günlük |
| `ProcessStepInstance` | **silinmez** (form tarihçesi); org retention'ı ile birlikte `ProcessInstance` bazında arşive gider (A sınıfı) | aylık (events ile birlikte) |

## 7. İzleme
Partition sayısı/boyutu (org) · arşiv job başarı/checksum · bekletilen partition sayısı (aktif süreç yüzünden) · KVKK işlem sayısı ve süresi.

## 8. Açık noktalar → [`engine-runtime-plan.md`](./engine-runtime-plan.md) §3
Q18 katman süreleri + org-bazlı `retentionPolicy` + TTK 10 yıl teyidi · Q19 silme-hakkı politikası (pseudonymization kabulü, arşivde read-time redaction) ·
Q2 RANGE partition · Q3 `detail` boyut/MinIO eşiği.

---

*Oluşturma: 2026-08-31 (v0.44). engine-runtime §9 saklama doldurma.*
