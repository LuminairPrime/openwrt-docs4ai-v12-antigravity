# openwrt-docs4ai v9 — Technical Design Document

> **Author:** Claude Opus (Antigravity)
> **Date:** 2026-03-05
> **Revision:** v3 (expanded documentation, improved validation, all-at-once approach)
> **Status:** DRAFT — awaiting final approval
> **Scope:** Complete v8→v9 migration plan covering staging, refactoring, bug fixes, documentation, and repo layout

---

## 1. Executive Summary

This project scrapes OpenWrt documentation from multiple upstream sources (wiki, ucode repo, LuCI repo, buildroot packages) and condenses it into LLM-optimized markdown files. The pipeline runs monthly via GitHub Actions.

**v8** is functional — the local smoke test now passes end-to-end (3 consecutive successes as of 2026-03-05). However, it writes directly to the repo workspace, has 3 bash scripts that break on Windows, uses an unsafe `git add --all`, and has a 409-line monolithic finalize script with no docstrings, no script headers, and minimal inline documentation.

**v9** introduces a **staging-then-promote** architecture so broken scrapes never overwrite good committed output. It also converts all bash to Python, splits the monolith, adds proper validation gating, and ships comprehensive project and in-script documentation. The goal: a pipeline that runs autonomously once a month, indefinitely, without maintenance.

---

## 2. Current Architecture Audit

### 2.1 File Inventory

| File | Language | Lines | Role |
|------|----------|-------|------|
| `00-pipeline.yml` | YAML | 118 | GitHub Actions workflow |
| `01-clone-repos.sh` | Bash | 46 | Clone ucode, luci, openwrt repos |
| `02a-scrape-wiki.py` | Python | 197 | Scrape openwrt.org wiki via sitemap |
| `02b-scrape-ucode.py` | Python | 111 | Generate ucode docs via jsdoc2md |
| `02c-scrape-jsdoc.py` | Python | 102 | Generate LuCI JS API docs via jsdoc2md |
| `02d-scrape-core-packages.sh` | Bash | 193 | Extract buildroot package metadata (embedded Python heredoc) |
| `02e-scrape-example-packages.sh` | Bash | 108 | Copy curated LuCI example apps |
| `03-add-links.py` | Python | 202 | Cross-reference injection + deprecation warnings |
| `04-generate-summaries.py` | Python | 117 | AI summaries via GitHub Models API |
| `05-finalize-publish.sh` | Bash | 409 | Assembly, validation, llms.txt, CHANGES.md, git commit |
| `00-smoke-test.py` | Python | 160 | Local smoke test runner |
| `requirements.txt` | Text | 3 | `requests`, `beautifulsoup4`, `lxml` |

### 2.2 Data Flow

```
  Upstream Sources            Scrapers              Enrichment           Finalize
 ┌──────────────┐         ┌──────────────┐      ┌──────────────┐     ┌─────────────┐
 │ openwrt.org  │─wiki──▶ │ 02a (Python) │──┐   │ 03 add-links │     │ 05 assemble │
 │ jow-/ucode   │─clone─▶ │ 02b (Python) │──┤   │ 04 AI sums   │     │    validate │
 │ openwrt/luci  │─clone─▶ │ 02c (Python) │──┼──▶│              │──▶  │    llms.txt │
 │ openwrt/openwrt│clone─▶ │ 02d (Bash)   │──┤   └──────────────┘     │    commit   │
 │              │        ▶ │ 02e (Bash)   │──┘                        └─────────────┘
 └──────────────┘         └──────────────┘
         01 clone ─────────────┘
```

### 2.3 Output Directories (v8 — all in repo root)

```
ucode-docs/                    # Individual ucode module .md files + llms.txt
luci-docs/                     # Individual LuCI API .md files + llms.txt
openwrt-wiki-docs/             # Individual wiki page .md files + llms.txt
openwrt-buildroot-docs/        # Per-category package docs + llms.txt
openwrt-examples/              # Curated LuCI app source files + llms.txt
ucode-complete-reference.md    # Concatenated mega-file
luci-jsapi-complete-reference.md
openwrt-wiki-complete-reference.md
openwrt-buildroot-complete-reference.md
openwrt-examples-complete-reference.md
llms.txt                       # Root index
CHANGES.md                     # Diff report
```

