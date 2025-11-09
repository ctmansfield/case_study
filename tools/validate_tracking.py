#!/usr/bin/env python3
import csv, sys, os

SCHEMA = ["date","context","histamine_score","folate_level","sbp","dbp","hr","fasting_glucose","sleep_deficit_hours","notes"]

def err(msg): print(f"[ERROR] {msg}"); return False

def main():
    path = "data/tracking/physio.csv"
    if not os.path.exists(path):
        print("[OK] No physio.csv yet.")
        return 0
    with open(path,newline='') as f:
        r=csv.DictReader(f)
        hdr=[h.strip().lower() for h in r.fieldnames]
        if hdr != SCHEMA:
            print(f"[ERROR] Bad header.\n expected: {SCHEMA}\n    found: {hdr}")
            return 1
        ok=True; ln=1
        for row in r:
            ln+=1
            def f(x):
                try: return float(x)
                except: return None
            # soft checks
            for k in ["histamine_score","folate_level","sbp","dbp","hr","fasting_glucose","sleep_deficit_hours"]:
                v=row.get(k,"").strip()
                if v=="":
                    continue
                val=f(v)
                if val is None:
                    print(f"[ERROR] line {ln}: {k} not numeric -> '{v}'"); ok=False
            # range hints (non-fatal)
            sbp=f(row.get("sbp","")); dbp=f(row.get("dbp","")); hr=f(row.get("hr",""))
            if sbp and not (70<=sbp<=250): print(f"[WARN] line {ln}: sbp {sbp} out of typical range")
            if dbp and not (40<=dbp<=150): print(f"[WARN] line {ln}: dbp {dbp} out of typical range")
            if hr  and not (30<=hr <=200): print(f"[WARN] line {ln}: hr {hr} out of typical range")
        if ok:
            print("[OK] physio.csv validated.")
            return 0
        return 1

if __name__=="__main__":
    sys.exit(main())
