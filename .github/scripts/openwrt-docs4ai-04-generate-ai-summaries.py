"""
Purpose: Generate AI summaries for API documentation files using AI.
Phase: AI Enrichment (Optional)
Layers: L2 -> L2 (In-place modification)
Inputs: OUTDIR/.L2-semantic/ucode/ and OUTDIR/.L2-semantic/luci/
Outputs: OUTDIR/.L2-semantic/ucode/ and OUTDIR/.L2-semantic/luci/ (Mutated)
Environment Variables: OUTDIR, SKIP_AI, GITHUB_TOKEN, LOCAL_DEV_TOKEN
Dependencies: requests
Notes: Appends ai_summary tags to the L2 YAML frontmatter. Skipped by default.

=========================== MANUAL AI REPLACEMENT PROMPT ===========================
Copy and paste the block below into an LLM (Claude, ChatGPT, or Antigravity) to 
perform this script's enrichment logic manually when the API is unavailable.

## Task: L2 AI Enrichment (Manual Pipeline Step)

You are performing the AI enrichment stage of the openwrt-docs4ai pipeline. 
This step mutates L2 semantic files by appending machine-generated metadata 
to their YAML frontmatter.

### The Mission
1. For each provided file, read the YAML frontmatter and the document body.
2. If the YAML already contains `ai_summary:`, skip it.
3. If the content below the `---` is less than 15 words, skip it.
4. Otherwise, generate the following three YAML fields:
   - `ai_summary`: 2-4 sentences starting with a verb. List specific functions.
   - `ai_when_to_use`: 1-2 sentence OpenWrt-specific use case.
   - `ai_related_topics`: List of 2-6 exact symbol names found in the text.
5. Mutate the file by inserting these fields BEFORE the closing `---`.

### Constraints
- DO NOT edit the document body. 
- DO NOT reorder existing fields.
- DO NOT hallucinate: every function mentioned must exist in the text.
- RESPONSE FORMAT: Return the ENTIRE modified file content inside a Markdown block.

### Context
`origin_type` helps define the source (c_source, js_source, wiki_page, readme).
`module` groups the subsystem (ucode, luci, procd, uci).

[PASTE FILE CONTENT BELOW]
====================================================================================
"""

import os
import re
import glob
import time
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib import config

sys.stdout.reconfigure(line_buffering=True)

OUTDIR = config.OUTDIR
SKIP_AI = os.environ.get("SKIP_AI", "true").lower() == "true"
MAX_FILES = int(os.environ.get("MAX_AI_FILES", "40"))

if SKIP_AI:
    print("[04] SKIP: AI summarization disabled (SKIP_AI=true)")
    sys.exit(0)

print("[04] Generate AI summaries for API documentation")

try:
    import requests
except ImportError:
    print("[04] FAIL: 'requests' package not installed")
    sys.exit(1)

import os
import re
import glob
import time
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib import config

sys.stdout.reconfigure(line_buffering=True)

OUTDIR = config.OUTDIR
SKIP_AI = os.environ.get("SKIP_AI", "true").lower() == "true"
MAX_FILES = int(os.environ.get("MAX_AI_FILES", "40"))

