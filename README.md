# Vijay Trading ERP

Warehouse & inventory operating system for **Vijay Trading Company**, Abohar (Punjab).

## 🔴 LIVE PRODUCTION
**https://mohitnarula1987-coder.github.io/Vijay-ERP/**

- Installable on phones as an app (PWA) → "Add to Home Screen".
- Auto-deploy: every commit to the `main` branch goes live in ~1–2 minutes.
- Latest verified restore point: GitHub Release **`v1.0-production`**.

## Locked stack (do not change without a written plan)
| Layer            | Choice                                            |
|------------------|---------------------------------------------------|
| Frontend         | Static HTML / CSS / JS (`index.html`)             |
| Backend          | Supabase (PostgreSQL + REST), region ap-south-1   |
| Source control   | GitHub — `main` = production                      |
| Hosting / deploy | GitHub Pages (auto-deploy from `main`, root `/`)  |
| Mobile           | PWA — installable, full-screen app mode           |

## ⚠️ Golden rules (read before touching anything)
1. **Production lives on the `main` branch.** Test risky changes on `staging` first.
2. **Never deploy manually** (no drag-drop to any host). The ONLY deploy path is: commit to `main` → GitHub Pages.
3. **Before any big change, create a restore point** (a GitHub Release). See `docs/RECOVERY_GUIDE.md`.
4. **Keep app files at the repo ROOT** (`index.html`, `importer.html`, `manifest.json`, `sw.js`, `icon-*.png`). Moving them into a folder **breaks the live link and all installed phone apps.**
5. **Retired files go to `/archive`** — never deleted blindly.

## Repository layout
```
/                      ← live app (served by GitHub Pages from root)
  index.html           ← main ERP (≈ 92 KB, single file)
  importer.html        ← data importer tool
  manifest.json        ← PWA app manifest
  sw.js                ← service worker (no-cache, keeps updates instant)
  icon-192.png         ← app icon
  icon-512.png         ← app icon
/docs                  ← documentation (this folder)
/archive               ← retired / historical files (kept, not deleted)
```

## Documentation
- `docs/SYSTEM_ARCHITECTURE.md` — how every piece fits together.
- `docs/DEPLOYMENT_RULES.md` — how deploys work + the deploy checklist.
- `docs/RECOVERY_GUIDE.md` — rollback & emergency restore.

---
*Owner: Mohit Narula. This is business-critical infrastructure — change carefully.*
