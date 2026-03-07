"""
openwrt-docs4ai-07-validate.py

Purpose  : Validate generated documentation before promotion.
           This is the STAGING GATE -- exits non-zero on any hard failure.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs) -- directory to validate
Flags    : --warn-only  -- print issues but always exit 0 (for local dev)
           --out-dir X  -- override OUTDIR
Outputs  : Prints validation report to stdout
Deps     : None (pure Python)
Notes    : Two-tier validation:
           - Hard failures: missing required files, empty files, HTML error pages,
             binary/non-UTF-8 content. These block promotion.
           - Soft warnings: low file counts, small file sizes. These are logged but
             do not block promotion.
           Split from the original monolithic 05-finalize-publish.sh.
           Ideas from GPT-5.2 plan: HTML error detection, UTF-8 checks.
"""

import os
import glob
import sys

sys.stdout.reconfigure(line_buffering=True)

# --- Argument parsing ---
warn_only = "--warn-only" in sys.argv
out_dir_override = None
for i, arg in enumerate(sys.argv):
    if arg == "--out-dir" and i + 1 < len(sys.argv):
        out_dir_override = sys.argv[i + 1]

OUTDIR = out_dir_override or os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))

print(f"[07] Validate documentation ({OUTDIR})")
if warn_only:
    print("[07] Running in --warn-only mode (will not fail)")

hard_failures = []
soft_warnings = []


def hard_fail(msg):
    hard_failures.append(msg)
    print(f"[07] FAIL: {msg}")


def soft_warn(msg):
    soft_warnings.append(msg)
    print(f"[07] WARN: {msg}")


# ============================================================
# Check 1: Required files exist
# ============================================================

REQUIRED_FILES = [
    "llms.txt",
    "index.md",
    "CHANGES.md",
]

REQUIRED_REF_FILES = [
    "ucode-complete-reference.md",
    "luci-jsapi-complete-reference.md",
]

# These are only required if their scrapers weren't skipped
OPTIONAL_REF_FILES = [
    "openwrt-wiki-complete-reference.md",
    "openwrt-buildroot-complete-reference.md",
    "openwrt-examples-complete-reference.md",
]

REQUIRED_DIRS = [
    "ucode-docs",
    "luci-docs",
]

for f in REQUIRED_FILES:
    path = os.path.join(OUTDIR, f)
    if not os.path.isfile(path):
        hard_fail(f"Required file missing: {f}")

for f in REQUIRED_REF_FILES:
    path = os.path.join(OUTDIR, f)
    if not os.path.isfile(path):
        hard_fail(f"Required reference file missing: {f}")

for f in OPTIONAL_REF_FILES:
    path = os.path.join(OUTDIR, f)
    if not os.path.isfile(path):
        soft_warn(f"Optional reference file missing: {f}")

for d in REQUIRED_DIRS:
    path = os.path.join(OUTDIR, d)
    if not os.path.isdir(path):
        hard_fail(f"Required directory missing: {d}/")

# ============================================================
# Check 2: Per-folder llms.txt files exist
# ============================================================

REQUIRED_SUBDIRS = {"ucode-docs", "luci-docs"}
OPTIONAL_SUBDIRS = {"openwrt-wiki-docs", "openwrt-buildroot-docs", "openwrt-examples"}

for subdir in REQUIRED_SUBDIRS | OPTIONAL_SUBDIRS:
    llms_path = os.path.join(OUTDIR, subdir, "llms.txt")
    dir_path = os.path.join(OUTDIR, subdir)
    if os.path.isdir(dir_path):
        if not os.path.isfile(llms_path):
            if subdir in REQUIRED_SUBDIRS:
                hard_fail(f"Per-folder index missing: {subdir}/llms.txt")
            else:
                soft_warn(f"Per-folder index missing (optional): {subdir}/llms.txt")
    # If directory doesn't exist, skip (scraper may have been skipped)

