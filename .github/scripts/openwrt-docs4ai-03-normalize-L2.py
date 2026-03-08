"""
Purpose: Two-pass L2 Normalization Engine (Schema Injection, Linking, Mermaid).
Phase: Normalization
Layers: L1 -> L2
Inputs: tmp/.L1-raw/
Outputs: tmp/.L2-semantic/ and tmp/cross-link-registry.json
Environment Variables: WORKDIR, OPENWRT_COMMIT, LUCI_COMMIT, UCODE_COMMIT
Dependencies: tiktoken, lib.config
Notes: Pass 1 calculates tiktoken, builds registry & injects YAML. Pass 2 cross-links.
"""

import os
import re
import json
import glob
import datetime
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib import config

sys.stdout.reconfigure(line_buffering=True)

try:
    import tiktoken
    encoder = tiktoken.get_encoding("cl100k_base")
    def count_tokens(text):
        return len(encoder.encode(text))
except ImportError:
    print("[03] WARN: tiktoken missing, falling back to word count * 1.3")
    def count_tokens(text):
        return int(len(text.split()) * 1.3)

print("[03] L2 Normalization Engine")

WORKDIR = config.WORKDIR
L1_DIR = config.L1_RAW_WORKDIR
L2_DIR = config.L2_SEMANTIC_WORKDIR

if not os.path.isdir(L1_DIR):
    print(f"[03] FAIL: L1 input directory not found: {L1_DIR}")
    sys.exit(1)

os.makedirs(L2_DIR, exist_ok=True)

TS = datetime.datetime.now(datetime.UTC).isoformat()

# Commit map for versioning
COMMITS = {
    "openwrt-core": os.environ.get("OPENWRT_COMMIT", "unknown"),
    "openwrt-hotplug": os.environ.get("OPENWRT_COMMIT", "unknown"),
    "procd": os.environ.get("OPENWRT_COMMIT", "unknown"),
    "uci": os.environ.get("OPENWRT_COMMIT", "unknown"),
    "wiki": "N/A",  # Wiki is live, no single commit
    "luci": os.environ.get("LUCI_COMMIT", "unknown"),
    "luci-examples": os.environ.get("LUCI_COMMIT", "unknown"),
    "ucode": os.environ.get("UCODE_COMMIT", "unknown"),
}

# --- Pass 1: YAML Injection & Registry Build ---
print("[03] Pass 1: YAML Schema Injection & Link Registry Build")

cross_link_registry = {
    "pipeline_date": TS,
    "symbols": {}
}

# Common words to ignore when scanning for code symbols in headings
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
    "procd"
}

def is_code_symbol(name):
    if name.lower() in COMMON_WORDS:
        return False
    if len(name) < 4:
        return False
    if re.match(r'^[a-z][a-zA-Z0-9]+$', name) and any(c.isupper() for c in name):
        return True
    if "." in name and len(name) >= 5:
        return True
    if "_" in name and len(name) >= 5:
        return True
    if re.match(r'^[A-Z]{3,6}$', name):
        return True
    return False

l2_files_pass1 = []

