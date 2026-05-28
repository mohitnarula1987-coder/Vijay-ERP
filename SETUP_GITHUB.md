# Vijay ERP — Git Repository Setup Guide
# File: SETUP_GITHUB.md

## Step 1 — Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `vijay-erp`
3. Visibility: **Private** (important!)
4. Initialize: ✅ Add README
5. Click "Create repository"

---

## Step 2 — Repository Folder Structure

```
vijay-erp/
├── index.html              ← Main ERP dashboard
├── importer.html           ← CSV Importer
├── deploy-status.html      ← Deployment status UI
├── netlify.toml            ← Netlify config
├── README.md
├── FROZEN.md               ← Architecture rules
│
├── .github/
│   └── workflows/
│       ├── deploy.yml      ← Main CI/CD pipeline
│       └── pr-check.yml    ← PR validation
│
├── tests/
│   ├── qa_tests.py         ← 55 automated tests
│   └── requirements.txt    ← requests
│
├── scripts/
│   ├── backup.py           ← Pre-deploy backup
│   ├── health_check.py     ← Post-deploy verify
│   └── log_deploy.py       ← Deployment logger
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEPLOY_GUIDE.md
│   └── QA_REPORT.md
│
└── backups/                ← Auto-created, gitignored
    └── .gitkeep
```

---

## Step 3 — Branch Protection Rules

Go to: Settings → Branches → Add rule

### For `main` branch:
- ✅ Require a pull request before merging
- ✅ Require status checks to pass:
  - `qa-tests` (required)
  - `backup` (required)
- ✅ Require branches to be up to date
- ✅ Do not allow bypassing above settings
- ✅ Restrict who can push: (Owner only)

### For `dev` branch:
- ✅ Require status checks: `qa-tests`
- No merge restrictions (free to push)

---

## Step 4 — GitHub Secrets (Required)

Go to: Settings → Secrets and variables → Actions → New repository secret

| Secret Name | Value | Where to get |
|---|---|---|
| `NETLIFY_AUTH_TOKEN` | Your token | netlify.com → User settings → Applications → Personal access tokens |
| `NETLIFY_SITE_ID` | Site API ID | Netlify → Site → Site settings → General → Site ID |
| `SUPABASE_URL` | https://vbprpviyhyqllmaodejz.supabase.co | Already known |
| `SUPABASE_KEY` | sb_publishable_7E5EVnRSIeQ4w2oxtmzutQ_YVGsLydc | Already known |

---

## Step 5 — Connect Netlify to GitHub

1. Login to netlify.com
2. Site: venerable-speculoos-8f80cb
3. Site configuration → Build & deploy → Continuous deployment
4. Link to Git provider → GitHub
5. Select repo: `vijay-erp`
6. Production branch: `main`
7. Build command: *(leave empty)*
8. Publish directory: `.`
9. Save

---

## Step 6 — First Push

```bash
# Clone your new repo
git clone https://github.com/YOUR_USERNAME/vijay-erp.git
cd vijay-erp

# Create dev branch
git checkout -b dev

# Add all files
git add .
git commit -m "feat: initial production ERP setup"
git push origin dev

# Test the pipeline on dev first
# Check GitHub Actions tab → see if QA passes

# When dev is stable → merge to main
git checkout main
git merge dev
git push origin main
# This triggers PRODUCTION deploy automatically
```

---

## Step 7 — Netlify Get Auth Token

1. Go to: https://app.netlify.com/user/applications
2. Click "New access token"
3. Description: "Vijay ERP GitHub Actions"
4. Copy the token → add to GitHub Secrets as `NETLIFY_AUTH_TOKEN`

---

## Step 8 — Get Site ID

1. Go to your Netlify site dashboard
2. Site configuration → General
3. Copy "Site ID" (looks like: a1b2c3d4-...)
4. Add to GitHub Secrets as `NETLIFY_SITE_ID`

---

## Deployment Flow (After Setup)

```
You make a code change
        ↓
git commit + push to dev
        ↓
GitHub Actions triggers automatically
        ↓
QA Tests run (55 tests)
        ↓
   PASS?      FAIL?
     ↓           ↓
Backup runs   ❌ BLOCKED
     ↓           No deploy
Preview URL  Notification
     ↓
You test preview
     ↓
Create PR: dev → main
     ↓
QA runs again on PR
     ↓
Merge to main
     ↓
Auto production deploy
     ↓
Health check runs
     ↓
   PASS?      FAIL?
     ↓           ↓
✅ LIVE!    Auto rollback
```
