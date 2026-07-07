# Flovo — Organizasyon (Organization) Tasarımı

> **Durum:** 🟢 DETAYLANIYOR
> **Amaç:** Flovo'yu kullanan **kurumu (tenant)** temsil eden **organizasyon** varlığını tanımlamak. Kullanıcılar,
> servisler, çeviriler ve ayarlar bir organizasyona bağlıdır.
>
> **İlişki:** `translation.md` kayıtları `organizationId` ile organizasyona bağlanır; `defaultLang`, çeviri
> çözümlemesinde **aktif dilin varsayılanını** belirler.

---

## 0. Organizasyon Nedir?
Bir **organizasyon**, Flovo'yu kullanan **kurumdur (tenant)**. Verinin en üst **kapsayıcısıdır**: kullanıcılar,
servisler (formlar/süreçler), durumlar, çeviriler vb. bir organizasyona aittir. Organizasyonlar birbirinden
**izoledir** — biri diğerinin verisini görüntüleyemez/güncelleyemez.

> **Not:** Model **başlangıç** halidir; ihtiyaç oldukça alan eklenir (fatura, plan, bölge, güvenlik vb.).

---

## 1. Organizasyon Veri Modeli (başlangıç)
| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `id` | int | Otomatik | Organizasyon ID'si (`translation.organizationId` buraya bağlanır) |
| `code` | string | Evet | Organizasyon **kodu** — **benzersiz (unique)**; **dış referanslarda** (API/entegrasyon) bu alan kullanılır |
| `name` | string | Evet | Organizasyon **adı** (kullanıcıya görünen) |
| `defaultLang` | string | Evet | **Varsayılan dil** — **sabit dil seti** (`tr` / `en` / `de`) içinden seçilir; aktif dilin başlangıç değeri |
| `logoUrl` | string | Hayır | Organizasyon **logosu** (görsel URL) |
| `idleTimeoutMinute` | int | Evet | **Boşta kalma zaman aşımı** (dakika). **null olamaz, varsayılan `0`.** `0` = zaman aşımı **uygulanmaz** (disable); `> 0` iken süre dolunca oturum kilitlenir |
| `adminUserIds` | List\<int\> | Evet | **Organizasyon adminleri** — en az **1 aktif**; yetki yapılandırmasını yalnız bunlar değiştirir, **tüm yetkilere** sahiptir (→ `permissions.md`) |

---

## 2. Alan Davranışları
- **`code`** — Organizasyonun **benzersiz** kimliğidir; API/entegrasyon gibi **dış referanslarda** `id` yerine `code` kullanılır.
- **`defaultLang`** — **Sabit dil seti** (`tr`/`en`/`de`) içinden seçilir. Kullanıcının aktif dili yoksa/belirsizse
  çeviriler bu dile göre çözülür (→ `translation.md` §3).
- **`logoUrl`** — Uygulama başlığı, raporlar ve bildirimlerde organizasyon markası için kullanılır.
- **`idleTimeoutMinute`** — Güvenlik için hareketsizlik süresi. **null olamaz; varsayılan `0`.** `0` iken zaman aşımı
  **uygulanmaz** (disable). `> 0` iken kullanıcı o kadar dakika işlem yapmazsa oturum kilitlenir.

---

## 3. İlişkiler
- **Çeviri (`translation.md`):** `translation.organizationId → organization.id`. `organizationId = null` çeviriler
  **ortak (Flovo)**; organizasyona ait olanlar bu organizasyonundur. `defaultLang` çözümlemede varsayılan dili verir.
- **Kullanıcılar / servisler / durumlar:** organizasyona bağlıdır (izolasyon). _(Kullanıcı modeli ayrıca ele alınacak.)_

---

## 4. Yetkilendirme (Permissions)
Yetkiler **organizasyon bazında** yönetilir; eski **kullanıcı bazında `authorizationLevel`** kaldırıldı. Ayrıntı → **`permissions.md`**.
- **`adminUsers`** — organizasyon adminleri (**en az 1 aktif**). Yetki yapılandırmasını **yalnız adminler** değiştirir;
  adminler **tüm yetkilere** sahiptir; **yetki yapılandırmasını** yalnız adminler değiştirir (yapısal veri erişimi `organizationSettings` grubuyla).
- **Grup-bazlı yetkiler** (her biri bir **kullanıcı grubu** ile; seçilen grubun üyeleri yetkiyi alır):
  **kullanıcı yerine geçme** · **organizasyon ayarları erişimi** · **servis ayarları erişimi** · **tüm raporları görme**.

> Bu ayarlar **Organization** varlığında tutulur ve organizasyon ayarları sayfasında listelenir
> (model: `../models/organization-settings/organization.md`).

---

## 5. Açık Kararlar / Sorular
> **Açık sorular tek yerde:** Bu dokümanın açık kararları/soruları, tutarsızlığı önlemek için **yalnız** merkezi
> [`todo.md`](../todo.md) dosyasında toplanır (önceliklendirilmiş tüm-doküman listesi). İlgili maddeler orada `(organization §..)`
> atfıyla bulunur; verilen kararlar bu dokümanın **gövdesinde** anlatılır.

---

## 6. Notlar / Ham Düşünceler
> _(Buraya ham düşünceler; sonra yukarı işlenir.)_

---

*Oluşturma: 2026-07-01.*