---

## 3. Bugs and Issues in v8

### 3.1 Critical

| # | Issue | Where | Impact |
|---|-------|-------|--------|
| B1 | **`git add --all .`** commits everything — scripts, temp files, node_modules if cleanup fails | `05:403` | Could commit garbage to repo |
| B2 | **Validation warnings don't fail the build** — `$WARN > 0` prints a message but exits 0 | `05:390-394` | Silently publishes broken output |
| B3 | **Pages artifact uploads entire workspace** — `path: '.'` instead of output dir | `pipeline.yml:102` | Exposes scripts/git history on Pages |

### 3.2 Moderate

| # | Issue | Where | Impact |
|---|-------|-------|--------|
| B4 | `shell=IS_WINDOWS` subprocess fragility | `02b:80`, `02c:53` | Works but brittle; `shutil.which` is cleaner |
| B5 | `npm install` runs without checking for `package.json` | `02b:21` | Noisy errors if no package.json |
| B6 | Silent file skips with no logging in 02b/02c | `02b:89-90`, `02c:63-65` | Hard to debug why modules are missing |
| B7 | `CHANGES.md` fails on first run (git diff on untracked file) | `05:258` | Non-fatal but confusing |
| B8 | Dead `static-docs/` promotion code | `05:221-231` | Dead code, no matching producer |
| B9 | Wiki scrape has no page cap — could run indefinitely | `02a` | Risk of very long runs |
| B10 | `cp --parents` in 02e is GNU-only, breaks on macOS/Windows | `02e:56` | Cross-platform failure |

### 3.3 Minor

| # | Issue | Where |
|---|-------|-------|
| B11 | Inconsistent step numbering in print statements vs actual flow | All scripts |
| B12 | No docstrings or header comments on any script | All scripts |
| B13 | `beautifulsoup4` and `lxml` in requirements.txt but never imported | `requirements.txt` |

---

## 4. v9 Target Repository Layout

```
openwrt-docs4ai/
├── .github/
│   ├── workflows/
│   │   └── pipeline.yml               # GitHub Actions workflow
│   └── scripts/                        # All pipeline scripts (Python only)
│       ├── openwrt-docs4ai-01-clone-repos.py
│       ├── openwrt-docs4ai-02a-scrape-wiki.py
│       ├── openwrt-docs4ai-02b-scrape-ucode.py
│       ├── openwrt-docs4ai-02c-scrape-jsdoc.py
│       ├── openwrt-docs4ai-02d-scrape-core-packages.py
│       ├── openwrt-docs4ai-02e-scrape-example-packages.py
│       ├── openwrt-docs4ai-03-add-links.py
│       ├── openwrt-docs4ai-04-generate-summaries.py
│       ├── openwrt-docs4ai-05a-assemble-references.py
│       ├── openwrt-docs4ai-05b-generate-index.py
│       ├── openwrt-docs4ai-05c-validate.py
│       └── requirements.txt
│
├── tests/
│   ├── openwrt-docs4ai-00-smoke-test.py
│   ├── openwrt-docs4ai-00-smoke-test-log.txt
│   └── openwrt-docs4ai-00-smoke-test-terminal-output-recent.txt
│
├── docs/                               # Human documentation about the project
│   └── plans/                          # Plan docs (this file, prior AI plans)
│
├── openwrt-condensed-docs/             # ALL generated documentation lives here
│   ├── ucode-docs/
│   ├── luci-docs/
│   ├── openwrt-wiki-docs/
│   ├── openwrt-buildroot-docs/
│   ├── openwrt-examples/
│   ├── ucode-complete-reference.md
│   ├── luci-jsapi-complete-reference.md
│   ├── openwrt-wiki-complete-reference.md
│   ├── openwrt-buildroot-complete-reference.md
│   ├── openwrt-examples-complete-reference.md
│   ├── llms.txt                        # Root entry point for AI/humans
│   ├── CHANGES.md
│   └── index.md                        # GitHub Pages link library
│
├── README.md
├── DEVELOPMENT.md
├── .gitignore
├── .gitattributes
└── .nojekyll                           # Skip Jekyll processing for GitHub Pages
```

