"""
Purpose: Generates telemetry tracking API drift (changelog.json).
Phase: Telemetry
Layers: L5
Inputs: OUTDIR/ (Current Run), baseline/signature-inventory.json (Baseline)
Outputs: OUTDIR/changelog.json, OUTDIR/CHANGES.md, OUTDIR/signature-inventory.json
Environment Variables: OUTDIR
Dependencies: lib.config
Notes: Fails safely if baseline is missing. Saves current signatures for next run.
"""

import os
import json
import datetime
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib import config

sys.stdout.reconfigure(line_buffering=True)

OUTDIR = config.OUTDIR
REGISTRY_PATH = os.path.join(OUTDIR, "cross-link-registry.json")
BASELINE_DIR = os.path.join(os.getcwd(), "baseline") # Logic for baseline source is underspecified in v12, assuming local 'baseline/' dir
BASELINE_PATH = os.path.join(BASELINE_DIR, "signature-inventory.json")

print("[06d] Generating L5 Changelog and Telemetry")

if not os.path.isfile(REGISTRY_PATH):
    print(f"[06d] FAIL: cross-link-registry.json not found at {REGISTRY_PATH}")
    sys.exit(1)

try:
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)
except Exception as e:
    print(f"[06d] FAIL: Could not parse registry: {e}")
    sys.exit(1)

# Current inventory: simple map of symbol -> signature
current_inventory = {sym: meta.get("signature") for sym, meta in registry.get("symbols", {}).items()}

# Load baseline
baseline_inventory = {}
if os.path.isfile(BASELINE_PATH):
    try:
        with open(BASELINE_PATH, "r", encoding="utf-8") as f:
            baseline_inventory = json.load(f).get("signatures", {})
        print(f"[06d] Loaded baseline with {len(baseline_inventory)} signatures.")
    except Exception as e:
        print(f"[06d] WARN: Could not parse baseline inventory: {e}")
else:
    print("[06d] INFO: No baseline inventory found. This is likely the first run.")

# Calculate drift
added = []
removed = []
changed = []

for sym, sig in current_inventory.items():
    if sym not in baseline_inventory:
        added.append({"symbol": sym, "signature": sig})
    elif baseline_inventory[sym] != sig:
        changed.append({
            "symbol": sym,
            "old": baseline_inventory[sym],
            "new": sig
        })

for sym in baseline_inventory:
    if sym not in current_inventory:
        removed.append({"symbol": sym, "signature": baseline_inventory[sym]})

changelog = {
    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
    "summary": {
        "added": len(added),
        "removed": len(removed),
        "changed": len(changed)
    },
    "details": {
        "added": added,
        "removed": removed,
        "changed": changed
    }
}

# Write changelog.json
with open(os.path.join(OUTDIR, "changelog.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(changelog, f, indent=2)

# Write CHANGES.md (Human readable summary)
changes_md = [
    "# openwrt-docs4ai API Displacement Log",
    f"**Run Date:** {datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M UTC')}",
    "",
    "## Summary",
    f"- **Added:** {len(added)}",
    f"- **Removed:** {len(removed)}",
    f"- **Changed:** {len(changed)}",
    ""
]

# FIX BUG-046: Track module-level changes
current_modules = set()
for meta in registry.get("symbols", {}).values():
    if "module" in meta: current_modules.add(meta["module"])

# We don't have a module-level baseline in the signature inventory yet, 
# but we can infer it from the symbols in the baseline.
baseline_modules = set()
for sym in baseline_inventory.keys():
    if "." in sym: baseline_modules.add(sym.split(".")[0])

added_mods = sorted(current_modules - baseline_modules)
removed_mods = sorted(baseline_modules - current_modules)

if added_mods:
    changes_md.append("## New Modules")
    for m in added_mods:
        changes_md.append(f"- `[NEW] {m}`")
    changes_md.append("")

if removed_mods:
    changes_md.append("## Removed Modules")
    for m in removed_mods:
        changes_md.append(f"- `[DEL] {m}`")
    changes_md.append("")

if added:
    changes_md.append("## Added Symbols")
    for item in sorted(added, key=lambda x: x["symbol"]):
        changes_md.append(f"- `{item['symbol']}` : `{item['signature']}`")
    changes_md.append("")

if removed:
    changes_md.append("## Removed Symbols")
    for item in sorted(removed, key=lambda x: x["symbol"]):
        changes_md.append(f"- `{item['symbol']}`")
    changes_md.append("")

if changed:
    changes_md.append("## Modified Signatures")
    for item in sorted(changed, key=lambda x: x["symbol"]):
        changes_md.append(f"- `{item['symbol']}`")
        changes_md.append(f"  - **Was:** `{item['old']}`")
        changes_md.append(f"  - **Now:** `{item['new']}`")
    changes_md.append("")

with open(os.path.join(OUTDIR, "CHANGES.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(changes_md))

# Save current inventory for next run
inventory_payload = {
    "generated": datetime.datetime.now(datetime.UTC).isoformat(),
    "signatures": current_inventory
}
with open(os.path.join(OUTDIR, "signature-inventory.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(inventory_payload, f, indent=2)

print(f"[06d] OK: changelog.json, CHANGES.md, signature-inventory.json")
