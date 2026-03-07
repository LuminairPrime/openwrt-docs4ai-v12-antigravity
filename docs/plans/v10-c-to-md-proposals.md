# Future Refactor: C-to-Markdown Tooling Proposals

This document explores native C/C++ documentation generator alternatives to replace the `jsdoc2md` (with `c-transpiler` plugin) workaround currently used to parse `ucode` C API files. The current `jsdoc2md` pipeline suffers from aggressive recursive directory scanning bugs that require Python temporary directory isolation to function correctly. 

If this workaround becomes unmaintainable, one of the following native tools should be adopted.

---

## 1. Tool Analysis & Tier List

We collated GitHub activity, Reddit community consensus, and "LLM / AI" readiness to rank the available tools.

### 🏆 S-Tier (Best Native Fit): **Doxide**
- **GitHub**: 123 stars | Latest release: v0.9.0 (Jan 21, 2025)
- **Reddit Consensus**: Highly praised in recent C++ discussions as an excellent, modern, responsive alternative to Doxygen. Noted for its clean YAML configuration and speed (powered by Tree-sitter).
- **AI/LLM Readiness**: **High**. Outputs incredibly clean, native Markdown. While not explicitly marketed as "AI-first", the unpolluted Markdown it generates from C code is exactly what LLM context windows require. 
- **Verdict**: The smartest drop-in replacement for producing standard markdown.

### 🥈 A-Tier (Industry Standard): **Doxygen + Doxybook2**
- **GitHub (Doxybook2)**: 189 stars | Latest release: Oct 2022
- **Reddit Consensus**: Doxygen is the undisputed industry standard for parsing C. Reddit developers frequently mention piping Doxygen XML into static site generators.
- **AI/LLM Readiness**: **High**. Doxygen recently implemented `MARKDOWN_SUPPORT = YES`. Several "LLM-Connector" open-source repositories explicitly utilize Doxygen XML-to-Markdown bridges to ingest C codebases into RAG (Retrieval-Augmented Generation) databases.
- **Verdict**: Bulletproof C parsing, but requires a heavier two-step toolchain.

### 🥉 C-Tier (Niche Utilities): **mdcdoc**
- **GitHub**: 4 stars | Active
- **Verdict**: Too small and untested for a critical pipeline, despite doing exactly what we need (stripping `/** ... */` from C code into Markdown).

### ❌ F-Tier (Dead / Format Mismatch): **Standardese** and **m.css**
- **Standardese (967 stars)**: Heavily discussed on Reddit 5 years ago as the "next-gen Doxygen", but was officially abandoned by its author in 2019. 
- **m.css (428 stars)**: Excellent C++ tool, but generates HTML themes, not pure raw Markdown, rendering it useless for LLM ingestion.

---

## 2. Refactor Upgrade Proposals

If we decide to strip `jsdoc2md` out of the pipeline, here are the two core approaches to doing so:

### Proposal A: Migrate to Doxide (Modern, Single-Step)
**How it works:**
We replace the `jsdoc2md` NPM dependency with `doxide`. In `02b-scrape-ucode.py`, we dynamically generate a minimal `doxide.yaml` configuring the `ucode` source folder, execute `doxide build`, and natively harvest the Markdown files.
- **Pros:** Fast, modern, single tool dependency. Excellent markdown syntax output. Naturally designed to read `#define` and C macros cleanly.
- **Cons:** It is a compiled C++ tool, requiring either pre-compiled binaries in the GitHub Actions runner, or installing it via `apt-get`/`brew`, which increases pipeline environment setup time.

### Proposal B: Migrate to Doxygen + Doxybook2 (Robust, Two-Step)
**How it works:**
We install `doxygen` and the `doxybook2` binary on the GitHub Actions runner. `02b-scrape-ucode.py` executes `doxygen Doxyfile` to dump the `ucode` API into XML files. A subsequent `subprocess.run` calls `doxybook2 --input xml/ --output ucode-docs/` to batch convert the XML into Markdown.
- **Pros:** Zero risk of parsing failures. Doxygen has perfectly parsed archaic and modern C syntax for 25 years.
- **Cons:** Extremely heavy. Will require heavy Python post-processing (Regex/BeautifulSoup) to trim the verbose Doxygen/Doxybook2 output templates down to the lean, dense "LLM-optimized" constraint.

---

## 3. Compare & Contrast: Upgrading vs. The Existing Workaround

**The Existing Workaround State:**
We currently run `npx jsdoc2md` over C files by copying each target C file into an isolated Python temporary directory. This tricks JSDoc into skipping its broken recursive directory-scanning logic.

| Metric | Proposal A (Doxide) | Proposal B (Doxygen) | Status Quo (JSDoc Workaround) |
| :--- | :--- | :--- | :--- |
| **Parsing Reliability** | High (Tree-sitter) | Absolute (Doxygen) | Fragile JS-Regex Hack |
| **Pipeline Speed** | Fast (< 1s) | Medium (~3s) | Fast enough (~1s total) |
| **CI Dependencies** | Requires installing binaries | Requires installing binaries | `npm install` (Already cached) |
| **Output Token Density** | Good (Clean MD) | Poor (Requires heavy templating) | Excellent (Stripped, focused API lists) |
| **Developer Cost** | High (Script rewrite) | Very High (Script + Template rewrite) | Zero (Already implemented) |

### Final Recommendation
**Leave the existing `jsdoc2md` workaround in place indefinitely.** 

While isolating JS binaries inside Python temporary folders is architecturally bizarre, the *output* it produces is practically perfect for LLM usage: low-token, highly specialized API extraction. Moving to Doxide or Doxygen requires introducing OS-compiled binaries to the CI workflow, and rewriting HTML/Markdown stripping regex logic from scratch.

**Trigger for Refactor:**
The only reason to execute Proposal A (Doxide) is if an upstream update to the `ucode` repository introduces a massive new syntax layout that the Javascript `c-transpiler` plugin completely fails to parse, causing `jsdoc2md` to throw fatal syntax errors. Until that day, the temp-dir workaround is stable, functional, and free.
