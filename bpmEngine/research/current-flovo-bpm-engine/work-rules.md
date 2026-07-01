# İş Kuralları (Work Rules)

## Genel Bakış

İş kuralları (WorkRule), form üzerinde dinamik davranışlar tanımlayan koşul-aksiyon tabanlı bir yapıdır. Belirli koşullar sağlandığında otomatik olarak tetiklenir ve form üzerinde değişiklikler yapar. Validasyon, değer atama, alan gizleme, veri kaynağı doldurma gibi işlemleri koşula bağlı olarak gerçekleştirir.

---

## Veri Modeli (WorkRuleDto)

### Temel Alanlar

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `id` | int | Otomatik | Kural ID'si |
| `accountId` | String | Evet | Hesap ID'si |
| `serviceId` | int | Evet | Servis ID'si |
| `code` | String | Evet | Kural kodu |
| `definition` | String | Evet | Kural tanımı |
| `icon` | String | Hayır | İkon |
| `environmentRestriction` | String | Hayır | Ortam kısıtlaması |
| `actionType` | ActionType | Evet | Kural aksiyon tipi |
| `workRuleRuntimeType` | WorkRuleRuntimeType | Hayır | Çalışma zamanı tipi |
| `workRuleConditionType` | KosulTuru | Hayır | Koşul türü (VE/VEYA) |
| `workRuleConditions` | List | Hayır | Koşul listesi |
| `activeViewProfiles` | List\<int\> | Hayır | Sadece bu profillerde çalış |
| `shouldNotWorkInReadonlyMode` | bool | Hayır | Salt okunur modda çalışmasın |

---

## Aksiyon Tipleri (ActionType)

İş kuralının tetiklendiğinde ne yapacağını belirler:

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `SetViewForFiels` | Alanlar için görünüm ayarla (visible/enabled/required) |
| 1 | `ChangeViewProfile` | Görüntüleme profili değiştir |
| 2 | `ApplyValidation` | Validasyon uygula |
| 3 | `ShowMessage` | Kullanıcıya mesaj göster |
| 4 | `AssignValueToField` | Alana değer ata |
| 5 | `FillDataSource` | Veri kaynağı doldur |
| 6 | `AssignValueToPropertyField` | Alan özelliğine değer ata |
| 7 | `SetStyle` | Dekorasyon/stil ayarla |

---

## Çalışma Zamanı Tipi (WorkRuleRuntimeType)

Kuralın ne zaman değerlendirileceğini belirler:

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `always` | Her zaman (form açıldığında ve her değişiklikte) |
| 1 | `firstOpening` | Sadece ilk açılışta |
| 2 | `whenChanging` | Sadece alan değiştiğinde |

---

## Koşul Türü (KosulTuru)

Birden fazla koşulun nasıl değerlendirileceğini belirler:

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `IfAllConditionAreProvided` | Tüm koşullar sağlanıyorsa (VE) |
| 1 | `IfAtLeastOneConditionProvided` | En az biri sağlanıyorsa (VEYA) |

---

## Koşul Yapısı (WorkRuleConditionDto)

Her koşul iki değerin karşılaştırılmasından oluşur:

| Alan | Tip | Açıklama |
|------|-----|----------|
| `referenceValue` | WorkRuleConditionCompareValueDto | Referans değer (sol taraf) |
| `valueToCompare` | WorkRuleConditionCompareValueDto | Karşılaştırılacak değer (sağ taraf) |
| `criteritionType` | CriteritionType | Karşılaştırma operatörü |
| `isConditionList` | bool | İç içe koşul grubu mu |
| `workRuleConditionType` | KosulTuru | Alt grup koşul türü |
| `workRuleConditions` | List | İç içe koşullar (recursive) |

### Karşılaştırma Değer Tipleri (WorkRuleConditionCompareType)

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `FormValue` | Form alanının değeri |
| 1 | `ViewProfile` | Aktif görüntüleme profili |
| 2 | `FixedValue` | Sabit değer |
| 3 | `FromCalculate` | Hesaplanmış değer (expression) |