**Key decisions:**
- **`openwrt-condensed-docs/`** — descriptive, signals intent to humans and AI crawlers, easy to link directly on GitHub. Not `docs/` (already used for project docs) or `output/` (too generic).
- **`docs/plans/`** — all planning documents (this file + existing AI-generated plans) move here to keep `docs/` root clean.
- **All bash scripts eliminated** — Python only for full cross-platform parity.
- **Script 05 split into 3 files** — assembly, indexing, validation are separate concerns.
- **Git commit/push logic stays in the workflow YAML** — not embedded in a script.
- **`.nojekyll`** — simplest GitHub Pages setup. No theme, no config, no build step. GitHub serves the markdown directly. (Idea from Sonnet plan.)

---

## 5. Core v9 Change: Staging Architecture

### 5.1a The OUTDIR Variable

Every script reads one environment variable at startup:

```python
# At the top of every script:
OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
os.makedirs(OUTDIR, exist_ok=True)
```

- **Local dev:** defaults to `./openwrt-condensed-docs` — same output location as the committed folder
- **CI staging:** pipeline sets `OUTDIR=$RUNNER_TEMP/staging` — nothing touches the committed folder until validation passes

### 5.1b The WORKDIR Variable

Cloned repositories go to a separate working directory, not OUTDIR:

```python
WORKDIR = os.environ.get("WORKDIR", os.path.join(os.getcwd(), "tmp"))
```

- **Local dev:** defaults to `./tmp` (already in `.gitignore`)
- **CI:** pipeline sets `WORKDIR=$RUNNER_TEMP/work`
- Clones land in `WORKDIR/repo-ucode/`, `WORKDIR/repo-luci/`, `WORKDIR/repo-openwrt/` — same human-readable names, just tidied into one directory
- Keeping them explicitly named `repo-*` is important for debugging during development

### 5.2 CI Pipeline Flow (v9)

```
 ┌─────────────────────────────────────────────────────────────────┐
 │                    $RUNNER_TEMP                                  │
 │  ┌────────────────┐  ┌───────────┐    ┌────────────┐           │
 │  │  work/         │  │  staging/ │───▶│  VALIDATE  │──┐        │
 │  │  (WORKDIR)     │─▶│  (OUTDIR) │    │  (05c)     │  │        │
 │  │  repo-ucode/   │  └───────────┘    └────────────┘  │        │
 │  │  repo-luci/    │                                   │        │
 │  │  repo-openwrt/ │                                   │        │
 │  └────────────────┘                                   │        │
 └───────────────────────────────────────────────────────│────────┘
            PASS ◄───────────────────────────────────────┘
              │
              ▼
 ┌─────────────────────────────────────────────────────────────────┐
 │              $GITHUB_WORKSPACE (the repo)                       │
 │  ┌────────────┐  ┌────────────────────┐  ┌──────────────────┐  │
 │  │  PROMOTE   │─▶│openwrt-condensed-  │─▶│ git commit       │  │
 │  │  (rsync)   │  │docs/ (final)       │  │ that folder only  │  │
 │  └────────────┘  └────────────────────┘  └──────────────────┘  │
 └─────────────────────────────────────────────────────────────────┘
```

On **failure**: staging is uploaded as a GitHub Actions artifact for debugging. Committed `openwrt-condensed-docs/` is untouched.

### 5.3 Pipeline Pseudocode (YAML)

```yaml
env:
  OUTDIR: ${{ runner.temp }}/staging
  WORKDIR: ${{ runner.temp }}/work
  PUBLISH_DIR: openwrt-condensed-docs

steps:
  - checkout  # openwrt-condensed-docs/ has last month's good files

  - install tools (pandoc, jsdoc2md, pip)

  - Phase 1: clone repos (writes to $WORKDIR/repo-*)
      python .github/scripts/01-clone-repos.py

  - Phase 2: parallel scrapers (read from $WORKDIR, write to $OUTDIR)
      python 02a & python 02b & python 02c & python 02d & python 02e & wait

  - Phase 3: enrichment (mutates files in $OUTDIR)
      python 03-add-links.py
      python 04-generate-summaries.py

  - Phase 4: assembly + indexing (writes merged files to $OUTDIR)
      python 05a-assemble-references.py
      python 05b-generate-index.py

  - Phase 5: VALIDATION GATE (exits non-zero on failure)
      python 05c-validate.py

  - Phase 6: promote (only reached if validate passes)
      rsync -a --delete $OUTDIR/ $GITHUB_WORKSPACE/openwrt-condensed-docs/

  - Phase 7: commit (safe add of known folder only)
      git add openwrt-condensed-docs/
      git diff --cached --quiet || git commit -m "docs: auto-update" && git push

  - on-failure: upload staging as artifact for debugging
```

