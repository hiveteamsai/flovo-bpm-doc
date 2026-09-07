# Research — Motor Runtime Anlatımı & Mimari Şeması (çalışma-zamanı mimarisi · v0.44 / v0.45)

> **Amaç:** v0.44'te yazılan **çalışma-zamanı mimarisi taslak setinin** (`WorkflowEvent` / `WorkflowProjection` / `WorkflowTimer` modelleri ·
> iki-TX otomatik adım · idempotency & çakışma sözleşmesi · hata/dayanıklılık · zamanlayıcı/uyandırma · saklama/KVKK) **tek sayfalık
> özet + detay anlatımı**. İnceleme ve sunum içindir; **bağlayıcı metin tasarım dokümanlarının kendisidir** (aşağıda). Anlatım dokümanlardan
> farklılaşırsa dokümanlar esas alınır.
> **Durum:** 📝 v0.44 taslak seti **onay bekliyor** (→ [`../../engine-runtime-plan.md`](../../engine-runtime-plan.md) R1–R17 · Q1–Q22); bu anlatım
> o setin **2026-08-31 (commit `416425d`) fotoğrafıdır**. Kararlar kesinleşince (plan §5 review log) sayfa ya güncellenir ya "arşiv" işareti alır.

## Dosyalar
| Dosya | İçerik |
|---|---|
| [`motor-runtime-v0-44-ozet-detay.html`](./motor-runtime-v0-44-ozet-detay.html) | **Özet + detay anlatımı (tek sayfa, sol yapışkan içindekiler).** **Özet:** sorun (senkron döngü → dağıtık olay-akışı) · tez ("süreç = Postgres'te duran durum + NATS'ta akan olaylar") · üç tablo · altı aktör · "nasıl çalışır — altı hareket" · altı garanti · durum makinesi diyagramı · kavram sözlüğü. **Örnek:** bir masraf formunun 12 satırlık `workflow_events` defteri (ERP 503 → retry timer → yönetici onayı → bitiş; TX-A/TX-B işaretli) + timeout / retry-tükendi alternatif yolları. **Detay:** yürütme durumu · WorkflowEvent (alanlar · 12 tip + payload · geçiş kuralları · indeks/partition) · iki-TX worker turu (sequence diyagramı + in-doubt) · idempotency/version/outbox + API 200/409/403/422 sözleşmesi · WorkflowProjection · WorkflowTimer & Scheduler (4 tür · claim döngüsü · R14 · preemption · cron TZ/DST) · hata & dayanıklılık (5 sınıf · retry formülü · onFail sırası · `parameters.error` · kurtarma · guard'lar) · saklama & KVKK (4 katman · pseudonymization). **İnceleme:** R1–R17 · Q1–Q22 (öncelikli, örnekli) · plan P1–P10 · 31 dosyalık doküman haritası. **Hız & performans değerlendirmesi** (kritik yol maliyet dökümü · risk→önlem · benchmark hedefi; R18 inline-devam önerisine dayalı — 2026-09-04). Tarayıcıda doğrudan açılır (yazı tipleri Google Fonts, diyagramlar mermaid — cdnjs; çevrimdışı açılırsa yazı tipi/diyagram düşer, metin okunur kalır). |
| [`motor-mimari-semasi-v0-45.html`](./motor-mimari-semasi-v0-45.html) | **Metot-düzeyi mimari şeması (📝 ÖNERİ — v0.45 çalışma).** Kuş bakışı bileşen diyagramı (4 barındırıcı → tek `engine` kütüphanesi → tablolar + NATS) · **tablolar** (rol · anahtar sütun · yazan metotlar) · **üç akış diyagramı** (numaralı sequence): kullanıcı aksiyonu inline zincir (`TakeAction → RecordActionTaken → Advance/RunStep → Suspend → BuildActionResponse`) · worker işi (redelivery · in-doubt · retry/onFail/dead-letter dalları) · scheduler (`ClaimDueTimers → ApplyTimer`) · **çağrı ağacı** (hangi metot hangisini hangi sırayla; düğüm başına I/U/D/R tablo etiketleri, TX sınırları) · **metot × tablo yazma matrisi** · **adım yürütücüleri** (idempotentlik, hata sınıfı) · **olay → dispatch → NATS** eşlemesi · notlar: **R18 inline devam** (dispatch'in sonraki `BeginStep`'te tüketimi) + **Q23** pencere parametreleri. **Metot adları/ayrıştırma dokümanlarda henüz yok — öneridir**; TX sınırları ve olay↔tablo eşlemesi v0.44 setiyle uyumludur. |

> **Çevrimiçi kopyalar** (Claude artifact, özel — paylaşım sayfa menüsünden): anlatım <https://claude.ai/code/artifact/2334df05-daed-420f-87fd-ca261faa3a82> · şema <https://claude.ai/code/artifact/88c0c91d-6f3e-4c2f-a37d-a48581d7726f>

## Anlatımın kaynağı (bağlayıcı dokümanlar)
| Doküman | Rol |
|---|---|
| [`../../engine-runtime.md`](../../engine-runtime.md) | Runtime mimarisi **ana spec** (state machine · bileşenler · akış · idempotency · ölçek) |
| [`../../engine-runtime-errors.md`](../../engine-runtime-errors.md) | Hata sınıfları · retry · in-doubt · onFail · dead-letter · kurtarma · guard'lar · compensation |
| [`../../engine-runtime-scheduler.md`](../../engine-runtime-scheduler.md) | Scheduler claim modeli · WorkflowTimer yaşam döngüsü · timeout/stepTimer/retry/cron · TZ/DST · housekeeping |
| [`../../engine-runtime-retention.md`](../../engine-runtime-retention.md) | Saklama katmanları · partition/arşiv · KVKK pseudonymization |
| [`../../engine-runtime-plan.md`](../../engine-runtime-plan.md) | Kararlar R1–R17 · açık sorular Q1–Q22 · plan P1–P10 · review log |
| [`../../models/processInstances/workflow-event.md`](../../models/processInstances/workflow-event.md) · [`workflow-projection.md`](../../models/processInstances/workflow-projection.md) · [`workflow-timer.md`](../../models/processInstances/workflow-timer.md) | Üç motor modeli |
| [`../../models/enums/workflow-event-type.md`](../../models/enums/workflow-event-type.md) · [`workflow-wait-reason.md`](../../models/enums/workflow-wait-reason.md) · [`workflow-timer-kind.md`](../../models/enums/workflow-timer-kind.md) · [`workflow-timer-status.md`](../../models/enums/workflow-timer-status.md) · [`workflow-error-class.md`](../../models/enums/workflow-error-class.md) | Enum'lar |

## Neden `research/` altında?
Tasarım dokümanı değil, **anlatım/sunum çıktısı** — [`../property-value-storage/form-deger-saklama-v2.html`](../property-value-storage/form-deger-saklama-v2.html) ve
[`../tech-stack/`](../tech-stack/index.md) HTML raporlarıyla aynı sınıf. Tasarım değişince önce dokümanlar güncellenir; bu sayfa onların **fotoğrafı** olarak yeniden üretilir.

*Oluşturma: 2026-09-01 (v0.45 çalışma dosyası) · şema eklendi: 2026-09-01.*
