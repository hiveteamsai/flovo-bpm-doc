# Enum — actionDisplayType (Action)

> **Kullanan model:** [`action.md`](../organization-settings/action.md) (`actionDisplayType`)
> **Amaç:** Aksiyonun **hangi ekran bağlamında görüneceğini** belirler.

## Değerler
| Değer | Anlam | Ne için |
|---|---|---|
| `invisible` | Hiçbir yerde görünmez. | Yalnız sistem/otomatik tetiklenen (ör. `autoAction`) aksiyonları gizlemek. |
| `everywhere` | Tüm bağlamlarda görünür. | Hem form detayında hem hızlı onay listesinde erişilebilir aksiyonlar. |
| `onlyFormDetail` | Yalnız form/instance detay ekranında görünür. | Detaya girmeden alınmaması gereken aksiyonlar. |
| `onlyFastApprove` | Yalnız hızlı onay (liste) ekranında görünür. | Detaya girmeden toplu/hızlı onaya uygun aksiyonlar. |

*Oluşturma: 2026-07-10.*
