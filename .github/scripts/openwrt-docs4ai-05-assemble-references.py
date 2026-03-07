"""
openwrt-docs4ai-05-assemble-references.py

Purpose  : Assemble *-complete-reference.md files by concatenating individual docs.
Env Vars : OUTDIR (default: ./openwrt-condensed-docs) — where to read/write
           SKIP_WIKI ("true" to skip wiki reference assembly)
           SKIP_BUILDROOT ("true" to skip buildroot/examples reference assembly)
Outputs  : $OUTDIR/ucode-complete-reference.md
           $OUTDIR/luci-jsapi-complete-reference.md
           $OUTDIR/openwrt-wiki-complete-reference.md
           $OUTDIR/openwrt-buildroot-complete-reference.md
           $OUTDIR/openwrt-examples-complete-reference.md
Deps     : None (pure Python)
Notes    : Each reference file is a single concatenated document suitable for
           feeding whole to an LLM as a complete knowledge source.
           Split from the original monolithic 05-finalize-publish.sh.
"""

import os
import glob
import datetime
import sys
import re

sys.stdout.reconfigure(line_buffering=True)

OUTDIR = os.environ.get("OUTDIR", os.path.join(os.getcwd(), "openwrt-condensed-docs"))
SKIP_WIKI = os.environ.get("SKIP_WIKI", "false").lower() == "true"
SKIP_BUILDROOT = os.environ.get("SKIP_BUILDROOT", "false").lower() == "true"

TS = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")

print("[05] Assemble complete reference files")


def assemble(label, subdir, out_name, pattern="*.md", header_title=None,
             skip_flag=False, source_desc=""):
    """Concatenate all matching .md files from subdir into a single reference file."""
    if skip_flag:
        print(f"[05] SKIP: {label} (skip flag set)")
        return

    src_dir = os.path.join(OUTDIR, subdir)
    if not os.path.isdir(src_dir):
        print(f"[05] SKIP: {label} (directory not found: {subdir})")
        return

    files = sorted(glob.glob(os.path.join(src_dir, pattern)))
    # Exclude llms.txt from concatenation
    files = [f for f in files if os.path.basename(f) != "llms.txt"]

    if not files:
        print(f"[05] SKIP: {label} (no .md files found)")
        return

    title = header_title or label
    out_path = os.path.join(OUTDIR, out_name)
    skeleton_name = out_name.replace("-complete-reference", "-skeleton")
    skeleton_path = os.path.join(OUTDIR, skeleton_name)

    total_lines = 0
    with open(out_path, "w", encoding="utf-8", newline="\n") as out, \
         open(skeleton_path, "w", encoding="utf-8", newline="\n") as skeleton:
        out.write(f"# {title}\n\n")
        out.write(f"> **Generated:** {TS}\n")
        if source_desc:
            out.write(f"> **Source:** {source_desc}\n")
        out.write(f"> **Contains:** {len(files)} documents concatenated\n\n")
        out.write("---\n\n")

        skeleton.write(f"# {title} (Skeleton Semantic Map)\n\n")
        skeleton.write(f"> **Contains:** Only headers and function signatures for {len(files)} files.\n\n")
        skeleton.write("---\n\n")

        for fpath in files:
            try:
                content = open(fpath, encoding="utf-8").read().strip()
            except Exception as e:
                print(f"[05] WARN: Could not read {fpath}: {e}")
                continue
                
            # Strip YAML frontmatter
            content = re.sub(r'(?s)^---.*?---\n+', '', content)
            # Strip redundant Markdown blockquote metadata
            content = re.sub(r'^> \*\*.*?\n+', '', content, flags=re.MULTILINE)
            
            # Extract skeleton lines (Headers only)
            skeleton_lines = [line for line in content.split("\n") if line.startswith("#")]
            skeleton_content = "\n".join(skeleton_lines)
            
            lines = content.count("\n") + 1
            total_lines += lines
            out.write(content.strip())
            out.write("\n\n---\n\n")
            
            if skeleton_content.strip():
                skeleton.write(skeleton_content.strip() + "\n\n")

    print(f"[05] OK: {out_name} & {skeleton_name} ({len(files)} files)")


# --- Assemble each reference ---

assemble(
    label="ucode reference",
    subdir="ucode-docs",
    out_name="ucode-complete-reference.md",
    header_title="ucode Complete Reference",
    source_desc="https://github.com/jow-/ucode"
)

assemble(
    label="LuCI JS API reference",
    subdir="luci-docs",
    out_name="luci-jsapi-complete-reference.md",
    header_title="LuCI JavaScript API Complete Reference",
    source_desc="https://github.com/openwrt/luci"
)

assemble(
    label="Wiki reference",
    subdir="openwrt-wiki-docs",
    out_name="openwrt-wiki-complete-reference.md",
    header_title="OpenWrt Wiki Developer Documentation Complete Reference",
    source_desc="https://openwrt.org/docs/",
    skip_flag=SKIP_WIKI
)

assemble(
    label="Buildroot reference",
    subdir="openwrt-buildroot-docs",
    out_name="openwrt-buildroot-complete-reference.md",
    header_title="OpenWrt Buildroot Package Documentation Complete Reference",
    source_desc="https://github.com/openwrt/openwrt",
    skip_flag=SKIP_BUILDROOT
)

assemble(
    label="Examples reference",
    subdir="openwrt-examples",
    out_name="openwrt-examples-complete-reference.md",
    pattern="**/*.uc",
    header_title="OpenWrt LuCI Application Examples Complete Reference",
    source_desc="https://github.com/openwrt/luci/tree/master/applications",
    skip_flag=SKIP_BUILDROOT
)

# For examples: also include .js files since pattern only matches one type
# Reassemble examples with both .uc and .js using a walkthrough approach
if not SKIP_BUILDROOT:
    examples_dir = os.path.join(OUTDIR, "openwrt-examples")
    out_path = os.path.join(OUTDIR, "openwrt-examples-complete-reference.md")
    if os.path.isdir(examples_dir):
        all_files = []
        for root, _, fnames in os.walk(examples_dir):
            for fn in sorted(fnames):
                if fn.endswith((".uc", ".js")):
                    all_files.append(os.path.join(root, fn))
                elif fn.endswith(".md") and fn != "llms.txt":
                    all_files.append(os.path.join(root, fn))
        all_files.sort()

        if all_files:
            with open(out_path, "w", encoding="utf-8", newline="\n") as out:
                out.write("# OpenWrt LuCI Application Examples Complete Reference\n\n")
                out.write(f"> **Generated:** {TS}\n")
                out.write("> **Source:** https://github.com/openwrt/luci/tree/master/applications\n")
                out.write(f"> **Contains:** {len(all_files)} source files\n\n")
                out.write("---\n\n")
                for fpath in all_files:
                    rel = os.path.relpath(fpath, examples_dir).replace("\\", "/")
                    ext = os.path.splitext(fpath)[1]
                    lang = {"uc": "javascript", "js": "javascript"}.get(
                        ext.lstrip("."), ""
                    )
                    try:
                        content = open(fpath, encoding="utf-8").read().strip()
                    except Exception:
                        continue
                    out.write(f"## `{rel}`\n\n")
                    if ext in (".uc", ".js"):
                        out.write(f"```{lang}\n{content}\n```\n\n")
                    else:
                        out.write(content + "\n\n")
                    out.write("---\n\n")
            print(f"[05] OK: openwrt-examples-complete-reference.md ({len(all_files)} source files)")

print("[05] Complete.")
