# Model — Organization

> **Durum:** 🟡 TASLAK (ilk çıkarım — gözden geçirilecek)
> **Amaç:** Flovo'yu kullanan **kurumu (tenant)** temsil eder. Verinin en üst kapsayıcısıdır; kullanıcı/servis/çeviri/
> durum vb. bir organizasyona bağlıdır. Organizasyonlar birbirinden **izoledir**.
> **Davranış/kullanım:** → `../genel-ayarlar/organization.md`

## Alanlar
| Alan | Tip | Anahtar | Açıklama / amaç |
|---|---|---|---|
| `id` | int | PK | Organizasyon ID'si. Diğer modeller `organizationId` ile buraya bağlanır. |
| `code` | string | Unique | Organizasyon **kodu**; **benzersiz**. **Dış referanslarda** (API/entegrasyon) `id` yerine bu kullanılır. |
| `name` | string | — | Organizasyon **adı** (kullanıcıya görünen). |
| `defaultLang` | string | — | **Varsayılan dil**; **sabit set** `tr`/`en`/`de` içinden. Çeviri çözümlemesinde aktif dilin başlangıcı. |
| `logoUrl` | string (null olabilir) | — | Organizasyon **logosu** (görsel URL). Başlık/rapor/bildirimlerde marka. |
| `idleTimeoutMinute` | int | — | **Boşta kalma zaman aşımı** (dk). **null olamaz, varsayılan `0`**. `0` = disable; `>0` iken süre dolunca oturum kilitlenir. |

## İlişkiler
- **1 – N** → `Solution` (`solution.organizationId`) — servisler bu solution'lar altında oluşturulur.
- **1 – N** → `Translation`, `Style`, `Action`, `Status` (hepsi `organizationId`) — **organizasyon havuzu**; o
  organizasyonun tüm servislerinde kullanılabilir.
- `organizationId = null` olan Translation/Style kayıtları **ortak/sistem** kabul edilir (organizasyon değil, Flovo sahibi).

## Notlar / açık noktalar
- `idleTimeoutMinute` alt/üst sınırı ve kilit davranışı → `../todo.md`.
- Sonraki alanlar: plan/abonelik, timezone, para birimi, bölge, güvenlik → `../todo.md`.

*Oluşturma: 2026-07-02.*
