#!/usr/bin/env python3
"""
Vijay ERP — Pre-Deploy Backup Script
File: scripts/backup.py
Runs BEFORE every deployment. Exports all stock + transaction data.
"""
import os, json, csv, requests
from datetime import datetime, timezone

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://vbprpviyhyqllmaodejz.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'sb_publishable_7E5EVnRSIeQ4w2oxtmzutQ_YVGsLydc')

HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

def fetch(table, params=''):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

def write_csv(filename, data, fields=None):
    if not data:
        print(f"  ⚠️  No data for {filename}")
        return 0
    os.makedirs('backups', exist_ok=True)
    fields = fields or list(data[0].keys())
    with open(f'backups/{filename}', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(data)
    return len(data)

def main():
    ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    print(f"\n{'='*55}")
    print(f"  VIJAY ERP — PRE-DEPLOY BACKUP")
    print(f"  Timestamp: {ts}")
    print(f"{'='*55}")

    summary = {'timestamp': ts, 'tables': {}}

    # 1. Warehouse Stock
    print("\n📦 Backing up warehouse_stock...")
    try:
        stock = fetch('warehouse_stock', 'select=*,variants(item_id,sku,variant_name),warehouses(name)')
        n = write_csv(f'stock_{ts}.csv', stock)
        summary['tables']['warehouse_stock'] = n
        print(f"  ✅ {n} rows")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        summary['tables']['warehouse_stock'] = f'ERROR: {e}'

    # 2. Stock Transactions
    print("\n📋 Backing up transactions...")
    try:
        txns = fetch('stock_transactions',
            'select=*,variants(item_id,variant_name),warehouses(name)'
            '&order=created_at.desc&limit=10000')
        n = write_csv(f'transactions_{ts}.csv', txns)
        summary['tables']['stock_transactions'] = n
        print(f"  ✅ {n} rows")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # 3. Variants Master
    print("\n🏷️  Backing up variants master...")
    try:
        variants = fetch('variants',
            'select=*,products(family_name,brands(name),categories(name))')
        n = write_csv(f'variants_{ts}.csv', variants)
        summary['tables']['variants'] = n
        print(f"  ✅ {n} rows")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # 4. Warehouses
    print("\n🏭 Backing up warehouses...")
    try:
        warehouses = fetch('warehouses', 'select=*')
        n = write_csv(f'warehouses_{ts}.csv', warehouses)
        summary['tables']['warehouses'] = n
        print(f"  ✅ {n} rows")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # 5. Write summary JSON
    os.makedirs('backups', exist_ok=True)
    with open(f'backups/backup_summary_{ts}.json', 'w') as f:
        json.dump(summary, f, indent=2)

    total = sum(v for v in summary['tables'].values() if isinstance(v, int))
    print(f"\n{'='*55}")
    print(f"  ✅ BACKUP COMPLETE")
    print(f"  Total rows backed up: {total}")
    print(f"  Files saved in: backups/")
    print(f"{'='*55}\n")

    return summary

if __name__ == '__main__':
    main()
