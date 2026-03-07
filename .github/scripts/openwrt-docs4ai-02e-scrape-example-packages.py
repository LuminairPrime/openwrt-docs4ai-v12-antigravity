"""
openwrt-docs4ai-02e-scrape-example-packages.py

Purpose  : Copy curated LuCI application examples from the LuCI repo.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs) — generated output destination
           WORKDIR (default: ./tmp) — where to find cloned source repos
           SKIP_BUILDROOT ("true" to skip entirely)
Outputs  : $OUTDIR/openwrt-examples/<app>/*.uc, *.js
           $OUTDIR/openwrt-examples/llms.txt
Deps     : None (pure Python file copy)
Notes    : Copies only .uc and .js files from 4 curated apps.
           Previously a bash script using GNU-only cp --parents;
           now uses shutil for cross-platform compatibility (B10).
"""

import os
import sys
import shutil
import datetime

sys.stdout.reconfigure(line_buffering=True)

OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
WORKDIR = os.environ.get("WORKDIR", os.path.join(os.getcwd(), "tmp"))
SKIP_BUILDROOT = os.environ.get("SKIP_BUILDROOT", "false").lower() == "true"

if SKIP_BUILDROOT:
    print("[02e] SKIP: Example extraction (SKIP_BUILDROOT=true)")
    sys.exit(0)

print("[02e] Extract curated LuCI application examples")

SRC = os.path.join(WORKDIR, "repo-luci", "applications")
OUT = os.path.join(OUTDIR, "openwrt-examples")
os.makedirs(OUT, exist_ok=True)

TS = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
LUCI_URL = "https://github.com/openwrt/luci/tree/master/applications"
LUCI_COMMIT = os.environ.get("LUCI_COMMIT", "unknown")

# App metadata: name -> description
APPS = {
    "luci-app-example": "Hello world / baseline — minimum viable app; ucode<->JS bridge, ACL, UCI form, rpcd scaffolding",
    "luci-app-commands": "HTTP API / controller — custom endpoints in ucode/controller/, URL parsing, secure popen execution",
    "luci-app-ddns": "Standard config app — service state (init_enabled), rpcd microbus, deep UCI read/write",
    "luci-app-dockerman": "Advanced / streaming — UNIX socket communication, HTTP streaming, large JSON, multi-file ucode",
}

# Write llms.txt header
with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"# OpenWrt Curated LuCI Application Examples\n")
    f.write(f"# Source: {LUCI_URL}\n")
    f.write(f"# Generated: {TS} from LuCI commit {LUCI_COMMIT}\n")
    f.write("#\n")
    f.write("# Four apps selected for distinct pedagogical value. Together they cover the\n")
    f.write("# full range of modern LuCI development patterns. All files are raw upstream\n")
    f.write("# source code — unmodified, suitable for direct use as coding templates.\n")
    f.write("#\n")
    f.write("# Recommended reading order:\n")
    f.write("#   1. luci-app-example    — baseline structure and ucode<->JS bridge\n")
    f.write("#   2. luci-app-commands   — HTTP endpoints and controller pattern\n")
    f.write("#   3. luci-app-ddns       — config management and service state\n")
    f.write("#   4. luci-app-dockerman  — advanced sockets, streaming, multi-file\n")
    f.write("#\n## Application Files\n\n")


for app, desc in APPS.items():
    app_dir = os.path.join(SRC, app)
    if not os.path.isdir(app_dir):
        print(f"[02e] WARN: {app} not found at {app_dir} — skipping")
        with open(os.path.join(OUT, "llms.txt"), "a", encoding="utf-8", newline="\n") as f:
            f.write(f"\n## {app}\n# NOTE: Not found in upstream repo at generation time.\n\n")
        continue

    print(f"[02e] Extracting {app}...")
    dest_dir = os.path.join(OUT, app)
    os.makedirs(dest_dir, exist_ok=True)

    # Walk and copy .uc and .js files, preserving directory structure
    uc_count = 0
    js_count = 0
    copied_files = []

    for root, _, files in os.walk(app_dir):
        for fname in sorted(files):
            if not (fname.endswith(".uc") or fname.endswith(".js")):
                continue
            src_file = os.path.join(root, fname)
            # Compute relative path within the app directory
            rel = os.path.relpath(src_file, app_dir)
            dst_file = os.path.join(dest_dir, rel)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)
            copied_files.append(rel)
            if fname.endswith(".uc"):
                uc_count += 1
            else:
                js_count += 1

    # Write per-app section to llms.txt
    with open(os.path.join(OUT, "llms.txt"), "a", encoding="utf-8", newline="\n") as f:
        f.write(f"\n## {app}\n")
        f.write(f"# Pattern: {desc}\n")
        f.write(f"# Source: {LUCI_URL}/{app}\n")
        f.write(f"# Files: {uc_count} .uc (ucode backend), {js_count} .js (JavaScript frontend)\n")
        f.write("#\n# File tree:\n")
        for rel in sorted(copied_files):
            ext = os.path.splitext(rel)[1]
            ftype = "[ucode]" if ext == ".uc" else "[js]   "
            f.write(f"#   {ftype}  {rel}\n")
        f.write("#\n")
        for rel in sorted(copied_files):
            ext = os.path.splitext(rel)[1]
            ftype = "ucode backend" if ext == ".uc" else "JavaScript frontend"
            f.write(f"- [{app}/{rel}](/openwrt-examples/{app}/{rel}): {app} — {ftype}\n")
        f.write("\n")

    print(f"[02e] OK: {app} ({uc_count} .uc, {js_count} .js)")

print("[02e] Complete.")
