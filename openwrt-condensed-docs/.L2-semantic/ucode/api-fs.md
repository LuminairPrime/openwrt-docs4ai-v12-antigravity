---
title: ucode fs module (UPDATED)
module: ucode
origin_type: c_source
token_count: 55
version: unknown
source_file: .L1-raw/ucode/api-fs.md
last_pipeline_run: '2026-03-08T10:52:48.001472+00:00'
upstream_path: lib/fs.c
language: c
ai_summary: "Mock summary for ucode fs (UPDATED). This handles atomic writes."
ai_when_to_use: "Essential for reliable ucode filesystem operations."
ai_related_topics: ["fs.readfile", "fs.writefile"]
---
# ucode fs module (UPDATED)

Exposes filesystem operations for ucode scripts. Updated for v12.

## fs.readfile(path)
Reads the entire content of a file. Fast.

## fs.writefile(path, data)
Writes data to a file. Atomic.
