# openwrt-docs4ai

> OpenWrt developer documentation, condensed and optimized for AI LLMs and humans.

[![Pipeline](https://github.com/LuminairPrime/openwrt-docs4ai/actions/workflows/openwrt-docs4ai-00-pipeline.yml/badge.svg)](https://github.com/LuminairPrime/openwrt-docs4ai/actions)

## What This Is

A monthly automated pipeline that scrapes OpenWrt project documentation from 5 upstream sources and condenses it into compact, LLM-ready markdown files. Two consumption modes:

1. **Complete references** — single files containing all docs per source (feed directly to an LLM)
2. **Individual files** — per-module, per-page markdown files (for targeted lookups)

## Using the Documentation

**Entry point:** [`openwrt-condensed-docs/llms.txt`](openwrt-condensed-docs/llms.txt)

| File | What It Contains | Skeleton Version Included? |
|------|-----------------|------------------------|
| `ucode-complete-reference.md` | ucode scripting language — all modules and tutorials | ⚡ `ucode-skeleton.md` (Headers & Signatures only) |
| `luci-jsapi-complete-reference.md` | LuCI web interface JavaScript API | ⚡ `luci-jsapi-skeleton.md` |
| `openwrt-wiki-complete-reference.md` | OpenWrt developer wiki (techref + guide-developer) | ⚡ `openwrt-wiki-skeleton.md` |
| `openwrt-buildroot-complete-reference.md` | Package metadata from the buildroot source tree | ⚡ `openwrt-buildroot-skeleton.md` |
| `openwrt-examples-complete-reference.md` | Curated LuCI application source code examples | ⚡ *(Inapplicable)* |

For targeted lookups, browse the subdirectories in [`openwrt-condensed-docs/`](openwrt-condensed-docs/). Every markdown file now contains YAML Frontmatter for LLM indexing accuracy.

For targeted lookups, browse the subdirectories in [`openwrt-condensed-docs/`](openwrt-condensed-docs/).

## Data Sources

| Source | Upstream | Method |
|--------|----------|--------|
| Wiki | [openwrt.org/docs/](https://openwrt.org/docs/) | DokuWiki namespace crawl + pandoc |
| ucode | [jow-/ucode](https://github.com/jow-/ucode) | jsdoc2md from source |
| LuCI JS API | [openwrt/luci](https://github.com/openwrt/luci) | jsdoc2md from source |
| Buildroot pkgs | [openwrt/openwrt](https://github.com/openwrt/openwrt) | Makefile parsing |
| Examples | [openwrt/luci](https://github.com/openwrt/luci) | Curated file copy |
| Procd API | [openwrt/openwrt](https://github.com/openwrt/openwrt) | C-comment Regex Regex Parser (`procd.sh`) |
| Hotplug | [openwrt/openwrt](https://github.com/openwrt/openwrt) | Source scanning (`hotplug-events`) |

## How It Works

Scripts in `.github/scripts/` run via GitHub Actions on the 1st of each month:

1. **Clone** upstream repos (shallow, sparse where possible)
2. **Scrape** all sources in parallel
3. **Enrich** with cross-references and optional AI summaries
4. **Assemble** complete reference files
5. **Validate** — staging gate checks file integrity before promotion
6. **Promote** — only validated output is committed to the repo

See [DEVELOPMENT.md](DEVELOPMENT.md) for technical details and local development setup.

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details. The generated documentation content is derived from upstream OpenWrt project sources and retains their respective licenses.
