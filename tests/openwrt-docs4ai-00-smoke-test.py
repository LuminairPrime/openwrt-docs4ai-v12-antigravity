"""
openwrt-docs4ai-00-smoke-test.py

Purpose  : Local smoke test runner -- executes the full pipeline in a temp directory.
Env Vars : None required (creates its own temp environment)
Flags    : --keep-temp   -- don't delete the temp dir after run (for inspection)
           --run-ai      -- include AI summarization step (off by default)
Outputs  : Test log appended to tests/openwrt-docs4ai-00-smoke-test-log.txt
Deps     : All pipeline dependencies (Python, Node.js, pandoc, git, jsdoc2md)
Notes    : Runs each script sequentially, reports PASS/FAIL per step.
           Sets OUTDIR and WORKDIR to temp subdirectories so the repo is untouched.
           The validate script (07) acts as the real pass/fail gate.
"""

import os
import sys
import subprocess
import tempfile
import shutil
import datetime
import time

# --- Configuration ---
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", ".github", "scripts")
SCRIPT_DIR = os.path.normpath(SCRIPT_DIR)
TEST_DIR   = os.path.dirname(os.path.abspath(__file__))
LOG_FILE   = os.path.join(TEST_DIR, "openwrt-docs4ai-00-smoke-test-log.txt")

KEEP_TEMP = "--keep-temp" in sys.argv
RUN_AI    = "--run-ai" in sys.argv

# Steps to run in order. Format: (label, script_basename, can_skip)
STEPS = [
    ("Clone repos",         "openwrt-docs4ai-01-clone-repos.py",             False),
    ("Scrape wiki",         "openwrt-docs4ai-02a-scrape-wiki.py",            False),
    ("Scrape ucode",        "openwrt-docs4ai-02b-scrape-ucode.py",           False),
    ("Scrape LuCI JSDoc",   "openwrt-docs4ai-02c-scrape-jsdoc.py",           False),
    ("Scrape packages",     "openwrt-docs4ai-02d-scrape-core-packages.py",   False),
    ("Scrape examples",     "openwrt-docs4ai-02e-scrape-example-packages.py", False),
    ("Cross-references",    "openwrt-docs4ai-03-add-links.py",               False),
    ("AI summaries",        "openwrt-docs4ai-04-generate-summaries.py",      True),
    ("Assemble references", "openwrt-docs4ai-05-assemble-references.py",    False),
    ("Generate indexes",    "openwrt-docs4ai-06-generate-index.py",         False),
    ("Validate",            "openwrt-docs4ai-07-validate.py",               False),
]


def run_step(label, script, env, temp_dir):
    """Run a single step. Returns (status, duration_seconds)."""
    script_path = os.path.join(SCRIPT_DIR, script)
    if not os.path.isfile(script_path):
        return "MISSING", 0

    start = time.time()

    # Add --warn-only for validate in smoke test mode
    cmd = [sys.executable, script_path]
    if "07-validate" in script:
        cmd.append("--warn-only")

    try:
        result = subprocess.run(
            cmd,
            env=env,
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per step
        )
        duration = time.time() - start

        # Print stdout for visibility
        if result.stdout.strip():
            for line in result.stdout.strip().split("\n"):
                print(f"  {line}")

        if result.returncode != 0:
            if result.stderr.strip():
                print(f"  STDERR: {result.stderr.strip()[:500]}")
            return "FAIL", duration

        return "PASS", duration

    except subprocess.TimeoutExpired:
        duration = time.time() - start
        return "TIMEOUT", duration
    except Exception as e:
        duration = time.time() - start
        print(f"  ERROR: {e}")
        return "ERROR", duration


def main():
    print("=" * 60)
    print("openwrt-docs4ai Smoke Test")
    print("=" * 60)

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Time: {ts}")
    print(f"Keep temp: {KEEP_TEMP}")
    print(f"Run AI: {RUN_AI}")
    print()

    # Create temp directory inside the project's tmp/ folder
    project_root = os.path.dirname(TEST_DIR)
    base_tmp = os.path.join(project_root, "tmp")
    os.makedirs(base_tmp, exist_ok=True)
    
    # Use mkdtemp but forced into our local tmp directory
    temp_dir = tempfile.mkdtemp(prefix="smoke-test-", dir=base_tmp)
    
    out_dir  = os.path.join(temp_dir, "openwrt-condensed-docs")
    work_dir = os.path.join(temp_dir, "work")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(work_dir, exist_ok=True)
    print(f"Temp dir: {temp_dir}")
    print(f"OUTDIR:   {out_dir}")
    print(f"WORKDIR:  {work_dir}")
    print()

    # Build environment for subprocesses
    env = os.environ.copy()
    env["OUTDIR"]  = out_dir
    env["WORKDIR"] = work_dir
    env["SKIP_AI"] = "true"  # Default: skip AI

    if RUN_AI:
        env["SKIP_AI"] = "false"
        if not (env.get("GITHUB_TOKEN") or env.get("LOCAL_DEV_TOKEN")):
            print("WARNING: --run-ai specified but no API token set.")
            print("  Set GITHUB_TOKEN or LOCAL_DEV_TOKEN to enable AI summaries.")

    # Run steps
    results = []
    total_start = time.time()

    for label, script, can_skip in STEPS:
        if can_skip and not RUN_AI and "04-generate" in script:
            print(f"[{len(results)+1:2d}/{len(STEPS)}] {label:25s} ... SKIPPED (use --run-ai)")
            results.append((label, "SKIPPED", 0))
            continue

        print(f"[{len(results)+1:2d}/{len(STEPS)}] {label:25s} ... ", end="", flush=True)
        status, duration = run_step(label, script, env, temp_dir)
        print(f"{status} ({duration:.1f}s)")
        results.append((label, status, duration))

        if status in ("FAIL", "ERROR", "TIMEOUT", "MISSING"):
            print(f"\n  *** Step failed: {label} ***")
            # Continue running remaining steps for diagnostic purposes

    total_time = time.time() - total_start
    print()
    print("=" * 60)
    print("Results:")
    print("-" * 60)

    pass_count = 0
    fail_count = 0
    skip_count = 0

    for label, status, duration in results:
        icon = {"PASS": "+", "FAIL": "X", "SKIPPED": "--",
                "TIMEOUT": "T", "ERROR": "!", "MISSING": "?"}
        print(f"  {icon.get(status, '?')} {label:25s} {status:8s} ({duration:.1f}s)")
        if status == "PASS":
            pass_count += 1
        elif status == "SKIPPED":
            skip_count += 1
        else:
            fail_count += 1

    print("-" * 60)
    overall = "PASS" if fail_count == 0 else "FAIL"
    print(f"  Overall: {overall} ({pass_count} pass, {fail_count} fail, "
          f"{skip_count} skip) in {total_time:.1f}s")
    print("=" * 60)

    # Log results
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{ts} | {overall} | "
                f"{pass_count}P/{fail_count}F/{skip_count}S | "
                f"{total_time:.0f}s")
        if fail_count > 0:
            failed = [r[0] for r in results if r[1] not in ("PASS", "SKIPPED")]
            f.write(f" | FAILED: {', '.join(failed)}")
        f.write("\n")

    # Cleanup
    if KEEP_TEMP:
        print(f"\nTemp directory preserved: {temp_dir}")
        print(f"  Output: {out_dir}")
    else:
        print(f"\nCleaning up temp directory...")
        shutil.rmtree(temp_dir, ignore_errors=True)

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
