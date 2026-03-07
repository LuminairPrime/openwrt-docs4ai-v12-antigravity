"""
openwrt-docs4ai-03-add-links.py

Purpose  : Inject cross-reference links between documentation files and flag
           deprecated symbols found in API docs when referenced by wiki pages.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs) — where generated docs live
Outputs  : Mutates .md files in $OUTDIR (adds hyperlinks for known symbols)
Deps     : None (pure Python)
Notes    : Two-pass process:
           1. Build a symbol index from ## headings in all .md files
           2. Inject [symbol](target) links where symbols appear in other files
           API symbols (ucode/luci) take priority over wiki symbols.
           Deprecated symbols get warning callouts injected into wiki pages.
"""

import os
import re
import glob

OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))

print("[03] Cross-reference injection (code-like symbols only)")

all_md = (
    sorted(glob.glob(os.path.join(OUTDIR, "ucode-docs", "*.md"))) +
    sorted(glob.glob(os.path.join(OUTDIR, "luci-docs", "*.md"))) +
    sorted(glob.glob(os.path.join(OUTDIR, "openwrt-wiki-docs", "*.md"))) +
    sorted(glob.glob(os.path.join(OUTDIR, "openwrt-buildroot-docs", "*.md")))
)

print(f"[03] Building symbol index from {len(all_md)} markdown files...")

# Common words that should not be treated as code symbols
COMMON_WORDS = {
    "name", "type", "value", "event", "data", "code", "info", "list",
    "item", "node", "text", "form", "page", "time", "date", "user",
    "host", "port", "path", "file", "mode", "status", "error", "result",
    "state", "flags", "index", "count", "length", "size", "version",
    "base", "init", "load", "open", "read", "write", "close", "send",
    "recv", "bind", "call", "stop", "start", "reset", "clear", "check",
    "parse", "fetch", "apply", "remove", "create", "update", "delete",
    "source", "target", "output", "input", "params", "options", "config",
    "return", "object", "string", "number", "boolean", "array", "table",
    "class", "method", "property", "function", "callback", "promise",
}

def is_code_symbol(name):
    """Heuristic: is this heading text a code-like API symbol?"""
    if name.lower() in COMMON_WORDS:
        return False
    if len(name) < 5:
        return False
    # camelCase
    if re.match(r'^[a-z][a-zA-Z0-9]+$', name) and any(c.isupper() for c in name):
        return True
    # dotted name (e.g., LuCI.network)
    if "." in name and len(name) >= 6:
        return True
    # snake_case
    if "_" in name and len(name) >= 7:
        return True
    # ALL_CAPS abbreviation
    if re.match(r'^[A-Z]{3,6}$', name):
        return True
    return False

# --- Pass 1: Build symbol index ---
symbol_index = {}

for fpath in all_md:
    root_url = "/" + os.path.relpath(fpath, OUTDIR).replace(os.sep, "/")
    try:
        content = open(fpath, encoding="utf-8").read()
    except Exception:
        continue

    for m in re.finditer(
        r'^#{2,4}\s+[`"]?([A-Za-z][A-Za-z0-9_.]+(?:\(\))?)[`"]?',
        content, re.MULTILINE
    ):
        symbol = m.group(1).rstrip("()")
        if not is_code_symbol(symbol):
            continue

        if symbol not in symbol_index:
            symbol_index[symbol] = root_url
        else:
            current      = symbol_index[symbol]
            this_is_api  = "ucode-docs" in fpath or "luci-docs" in fpath
            curr_is_wiki = "wiki" in current or "buildroot" in current
            curr_is_api  = "ucode-docs" in current or "luci-docs" in current
            # API docs take priority over wiki/buildroot
            if this_is_api and curr_is_wiki:
                symbol_index[symbol] = root_url

print(f"[03] Symbol index: {len(symbol_index)} code-like symbols")

# --- Pass 2: Inject cross-references ---
total_injected = 0
files_modified = 0

