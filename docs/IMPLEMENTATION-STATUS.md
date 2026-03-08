# v12 Implementation Status

## Current Checkpoint
**Pending Checkpoint 3**

## Log
### 2026-03-08 (Checkpoint 1)
- **Refactored `02a-scrape-wiki.py`**: Stripped YAML injection, implemented `.cache/wiki-lastmod.json`, output pure prose to `.L1-raw/wiki/`.
- **Refactored `02b-scrape-ucode.py`**: Cleaned JS/C extraction, kept `jsdoc2md` isolated temp dir workaround exactly as required, pure markdown out.
- **Refactored `02c-to-02h` extractors**:
  - `02c`: LuCI JS API
  - `02d`: Core packages and Makefiles
  - `02e`: Curated examples (wrapped in Markdown code blocks)
  - `02f`: procd API
  - `02g`: UCI schemas
  - `02h`: hotplug events
- **Validation**: All extractors now use the A5 10-line header, output securely to `tmp/.L1-raw/` using `lib.extractor.write_l1_markdown()`, generate `.meta.json` sidecars, and avoid YAML frontmatter.
- **Testing**: `tests/smoke-test-log.txt` preserves run logs (mocked jsdoc plugin for 00-test).
- **Git State**: Committed Checkpoint 1 as `feat: complete Checkpoint 1 (refactor 02a-02h extractors to L1 schema)`.

### 2026-03-08 (Checkpoint 2, 2.5, 2.7)
- **Created `03-normalize-L2.py` Engine**: Replaced `03-add-links.py` with a two-pass architecture.
  - Pass 1: Global tiktoken counting, YAML frontmatter injection, Mermaid template injection, and building `cross-link-registry.json`.
  - Pass 2: Injects relative cross-links using the generated registry.
- **Created `03b-promote-intermediates.py` (CP 2.5)**: Coded explicit promotion of `$WORKDIR/.L1-raw`, `.L2-semantic`, `cross-link-registry.json`, and `repo-manifest.json` to `$OUTDIR`.
- **Refactored `04-generate-summaries.py` (CP 2.7)**: Adjusted AI enrichment to target the promoted stable L2 layer in `$OUTDIR/.L2-semantic/` and inject `ai_summary` securely into existing YAML frontmatter.
- **Git State**: Committed Checkpoints 2, 2.5, and 2.7 as `feat: complete Checkpoints 2/2.5/2.7 (L2 Normalizer, Promotion, AI Enrich)`.

### 2026-03-08 (Checkpoint 3)
- **Refactored `05-assemble-references.py`**: Rewrote the monolithic assembler to consume the stable `$OUTDIR/.L2-semantic/` directory instead of ad-hoc L1 paths.
- It parses the L2 YAML schema, strips it, concatenates bodies, and wraps everything in the rigid L4 Monolith Schema YAML frontmatter.
- It concurrently generates the L3 `*-skeleton.md` files by extracting headers and function signatures during the iteration pass.
- **Git State**: Committed Checkpoint 3 as `feat: complete Checkpoint 3 (L4 Monolithic Assembler)`.

## Next Action
- Begin Checkpoint 4: The L3 & L5 Map Generators (Scripts 06a-d & 07).
