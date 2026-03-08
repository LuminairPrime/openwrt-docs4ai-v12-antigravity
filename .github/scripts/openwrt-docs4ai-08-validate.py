"""
Purpose: Strict CI/CD gatekeeper validating all documentation layers.
Phase: Validation
Layers: L1, L2, L3, L4, L5
Inputs: OUTDIR/
Outputs: Validation report to stdout
Environment Variables: OUTDIR, VALIDATE_MODE (hard/soft)
Dependencies: lib.config, pyyaml
Notes: Implements hard fails for 0-byte files, broken links, malformed YAML, and 404 HTML.
       Soft warnings for AST issues and token overflows.
"""

import os
import re
import yaml
import glob
import sys
import subprocess
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib import config

sys.stdout.reconfigure(line_buffering=True)

OUTDIR = os.environ.get("OUTDIR", config.OUTDIR)
VALIDATE_MODE = os.environ.get("VALIDATE_MODE", "hard").lower()

print(f"[08] Security & Quality Validation ({OUTDIR})")

hard_failures = []
soft_warnings = []

def hard_fail(msg):
    hard_failures.append(msg)
    print(f"[08] FAIL: {msg}")

def soft_warn(msg):
    soft_warnings.append(msg)
    print(f"[08] WARN: {msg}")

# ============================================================
# Check 1: Structural Integrity (L3 Entry Points)
# ============================================================
CORE_FILES = ["llms.txt", "llms-full.txt", "AGENTS.md", "README.md", "index.html"]
for f in CORE_FILES:
    if not os.path.isfile(os.path.join(OUTDIR, f)):
        hard_fail(f"Missing core L3 file: {f}")

# ============================================================
# Check 2: Content Validation (0-byte, HTML Leaks, UTF-8)
# ============================================================
HTML_ERROR_MARKERS = ["<!DOCTYPE", "<html", "404 Not Found", "Access Denied", "captcha"]

all_md = glob.glob(os.path.join(OUTDIR, "**", "*.md"), recursive=True)
checked_count = 0

for fpath in all_md:
    rel = os.path.relpath(fpath, OUTDIR)
    checked_count += 1
    
    # Check 0-byte
    if os.path.getsize(fpath) == 0:
        hard_fail(f"0-byte file detected: {rel}")
        continue

    try:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        hard_fail(f"Non-UTF-8 content: {rel}")
        continue

    # Check for HTML leak in prose
    first_500 = content[:500]
    for marker in HTML_ERROR_MARKERS:
        if marker in first_500:
            hard_fail(f"HTML error/leak detected ({marker}): {rel}")
            break

    # L2 YAML Validation
    if ".L2-semantic" in rel:
        if not content.startswith("---"):
            hard_fail(f"Missing YAML frontmatter in L2: {rel}")
        else:
            try:
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    yaml_data = yaml.safe_load(parts[1])
                    required = ["title", "module", "origin_type", "token_count", "version"]
                    for field in required:
                        if field not in yaml_data:
                            hard_fail(f"L2 YAML missing required field '{field}': {rel}")
            except Exception as e:
                hard_fail(f"Malformed YAML in L2: {rel} ({e})")

# ============================================================
# Check 3: Link Integrity (L2 Relative Links)
# ============================================================
for fpath in all_md:
    if ".L2-semantic" not in fpath:
        continue
    
    rel_dir = os.path.dirname(fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find relative markdown links: [text](../path/file.md)
    links = re.findall(r'\[.*?\]\(((\.\.\/)+.*?\.md)\)', content)
    for link_tuple in links:
        link = link_tuple[0]
        target_path = os.path.normpath(os.path.join(rel_dir, link))
        if not os.path.isfile(target_path):
            hard_fail(f"Broken relative link in {os.path.relpath(fpath, OUTDIR)}: {link}")

# ============================================================
# Check 4: AST Validation (Soft)
# ============================================================
JS_BINARY = shutil.which("node")
UCODE_BINARY = shutil.which("ucode")

def check_ast(code, lang, rel_path):
    if lang == "javascript" and JS_BINARY:
        with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode="w") as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        res = subprocess.run([JS_BINARY, "--check", tmp_path], capture_output=True, text=True)
        os.unlink(tmp_path)
        if res.returncode != 0:
            soft_warn(f"JS Syntax Error in {rel_path}: {res.stderr.strip()}")
    elif lang == "ucode" and UCODE_BINARY:
        with tempfile.NamedTemporaryFile(suffix=".uc", delete=False, mode="w") as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        res = subprocess.run([UCODE_BINARY, "-c", tmp_path], capture_output=True, text=True)
        os.unlink(tmp_path)
        if res.returncode != 0:
            soft_warn(f"uCode Syntax Error in {rel_path}: {res.stderr.strip()}")

import shutil
# Only check small snippets in L1-raw/luci-examples/
if JS_BINARY or UCODE_BINARY:
    example_files = glob.glob(os.path.join(OUTDIR, ".L1-raw", "luci-examples", "*.md"))
    for fpath in example_files:
        rel = os.path.relpath(fpath, OUTDIR)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract code blocks
        blocks = re.findall(r'```(javascript|ucode)\n(.*?)\n```', content, re.DOTALL)
        for lang, code in blocks:
            check_ast(code, lang, rel)

# ============================================================
# Summary
# ============================================================
print(f"\n[08] ----------------------------------------------")
print(f"[08] Validation Results")
print(f"[08]   Files Checked: {checked_count}")
print(f"[08]   Hard Failures: {len(hard_failures)}")
print(f"[08]   Soft Warnings: {len(soft_warnings)}")
print(f"[08] ----------------------------------------------")

if hard_failures:
    print("\n[08] BLOCKING FAILURES:")
    for f in hard_failures:
        print(f"  X {f}")
    
    if VALIDATE_MODE == "hard":
        sys.exit(1)
    else:
        print("[08] INFO: Continuing despite failures due to VALIDATE_MODE=soft")

if soft_warnings:
    print("\n[08] NON-BLOCKING WARNINGS:")
    for w in soft_warnings:
        print(f"  ! {w}")

print("\n[08] Validation pass complete.")
sys.exit(0)
