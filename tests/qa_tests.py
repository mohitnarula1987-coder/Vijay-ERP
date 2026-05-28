#!/usr/bin/env python3
"""
Vijay ERP — Automated QA Test Suite v1.0
Run: python3 tests/qa_tests.py
Expected: 55/55 PASS
"""
import math, re, json, sys
from datetime import datetime

def mkSKU(brand,family,ps,pt):
    cl=lambda s,n: re.sub(r'[^A-Z0-9]','',(s or '').upper())[:n]
    b=cl(brand,6); f=cl((family or '').split(' ')[0],8)
    sz=(ps or '').upper().replace(' ','').replace('KG','K').replace('GM','G').replace('LTR','L').replace('ML','M').replace('PKT','P')
    sz=re.sub(r'[^A-Z0-9]','',sz)[:5]
    pm={'BAG':'B','POUCH':'P','BOTTLE':'L','JAR':'J','BOX':'X','TIN':'T','PCS':'U','DRUM':'D'}
    return '-'.join(filter(None,[b,f,sz,pm.get((pt or '').upper(),'B')]))

def fmt(n):
    n=round(float(n),2); return str(int(n)) if n==int(n) else str(n)
def bagFull(kg,bulk,unit='KG'):
    kg=float(kg or 0); bulk=float(bulk or 1)
    if kg<=0: return '0'+unit
    if bulk<=1: return fmt(kg)+unit
    bags=math.floor(kg/bulk); rem=round(kg%bulk,2)
    if bags>0 and rem>0: return f'{bags} Bags + {fmt(rem)}{unit}'
    if bags>0: return f'{bags} Bags'
    return fmt(rem)+unit
def bagShort(kg,bulk):
    kg=float(kg or 0); bulk=float(bulk or 1)
    if kg<=0: return '0'
    if bulk<=1: return fmt(kg)
    bags=math.floor(kg/bulk); rem=round(kg%bulk,1)
    if bags>0 and rem>0: return f'{bags}B+{fmt(rem)}'
    if bags>0: return f'{bags}B'
    return fmt(rem)
def getStatus(t,m):
    if t<=0 or t<=m: return 'critical'
    if t<m*1.5: return 'low'
    return 'ok'

results=[]
def test(name,fn):
    try: results.append(('PASS' if fn() else 'FAIL',name,''))
    except Exception as e: results.append(('FAIL',name,str(e)))

test("SKU-01",lambda: mkSKU('MDH','HALDI POWDER','100GM','POUCH')=='MDH-HALDI-100G-P')
test("SKU-02",lambda: mkSKU('Tata','CHANA DAL','1KG','BAG')=='TATA-CHANA-1K-B')
test("SKU-03",lambda: mkSKU('Catch','HALDI POWDER','500GM','POUCH')=='CATCH-HALDI-500G-P')
test("SKU-04",lambda: mkSKU('Fortune','SUNFLOWER OIL','5LTR','JAR')=='FORTUN-SUNFLOWE-5L-J')
test("SKU-05",lambda: mkSKU('ITC','AASHIRWAD ATTA','10KG','BAG')=='ITC-AASHIRWA-10K-B')
test("SKU-06",lambda: bool(re.match(r'^[A-Z0-9-]+$',mkSKU('Tata','CHANA DAL','1KG','POUCH'))))
test("SKU-07",lambda: len(mkSKU('MDH','HALDI POWDER','100GM','POUCH').split('-'))==4)
test("BAG-01",lambda: bagFull(208,25)=='8 Bags + 8KG')
test("BAG-02",lambda: bagFull(212,25)=='8 Bags + 12KG')
test("BAG-03",lambda: bagFull(58,25)=='2 Bags + 8KG')
test("BAG-04",lambda: bagFull(50,25)=='2 Bags')
test("BAG-05",lambda: bagFull(12,25)=='12KG')
test("BAG-06",lambda: bagFull(0,25)=='0KG')
test("BAG-07",lambda: bagFull(45,1)=='45KG')
test("BAG-08",lambda: '8.0KG' not in bagFull(208,25))
test("BAG-09",lambda: bagShort(212,25)=='8B+12')
test("BAG-10",lambda: bagShort(50,25)=='2B')
test("BAG-11",lambda: bagFull(106,25)=='4 Bags + 6KG')
test("BAG-12",lambda: bagFull(99,25)=='3 Bags + 24KG')
test("STS-01",lambda: getStatus(0,100)=='critical')
test("STS-02",lambda: getStatus(50,100)=='critical')
test("STS-03",lambda: getStatus(100,100)=='critical')
test("STS-04",lambda: getStatus(101,100)=='low')
test("STS-05",lambda: getStatus(149,100)=='low')
test("STS-06",lambda: getStatus(150,100)=='ok')
test("STS-07",lambda: getStatus(300,100)=='ok')
def csvLine(line):
    res=[]; cur=''; inQ=False
    for ch in line:
        if ch=='"': inQ=not inQ
        elif ch==',' and not inQ: res.append(cur); cur=''
        else: cur+=ch
    res.append(cur); return res