# AI Caching State
CACHE_PATH = os.environ.get("AI_CACHE_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "ai-summaries-cache.json"))
ai_cache = {}
if os.path.exists(CACHE_PATH):
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            ai_cache = json.load(f)
        print(f"[04] Loaded AI Cache: {len(ai_cache)} entries")
    except Exception as e:
        print(f"[04] WARN: Could not load AI Cache ({e})")

if SKIP_AI:
    print("[04] SKIP: AI summarization disabled (SKIP_AI=true)")
    sys.exit(0)

print("[04] Generate AI summaries (Cache-First Mode)")

try:
    import requests
except ImportError:
    print("[04] FAIL: 'requests' package not installed")
    sys.exit(1)

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("LOCAL_DEV_TOKEN")
if not TOKEN:
    print("[04] SKIP: No API token (GITHUB_TOKEN or LOCAL_DEV_TOKEN not set)")
    sys.exit(0)

API_URL = "https://models.inference.ai.azure.com/chat/completions"
MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a technical documentation assistant for OpenWrt — a Linux-based
operating system for embedded network devices. You write clear, accurate,
developer-focused descriptions.

Given an API/module doc as context, produce a JSON object with:
1. "summary": 2-4 sentences describing purpose and key functions.
2. "when_to_use": 1-2 sentence OpenWrt-specific use case.
3. "related_topics": list of 2-6 exact symbol names.

Follow spelling/naming in the text exactly. Summarize technical purpose precisely."""

def summarize(content, fname):
    user_msg = f"Summarize this OpenWrt API module documentation:\n\n{content[:4000]}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.3,
        "max_tokens": 500
    }

    for attempt in range(3):
        try:
            resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", 30))
                print(f"[04] Rate-limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
                continue
            if resp.status_code == 403 or "no quota" in resp.text.lower() or "limit reached" in resp.text.lower():
                print(f"[04] API quota limit reached. Response: {resp.text}")
                return None
            resp.raise_for_status()
            data = resp.json()
            raw_res = json.loads(data["choices"][0]["message"]["content"])
            # Normalize multiline summary for YAML
            if "summary" in raw_res: raw_res["summary"] = raw_res["summary"].replace("\n", " ").strip()
            if "when_to_use" in raw_res: raw_res["when_to_use"] = raw_res["when_to_use"].replace("\n", " ").strip()
            return raw_res
        except Exception as e:
            print(f"[04] WARN: API error for {fname} (attempt {attempt + 1}): {e}")
            time.sleep(5)
    return None

l2_dir = os.path.join(OUTDIR, "L2-semantic")
l1_raw_dir = config.L1_RAW_WORKDIR # We need hashes from L1 meta

targets = []
for module in ["ucode", "luci"]:
    targets.extend(glob.glob(os.path.join(l2_dir, module, "*.md")))

to_process = []
for fpath in targets:
    try:
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        if "ai_summary:" in content:
            continue
        to_process.append(fpath)
    except Exception:
        continue

print(f"[04] {len(to_process)} files need summaries (Cap: {MAX_FILES}, Token Budget: ${config.LLM_BUDGET_LIMIT})")

summarized = 0
cached = 0
cache_updated = False

for fpath in to_process[:MAX_FILES]:
    fname = os.path.basename(fpath)
    mod_name = os.path.basename(os.path.dirname(fpath))
    
    # Try to find content_hash from L1 meta
    content_hash = "unknown"
    meta_path = os.path.join(l1_raw_dir, mod_name, fname.replace(".md", ".meta.json"))
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as fm:
                meta = json.load(fm)
                content_hash = meta.get("content_hash", "unknown")
        except: pass

    # 1. Lookup Cache
    res = None
    if content_hash in ai_cache and content_hash != "unknown":
        res = ai_cache[content_hash]
        cached += 1
    else:
        # 2. Call LLM
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        res = summarize(content, fname)
        if res:
            if content_hash != "unknown":
                ai_cache[content_hash] = res
                cache_updated = True
            summarized += 1
            time.sleep(1) # Gentle pacing
        else:
            print(f"[04] FAIL: {fname} — no summary generated")
            continue

    # 3. Inject Enriched YAML
    with open(fpath, encoding="utf-8") as f:
        content = f.read()
        
    fm_match = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n?(.*)', content, re.DOTALL)
    if fm_match and res:
        fm_text = fm_match.group(1).strip()
        body_text = fm_match.group(2)
        
        # Safe YAML Injection
        new_lines = [fm_text]
        new_lines.append(f'ai_summary: "{res.get("summary", "").replace("\"", "\\\"")}"')
        new_lines.append(f'ai_when_to_use: "{res.get("when_to_use", "").replace("\"", "\\\"")}"')
        
        topics = res.get("related_topics", [])
        topics_str = ", ".join([f'"{t}"' for t in topics])
        new_lines.append(f'ai_related_topics: [{topics_str}]')
        
        new_content = f"---\n" + "\n".join(new_lines) + f"\n---\n{body_text}"
        with open(fpath, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
        if (summarized + cached) % 10 == 0:
            print(f"[04] Progress: {summarized + cached}/{len(to_process)}")

if cache_updated:
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(ai_cache, f, indent=2)
        print(f"[04] Cache updated ({len(ai_cache)} total entries)")
    except Exception as e:
        print(f"[04] ERR: Could not save cache: {e}")

print(f"[04] Complete: {summarized} generated, {cached} reused from cache.")
