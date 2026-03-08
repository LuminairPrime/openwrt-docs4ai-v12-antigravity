# openwrt-docs4ai: Execution Roadmap and Rollout Milestones (v12)

> **Date:** 2026-03-07
> **Scope:** A sequential project management roadmap detailing the iterative refactoring and implementation of the L0-L5 topology. This document serves as the tactical milestone checklist for the v12 development sprint, guaranteeing stability by deploying changes iteratively across validated checkpoints.

---

## The Strategic Sequence

To minimize downtime and avoid breaking the existing GitHub Pages deployment during the transition, we must refactor the scripts sequentially—from extraction (L1) through normalization (L2) and finally into presentation (L3-L5). 

We will *not* merge to `main` until the entire 6-checkpoint sequence is running successfully locally.

### Checkpoint 0: Shared Lib & The Smoke Test Suite
**Goal:** Establish the foundational utilities and a rapid local feedback loop before refactoring extractors.
1.  **Create Mock Fixtures (`tests/fixtures/`):** Generate 100% frozen HTML and C-source mocks. This guarantees the smoke test is **deterministic, offline-capable, and independent** of upstream network or repository changes.
2.  **Create `tests/00-smoke-test.py`:** A runner that executes the entire pipeline logic (L2-L5) using the seeded mocks. It MUST include a dedicated test case for **sibling link validation** and **balanced-bracket parameter parsing**.
3.  **Mandatory Config Library:** Build `lib/config.py` as the **Single Source of Truth**. All scripts MUST import their paths and constants from this library.
4.  **Manual Repositories:** Write `CONTRIBUTING.md` (instructions for adding new scrapers) and `docs/ARCHITECTURE.md` (layer definitions mapping).

### Checkpoint 1: The L1 Extractor Refactor (Scripts `02a` to `02h`)
**Goal:** Strip all metadata injection from scrapers so they output pure markdown text to `$WORKDIR/.L1-raw/`.
1.  **Refactor `02a` (Wiki Scraper) First:** Start with the hardest and most complex script. Ensure wiki logic implements network caching (`.cache/wiki-lastmod.json`), maintains a `MANDATORY_PAGES` target list, and outputs pure prose to `.L1-raw/wiki/`.
2.  **Refactor `02b` (ucode C API):** Implement the known `jsdoc2md` bug workaround. (The C transpiler plugin ignores explicit files and recursively scans directories, so each `.c` file must be physically copied into an isolated temporary directory before invoking `jsdoc2md`). Output to `.L1-raw/ucode/`.
3.  **Refactor Remaining `02x`:** Update the rest in dependency order. Point outputs to `$WORKDIR/.L1-raw/{module}/`. Do NOT allow any script to inject YAML (enforce this via validation). Provide parallel validation outputs via `.meta.json` sidebar metadata files.

### Checkpoint 2: The L2 Normalization & Promotion Engine (Script `03`)
**Goal:** Implement the three-phase modular transformation and natively integrated staging promotion logic.
1.  **Phase 1 (YAML & Registry):** Program `03` to iterate over `.L1-raw/`. Inject the **L2 Semantic Schema**, count tokens globally (Fallback: word count * 1.35), and build the symbol registry. Ensure **fatal exits** on missing or malformed `.meta.json`.
2.  **Phase 2 (Cross-linking):** Safely resolve Markdown links across text bodies. MUST protect headers (`#`), code blocks, and existing link/diagram syntax from mutation. 
3.  **Phase 3 (Deprecation Warnings):** Scan API docs for `**Deprecated**` symbols and inject warning callouts into wiki pages that reference them.
4.  **Phase 4 (Promotion):** Atomically promote intermediate layers (`.L1-raw`, `.L2-semantic`, `cross-link-registry.json`, `repo-manifest.json`) from ephemeral `WORKDIR` to the stable `OUTDIR` staging area.

### Checkpoint 2.7: The Optional AI Enricher (Script `04`)
**Goal:** Run the cost-gated AI summarization against the stable `OUTDIR` files explicitly after promotion.
1.  **Optional AI Ext (`04`):** Define `04-generate-ai-summaries.py` to optionally append `ai_summary` tags to the new L2 schemas *in place* in `$OUTDIR/.L2-semantic/` if enabled via `SKIP_AI=false`.

