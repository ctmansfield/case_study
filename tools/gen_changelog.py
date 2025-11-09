#!/usr/bin/env python3
import re, pathlib, sys, datetime

src = pathlib.Path("meta/version_log.md")
dst = pathlib.Path("CHANGELOG.md")

if not src.exists():
    print("version_log missing; skipping"); sys.exit(0)

lines = src.read_text(encoding="utf-8").splitlines()
entries = []
for ln in lines:
    m = re.match(r"^\s*-\s*(\d{4}-\d{2}-\d{2})\s*—\s*(.+)$", ln)
    if m:
        date, text = m.groups()
        entries.append((date, text))

# group newest-first
entries.sort(key=lambda x: x[0], reverse=True)

out = []
out.append("# Changelog\n")
out.append("_Auto-generated from `meta/version_log.md`._\n")
curr = None
for date, text in entries:
    if date != curr:
        out.append(f"\n## {date}\n")
        curr = date
    out.append(f"- {text}")
dst.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"Wrote {dst}")
