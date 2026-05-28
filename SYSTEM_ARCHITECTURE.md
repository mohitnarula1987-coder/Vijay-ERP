# System Architecture — Vijay Trading ERP

_Last updated at the v1.0-production milestone._

## 1. Big picture

```
   Phone / Browser
        │
        ▼
  GitHub Pages  ──serves──►  index.html (static app + PWA)
        ▲
        │ auto-deploy on every commit
   GitHub repo (main branch)  ← single source of truth
        ▲                         │
        │ (developer commits)     │ app makes API calls at runtime
                                  ▼
                          Supabase (database + REST API)
```

The frontend is **fully static** — there is no application server. All data lives in **Supabase** and is fetched directly by the browser at runtime. GitHub Pages only serves files; it never touches the data.

## 2. Components

| Component       | Detail                                                                 |
|-----------------|------------------------------------------------------------------------|
| GitHub repo     | `github.com/mohitnarula1987-coder/Vijay-ERP` (public). `main` = prod.  |
| Live URL        | `https://mohitnarula1987-coder.github.io/Vijay-ERP/`                   |
| Hosting         | GitHub Pages, "Deploy from a branch" → `main` / root `/`.              |
| Backend         | Supabase project ref `vbprpviyhyqllmaodejz`, region `ap-south-1` (Mumbai). |
| API key         | A Supabase **publishable (anon)** key is embedded in `index.html`. This key is meant for client use; real protection comes from RLS (see §6). |
| Offsite backup  | A frozen copy of the source is stored in the owner's Google Drive.     |

## 3. Application modules (tabs in `index.html`)
Dashboard, Stock, Voucher, History, Reports, Alerts, Barcode, Tools.
Login is currently a **demo login** (phone number + PIN `1234`) — to be replaced with real auth in Phase 1.

## 4. Data model (current)
- **16 items**, across **3 warehouses**: `4No` (largest), `50No`, `W3`.
- **15 items** currently flagged **critical / reorder** (e.g. Aashirwad Atta, Chana Dal, Haldi Powder, etc.).
- Warehouse stock columns are presently **hardcoded for 3 warehouses** — this is the main thing that must become dynamic before multi-warehouse expansion (Phase 2).

## 5. What is "frozen" (don't casually edit)
- Core layout CSS variables in `index.html` (marked "FROZEN" in the file).
- The Supabase connection details (URL + key) — moving these wrong breaks data loading.
- File locations at root (see README golden rule #4).

## 6. Known limitations → Phase 1 backlog
- **RLS (Row Level Security) is currently OFF** in Supabase. With the key public, this means the database is effectively open. **Highest-priority security item.**
- Repo is **public** (the key is visible). The real fix is RLS + proper roles, not hiding the repo.
- **Demo auth** (PIN 1234) — needs real per-user login + roles (Owner / Manager / Staff).
- Single monolithic `index.html` — fine now, but will be refactored into modules (Phase 2) before heavy scaling.

> ⚠️ Do **not** enable RLS naively — the app currently relies on RLS being off. Enabling it without writing matching policies will break data loading. This needs a planned migration (Phase 1).