for root, _, files in os.walk(L1_DIR):
    for f in files:
        if not f.endswith(".md"):
            continue
            
        md_path = os.path.join(root, f)
        meta_path = os.path.splitext(md_path)[0] + ".meta.json"
        
        try:
            with open(md_path, "r", encoding="utf-8") as file:
                content = file.read()
        except:
            continue
            
        meta = {}
        if os.path.isfile(meta_path):
            with open(meta_path, "r", encoding="utf-8") as file:
                try:
                    meta = json.load(file)
                except:
                    pass
                    
        module = meta.get("module", "unknown")
        origin_type = meta.get("origin_type", "unknown")
        lang = meta.get("language", "")
        upath = meta.get("upstream_path", "")
        slug = meta.get("slug", os.path.splitext(f)[0])
        version = COMMITS.get(module, "unknown")
        
        # Grab title from H1 or fallback
        title_m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_m.group(1).strip() if title_m else slug
        
        # Grab description: first sentence of first non-heading, non-quote line
        desc = ""
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith(">") and not line.startswith("```"):
                sentence_end = line.find(". ")
                if sentence_end != -1:
                    desc = line[:sentence_end+1]
                else:
                    desc = line[:100] + ("..." if len(line) > 100 else "")
                break
                
        # Token calculation
        t_count = count_tokens(content)
        
        # Inject Mermaid sequentially
        if module == "procd" and "init" in title.lower():
            mermaid_tmpl = os.path.join(os.path.dirname(__file__), "..", "..", "templates", "mermaid", "procd-init-sequence.md")
            if os.path.isfile(mermaid_tmpl):
                with open(mermaid_tmpl, "r", encoding="utf-8") as tmpl_f:
                    mermaid_content = tmpl_f.read().strip()
                # Insert just after the first header/quote block
                split_idx = content.find("---\n\n")
                if split_idx != -1:
                    ins_pt = split_idx + 6
                    content = content[:ins_pt] + mermaid_content + "\n\n" + content[ins_pt:]
                else:
                    content = content + "\n\n" + mermaid_content
                # Update tokens
                t_count = count_tokens(content)

        # YAML Injection
        yaml = []
        yaml.append("---")
        yaml.append(f'title: "{title.replace('"', "")}"')
        yaml.append(f'module: "{module}"')
        yaml.append(f'origin_type: "{origin_type}"')
        yaml.append(f'token_count: {t_count}')
        yaml.append(f'version: "{version}"')
        
        l1_rel = os.path.relpath(md_path, WORKDIR).replace("\\", "/")
        yaml.append(f'source_file: "{l1_rel}"')
        
        if upath:
            yaml.append(f'upstream_path: "{upath}"')
        if lang:
            yaml.append(f'language: "{lang}"')
        if desc:
            yaml.append(f'description: "{desc.replace('"', "")}"')
            
        yaml.append(f'last_pipeline_run: "{TS}"')
        yaml.append("---\n")
        
        full_l2_content = "\n".join(yaml) + content
        
        l2_out_dir = os.path.join(L2_DIR, module)
        os.makedirs(l2_out_dir, exist_ok=True)
        l2_out_file = os.path.join(l2_out_dir, f)
        
        with open(l2_out_file, "w", encoding="utf-8", newline="\n") as out:
            out.write(full_l2_content)
            
        l2_files_pass1.append({"path": l2_out_file, "module": module, "root_rel": f"{module}/{f}"})
        
        # Extract symbols for registry
        l2_rel = f"{module}/{f}"
        # Matches: ## Symbol or ## Symbol(args)
        for m in re.finditer(r'^#{2,4}\s+[`"]?([A-Za-z][A-Za-z0-9_.]+(?:\(.*\))?)[`"]?', content, re.MULTILINE):
            raw_node = m.group(1)
            symbol = re.split(r'\(', raw_node)[0].strip()
            if not is_code_symbol(symbol):
                continue
            
            # Signature is either the balanced paren block or just the symbol()
            signature = raw_node
            if "(" not in signature:
                signature = f"{symbol}()"
            
            payload = {
                "signature": signature,
                "file": l1_rel,
                "relative_target": f"../{l2_rel}",
                "returns": "any",
                "parameters": []
            }
            
            if symbol not in cross_link_registry["symbols"]:
                cross_link_registry["symbols"][symbol] = payload
            else:
                # Prefer API docs (ucode/luci) over others for the linking target
                current = cross_link_registry["symbols"][symbol]["file"]
                this_is_api = any(x in l1_rel for x in ["ucode", "luci"])
                curr_is_api = any(x in current for x in ["ucode", "luci"])
                if this_is_api and not curr_is_api:
                    cross_link_registry["symbols"][symbol] = payload

# Save cross-link registry
registry_path = os.path.join(WORKDIR, "cross-link-registry.json")
with open(registry_path, "w", encoding="utf-8") as reg_f:
    json.dump(cross_link_registry, reg_f, indent=2)

print(f"[03] Pass 1 complete: {len(l2_files_pass1)} L2 files staged, {len(cross_link_registry['symbols'])} symbols registered.")

# --- Pass 2: Linking ---
print("[03] Pass 2: Injecting Cross-Links")

total_injected = 0
files_modified = 0

# Pre-compile patterns once for performance
sorted_symbols = sorted(cross_link_registry["symbols"].items(), key=lambda x: -len(x[0]))
compiled_patterns = []
for symbol, meta in sorted_symbols:
    target = meta["relative_target"]
    pat = re.compile(rf'\b{re.escape(symbol)}\b(?:\(\))?')
    compiled_patterns.append((symbol, target, pat))

for file_info in l2_files_pass1:
    fpath = file_info["path"]
    this_mod = file_info["module"]
    this_rel = file_info["root_rel"]
    
    with open(fpath, "r", encoding="utf-8") as file:
        original = file.read()
        
    protected = set()
    for fence in re.finditer(r'```.*?```|~~~.*?~~~|---.*?---', original, re.DOTALL):
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

    for symbol, target, pat in compiled_patterns:
        if target.endswith(this_rel): # Don't link to self
            continue
            
        for m in pat.finditer(original):
            s, e = m.start(), m.end()
            if any(i in protected for i in range(s, e)):
                continue
            if overlaps_existing(s, e):
                continue
            matched_text = m.group(0)
            spans.append((s, e, f"[{matched_text}]({target})"))

    if spans:
        spans.sort(key=lambda x: x[0])
        out = []
        last = 0
        for s, e, rep in spans:
            out.append(original[last:s])
            out.append(rep)
            last = e
        out.append(original[last:])
        modified = "".join(out)
        
        with open(fpath, "w", encoding="utf-8", newline="\n") as out_f:
            out_f.write(modified)
            
        files_modified += 1
        total_injected += len(spans)

print(f"[03] Pass 2 complete: {total_injected} links injected across {files_modified} files.")

print("[03] Engine run complete.")
