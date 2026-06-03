#!/usr/bin/env python3
"""Extract and optionally render a lucide icon.

The script reads the local lucide ESM icon definition, writes a standalone SVG,
and can render a transparent PNG through Node + sharp when available.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path

from runtime_paths import DEFAULT_LUCIDE, resolve_lucide_dir, resolve_node_bin, resolve_node_modules


def lucide_svg(icon: str, color: str, lucide_dir: Path | None = None) -> str:
    lucide_dir = resolve_lucide_dir(lucide_dir)
    js_path = lucide_dir / f"{icon}.js"
    if not js_path.exists():
        raise FileNotFoundError(f"lucide icon not found: {js_path}")
    js = js_path.read_text(encoding="utf-8")
    entries = re.findall(r'\[\s*"([a-zA-Z]+)"\s*,\s*\{([^}]*)\}\s*\]', js, re.S)
    if not entries:
        raise ValueError(f"cannot parse lucide icon: {icon}")

    parts: list[str] = []
    for tag, attrs_blob in entries:
        attrs = {}
        for key, quoted, numeric in re.findall(r'([a-zA-Z:-]+):\s*(?:"([^"]*)"|([0-9.]+))', attrs_blob):
            attrs[key] = quoted or numeric
        fixed = []
        for key, value in attrs.items():
            fixed.append(f'{key}="{value}"')
        parts.append(f"<{tag} {' '.join(fixed)} />")

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round">{"".join(parts)}</svg>'
    )


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Write lucide SVG and optional PNG.")
    parser.add_argument("icon", help="lucide icon name, e.g. target or bot")
    parser.add_argument("--color", default="#0057C8", help="Icon stroke color.")
    parser.add_argument("--out", required=True, help="Output path without extension or SVG path.")
    parser.add_argument("--png", action="store_true", help="Also render PNG with sharp.")
    parser.add_argument("--size", type=int, default=512, help="PNG size in pixels.")
    parser.add_argument("--lucide-dir", default="", help="Lucide ESM icon directory. Defaults to IML_PPTX_LUCIDE_DIR or Codex runtime.")
    parser.add_argument("--node-bin", default="", help="Node executable for PNG rendering. Defaults to IML_PPTX_NODE_BIN or Codex runtime.")
    parser.add_argument("--node-modules", default="", help="node_modules directory containing sharp. Defaults to IML_PPTX_NODE_MODULES or Codex runtime.")
    args = parser.parse_args()

    out = Path(args.out)
    svg_path = out if out.suffix.lower() == ".svg" else out.with_suffix(".svg")
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(lucide_svg(args.icon, args.color, Path(args.lucide_dir) if args.lucide_dir else None), encoding="utf-8")
    print(svg_path)

    if args.png:
        png_path = svg_path.with_suffix(".png")
        render_png(svg_path, png_path, args.size, Path(args.node_bin) if args.node_bin else None, Path(args.node_modules) if args.node_modules else None)
        print(png_path)


if __name__ == "__main__":
    main()
