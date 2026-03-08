"""
Purpose: Scrape OpenWrt netifd and core hotplug.d event handlers.
Phase: Extraction
Layers: L0 -> L1
Inputs: tmp/repo-openwrt/package/**/etc/hotplug.d/*
Outputs: tmp/.L1-raw/openwrt-hotplug/*.md and .meta.json
Environment Variables: WORKDIR
Dependencies: lib.config, lib.extractor
Notes: Concatenates all discovered hotplug scripts into one reference document.
"""

import os
import glob
import datetime
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib import config, extractor

sys.stdout.reconfigure(line_buffering=True)

print("[02h] Scrape hotplug.d events")

package_dir = os.path.join(config.WORKDIR, "repo-openwrt", "package")
if not os.path.isdir(package_dir):
    print(f"[02h] SKIP: repository not found at {package_dir}")
    sys.exit(0)

hotplug_files = []
for root, dirs, files in os.walk(package_dir):
    if "etc" in dirs:
        etc_hotplug_dir = os.path.join(root, "etc", "hotplug.d")
        if os.path.isdir(etc_hotplug_dir):
            for subroot, _, fs in os.walk(etc_hotplug_dir):
                for f in fs:
                    full_path = os.path.join(subroot, f)
                    if os.path.isfile(full_path):
                        hotplug_files.append((f, full_path, subroot))

if not hotplug_files:
    print("[02h] FAIL: No hotplug event scripts found")
    sys.exit(1)

ts = datetime.datetime.now(datetime.UTC).isoformat()
saved = 0
total_lines = 0

content_lines = []
content_lines.append("# OpenWrt Core Hotplug Events\n")
content_lines.append("> **Extracted from:** default `etc/hotplug.d/` scripts across the OpenWrt repository\n")
content_lines.append("> **Note for LLMs:** Developers building apps use these scripts as templates. Analyze the `$ACTION`, `$INTERFACE`, and subsystem blocks to understand exactly which environment variables OpenWrt injects during hotplug events.\n\n---\n")

for f, fpath, subroot in sorted(hotplug_files):
    try:
        with open(fpath, "r", encoding="utf-8", errors="replace") as file:
            content = file.read().strip()
            
        if not content:
            continue
            
        rel_path = os.path.relpath(fpath, os.path.join(config.WORKDIR, "repo-openwrt", "package")).replace("\\", "/")
        event_type = os.path.basename(subroot)
        
        content_lines.append(f"## Event Category: `{event_type}` — File: `{rel_path}`\n")
        content_lines.append(extractor.wrap_code_block("Shell Script", content, "bash"))
        content_lines.append("\n---\n")
        
        saved += 1
        total_lines += content.count("\n") + 1
        
    except Exception as e:
        print(f"[02h] WARN: Could not process {fpath}: {e}")

slug = "netifd-hotplug-events"
metadata = {
    "extractor": "02h-scrape-hotplug-events.py",
    "origin_type": "hotplug_event",
    "module": "openwrt-hotplug",
    "slug": slug,
    "original_url": None,
    "language": "bash",
    "upstream_path": "package/**/etc/hotplug.d/*",
    "fetch_status": "success",
    "extraction_timestamp": ts
}

extractor.write_l1_markdown("openwrt-hotplug", "hotplug_event", slug, "\n".join(content_lines), metadata)

print(f"[02h] Complete: Wrote {slug} ({saved} scripts, {total_lines} lines)")
if saved == 0:
    print("[02h] FAIL: Zero output files generated. Exiting with error.")
    sys.exit(1)
