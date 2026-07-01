# Flovo BPM Engine - Genel Dokümantasyon

## Giriş

Flovo BPM (Business Process Management) Engine, Pratico uygulamasının iş süreçleri yönetim motorudur. Formlar (servisler) üzerinde tanımlanan iş akışlarını yönetir, kullanıcı onaylarını koordine eder, koşullu dallanmaları işler ve form üzerinde dinamik davranışlar sağlar.

---

## Mimari Genel Bakış

```
┌─────────────────────────────────────────────────────────────────┐
│                        FLOVO BPM ENGINE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Properties │  │ View        │  │  Work Rules             │ │
│  │  (Alanlar)  │  │ Profiles    │  │  (İş Kuralları)         │ │
│  │             │  │ (Profiller) │  │                         │ │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘ │
│         │                │                       │              │
│         └────────────────┼───────────────────────┘              │
│                          │                                      │
│                          ▼                                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    FORM RUNTIME                            │  │
│  │  (Kullanıcı formu görüntüler ve düzenler)                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                          │                                      │
│                          ▼                                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              PROCESS STEPS (Süreç Akışı)                  │  │
│  │                                                           │  │
│  │  ┌─────┐    ┌──────┐    ┌─────────┐    ┌──────┐         │  │
│  │  │Start│───▶│User  │───▶│Condition│───▶│End   │         │  │
│  │  └─────┘    └──────┘    └─────────┘    └──────┘         │  │
│  │                                                           │  │
│  │  Actions ──────▶ Status Change                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Temel Kavramlar

### Servis (Service/Form)
BPM motorundaki temel birimdir. Bir servis, bir iş sürecinin tamamını temsil eder (örn: İzin Talebi, Satın Alma Talebi, Masraf Formu). Her servisin kendi alanları, süreç adımları, aksiyonları, durumları, iş kuralları ve görüntüleme profilleri vardır.

### Hesap (Account) & Çözüm (Solution)
- **Account:** Organizasyonu temsil eder
- **Solution:** Bir veya birden fazla servisi barındıran çözüm paketi

---

## Bileşenler ve İlişkileri

### 1. Form Alanları (Properties)
Form üzerindeki tüm giriş ve görüntüleme elemanlarıdır. 29 farklı kontrol tipi desteklenir.

**Detay:** [properties.md](./properties.md)

### 2. Görüntüleme Profilleri (View Profiles)
Formun farklı süreç adımlarında nasıl görüntüleneceğini kontrol eder. Alanların görünürlüğü, düzenlenebilirliği ve zorunluluğu profil bazlı belirlenir.

**Detay:** [view-profiles.md](./view-profiles.md)

### 3. İş Kuralları (Work Rules)
Form üzerinde koşula bağlı dinamik davranışlar tanımlar. Validasyon, değer atama, alan gizleme, veri kaynağı doldurma gibi 7 farklı aksiyon tipi desteklenir.

**Detay:** [work-rules.md](./work-rules.md)

### 4. Süreç Adımları (Process Steps)
İş akışının rotasını tanımlar. 15 farklı adım tipi ile karmaşık iş akışları modellenebilir.

**Detay:** [process-steps.md](./process-steps.md)

### 5. Aksiyonlar (Actions)
Kullanıcının süreç adımlarında gerçekleştirdiği eylemlerdir. Onaylamak, reddetmek, göndermek gibi işlemleri temsil eder.

**Detay:** [actions.md](./actions.md)

### 6. Durumlar (Statuses)
Kaydın mevcut aşamasını gösteren etiketlerdir. Aksiyon tetiklendiğinde durum otomatik değişir.

**Detay:** [statuses.md](./statuses.md)

---

## BPM Yaşam Döngüsü

### 1. Tasarım Zamanı (Design Time)

Sistem yöneticisi aşağıdaki sırayla BPM sürecini tasarlar:

```
1. Form Alanları Tanımla (Properties)
   └── Kontrol tipi, etiket, veri kaynağı, kısıtlamalar