### Karşılaştırma Operatörleri (CriteritionType)

| Operatör | Açıklama |
|----------|----------|
| Eşittir | = |
| Eşit Değildir | != |
| Boş | null/empty |
| Boş Değil | not null/not empty |
| Daha Büyük | > |
| Daha Büyük veya Eşit | >= |
| Daha Küçük | < |
| Daha Küçük veya Eşit | <= |
| İle Başlar | startsWith |
| İle Biter | endsWith |
| İçerir | contains |
| İçermez | not contains |

---

## Aksiyon Detayları

### 1. Alanlar İçin Görünüm Ayarla (SetViewForFields)

Belirli form alanlarının görünürlük, düzenlenebilirlik ve zorunluluk durumlarını değiştirir.

**Özellikler:**
- Hedef alanlar seçilir
- Her alan için `visible`, `enabled`, `required` ayarlanır

### 2. Validasyon Uygula (ApplyValidation)

Form üzerinde özel validasyon kuralı uygular. Koşul sağlanmazsa kullanıcıya hata mesajı gösterilir.

**Özellikler:**
- Validasyon mesajı tanımlanır
- Değer atama yöntemi ile dinamik mesaj oluşturulabilir

### 3. Mesaj Göster (ShowMessage)

Kullanıcıya bilgilendirme mesajı gösterir.

**Özellikler:**
- Başlık ve mesaj içeriği tanımlanır
- Dinamik değerler (hesaplama, alan değeri) kullanılabilir

### 4. Alana Değer Ata (AssignValueToField)

Bir form alanına otomatik değer atar.

**Değer Atama Yöntemleri (ValueAssignType):**

| Index | Enum | Açıklama |
|-------|------|----------|
| 0 | `FixedValue` | Sabit değer |
| 1 | `FieldValue` | Başka bir form alanının değeri |
| 2 | `FromCalculation` | Expression ile hesaplanmış değer |
| 3 | `FromDataSet` | Veri setinden |
| 4 | `FromEba` | Eba entegrasyonundan |
| 5 | `Search` | Arama ile |
| 6 | `Function` | Function çağrısı ile |

### 5. Veri Kaynağı Doldur (FillDataSource)

Modal liste, combobox gibi alanların veri kaynaklarını dinamik olarak doldurur.

**Kaynak Tipleri:**
- Organization Data (organizasyon verisi)
- User Data (kullanıcı verisi)
- Parametreli API çağrıları

### 6. Alan Özelliğine Değer Ata (AssignValueToPropertyField)

Form alanının kendisine değil, özellik bilgisine değer atar.

### 7. Dekorasyon Ayarla (SetStyle)

Alan veya formun görsel stilini değiştirir.

---

## Çalışma Prensibi

```
┌─────────────────────────────────────────┐
│         Form Açılır / Alan Değişir       │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│   WorkRuleRuntimeType kontrolü          │
│   (always / firstOpening / whenChanging)│
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│   ActiveViewProfiles kontrolü           │
│   (mevcut profil listede mi?)           │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│   Koşullar değerlendirilir              │
│   (VE/VEYA mantığı, recursive)          │
└─────────────────┬───────────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
    Koşul TRUE        Koşul FALSE
         │                 │
         ▼                 ▼
┌──────────────┐   ┌──────────────┐
│ Aksiyon      │   │ Aksiyon      │
│ Çalıştır     │   │ Çalışmaz     │
└──────────────┘   └──────────────┘
```

### Değerlendirme Sırası

1. Tüm iş kuralları sırasıyla değerlendirilir
2. `shouldNotWorkInReadonlyMode: true` ise salt okunur modda atlanır
3. `activeViewProfiles` dolu ise aktif profil kontrolü yapılır
4. Koşullar recursive olarak değerlendirilir (iç içe koşul grupları desteklenir)
5. Koşul sağlanırsa ilgili aksiyon tipi çalıştırılır

---

## API Endpoint'leri

