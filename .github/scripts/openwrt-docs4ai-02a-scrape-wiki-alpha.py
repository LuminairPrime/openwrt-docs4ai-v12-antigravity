"""
openwrt-docs4ai-02a-scrape-wiki-alpha.py

Purpose  : Scrape specific OpenWrt developer wiki pages (like ubus) to test targeted extraction.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs)
Outputs  : $OUTDIR/openwrt-wiki-alpha-docs/*.md
"""

import os
import re
import time
import datetime
import subprocess
import sys

sys.stdout.reconfigure(line_buffering=True)
try:
    import requests
except ImportError:
    print("[02a-alpha] FAIL: 'requests' package not installed")
    sys.exit(1)

OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
print("[02a-alpha] Scrape explicit targeted OpenWrt wiki pages")

OUT_DIR = os.path.join(OUTDIR, "openwrt-wiki-alpha-docs")
os.makedirs(OUT_DIR, exist_ok=True)

DELAY  = 1.5

# Specific target pages (e.g. ubus)
TARGET_PAGES = [
    "/docs/techref/ubus",
]

session = requests.Session()

def path_to_filename(url_path):
    parts = url_path.strip("/").split("/")
    if parts and parts[0] == "docs":
        parts = parts[1:]
    slug = "-".join(p for p in parts if p)
    slug = re.sub(r"[^a-z0-9-]", "-", slug.lower())
    return f"openwrt-{slug}.md" if slug else "openwrt-misc.md"

def fetch_page_lastmod(url):
    try:
        r = session.head(url, timeout=15, allow_redirects=True)
        lm = r.headers.get("Last-Modified")
        if lm:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(lm)
            return datetime.datetime(dt.year, dt.month, dt.day)
    except Exception:
        pass
    return None

saved = 0
failed = 0

for path in TARGET_PAGES:
    url = f"https://openwrt.org{path}"
    fname = path_to_filename(path)

    time.sleep(DELAY)
    raw_url = f"{url}?do=export_raw"
    try:
        r = session.get(raw_url, timeout=20)
        r.raise_for_status()
        raw_content = r.text
    except Exception as e:
        print(f"[02a-alpha] FAIL: {path} ({e})")
        failed += 1
        continue

    if not raw_content.strip() or "This topic does not exist" in raw_content:
        print(f"[02a-alpha] SKIP: Empty or missing content for {path}")
        continue

    last_mod = fetch_page_lastmod(url)

    try:
        result = subprocess.run(
            ["pandoc", "-f", "dokuwiki", "-t", "gfm", "--wrap=none"],
            input=raw_content, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=30
        )
        md = result.stdout or ""
    except Exception as e:
        print(f"[02a-alpha] FAIL: pandoc error for {path} ({e})")
        failed += 1
        continue

    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    
    date_str = last_mod.strftime("%Y-%m-%d") if last_mod else "unknown"
    fetch_ts = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
    title_m  = re.search(r"^#+ (.+)$", md, re.MULTILINE)
    title    = title_m.group(1).strip() if title_m else path.split("/")[-1]

    with open(os.path.join(OUT_DIR, fname), "w", encoding="utf-8", newline="\n") as f:
        f.write("---\n")
        f.write(f"module: {title}\n")
        f.write(f"title: Wiki - {title}\n")
        f.write(f"source: {url}\n")
        f.write(f"generated: {fetch_ts}\n")
        f.write("---\n\n")
        f.write(f"# {title}\n\n")
        f.write(f"> **Source:** {url}\n")
        f.write(f"> **Last modified:** {date_str}\n\n")
        f.write("---\n\n")
        f.write(re.sub(r"^#+ .+\n\n?", "", md, count=1))

    saved += 1
    print(f"[02a-alpha] OK: {fname} [{date_str}] -- {title[:55]}")

print(f"[02a-alpha] Complete: {saved} fetched, {failed} failed.")
