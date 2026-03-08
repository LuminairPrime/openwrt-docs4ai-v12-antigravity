"""
Purpose: Generates the web landing page (index.html).
Phase: Presentation
Layers: L3
Inputs: OUTDIR/llms.txt
Outputs: OUTDIR/index.html
Environment Variables: OUTDIR
Dependencies: lib.config
Notes: Reads the generated llms.txt to build a human-friendly navigation menu.
"""

import os
import re
import datetime
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib import config

sys.stdout.reconfigure(line_buffering=True)

OUTDIR = config.OUTDIR
LLMS_TXT = os.path.join(OUTDIR, "llms.txt")
TS = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")

print("[07] Generating index.html web landing page")

if not os.path.isfile(LLMS_TXT):
    print(f"[07] FAIL: llms.txt not found at {LLMS_TXT}")
    sys.exit(1)

try:
    with open(LLMS_TXT, "r", encoding="utf-8") as f:
        llms_content = f.read()
except Exception as e:
    print(f"[07] FAIL: Could not read llms.txt: {e}")
    sys.exit(1)

# Extract categories and modules from llms.txt
# Patterns look like:
# ## Category
# - [module](./module/llms.txt): description (~tokens)
sections = re.findall(r'## (.*?)\n((?:- \[.*?\]\(.*?\):.*?\n)+)', llms_content)

html_list = []
for title, items in sections:
    html_list.append(f"<h2>{title}</h2>")
    html_list.append("<ul>")
    for item in items.strip().split("\n"):
        # Parse: - [module](link): desc (~tokens)
        m = re.match(r'- \[(.*?)\]\((.*?)\): (.*)', item)
        if m:
            name, link, desc_token = m.groups()
            # Link to the module's HTML folder or monolith if we had a better mapper, 
            # for now link to the .md context or the module sub-index.
            html_list.append(f'  <li><a href="{link}">{name}</a>: {desc_token}</li>')
    html_list.append("</ul>")

# Construct final HTML
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>openwrt-docs4ai API Documentation</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 40px auto; padding: 0 20px; }}
        h1 {{ border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        h2 {{ margin-top: 30px; color: #0366d6; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin-bottom: 8px; padding: 8px; border-radius: 4px; background: #f6f8fa; }}
        a {{ color: #0366d6; text-decoration: none; font-weight: bold; }}
        a:hover {{ text-decoration: underline; }}
        .meta {{ font-size: 0.85em; color: #666; margin-top: 40px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style>
</head>
<body>
    <h1>openwrt-docs4ai Navigation</h1>
    <p>This repository provides LLM-optimized documentation for OpenWrt. Select a module below to view its context or jump to the <a href="llms.txt">AI-optimized index (llms.txt)</a>.</p>

    {"".join(html_list)}

    <div class="meta">
        Generated: {TS}<br>
        Pipeline Version: v12<br>
        <a href="https://github.com/openwrt/openwrt-condensed-docs">Source Repository</a>
    </div>
</body>
</html>
"""

with open(os.path.join(OUTDIR, "index.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(html_content)

print("[07] OK: index.html generated successfully.")
