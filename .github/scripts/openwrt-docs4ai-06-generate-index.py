"""
openwrt-docs4ai-06-generate-index.py

Purpose  : Generate the root llms.txt index, CHANGES.md, and index.md for Pages.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs) — where to read/write
Outputs  : $OUTDIR/llms.txt      — root navigational index for LLMs
           $OUTDIR/CHANGES.md    — diff of changes since last commit
           $OUTDIR/index.md      — GitHub Pages landing page
Deps     : git (system binary, for CHANGES.md diff)
Notes    : Split from the original monolithic 05-finalize-publish.sh.
           CHANGES.md gracefully handles first-run (no prior commit to diff against).
"""

import os
import glob
import datetime
import subprocess
import sys

sys.stdout.reconfigure(line_buffering=True)

OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
TS = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")

print("[06] Generate indexes and change log")

# --- Env vars for commit metadata ---
UCODE_COMMIT   = os.environ.get("UCODE_COMMIT",   "unknown")
LUCI_COMMIT    = os.environ.get("LUCI_COMMIT",    "unknown")
OPENWRT_COMMIT = os.environ.get("OPENWRT_COMMIT", "unknown")


# ============================================================
# 1. Root llms.txt — aggregates all per-folder llms.txt files
# ============================================================

DATASETS = [
    ("ucode-docs",    "ucode Documentation",           "ucode-complete-reference.md",
     "https://github.com/jow-/ucode", UCODE_COMMIT),
    ("luci-docs",     "LuCI JS API Documentation",     "luci-jsapi-complete-reference.md",
     "https://github.com/openwrt/luci", LUCI_COMMIT),
    ("openwrt-wiki-docs", "OpenWrt Wiki Developer Docs", "openwrt-wiki-complete-reference.md",
     "https://openwrt.org/docs/", ""),
    ("openwrt-buildroot-docs", "OpenWrt Buildroot Packages", "openwrt-buildroot-complete-reference.md",
     "https://github.com/openwrt/openwrt", OPENWRT_COMMIT),
    ("openwrt-examples", "LuCI Application Examples",  "openwrt-examples-complete-reference.md",
     "https://github.com/openwrt/luci", LUCI_COMMIT),
]

llms_path = os.path.join(OUTDIR, "llms.txt")
with open(llms_path, "w", encoding="utf-8", newline="\n") as f:
    f.write("# openwrt-docs4ai — condensed OpenWrt documentation\n\n")
    f.write(f"> Generated: {TS}\n\n")
    f.write("This repository provides LLM-optimized documentation scraped from\n")
    f.write("multiple upstream OpenWrt sources. Two consumption modes:\n\n")
    f.write("1. **Complete references** — single files containing all docs per source\n")
    f.write("2. **Individual files** — per-module/per-page markdown files\n\n")
    f.write("---\n\n## Complete Reference Files\n\n")

    for subdir, label, ref_file, source_url, commit in DATASETS:
        ref_path = os.path.join(OUTDIR, ref_file)
        if os.path.isfile(ref_path):
            size_kb = os.path.getsize(ref_path) // 1024
            lines = sum(1 for _ in open(ref_path, encoding="utf-8"))
            f.write(f"- [{ref_file}](/{ref_file}): {label} ({lines} lines, {size_kb} KB)")
            if commit:
                f.write(f" — commit: {commit}")
            f.write("\n")
            
            skeleton_file = ref_file.replace("-complete-reference", "-skeleton")
            skeleton_path = os.path.join(OUTDIR, skeleton_file)
            if os.path.isfile(skeleton_path):
                skeleton_kb = os.path.getsize(skeleton_path) // 1024
                skeleton_lines = sum(1 for _ in open(skeleton_path, encoding="utf-8"))
                f.write(f"  - ⚡ [{skeleton_file}](/{skeleton_file}) (Skeleton/Headers Version — {skeleton_lines} lines, {skeleton_kb} KB)\n")

    f.write("\n## Documentation Directories\n\n")
    for subdir, label, _, source_url, _ in DATASETS:
        sub_llms = os.path.join(OUTDIR, subdir, "llms.txt")
        if os.path.isfile(sub_llms):
            # Count .md files, but for examples dir also count .js and .uc files
            md_count = len(glob.glob(os.path.join(OUTDIR, subdir, "*.md")))
            js_uc_count = 0
            for root, dirs, files in os.walk(os.path.join(OUTDIR, subdir)):
                for fn in files:
                    if fn.endswith(('.js', '.uc')):
                        js_uc_count += 1
            file_count = md_count + js_uc_count
            f.write(f"- [{subdir}/llms.txt](/{subdir}/llms.txt): {label} index ({file_count} files)\n")

    f.write(f"\n## Metadata\n\n")
    f.write(f"- [CHANGES.md](/CHANGES.md): What changed since last update\n")
    f.write(f"- Source: {', '.join(d[3] for d in DATASETS)}\n")

print(f"[06] OK: llms.txt")


# ============================================================
# 2. CHANGES.md — diff report
# ============================================================

changes_path = os.path.join(OUTDIR, "CHANGES.md")

# Check if git is tracking the output folder
try:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "openwrt-condensed-docs/llms.txt"],
        capture_output=True, text=True, cwd=os.path.dirname(OUTDIR) or "."
    )
    has_prior = (result.returncode == 0)
except Exception:
    has_prior = False