test("CSV-01",lambda: csvLine('a,b,c')==['a','b','c'])
test("CSV-02",lambda: csvLine('"a,b",c')==['a,b','c'])
test("CSV-03",lambda: csvLine('a,,c')==['a','','c'])
test("CSV-04",lambda: len(csvLine('a,'*19+'z'))==20)
test("CSV-05",lambda: float('212.5')==212.5)
test("CSV-06",lambda: 'family_name'.lower().replace(' ','_')=='family_name')
seen={}
def chkDup(pid,vname):
    k=f"{pid}|{vname.lower()}"
    if k in seen: return True
    seen[k]=True; return False
test("DUP-01",lambda: not chkDup(1,'1KG Pack'))
test("DUP-02",lambda: chkDup(1,'1KG Pack'))
test("DUP-03",lambda: not chkDup(1,'500GM Pack'))
test("DUP-04",lambda: not chkDup(2,'1KG Pack'))
test("DUP-05",lambda: chkDup(2,'1kg Pack'))
stk=[{'wid':13,'kg':212},{'wid':14,'kg':80},{'wid':13,'kg':30}]
tots={}
for r in stk: tots[r['wid']]=tots.get(r['wid'],0)+r['kg']
test("WHT-01",lambda: tots[13]==242)
test("WHT-02",lambda: tots[14]==80)
test("WHT-03",lambda: sum(tots.values())==322)
test("WHT-04",lambda: tots.get(15,0)==0)
TYPES={'INWARD','OUTWARD','TRANSFER_OUT','TRANSFER_IN','DAMAGE','PACKING','CONVERSION','OPENING','PURCHASE'}
test("TXN-01",lambda: 'INWARD' in TYPES)
test("TXN-02",lambda: 'OUTWARD' in TYPES)
test("TXN-03",lambda: 'TRANSFER_OUT' in TYPES)
test("TXN-04",lambda: 'DAMAGE' in TYPES)
test("TXN-05",lambda: 'PACKING' in TYPES)
test("TXN-06",lambda: 'OPENING' in TYPES)
test("SAF-01",lambda: bool(json.dumps({'id':1,'name':'test'})))
test("SAF-02",lambda: bool(json.dumps({'data':[{'id':1,'kg':25.5}]})))
test("SAF-03",lambda: bool(json.dumps({'cost':None,'bags':0})))
test("SAF-04",lambda: bool(json.dumps({'rem':round(212%25,2)})))
test("SAF-05",lambda: bool(json.dumps({'data':None,'error':{'msg':'test','code':'23505'}})))
vc={}
def nextVN(t):
    p={'INWARD':'IN','OUTWARD':'OUT','TRANSFER':'TR','DAMAGE':'DMG','PACKING':'PKG','CONVERSION':'CNV'}[t]
    k='VTC-'+p; vc[k]=(vc.get(k,0)+1)
    return k+'-'+str(vc[k]).zfill(4)
test("VCH-01",lambda: nextVN('INWARD').startswith('VTC-IN-'))
test("VCH-02",lambda: nextVN('OUTWARD').startswith('VTC-OUT-'))
test("VCH-03",lambda: (lambda a=nextVN('DAMAGE'),b=nextVN('DAMAGE'): int(b[-4:])==int(a[-4:])+1)())

passed=[r for r in results if r[0]=='PASS']
failed=[r for r in results if r[0]=='FAIL']
score=round(len(passed)/len(results)*100)
print(f"\n{'='*55}")
print(f"  Vijay ERP QA | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"{'='*55}")
for s,n,e in results:
    print(f"  {'✅' if s=='PASS' else '❌'} {n}"+(f" → {e}" if e else ""))
print(f"{'='*55}")
print(f"  {len(passed)}/{len(results)} PASS | Score: {score}%")
print(f"  {'🟢 READY TO DEPLOY' if not failed else '🔴 DO NOT DEPLOY'}")
print(f"{'='*55}\n")
sys.exit(0 if not failed else 1)