# ============================================================
# Check 3: File content validation
# ============================================================

all_md = glob.glob(os.path.join(OUTDIR, "**", "*.md"), recursive=True)

# HTML error pages that accidentally got saved as .md
HTML_MARKERS = [
    "<!DOCTYPE",
    "<!doctype",
    "<html",
    "Access denied",
    "captcha",
    "404 Not Found",
    "<title>Error</title>",
]

empty_count = 0
html_error_count = 0
binary_count = 0
tiny_count = 0

MAX_FILE_SIZE_MB = 2.0
large_file_count = 0

for fpath in all_md:
    rel = os.path.relpath(fpath, OUTDIR)
    
    # Check for maximum file size ceiling
    size_mb = os.path.getsize(fpath) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        hard_fail(f"File {rel} exceeds maximum permissible size of {MAX_FILE_SIZE_MB}MB ({size_mb:.2f}MB).")
        large_file_count += 1
        continue

    # Check for binary/encoding issues
    try:
        content = open(fpath, encoding="utf-8").read()
    except UnicodeDecodeError:
        hard_fail(f"Non-UTF-8 content (binary?): {rel}")
        binary_count += 1
        continue

    # Check for empty/whitespace-only files
    if not content.strip():
        hard_fail(f"Empty file: {rel}")
        empty_count += 1
        continue

    # Check for HTML error pages
    first_500 = content[:500]
    for marker in HTML_MARKERS:
        if marker in first_500:
            hard_fail(f"HTML error page detected ({marker}): {rel}")
            html_error_count += 1
            break

    # Check for suspiciously small files (less than 3 lines)
    line_count = content.count("\n") + 1
    if line_count < 3:
        soft_warn(f"Very small file ({line_count} lines): {rel}")
        tiny_count += 1

# ============================================================
# Check 4: Minimum file counts per directory
# ============================================================

MIN_COUNTS = {
    "ucode-docs": 3,   # At minimum: a few tutorials or modules
    "luci-docs": 2,    # At minimum: a couple API modules
}

for subdir, min_count in MIN_COUNTS.items():
    dir_path = os.path.join(OUTDIR, subdir)
    if os.path.isdir(dir_path):
        md_count = len(glob.glob(os.path.join(dir_path, "*.md")))
        if md_count < min_count:
            soft_warn(f"{subdir}/ has only {md_count} .md files (expected >={min_count})")

# ============================================================
# Check 5: Reference file minimum sizes
# ============================================================

for ref_file in REQUIRED_REF_FILES + OPTIONAL_REF_FILES:
    ref_path = os.path.join(OUTDIR, ref_file)
    if os.path.isfile(ref_path):
        size_kb = os.path.getsize(ref_path) // 1024
        if size_kb < 1:
            soft_warn(f"Reference file very small ({size_kb} KB): {ref_file}")

# ============================================================
# Summary
# ============================================================

print()
print(f"[07] =============================================")
print(f"[07] Validation Summary")
print(f"[07]   Total .md files checked: {len(all_md)}")
print(f"[07]   Hard failures: {len(hard_failures)}")
print(f"[07]   Soft warnings: {len(soft_warnings)}")
print(f"[07] =============================================")

if hard_failures:
    print()
    print("[07] Hard failures (blocking):")
    for msg in hard_failures:
        print(f"[07]   X {msg}")

if soft_warnings:
    print()
    print("[07] Soft warnings (non-blocking):")
    for msg in soft_warnings:
        print(f"[07]   ! {msg}")

if hard_failures and not warn_only:
    print()
    print("[07] RESULT: FAIL -- hard failures detected, blocking promotion.")
    sys.exit(1)
elif hard_failures and warn_only:
    print()
    print("[07] RESULT: WARN-ONLY -- failures detected but --warn-only is set.")
    sys.exit(0)
else:
    print()
    print("[07] RESULT: PASS -- documentation is valid for promotion.")
    sys.exit(0)
