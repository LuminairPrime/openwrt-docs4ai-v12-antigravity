# openwrt-docs4ai: Schema Definitions and Data Topology (v12)

> **Date:** 2026-03-07
> **Scope:** This document establishes the authoritative data dictionary and schema contract for the documentation supply chain. It dictates the exact structural boundaries, data formats, and constraint rules for the six discrete documentation states (L0-L5) to ensure deterministic interoperability across downstream AI, IDE, and indexing consumers.

---

## 1. Top-Level Directory and Versioning Strategy

To eliminate clutter and inconsistent output states, all generated documentation will strictly abide by a layered output convention. The system implements a **staging-then-promote** architecture using two primary environment variables:

- **`WORKDIR` (Default: `./tmp`)**: Ephemeral working area for cloned repos (L0), intermediate build artifacts (L1, L2), and cross-link registries. Never committed.
- **`OUTDIR` (Default: `./openwrt-condensed-docs`)**: Destination for all publishable documentation artifacts (L3, L4, L5).

**In CI**, `WORKDIR` is `$RUNNER_TEMP/work` and `OUTDIR` is `$RUNNER_TEMP/staging`. After validation passes, `OUTDIR` is promoted to the committed workspace. **In local development**, `OUTDIR` points directly to the workspace for immediate inspection.

### 1.1 The Stakeholders & Layer Mapping
No single output satisfies all consumers. We map stakeholders to specific layers:

| Stakeholder | Persona | Target Layer | Output Format |
|:---|:---|:---:|:---|
| **Raw Analyst** | Build custom tools from pure content | **L1, L2** | `.md` with/without YAML |
| **Context Injector** | RAG systems / Vector DBs | **L2** | Atomic `.md` + YAML |
| **Omniscient Architect** | Frontier LLMs (Huge Context) | **L4** | Monolithic `.md` |
| **Agile Developer** | Human needing quick lookups | **L3, L4** | Web / Markdown |
| **IDE Plugin** | LSP autocomplete engines | **L3** | `.d.ts` schemas |
| **Security Linter** | CI/CD tracking API changes | **L5** | `changelog.json` |

---

## 2. The L0 → L5 Documentation Layers (With Explicit Schemas)

The pipeline guarantees that by the time data cascades to the next layer, it complies absolutely with that layer's rigid formatting schema.

### Layer 0 (L0): The Raw Source
*   **Format:** Untouched Upstream (Git repositories, raw HTML responses, `Makefile`, `.c`, `.uc`)
*   **Directory:** `tmp/repo-*/`
*   **Attributes:** Zero consistency. Not published. Exists only ephemerally during the pipeline run.

---

### Layer 1 (L1): The Normalized Payload (The Extracts)
*   **Format:** Standardized Markdown (`.md`).
*   **Directory:** Generated in `$WORKDIR/L1-raw/{module_name}/`, then archived to `$OUTDIR/L1-raw/`.
*   **Naming Rule:** `{origin_type}-{slug}.md` (e.g., `api-fs-module.md` or `config-network.md`).
*   **Schema Rule:** Pure informational content stripped of source-domain noise. No YAML frontmatter. No cross-links. 
*   **Size Thresholds:** L1 files exceeding 50,000 tokens should trigger a soft warning during validation. Files exceeding 100,000 tokens should be flagged for manual review or algorithm splitting.
*   **Mandatory Rule (Code Wrapping):** If the source is raw code (e.g., LuCI JavaScript examples), it MUST be wrapped in a Markdown code block structure with the filename as a heading.

**Explicit Schema Example A (L1 - `.meta.json` Sidecar):**
```json
{
  "extractor": "02b",
  "origin_type": "c_source",
  "module": "ucode",
  "slug": "api-fs-module",
  "upstream_path": "lib/fs.c",
  "original_url": null,
  "language": "c",
  "content_hash": "a1b2c3d4",
  "fetch_status": "success",
  "extraction_timestamp": "2026-03-07T12:00:00Z"
}
```
*(Note: `original_url` is populated only by the wiki scraper `02a`)*

**Explicit Schema Example B (L1 - Prose Extraction):**
```markdown
# ucode fs module
The `fs` module provides file system operations. It is a core feature of the ucode virtual machine.
```

