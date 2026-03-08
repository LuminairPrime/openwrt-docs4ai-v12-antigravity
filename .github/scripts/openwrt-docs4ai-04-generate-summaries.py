"""
Purpose: Generate AI summaries for API documentation files using GitHub Models API.
Phase: Enrichment (Optional)
Layers: L2 -> L2 (In-place modification)
Inputs: OUTDIR/.L2-semantic/ucode/ and OUTDIR/.L2-semantic/luci/
Outputs: OUTDIR/.L2-semantic/ucode/ and OUTDIR/.L2-semantic/luci/ (Mutated)
Environment Variables: OUTDIR, SKIP_AI, GITHUB_TOKEN, LOCAL_DEV_TOKEN
Dependencies: requests
Notes: Appends ai_summary tags to the L2 YAML frontmatter. Skipped by default.
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

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("LOCAL_DEV_TOKEN")
if not TOKEN:
    print("[04] SKIP: No API token (GITHUB_TOKEN or LOCAL_DEV_TOKEN not set)")
    sys.exit(0)

API_URL = "https://models.inference.ai.azure.com/chat/completions"
MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a technical documentation assistant for OpenWrt — a Linux-based
operating system for embedded network devices. You write clear, accurate,
developer-focused descriptions.

Given an API/module doc as context, produce a 2-4 sentence summary that answers:
1. What does this module do?
2. What are its key functions/methods?
3. When would a developer use it?

Use plain technical language. No filler or marketing phrases. Do not repeat the module name
in your summary. Start with the verb describing the module's purpose."""

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
        "temperature": 0.3,
        "max_tokens": 300
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
                print("[04] Aborting AI summaries gracefully to continue pipeline.")
                sys.exit(0)
            resp.raise_for_status()
            data = resp.json()
            # Normalize multiline string for YAML
            summary = data["choices"][0]["message"]["content"].strip()
            return summary.replace("\n", " ")
        except Exception as e:
            print(f"[04] WARN: API error for {fname} (attempt {attempt + 1}): {e}")
            time.sleep(5)
    return None

l2_dir = os.path.join(OUTDIR, ".L2-semantic")
targets = []
for module in ["ucode", "luci"]:
    targets.extend(glob.glob(os.path.join(l2_dir, module, "*.md")))

to_process = []
for fpath in targets:
    try:
        content = open(fpath, encoding="utf-8").read()
        if "ai_summary:" in content:
            continue
        to_process.append(fpath)
    except Exception:
        continue

print(f"[04] {len(to_process)} files need summaries (cap: {MAX_FILES})")

summarized = 0
for fpath in to_process[:MAX_FILES]:
    fname = os.path.basename(fpath)
    content = open(fpath, encoding="utf-8").read()

    summary = summarize(content, fname)
    if not summary:
        print(f"[04] FAIL: {fname} — no summary generated")
        continue

    # Inject ai_summary before the closing --- of the yaml frontmatter
    end_yaml_pos = content.find("\n---\n")
    if end_yaml_pos != -1:
        # Avoid breaking YAML formatting
        safe_summary = summary.replace('"', '\\"')
        summaried = (
            content[:end_yaml_pos] +
            f'\nai_summary: "{safe_summary}"' +
            content[end_yaml_pos:]
        )
        with open(fpath, "w", encoding="utf-8", newline="\n") as f:
            f.write(summaried)
        summarized += 1
        print(f"[04] OK: {fname}")
        time.sleep(2)
    else:
        print(f"[04] WARN: Could not find YAML frontmatter in {fname}")

print(f"[04] Complete: {summarized} summaries generated.")
