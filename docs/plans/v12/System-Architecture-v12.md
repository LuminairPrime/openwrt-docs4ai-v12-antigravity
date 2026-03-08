# openwrt-docs4ai: System Architecture and Implementation Design (v12)

> **Date:** 2026-03-07
> **Scope:** The definitive technical architecture for the v12 multi-tier data supply chain. This document maps the sequence of extractor algorithms, defining normalization mechanics, validation constraints, the overarching continuous integration topology, and the exact environment vectors governing runtime execution.

---

## 1. Executive Summary

Version 12 represents a profound paradigm shift from "Data Extraction" to a "Data Supply Chain." 

We are rebuilding the internal pipeline topology to produce strict, categorized layers of documentation. By decoupling the extraction logic (scraping) from the presentation logic (metadata injection + formatting), we can generate exact, schema-validated documentation tailored for vastly different stakeholders (Raw Analysts, Vector DBs, IDEs, and LLMs). A given stakeholder can now point an ingestion tool at a specific layer (e.g., L2) and guarantee that *every* file conforms to the strict YAML schema defined in our topology.

---

## 2. Core Architectural Refactoring (The Supply Chain)

### 2.0 Architectural Invariants (Mandatory)
- **Centralized Configuration**: All scripts MUST import constants (dirs, modules, regex patterns) from `lib/config.py`. Hardcoded paths in scripts are a hard failure.
- **Staging-First Build**: Scripts MUST write to isolated `staging/` or `tmp/` directories. Atomic promotion to the repository branch occurs ONLY after the validation suite (`08`) passes.
- **Resource Management**: Every file operation MUST use a context manager (`with open(...) as f:`). Bare `open().read()` calls are prohibited to prevent file handle exhaustion in high-concurrency environments.
- **Cross-Platform Pathing**: All internal references (links, manifests) MUST use POSIX forward-slashes (`/`). Scripts running on Windows must normalize paths before storage.

The pipeline scripts will be aggressively refactored to align with the explicit schema examples defined in `v12-documentation-topology-tech-spec.md`.

