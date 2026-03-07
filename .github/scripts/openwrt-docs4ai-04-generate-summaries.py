"""
openwrt-docs4ai-04-generate-summaries.py

Purpose  : Generate AI summaries for API documentation files using GitHub Models API.
Status   : COMPLETELY OPTIONAL — this script is skipped by default (SKIP_AI=true).
           GitHub free accounts are limited to ~50 AI model requests per month,
           making automated summarization impractical for regular pipeline runs.
           The pipeline produces fully valid output without AI summaries.

Env Vars : OUTDIR (default: ./openwrt-condensed-docs) — where generated docs live
           SKIP_AI ("true" to skip entirely — THIS IS THE DEFAULT)
           GITHUB_TOKEN — API token for GitHub Models (CI)
           LOCAL_DEV_TOKEN — alternative token for local development
           MAX_AI_FILES (default: 40) — cap on files to summarize per run
Outputs  : Mutates .md files in $OUTDIR — prepends AI summary section
Deps     : requests
Notes    : Only processes module docs (ucode-module-*.md, luci-api-*.md).
           Rate-limited with retry-after-backoff to stay within free tier.
           Files already containing "## AI Summary" are skipped.

Manual Alternative:
  Instead of running this script, you can manually summarize files by pasting
  the following prompt into any AI chatbot (ChatGPT, Claude, Gemini, etc.)
  along with the content of one or more .md files from openwrt-condensed-docs/:

  ┌─────────────────────── COPY-PASTE PROMPT ───────────────────────┐
  │ You are a technical documentation assistant for OpenWrt — a     │
  │ Linux-based OS for embedded network devices. For each API/module│
  │ doc I provide, produce a 2-4 sentence summary that answers:    │
  │   1. What does this module do?                                 │
  │   2. What are its key functions/methods?                       │
  │   3. When would a developer use it?                            │
  │ Use plain technical language. No filler. Do not repeat the     │
  │ module name. Start with the verb describing the module's       │
  │ purpose. Format each summary as:                               │
  │   ## AI Summary                                                │
  │   <your summary here>                                          │
  │   ---                                                          │
  │ Place the summary block after the metadata header (after the   │
  │ first "---" separator) in each file.                           │
  └─────────────────────────────────────────────────────────────────┘
"""

import os
import re
import glob
import time
import sys

sys.stdout.reconfigure(line_buffering=True)

OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
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

# Token resolution: prefer GITHUB_TOKEN over LOCAL_DEV_TOKEN
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
    """Call GitHub Models API to generate a summary. Returns summary text or None."""
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
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"[04] WARN: API error for {fname} (attempt {attempt + 1}): {e}")
            time.sleep(5)
    return None


# --- Collect target files ---
targets = (
    sorted(glob.glob(os.path.join(OUTDIR, "ucode-docs", "ucode-module-*.md"))) +
    sorted(glob.glob(os.path.join(OUTDIR, "luci-docs", "luci-api-*.md")))
)

# Filter out files that already have summaries
to_process = []
for fpath in targets:
    try:
        content = open(fpath, encoding="utf-8").read()
        if "## AI Summary" in content:
            continue
        to_process.append(fpath)
    except Exception:
        continue

print(f"[04] {len(to_process)} files need summaries (cap: {MAX_FILES})")

# --- Process files ---
summarized = 0
for fpath in to_process[:MAX_FILES]:
    fname = os.path.basename(fpath)
    content = open(fpath, encoding="utf-8").read()

    summary = summarize(content, fname)
    if not summary:
        print(f"[04] FAIL: {fname} — no summary generated")
        continue

    # Inject summary after the metadata header (after first "---\n\n")
    sep = "---\n\n"
    pos = content.find(sep)
    if pos != -1:
        insert_pos = pos + len(sep)
        summaried = (
            content[:insert_pos] +
            f"## AI Summary\n\n{summary}\n\n---\n\n" +
            content[insert_pos:]
        )
    else:
        summaried = content + f"\n\n## AI Summary\n\n{summary}\n"

    with open(fpath, "w", encoding="utf-8", newline="\n") as f:
        f.write(summaried)

    summarized += 1
    print(f"[04] OK: {fname}")
    time.sleep(2)  # rate limit buffer

print(f"[04] Complete: {summarized} summaries generated.")
