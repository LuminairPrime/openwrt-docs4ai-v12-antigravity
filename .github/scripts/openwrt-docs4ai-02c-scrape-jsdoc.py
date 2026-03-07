"""
openwrt-docs4ai-02c-scrape-jsdoc.py

Purpose  : Generate LuCI JavaScript API documentation using jsdoc2md.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs) — generated output destination
           WORKDIR (default: ./tmp) — where to find cloned source repos
Outputs  : $OUTDIR/luci-docs/luci-api-*.md
           $OUTDIR/luci-docs/llms.txt
Deps     : jsdoc2md (npm global install), Node.js
Notes    : Processes all .js files under luci-base/htdocs/luci-static/resources/.
           Modules with fewer than 15 words of jsdoc output are skipped.
           Falls back to whole-directory mode if no individual files produce output.
"""

import os
import subprocess
import glob
import datetime
import sys
import re
import shutil
import html

sys.stdout.reconfigure(line_buffering=True)

OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
WORKDIR = os.environ.get("WORKDIR", os.path.join(os.getcwd(), "tmp"))
TS = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")

print("[02c] Generate LuCI JS API documentation (JSDoc)")

repo_luci = os.path.join(WORKDIR, "repo-luci")
if not os.path.exists(repo_luci):
    print(f"[02c] SKIP: {repo_luci} not found")
    sys.exit(0)

# Find jsdoc2md binary explicitly
jsdoc2md = shutil.which("jsdoc2md") or shutil.which("jsdoc2md.cmd")
if not jsdoc2md:
    print("[02c] WARN: jsdoc2md not found in PATH — skipping LuCI JSDoc steps")
    sys.exit(0)

luci_commit = os.environ.get("LUCI_COMMIT", "unknown")
out_dir = os.path.join(OUTDIR, "luci-docs")
os.makedirs(out_dir, exist_ok=True)
repo_url = "https://github.com/openwrt/luci"
live_base = "https://openwrt.github.io/luci/jsapi"

# Write index header
with open(os.path.join(out_dir, "llms.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"# LuCI JS API Documentation Index\n# Source: {repo_url} (commit: {luci_commit})\n")
    f.write(f"# Live docs: {live_base}/\n# Generated: {TS}\n#\n")
    f.write("# LuCI is the OpenWrt web configuration interface.\n")
    f.write("# This index covers its complete client-side JavaScript API.\n#\n")
    f.write("# Standalone use: each .md file in this folder is self-contained with full\n")
    f.write("# metadata headers. This llms.txt provides the navigational index.\n#\n## Files in this directory\n\n")

# --- Process LuCI JS source files ---
print("[02c] Processing LuCI JS API source files...")
target_dir = os.path.join(repo_luci, "modules", "luci-base", "htdocs", "luci-static", "resources")

file_count = 0
skip_count = 0

luci_srcs = []
for root, _, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".js"):
            luci_srcs.append(os.path.join(root, file))
luci_srcs.sort()

for src in luci_srcs:
    filename = os.path.basename(src)
    mod = os.path.splitext(filename)[0]
    relpath = os.path.relpath(src, repo_luci).replace("\\", "/")

    cmd = [jsdoc2md, "--heading-depth", "2", "--global-index-format", "none", "--files", relpath]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_luci, encoding="utf-8")
    stdout = res.stdout or ""
    stderr = res.stderr or ""

    if stderr:
        with open("jsdoc-luci.err", "a", encoding="utf-8") as err_f:
            err_f.write(f"Stderr for {mod}:\n{stderr}\n")

    output = stdout.strip()
    word_count = len(output.split())

    if not output or word_count < 15:
        print(f"[02c] SKIP: {mod} (too short, {word_count} words)")
        skip_count += 1
        continue

    # Post-process: convert common HTML tags to markdown for LLM readability
    output = re.sub(r'<pre class="prettyprint[^"]*"><code>', '```\n', output)
    output = output.replace('</code></pre>', '\n```')
    output = re.sub(r'</?code>', '`', output)
    output = re.sub(r'</?p>', '', output)
    output = re.sub(r'</?(?:dl|dt|dd|ul|li|table|thead|tbody|tr|th|td|h[1-6]|a(?:\s+[^>]*)?|/a)[^>]*>', '', output)
    output = html.unescape(output)
    # Clean up excessive blank lines from tag removal
    output = re.sub(r'\n{3,}', '\n\n', output)

    live_url = f"{live_base}/LuCI.html" if mod == "luci" else f"{live_base}/LuCI.{mod}.html"
    outfile = os.path.join(out_dir, f"luci-api-{mod}.md")
    member_count = output.count("##")

    with open(outfile, "w", encoding="utf-8", newline="\n") as fw:
        fw.write("---\n")
        fw.write(f"module: {mod}\n")
        fw.write(f"title: LuCI API - {mod}\n")
        fw.write(f"source: {repo_url}/blob/master/{relpath}\n")
        fw.write(f"generated: {TS} from commit {luci_commit}\n")
        fw.write("---\n\n")
        fw.write(f"# LuCI API: `{mod}`\n\n")
        fw.write(f"> **Live docs:** {live_url}\n\n---\n\n")
        fw.write(output)

    member_word = "member" if member_count == 1 else "members"
    with open(os.path.join(out_dir, "llms.txt"), "a", encoding="utf-8", newline="\n") as f:
        f.write(f"- [luci-api-{mod}.md](/luci-docs/luci-api-{mod}.md): LuCI `{mod}` JS API — {member_count} documented {member_word}\n")

    file_count += 1
    print(f"[02c] OK: luci-api-{mod}.md ({member_count} members)")

# Fallback: if no individual files produced output, try whole-directory mode
if file_count == 0 and len(luci_srcs) > 0:
    print("[02c] WARN: 0 files generated individually. Running whole-directory fallback.")
    target_rel = os.path.relpath(target_dir, repo_luci).replace("\\", "/")
    cmd = [jsdoc2md, "--heading-depth", "2", "--global-index-format", "none",
           "--files", f"{target_rel}/**/*.js"]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_luci, encoding="utf-8")
    output = res.stdout.strip()
    if output:
        with open(os.path.join(out_dir, "luci-api-all.md"), "w", encoding="utf-8", newline="\n") as fw:
            fw.write(f"# LuCI API: All\n\n{output}")
        with open(os.path.join(out_dir, "llms.txt"), "a", encoding="utf-8", newline="\n") as f:
            f.write(f"- [luci-api-all.md](/luci-docs/luci-api-all.md): LuCI complete API\n")

# Print any jsdoc warnings
if os.path.exists("jsdoc-luci.err"):
    print("\n=== jsdoc warnings/errors (LuCI) ===")
    with open("jsdoc-luci.err", "r", encoding="utf-8") as err_f:
        print(err_f.read())
    print("=== end jsdoc warnings ===")
    os.remove("jsdoc-luci.err")

print(f"[02c] Complete: {file_count} files generated, {skip_count} skipped.")
