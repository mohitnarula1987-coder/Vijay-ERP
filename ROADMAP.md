# Vijay Trading ERP — Roadmap & To-Do

_The master plan. Pick items as time allows, in order of priority.
**Golden rule before any big item: create a restore point (Release) + test on `staging` first.**_

---

## ✅ DONE — Phase 0 (Foundation & Safety)
- Locked stack: Static HTML + Supabase + GitHub + GitHub Pages + PWA.
- Auto-deploy: commit to `main` → live in ~1–2 min. No manual deploys.
- Live URL: https://mohitnarula1987-coder.github.io/Vijay-ERP/
- PWA files in place (manifest, service worker, icons).
- Restore point: Release `v1.0-production`.
- Branches: `main` (production) + `staging` (testing).
- Documentation pack (README, ARCHITECTURE, DEPLOYMENT_RULES, RECOVERY_GUIDE).
- Repo cleaned of all junk; github-pages deployment green.

---

## 🔸 IMMEDIATE POLISH (low effort, do anytime)
| # | Task | Why | Risk |
|---|------|-----|------|
| 1 | Install app on each staff phone (Safari/Chrome → "Add to Home Screen") | App icon + full-screen on phones | None |
| 2 | Create a new restore point `v1.1` of the current clean state | Snapshot of the cleaned repo | None |
| 3 | (Optional) Move docs into a `/docs` folder + fix README links | Tidier structure | None |
| 4 | (Optional) Add iOS splash-screen images (`apple-touch-startup-image`) | Polished launch on iPhone | Low |
| 5 | Decommission the OLD Netlify live site (fanciful-fudge, on nitin's account) once confident GitHub Pages is the only live URL | Removes a second live URL = avoids future confusion | Low — keep as fallback for a few days first |

---

## 🔴 PHASE 1 — SECURITY (HIGHEST PRIORITY — do this next)
> ⚠️ Right now Supabase **RLS is OFF** and the key is public → the database is effectively open to anyone. This is the most important fix.

| # | Task | Notes |
|---|------|-------|
| 1 | Enable Supabase **RLS** with proper policies | **Careful:** the app currently relies on RLS being OFF. Enabling it without matching policies WILL break data loading. Needs a planned migration + testing on staging. |
| 2 | Real authentication (replace demo phone + PIN `1234`) | Per-user login via Supabase Auth |
| 3 | Role-based access: **Owner / Manager / Staff** | Different permissions per role |
| 4 | Secrets / API review | Publishable key is OK client-side; ensure NO service-role/admin keys ever land in the repo or browser |
| 5 | Turn on Supabase **scheduled database backups** | Protects the actual business data (separate from code backups) |

---

## 🟠 PHASE 2 — Scaling Refactor
| # | Task | Why |
|---|------|-----|
| 1 | Make warehouse stock columns **dynamic** (currently hardcoded for 3 warehouses) | Required before multi-warehouse |
| 2 | Refactor monolithic `index.html` into a **modular** app (e.g. React/Vite) | Maintainable as features grow |
| 3 | Code-quality pass: reusable components, naming standards, version comments, inline docs | "Future-developer friendly" |

---

## 🟢 PHASE 3+ — Feature Modules (after security + scaling base)
- Barcode scanner integration
- Thermal printing (labels / invoices)
- Audit logs (who changed what, when)
- Purchase + ledger modules
- Inventory forecasting (reorder prediction)
- Packing / dispatch automation
- Multi-warehouse expansion
- Warehouse CCTV + AI integration
- (Optional) Custom domain, e.g. `erp.vijaytrading.com` → GitHub Pages

---

## 🔁 ONGOING HABITS (keep doing forever)
1. **Before any big change:** create a Release tag (restore point).
2. **Test risky changes on `staging`** first, then merge to `main`.
3. **Never deploy manually** — only commit → GitHub Pages.
4. **Monthly:** download the latest source zip → save a dated copy in Google Drive.
5. **If something breaks:** restore from the latest Release first (see `RECOVERY_GUIDE.md`), debug later.

---
_Owner: Mohit Narula. Update this file as items are completed._
