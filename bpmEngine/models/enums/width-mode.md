# Enum — WidthMode (genişlik modu)

> Kaynak: app-repo hiveteamsai/flovo-ibpm-v2 @ e825628 · ölçüm 2026-09-08
> Bu doküman UYGULAMADAN geriye yazılmıştır (uygulama dokümanın önündeydi).
> Sonraki değişiklikte sıra tersine döner: önce doküman, sonra uygulama.

> **Durum:** 🟢 Uygulamada canlı (kolon + UI) · dokümana v0.47 ile eklendi
> **Nerede:** `ProcessViewProfileProperty.widthMode` / `.mobileWidthMode`

| değer | TR etiket | Anlam |
|---|---|---|
| `fraction` | Kesir | Alan, 12 kolonluk gridde `displayWidth` kadar yer kaplar (ör. 6 → yarım satır). **Varsayılan.** |
| `fill` | Doldur | Alan, bulunduğu satırda **kalan boşluğu** doldurur. Aynı satırda birden fazla `fill` varsa kalan alan **eşit** bölünür. |

**Varsayılan `fraction`'dır.** Gerekçe: `fill` varsayılan olsaydı, genişliği hiç ayarlanmamış eski
alanların yerleşimi değişirdi (geriye dönük uyumluluk).
