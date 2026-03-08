import os
import sys
import argparse
import tempfile
import subprocess
import shutil
import json

# Add project root to PYTHONPATH so we can run scripts from anywhere
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

def run_script(script_path, env, log_file):
    print(f"Running {script_path}...", flush=True)
    with open(log_file, 'a') as f:
        f.write(f"\n--- Running {script_path} ---\n")
        
    # Execute the python script
    cmd = [sys.executable, script_path]
    
    # We use subprocess.Popen to stream output to both console and file
    process = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=project_root)
    
    with open(log_file, 'a') as f:
        for line in process.stdout:
            sys.stdout.write(line)
            f.write(line)
            
    process.wait()
    if process.returncode != 0:
        print(f"Error: {script_path} failed with exit code {process.returncode}")
        sys.exit(process.returncode)

def main():
    parser = argparse.ArgumentParser(description="v12 End-to-End Smoke Test")
    parser.add_argument("--keep-temp", action="store_true", help="Keep the temporary directory after completion")
    parser.add_argument("--skip-wiki", action="store_true", help="Skip the wiki scraper script")
    parser.add_argument("--only", type=str, help="Only run a specific script (e.g., '02b')", default=None)
    args = parser.parse_args()

    log_file = os.path.join(project_root, "tests", "smoke-test-log.txt")
    
    # Clear old log
    if os.path.exists(log_file):
        os.remove(log_file)
        
    print(f"Starting v12 Smoke Test. Logging to {log_file}")

    temp_dir_obj = tempfile.TemporaryDirectory()
    temp_dir = temp_dir_obj.name
    
    try:
        # Define Environment Variables for the test
        env = os.environ.copy()
        env["WORKDIR"] = temp_dir
        env["OUTDIR"] = os.path.join(temp_dir, "out")
        
        if args.skip_wiki:
            env["SKIP_WIKI"] = "true"
            
        # Copy fixtures into expected L0 structure
        repos = ["repo-wiki", "repo-ucode", "repo-luci", "repo-openwrt"]
        for r in repos:
            os.makedirs(os.path.join(temp_dir, r), exist_ok=True)
            
        os.makedirs(os.path.join(temp_dir, "repo-ucode", "lib"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "repo-ucode", "jsdoc", "c-transpiler"), exist_ok=True)
        
        with open(os.path.join(temp_dir, "repo-ucode", "jsdoc", "c-transpiler", "index.js"), "w") as f:
            f.write("module.exports = function() {};")
            
        shutil.copy(
            os.path.join(project_root, "tests", "fixtures", "wiki-page.html"), 
            os.path.join(temp_dir, "repo-wiki", "wiki-page.html")
        )
        shutil.copy(
            os.path.join(project_root, "tests", "fixtures", "source.c"),
            os.path.join(temp_dir, "repo-ucode", "lib", "source.c")
        )

        scripts_dir = os.path.join(project_root, ".github", "scripts")
        
        if args.only:
            # Find the specific script
            for script in os.listdir(scripts_dir):
                if args.only in script and script.endswith(".py"):
                    scripts_to_run.append(script)
        else:
            # v12 Default Sequence
            scripts_to_run = [
                "openwrt-docs4ai-02a-scrape-wiki.py",
                "openwrt-docs4ai-02b-scrape-ucode.py",
                "openwrt-docs4ai-02c-scrape-jsdoc.py",
                "openwrt-docs4ai-02d-scrape-core-packages.py",
                "openwrt-docs4ai-02e-scrape-example-packages.py",
                "openwrt-docs4ai-02f-scrape-procd-api.py",
                "openwrt-docs4ai-02g-scrape-uci-schemas.py",
                "openwrt-docs4ai-02h-scrape-hotplug-events.py",
                "openwrt-docs4ai-03-normalize-L2.py",
                "openwrt-docs4ai-03b-promote-intermediates.py",
                "openwrt-docs4ai-04-generate-summaries.py",
                "openwrt-docs4ai-05-assemble-references.py",
                "openwrt-docs4ai-06a-generate-llms-txt.py",
                "openwrt-docs4ai-06b-generate-agents-md.py",
                "openwrt-docs4ai-06c-generate-ide-schemas.py",
                "openwrt-docs4ai-06d-generate-changelog.py",
                "openwrt-docs4ai-07-generate-index-html.py",
                "openwrt-docs4ai-08-validate.py"
            ]
                
        # Seed L1 mocks manually for stable logic testing
        l1_dir = os.path.join(temp_dir, ".L1-raw")
        os.makedirs(os.path.join(l1_dir, "uci"), exist_ok=True)
        os.makedirs(os.path.join(l1_dir, "procd"), exist_ok=True)
        
        with open(os.path.join(l1_dir, "uci", "api.md"), "w", encoding="utf-8") as f:
            f.write("# UCI API\n\n## uci.get()\nReturns a config value.\n\n## uci.set()\nSets a value.")
        with open(os.path.join(l1_dir, "uci", "api.meta.json"), "w", encoding="utf-8") as f:
            json.dump({"module": "uci", "origin_type": "c_source", "language": "c", "slug": "api"}, f)
            
        with open(os.path.join(l1_dir, "procd", "init.md"), "w", encoding="utf-8") as f:
            f.write("# Procd Init\n\n## procd.add_service()\nAdds a service. Also uses uci.get().")
        with open(os.path.join(l1_dir, "procd", "init.meta.json"), "w", encoding="utf-8") as f:
            json.dump({"module": "procd", "origin_type": "c_source", "language": "c", "slug": "init"}, f)

        os.makedirs(os.path.join(l1_dir, "ucode"), exist_ok=True)
        with open(os.path.join(l1_dir, "ucode", "api-fs.md"), "w", encoding="utf-8") as f:
            f.write("# ucode fs module\n\n## fs.open(path, mode = 'r')\nOpens a file.")
        with open(os.path.join(l1_dir, "ucode", "api-fs.meta.json"), "w", encoding="utf-8") as f:
            json.dump({"module": "ucode", "origin_type": "c_source", "language": "c", "slug": "api-fs"}, f)

        with open(os.path.join(l1_dir, "ucode", "complex.md"), "w", encoding="utf-8") as f:
            f.write("# Complex ucode module\n\n## complex.foo(a = [1, 2], b = {x: 1})\nComplex function.\n\nSee [api-fs](api-fs.md) for more.")
        with open(os.path.join(l1_dir, "ucode", "complex.meta.json"), "w", encoding="utf-8") as f:
            json.dump({"module": "ucode", "origin_type": "c_source", "language": "c", "slug": "complex"}, f)

        for script in scripts_to_run:
            # Skip all extractors (02a-02h)
            if any(x in script for x in ["02a", "02b", "02c", "02d", "02e", "02f", "02g", "02h"]):
                continue
            script_full_path = os.path.join(scripts_dir, script)
            if os.path.isfile(script_full_path):
                run_script(script_full_path, env, log_file)
            else:
                print(f"Skipping missing script: {script}")

        print("\nSmoke test completed successfully!")
        
    finally:
        if args.keep_temp:
            print(f"\nSkipping cleanup. Temporary files preserved at: {temp_dir}")
            # we must explicitly prevent the context manager from deleting it by not closing the temp_dir_obj 
            # or by disabling its cleanup. For TemporaryDirectory in python slightly tricky, 
            # best way is to set _finalizer to None
            if hasattr(temp_dir_obj, "_finalizer") and temp_dir_obj._finalizer:
                temp_dir_obj._finalizer.detach()
        else:
            print("\nCleaning up temporary files...")
            temp_dir_obj.cleanup()

if __name__ == "__main__":
    main()