---

## 6. Script Changes — Detailed

### 6.1 Bash → Python Conversions

There is no fundamental reason these scripts are in bash — Python does the same job with better cross-platform support. `02d` is already 90% Python in a heredoc, and `05` already drops into an embedded Python block mid-script. Converting them is a coin flip for functionality but a clear win for maintainability.

| Script | Why Convert | Complexity |
|--------|-------------|------------|
| `01-clone-repos.sh` | Writes to `GITHUB_ENV`, conditional logic, path handling. Also needs WORKDIR support. | Low — just `subprocess.run(["git", "clone", ...])` into `WORKDIR/repo-*/` |
| `02d-scrape-core-packages.sh` | Already 90% Python in a heredoc — just extract and use OUTDIR | Low — delete the bash wrapper |
| `02e-scrape-example-packages.sh` | Uses `cp --parents` (GNU-only), `find -print0` | Medium — replace with `shutil.copytree` + `pathlib` |

### 6.2 Script 05 Split

The 409-line `05-finalize-publish.sh` becomes three focused Python scripts:

**`05a-assemble-references.py`** (~150 lines)
- Assembles the 5 `*-complete-reference.md` files from modular docs
- One function per reference type (ucode, luci, wiki, buildroot, examples)
- Reads from `OUTDIR`, writes back to `OUTDIR`
- Each dataset skippable via `SKIP_WIKI`, `SKIP_BUILDROOT` env vars

**`05b-generate-index.py`** (~100 lines)
- Generates root `llms.txt` by aggregating per-folder `llms.txt` files
- Generates `CHANGES.md` by diffing against last committed version
- Generates `index.md` for GitHub Pages (link library with one-line descriptions)
- Handles first-run edge case (no prior commit to diff against)

**`05c-validate.py`** (~100 lines)
- Checks file existence, minimum sizes, minimum line counts
- Checks for HTML error pages accidentally saved as markdown (detects `<!DOCTYPE`, `Access denied`, `captcha`, `404 Not Found`)
- Checks for empty/whitespace-only files
- Checks file encoding is valid UTF-8, no binary junk
- Verifies per-folder `llms.txt` files exist and have a minimum number of entries
- **Exits non-zero on any hard failure** (this is the staging gate)
- Accepts `--warn-only` flag for local development
- Reads from `OUTDIR` by default

### 6.3 Git Commit Logic

Moves **out of scripts** and **into the workflow YAML**. This is cleaner because:
- Commit/push is a CI concern, not a script concern
- No risk of a script accidentally committing
- Clear separation: scripts produce files, CI commits them

### 6.4 OUTDIR/WORKDIR Integration Per Script

Every script change is the same pattern — add ~3 lines at the top:

```python
OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
# Then replace all hardcoded paths like "ucode-docs" with:
out_dir = os.path.join(OUTDIR, "ucode-docs")
```

For the clone script (01), repos clone into WORKDIR:

```python
WORKDIR = os.environ.get("WORKDIR", os.path.join(os.getcwd(), "tmp"))
# Clones go to WORKDIR/repo-ucode/, WORKDIR/repo-luci/, WORKDIR/repo-openwrt/
```

Scrapers (02a–02e) need both: they read from WORKDIR (source repos) and write to OUTDIR (generated docs).

### 6.5 Workflow Dispatch Improvements

Add `max_ai_files` as a workflow dispatch input for script 04 (currently hardcoded as `MAX_FILES = 40`). This lets you adjust AI quota usage without a code change:

```yaml
inputs:
  max_ai_files:
    description: 'Maximum files for AI summarization (saves quota)'
    type: number
    default: 40
```

---

## 7. Bug Fixes

