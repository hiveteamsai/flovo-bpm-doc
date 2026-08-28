# Enum — SubTextType

> **Kullanan model:** [`../service-settings/jsonTemplateModels/business-rule/data-source/fill-data-source-organization.md`](../service-settings/jsonTemplateModels/business-rule/data-source/fill-data-source-organization.md) · [`../service-settings/jsonTemplateModels/business-rule/data-source/fill-data-source-user.md`](../service-settings/jsonTemplateModels/business-rule/data-source/fill-data-source-user.md) — alan `subTextType`
> **Amaç:** `fillDataSource` ile doldurulan liste öğelerinin **alt metnini** (ikincil satır) hangi alandan alacağını belirler.

## Nedir?
Bir seçim listesinde her öğenin ana metninin **altında** gösterilecek küçük ikincil bilgiyi seçer (ör. kullanıcı adının altında departmanı).

## Değerler
| Değer | Alt metin |
|---|---|
| `code` | Kod. |
| `username` | Kullanıcı adı. |
| `department` | Departman. |
| `profession` | Unvan. |
| `ref1` | Serbest referans 1. |
| `ref2` | Serbest referans 2. |

## Notlar
- Eski koddaki yazım hatası **`departmant` → `department`** olarak düzeltildi (yeni motor).

*Oluşturma: 2026-08-26.*