2. Görüntüleme Profilleri Oluştur (View Profiles)
   └── Hangi alanlarda ne görünsün, düzenlensin, zorunlu olsun

3. İş Kuralları Tanımla (Work Rules)
   └── Koşul → Aksiyon (validasyon, değer atama, görünüm)

4. Aksiyonlar Tanımla (Actions)
   └── Kod, ikon, tip, davranış seçenekleri

5. Durumlar Tanımla (Statuses)
   └── Kod, ikon, tip

6. Süreç Adımları Tasarla (Process Steps)
   └── Adım sırası, tip, kullanıcı atama, aksiyon bağlama
```

### 2. Çalışma Zamanı (Runtime)

Kullanıcı bir kayıt oluşturduğunda veya mevcut bir kaydı açtığında:

```
┌─────────────────────────────────────────────────────┐
│ 1. KAYIT OLUŞTURMA                                  │
│    - Kullanıcı yeni kayıt başlatır                 │
│    - Süreç "Başlangıç" adımından başlar             │
│    - İlk görüntüleme profili yüklenir               │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│ 2. FORM RENDER                                      │
│    - Aktif profildeki alanlar render edilir          │
│    - İş kuralları (WorkRule) çalıştırılır           │
│      • Alanlar gizlenir/gösterilir                  │
│      • Değerler otomatik atanır                     │
│      • Veri kaynakları doldurulur                   │
│      • Validasyonlar hazırlanır                     │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│ 3. KULLANICI ETKİLEŞİMİ                            │
│    - Kullanıcı formu doldurur                       │
│    - Alan değiştiğinde iş kuralları tekrar çalışır  │
│    - Validasyonlar kontrol edilir                   │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│ 4. AKSİYON TETİKLEME                               │
│    - Kullanıcı aksiyona basar                       │
│    - Validasyon: Form geçerli mi?                   │
│    - Sebep: Gerekiyorsa sebep giriş ekranı          │
│    - Geçmiş: Gerekiyorsa akış geçmişi gösterilir   │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│ 5. SÜREÇ İLERLEME                                   │
│    - Kayıt hedef adıma (targetProcessStepId) geçer │
│    - Durum güncellenir (changeStatusId)             │
│    - Sonraki adım tipine göre:                      │
│      • Kullanıcı/Grup → Bildirim gönder, bekle     │
│      • Function → API çağrısı yap, devam et        │
│      • Karşılaştırma → Koşul değerlendir, dallan   │
│      • Bildirim → Bildirim gönder, devam et        │
│      • Süreç Bitişi → Süreci tamamla               │
└─────────────────────────────────────────────────────┘
```

### 3. Zaman Aşımı (Timeout)

Kullanıcı adımlarında belirlenen süre dolduğunda:
- Otomatik bildirim gönderilebilir
- Belirlenen aksiyonla otomatik ilerleme yapılabilir

---

## Bileşenler Arası İlişkiler

```
Properties ◄─────── View Profiles
    │                     │
    │                     │
    ▼                     ▼
Work Rules ──────► Form Runtime ◄──── Process Steps
                      │                     │
                      │                     │
                      ▼                     ▼
                  User Action ────────► Actions
                                           │
                                           ▼
                                       Statuses
