# Vijay ERP — Architecture Documentation
# File: docs/ARCHITECTURE.md

## System Overview

```
┌─────────────────────────────────────────────────────┐
│              VIJAY TRADING ERP — v2.0               │
│         Enterprise Grocery Warehouse System         │
└─────────────────────────────────────────────────────┘

┌──────────────┐    push     ┌──────────────────────┐
│   Developer  │ ──────────▶ │   GitHub Repository  │
│  (You/Team)  │             │   vijay-erp (Private)│
└──────────────┘             └──────────┬───────────┘
                                        │
                              GitHub Actions CI/CD
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
             ┌──────────┐      ┌──────────────┐    ┌──────────────┐
             │ QA Tests │      │ Pre-Deploy   │    │   Deploy to  │
             │ 55 tests │      │   Backup     │    │   Netlify    │
             │ Python   │      │   Supabase   │    │  CDN Edge    │
             └─────┬────┘      └──────────────┘    └──────┬───────┘
                   │                                       │
              PASS/FAIL                           Health Check
                   │                                       │
              FAIL → ❌                             FAIL → Rollback
              Block deploy                         Restore last stable
```

## Frontend (Netlify CDN)
```
venerable-speculoos-8f80cb.netlify.app
├── index.html          ← Single-page ERP application
├── importer.html       ← CSV bulk importer
├── deploy-status.html  ← CI/CD status dashboard
└── netlify.toml        ← Edge config + security headers
```

## Database (Supabase PostgreSQL)
```
Project: vbprpviyhyqllmaodejz
Region: ap-south-1 (Mumbai)

FROZEN TABLES (DO NOT ALTER SCHEMA):
├── brands              ← Tata, MDH, Catch, Fortune, ITC...
├── categories          ← Dal, Masala, Oil, Tea, Atta...
├── products            ← family_name + brand_id + category_id
├── variants            ← item_id, sku, bulk_pack_kg, min_stock
├── warehouses          ← id:13=4No, id:14=50No, id:15=W3
├── warehouse_stock     ← Live stock levels (bags+loose+total)
├── stock_transactions  ← All IN/OUT/TRANSFER/DAMAGE records
└── users               ← Phone + PIN + role

KEY TRIGGERS:
└── trg_apply_txn → auto-updates warehouse_stock after each transaction
```

## FROZEN ARCHITECTURE (Never Change)

### Warehouse IDs
| Name    | DB ID | Position |
|---------|-------|----------|
| 4No.    | 13    | 1        |
| 50No.   | 14    | 2        |
| W3      | 15    | 3        |

### SKU Format
```
BRAND-FAMILY-SIZE-PACKTYPE
MDH-HALDI-100G-P
TATA-CHANA-1K-B
FORTUN-SUNFLOWE-5L-J
```

### Bag Display Logic (No "loose" word)
```
bags = floor(total_kg / bulk_pack_kg)
rem  = total_kg % bulk_pack_kg
"8 Bags + 12KG"
```

### Status Logic
```
total <= min_stock  → CRITICAL
total < min * 1.5  → LOW
total >= min * 1.5  → OK
```

## CI/CD Pipeline

```
Code Change
    ↓
git push dev
    ↓
GitHub Actions
    ├── QA Tests (55 automated)
    ├── Backup (Supabase export)
    └── Preview Deploy (dev URL)
        ↓
        PR: dev → main
        ↓
    QA Tests again
        ↓
    Merge approved
        ↓
    Production Deploy
        ↓
    Health Check
        ↓
   PASS → ✅ LIVE
   FAIL → ⏪ Auto Rollback
```

## Security Model

```
Layer 1: GitHub (Private repo, branch protection)
Layer 2: GitHub Secrets (API keys never in code)
Layer 3: Netlify Headers (XSS, CSRF, clickjacking protection)
Layer 4: Supabase (Row Level Security, anon key limits)
Layer 5: Role-based UI (Owner/Manager/Supervisor/Staff)
Layer 6: PIN authentication (session-based)
```

## Data Safety Rules

1. Supabase data is NEVER touched by deployments
2. Rollback only affects frontend HTML/JS
3. Backup runs BEFORE every deploy (90-day retention)
4. Warehouse_stock trigger protects data integrity
5. All transactions are append-only (no deletes in UI)

## Scaling Path

```
Current:  1 business, 3 warehouses, ~20 items
Phase 2:  Multiple users, barcode scanning
Phase 3:  Billing module, dispatch, challans
Phase 4:  Multiple locations, franchise support
Phase 5:  AI demand forecasting
```