### Checkpoint 3: The L4 Monolithic Assembler (Script `05`)
**Goal:** Stitch the clean L2 arrays together into context-window files, and produce structural sketches.
1.  **Concatenation Logic:** Point at `.L2-semantic/`. Strip internal YAML, insert TOCs with token budgets, and construct **L4 Monoliths**. During the same iteration across grouped modules, output the **L3 Skeletons** (`*-skeleton.md`) as compact navigational aids. Warn if a monolith exceeds 100,000 tokens.

### Checkpoint 4: The L3 & L5 Map Generators (Scripts `06a-d` & `07`)
**Goal:** Split the overgrown indexer into a suite of single-responsibility generators directly outputting to `$OUTDIR`.
1.  **`06a-generate-llms-txt.py`:** Generates both the decision tree `llms.txt` and the `llms-full.txt` lists.
2.  **`06b-generate-agents-md.py`:** Synthesizes the machine-readable repository interaction map `AGENTS.md` and generates the human-readable `openwrt-condensed-docs/README.md` (output self-documentation).
3.  **`06c-generate-ide-schemas.py`:** For v12, extracts signatures and generates `.d.ts` schemas strictly for the `ucode` module only. Outputs to `$OUTDIR/ucode/ucode.d.ts`.
4.  **`06d-generate-changelog.py`:** Generates telemetry tracking API drift (`changelog.json`), failing safely on the "first run" missing baseline scenario.
5.  **`07-generate-index-html.py`:** Outputs the frontend landing payload. Because this script requires `llms.txt` to inject dynamic lists, it is incremented to a new sequential integer (`07`) to mathematically separate it from the parallelizable `06a-d` group.

### Checkpoint 5: The Security & Quality Enforcer (Script `08`)
**Goal:** Build the strict CI/CD gatekeeper `08-validate.py` before touching the workflow files.
1.  **Two-Tier Design:** Build a validation tool that supports `hard_fail()` and `soft_warn()`. Support both `VALIDATE_MODE` and `--warn-only`.
2.  **Hard Checks:** Block CI if `llms.txt` is missing, files are 0 bytes, **exceed 2MB**, YAML is corrupted, or wiki pages crawl Cloudflare/404 HTML text.
3.  **Soft Checks:** Log non-fatal AST parsing warnings from embedded `c`/`javascript` subsets against `node --check` / `ucode -c`.

### Checkpoint 6: CI/CD Pipeline Configuration
**Goal:** Update GitHub Actions (`00-pipeline.yml`) to correctly route our new layered output.
1.  **Dependencies:** Cache pip (`tiktoken`, `pyyaml`, `requests`, `lxml`) and npm (`jsdoc2md`) via `actions/cache` to eliminate the 1-3 minute re-installation overhead.
2.  **Matrix Extractors:** Configure GitHub Actions to execute `02a`-`02h` in parallel. Parallel jobs MUST upload their isolated `.L1-raw/` artifacts, and a subsequent synchronization job MUST download and merge them into a unified `$WORKDIR/.L1-raw/` directory to prevent runner filesystem isolation bugs.
3.  **Workspace Promotion & Concurrency:** Build layers in isolation. Utilize GitHub Actions `concurrency` groups to prevent simultaneous push collisions. Implement a retry-on-conflict logic for the final `git push`. Execute promotion back to the repository branch ONLY if validation (`08`) passes.
4.  **Failure Artifact Flow:** On validation failure (`08-validate.py`), strictly upload `$OUTDIR` (staging) as a downloadable artifact (`actions/upload-artifact`) with 7-day retention for debugging.
5.  **Targeted Parallel Indexes:** Ensure generators `06a, 06b, 06c, 06d` run in parallel. Ensure `07-generate-index-html.py` waits for `06a` to complete, as it mathematically consumes the L3 Map.
6.  **Pages Deployment:** Assemble an `$OUTDIR/public/` directory containing exclusively the generated L3, L4, and L5 files, and push *only* this directory to GitHub Pages to prevent leaking L1/L2 intermediate layers.

---

## Immediate Next Steps (For the Developer)

When development begins, construct **Checkpoint 0** (the Smoke Test and Shared Libs) to allow testing `WORKDIR` mutations locally. After that, move onto **Checkpoint 1 (02a Wiki Scraper)** and steadily work down the checklist, matching the output schemas requested by Opus.
