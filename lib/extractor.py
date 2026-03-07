import os
import json

from lib import config

def write_l1_markdown(module, origin_type, slug, content, metadata=None):
    """
    Writes pure markdown text to the L1 working directory and a companion .meta.json sidecar.
    """
    out_dir = os.path.join(config.L1_RAW_WORKDIR, module)
    os.makedirs(out_dir, exist_ok=True)
    
    base_name = f"{origin_type}-{slug}"
    md_path = os.path.join(out_dir, f"{base_name}.md")
    meta_path = os.path.join(out_dir, f"{base_name}.meta.json")
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    if metadata:
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

def wrap_code_block(title, code, lang):
    """
    Wraps raw code in L1 markdown compliant format (header + fenced block).
    """
    return f"# {title}\n```{lang}\n{code}\n```\n"
