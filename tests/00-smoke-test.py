import os
import sys
import argparse
import tempfile
import subprocess
import shutil

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
        os.makedirs(os.path.join(temp_dir, "repo-wiki"), exist_ok=True)
        os.makedirs(os.path.join(temp_dir, "repo-ucode", "lib"), exist_ok=True)
        
        shutil.copy(
            os.path.join(project_root, "tests", "fixtures", "wiki-page.html"), 
            os.path.join(temp_dir, "repo-wiki", "wiki-page.html")
        )
        shutil.copy(
            os.path.join(project_root, "tests", "fixtures", "source.c"),
            os.path.join(temp_dir, "repo-ucode", "lib", "source.c")
        )

        scripts_dir = os.path.join(project_root, ".github", "scripts")
        scripts_to_run = []
        
        if args.only:
            # Find the specific script
            for script in os.listdir(scripts_dir):
                if args.only in script and script.endswith(".py"):
                    scripts_to_run.append(script)
        else:
            # Run all scripts that end with .py in order, but we only have dummy fixtures so we can only run specific ones
            # Actually for Checkpoint 0, we just need to verify the runner works
            # Since extractors aren't refactored yet, we can't run them all.
            # We will just log that the runner is ready.
            print("Smoke test runner initialized. No scripts executed because full pipeline is not yet v12 compliant.")
            with open(log_file, 'a') as f:
                f.write("Smoke test runner initialized successfully.\n")
                
        for script in sorted(scripts_to_run):
            if args.skip_wiki and "02a" in script:
                continue
            run_script(os.path.join(scripts_dir, script), env, log_file)

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
