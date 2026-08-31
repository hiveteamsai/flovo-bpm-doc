# Enum — WorkflowWaitReason

> **Kullanan model:** [`../processInstances/workflow-projection.md`](../processInstances/workflow-projection.md) — alan `waitReason`, tip **WorkflowWaitReason**
> **Amaç:** `executionState = waiting` iken sürecin **neyi beklediğini** ayrıştırır. `ProcessExecutionState` kasıtlı olarak küçük tutulur
> (`waiting` tek değer); bekleme **sebebi** bu enum ile projeksiyonda taşınır (liste/filtre: "onay bekleyenler" ≠ "retry bekleyenler").
> **Durum:** 📝 TASLAK v0.44 — onay bekliyor.

## Değerler
| Değer | Anlam | Uyandıran |
|---|---|---|
| `humanTask` | İnsan aksiyonu bekleniyor (Kullanıcı / Kullanıcı Grubu / Üst Form Kullanıcı) | `actionTaken` (kullanıcı/API) · `timerFired` (timeout) |
| `processing` | `autoAction`'sız **Processing** adımı — dış webhook/aksiyon bekleniyor | `actionTaken` (webhook / Customer API) |
| `timer` | **Timer** adımı (§3.7) süresi bekleniyor | `timerFired` |
| `retry` | Geçici hata sonrası **yeniden deneme** bekleniyor (backoff) | `timerFired(kind=retry)` |
| `subProcess` | `async=false` tetiklenen alt sürecin **bitişi** bekleniyor _(🟦 öneri — ServiceTrigger senkron bekleme runtime karşılığı; → plan Q)_ | alt sürecin `ended` olayı |

## Notlar
- `executionState ≠ waiting` iken `waitReason = null`.
- Frontend "bekleyen formlar" listesi yalnız `humanTask` (ve görünürlük için `processing`) ile ilgilenir; `retry`/`timer` motor-içi beklemedir.

*Oluşturma: 2026-08-31.*