| Bug | Fix | Script |
|-----|-----|--------|
| B1: `git add --all` | Move to YAML, `git add openwrt-condensed-docs/` only | pipeline.yml |
| B2: Validation doesn't fail build | `sys.exit(1)` on hard failures in new `05c-validate.py` | 05c |
| B3: Pages uploads whole workspace | Change `path: '.'` to `path: 'openwrt-condensed-docs'` | pipeline.yml |
| B4: `shell=IS_WINDOWS` | Use `shutil.which("jsdoc2md")`, no `shell=True` | 02b, 02c |
| B5: npm install without package.json check | Guard with `os.path.isfile(...)` | 02b |
| B6: Silent skips | Log skipped files: `print(f"  SKIP ({word_count} words): {mod}")` | 02b, 02c |
| B7: CHANGES.md first-run | Check `git ls-files --error-unmatch` before diffing | 05b |
| B8: Dead static-docs code | Delete entirely | 05 (gone in split) |
| B9: No wiki page cap | Add `MAX_PAGES` env var with default 300 | 02a |
| B10: GNU `cp --parents` | Convert to Python `shutil.copytree` | 02e→.py |
| B11: Step numbering | Renumber consistently in all print statements | All |
| B12: No docstrings | Add standardized header blocks (see §8) | All |
| B13: Unused deps | Remove `beautifulsoup4` and `lxml` from requirements.txt | requirements.txt |
| B14: `jsdoc2md` recursive C polling bug | JSDoc implicitly scans directories for `.c` files, ignoring exact CLI overrides. Isolated the parser by generating ad-hoc `tempfile` directories for each C file processed. (See `v10-c-to-md-proposals.md` for replacement architecture proposals). | 02b |

---

## 8. Documentation Plan

The original prompt emphasizes: *"I want this repo and its files to have good documentation (both technical documentation about the operation and in script comment documentation)."* This section covers both.

### 8.1 In-Script Documentation

**Script Header Block** — every script gets a standardized docstring:

```python
"""
openwrt-docs4ai-02a-scrape-wiki.py

Purpose  : Scrape OpenWrt developer wiki pages to individual markdown files.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs) — generated output destination
           WORKDIR (default: ./tmp) — where to find cloned source repos
           SKIP_WIKI ("true" to skip entirely)
           WIKI_MAX_PAGES (default: 300)
Outputs  : $OUTDIR/openwrt-wiki-docs/*.md
           $OUTDIR/openwrt-wiki-docs/llms.txt
Deps     : requests, pandoc (system binary)
Notes    : Incremental — unchanged pages (by lastmod date) are preserved.
           Rate-limited (1.5s between requests) to respect openwrt.org.
"""
```

**Inline Comments** — on non-obvious logic only. No comments restating what the code clearly says. Focus on *why*, not *what*. Examples:
- Why a particular regex pattern was chosen
- Why a file is skipped below a certain word count threshold
- Why `shell=True` is or isn't used in subprocess calls

**Standardized Logging** — consistent prefix format across all scripts for easier log reading in GitHub Actions:

```python
print("[01] Cloning ucode repository...")          # Step identity + action
print("[02a] OK: openwrt-techref-ubus.md (142 lines)")   # Success with detail
print("[02a] SKIP: page too short (45 words)")     # Skipped with reason
print("[02b] WARN: jsdoc2md not found")            # Warning, non-fatal
print("[05c] FAIL: ucode-complete-reference.md missing")  # Hard failure
```

### 8.2 README.md Outline

```markdown
# openwrt-docs4ai

> OpenWrt developer documentation, condensed and optimized for AI LLMs and humans.

## What This Is
- Monthly pipeline scraping 5 upstream sources into compact markdown
- Two formats: modular files (per-module) and complete references (mega-files)
- Entry point: `openwrt-condensed-docs/llms.txt`

## Using the Documentation
- Point your LLM at `openwrt-condensed-docs/llms.txt` for the index
- For deep dives: feed a `*-complete-reference.md` file directly
- For targeted lookups: use individual files in the subdirectories
- GitHub Pages: [link to live site]

## How It Works
- Scripts in `.github/scripts/` run via GitHub Actions monthly
- Staging architecture: generate → validate → promote (never overwrites good output)
- See DEVELOPMENT.md for technical details

## Data Sources
- openwrt.org wiki (techref + guide-developer sections)
- ucode language and module API (jsdoc2md from the jow-/ucode repo)
- LuCI JavaScript client API (jsdoc2md from the openwrt/luci repo)
- OpenWrt buildroot package metadata (Makefiles + READMEs)
- Curated LuCI application examples (4 apps demonstrating key patterns)

## [GitHub Actions Badge]
```

