"""
openwrt-docs4ai-02f-scrape-procd-api.py

Purpose  : Scrape the openwrt procd shell API documentation from procd.sh comments.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs)
           WORKDIR (default: ./tmp)
Outputs  : $OUTDIR/openwrt-procd-docs/procd-api.md
"""

import os
import re
import datetime

OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
WORKDIR = os.environ.get("WORKDIR", os.path.join(os.getcwd(), "tmp"))
OUT_DIR = os.path.join(OUTDIR, "openwrt-procd-docs")

print("[02f] Scrape procd init.d API documentation")

procd_sh_path = os.path.join(WORKDIR, "repo-openwrt", "package", "system", "procd", "files", "procd.sh")

if not os.path.isfile(procd_sh_path):
    print(f"[02f] SKIP: procd.sh not found at {procd_sh_path}")
    exit(0)

os.makedirs(OUT_DIR, exist_ok=True)

with open(procd_sh_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Extract the header block comments
doc_lines = []
for line in lines:
    if line.startswith("#"):
        doc_lines.append(line.lstrip("#").strip())
    elif not line.strip():
        # Keep going through empty lines until it stops being comments
        continue
    else:
        break # stopped being comments

markdown_content = "\n".join(doc_lines).strip()
if not markdown_content:
    print("[02f] WARN: Could not extract documentation from procd.sh")
    exit(1)

out_file = os.path.join(OUT_DIR, "procd-api.md")
ts = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")

with open(out_file, "w", encoding="utf-8", newline="\n") as f:
    f.write("---\n")
    f.write("module: procd\n")
    f.write("title: procd init.d API\n")
    f.write("source: package/system/procd/files/procd.sh\n")
    f.write(f"generated: {ts}\n")
    f.write("---\n\n")
    f.write("# procd init.d API Reference\n\n")
    f.write("> **Extracted from:** `procd.sh` block comments\n\n")
    f.write("```shell\n")
    f.write(markdown_content)
    f.write("\n```\n")

print(f"[02f] OK: Wrote procd-api.md ({len(doc_lines)} lines)")
