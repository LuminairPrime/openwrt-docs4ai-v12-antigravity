# openwrt-docs4ai v11 — Technical Specifications & Future Roadmap

> **Author:** Claude Opus (Antigravity)
> **Date:** 2026-03-06
> **Scope:** Outlining the future "AI-Native Documentation" vision and defining the targeted features for the next v11 release pipeline.

## 1. Executive Summary

Version 10 successfully hardened the CI/CD deployment pipeline and introduced deep LLM optimizations via `*-skeleton.md` semantic maps and YAML frontmatter. With the extraction engine natively handling core C daemons (`procd`, `hotplug`, `uci`) and pipeline safeguards active, the architecture is structurally sound.

**v11** shifts the focus from *extraction reliability* to *Agentic Developer Experience (ADX)*. The goal is no longer just providing data, but structuring it so autonomous Agents (like Cursor, Claude Desktop, and CLI tools) can instantly grok the repository context, chunk relationships recursively using GraphRAG logic, and navigate the API effortlessly.

---

## 2. Core v11 Objectives

### 2.1 The "Agentic Web" Standards (`AGENTS.md` & `llms-full.txt`)
- **`AGENTS.md` Implementation:** Automatically synthesize a project-root `AGENTS.md` file designed to instruct local AI tools on how to interact with the repository, including build commands, testing protocols, and documentation taxonomy.
- **Dual-Faceted Indexing:** Formalize the `llms.txt` web specification. Restructure the root `/llms.txt` into a clean, hierarchical "Decision Tree" (What should I read first?) and move the bulk aggregation paths into `/llms-full.txt` for zero-config ingest by external AI aggregation platforms (e.g., Mintlify, Docling).

### 2.2 Token-Budget Annotations
- **Size/Token Counters in the Index:** Inject token-budget hints directly into the `llms.txt` manifests (e.g., `- [ucode-module-fs.md] (~4.2K words, 12 functions)`). This allows downstream Agent frameworks to prioritize or skip fetching heavy documents before exceeding their context windows. 

### 2.3 Visual & Architectural Generics (Mermaid.js)
- **Automated Sequence Diagrams:** OpenWrt heavily relies on asynchronous message buses (ubus). We will enhance the documentation assembly step to inject generic ````mermaid` sequence diagrams into the headers of event-driven modules, giving LLMs spatial awareness of the system events.

### 2.4 CI/CD Optimization & Cost Reduction
- **Incremental Wiki Scraping (`If-Modified-Since`):** Modify `02a-scrape-wiki.py` to cache ETag / Last-Modified headers locally. Only re-fetch and convert wiki pages that have actively changed since the last run.
- **Push Trigger Refactoring:** Reduce pipeline spam by restricting the `on: push` trigger to paths that directly modify scraper scripts (`.github/scripts/**`), relying primarily on the monthly cron schedule. 

---

## 3. Advanced / Aspirational Concepts (v12+)

The following ideas represent the bleeding edge of AI documentation theory and are tracked for future integration:

### 3.1 GraphRAG Knowledge Map Extraction
Flat `llms.txt` files are great for standard context windows, but modern semantic reasoning thrives on node-edge relationships. Future pipelines could output an `openwrt-knowledge-graph.jsonl` linking dependencies: `(luci-app-firewall) -[REQUIRES]-> (uci)`.

### 3.2 Pre-Packaged AI Prompt Snippets
Dynamically injecting prompt templates at the bottom of major reference files (`> **AI Prompt Snippet:** "I want to script a ubus listener using... "`) to drastically lower the human cognitive load.

### 3.3 Semantic AST-Based "Breaking Changes" Engine
Instead of standard git-diffing for `CHANGES.md`, utilizing Abstract Syntax Tree (AST) parsing to automatically alert developers: `> [!WARNING] The signature for fs.popen() changed; 'mode' is now required.`

### 3.4 Automated Code-Snippet Validation
Executing `ucode -c` or node linters on the code blocks embedded within the scraped documentation as part of the validation gate, ensuring the LLMs never ingest hallucinated or broken upstream examples.

---

## 4. Proposed v11 Implementation Plan

1. **Phase 1: CI Optimizations**
   - Update `00-pipeline.yml` to restrict push triggers.
   - Inject the HTTP caching logic into `02a-scrape-wiki.py`.

2. **Phase 2: Index Metaprogramming**
   - Refactor `06-generate-index.py` to output both `llms.txt` and `llms-full.txt`.
   - Update metadata collection hooks to record word/line count logic natively into the manifest map during iteration.

3. **Phase 3: Agent Tooling**
   - Add a new workflow phase to synthesize and dump `AGENTS.md`.

*This spec serves as the foundational design block for the next sprint.*
