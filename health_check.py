#!/usr/bin/env python3
"""
Vijay ERP — Post-Deploy Health Check
File: scripts/health_check.py
Runs AFTER every deployment. Verifies site is up and data loads.
"""
import sys, time, requests

def check(url, name, expected=None, timeout=15):
    try:
        r = requests.get(url, timeout=timeout)
        ok = r.status_code == 200
        if expected and ok:
            ok = expected in r.text
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"  {status}  {name} ({r.status_code}, {r.elapsed.total_seconds():.2f}s)")
        return ok
    except Exception as e:
        print(f"  ❌ FAIL  {name} — {e}")
        return False

def main():
    site_url = sys.argv[1] if len(sys.argv) > 1 else 'https://venerable-speculoos-8f80cb.netlify.app'

    print(f"\n{'='*55}")
    print(f"  VIJAY ERP — POST-DEPLOY HEALTH CHECK")
    print(f"  Target: {site_url}")
    print(f"{'='*55}")

    # Wait for Netlify CDN propagation
    print("\n⏳ Waiting 15s for CDN propagation...")
    time.sleep(15)

    results = []

    # 1. Site loads
    results.append(check(site_url, "Site loads (200 OK)", "Vijay Trading ERP"))

    # 2. Critical JS libraries present
    results.append(check(site_url, "Supabase client present", "supabase"))
    results.append(check(site_url, "jsPDF present", "jspdf"))
    results.append(check(site_url, "Login screen present", "SIGN IN"))

    # 3. Check Supabase API directly
    sb_url = 'https://vbprpviyhyqllmaodejz.supabase.co/rest/v1/warehouses?select=id,name'
    sb_headers = {
        'apikey': 'sb_publishable_7E5EVnRSIeQ4w2oxtmzutQ_YVGsLydc',
        'Authorization': 'Bearer sb_publishable_7E5EVnRSIeQ4w2oxtmzutQ_YVGsLydc'
    }
    try:
        r = requests.get(sb_url, headers=sb_headers, timeout=10)
        data = r.json()
        ok = r.status_code == 200 and len(data) >= 3
        print(f"  {'✅ PASS' if ok else '❌ FAIL'}  Supabase DB ({len(data)} warehouses)")
        results.append(ok)
    except Exception as e:
        print(f"  ❌ FAIL  Supabase DB — {e}")
        results.append(False)

    # 4. Check stock data exists
    try:
        sb_stock = 'https://vbprpviyhyqllmaodejz.supabase.co/rest/v1/warehouse_stock?select=variant_id&limit=1'
        r = requests.get(sb_stock, headers=sb_headers, timeout=10)
        ok = r.status_code == 200 and len(r.json()) > 0
        print(f"  {'✅ PASS' if ok else '❌ FAIL'}  Stock data accessible")
        results.append(ok)
    except Exception as e:
        print(f"  ❌ FAIL  Stock data — {e}")
        results.append(False)

    passed = sum(results)
    total = len(results)
    score = round(passed/total*100)

    print(f"\n{'='*55}")
    print(f"  RESULTS: {passed}/{total} checks passed ({score}%)")

    if score == 100:
        print(f"  ✅ HEALTH CHECK PASSED — Site is live and healthy")
        print(f"{'='*55}\n")
        sys.exit(0)
    else:
        print(f"  ❌ HEALTH CHECK FAILED — Rollback recommended")
        print(f"{'='*55}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
