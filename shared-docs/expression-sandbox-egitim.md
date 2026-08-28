# Flovo iBPM — İfade (Expression) / Sandbox Eğitim Dökümanı

> **Kapsam:** Feature #74 (E2.2) — motor-içi ifade değerlendirme motoru (expression evaluator / sandbox).
> **Hedef kitle:** İş-kuralı / form-hesaplama tasarlayan yapılandırıcı (designer/admin) + geliştirici.
> **Durum notu (dürüst):** İfade **dili + sandbox motoru** hazır ve test-edilmiştir (Story #80). Motorun ürün-içine
> bağlanması (form-hesap / iş-kuralı / aksiyon-parametre ekranları) **ayrı ve sonraki bir dilimde** (E2.2-S3) planlıdır —
> yani bu döküman "bugün mevcut olan ifade dili + güvenlik modeli"ni anlatır; "nereye yazılacağı"nın UI'ı gelmekte.
> **Kaynak (SSOT):** ADR-E2.2 (`docs/adr/ADR-E2.2-sandbox-credential-encryption.md`) · `internal/domain/expr/evaluator.go`

---

## 1. Nedir? — bir cümlede

İfade motoru; **güvenli, sınırlı, deterministik** küçük bir formül dilidir. Bir **ifade metni** (ör. `amount * 2 + 1`)
ile o ifadenin görebileceği **değişkenler** (ör. `amount = 10`) verir; motor sonucu döndürür (`21`).

Dil olarak **CEL** (Common Expression Language — Google'ın `cel-go` kütüphanesi) kullanılır. CEL; Kubernetes, Envoy ve
policy-motorlarında güvenlik sınırında kullanılan, **formal spesifikasyonu olan, Turing-complete OLMAYAN** bir ifade dilidir.

### Ne DEĞİLDİR (bilinçli tasarım)
- Genel amaçlı bir programlama dili değildir (JavaScript / Lua / Python **gömülü değil**).
- Döngü / özyineleme (recursion) yazamazsınız → **sonsuz döngü yapısal olarak imkânsız**.
- Dosya / ağ / veritabanı / komut çalıştırma **yoktur** (aşağıda §5).
- Akış (flow) kararı **veremez** — ifade yalnız **veri okur/hesaplar**; hangi adıma gidileceğini motor bağımsız belirler.

---

## 2. Nerede kullanılır? (Y1 yüzeyleri)

İfade motoru şu yerlerde **semi-trusted** (tenant tasarımcısı/admini yazar) ifadeleri değerlendirmek için tasarlandı:

| Yüzey | Örnek |
|---|---|
| **Form hesaplaması** (`valueAssignType = fromCalculation`) | Bir form alanının değeri başka alanlardan hesaplanır: `quantity * unitPrice` |
| **İş kuralı (business rule)** | Bir koşulun sağlanıp sağlanmadığı: `amount > threshold && status == "approved"` |
| **Aksiyon parametre ifadesi** | Bir aksiyona giden parametrenin değeri: `"REF-" + code` |
| **Koşullu çalışma** | Bir adımın/aksiyonun çalışıp çalışmayacağı: `qty > 0` |

> **Durum:** Yukarıdaki yüzeylerin **UI-bağlantısı** (ifadeyi ekrandan girme) ayrı dilim E2.2-S3'te gelir. Motor + dil
> hazır; bu döküman ifade yazımının **dil kurallarını** öğretir.

---

## 3. Temel kullanım modeli

Her ifade değerlendirmesi iki girdi alır, bir çıktı verir:

```
İfade (program)      : "amount * 2 + 1"          ← CEL metni
Değişkenler (env)    : { amount: 10 }            ← ifadenin görebileceği TEK dış veri
--------------------------------------------------
Sonuç                : 21
```

**Kritik kural — deny-by-default (varsayılan-reddet):** İfade **YALNIZ** kendisine verilen değişkenleri + saf CEL
standart-kütüphanesini görür. `env`'de olmayan bir isim kullanırsanız ifade **derleme anında reddedilir** (çalışmadan hata).

---

## 4. Örnek ifadeler (girdi → çıktı)

Aşağıdakiler motorun birim-testlerinden alınmış, **çalışan** örneklerdir:

| Tür | İfade | Değişkenler (girdi) | Sonuç (çıktı) |
|---|---|---|---|
| Aritmetik | `amount * 2 + 1` | `{ amount: 10 }` | `21` |
| Karşılaştırma | `amount > threshold` | `{ amount: 5, threshold: 3 }` | `true` |
| Koşul (ternary) | `qty > 0 ? "ok" : "empty"` | `{ qty: 4 }` | `"ok"` |
| Liste — filtre + say | `size(items.filter(x, x > 2))` | `{ items: [1,2,3,4] }` | `2` |
| Liste — map | `items.map(x, x * 2)` | `{ items: [1,2,3] }` | `[2,4,6]` |
| Regex eşleşme (RE2) | `code.matches("^[A-Z]{3}$")` | `{ code: "TRY" }` | `true` |
| String birleştirme | `"REF-" + code` | `{ code: "A1" }` | `"REF-A1"` |
| Mantıksal | `a && (b \|\| c)` | `{ a: true, b: false, c: true }` | `true` |

**Reddedilen (güvenlik) örnekleri:**

| İfade | Sonuç | Neden |
|---|---|---|
| `unknown_field + 1` | ❌ `compile_error` | `unknown_field` env'de yok (deny-by-default) |
| `now()` | ❌ `compile_error` | Non-deterministik fonksiyon varsayılan kapalı (§5) |
| `readFile("/etc/passwd")` | ❌ `compile_error` | Dosya erişimi yok |
| `http("...")` / `lookup("...")` | ❌ `compile_error` | Ağ / host-fonksiyon yok |

---

## 5. Kullanılabilir fonksiyonlar/metodlar + güvenlik-limitleri

### 5.1 Mevcut fonksiyonlar — CEL standart kütüphanesi (saf)

İfade içinde yalnız **saf CEL standart-kütüphanesi** + verdiğiniz değişkenler kullanılabilir. Sık kullanılanlar:

- **Aritmetik/mantık:** `+ - * / %`, `< <= > >= == !=`, `&& || !`, `koşul ? a : b`
- **String:** `size(s)`, `s.contains(x)`, `s.startsWith(x)`, `s.endsWith(x)`, `s.matches(regex)` (RE2 — güvenli, catastrophic-backtracking yok)
- **Liste/harita:** `size(list)`, `x in list`, `list.filter(x, koşul)`, `list.map(x, ifade)`, `list.all(x, koşul)`, `list.exists(x, koşul)`
- **Tip dönüşümü:** `int(x)`, `double(x)`, `string(x)`, `bool(x)`
- **Var mı:** `has(obj.field)`

> Tam liste CEL dil-spesifikasyonundadır. **Bizim sandbox saf-stdlib'e kısıtlar** — I/O yapan hiçbir fonksiyon yoktur.

### 5.2 Güvenlik invariant'ları (hepsi birim-testli)

| İnvariant | Ne demek |
|---|---|
| **Deny-by-default** | Yalnız verilen değişkenler görünür; tanımsız isim → derlemede RED |
| **Ambient-authority yok** | Ağ / dosya / DB / komut / reflection / import **yok** |
| **Determinizm** | `now()` / rastgele **varsayılan kapalı** (event-replay saflığı için); gerekirse motor **audit'li, inject-edilmiş** binding olarak verir (§6) |
| **Tenant izolasyonu** | Değerlendirme ortamı her istekte **RLS-filtreli** veriden kurulur; bir ifade başka tenant'ın verisine **fiziksel olarak** referans veremez |
| **Kaynak-limiti (DoS)** | timeout `100ms` · CEL cost tavanı `1.000.000` · program uzunluğu `4096` char · AST düğüm `256` / derinlik `32` |
| **Hata-redaksiyonu** | Kullanıcıya giden hata mesajı **genel/sanitize** (ifade metni / değişken adı / iç yapı sızmaz); tam detay yalnız server-side audit-log'a |

---

## 6. Değişkenler nereden gelir? (env + motor-inject binding)

İfadenin gördüğü değişkenler **iki kaynaktan** motor tarafından hazırlanır — ifadeyi yazan bunları **çağırmaz**, hazır bulur:

1. **Instance alan değerleri:** İçinde bulunulan kaydın (form/instance) alanları — fetch anında zaten **RLS ile tenant-scoped**.
2. **Motor-inject, RLS-scoped, önceden-çözülmüş binding'ler:** parent/lineage değerleri (ör. üst-instance, ilişkili-kayıt),
   veya `today` gibi non-default değerler. Bunlar **eval-context değişkenidir, ifadenin çağırdığı fonksiyon değil**;
   kullanımı audit-log'a yazılır (determinizm-esnetme bilinçli + izli olsun diye).

**Örnek — non-default binding (`today`):**
```
inject olmadan:  today == "2026-08-18"   → ❌ compile_error (today tanımsız)
inject ile:      today == "2026-08-18"   → ✅ true   (motor `today` binding'ini audit'le sağlar)
```

> **Kırmızı çizgi:** Hiçbir binding, ifadenin **akış-kapılamasını** (flow-gating) etkilemesine izin vermez. İfade yalnız
> **veri okur**; adım/akış kararını motor bağımsız verir.

---

## 7. Yeni bir ifade/kural nasıl yazılır? (adım adım)

1. **Hangi değişkenler mevcut?** — o yüzeyde (form-hesap / iş-kuralı) motorun sağladığı alan adlarını öğrenin (ör. `amount`, `quantity`, `status`). Yalnız bunları + saf-stdlib'i kullanabilirsiniz.
2. **İfadeyi CEL ile yazın** — §4'teki kalıpları temel alın. Örnek: "tutar eşiği aşıyorsa onay gerekli":
   `amount > threshold ? "needs_approval" : "auto"`
3. **Tipe dikkat** — CEL güçlü-tiplidir; `int` ile `string`'i doğrudan toplayamazsınız. Gerekirse `string(x)` / `int(x)`.
4. **Basit ve kısa tutun** — 4096 char / 256 AST-düğüm sınırı var; karmaşık mantığı birden çok kurala bölün.
5. **Test edin** — girdi→çıktı örneğiyle doğrulayın (yukarıdaki tablo formatı). Reddedilirse hata-kodu (§8) yönü gösterir.

---

## 8. "Kendi metodumu (fonksiyonumu) oluşturmak istersem?" — mevcut durum + uzatma noktası

Bu, en çok sorulan konu. Dürüst ve net cevap **mevcut MVP durumuna** göre:

### 8.1 Bugün (MVP): kullanıcı-tanımlı özel fonksiyon YOK
Sandbox **saf-stdlib-only**'dir. İfade içinde **kendi Go/JS fonksiyonunuzu tanımlayıp çağıramazsınız** ve
**dinamik lookup fonksiyonu** (ör. `lookup("...")`) yoktur — bu bilinçli bir güvenlik kararıdır (ADR-E2.2 §2.3).

**Peki ihtiyacınız olan değer stdlib'de yoksa?** → İki yol vardır:
- **(a) Motor-inject binding (önerilen, bugün mümkün):** İhtiyaç duyduğunuz değeri (parent-değer, ilişkili-kayıt,
  hesaplanmış-referans) motor **önceden çözer** ve ifadeye bir **değişken** olarak verir (§6). İfadeniz onu hazır bulur.
  Yani "yeni metod" yerine "yeni **binding**" — daha güvenli, aynı sonuç.
- **(b) İfadeyi parçalayın:** Karmaşık bir hesabı, mevcut stdlib + değişkenlerle birden çok basit ifadeye bölün.

### 8.2 Geliştirici uzatma-noktası (kod seviyesi, bugün stdlib-dışı fonksiyon EKLENMEZ)
Motora yeni bir **saf fonksiyon** eklemek teknik olarak `cel.Function(...)` ile compile-ortamına whitelist eklemekle olur —
ama bu **kullanıcı-yüzeyi değil, kod-değişikliğidir** ve MVP'de bilinçli olarak **kapalıdır** (hard-gate: her yeni host-fn
kendi güvenlik-review'undan geçmeli). Yani "kendi metodunu ekleme" = **bir geliştirme/onay konusu**, ekrandan yapılan bir işlem değil.

### 8.3 Gelecek (post-MVP): iki genişleme yolu — planlı ama henüz tetiklenmemiş
- **Küratörlü dinamik-lookup host-fonksiyonu:** Gerçek dinamik-lookup ihtiyacı çıkarsa, RLS-checked, küratörlü bir host-fn
  **kendi review'uyla** eklenebilir (ADR-E2.2 §2.3 post-MVP genişlemesi).
- **Gerçek "kod" (plugin/SDK):** Kullanıcının keyfi kod yüklemesi (Y3) — açıldığında **out-of-process WASM izolasyonu**
  (`wazero`) zorunlu; MVP'de kapalı, talep-güdümlü (PI-3+). (ADR-E2.2 §4)

> **Özet:** Bugün "yeni metod" = **motor-inject binding** (veri sağlama) yoluyla karşılanır; kod-seviyesi yeni-fonksiyon
> ve kullanıcı-plugin'i **planlı ama onay/review-gate arkasında**, MVP'de kapalıdır.

---

## 9. Hata mesajları (kategoriler)

İfade başarısız olursa, kullanıcıya **redakte** bir kategori döner (detay yalnız server-side audit'te):

| Kod | Anlamı | Tipik neden |
|---|---|---|
| `compile_error` | Derleme/tip hatası | tanımsız değişken, sözdizimi, tip-uyumsuzluğu |
| `too_complex` | Karmaşıklık bütçesi aşıldı | program çok uzun / AST çok derin/çok düğümlü |
| `timeout` | Süre aşıldı (100ms) | ağır ifade |
| `cost_exceeded` | Hesap-maliyeti tavanı aşıldı | büyük liste üzerinde ağır işlem |
| `runtime_error` | Çalışma-anı hatası | ör. tip-dönüşüm hatası |

---

## 10. Özet (cheat-sheet)

- İfade = **CEL** metni + **değişkenler** → **sonuç**.
- Yalnız **verilen değişkenler + saf stdlib** görünür (deny-by-default).
- **Ağ/dosya/DB/komut yok**, **döngü yok**, **now()/rastgele varsayılan yok**, **kaynak-limitli**.
- Yeni değer lazımsa → **motor-inject binding** (yeni "metod" değil).
- Örnek: `amount > threshold ? "needs_approval" : "auto"`

---

*SSOT: ADR-E2.2 (`docs/adr/ADR-E2.2-sandbox-credential-encryption.md`, ACCEPTED) · impl: `apps/api-go/internal/domain/expr/evaluator.go`
(Story #80) · Feature #74. Bu döküman ifade **dili + sandbox**'ı anlatır; ürün-içi UI-bağlantısı (form-hesap/iş-kuralı ekranları)
ayrı dilim E2.2-S3'te. Hazırlayan: James (TL/SA, agent-207), 2026-08-28.*
