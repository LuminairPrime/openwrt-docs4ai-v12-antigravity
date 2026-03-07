# Contributing to openwrt-docs4ai

To add a new scraper:
1. Create `02x-scrape-[name].py`.
2. Ensure it writes pure markdown to `$WORKDIR/.L1-raw/[module]/`.
3. Provide a `.meta.json` sidecar alongside the markdown file with keys like `original_source`, `extractor`, `extraction_timestamp`.
4. Ensure no YAML is injected directly into the markdown.
5. All C/JS output must use markdown fences.
