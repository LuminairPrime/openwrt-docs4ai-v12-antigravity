"""
Purpose: Generates the repository interaction map (AGENTS.md) and human README.md.
Phase: Indexing
Layers: L3
Inputs: OUTDIR/
Outputs: OUTDIR/AGENTS.md, OUTDIR/README.md
Environment Variables: OUTDIR
Dependencies: lib.config
Notes: Provides machine-readable guidelines for AI agents and human-readable docs.
"""

import os
import datetime
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib import config

sys.stdout.reconfigure(line_buffering=True)

OUTDIR = config.OUTDIR
REGISTRY_PATH = os.path.join(OUTDIR, "cross-link-registry.json")
TS = datetime.datetime.now(datetime.UTC).isoformat()

print("[06b] Generating AGENTS.md and README.md")

module_count = 0
total_tokens = 0
if os.path.isfile(REGISTRY_PATH):
    try:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            registry = json.load(f)
            total_tokens = sum(meta.get("token_count", 0) for meta in registry.get("symbols", {}).values())
            # Count modules by checking L2 directory or registry symbols
            modules = set()
            for meta in registry.get("symbols", {}).values():
                if "module" in meta: modules.add(meta["module"])
            module_count = len(modules)
    except: pass

os.makedirs(OUTDIR, exist_ok=True)

agents_content = """# AGENTS.md — AI Agent Instructions for openwrt-docs4ai

## Repository Structure
- `llms.txt` — Start here. Hierarchical index linking to each target subsystem.
- `llms-full.txt` — Flat listing of every document with token counts.
- `[module]/*-complete-reference.md` — Monolithic L4 file best ingested if context size permits.
- `[module]/*-skeleton.md` — Structural API outlines serving as navigational aids.
- `[module]/*.d.ts` — TypeScript definitions for IDEs and static analysis.

## Conventions
- All token counts use `cl100k_base` encoding.
- Cross-references use relative Markdown links.
- Files strictly adhere to the v12 Schema Definitions.

## Rules & Constraints
1. **Entry Point:** Always begin navigation at `llms.txt`. Do not guess paths.
2. **Context Budgets:** Respect your context window limits. Prefer `*-skeleton.md` files for structural understanding before fetching monolithic references.
3. **No Hallucination:** DO NOT hallucinate API parameters or functions outside of what is defined in the `*-skeleton.md` indexes or the text bodies.
4. **Wiki Scraping:** DO NOT blindly scrape the live OpenWrt wiki. Use these pre-processed, deduplicated documents instead to save tokens and avoid 404s.
"""

readme_content = f"""# openwrt-docs4ai Generated Pipeline Output

**Pipeline Run Date:** {TS}
**Baseline Version:** Auto-generated via CI/CD

This repository branch contains the automatically generated, stable L3, L4, and L5 documentation layers for OpenWrt. 

To ingest this repository into an AI context window (e.g. Claude, GPT-4, Cursor), begin your prompt by referencing:

```
https://openwrt.github.io/openwrt-docs4ai/llms.txt
```

For AI Agents iterating on workflows, please read [AGENTS.md](./AGENTS.md) for structural mapping and rules.
"""

with open(os.path.join(OUTDIR, "AGENTS.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write(agents_content)

with open(os.path.join(OUTDIR, "README.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write(readme_content)

print("[06b] Complete.")