if has_prior:
    try:
        diff_result = subprocess.run(
            ["git", "diff", "--stat", "HEAD", "--", "openwrt-condensed-docs/"],
            capture_output=True, text=True, cwd=os.path.dirname(OUTDIR) or "."
        )
        diff_text = diff_result.stdout.strip()
    except Exception:
        diff_text = "(diff unavailable)"
else:
    diff_text = "(first run — no prior commit to diff against)"

with open(changes_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(f"# Changes\n\n> Generated: {TS}\n\n")
    f.write("## File Changes Since Last Commit\n\n```\n")
    f.write(diff_text if diff_text else "(no changes detected)")
    f.write("\n```\n")
    if not diff_text or diff_text == "(no changes detected)":
        f.write("\n> This file shows incremental changes between pipeline runs.\n")
        f.write("> On first generation or when upstream hasn't changed, no diff is shown.\n")
    f.write("\n## Source Commits\n\n")
    f.write(f"- ucode: `{UCODE_COMMIT}`\n")
    f.write(f"- LuCI: `{LUCI_COMMIT}`\n")
    f.write(f"- OpenWrt: `{OPENWRT_COMMIT}`\n")

print(f"[06] OK: CHANGES.md")


# ============================================================
# 3. index.md — GitHub Pages landing page
# ============================================================

index_path = os.path.join(OUTDIR, "index.md")
with open(index_path, "w", encoding="utf-8", newline="\n") as f:
    f.write("# openwrt-docs4ai\n\n")
    f.write("Condensed OpenWrt documentation, optimized for AI LLMs and developers.\n\n")
    f.write(f"*Last updated: {TS}*\n\n")
    f.write("## Quick Start\n\n")
    f.write("Point your LLM at [llms.txt](llms.txt) for the full index.\n\n")
    f.write("## Complete References (single-file, ready to feed to LLMs)\n\n")
    for subdir, label, ref_file, source_url, commit in DATASETS:
        ref_path = os.path.join(OUTDIR, ref_file)
        if os.path.isfile(ref_path):
            f.write(f"- [{ref_file}]({ref_file}) — {label}\n")
    f.write("\n## Individual Files (per-module, per-page)\n\n")
    for subdir, label, _, source_url, _ in DATASETS:
        sub_llms = os.path.join(OUTDIR, subdir, "llms.txt")
        if os.path.isfile(sub_llms):
            f.write(f"- [{subdir}/]({subdir}/llms.txt) — {label}\n")
    f.write(f"\n## Changes\n\n- [CHANGES.md](CHANGES.md)\n")
    f.write(f"\n---\n\n*Generated by [openwrt-docs4ai]"
            f"(https://github.com/LuminairPrime/openwrt-docs4ai-v8) pipeline.*\n")

print(f"[06] OK: index.md")

# ============================================================
# 4. index.html — GitHub Pages HTML Landing
# ============================================================

html_path = os.path.join(OUTDIR, "index.html")
with open(html_path, "w", encoding="utf-8", newline="\n") as f:
    f.write('<!DOCTYPE html>\n<html lang="en"><head>\n')
    f.write('<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
    f.write(f'<title>openwrt-docs4ai</title>\n')
    f.write('<style>body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; padding: 2rem; max-width: 800px; margin: 0 auto; color: #24292e; background-color: #f6f8fa; } .container { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); } a { color: #0366d6; text-decoration: none; font-weight: 500;} a:hover { text-decoration: underline; } code { background: #f0f0f0; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace; }</style>\n')
    f.write('</head><body>\n')
    f.write('<div class="container">\n')
    f.write('<h1>openwrt-docs4ai</h1>\n')
    f.write('<p>Condensed OpenWrt documentation, optimized for AI LLMs and developers.</p>\n')
    f.write(f'<p><em>Last updated: {TS}</em></p>\n')
    f.write('<h2>Quick Start</h2>\n')
    f.write('<p>Point your LLM at <a href="llms.txt">llms.txt</a> for the full index.</p>\n')
    
    f.write('<h2>Complete References (single-file, ready to feed to LLMs)</h2>\n<ul>\n')
    for subdir, label, ref_file, source_url, commit in DATASETS:
        ref_path = os.path.join(OUTDIR, ref_file)
        if os.path.isfile(ref_path):
            f.write(f'  <li><a href="{ref_file}">{ref_file}</a> — {label}</li>\n')
    f.write('</ul>\n')

    f.write('<h2>Individual Files (per-module, per-page)</h2>\n<ul>\n')
    for subdir, label, _, source_url, _ in DATASETS:
        sub_llms = os.path.join(OUTDIR, subdir, "llms.txt")
        if os.path.isfile(sub_llms):
            f.write(f'  <li><a href="{subdir}/llms.txt">{subdir}/</a> — {label}</li>\n')
    f.write('</ul>\n')

    f.write('<h2>Changes</h2>\n<ul>\n')
    f.write('  <li><a href="CHANGES.md">CHANGES.md</a></li>\n')
    f.write('</ul>\n')

    f.write('<hr><p><em>Generated by <a href="https://github.com/LuminairPrime/openwrt-docs4ai-v8">openwrt-docs4ai</a> pipeline.</em></p>\n')
    f.write('</div>\n')
    f.write('</body></html>\n')

print(f"[06] OK: index.html")
print("[06] Complete.")