### 8.3 DEVELOPMENT.md Outline

```markdown
# Development Guide

## Prerequisites
- Python 3.11+ (3.12 recommended)
- Node.js 20+ (for jsdoc2md)
- pandoc (for wiki dokuwiki→markdown conversion)
- git

## Quick Start (Windows)
1. Clone the repo
2. Install: `pip install -r .github/scripts/requirements.txt`
3. Install: `npm install -g jsdoc-to-markdown`
4. Install pandoc from https://pandoc.org/installing.html
5. Run: `python tests/openwrt-docs4ai-00-smoke-test.py`

## Environment Variables Reference

| Variable | Default | Used By | Purpose |
|----------|---------|---------|---------|
| OUTDIR | ./openwrt-condensed-docs | All scripts | Output destination |
| WORKDIR | ./tmp | 01, 02a-02e | Cloned repo location |
| SKIP_WIKI | false | 02a, 05a | Skip wiki scraping |
| SKIP_BUILDROOT | false | 01, 02d, 05a | Skip buildroot extraction |
| SKIP_AI | false | 04 | Skip AI summarization |
| WIKI_MAX_PAGES | 300 | 02a | Cap on wiki pages fetched |
| GITHUB_TOKEN | (none) | 04 | GitHub Models API auth |
| LOCAL_DEV_TOKEN | (none) | 04 | Local dev API auth |

## Running the Smoke Test
- Full run: `python tests/openwrt-docs4ai-00-smoke-test.py`
- Skip AI: (default, AI is opt-in) — add `--run-ai` to include
- Keep output for inspection: `--keep-temp`
- Results logged to `tests/openwrt-docs4ai-00-smoke-test-log.txt`

## Adding a New Scraper
1. Create `.github/scripts/openwrt-docs4ai-02f-scrape-<name>.py`
2. Follow the header block template (see any existing 02x script)
3. Read sources from WORKDIR, write output to OUTDIR/<name>-docs/
4. Generate a per-folder `llms.txt` index in your output directory
5. Add your script to the Phase 2 parallel block in `pipeline.yml`
6. Add validation rules for your output in `05c-validate.py`
7. Add assembly logic for your complete reference in `05a-assemble-references.py`
8. Add your index to the root `llms.txt` aggregation in `05b-generate-index.py`
9. Add your step to `tests/openwrt-docs4ai-00-smoke-test.py`

## Architecture
- See docs/plans/ for technical design documents
- Staging architecture explained in the v9 plan
```

### 8.4 .gitignore

```gitignore
# Cloned source repos (generated by script 01)
tmp/

# Legacy v8 clone locations (in case someone runs old scripts)
repo-ucode/
repo-luci/
repo-openwrt/

# Build artifacts
node_modules/
.venv/
*.err

# Smoke test terminal output (large, regenerated each run)
tests/openwrt-docs4ai-00-smoke-test-terminal-output-recent.txt
```

Note: `tests/openwrt-docs4ai-00-smoke-test-log.txt` is **kept in git** as a persistent run history.

---

## 9. Smoke Test Updates

The existing smoke test (`tests/openwrt-docs4ai-00-smoke-test.py`) needs these changes:

1. **Pass `OUTDIR` and `WORKDIR` to subprocesses** — set `env["OUTDIR"] = os.path.join(temp_dir, "openwrt-condensed-docs")` and `env["WORKDIR"] = os.path.join(temp_dir, "tmp")` so scripts read/write in the right places
2. **Call `05c-validate.py`** after assembly/indexing — use it as the real validation gate
3. **Handle the 05 split** — update the step list to run `05a`, `05b`, `05c` instead of monolithic `05`
4. **Remove bash dependency for converted scripts** — change runner from `"bash"` to `"python"` for 01, 02d, 02e
5. **All scripts now Python** — the runner logic simplifies: every step is just `["python", script_path]`

The remote smoke test in the CI pipeline is simply step 5 of the workflow — running `05c-validate.py` against the staging directory. No separate "remote smoke test script" is needed; the validate script *is* the remote smoke test. The local smoke test runner already handles running all scripts in sequence, and its logic doesn't need to be duplicated.