| Endpoint | HTTP | Açıklama |
|----------|------|----------|
| `GetWorkRules` | POST | İş kurallarını listele |
| `AddOrUpdateWorkRule` | POST | İş kuralı ekle/güncelle |
| `DeleteWorkRule/{id}` | POST | İş kuralı sil |

### İstek Header'ları

```
accountId: string
solutionid: string
ServiceId: string
```

---

## Dosya Yapısı

```
lib/Models/Settings/FlvSettings/WorkRule/
├── WorkRule.dart                                    # Ana model + koşullar (part dosyaları dahil)
├── Enums/
│   ├── ActionType.dart                             # Aksiyon tipi enum
│   ├── CriteritionType.dart                        # Karşılaştırma operatörleri
│   ├── KosulTuru.dart                              # Koşul türü (VE/VEYA)
│   ├── ValueAssignType.dart                        # Değer atama yöntemi
│   ├── WorkRuleConditionReferenceValue.dart        # Karşılaştırma değer tipi
│   ├── WorkRuleRuntimeType.dart                    # Çalışma zamanı tipi
│   └── PropertyType.dart                           # Özellik tipi
├── ActionTypeSetViewForFieldsWorkRuleDto.dart      # Alan görünüm ayarı
├── ActionTypeApplyValidationWorkRuleDto.dart       # Validasyon
├── ActionTypeAssignValueToFieldWorkRuleDto.dart    # Değer atama
├── ActionTypeAssignValueToPropertyFieldWorkRuleDto.dart # Özellik değer atama
├── ActionTypeShowMessageWorkRuleDto.dart           # Mesaj göster
├── ActionTypeSetStyleWorkRuleDto.dart              # Stil ayarla
├── DataSetDto.dart                                 # Veri seti modeli
├── GetWorkRuleDataSetDto.dart                      # Veri seti API yanıtı
├── GetDatasetSourceInputDto.dart                   # Veri seti girdi modeli
└── FillDataSource/
    ├── ActionTypeFillDataSourceWorkRuleDto.dart    # Veri kaynağı doldurma
    ├── DataSource.dart                             # Veri kaynağı modeli
    ├── PropertyDataSourceFromOrganizationDataDto.dart # Organizasyon verisi
    └── PropertyDataSourceFromUserDataDto.dart      # Kullanıcı verisi

lib/Pages/Settings/FlvSettings/WorkRule/
├── WorkRuleSettingsPage.dart                       # Liste sayfası
├── WorkRuleDetailPage.dart                         # Kural detay sayfası
├── WorkRuleConditionDetailPage.dart                # Koşul detay sayfası
├── ConditionCompareValueDetailPage.dart            # Karşılaştırma değeri sayfası
├── ConditionView.dart                              # Koşul görünümü widget'ı
└── ActionTypeViews/
    ├── SetViewForFieldsView.dart                   # Alan görünüm UI
    ├── SetViewForFieldsDetailPage.dart             # Alan görünüm detay
    ├── ApplyValidayionView.dart                    # Validasyon UI
    ├── ShowMessageView.dart                        # Mesaj UI
    ├── SetStyleView.dart                           # Stil UI
    ├── AssignValueToPropertyFieldView.dart         # Özellik atama UI
    ├── AssignValueToField/
    │   ├── AssignValueToFieldView.dart             # Değer atama ana UI
    │   ├── AssignToValueDetailPage.dart            # Değer atama detay
    │   ├── FromCalculateView.dart                  # Hesaplama görünümü
    │   ├── FromFunctionView.dart                   # Function görünümü
    │   ├── FromDataSetView.dart                    # Veri seti görünümü
    │   └── FromDataSetParameterDetailPage.dart     # Veri seti parametre
    └── FillDataSource/
        ├── FillDataSourceView.dart                 # Veri kaynağı UI
        ├── FillDataSourceDetailPage.dart           # Veri kaynağı detay
        ├── FillDataSourceParametersView.dart       # Parametreler
        └── FillDataSourceParameterDetailPage.dart  # Parametre detay
```
