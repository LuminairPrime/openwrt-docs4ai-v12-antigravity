"""
openwrt-docs4ai-00-alpha-smoke-test.py

Purpose  : Run the 4 brand new v10 alpha scrapers in an isolated environment.
Outputs  : tmp/alpha-test/openwrt-condensed-docs/
"""

import os
import subprocess
import shutil

print("==================================================")
print("  OpenWrt Docs4AI — Alpha Scraper Smoke Test")
print("==================================================")

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(repo_root)

WORKDIR = os.path.abspath("tmp")
OUTDIR = os.path.abspath(os.path.join("tmp", "alpha-test", "openwrt-condensed-docs"))

# Clean previous run
if os.path.isdir(OUTDIR):
    shutil.rmtree(OUTDIR)
os.makedirs(OUTDIR, exist_ok=True)

sub_env = os.environ.copy()
sub_env["WORKDIR"] = WORKDIR
sub_env["OUTDIR"] = OUTDIR

SCRIPTS = [
    ".github/scripts/openwrt-docs4ai-02f-scrape-procd-api.py",
    ".github/scripts/openwrt-docs4ai-02g-scrape-uci-schemas.py",
    ".github/scripts/openwrt-docs4ai-02h-scrape-hotplug-events.py",
    ".github/scripts/openwrt-docs4ai-02a-scrape-wiki-alpha.py"
]

for script in SCRIPTS:
    print(f"\n---> Executing: {script}")
    result = subprocess.run(["python", script], env=sub_env, check=False, text=True, capture_output=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"!!! FAIL: Script exited with {result.returncode}")

print("\n==================================================")
print(f"  Smoke test complete.")
print(f"  Inspect output artifacts at: {OUTDIR}")
print("==================================================")