for fpath in all_md:
    this_root_url = "/" + os.path.relpath(fpath, OUTDIR).replace(os.sep, "/")
    try:
        original = open(fpath, encoding="utf-8").read()
    except Exception:
        continue

    # Build set of character positions that are inside code/links (protected zones)
    protected = set()
    for fence in re.finditer(r'```.*?```|~~~.*?~~~', original, re.DOTALL):
        protected.update(range(fence.start(), fence.end()))
    for code in re.finditer(r'`[^`\n]+`', original):
        protected.update(range(code.start(), code.end()))
    for link in re.finditer(r'\[[^\]]+\]\([^)]+\)', original):
        protected.update(range(link.start(), link.end()))

    spans = []

    def overlaps_existing(s, e):
        for es, ee, _ in spans:
            if not (e <= es or s >= ee):
                return True
        return False

    # Match longer symbols first to avoid partial matches
    for symbol, target_url in sorted(symbol_index.items(), key=lambda x: -len(x[0])):
        if target_url == this_root_url:
            continue
        pat = re.compile(rf'\b{re.escape(symbol)}\b(?!\()')
        for m in pat.finditer(original):
            s, e = m.start(), m.end()
            if any(i in protected for i in range(s, e)):
                continue
            if overlaps_existing(s, e):
                continue
            spans.append((s, e, f"[{symbol}]({target_url})"))

    if not spans:
        continue

    spans.sort(key=lambda x: x[0])
    out  = []
    last = 0
    for s, e, rep in spans:
        out.append(original[last:s])
        out.append(rep)
        last = e
    out.append(original[last:])
    modified = "".join(out)

    with open(fpath, "w", encoding="utf-8", newline="\n") as f:
        f.write(modified)
    files_modified += 1
    total_injected += len(spans)

print(f"[03] Cross-references: {total_injected} injected across {files_modified} files.")

# --- Pass 3: Deprecation checker ---
print("[03] Deprecation checker...")

deprecated = {}
for fpath in sorted(
    glob.glob(os.path.join(OUTDIR, "ucode-docs", "*.md")) +
    glob.glob(os.path.join(OUTDIR, "luci-docs", "*.md"))
):
    root_url = "/" + os.path.relpath(fpath, OUTDIR).replace(os.sep, "/")
    try:
        content = open(fpath, encoding="utf-8").read()
    except Exception:
        continue
    for m in re.finditer(
        r'^(#{2,4})\s+[`"]?([A-Za-z][A-Za-z0-9_.]+)[`"]?',
        content, re.MULTILINE
    ):
        symbol = m.group(2).rstrip("()")
        window = content[m.end():m.end() + 1500]
        if re.search(r'\*\*Deprecated\*\*', window, re.IGNORECASE):
            deprecated[symbol] = root_url
            print(f"[03] Deprecated: {symbol} (in {os.path.basename(fpath)})")

if not deprecated:
    print("[03] No deprecated symbols found in API docs.")
else:
    print(f"[03] Found {len(deprecated)} deprecated symbols.")

injected = 0
for fpath in sorted(glob.glob(os.path.join(OUTDIR, "openwrt-wiki-docs", "*.md"))):
    try:
        content = open(fpath, encoding="utf-8").read()
    except Exception:
        continue

    warnings = [
        (sym, url) for sym, url in deprecated.items()
        if re.search(rf'\b{re.escape(sym)}\b', content)
    ]
    if not warnings:
        continue

    callout = ["> [!WARNING]"]
    for sym, url in warnings:
        callout.append(
            f"> This page references `{sym}`, which is marked as "
            f"**deprecated** in the official API documentation. "
            f"See [{sym}]({url}) for the current approach."
        )
    callout_text = "\n".join(callout) + "\n\n"

    pos = content.find("\n\n---\n\n")
    if pos != -1:
        pos += len("\n\n---\n\n")
        content = content[:pos] + callout_text + content[pos:]
    else:
        pos = content.find("\n\n")
        if pos != -1:
            content = content[:pos + 2] + callout_text + content[pos + 2:]

    with open(fpath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    injected += 1

print(f"[03] Deprecation warnings: {injected} wiki pages flagged.")
print("[03] Complete.")
