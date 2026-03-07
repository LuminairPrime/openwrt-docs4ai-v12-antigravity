# openwrt-docs4ai v12 Execution Map

## Layers and Artifacts
- **L0 (Raw Source)**: `tmp/repo-*/` (Untouched upstream clones)
- **L1 (Normalized Payload)**: `tmp/.L1-raw/{module}/` -> `openwrt-condensed-docs/.L1-raw/{module}/` (Pure `.md` files)
- **L2 (Enriched Domain)**: `tmp/.L2-semantic/{module}/` -> `openwrt-condensed-docs/.L2-semantic/{module}/` (Markdown + YAML Frontmatter)
- **L3 (Navigational Maps)**: `openwrt-condensed-docs/` (`llms.txt`, `llms-full.txt`, `AGENTS.md`, `README.md`, `index.html`, `ucode.d.ts`, `*-skeleton.md`)
- **L4 (Assembled Monoliths)**: `openwrt-condensed-docs/{module}/{module}-complete-reference.md`
- **L5 (Telemetry)**: `openwrt-condensed-docs/` (`CHANGES.md`, `changelog.json`)
- **Other Pipeline Artifacts**: `tmp/repo-manifest.json`, `tmp/cross-link-registry.json`, `signature-inventory.json` (Release artifact)

## Environment Variables
- `WORKDIR` (default `tmp`)
- `OUTDIR` (default `openwrt-condensed-docs`)
- `SKIP_WIKI` (default `false`)
- `SKIP_AI` (default `true`)
- `WIKI_MAX_PAGES` (default `300`)
- `MAX_AI_FILES` (default `40`)
- `VALIDATE_MODE` (default `hard`)
- `MERMAID_INJECT` (default `true`)
- `GITHUB_TOKEN` (default empty)
- `LOCAL_DEV_TOKEN` (default empty)
- `LLM_BUDGET_LIMIT` (default `$5.00`)
- `TOKENIZER` (default `cl100k_base`)
- `DTS_GENERATE` (default `true`)
- `BASELINE_SOURCE` (default `github-release`)

## Script Handoffs & Dependencies
- `01-clone-repos.py` -> Clones to L0 (`tmp/repo-*/`) and generates `tmp/repo-manifest.json`
- `02a`-`02h` -> Reads L0, writes to L1 (`tmp/.L1-raw/{module}/`) with `.meta.json` sidecars mapping schema fields
- `03-enrich-semantics.py` -> Reads L1 and `meta.json`, writes to L2 (`tmp/.L2-semantic/{module}/`) & generates `tmp/cross-link-registry.json`
- (Promotion Phase) -> Copies `tmp/.L1-raw` and `tmp/.L2-semantic` to `openwrt-condensed-docs/` along with `repo-manifest.json` and `cross-link-registry.json`
- `04-generate-summaries.py` (Optional) -> Mutates `openwrt-condensed-docs/.L2-semantic/` in-place
- `05-assemble-references.py` -> Reads L2, generates L3 skeletons and L4 monoliths
- `06a-generate-llms-txt.py` -> Reads L2, generates `llms.txt` and `llms-full.txt`
- `06b-generate-agents-md.py` -> Generates `AGENTS.md` and root `README.md`
- `06c-generate-ide-schemas.py` -> Generates `ucode.d.ts` strictly for ucode module
- `06d-generate-changelog.py` -> Generates L5 `CHANGES.md` and `changelog.json`
- `07-generate-index-html.py` -> Generates `index.html`, runs after 06a-06d
- `08-validate.py` -> Runs validation checks (Hard/Soft)

## Schema Requirements
- L1: `.meta.json` sidebar for extracting metadata, pure markdown, H1 title, explicit code fences.
- L2: YAML frontmatter requires `title`, `module`, `origin_type`, `token_count`, `version`. Markdown body is cross-linked.
- L3: `llms.txt` hierarchy, `.d.ts` schemas for ucode.
- L4: Monolithic `.md` matching the L2 docs, single YAML frontmatter block for the whole file.
- L5: `signature-inventory.json` from previous run diffed against current to produce `changelog.json`.

## Validation Rules
- Hard Fails: Missing `llms.txt`, 0-byte files, malformed YAML, Schema JSON validation failure, Broken/Dead relative markdown links, HTTP error leaks from wiki scraper.
- Soft Warnings: AST syntax parse errors inside L1 code blocks (`node --check`, `ucode -c`), extractor failing to extract a single file.
