#!/usr/bin/env python3
"""Render a page-level icon manifest into SVG and PNG assets.

Manifest format:
[
  {"name": "risk", "semantic": "风险提示", "icon": "triangle-alert", "color": "#E65100"}
]

The script looks for offline SVGs in resources/icons/svg first and falls back
to the local lucide source parser used by render_lucide_icon.py.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path

from runtime_paths import resolve_lucide_dir, resolve_node_bin, resolve_node_modules


SKILL_DIR = Path(__file__).resolve().parents[1]
RESOURCE_SVG = SKILL_DIR / "resources" / "icons" / "svg"


def lucide_svg(icon: str, color: str, lucide_dir: Path | None = None) -> str:
    lucide_dir = resolve_lucide_dir(lucide_dir)
    js_path = lucide_dir / f"{icon}.js"
    if not js_path.exists():
        raise FileNotFoundError(f"icon not found in resources or lucide: {icon}")
    js = js_path.read_text(encoding="utf-8")
    entries = re.findall(r'\[\s*"([a-zA-Z]+)"\s*,\s*\{([^}]*)\}\s*\]', js, re.S)
    parts: list[str] = []
    for tag, attrs_blob in entries:
        attrs = {}
        for key, quoted, numeric in re.findall(r'([a-zA-Z:-]+):\s*(?:"([^"]*)"|([0-9.]+))', attrs_blob):
            attrs[key] = quoted or numeric
        parts.append("<{} {} />".format(tag, " ".join(f'{k}="{v}"' for k, v in attrs.items())))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round">{"".join(parts)}</svg>'
    )


def recolor_svg(svg: str, color: str) -> str:
    color = color if color.startswith("#") else f"#{color}"
    if re.search(r'stroke="[^"]+"', svg):
        svg = re.sub(r'stroke="[^"]+"', f'stroke="{color}"', svg, count=1)
    else:
        svg = svg.replace("<svg ", f'<svg stroke="{color}" ', 1)
    return svg


def load_svg(icon: str, color: str, lucide_dir: Path | None = None) -> str:
    resource_path = RESOURCE_SVG / f"{icon}.svg"
    if resource_path.exists():
        return recolor_svg(resource_path.read_text(encoding="utf-8"), color)
    return lucide_svg(icon, color, lucide_dir)


def render_png(svg_path: Path, png_path: Path, size: int, node_bin: Path | None = None, node_modules: Path | None = None) -> None:
    node_script = f"""
const fs = require('fs');
const sharp = require('sharp');
(async () => {{
  await sharp(fs.readFileSync({str(svg_path)!r}), {{ density: 384 }})
    .resize({size}, {size}, {{ fit: 'contain' }})
    .png()
    .toFile({str(png_path)!r});
}})().catch((err) => {{ console.error(err); process.exit(1); }});
"""
    env = os.environ.copy()
    env["NODE_PATH"] = str(resolve_node_modules(node_modules))
    subprocess.run([str(resolve_node_bin(node_bin)), "-e", node_script], check=True, env=env)


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_") or "icon"


def main() -> None:
    parser = argparse.ArgumentParser(description="Render icon manifest to SVG/PNG assets.")
    parser.add_argument("manifest", help="JSON manifest file.")
    parser.add_argument("--out", required=True, help="Output directory.")
    parser.add_argument("--png", action="store_true", help="Also render PNGs.")
    parser.add_argument("--size", type=int, default=512, help="PNG size.")
    parser.add_argument("--lucide-dir", default="", help="Lucide ESM icon directory. Defaults to IML_PPTX_LUCIDE_DIR or Codex runtime.")
    parser.add_argument("--node-bin", default="", help="Node executable for PNG rendering. Defaults to IML_PPTX_NODE_BIN or Codex runtime.")
    parser.add_argument("--node-modules", default="", help="node_modules directory containing sharp. Defaults to IML_PPTX_NODE_MODULES or Codex runtime.")
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    if isinstance(manifest, dict):
        manifest = manifest.get("icons", [])
    if not isinstance(manifest, list):
        raise SystemExit("Manifest must be a list or an object with an 'icons' list.")

    out = Path(args.out)
    svg_dir = out / "svg"
    png_dir = out / "png"
    svg_dir.mkdir(parents=True, exist_ok=True)
    if args.png:
        png_dir.mkdir(parents=True, exist_ok=True)

    rendered = []
    for item in manifest:
        icon = item["icon"]
        name = safe_name(item.get("name") or icon)
        color = item.get("color", "#0057C8")
        svg_path = svg_dir / f"{name}.svg"
        svg_path.write_text(load_svg(icon, color, Path(args.lucide_dir) if args.lucide_dir else None), encoding="utf-8")
        row = {"name": name, "icon": icon, "svg": str(svg_path)}
        if args.png:
            png_path = png_dir / f"{name}.png"
            render_png(svg_path, png_path, args.size, Path(args.node_bin) if args.node_bin else None, Path(args.node_modules) if args.node_modules else None)
            row["png"] = str(png_path)
        rendered.append(row)
        print(f"{name}\t{icon}\t{color}")

    (out / "rendered_manifest.json").write_text(json.dumps(rendered, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"rendered: {len(rendered)}")


if __name__ == "__main__":
    main()
