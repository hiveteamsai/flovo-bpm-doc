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
| `failed` | Hatalı | Adım hatası `onFail` ile karşılanamadı / retry tükendi (dead-letter). |
| `done` | Bitti | Süreç Bitişi / Alt Süreç Bitişi'ne ulaşıldı (Ended). |

## Notlar
- Geçişler: `new → running ⇄ waiting → done/failed` (→ engine-runtime.md §1 state machine).
- Kaynak-hakikat = `workflow_events`; bu alan türetilmiş projeksiyondur (replay ile yeniden kurulabilir — Partial Event Sourcing).

*Oluşturma: 2026-08-28.*