```

| İlişki | Açıklama |
|--------|----------|
| Properties → View Profiles | Profiller hangi alanların nasıl gösterileceğini belirler |
| Properties → Work Rules | İş kuralları alan değerlerine göre tetiklenir |
| View Profiles → Work Rules | Kurallar belirli profillerde çalışacak şekilde kısıtlanabilir |
| View Profiles → Process Steps | Her adıma bir görüntüleme profili atanır |
| Process Steps → Actions | Her adımda kullanılacak aksiyonlar belirlenir |
| Actions → Statuses | Aksiyon tetiklendiğinde durum değişir |
| Actions → Process Steps | Aksiyon hedef adıma yönlendirir |

---

## Teknik Altyapı

### Backend İletişimi
Tüm BPM bileşenleri `RemoteApiService` üzerinden RESTful API çağrıları ile yönetilir. Ayrı bir BPM servis katmanı yoktur; iş mantığı backend'de çalışır, frontend ayar yönetimi ve görüntüleme sağlar.

### Ortak İstek Header'ları
Her API çağrısında:
```
accountId: string    (Hesap ID)
solutionid: string   (Çözüm ID)
ServiceId: string    (Servis ID)
```

### Veri Depolama
- Tüm konfigürasyon backend veritabanında saklanır
- Frontend sadece görüntüleme ve düzenleme arayüzü sağlar
- Değişiklikler anlık olarak backend'e gönderilir

### Çoklu Dil Desteği
- Tüm metin alanları çeviri desteğine sahiptir
- Bildirimler TR/EN olarak ayrı tanımlanabilir
- UI metinleri `BaseLanguage` → `TrLanguage`/`EnLanguage` ile yönetilir

### Platform Desteği
- Mobil (iOS/Android) ve Web platformlarında çalışır
- Web'de geniş ekran düzeni (ViewProfileSettingsDetailWebPage)
- Responsive tasarım (900px breakpoint)

---

## Dosya İndeksi

| Dosya | Konu |
|-------|------|
| [actions.md](./actions.md) | Aksiyonlar - tanımlama, tipler, davranışlar |
| [statuses.md](./statuses.md) | Durumlar - tanımlama, akış |
| [view-profiles.md](./view-profiles.md) | Görüntüleme profilleri - alan kontrolü, rapor |
| [work-rules.md](./work-rules.md) | İş kuralları - koşullar, aksiyon tipleri, çalışma mantığı |
| [properties.md](./properties.md) | Form alanları - kontrol tipleri, özellikler |
| [process-steps.md](./process-steps.md) | Süreç adımları - akış, adım tipleri |

---

## API Endpoint Özeti

### Properties (Form Alanları)
| Endpoint | Açıklama |
|----------|----------|
| `GetProperties` | Alanları listele |
| `AddOrUpdateProperty` | Alan ekle/güncelle |
| `DeleteProperty/{id}` | Alan sil |

### View Profiles (Profiller)
| Endpoint | Açıklama |
|----------|----------|
| `GetProcessViewProfiles` | Profilleri listele |
| `AddOrUpdateProcessViewProfile` | Profil ekle/güncelle |
| `DeleteProcessViewProfile/{id}` | Profil sil |

### Work Rules (İş Kuralları)
| Endpoint | Açıklama |
|----------|----------|
| `GetWorkRules` | Kuralları listele |
| `AddOrUpdateWorkRule` | Kural ekle/güncelle |
| `DeleteWorkRule/{id}` | Kural sil |

### Process Steps (Süreç Adımları)
| Endpoint | Açıklama |
|----------|----------|
| `GetProcessSteps` | Adımları listele |
| `AddOrUpdateProcessStep` | Adım ekle/güncelle |
| `DeleteProcessStep/{id}` | Adım sil |
| `AddOrUpdateProcessActionList` | Sıralama güncelle |

### Actions (Aksiyonlar)
| Endpoint | Açıklama |
|----------|----------|
| `GetProcessActions` | Aksiyonları listele |
| `AddOrUpdateProcessAction` | Aksiyon ekle/güncelle |
| `DeleteProcessAction/{id}` | Aksiyon sil |

### Statuses (Durumlar)
| Endpoint | Açıklama |
|----------|----------|
| `GetProcessStatuses` | Durumları listele |
| `AddOrUpdateProcessStatus` | Durum ekle/güncelle |
| `DeleteProcessStatus/{id}` | Durum sil |

### Process Step Conditions (Koşullar)
| Endpoint | Açıklama |
|----------|----------|
| `GetProcessStepCondition/{id}` | Koşul getir |
| `AddOrUpdateProcessStepCondition` | Koşul ekle/güncelle |
| `DeleteProcessStepCondition/{id}` | Koşul sil |
