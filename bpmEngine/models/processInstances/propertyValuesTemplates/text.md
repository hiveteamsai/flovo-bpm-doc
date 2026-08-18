# Değer Şablonu — `text` (Text — statik)

> **Durum:** 🟡 TASLAK — ilk çıkarım; düzenlenecek.
> **Kapsam:** `text` (statik label) değerinin **`InstanceValue.data` içindeki şekli** + fihrist yansıması.
> **Alan davranışı:** → [`../../../service-settings/properties.md`](../../../service-settings/properties.md) §3.9 · **model:** [`../../service-settings/property.md`](../../service-settings/property.md).

## 1. JSONB değer şekli — `data["<code>"]`
**Değer YOK — girdi değildir.** `text`, başlık/açıklama gösteren **statik label**'dır; içeriği `defaultValue` (tasarım-zamanı, `Property`'de) + tipografi ayarlarıdır (`fontSize`/`isBold`/`textAlignment`…). Kullanıcı bir değer üretmez → `data`'da **anahtar bulunmaz** (anahtar-her-zaman-bulunur kuralının **istisnası** — değer saklamayan statik tip; → [`../instance-value.md`](../instance-value.md)).

## 2. Projeksiyon — `projectToAttr`
- **Projekte edilmez** (`projectToAttr=false` — anlamsız; saklanan/aranan bir değer yok).

## 3. Notlar
- `defaultValue` metni çevrilecekse `Property.translationCode` üzerinden (statik etiket çevirisi) — bu, **değer** değil **tanım** çevirisidir.

*Oluşturma: 2026-08-06.*
