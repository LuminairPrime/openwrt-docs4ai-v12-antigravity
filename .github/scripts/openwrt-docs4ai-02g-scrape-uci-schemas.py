"""
openwrt-docs4ai-02g-scrape-uci-schemas.py

Purpose  : Scrape the openwrt UCI configuration schemas from package defaults.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs)
           WORKDIR (default: ./tmp)
Outputs  : $OUTDIR/openwrt-uci-docs/*.md
"""

import os
import glob
import datetime

OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
WORKDIR = os.environ.get("WORKDIR", os.path.join(os.getcwd(), "tmp"))
OUT_DIR = os.path.join(OUTDIR, "openwrt-uci-docs")

print("[02g] Scrape UCI default configurations")

package_dir = os.path.join(WORKDIR, "repo-openwrt", "package")
if not os.path.isdir(package_dir):
    print(f"[02g] SKIP: repository not found at {package_dir}")
    exit(0)

os.makedirs(OUT_DIR, exist_ok=True)

schema_files = []
# Find all etc/config/ files
for root, dirs, files in os.walk(package_dir):
    if "etc" in dirs and "config" in os.listdir(os.path.join(root, "etc")):
        config_dir = os.path.join(root, "etc", "config")
        for f in os.listdir(config_dir):
            full_path = os.path.join(config_dir, f)
            if os.path.isfile(full_path):
                schema_files.append((f, full_path))

if not schema_files:
    print("[02g] WARN: No UCI schema files found")
    exit(1)

ts = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
saved = 0

for schema_name, fpath in schema_files:
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Optional: Filter out pure bash logic, but for defaults, keeping it raw is generally fine
        if "config " not in content:
            continue
            
        rel_path = os.path.relpath(fpath, os.path.join(WORKDIR, "repo-openwrt"))
        out_file = os.path.join(OUT_DIR, f"uci-{schema_name}.md")
        
        with open(out_file, "w", encoding="utf-8", newline="\n") as out:
            out.write("---\n")
            out.write(f"module: uci_{schema_name}\n")
            out.write(f"title: UCI Schema: {schema_name}\n")
            out.write(f"source: {rel_path}\n")
            out.write(f"generated: {ts}\n")
            out.write("---\n\n")
            out.write(f"# UCI Default Schema: `{schema_name}`\n\n")
            out.write(f"> **Source:** `{rel_path}`\n\n")
            out.write("```uci\n")
            out.write(content.strip())
            out.write("\n```\n")
            
        saved += 1
        
    except Exception as e:
        print(f"[02g] WARN: Could not process {fpath}: {e}")

print(f"[02g] OK: Wrote {saved} UCI default schemas")