**Explicit Schema Example C (L1 - Raw Code Wrapping):**
````markdown
# luci-app-example.js
```javascript
'use strict';
return L.Class.extend({
    // Raw code goes here exactly as fetched from the upstream repo
    render: function() { return E('div', 'Hello World'); }
});
```
````

---

### Layer 2 (L2): The Enriched Domain (The Semantic Mesh)
*   **Format:** Markdown with rigid YAML Frontmatter (`.md`). Intermediate JSON (`cross-link-registry.json`).
*   **Directory:** Generated in `$WORKDIR/L2-semantic/{module_name}/`, then archived to `$OUTDIR/L2-semantic/`.
*   **Schema Rule:** Every file, regardless of L0 origin, contains an identical baseline YAML metadata block (with explicit optional AI extension fields appended conditionally later). Cross-references are injected mathematically as relative Markdown links.
*   **Cross-Link Safety:** The linker MUST only link fully-qualified symbols (e.g., `fs.open()`), never bare words. The linker MUST NEVER inject links inside fenced code blocks or inline \`code spans\`.

**The `origin_type` Enum:**
Valid values: `c_source`, `js_source`, `wiki_page`, `makefile_meta`, `readme`, `uci_schema`, `hotplug_event`, `example_app`, `header_api`.

**Explicit Schema Example (L2 - Semantic File):**
```markdown
---
title: "ucode fs module"              # REQUIRED
module: "ucode"                       # REQUIRED
origin_type: "c_source"               # REQUIRED (from Enum)
token_count: 840                      # REQUIRED
version: "e87be9d"                    # REQUIRED
source_file: "L1-raw/ucode/api-fs-module.md" # RECOMMENDED (pipeline L1 traceability)
upstream_path: "lib/fs.c"             # RECOMMENDED (raw analyst original code)
language: "c"                         # RECOMMENDED (for .d.ts gen)
ai_summary: "Native filesystem access module for ucode. Implements robust, low-level POSIX-style operations including atomic file writes, directory traversal, file stat, and symbolic link management." # PROFESSIONAL REQUIREMENT
ai_when_to_use: "Use for all ucode-based filesystem interactions on OpenWrt, especially when atomicity or precise permission control is required."
ai_related_topics: ["fs.readfile", "fs.writefile", "fs.stat"]
description: "File system operations" # Fallback for legacy indexing
last_pipeline_run: "2026-03-07T12:00:00Z" # RECOMMENDED (freshness indicator)
---
# ucode fs module
The `fs` module provides file system operations. See also [uloop.timer()](../uloop/api-uloop-module.md).
```

**Explicit Schema Example (L2 - `cross-link-registry.json`):**
```json
{
  "pipeline_date": "2026-03-07T12:00:00Z",
  "symbols": {
    "fs.open": { 
      "signature": "fs.open(path, flags)", 
      "file": "L1-raw/ucode/api-fs-module.md", 
      "returns": "number",
      "parameters": [
        {"name": "path", "type": "string"},
        {"name": "flags", "type": "string"}
      ],
      "relative_target": "../ucode/api-fs-module.md"
    }
  }
}
```

---

### Layer 3 (L3): Navigational Maps & Operational Indexes
*   **Format:** `llms.txt`, `llms-full.txt`, `*-skeleton.md`, `.d.ts`, `AGENTS.md`, `README.md`, `index.html`
*   **Directory:** `$OUTDIR/` (Root level) and `$OUTDIR/{module_name}/`
*   **Schema Rule:** Procedurally generated from L2 metadata, cross-link registries, and static policy configurations (e.g. `lib/constants.py`).

**Explicit Schema Example A1 (L3 - Root `llms.txt` Decision Tree):**
```markdown
# openwrt-docs4ai - LLM Routing Index
> For a flat file listing, see [llms-full.txt](./llms-full.txt)

> **Version:** openwrt/openwrt@abcdef1
> **Total Context Available:** ~45k tokens

## Core Daemons
- [procd](./procd/llms.txt): init system daemon (~1.2k tokens)
- [uci](./uci/llms.txt): universal configuration interface (~3.4k tokens)

