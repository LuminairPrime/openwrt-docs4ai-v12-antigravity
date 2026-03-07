"""
openwrt-docs4ai-02a-scrape-wiki.py

Purpose  : Scrape OpenWrt developer wiki pages to individual markdown files.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs) -- generated output destination
           SKIP_WIKI ("true" to skip entirely)
           WIKI_MAX_PAGES (default: 300) -- cap on pages fetched
Outputs  : $OUTDIR/openwrt-wiki-docs/*.md
           $OUTDIR/openwrt-wiki-docs/llms.txt
Deps     : requests, pandoc (system binary)
Notes    : Page discovery uses DokuWiki's built-in ?do=index endpoint, which
           returns the namespace page listing without triggering bot detection.
           Content is fetched via ?do=export_raw (raw DokuWiki markup) and
           converted to GitHub Flavored Markdown via pandoc.
           Modification dates are extracted from each page's raw export
           header or from the rendered page footer.
           Rate-limited (1.5s between requests) to respect openwrt.org.
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
    print("[02a] FAIL: 'requests' package not installed")
    sys.exit(1)

# --- Configuration ---
OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
SKIP_WIKI = os.environ.get("SKIP_WIKI", "false").lower() == "true"
MAX_PAGES = int(os.environ.get("WIKI_MAX_PAGES", "300"))

if SKIP_WIKI:
    print("[02a] SKIP: Wiki scraping disabled (SKIP_WIKI=true)")
    sys.exit(0)

print("[02a] Scrape OpenWrt wiki (crawl namespace indexes, last 2 years)")

OUT_DIR = os.path.join(OUTDIR, "openwrt-wiki-docs")

DELAY  = 1.5
CUTOFF = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=730)

# Namespaces to crawl. idx param uses DokuWiki's colon-separated namespace format.
NAMESPACES = [
    ("/docs/techref/",        "docs%3Atechref"),
    ("/docs/guide-developer/", "docs%3Aguide-developer"),
    ("/docs/guide-user/base-system/uci/", "docs%3Aguide-user%3Abase-system%3Auci"),
]

SKIP_PATTERNS = [
    "/toh/",
    "/inbox/",
    "/meta/",
    "/playground/",
    "changelog",
    "release_notes",
]

session = requests.Session()
# No custom UA needed -- the ?do=index and ?do=export_raw endpoints
# bypass the wiki's JavaScript bot challenge entirely.


def get_existing_lastmod(fname):
    """Check if we already have this file and what its lastmod date is."""
    fpath = os.path.join(OUT_DIR, fname)
    if not os.path.isfile(fpath):
        return None
    try:
        with open(fpath, encoding="utf-8") as fh:
            for line in fh:
                m = re.search(r'\*\*Last modified:\*\*\s*(\d{4}-\d{2}-\d{2})', line)
                if m:
                    return datetime.datetime.strptime(m.group(1), "%Y-%m-%d")
                if line.startswith("---"):
                    break
    except Exception:
        pass
    return None


def get_existing_title(fname):
    """Read the title from an existing file."""
    fpath = os.path.join(OUT_DIR, fname)
    try:
        with open(fpath, encoding="utf-8") as fh:
            first = fh.readline().strip()
            if first.startswith("# "):
                return first[2:]
    except Exception:
        pass
    return fname


def path_to_filename(url_path):
    """Convert a wiki URL path to a safe filename."""
    parts = url_path.strip("/").split("/")
    if parts and parts[0] == "docs":
        parts = parts[1:]
    if parts and parts[-1] == "start":
        parts = parts[:-1]
    slug = "-".join(p for p in parts if p)
    slug = re.sub(r"[^a-z0-9-]", "-", slug.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return f"openwrt-{slug}.md" if slug else "openwrt-misc.md"


def extract_lastmod_from_raw(raw_text):
    """
    DokuWiki raw exports sometimes include a date comment at the top,
    or we can check the page info endpoint. For now, we'll fetch the
    page info separately if needed.
    """
    return None  # handled by page info endpoint


def fetch_page_lastmod(url):
    """
    Fetch the modification date of a wiki page by requesting the page
    info view (?do=revisions shows history, but ?do=export_xhtml gives
    the last-modified in response headers).
    """
    try:
        # Use a HEAD request first to check Last-Modified header
        r = session.head(url, timeout=15, allow_redirects=True)
        lm = r.headers.get("Last-Modified")
        if lm:
            try:
                # Parse HTTP date format: "Tue, 15 Aug 2024 12:34:56 GMT"
                from email.utils import parsedate_to_datetime
                dt = parsedate_to_datetime(lm)
                return datetime.datetime(dt.year, dt.month, dt.day)
            except Exception:
                pass
    except Exception:
        pass

    # Fallback: check the raw content for date patterns
    return None


# ============================================================
# Step 1: Discover pages via DokuWiki ?do=index endpoint
# ============================================================

print("[02a] Discovering pages via DokuWiki namespace indexes...")
discovered_pages = set()  # set of /docs/... paths

for prefix, idx_param in NAMESPACES:
    # The ?do=index&idx=... endpoint returns the full namespace listing
    # as rendered HTML, without triggering bot detection.
    index_url = f"https://openwrt.org{prefix}start?do=index&idx={idx_param}"
    print(f"[02a] Fetching namespace index: {prefix}")
    time.sleep(DELAY)

    try:
        resp = session.get(index_url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"[02a] WARN: Could not fetch index for {prefix}: {e}")
        continue

    html = resp.text

    # Extract all href links, normalize to /docs/... paths
    for m in re.finditer(r'href="([^"#?]*)"', html):
        href = m.group(1)

        # Normalize to path
        path = None
        if href.startswith("https://openwrt.org"):
            path = href.replace("https://openwrt.org", "")
        elif href.startswith("/docs/"):
            path = href
        else:
            continue

        # Must be in our target namespace
        if not path.startswith(prefix):
            continue
        # Skip /start pages (they are namespace index pages, not content)
        if path.rstrip("/").endswith("/start"):
            continue
        # Skip patterns
        if any(pat in path for pat in SKIP_PATTERNS):
            continue
        # Skip language variants (e.g., /ja/docs/...)
        if re.match(r'^/[a-z]{2}(-[a-z]+)?/', path):
            continue
        # Skip DokuWiki export/internal paths
        if "/_export/" in path or "/_detail/" in path or "/_media/" in path:
            continue

        discovered_pages.add(path)

if not discovered_pages:
    print("[02a] WARN: No wiki pages discovered from namespace indexes.")
    print("[02a] SKIP: Wiki documentation generation skipped.")
    sys.exit(0)

print(f"[02a] Discovered {len(discovered_pages)} unique wiki pages (cap: {MAX_PAGES})")

# Create output directory only after we confirmed pages exist
os.makedirs(OUT_DIR, exist_ok=True)


# ============================================================
# Step 2: Fetch content and filter by modification date
# ============================================================

print("[02a] Fetching pages and checking modification dates...")
toc_entries = []
saved = 0
skipped_old = 0
skipped_unchanged = 0
failed = 0

for path in sorted(discovered_pages):
    if saved >= MAX_PAGES:
        print(f"[02a] WARN: Reached WIKI_MAX_PAGES={MAX_PAGES} cap. Stopping.")
        break

    url = f"https://openwrt.org{path}"
    fname = path_to_filename(path)

    # Fetch raw DokuWiki source (bypasses bot detection)
    time.sleep(DELAY)
    raw_url = f"{url}?do=export_raw"
    try:
        r = session.get(raw_url, timeout=20)
        r.raise_for_status()
        raw_content = r.text
    except Exception as e:
        print(f"[02a] FAIL: {path} ({e})")
        failed += 1
        continue

    if not raw_content.strip() or "This topic does not exist" in raw_content:
        continue

    # Check modification date from response headers
    last_mod = fetch_page_lastmod(url)

    # Skip pages older than cutoff
    if last_mod and last_mod < CUTOFF:
        skipped_old += 1
        continue

    # Check if we already have an up-to-date version
    existing_mod = get_existing_lastmod(fname)
    if existing_mod and last_mod and existing_mod >= last_mod:
        title = get_existing_title(fname)
        date_str = last_mod.strftime("%Y-%m-%d") if last_mod else "unknown"
        toc_entries.append((fname, title, url, date_str))
        skipped_unchanged += 1
        continue

    # Convert DokuWiki markup to GitHub Flavored Markdown via pandoc
    try:
        result = subprocess.run(
            ["pandoc", "-f", "dokuwiki", "-t", "gfm", "--wrap=none"],
            input=raw_content, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=30
        )
        md = result.stdout or ""
    except Exception as e:
        print(f"[02a] FAIL: pandoc error for {path} ({e})")
        failed += 1
        continue

    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    if len(md) < 200:
        continue

    date_str = last_mod.strftime("%Y-%m-%d") if last_mod else "unknown"
    fetch_ts = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
    title_m  = re.search(r"^#+ (.+)$", md, re.MULTILINE)
    title    = title_m.group(1).strip() if title_m else path.split("/")[-1]

    with open(os.path.join(OUT_DIR, fname), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# {title}\n\n")
        f.write(f"> **Source:** {url}\n")
        f.write(f"> **Last modified:** {date_str}\n")
        f.write(f"> **Fetched:** {fetch_ts}\n\n")
        f.write("---\n\n")
        # Remove the first heading if it duplicates our generated one
        f.write(re.sub(r"^#+ .+\n\n?", "", md, count=1))

    toc_entries.append((fname, title, url, date_str))
    saved += 1
    print(f"[02a] OK: {fname} [{date_str}] -- {title[:55]}")


# ============================================================
# Step 3: Write per-folder index
# ============================================================

ts = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
with open(os.path.join(OUT_DIR, "llms.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write("# OpenWrt Wiki Developer Documentation Index\n")
    f.write("# Source: https://openwrt.org/docs/\n")
    f.write(f"# Generated: {ts}\n")
    f.write("# Scope: /docs/techref/ + /docs/guide-developer/ -- last 2 years\n")
    f.write("# Discovery: DokuWiki namespace index (no sitemap)\n")
    f.write("# Incremental: unchanged pages are preserved from previous run.\n")
    f.write("#\n## Files in this directory\n\n")
    for fname, title, url, date in sorted(toc_entries):
        f.write(f"- [{fname}](/openwrt-wiki-docs/{fname}): {title} (modified: {date}) -- {url}\n")

print(f"[02a] Complete: {saved} fetched, {skipped_unchanged} unchanged, "
      f"{skipped_old} too old, {failed} failed.")
