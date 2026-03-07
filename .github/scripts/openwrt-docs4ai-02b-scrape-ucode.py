"""
openwrt-docs4ai-02b-scrape-ucode.py

Purpose  : Generate ucode language and module API documentation using jsdoc2md.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs) — generated output destination
           WORKDIR (default: ./tmp) — where to find cloned source repos
Outputs  : $OUTDIR/ucode-docs/ucode-tutorial-*.md
           $OUTDIR/ucode-docs/ucode-module-*.md
           $OUTDIR/ucode-docs/llms.txt
Deps     : jsdoc2md (npm global install), Node.js
Notes    : Processes tutorials from docs/ and modules from lib/ in the ucode repo.
           Modules with fewer than 15 words of jsdoc output are skipped.
"""

import os
import subprocess
import glob
import datetime
import sys
import re
import shutil
import tempfile
import html

sys.stdout.reconfigure(line_buffering=True)

OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
WORKDIR = os.environ.get("WORKDIR", os.path.join(os.getcwd(), "tmp"))
TS = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")

print("[02b] Generate ucode documentation (JSDoc)")

repo_ucode = os.path.join(WORKDIR, "repo-ucode")
if not os.path.exists(repo_ucode):
    print(f"[02b] SKIP: {repo_ucode} not found")
    sys.exit(0)

# Find jsdoc2md binary explicitly (avoids shell=True fragility)
jsdoc2md = shutil.which("jsdoc2md") or shutil.which("jsdoc2md.cmd")
if not jsdoc2md:
    print("[02b] WARN: jsdoc2md not found in PATH — skipping ucode JSDoc steps")
    sys.exit(0)

ucode_commit = os.environ.get("UCODE_COMMIT", "unknown")

# Check for package.json before running npm install
if os.path.isfile(os.path.join(repo_ucode, "package.json")):
    subprocess.run(["npm", "install", "--silent"], cwd=repo_ucode,
                   shell=(os.name == "nt"), capture_output=True)
else:
    print("[02b] No package.json in repo-ucode — using global jsdoc2md")

# Look for jsdoc config
ucode_conf = None
for conf in ["jsdoc/conf.json", "jsdoc.conf.json", ".jsdoc.json", ".jsdoc.conf.json"]:
    if os.path.isfile(os.path.join(repo_ucode, conf)):
        ucode_conf = os.path.join(repo_ucode, conf)
        print(f"[02b] Found jsdoc config: {ucode_conf}")
        break

out_dir = os.path.join(OUTDIR, "ucode-docs")
os.makedirs(out_dir, exist_ok=True)
repo_url = "https://github.com/jow-/ucode"