### 2.1 Standardizing the Extractors (L1 Target)
- **Target Scripts:** `02a` through `02h` (The Scraper Suite).
- **Implementation:** Strip all YAML frontmatter injection from extractors. The scripts fetch data, write to `$WORKDIR/.L1-raw/`, and emit a companion `.meta.json` sidebar containing origin context.
- **Content Integrity:** Every L1 file MUST have a `content_hash` (truncated SHA256) calculated during the write process and stored in its `.meta.json`.
- **Wiki Rate Limiting & Sniper Targets:** The wiki scraper (`02a`) MUST enforce a hard 1.5-second delay to defend against global bot rate-limits. Additionally, `02a` MUST maintain an internal `MANDATORY_PAGES` list (e.g., `/docs/techref/ubus`). These "sniper" targets MUST always be attempted and MUST bypass any age-based cutoff logic (`CUTOFF`) to ensure critical API context is never lost during pruning cycles.
- **DokuWiki Ghost Pages:** Scrapers targeting DokuWiki MUST check for the "This topic does not exist" string in raw exports to catch 200 OK responses for non-existent pages.
- **Extractor Failure Modes:** Individual file extraction failures (e.g. 404, bad markup) are handled as *soft warnings*—the script logs, skips the file, and proceeds. However, if a script processes the upstream target and yields **zero output files**, it must exit non-zero (hard fail), signaling that the upstream structure likely changed and the scraper is broken.
- **Filename Collision Resolution:** If two independent source files resolve to the exact same `{origin_type}-{slug}.md` destination, the scraper MUST append a 4-character content hash to the filename base to guarantee uniqueness.
- **The Code Wrapper Compliance Check:** Scripts fetching raw code must conform to the **L1 Raw Code Schema**. They will wrap the code in markdown fences (```` ```javascript ````) prepended with an `H1` denoting the file name.

### 2.2 The Normalization & Promotion Engine (L2 Target, Modular Three-Phase)
- **Target Script:** `03-normalize-L2.py`.
- **Integrated Pipeline Role:** This script functions as the primary state-machine for documentation enrichment. It natively handles metadata injection, cross-linking, and the final atomic promotion to the staging area to guarantee that only fully-processed artifacts reach the output directory.
- **Modular Internal Structure:** The script MUST be partitioned into discrete, testable functions for (1) `pass_1_normalize_all`, (2) `pass_2_link_all`, and (3) `promote_to_staging`.
- **Reproducible Determinism:** Iterate over modules and files in sorted alphabetical order. Output YAML keys in identical deterministic sequences via a robust YAML serializer (`pyyaml`). 
- **Performance Constraints:** All regex patterns used for symbol replacement MUST be pre-compiled *once* outside the file processing loops.
- **Implementation (Pass 1 - Stamping):** Ingest `.L1-raw/` and `.meta.json` files. Calculate tokens for the Markdown *body only*. Apply the **L2 Semantic Schema**. Extract signatures to a JSON registry (`cross-link-registry.json`). 
- **Pass 1 Failure Boundary:** If the corresponding `.meta.json` is missing or malformed, `03-normalize-L2.py` MUST trigger a fatal error and exit non-zero immediately.
- **Implementation (Pass 3 - Deprecation):** Scan `ucode` and `luci` API docs for symbols followed by "Deprecated" markers. Tag these in the registry. For wiki pages referencing these symbols, inject a `[!WARNING]` callout to alert the agent/user of upcoming API breakage.
- **Implementation (Promotion):** Once the three passes are clean, atomically copy the stage layers from `WORKDIR` to `OUTDIR`. Clear existing `OUTDIR` staging subdirectories first to ensure build purity.
- **Optional AI Extractor (`04`):** If `SKIP_AI=false`, script `04` appends the `ai_summary` field in-place within the staged layer. 
- **Manual AI Override Pattern:** The script docstring MUST include a "Manual Override" prompt. This prompt is designed as an **operational mission plan** (pseudocode) that allows a human to paste the prompt and file content into a frontier LLM (Claude/GPT) to achieve a 1-to-1 functional replacement for the script when API credits are exhausted or the environment is isolated.
- **Prompt Content Standards:** The prompt MUST specify the exact YAML tags to generate (`ai_summary`, `ai_when_to_use`, `ai_related_topics`), enforce "No Hallucination" rules (only naming symbols present in the text), and mandate a "Clean Copy" response format (Markdown block with modified content only).

**Explicit Schema Example (Manifest - `repo-manifest.json`):**
```json
{
  "openwrt": { 
    "url": "https://github.com/openwrt/openwrt",
    "branch": "master",
    "commit": "abcdef1", 
    "timestamp": "2026-03-07T12Z",
    "fetch_status": "success",
    "error_state": null
  },
  "ucode": { "url": "https://github.com/jow-/ucode", "branch": "master", "commit": "e87be9d", "timestamp": "2026-03-07T12Z", "fetch_status": "success", "error_state": null },
  "luci": { "url": "https://github.com/openwrt/luci", "branch": "master", "commit": "1a2b3c4", "timestamp": "2026-03-07T12Z", "fetch_status": "success", "error_state": null },
  "procd": { "url": "https://git.openwrt.org/project/procd.git", "branch": "master", "commit": "9f8e7d6", "timestamp": "2026-03-07T12Z", "fetch_status": "success", "error_state": null }
}
```

### 2.3 Formalizing the Indexes (L3 & L5 Targets)
- **Target Scripts:** `06a` through `06d` (Parallel Generators), `07` (Sequential HTML generator).
- **Implementation:** The index generators validate and aggregate YAML metadata from the `.L2-semantic/` directory to build the `llms.txt` maps, `.d.ts` schemas, and HTML indexes into the root `$OUTDIR`.
- **IDE TypeScript Generics:** Extract function definitions via `cross-link-registry.json` (authoritative inventory list), parsing parameter types from the associated L2 Markdown headings. For v12, `.d.ts` generation is strictly scoped to `ucode` module APIs only (`$OUTDIR/ucode/ucode.d.ts`); LuCI JS is deferred. The pipeline MUST map types as follows: `string`->`string`, `int`/`double`->`number`, `bool`->`boolean`, `array`->`any[]`, `object`->`Record<string, any>`, `resource`->`object`, `null`->`null`, `unknown`->`any`.
- **L5 Telemetry Expansion:** Output both the `CHANGES.md` human diff and the `changelog.json` schema. Baseline retrieval fallback chain: (1) try `github-release` with token, (2) if token empty/API fails, check for local `signature-inventory.json` in the committed workspace, (3) operate in "no baseline" mode. Log which path was taken.

---

## 3. Agentic Web Enhancements (Migrated from v11 Plan)

These features ensure that autonomous agents can grok the repository instantly without blind scraping.

### 3.1 `AGENTS.md` and Dual-Faceted Routing
- Automatically synthesize a root `AGENTS.md` specifying repository interaction rules, test suite commands, and the documentation taxonomy.
- Restructure the top-level `/llms.txt` into an optimal "Decision Tree" (guiding an Agent to the correct subfolder).
- Create a secondary `/llms-full.txt` that functions as a flat aggregate catalog for automated ingestors.

### 3.2 Visual Architecture Mapping (Mermaid.js)
- Enhance the L2 normalization engine (`03`) to recognize target architecture files and statically inject curated ````mermaid` sequence diagram templates from the `templates/mermaid/` directory into the headers of relevant core daemons (e.g., `procd`, `hotplug`). *Note: Dynamic/Automatic diagram rendering is explicitly out of scope for v12 due to hallucination risks.*

---

## 4. Pipeline Execution & Delivery Updates

### 4.1 Artifact Splitting
- Modify `openwrt-docs4ai-00-pipeline.yml` to bundle `.L1-raw/` and `.L2-semantic/` as downloadable `.zip` release artifacts attached to the monthly run.
- GitHub Pages will exclusively host the L3, L4, and L5 layers as the "human and agent front-door."

### 4.2 Incremental Cost Reduction
- **Wiki Scraping Cache (`If-Modified-Since`):** Modify `02a-scrape-wiki.py` to store and check local HTTP `Last-Modified` metadata logic in `.cache/wiki-lastmod.json`, persisting across CI runs via `actions/cache`.
- **Concurrency & Push Triggers:** Enforce workflow concurrency to cancel in-progress runs on branch pushes using `concurrency: { group: docs-pipeline-${{ github.ref }}, cancel-in-progress: true }`. Restrict `push` triggers to `.github/scripts/**`, template folders, and `.yaml` workflow files.
- **Diff Commits:** Execute a diff comparison mapping of the generated output vs existing branch output. If no diff exists, the pipeline simply skips committing instead of creating an empty bump commit.

---

## 5. Security and Validation
- **Two-Tier Validation Engine (`08-validate.py`):** Validation is split into Hard Fails and Soft Warns.
- **Hard Checks (Fails CI):** 
  - Missing `llms.txt` or zero-byte files.
  - Files exceeding a **2.0MB Size Ceiling** (indicates crawler loops or binary leak).
  - Malformed YAML frontmatter anywhere globally.
  - Strict JSON schema validation failures for the pipeline control files (`repo-manifest.json`, `cross-link-registry.json`, `signature-inventory.json`).
  - **Broken Link Detection:** The validator MUST use a **negative-lookahead regex** to identify relative Markdown links while ignoring external protocols: `\[.*?\]\(((?!https?:\/\/|mailto:|[a-z0-9]+:).*?\.md)\)`. This ensures that sibling links without `./` or `../` prefixes are correctly validated.
  - **HTML Leak Protection:** The script MUST check L1 files against this explicit signature list: `404 Not Found`, `Cloudflare`, `Access Denied`, `<!DOCTYPE`, `<html`, `Just a moment...`, `Checking your browser`, `captcha`, `Service Temporarily Unavailable`, and `Rate limit exceeded`.
- **The AST Linter Guardrail (Soft Warn Mode):** Validates the code blocks embedded within the generated markdown syntactically against standard tools (e.g. `node --check`, `ucode -c`). Since code extracts are often partial expressions or isolated, this runs as a *soft warning* rather than a hard failure to avoid brittle CI pipelines.

---

## 6. Development Standards & Environment

### 6.1 Logging and Header Specifications
- **Script Headers:** Every pipeline script MUST begin with a standardized docstring block declaring: Purpose, Phase, Layers, Environment Variables, Inputs, Outputs, Dependencies, and Notes. *(Refer explicitly to Addendum Section A5 from the Opus review for the exact 10-line Python template.)*
- **Logging Format:** All scripts must emit logs conforming to `[SCRIPT_ID] LEVEL: message` (e.g. `[02a] OK: Scraped 15 pages`).

### 6.2 Environment Variable Matrix
| Variable | Default Value | Scripts Utilizing | Purpose |
|:---|:---|:---|:---|
| `WORKDIR` | `tmp` | All | Ephemeral dir for repo clones & intermediate outputs. |
| `OUTDIR` | `openwrt-condensed-docs` | `03`, `04`, `05`, `06*`, `07`, `08` | Stable dir for final deliverable publishing. |
| `SKIP_WIKI` | `false` | `02a` | Bypasses the wiki scraper (which takes ~10m) if true. |
| `SKIP_AI` | `true` | `04` | AI enrichment is opt-in (costs money). Set to false to run. |
| `WIKI_MAX_PAGES` | `300` | `02a` | Breadth safety limit for scraper traversal graph. |
| `MAX_AI_FILES` | `40` | `04` | Quota budget limit defining how many files to hit the LLM with. |
| `VALIDATE_MODE` | `hard` | `08` | Strict validation enforcement mode. `warn` permits failures. Supports `--warn-only` CLI flag. |
| `MERMAID_INJECT`| `true` | `03` | Toggle curated template diagram injection. |
| `GITHUB_TOKEN` | (Empty) | `06d` | Required to fetch previous Releases for signature baseline. |
| `LOCAL_DEV_TOKEN` | (Empty) | `04` | Local dev override for querying the upstream LLM inference API. |
| `LLM_BUDGET_LIMIT`| `$5.00`| `04` | Hard-coded circuit breaker terminating `04` to prevent infinite loop billing overruns. |
| `TOKENIZER` | `cl100k_base` | `03`, `04` | Specifies the tokenizer target for token cost sizing. |
| `DTS_GENERATE` | `true` | `06c` | Kill-switch toggle for experimental TypeScript definitions. |
| `BASELINE_SOURCE`| `github-release`| `06d` | Options: `github-release`, `local`, `none`. Drives diff tests. |
| `AI_CACHE_PATH` | `ai-summaries-cache.json` | `04` | Path to the persistent JSON archive of generated AI metadata. |
| `RUNNER_TEMP` | (CI Built-in) | CI YAML, `WORKDIR` | GitHub absolute path to runner temporary volume. |
| `GITHUB_WORKSPACE` | (CI Built-in) | CI YAML | GitHub standard workspace path where repo is executed. |