---

## 10. Evaluation of Prior Plans

I reviewed all four existing v9 plans in `docs/`. Here's my assessment:

| Plan | Strengths | Weaknesses |
|------|-----------|------------|
| **Sonnet (claude.ai)** | Most comprehensive — specific bug numbers, line references, actionable. `.nojekyll` idea is good. Best overall. | Slightly over-engineered (05d-commit.sh as separate shell script is unnecessary) |
| **GPT-5.2 (Perplexity)** | Best validation design: two-tier (hard/soft), dataset-specific invariants, HTML error page detection, UTF-8 checks. `status/*.json` concept is clever. | Very dense, scope too large for v9. |
| **Gemini (AI Studio)** | Clean phased approach, good "overlay promotion" concept, standardized error logging | Light on bug fixes, less actionable |
| **Gemini (Perplexity)** | Concise and readable, standardized `[INFO]`/`[ERROR]` logging idea | Missing specific bugs, missing 05-split design |

**Most useful plan: Sonnet (claude.ai)** — best combination of specific bugs and practical solutions. This plan synthesizes its strongest ideas with GPT-5.2's validation tiers and Gemini's logging concept.

**Ideas adopted from other plans into this document:**
- Two-tier validation (hard fail / soft warn) — from GPT-5.2
- HTML error page detection in validation — from GPT-5.2
- UTF-8 encoding checks — from GPT-5.2
- Standardized log prefixes (`[01]`, `[02a]`, etc.) — from Gemini Perplexity
- `.nojekyll` for simple GitHub Pages — from Sonnet
- "How to add a new scraper" guide — from Gemini AI Studio
- `MAX_FILES` as workflow dispatch input — from Sonnet

---

## 11. Implementation Approach

### All-at-once with checkpoint verification

Since every script needs to be opened for OUTDIR anyway, and the pipeline can stay down during development, we'll do all changes in a single pass. This avoids touching the same files twice (e.g., adding OUTDIR to the bash version of 02e and then immediately rewriting it in Python).

The smoke test runs after each phase as a checkpoint — but we're not shipping intermediate states.

### Phase order

| Phase | Tasks | Checkpoint |
|-------|-------|------------|
| **A**: Repo restructure | Move output to `openwrt-condensed-docs/`, plans to `docs/plans/`, create `.gitignore` | Smoke test (paths) |
| **B**: OUTDIR + WORKDIR | Add env vars to all existing scripts | Smoke test (full run) |
| **C**: Bash → Python | Convert `01`, `02d`, `02e` to Python | Smoke test (full run) |
| **D**: Split 05 | Create `05a`, `05b`, `05c`; delete monolith | Smoke test (full run) |
| **E**: Bug fixes | Apply B1–B13 | Smoke test (full run) |
| **F**: Pipeline YAML | Staging, rsync promotion, safe commit, artifact upload, dispatch inputs | Review YAML manually |
| **G**: Smoke test update | OUTDIR/WORKDIR support, step list, validate call | Smoke test (meta!) |
| **H**: Documentation | README.md, DEVELOPMENT.md, script headers, inline comments, `.nojekyll` | Read and review |

### Why not phased releases?

- Every script gets touched for OUTDIR anyway — no savings from splitting
- Phasing means touching the same files twice (OUTDIR-into-bash, then bash-to-Python)
- The smoke test catches regressions regardless of batch size
- Low-priority app with no uptime SLA — no reason to ship intermediate states

---

## 12. Out of Scope for v9 (Future v10+ Ideas)

These are interesting ideas from the existing plans, but they'd over-engineer a pipeline that runs 5 minutes/month. Deferred until the staging gate and refactoring have proven themselves stable:

