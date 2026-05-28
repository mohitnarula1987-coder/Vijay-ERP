# Deployment Rules & Flow — Vijay Trading ERP

**There is exactly ONE way to deploy. Follow it. No exceptions.**

## The only deploy flow
```
Edit / add a file  →  Commit to `main`  →  GitHub Pages auto-builds  →  Live in ~1–2 min
```
- No manual uploads to Netlify, Vercel, or any host. Ever.
- No drag-drop deploys. Ever.
- GitHub Pages rebuilds automatically on every push to `main`.

## Branch strategy
| Branch    | Purpose                                  | Deploys to live? |
|-----------|------------------------------------------|------------------|
| `main`    | **Production** — what customers/staff use | ✅ Yes (auto)    |
| `staging` | Testing risky changes safely             | ❌ No            |

**Rule:** anything risky (layout changes, new modules, big edits) goes to `staging` first. Only merge into `main` once it's verified.

## Pre-deploy checklist (run through this before committing to `main`)
- [ ] Is there a recent **restore point** (Release tag)? If this is a big change, create one first.
- [ ] Did I test the change on `staging` (or at least review it carefully)?
- [ ] Am I editing the **right file**, at the repo **root** (not creating a duplicate elsewhere)?
- [ ] Did I avoid moving `index.html` / PWA files out of root?
- [ ] After deploy: open the live URL and confirm the dashboard + data load.

## Accidental-overwrite protection
- Treat `main` as sacred. For big work, branch off (`staging` or a `feature/...` branch) and merge back.
- Keep Release tags (e.g. `v1.0-production`, `v1.1`, …) at each stable milestone — they are permanent, downloadable snapshots.
- The Google Drive frozen copy is the offsite backup of last resort.

## Cache / versioning safety
- The service worker (`sw.js`) is intentionally **no-cache (pass-through)**. This means every push shows up immediately — no stale screens. **Do not** add aggressive caching to `sw.js` without a versioning + cache-busting plan, or users will see old versions.
- If you ever add caching later: bump a `CACHE_VERSION` string in `sw.js` on every release so old caches are cleared.

## When something breaks after a deploy
Go straight to `RECOVERY_GUIDE.md` and roll back. Don't debug on production under pressure — restore the last good version first, then investigate calmly.
