"""
Purpose: Assemble L4 monolithic references and L3 skeletons from L2 semantics.
Phase: Assembly
Layers: L2 -> L3/L4
Inputs: OUTDIR/.L2-semantic/
Outputs: OUTDIR/{module}/{module}-complete-reference.md
         OUTDIR/{module}/{module}-skeleton.md
Environment Variables: OUTDIR
Dependencies: pyyaml, lib.config
Notes: Strips internal L2 YAML, injects L4 wrapper YAML, warns on >100k tokens.
"""

import os
import glob
import datetime
import sys
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib import config

sys.stdout.reconfigure(line_buffering=True)

try:
    import yaml
except ImportError:
    print("[05] FAIL: 'pyyaml' package not installed")
    sys.exit(1)

OUTDIR = config.OUTDIR
L2_DIR = os.path.join(OUTDIR, ".L2-semantic")

if not os.path.isdir(L2_DIR):
    print(f"[05] FAIL: L2 semantic directory not found: {L2_DIR}")
    sys.exit(1)

TS = datetime.datetime.now(datetime.UTC).isoformat()

print("[05] Assemble L4 monolithic files and L3 skeletons")

modules = [d for d in os.listdir(L2_DIR) if os.path.isdir(os.path.join(L2_DIR, d))]

if not modules:
    print("[05] FAIL: No modules found in L2 semantic directory.")
    sys.exit(1)

warn_count = 0
outputs_generated = 0

for module in sorted(modules):
    mod_dir = os.path.join(L2_DIR, module)
    md_files = sorted(glob.glob(os.path.join(mod_dir, "*.md")))
    
    if not md_files:
        continue
        
    print(f"[05] Processing module: {module} ({len(md_files)} files)")
    
    # We output to the top-level OUTDIR / module path for publishable layers
    out_mod_dir = os.path.join(OUTDIR, module)
    os.makedirs(out_mod_dir, exist_ok=True)
    
    l4_path = os.path.join(out_mod_dir, f"{module}-complete-reference.md")
    l3_skeleton_path = os.path.join(out_mod_dir, f"{module}-skeleton.md")
    
    total_tokens = 0
    concatenated_bodies = []
    skeleton_lines = []
    
    # Process each L2 file
    for fpath in md_files:
        try:
            content = open(fpath, encoding="utf-8").read().strip()
        except Exception as e:
            print(f"[05] WARN: Could not read {fpath}: {e}")
            continue
            
        # Extract and parse frontmatter
        fm_match = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n?(.*)', content, re.DOTALL)
        if not fm_match:
            print(f"[05] WARN: Invalid L2 schema in {fpath}")
            continue
            
        fm_text = fm_match.group(1)
        body_text = fm_match.group(2).strip()
        
        try:
            fm = yaml.safe_load(fm_text) or {}
        except Exception as e:
            print(f"[05] WARN: YAML parse error in {fpath}: {e}")
            continue
            
        # Accumulate metrics
        total_tokens += fm.get("token_count", 0)
        
        # Prepare L4 section body
        concatenated_bodies.append(body_text)
        concatenated_bodies.append("\n\n---\n\n")
        
        # Extract skeleton lines (Headers and function signatures)
        # We assume headers (#) and potentially list items starting with code (`foo()`)
        for line in body_text.splitlines():
            if line.startswith("#"):
                skeleton_lines.append(line)
            # Find function signatures in lists or bold
            elif re.match(r'^[-*]\s+[`*_a-zA-Z0-9]', line):
                # Filter to only lines that look like a signature definition
                if "(" in line and ")" in line and len(line) < 150:
                    # Strip any description after a colon/dash
                    sig = re.split(r'[:|—\-]\s', line, maxsplit=1)[0].strip()
                    skeleton_lines.append(sig)
                    
        skeleton_lines.append("") # Spacer between files in skeleton
        
    # Warn if L4 monolith exceeds 100k limit
    if total_tokens > 100000:
        print(f"[05] WARN: {module} monolith exceeds 100k tokens ({total_tokens})")
        warn_count += 1
        
    # Write L4 Monolith
    with open(l4_path, "w", encoding="utf-8", newline="\n") as l4:
        # L4 Monolith YAML frontmatter
        l4.write("---\n")
        l4.write(f'module: "{module}"\n')
        l4.write(f'total_token_count: {total_tokens}\n')
        l4.write(f'section_count: {len(md_files)}\n')
        l4.write(f'is_monolithic: true\n')
        l4.write(f'generated: "{TS}"\n')
        l4.write("---\n\n")
        
        l4.write(f"# {module} Complete Reference\n\n")
        l4.write(f"> **Contains:** {len(md_files)} documents concatenated\n")
        l4.write(f"> **Tokens:** ~{total_tokens} (cl100k_base)\n\n---\n\n")
        
        l4.write("".join(concatenated_bodies))
        
    outputs_generated += 1
        
    # Write L3 Skeleton
    with open(l3_skeleton_path, "w", encoding="utf-8", newline="\n") as l3:
        l3.write(f"# {module} (Skeleton Semantic Map)\n\n")
        l3.write(f"> **Contains:** Headers and function signatures for {module}.\n")
        l3.write(f"> **Generated:** {TS}\n\n---\n\n")
        
        l3.write("\n".join(skeleton_lines).strip())
        l3.write("\n")
        
    outputs_generated += 1
    
    print(f"[05] OK: {module} L4 ({total_tokens} tokens) and L3 skeleton")

print(f"[05] Complete: {outputs_generated} artifacts generated.")
if warn_count > 0:
    print(f"[05] Process finished with {warn_count} size warnings.")