- **Per-dataset `status/*.json` metadata files** (GPT-5.2) — clever monitoring, but overkill right now
- **Matrix parallelization in GitHub Actions** — sequential with soft-fail is simpler and plenty fast
- **Per-dataset independence** (GPT-5.2) — partial-success promotion where failed datasets keep last-known-good. Good concept but adds significant complexity
- **Delta/incremental updates** — wiki already does this; others don't need it yet
- **Golden samples test set** — good for catching pandoc/jsdoc regressions in a future v10
- **Format drift guards / schema checks** — add after the staging gate proves itself
- **Historical Metrics Log** — Have `06-generate-index.py` append run statistics (Date, WikiCount, LuCICount, TotalSizeMB, etc.) to a persistent `docs/metrics-history.csv` file to track source health over years.
- **Enhanced Local Smoke Test Logging** — Update the smoke test run log (`tests/openwrt-docs4ai-00-smoke-test-log.txt`) to record the individual file count and total byte size of each generated output folder for better local diagnostics.

---

## 13. Verification Plan

### 13.1 Automated: Local Smoke Test

After each phase, run:
```powershell
python tests/openwrt-docs4ai-00-smoke-test.py
```
All steps must show `PASS` or `SKIPPED` (for AI step). The test log at `tests/openwrt-docs4ai-00-smoke-test-log.txt` will record results.

### 13.2 Automated: Validate Script

Once `05c-validate.py` exists:
```powershell
python .github/scripts/openwrt-docs4ai-05c-validate.py --out-dir ./openwrt-condensed-docs
```
Must exit 0 with all checks passing.

### 13.3 Manual: Verify Output Integrity

After a full smoke test run with `--keep-temp`:
1. Inspect `tmp/openwrt-docs4ai-smoke-test-*/openwrt-condensed-docs/llms.txt` — should list all datasets
2. Spot-check 2-3 `.md` files in each output subdirectory for correct headers including `**Source:**`, `**Generated:**`
3. Confirm `CHANGES.md` is generated (even if empty on first run)
4. Verify no HTML error pages slipped through (search for `<!DOCTYPE` in output)

### 13.4 Manual: CI Dry Run

Push to a branch and trigger `workflow_dispatch` manually. Verify:
- Pipeline uses `$RUNNER_TEMP/staging` for OUTDIR and `$RUNNER_TEMP/work` for WORKDIR (check step logs)
- Validation step runs before commit
- Only `openwrt-condensed-docs/` is committed (check the commit diff)
- On intentional failure: staging is uploaded as artifact

### 13.5 Documentation Review

- README.md: read on GitHub — does it make sense to someone seeing the repo for the first time?
- DEVELOPMENT.md: follow the Quick Start steps on a clean Windows machine
- Script headers: every `.py` file in `.github/scripts/` should have the standardized docstring

---

## 14. Review Decisions (Resolved)

| Question | Decision |
|----------|----------|
| Output folder name | `openwrt-condensed-docs/` — descriptive, lowercase-hyphenated, easy to reference |
| Plan docs location | Move to `docs/plans/` — good practice to keep project docs tidy |
| v9 scope | Confirmed — staging + refactoring + docs. v10+ ideas deferred. Pipeline runs 5 min/month; keep it simple. |
| Clone directories | Move to `WORKDIR/repo-*/` — tidier, same human-readable names for debugging |
| Implementation approach | All-at-once with smoke test checkpoints between phases. No phased releases. |
| Bash → Python | All bash converted to Python. No fundamental capability gap; bash was a coin flip and Python wins on cross-platform. |

---

## 15. Known Architectural Workarounds

### 15.1 `jsdoc2md` C-File Parsing Bug
**The Problem:** The `jsdoc2md` parser combined with the `c-transpiler` plugin contains a severe logic bug where supplying an `includePattern` for `.c` files causes the underlying engine to recursively scan the entire directory and inject every C file's documentation into every single generated output file. It completely ignores explicit file arrays passed via the `--files` CLI argument.
**The v9 Workaround:** `02b-scrape-ucode.py` executes `jsdoc2md` by creating a Python `tempfile.TemporaryDirectory()`, copying the single target C file into it, writing an ephemeral configuration file, and executing the binary inside that isolated void. By feeding the buggy recursive directory scanner an empty directory containing only the target file, it successfully outputs clean, concise token-efficient API documentation.
**Future Remediation:** This workaround is stable and costs zero development overhead. If it breaks in the future due to upstream `ucode` syntax updates that the Javascript transpile plugin cannot understand, DO NOT attempt to rewrite the Javascript plugin. Instead, consult `docs/plans/v10-c-to-md-proposals.md` and upgrade the entire pipeline step to a native C-to-Markdown tool like **Doxide**.