## Complete Aggregation
If your context window permits, you may fetch the flat URL index:
- [llms-full.txt](./llms-full.txt)
```

**Explicit Schema Example A2 (L3 - `llms-full.txt` Flat Catalog):**
```markdown
# openwrt-docs4ai - Complete Flat Catalog
> **Total Context:** ~45k tokens

- [procd/api-init-module.md](./procd/api-init-module.md) (1.2k tokens) - init system daemon
- [uci/api-config-module.md](./uci/api-config-module.md) (3.4k tokens) - universal configuration interface
```

**Explicit Schema Example A3 (L3 - Module-Level `llms.txt` Index):**
```markdown
# procd module
> **Total Context:** ~1.2k tokens

- [api-init-module.md](./api-init-module.md) (800 tokens) - init system daemon
- [api-service-module.md](./api-service-module.md) (400 tokens) - service management
```

**Explicit Schema Example A3 (L3 - `AGENTS.md` Instructions):**
```markdown
# AGENTS.md — AI Agent Instructions for openwrt-docs4ai
## Repository Structure
- `llms.txt` — Start here. Hierarchical index linking to each target subsystem.
- `llms-full.txt` — Flat listing of every document with token counts.
- `[module]/*-complete-reference.md` — Monolithic L4 file best ingested if context size permits.
- `[module]/*-skeleton.md` — Structural API outlines serving as navigational aids.
- `[module]/*.d.ts` — TypeScript definitions for IDEs and static analysis.
## Conventions
- All token counts use `cl100k_base` encoding.
- Cross-references use relative Markdown links.
## MUST NOT
- DO NOT blindly scrape the wiki. Use these documents instead.
- DO NOT hallucinate APIs outside of what is defined in the `*-skeleton.md` indexes.
```

**Explicit Schema Example B (L3 - `*-skeleton.md` Structural Map):**
```markdown
# ucode fs module (Skeleton)
## Functions
- `fs.open(path, flags)` : returns file descriptor
- `fs.read(fd, len)`     : returns string
```

**Explicit Schema Example C (L3 - IDE Schema `.d.ts`):**
- **Parameter Parsing Rule:** When extracting signatures from Markdown headers, the generator MUST use a **balanced-bracket counter** to split parameters by commas. This ensures that default values containing nested commas (e.g., `[1, 2]` or `{a: 1}`) do not cause malformed TypeScript declarations.
```typescript
/** 
 * AUTOGENERATED VIA openwrt-docs4ai
 * Target: Language Server Protocol (LSP) IDE Autocomplete 
 */
declare module "fs" {
    /** Opens a file descriptor for the given path. */
    export function open(path: any, flags: any);
}
```

**Explicit Schema Example D (L3 - Web Landing `index.html`):**
```html
<!DOCTYPE html>
<html>
<head><title>openwrt-docs4ai Navigation</title></head>
<body>
    <h1>openwrt-docs4ai API Documentation</h1>
    <p>Select a view format below:</p>
    <ul>
        <li><a href="llms.txt">AI Index (llms.txt)</a></li>
        <li><a href="ucode/ucode-complete-reference.md">ucode L4 Monolith</a></li>
    </ul>
</body>
</html>
```

**Explicit Schema Example E (Category D - Self-Documenting `README.md`):**
```markdown
# openwrt-docs4ai Generated Pipeline Output
**Pipeline Run Date:** 2026-03-07T12:00:00Z
**Baseline Version:** abcd123

This repository branch contains the automatically generated, stable L3, L4, and L5 layers.
To ingest this repository into an LLM context, begin at `llms.txt`.
```

---

### Layer 4 (L4): The Assembled Monoliths
*   **Format:** Massive Markdown (`.md`)
*   **Directory:** `$OUTDIR/{module_name}/`
*   **Schema Rule:** A concatenation of L2 Markdown bodies. Internal L2 YAML is stripped and replaced with a single unified L4 monolith YAML block.

**Explicit Schema Example (L4 - Monolithic Context):**
```markdown
---
module: "ucode"
total_token_count: 1460
section_count: 2
---
# ucode Complete Reference

