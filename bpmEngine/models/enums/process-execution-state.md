# Enum — ProcessExecutionState

> **Kullanan model:** [`../processInstances/process-instance.md`](../processInstances/process-instance.md) — alan `executionState`, tip **ProcessExecutionState**
> **Amaç:** Bir `ProcessInstance`'ın **motor yürütme durumunu** belirtir — motorun iç konumu. Kullanıcının gördüğü **iş durumu**
> (`Instance.statusId`) ile **karıştırılmaz**; ikisi bağımsız evrilir. `workflow_events` (append-only) log'undan **türetilen
> projeksiyondur** (hızlı sorgu: "koşan / bekleyen / hatalı süreçler"). Runtime mimarisi → [`../../engine-runtime.md`](../../engine-runtime.md) §1.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `new` | Yeni | Süreç başlatıldı, ilk adım henüz koşmadı (StartRequested). |
| `running` | Koşuyor | Motor aktif olarak otomatik adım zincirini ilerletiyor (kuyrukta iş var). |
| `waiting` | Bekliyor | İnsan/timer/processing beklemesinde **askıda** (worker serbest; `InstanceAwaitingUser` dolu). |
| `failed` | Hatalı | Adım hatası `onFail` ile karşılanamadı / retry tükendi / tasarım ya da guard hatası (dead-letter). **Admin kurtarması** bekler (`retry`/`skip` → `running`, `cancel` → `cancelled`). |
| `done` | Bitti | Süreç Bitişi / Alt Süreç Bitişi'ne ulaşıldı (`ended`) veya terminal otomatik adım kolu bitirdi. |
| `cancelled` | İptal edildi | 📝 **v0.44 öneri (plan Q6):** admin `failed`/`waiting` süreci **iptal** etti — BİTİŞ düğümüne ulaşılmadı. `Instance.statusId` **değişmez** (iş durumu ayrı). |

## Notlar
- Geçişler: `new → running ⇄ waiting → done | failed → (recovered → running) | cancelled` (→ engine-runtime.md §1 state machine · olay tipleri → [`workflow-event-type.md`](./workflow-event-type.md)).
- **`waiting` tek değerdir;** neyi beklediği (`humanTask`/`processing`/`timer`/`retry`/`subProcess`) `WorkflowProjection.waitReason` ile ayrışır → [`workflow-wait-reason.md`](./workflow-wait-reason.md) (ayrı `retrying` durumu **yoktur** — plan R13).
- Kaynak-hakikat = `workflow_events`; bu alan türetilmiş projeksiyondur (replay ile yeniden kurulabilir — Partial Event Sourcing). Aynı değer `ProcessInstance.executionState` (liste kopyası) ve
  [`WorkflowProjection.executionState`](../processInstances/workflow-projection.md) (imleç) üzerinde **aynı TX'te** yazılır.

*Oluşturma: 2026-08-28. Güncelleme: 2026-08-31 (v0.44) — `cancelled` + `waitReason` notu.*
