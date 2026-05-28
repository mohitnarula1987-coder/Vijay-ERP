# Recovery & Disaster Restore Guide — Vijay Trading ERP

This is the "break glass in emergency" guide. **Stay calm. Production can always be restored** because every stable version is saved as a Release.

## Your safety nets (in order of ease)
1. **GitHub Releases** — each is a permanent, downloadable snapshot. Latest: `v1.0-production`.
2. **Git history** — every commit can be reverted.
3. **Google Drive frozen copy** — offsite backup of the source (last resort).

---

## Scenario A — "I made a bad change, the live site is broken"
**Fastest fix: revert the last commit.**
1. Go to the repo → click the **commit list** (the "N Commits" link, top of the file list).
2. Find the bad commit → open it → click **"Revert"** (or the `...` menu → Revert).
3. Confirm → commit the revert to `main`.
4. Wait ~1–2 min → GitHub Pages redeploys the previous good version.

## Scenario B — "I want to restore a known-good version (e.g. v1.0)"
1. Repo → **Releases** → open **`v1.0-production`**.
2. Download **Source code (zip)**.
3. Unzip on your PC.
4. Repo → **Add file → Upload files** → drag the restored files → commit to `main`.
5. Live site returns to that exact version in ~1–2 min.

## Scenario C — "I deleted a file by mistake"
- If not yet committed: just refresh, it's still there.
- If committed: use **Scenario A** (revert that commit) — the file comes back.

## Scenario D — "Data looks wrong / missing"
- This is a **Supabase** issue, NOT a deploy issue (the app code is fine).
- Do **not** redeploy. Log into Supabase → check the project `vbprpviyhyqllmaodejz` → Table editor / logs.
- Supabase keeps its own backups; restore data from there. (Set up Supabase scheduled backups in Phase 1.)

## Scenario E — "GitHub Pages link shows 404"
- Settings → Pages → confirm Source = "Deploy from a branch", Branch = `main` / root.
- Check the **Actions** / **Deployments** tab for a failed build; re-run if needed.
- The URL is case-sensitive: `.../Vijay-ERP/` (capital V-E, trailing slash).

---

## Routine backup habit (recommended)
- **At every stable milestone**, create a new Release tag (`v1.1`, `v1.2`, …) with a one-line note of what changed.
- **Monthly**, download the latest Source zip and save a dated copy to Google Drive.
- This gives you point-in-time restore for years.

## Key IDs to keep safe (owner only)
- GitHub repo: `mohitnarula1987-coder/Vijay-ERP`
- Live URL: `https://mohitnarula1987-coder.github.io/Vijay-ERP/`
- Supabase project ref: `vbprpviyhyqllmaodejz` (region ap-south-1)
- Restore point: Release `v1.0-production`

> The single most important habit: **make a restore point (Release) before any big change.** With that, nothing is ever truly lost.