# Write index header
with open(os.path.join(out_dir, "llms.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"# ucode Documentation Index\n# Source: {repo_url} (commit: {ucode_commit})\n")
    f.write(f"# Live docs: https://ucode.mein.io/\n# Generated: {TS}\n#\n")
    f.write("# ucode is a tiny ECMAScript-like scripting language for OpenWrt.\n")
    f.write("# Provides bindings for ubus, uci, uloop, netlink, and other OpenWrt APIs.\n")
    f.write("# Syntax closely resembles ECMAScript; synchronous; no OOP standard library.\n#\n")
    f.write("# Standalone use: each .md file in this folder is self-contained with full\n")
    f.write("# metadata headers. This llms.txt provides the navigational index.\n#\n## Files in this directory\n\n")

# --- Process tutorials ---
print("[02b] Processing tutorials...")
for src in sorted(glob.glob(os.path.join(repo_ucode, "docs", "tutorial-*.md"))):
    base = os.path.basename(src)
    dest = re.sub(r'tutorial-[0-9]*-', 'ucode-tutorial-', base)

    with open(src, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    title = "Tutorial"
    for line in lines:
        if line.startswith("#"):
            title = line.strip("# \n")
            break

    with open(os.path.join(out_dir, dest), "w", encoding="utf-8", newline="\n") as fw:
        rel_src = src.replace(repo_ucode + os.sep, "").replace("\\", "/")
        fw.write("---\n")
        fw.write(f"module: {title}\n")
        fw.write(f"title: ucode Tutorial - {title}\n")
        fw.write(f"source: {repo_url}/blob/master/{rel_src}\n")
        fw.write(f"generated: {TS} from commit {ucode_commit}\n")
        fw.write("---\n\n")
        fw.write(f"# {title}\n\n")
        fw.write(f"> **Live docs:** https://ucode.mein.io/{os.path.basename(src).replace('.md', '')}.html\n\n---\n\n")
        fw.writelines(lines[1:] if lines and lines[0].startswith("#") else lines)

    with open(os.path.join(out_dir, "llms.txt"), "a", encoding="utf-8", newline="\n") as f:
        f.write(f"- [{dest}](/ucode-docs/{dest}): ucode tutorial — {title}\n")

    print(f"[02b] OK: {dest}")

# --- Process modules ---
print("[02b] Processing modules...")
srcs = sorted(glob.glob(os.path.join(repo_ucode, "lib", "*.js")) +
              glob.glob(os.path.join(repo_ucode, "lib", "*.c")))

for src in srcs:
    mod = os.path.splitext(os.path.basename(src))[0]

    plugin_path = os.path.abspath(os.path.join(repo_ucode, "jsdoc", "c-transpiler")).replace('\\', '/')

    # WORKAROUND: jsdoc2md has a bug where parsing `.c` files via `includePattern` triggers
    # recursive directory scanning, totally ignoring explicit CLI `--files` arguments. This
    # results in every module containing the docs for every other module.
    # We bypass this by executing jsdoc2md inside an isolated temporary directory containing
    # ONLY the target C file, forcing it to scan emptiness.
    # NOTE: While this hack is unusual, it guarantees the dense, token-efficient output we
    # need for LLMs. If this ever breaks, DO NOT try to fix jsdoc. Instead, look at
    # `docs/plans/v10-c-to-md-proposals.md` and upgrade to a native C tool like Doxide.
    with tempfile.TemporaryDirectory() as tempd:
        temp_c = os.path.join(tempd, os.path.basename(src))
        shutil.copy2(src, temp_c)
        
        ephemeral_conf = os.path.join(tempd, "jsdoc-ephemeral.json")
        with open(ephemeral_conf, "w", encoding="utf-8") as cw:
            cw.write('{"source": {"includePattern": ".+\\\\.c(pp)?$"}, "plugins": ["' + plugin_path + '"]}')

        cmd = [jsdoc2md, "--heading-depth", "2", "--global-index-format", "none",
               "--configure", "jsdoc-ephemeral.json", "--files", os.path.basename(temp_c)]

        res = subprocess.run(cmd, capture_output=True, text=True, cwd=tempd, encoding="utf-8")
    stdout = res.stdout or ""
    stderr = res.stderr or ""

    if stderr:
        with open("jsdoc-ucode.err", "a", encoding="utf-8") as err_f:
            err_f.write(f"Stderr for {mod}:\n{stderr}\n")

    output = stdout.strip()
    word_count = len(output.split())
    if not output or word_count < 15:
        print(f"[02b] SKIP: {mod} (too short, {word_count} words)")
        continue

    # Post-process: convert common HTML tags to markdown for LLM readability
    output = re.sub(r'<pre class="prettyprint[^"]*"><code>', '```\n', output)
    output = output.replace('</code></pre>', '\n```')
    output = re.sub(r'</?code>', '`', output)
    output = re.sub(r'</?p>', '', output)
    output = re.sub(r'</?(?:dl|dt|dd|ul|li|table|thead|tbody|tr|th|td|h[1-6])[^>]*>', '', output)
    output = html.unescape(output)
    # Clean up excessive blank lines from tag removal
    output = re.sub(r'\n{3,}', '\n\n', output)

    outfile = os.path.join(out_dir, f"ucode-module-{mod}.md")
    member_count = output.count("##")

    rel_src_fwd = src.replace(repo_ucode + os.sep, "").replace("\\", "/")
    with open(outfile, "w", encoding="utf-8", newline="\n") as fw:
        fw.write("---\n")
        fw.write(f"module: {mod}\n")
        fw.write(f"title: ucode module - {mod}\n")
        fw.write(f"source: {repo_url}/blob/master/{rel_src_fwd}\n")
        fw.write(f"generated: {TS} from commit {ucode_commit}\n")
        fw.write("---\n\n")
        fw.write(f"# ucode module: `{mod}`\n\n")
        fw.write(f"> **Live docs:** https://ucode.mein.io/module-{mod}.html\n\n---\n\n")
        fw.write(output)

    member_word = "member" if member_count == 1 else "members"
    with open(os.path.join(out_dir, "llms.txt"), "a", encoding="utf-8", newline="\n") as f:
        f.write(f"- [ucode-module-{mod}.md](/ucode-docs/ucode-module-{mod}.md): ucode `{mod}` module — {member_count} documented {member_word}\n")

    print(f"[02b] OK: ucode-module-{mod}.md ({member_count} members)")

# Print any jsdoc warnings
if os.path.exists("jsdoc-ucode.err"):
    print("\n=== jsdoc warnings/errors (ucode) ===")
    with open("jsdoc-ucode.err", "r", encoding="utf-8") as err_f:
        print(err_f.read())
    print("=== end jsdoc warnings ===")
    os.remove("jsdoc-ucode.err")

print("[02b] Complete.")
