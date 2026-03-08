# Development Guide

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ (3.12 recommended) | All pipeline scripts |
| Node.js | 20+ | jsdoc2md for API doc generation |
| pandoc | 3.0+ | Wiki dokuwiki→markdown conversion |
| git | 2.25+ | Repo cloning, sparse checkout |
| jsdoc2md | (npm global) | JSDoc to markdown conversion |

## Quick Start (Windows)

```powershell
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/openwrt-docs4ai.git
cd openwrt-docs4ai

# 2. Install Python dependencies
pip install -r .github/scripts/requirements.txt

# 3. Install jsdoc2md globally
npm install -g jsdoc-to-markdown

# 4. Install pandoc (download from https://pandoc.org/installing.html)
#    Or via winget:
winget install --id JohnMacFarlane.Pandoc

# 5. Run the smoke test
python tests/openwrt-docs4ai-00-smoke-test.py
```

### Smoke Test Options

```powershell
# Run with AI summarization (requires API token)
python tests/openwrt-docs4ai-00-smoke-test.py --run-ai

# Keep temp directory for inspection after run
# (preserves files in ./tmp/smoke-test-*/ instead of deleting them)
python tests/openwrt-docs4ai-00-smoke-test.py --keep-temp
```

Results are logged to `tests/openwrt-docs4ai-00-smoke-test-log.txt`.

## Environment Variables

| Variable | Default | Used By | Purpose |
|----------|---------|---------|---------|
| `OUTDIR` | `./openwrt-condensed-docs` | All scripts | Where generated docs are written |
| `WORKDIR` | `./tmp` | 01, 02a–02e | Where source repos are cloned |
| `SKIP_WIKI` | `false` | 02a, 05 | Skip wiki scraping |
| `SKIP_BUILDROOT` | `false` | 01, 02d, 02e, 05 | Skip buildroot/examples |
| `SKIP_AI` | `true` | 04 | Skip AI summarization (default: skipped, see note below) |
| `WIKI_MAX_PAGES` | `300` | 02a | Cap on wiki pages fetched |
| `MAX_AI_FILES` | `40` | 04 | Cap on files to send to AI |
| `GITHUB_TOKEN` | *(none)* | 04 | GitHub Models API auth (CI) |
| `LOCAL_DEV_TOKEN` | *(none)* | 04 | Local development API auth |

## Pipeline Architecture

```
WORKDIR/repo-*  →  OUTDIR/  →  validate  →  promote  →  git commit
(source repos)     (staging)    (07)        (rsync)     (only openwrt-condensed-docs/)
```

In CI, `OUTDIR` points to `$GITHUB_WORKSPACE/staging` so nothing touches the repo until validation passes. Locally, `OUTDIR` defaults to `./openwrt-condensed-docs`.

> **Note on AI Summaries (script 04):** GitHub's free account tier provides only ~50 AI model
> requests per month, making automated summarization impractical for regular pipeline runs.
> The `SKIP_AI` flag defaults to `true` and the pipeline produces fully valid output without
> AI summaries. To manually generate summaries, see the copy-paste prompt in
> `.github/scripts/openwrt-docs4ai-04-generate-ai-summaries.py` — paste it into any AI chatbot
> along with the `.md` file content you want summarized.

## Script Reference

| Script | Phase | Purpose |
|--------|-------|---------|
| `01-clone-repos.py` | 1 | Clone upstream repos into WORKDIR |
| `02a-scrape-wiki.py` | 2 | Scrape OpenWrt wiki (incremental) |
| `02b-scrape-ucode.py` | 2 | Generate ucode API docs (jsdoc2md) |
| `02c-scrape-jsdoc.py` | 2 | Generate LuCI JS API docs (jsdoc2md) |
| `02d-scrape-core-packages.py` | 2 | Extract buildroot package metadata |
| `02e-scrape-example-packages.py` | 2 | Copy curated LuCI examples |
| `02f-scrape-procd-api.py` | 2 | Scrape `procd` init script blocks |
| `02h-scrape-hotplug-events.py` | 2 | Extract network and subsystem hotplug env variables |
| `03-normalize-semantic.py` | 3 | Inject cross-references between docs |
| `04-generate-ai-summaries.py` | 3 | AI-generated module summaries |
| `05-assemble-references.py` | 4 | Build complete reference mega-files & `*-skeleton.md` maps |
| `06-generate-index.py` | 4 | Generate llms.txt, CHANGES.md, index.md |
| `07-validate.py` | 5 | Validation gate (staging check + 2MB size cap) |

## Adding a New Scraper

1. Create `.github/scripts/openwrt-docs4ai-02f-scrape-<name>.py`
2. Follow the header block template (copy from any existing 02x script)
3. Read sources from `WORKDIR`, write output to `OUTDIR/<name>-docs/`
4. Generate a per-folder `llms.txt` index in your output directory
5. Add your script to the Phase 2 parallel block in `pipeline.yml`
6. Add validation rules for your output in `07-validate.py`
7. Add assembly logic in `05-assemble-references.py`
8. Add your index entry to `06-generate-index.py`
9. Add your step to `tests/openwrt-docs4ai-00-smoke-test.py`

## Logging Convention

All scripts use a standardized prefix for log output:

```
[01]  OK: ucode @ abc123               # Success with detail
[02a] SKIP: page too short (45 words)   # Skipped with reason
[02b] WARN: jsdoc2md not found          # Warning, non-fatal
[07] FAIL: llms.txt missing            # Hard failure
```

## Windows Notes

- All scripts are Python — no bash/shell dependency
- Line endings: `.gitattributes` enforces LF for `.py` files
- Path handling: all scripts use `os.path.join()`, no hardcoded `/`
- `jsdoc2md` on Windows: the tool resolves via `shutil.which("jsdoc2md.cmd")`

## Toolchain Gotchas

- **jsdoc underscore exclusion**: The `jsdoc` engine silently excludes any file or directory
  whose path contains an underscore (e.g., `_temp`, `_build`). This bit the CI pipeline when
  `WORKDIR` was set to `$RUNNER_TEMP/work` (which resolved to `/home/runner/work/_temp/work`).
  Always use paths without leading underscores for `OUTDIR` and `WORKDIR`.
