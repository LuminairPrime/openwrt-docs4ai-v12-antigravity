# openwrt-docs4ai v10 — Pipeline Resilience & Synergy Upgrades

> **Author:** Claude Opus (Antigravity)
> **Date:** 2026-03-05
> **Scope:** Implementing deep resilience fixes and immediate low-risk LLM synergistic optimizations.

## 1. Executive Summary

Version 9 delivered a functional staging-and-promote pipeline, but left subtle edge cases in partial-failure recovery and optimal LLM formatting. **v10** addresses the critical staging deletion flaw, patches bash background process swallowed errors, fixes HTML entity encoding, and introduces synergistic LLM frontmatter and lite-file components.

*(Note: Adding net-new scrapers for core C daemons like `procd`/`netifd` is explicitly deferred to future milestones to avoid timeline risk and folder-bloat).*

---

## 2. GitHub Actions Resilience Upgrades (`00-pipeline.yml`)

### 2.1 Pre-Seeding the Staging Directory
**Goal:** Prevent `rsync --delete` from wiping out historically good documentation if a specific dataset scraper crashes.
**Implementation:**
Add a step immediately prior to Phase 1/2 to seed the empty `$OUTDIR` with the contents of the last committed valid build.

```yaml
      - name: Seed staging directory with last known good documentation
        run: |
          mkdir -p "$OUTDIR"
          if [ -d "$GITHUB_WORKSPACE/$PUBLISH_DIR" ]; then
            cp -a "$GITHUB_WORKSPACE/$PUBLISH_DIR/"* "$OUTDIR/" || true
          fi
```

### 2.2 Catching Silent Subprocess Failures
**Goal:** Stop the pipeline from reporting `Success (0)` if three scrapers fail in the background.
**Implementation:**
Modify Phase 2 `wait`. Standard Bash `wait` returns 0 if we just wait for everything. We need to catch errors.

```bash
# In Phase 2:
python .github/scripts/openwrt-docs4ai-02a-scrape-wiki.py & pid_a=$!
python .github/scripts/openwrt-docs4ai-02b-scrape-ucode.py & pid_b=$!
python .github/scripts/openwrt-docs4ai-02c-scrape-jsdoc.py & pid_c=$!
python .github/scripts/openwrt-docs4ai-02d-scrape-core-packages.py & pid_d=$!
python .github/scripts/openwrt-docs4ai-02e-scrape-example-packages.py & pid_e=$!

# Wait and collect exit codes
exit_code=0
for pid in $pid_a $pid_b $pid_c $pid_d $pid_e; do
  wait $pid || exit_code=1
done

if [ $exit_code -ne 0 ]; then
  echo "One or more scraping processes failed!"
  exit 1
fi
```

### 2.3 CI Concurrency Guard
**Goal:** Prevent overlapping workflow dispatches from race-conditioning the repository.
**Implementation:** Add at the top of `00-pipeline.yml`:
```yaml
concurrency:
  group: docs-pipeline
  cancel-in-progress: true
```

---

## 3. Python String Formatting & File Metadata

### 3.1 YAML Frontmatter Integration
**Goal:** LLM IDE tools (Cursor, Copilot) process standard `---` YAML frontmatter far better than markdown `> **Source:**` blocks. 
**Implementation:** Update `02a`, `02b`, `02c`, `02d`, `02e` to output proper frontmatter at the top of every file.

```markdown
---
layout: default
title: fs
module: fs
source: lib/fs.c
description: filesystem API
generated: 2026-03-05 14:00 UTC
commit: a7e0157
---
# ucode module: fs
...
```

### 3.2 HTML Entity Decoding
**Goal:** Stop `<` and `>` from turning into unreadable `&lt;` and `&gt;` blocks in the LLM outputs.
**Implementation:** In `02b` and `02c`, replace manual string `.replace()` calls with the native Python standard library module `html`:

```python
import html

# After regex stripping block:
output = html.unescape(output)
```

---

## 4. LLM "Skeleton" Reference Assembly (`05-assemble-references.py`)

**Goal:** Large reference files (like the 800KB Wiki doc) blow out smaller LLM context windows. We must generate a matching set of `*-skeleton.md` files that contain only Titles/Headers and function signatures, giving the LLM an ultra-dense searchable index map of the system.
**Implementation:**
Modify the `assemble()` loop in `05`:
1. **Redundant Headers:** Before appending to the *Complete* reference, regex strip the `# title` and `Source` headers specific to that file (since the frontmatter/headers are now redundant in a mega-file).
2. **Skeleton Generation:** Create a parallel `out.write()` stream mapped to `*-skeleton.md`.
3. **Skeleton Content Filtering:** Run a regex parsing logic to extract only lines beginning with `#`, `##`, `###`, and potentially lines immediately containing function signature constraints.

---

## 5. File Size Ceiling (Safeguard)

**Goal:** Prevent runaway storage footprint.
**Implementation:** 
In `05c-validate.py`, add a check that iterates over every single file in the deployment folder.
```python
MAX_FILE_SIZE_MB = 2.0  # complete-reference files usually float around 0.5-1.5 MB max

size_mb = os.path.getsize(fpath) / (1024 * 1024)
if size_mb > MAX_FILE_SIZE_MB:
    hard_fail(f"File {rel} exceeds maximum permissible size of {MAX_FILE_SIZE_MB}MB ({size_mb:.2f}MB).")
```

---

## 6. Implementation Rollout Plan

To ensure no regressions, do the rollout in layers:
1. **GitHub Actions YAML Updates**: Apply Staging Seed, Concurrency, and Parallel Wait logic. Run smoke test.
2. **Scraper Data Headers**: Convert `02*` files to output YAML frontmatter and implement `html.unescape`. Run smoke test.
3. **Validation Thresholds**: Update `05c` with absolute file size caps. Run smoke test.
4. **Assembly Optimization**: Modify `05a` to generate `*-lite.md` and omit redundant concatenation strings. Update `05b` (index generation) to include the new `*-lite.md` artifacts in the root `llms.txt`. Run smoke test.

*No new external datasets/repositories are introduced in this update, keeping variables strictly controlled to architectural health.*
