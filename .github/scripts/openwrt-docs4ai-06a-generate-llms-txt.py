"""
Purpose: Generates the L3 navigational maps (llms.txt and llms-full.txt).
Phase: Aggregation / Indexing
Layers: L4 -> L3
Inputs: OUTDIR/ 
Outputs: OUTDIR/llms.txt, OUTDIR/llms-full.txt, OUTDIR/{module}/llms.txt
Environment Variables: OUTDIR, OPENWRT_COMMIT, LUCI_COMMIT, WORKDIR
Dependencies: pyyaml, lib.config
Notes: Creates both the hierarchical entry point and the flat global catalog.
"""

import os
import glob
import datetime
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib import config

sys.stdout.reconfigure(line_buffering=True)

try:
    import yaml
except ImportError:
    print("[06a] FAIL: 'pyyaml' package not installed")
    sys.exit(1)

OUTDIR = config.OUTDIR
L2_DIR = os.path.join(OUTDIR, ".L2-semantic")

if not os.path.isdir(L2_DIR):
    print(f"[06a] FAIL: L2 directory not found: {L2_DIR}")
    sys.exit(1)

# Grab version info
versions = [
    f"openwrt/openwrt@{os.environ.get('OPENWRT_COMMIT', 'unknown')}",
    f"openwrt/luci@{os.environ.get('LUCI_COMMIT', 'unknown')}"
]
version_str = ", ".join(versions)

# Global metrics
global_tokens = 0
global_files = []

# Module summaries for the root llms.txt
module_registry = {}

# Constants for categorized display in root index
CATEGORIES = {
    "Core Daemons": ["procd", "uci", "openwrt-hotplug"],
    "Scripting & Logic": ["ucode", "luci"],
    "Ecosystem": ["openwrt-core", "luci-examples"],
    "Manuals": ["wiki"]
}

print("[06a] Generating L3 Navigational Maps (llms.txt)")

for module in sorted(os.listdir(L2_DIR)):
    mod_dir = os.path.join(L2_DIR, module)
    if not os.path.isdir(mod_dir):
        continue

    mod_files = []
    mod_tokens = 0
    mod_desc = module

    for fpath in sorted(glob.glob(os.path.join(mod_dir, "*.md"))):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract YAML
            yaml_block = content.split("---")[1] if "---" in content else ""
            fm = yaml.safe_load(yaml_block) or {}
            
            tokens = fm.get("token_count", 0)
            desc = fm.get("description", "No description")
            
            global_tokens += tokens
            mod_tokens += tokens
            
            rel_path = f"{module}/{os.path.basename(fpath)}"
            
            record = {
                "rel_path": rel_path,
                "tokens": tokens,
                "desc": desc
            }
            mod_files.append(record)
            global_files.append(record)
            
            # Use the first file's desc as the module desc roughly
            if len(mod_files) == 1:
                mod_desc = desc
                
        except Exception as e:
            print(f"[06a] WARN: Skipping {fpath}: {e}")

    if not mod_files:
        continue
        
    # Write Module-Level llms.txt
    out_mod_dir = os.path.join(OUTDIR, module)
    os.makedirs(out_mod_dir, exist_ok=True)
    
    with open(os.path.join(out_mod_dir, "llms.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# {module} module\n")
        f.write(f"> **Total Context:** ~{mod_tokens} tokens\n\n")
        for rec in mod_files:
            target = f"./{os.path.basename(rec['rel_path'])}"
            f.write(f"- [{os.path.basename(rec['rel_path'])}]({target}) ({rec['tokens']} tokens) - {rec['desc']}\n")
            
    module_registry[module] = {
        "tokens": mod_tokens,
        "desc": mod_desc,
        "path": f"./{module}/llms.txt"
    }

print(f"[06a] Indexed {len(global_files)} files totaling ~{global_tokens} tokens.")

# Write Root llms.txt
with open(os.path.join(OUTDIR, "llms.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write("# openwrt-docs4ai - LLM Routing Index\n")
    f.write("> For a flat file listing, see [llms-full.txt](./llms-full.txt)\n\n")
    f.write(f"> **Version:** {version_str}\n")
    f.write(f"> **Total Context Available:** ~{global_tokens} tokens\n\n")
    
    for cat_name, mod_list in CATEGORIES.items():
        found = [m for m in mod_list if m in module_registry]
        if found:
            f.write(f"## {cat_name}\n")
            for m in found:
                reg = module_registry[m]
                f.write(f"- [{m}]({reg['path']}): {reg['desc']} (~{reg['tokens']} tokens)\n")
            f.write("\n")
            
    # Fallback for explicitly un-categorized modules
    uncat = [m for m in module_registry.keys() if not any(m in cat_list for cat_list in CATEGORIES.values())]
    if uncat:
        f.write("## Other Components\n")
        for m in sorted(uncat):
            reg = module_registry[m]
            f.write(f"- [{m}]({reg['path']}): {reg['desc']} (~{reg['tokens']} tokens)\n")
        f.write("\n")
            
    f.write("## Complete Aggregation\n")
    f.write("If your context window permits, you may fetch the flat URL index:\n")
    f.write("- [llms-full.txt](./llms-full.txt)\n")

# Write Root llms-full.txt
with open(os.path.join(OUTDIR, "llms-full.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write("# openwrt-docs4ai - Complete Flat Catalog\n")
    f.write(f"> **Total Context:** ~{global_tokens} tokens\n\n")
    
    for rec in sorted(global_files, key=lambda x: x["rel_path"]):
        f.write(f"- [{rec['rel_path']}](./{rec['rel_path']}) ({rec['tokens']} tokens) - {rec['desc']}\n")

print("[06a] Complete: Generated llms.txt, llms-full.txt, and module-level indexes.")
