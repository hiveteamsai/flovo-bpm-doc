# Model — Style

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Bir öğenin **renk/görünümünü** tanımlayan yeniden-kullanılabilir varlık. En temel hâliyle **bg color +
> font color**. **Yalnız Action ve Status** tarafından kullanılır (form alanları bu varlığı kullanmaz).
> **Davranış/kullanım:** → `../../organization-settings/style.md`

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Stil ID'si (referans için). |
| `code` | string (opsiyonel) | — | Alternatif referans kodu (kullanılırsa). |
| `name` | string | — | Stil adı (kullanıcıya görünen). |
| `bgColor` | string (hex/renk) | — | Arka plan rengi. |
| `fontColor` | string (hex/renk) | — | Yazı **ve ikon** rengi (tüketicide metin + ikon; örn. durum etiketinde `definition` + `icon`). |
| `organizationId` | int? | FK → Organization.id | Sahibi organizasyon. **`null` = sistem stili** (tüm organizasyonlarca kullanılır, salt-okunur). |

## Sahiplik & görünürlük
- Organizasyon **kendi** stillerini (`organizationId = <org>`) + **sistem** stillerini (`null`) görür/kullanır.
- Sistem stilleri (`null`) organizasyonlarca **güncellenemez**. Bir organizasyon başkasının stilini göremez.

## Benzersizlik
> `code` doluysa `(organizationId, code)` **benzersiz** — aynı organizasyonda aynı `code`'lu iki stil olamaz.
> `organizationId=null` (sistem stilleri) tarafında da `code` benzersizdir.

## İlişkiler
- **N – 1** → `Organization` (`organizationId`).
- **1 – N** ← `Action.styleId`, `Status.styleId` (bir stil, birçok aksiyon/durumda kullanılır).

## Notlar / açık noktalar
- Kapsam: yalnız **bg + font** mı, daha fazlası mı (fontSize/isBold/border/iconColor)? → `../../todo.md`.
- **Not:** İş kuralı `setStyle` bu varlığı **seçmez**; tekil görünüm niteliğini (fontSize/titleColor) değiştirir.

*Oluşturma: 2026-07-02.*