## Table of Contents
1. [ucode fs module](#ucode-fs-module) (840 tokens)
2. [ucode uloop module](#ucode-uloop-module) (620 tokens)

## ucode fs module
The `fs` module provides file system operations.

## ucode uloop module
The `uloop` module provides the event loop implementation.
```

---

### Layer 5 (L5): Telemetry & Differential Flow
*   **Format:** `.md` (Human readable diff), `.json` (Machine readable diff)
*   **Directory:** `$OUTDIR/` (Root level)
*   **Schema Rule:** Standardized audit trails tracking API changes between pipeline runs.
*   **Baseline Retrieval:** The prior run's `signature-inventory.json` is fetched from the latest GitHub Release. If missing (first run), tracking defaults to "no baseline" mode.

**Explicit Schema Example A (L5 - `CHANGES.md`):**
```markdown
# API Drift Report (2026-03-07)
## ucode module
- [REMOVED] `fs.deprecated_function()`
- [ADDED] `fs.new_feature(param)`
```

**Explicit Schema Example B (L5 - `changelog.json`):**
```json
{
  "pipeline_date": "2026-03-07T12:00:00Z",
  "commit_hash": "e87be9d",
  "changes": {
    "ucode": {
      "dropped_signatures": ["fs.deprecated_function()"],
      "added_signatures": ["fs.new_feature(param)"]
    }
  }
}
```

**Explicit Schema Example C (L5 - `signature-inventory.json`):**
```json
{
  "pipeline_date": "2026-03-07T12:00:00Z",
  "modules": {
    "ucode": {
      "fs.open": { "signature": "fs.open(path, flags)", "returns": "number", "file": "L1-raw/ucode/api-fs-module.md" },
      "fs.read": { "signature": "fs.read(fd, len)", "returns": "string", "file": "L1-raw/ucode/api-fs-module.md" }
    }
  }
}
```

---

## 3. Pipeline Script Mapping (The "Algorithm Upgrade Plan")

| Script | Assigned Function | Output Layer | Data Mutation |
| :--- | :--- | :--- | :--- |
| `01-clone-repos.py` | Source Fetcher | **L0** | Remote Server to Local Disk |
| `02*-scrape-*.py` | Domain Normalizers | **L1** | HTML/Code Block to Pure `.md` |
| `03-normalize-semantic.py` | Semantic Enricher | **L2** | `L1 + YAML Frontmatter + Markdown Links` |
| `04-generate-ai-summaries.py` | AI Enricher (Opt) | **L2 (Meta)** | Augments L2 YAML with AI metadata |
| `05-assemble-references.py`| The Aggregator | **L3, L4** | `L2` Concatenation → Monoliths (`L4`) & Skeletons (`L3`) |
| `06a-generate-llms-txt.py` | Routing Indexes | **L3** | `L2 Metadata` → `llms.txt` / `llms-full.txt` |
| `06b-generate-agents-md.py` | Routing Indexes | **L3** | Generates `AGENTS.md` & `README.md` |
| `06c-generate-ide-schemas.py`| IDE Definition | **L3** | Extracts signatures → `.d.ts` schemas |
| `06d-generate-changelog.py` | Telemetry Builder | **L5** | Generates `CHANGES.md` and `changelog.json` |
| `07-generate-index-html.py` | HTML Landing | **L3** | Combines L3 maps into `index.html` |
| `08-validate.py` | Quality Gate | **N/A** | Hard fails on invalid schemas |

*Note: Alphabetical suffixes (e.g., `06a`, `06b`) denote tasks that execute in strict parallel. Because `07` mathematically consumes the output of `06a` (`llms.txt`), it increments to the next integer to signify a sequential stage barrier. `08` runs last to validate the final output.*

---

## 4. Archiving & Artifact Release Strategy

1.  **GitHub Releases (ZIP files):**
    *   `openwrt-docs4ai-L1-raw.zip` (Contents of `L1-raw/`)
    *   `openwrt-docs4ai-L2-semantic.zip` (Contents of `L2-semantic/`)
    *   `signature-inventory.json` (Baseline for the next pipeline run)
2.  **GitHub Pages (Live Hosting):**
    *   Deploys only **L3**, **L4**, and **L5**. (The navigational maps, the monoliths, and the changes).
    *   Must include `.nojekyll` in the root output to disable Jekyll filtering of hidden folders and YAML frontmatter.
    *   The `index.html` file provides human navigation to these specific layers.
