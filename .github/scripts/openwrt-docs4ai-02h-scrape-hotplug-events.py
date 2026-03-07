"""
openwrt-docs4ai-02h-scrape-hotplug-events.py

Purpose  : Scrape OpenWrt netifd and core hotplug.d event handlers to reveal environment variables.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs)
           WORKDIR (default: ./tmp)
Outputs  : $OUTDIR/openwrt-hotplug-docs/netifd-hotplug-events.md
"""

import os
import glob
import datetime

OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
WORKDIR = os.environ.get("WORKDIR", os.path.join(os.getcwd(), "tmp"))
OUT_DIR = os.path.join(OUTDIR, "openwrt-hotplug-docs")

print("[02h] Scrape hotplug.d events")

package_dir = os.path.join(WORKDIR, "repo-openwrt", "package")
if not os.path.isdir(package_dir):
    print(f"[02h] SKIP: repository not found at {package_dir}")
    exit(0)

os.makedirs(OUT_DIR, exist_ok=True)

hotplug_files = []
# Find all etc/hotplug.d/ files
for root, dirs, files in os.walk(package_dir):
    if "etc" in dirs and "hotplug.d" in os.listdir(os.path.join(root, "etc")):
        hotplug_dir = os.path.join(root, "etc", "hotplug.d")
        for subroot, _, fs in os.walk(hotplug_dir):
            for f in fs:
                full_path = os.path.join(subroot, f)
                if os.path.isfile(full_path):
                    hotplug_files.append((f, full_path, subroot))

if not hotplug_files:
    print("[02h] WARN: No hotplug event scripts found")
    exit(1)

ts = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
out_file = os.path.join(OUT_DIR, "netifd-hotplug-events.md")
saved = 0
total_lines = 0

with open(out_file, "w", encoding="utf-8", newline="\n") as out:
    out.write("---\n")
    out.write("module: hotplug_events\n")
    out.write("title: OpenWrt hotplug.d Event Handlers\n")
    out.write("source: package/**/etc/hotplug.d/*\n")
    out.write(f"generated: {ts}\n")
    out.write("---\n\n")
    out.write("# OpenWrt Core Hotplug Events\n\n")
    out.write("> **Extracted from:** default `etc/hotplug.d/` scripts across the OpenWrt repository\n")
    out.write("> **Note for LLMs:** Developers building apps use these scripts as templates. Analyze the `$ACTION`, `$INTERFACE`, and subsystem blocks to understand exactly which environment variables OpenWrt injects during hotplug events.\n\n")
    out.write("---\n\n")

    for f, fpath, subroot in sorted(hotplug_files):
        try:
            with open(fpath, "r", encoding="utf-8") as file:
                content = file.read().strip()
                
            if not content:
                continue
                
            rel_path = os.path.relpath(fpath, os.path.join(WORKDIR, "repo-openwrt", "package"))
            event_type = os.path.basename(subroot)
            
            out.write(f"## Event Category: `{event_type}` — File: `{rel_path}`\n\n")
            out.write("```shell\n")
            out.write(content)
            out.write("\n```\n\n---\n\n")
            
            saved += 1
            total_lines += content.count("\n") + 1
            
        except Exception as e:
            print(f"[02h] WARN: Could not process {fpath}: {e}")

print(f"[02h] OK: Wrote netifd-hotplug-events.md ({saved} scripts, {total_lines} lines)")
