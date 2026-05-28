# Vijay ERP — Step-by-Step Deploy Guide
# File: docs/DEPLOY_GUIDE.md
# Total setup time: ~30 minutes

═══════════════════════════════════════════════
PHASE A — ONE-TIME SETUP (30 minutes)
═══════════════════════════════════════════════

STEP 1: Create GitHub Account (if not done)
────────────────────────────────────────────
1. Go to github.com/signup
2. Create account with: mohitnarula1987@gmail.com
3. Verify email

STEP 2: Create Private Repository
────────────────────────────────────────────
1. github.com → + → New repository
2. Name: vijay-erp
3. Private: ✅ YES
4. Add README: ✅ YES
5. Click: Create repository

STEP 3: Get Netlify Auth Token
────────────────────────────────────────────
1. app.netlify.com → Your avatar → User settings
2. Applications → Personal access tokens
3. New access token → Name: "GitHub Actions"
4. ⚠️ COPY AND SAVE THIS TOKEN (shown only once!)

STEP 4: Get Netlify Site ID
────────────────────────────────────────────
1. app.netlify.com → venerable-speculoos-8f80cb site
2. Site configuration → General → Site information
3. Copy: Site ID (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

STEP 5: Add GitHub Secrets
────────────────────────────────────────────
1. Your GitHub repo → Settings → Secrets → Actions
2. Add these 4 secrets:

   Name: NETLIFY_AUTH_TOKEN
   Value: (paste token from Step 3)

   Name: NETLIFY_SITE_ID
   Value: (paste Site ID from Step 4)

   Name: SUPABASE_URL
   Value: https://vbprpviyhyqllmaodejz.supabase.co

   Name: SUPABASE_KEY
   Value: sb_publishable_7E5EVnRSIeQ4w2oxtmzutQ_YVGsLydc

STEP 6: Upload Files to GitHub
────────────────────────────────────────────
Option A — GitHub Web Upload (Easiest):
1. Your repo → Add file → Upload files
2. Upload all files from the Google Drive folder
3. Commit: "Initial production setup"

Option B — Git CLI:
   git clone https://github.com/YOUR_USERNAME/vijay-erp.git
   cd vijay-erp
   (copy all files here)
   git add .
   git commit -m "Initial production setup"
   git push origin main

STEP 7: Create Folder Structure
────────────────────────────────────────────
Create these folders in your repo:
   .github/workflows/    ← paste deploy.yml here
   tests/                ← paste qa_tests.py here
   scripts/              ← paste backup.py, health_check.py here
   docs/                 ← paste ARCHITECTURE.md etc here
   backups/              ← create empty file: .gitkeep

STEP 8: Connect Netlify to GitHub
────────────────────────────────────────────
1. app.netlify.com → venerable-speculoos-8f80cb
2. Site configuration → Build & deploy → Continuous deployment
3. Connect to Git provider → GitHub
4. Authorize → Select repo: vijay-erp
5. Production branch: main
6. Build command: (LEAVE EMPTY)
7. Publish directory: .
8. Save

STEP 9: Test the Pipeline
────────────────────────────────────────────
1. Make any small change in index.html
   (e.g., add a comment: <!-- v2.0 -->)
2. Push to main branch
3. GitHub → Actions tab → Watch pipeline run
4. Should see: QA → Backup → Deploy → Health Check
5. Visit: venerable-speculoos-8f80cb.netlify.app/status

═══════════════════════════════════════════════
PHASE B — DAILY WORKFLOW
═══════════════════════════════════════════════

Making a Small Fix:
────────────────────────────────────────────
1. Edit file on GitHub directly (github.com → file → edit)
2. Commit to main branch
3. Wait 2-3 minutes → Auto deploys
4. Check deploy-status.html

Making a Big Feature:
────────────────────────────────────────────
1. Create branch: dev
2. Make changes on dev
3. Test on preview URL
4. Create Pull Request: dev → main
5. QA runs automatically
6. Merge → Production deploy

Emergency Rollback:
────────────────────────────────────────────
1. Netlify → Site → Deploys
2. Find last working deploy
3. Click "Publish deploy"
4. ✅ Site restored in 30 seconds
5. ⚠️ Stock data NOT affected (stays in Supabase)

═══════════════════════════════════════════════
PHASE C — MONITORING
═══════════════════════════════════════════════

Check deploy status:
→ venerable-speculoos-8f80cb.netlify.app/status

Check GitHub Actions:
→ github.com/YOUR_USERNAME/vijay-erp/actions

Check Netlify deploys:
→ app.netlify.com → site → Deploys

Check Supabase data:
→ supabase.com → vbprpviyhyqllmaodejz → Table Editor
