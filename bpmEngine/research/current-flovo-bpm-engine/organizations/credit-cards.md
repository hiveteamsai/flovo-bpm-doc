# Kredi Kartları (Credit Cards)

## Genel Bakış

Kredi kartları, organizasyonun harcama/masraf süreçlerinde kullanılan kurumsal kartları tanımlar. Kartlar bir şirkete ve isteğe bağlı olarak bir kullanıcıya bağlanabilir; ayrıca ortak (herkesin kullanabileceği) kart olarak işaretlenebilir.

---

## Veri Modeli (AccountCreditCardDto)

| Alan | Tip | Açıklama |
|------|-----|----------|
| `id` | int | Kart ID'si |
| `accountId` | String | Hesap ID'si |
| `accountCompanyId` | int | Bağlı şirket ID'si |
| `kod` | String | Kart kodu |
| `tanim` | String | Kart adı/tanımı |
| `cardNumber` | String | Kart numarası |
| `userId` | int | Bağlı kullanıcı ID'si |
| `username` | String | Bağlı kullanıcı e-postası |
| `isCommonCard` | bool | Ortak kart mı (herkes kullanabilir) |
| `selected` | bool | Seçili mi |
| `status` | bool | Aktiflik durumu |
| `syncronizationStatus` | bool | Senkronizasyon durumu |

`AccountCreditCardDto`, `IOrganizationParameter` arayüzünü uygular. `getUserCode` getter'ı, `username` üzerinden ağ (Network) verisinden kullanıcı kodunu çözer.

---

## Liste Yanıtı (GetAccountCreditCardsDto)

| Alan | Açıklama |
|------|----------|
| `accountCreditCardDtos` | Kredi kartları listesi |
| `accountCompanyDtos` | Şirket seçimi için şirketler |

---

## Çalışma Prensibi

1. **Tanımlama:** Kod, tanım, kart numarası ve şirket ile kart oluşturulur.
2. **Kullanıcı Ataması:** Kart bir kullanıcıya (`userId` / `username`) atanabilir. Kullanıcı modelinde `userAccountCreditCardDtos` ile bu kartlar tutulur.
3. **Ortak Kart:** `isCommonCard: true` ile kart tüm kullanıcılara açılır.
4. **Masraf Süreçleri:** Harcama/masraf formlarında ödeme aracı olarak seçilir.

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetAccountCreditCards` | POST | Kredi kartlarını listele |
| `AddOrUpdateAccountCreditCard` | POST | Kart ekle/güncelle |
| `DeleteAccountCreditCard/{id}` | POST | Kart sil |

---

## Dosya Yapısı

```
lib/Models/Settings/OrganizationSettings/
└── AccountCreditCardDto.dart   # GetAccountCreditCardsDto, AccountCreditCardDto

lib/Pages/Settings/OrganizationSettings/CreditCards/
├── CreditCardsPage.dart          # Liste sayfası
└── CreditCardDetailPage.dart     # Detay/düzenleme sayfası
```
