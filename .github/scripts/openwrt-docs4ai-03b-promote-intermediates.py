"""
Purpose: Promote intermediate build layers to the stable staging path.
Phase: Promotion
Layers: L1/L2 -> L1/L2 (WORKDIR -> OUTDIR)
Inputs: tmp/.L1-raw/, tmp/.L2-semantic/, tmp/cross-link-registry.json
Outputs: openwrt-condensed-docs/.L1-raw/ etc.
Environment Variables: WORKDIR, OUTDIR
Dependencies: shutil
Notes: Safely copies the built L1/L2 structures into the output staging directory
       for downstream scripts (04-08) to read.
"""

import os
import shutil
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib import config

sys.stdout.reconfigure(line_buffering=True)

print("[03b] Promote intermediate layers to staging OUTDIR")

WORKDIR = config.WORKDIR
OUTDIR = config.OUTDIR

os.makedirs(OUTDIR, exist_ok=True)

l1_src = os.path.join(WORKDIR, ".L1-raw")
l2_src = os.path.join(WORKDIR, ".L2-semantic")
registry_src = os.path.join(WORKDIR, "cross-link-registry.json")
manifest_src = os.path.join(WORKDIR, "repo-manifest.json")

def promote_dir(src, dst_name):
    dst = os.path.join(OUTDIR, dst_name)
    if os.path.isdir(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f"[03b] Promoted {src} -> {dst}")
    else:
        print(f"[03b] WARN: directory {src} not found to promote.")

def promote_file(src):
    if os.path.isfile(src):
        dst = os.path.join(OUTDIR, os.path.basename(src))
        shutil.copy2(src, dst)
        print(f"[03b] Promoted {src} -> {dst}")
    else:
        print(f"[03b] INFO: File {src} not found to promote (it may be optional).")

promote_dir(l1_src, ".L1-raw")
promote_dir(l2_src, ".L2-semantic")
promote_file(registry_src)
promote_file(manifest_src)

print("[03b] Complete.")
