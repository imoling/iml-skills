#!/usr/bin/env python3
"""Build offline icon resources for iml-pptx.

This creates:
- resources/icons/index.json: all available lucide icons with simple tokens.
- resources/icons/semantic_packs.json: curated business/PPT semantic packs.
- resources/icons/svg/*.svg: offline SVG assets for curated semantic packs.

The goal is richer icon selection without pre-rendering thousands of PNG files.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from runtime_paths import DEFAULT_LUCIDE, resolve_lucide_dir


SKILL_DIR = Path(__file__).resolve().parents[1]
RESOURCE_DIR = SKILL_DIR / "resources" / "icons"
SVG_DIR = RESOURCE_DIR / "svg"

SEMANTIC_PACKS = {
    "ai": [
        "bot", "brain-circuit", "brain", "cpu", "sparkles", "route", "workflow",
        "network", "blocks", "messages-square", "scan-eye", "wand-sparkles",
        "circuit-board", "microchip", "square-function", "message-circle-code",
    ],
    "tool": [
        "plug", "cable", "code-xml", "terminal", "wrench", "hammer", "package",
        "puzzle", "settings", "square-function", "webhook", "braces", "file-code",
        "git-pull-request", "command", "monitor-cog",
    ],
    "data": [
        "database", "files", "file-text", "book-open", "library", "table",
        "folder-search", "chart-network", "hard-drive", "server-cog", "file-stack",
        "notebook-tabs", "scroll-text", "archive", "server",
    ],
    "workflow": [
        "workflow", "git-branch", "route", "split", "merge", "shuffle",
        "repeat", "list-check", "arrow-right-left", "waypoints", "milestone",
        "git-fork", "list-tree", "combine", "refresh-cw",
    ],
    "governance": [
        "shield-check", "lock-keyhole", "scale", "badge-check", "file-lock",
        "landmark", "scan-eye", "clipboard-check", "book-check", "key-round",
        "fingerprint-pattern", "file-badge", "file-check", "shield-user",
    ],
    "risk": [
        "triangle-alert", "circle-x", "shield-alert", "bug", "siren",
        "octagon-alert", "badge-alert", "file-exclamation-point", "circle-alert",
        "shield-x", "bell-ring", "ban", "message-circle-warning",
    ],
    "market": [
        "coins", "badge-dollar-sign", "tag", "chart-no-axes-column-increasing",
        "chart-no-axes-column-decreasing", "receipt", "trending-up", "globe",
        "chart-pie", "chart-spline", "banknote", "wallet", "hand-coins",
    ],
    "people": [
        "users", "user-round-cog", "contact", "id-card", "handshake",
        "building-2", "briefcase-business", "user-check", "presentation",
        "user-round-check", "users-round", "contact-round", "user-check",
    ],
    "ecosystem": [
        "network", "share-2", "layers", "boxes", "blocks", "component",
        "waypoints", "combine", "gallery-horizontal-end", "puzzle", "plug",
        "git-merge", "network", "share",
    ],
    "industry": [
        "factory", "hospital", "school", "truck", "train-front", "ship",
        "utility-pole", "fuel", "hard-hat", "building-2", "warehouse",
        "landmark", "drill", "construction",
    ],
    "quality": [
        "clipboard-check", "list-checks", "gauge", "ruler", "microscope",
        "scan-search", "badge-check", "circle-check-big", "file-check",
        "chart-no-axes-combined", "activity", "radar",
    ],
    "time": [
        "clock", "history", "calendar-days", "refresh-cw", "rotate-cw",
        "milestone", "timer", "calendar-clock", "hourglass", "calendar-check",
    ],
    "communication": [
        "message-square", "messages-square", "message-circle", "send",
        "mail", "phone", "headset", "radio", "rss", "megaphone",
    ],
    "cloud_saas": [
        "cloud", "cloud-cog", "server", "server-cog", "database", "globe",
        "panel-top", "monitor", "laptop", "router", "satellite-dish",
    ],
}


def available_icons(lucide_dir: Path) -> list[str]:
    return sorted(p.stem for p in lucide_dir.glob("*.js") if not p.name.endswith(".map"))


def lucide_svg(icon: str, color: str = "#0057C8", lucide_dir: Path | None = None) -> str:
    lucide_dir = resolve_lucide_dir(lucide_dir)
    js_path = lucide_dir / f"{icon}.js"
    if not js_path.exists():
        raise FileNotFoundError(f"lucide icon not found: {js_path}")
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


def tokens_for(icon: str) -> list[str]:
    return [part for part in icon.replace("_", "-").split("-") if part]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build offline lucide icon resources for iml-pptx.")
    parser.add_argument("--lucide-dir", default="", help="Lucide ESM icon directory. Defaults to IML_PPTX_LUCIDE_DIR or Codex runtime.")
    args = parser.parse_args()
    lucide_dir = resolve_lucide_dir(args.lucide_dir or None)

    RESOURCE_DIR.mkdir(parents=True, exist_ok=True)
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    icons = available_icons(lucide_dir)
    icon_set = set(icons)

    packs = {
        domain: [icon for icon in icon_list if icon in icon_set]
        for domain, icon_list in SEMANTIC_PACKS.items()
    }
    missing = {
        domain: [icon for icon in icon_list if icon not in icon_set]
        for domain, icon_list in SEMANTIC_PACKS.items()
    }
    missing = {k: v for k, v in missing.items() if v}

    source_meta = {
        "source": "lucide-esm-icons",
        "source_kind": "runtime_or_override",
        "source_hint": "Use IML_PPTX_LUCIDE_DIR or --lucide-dir to override the lucide icon directory.",
    }

    (RESOURCE_DIR / "semantic_packs.json").write_text(
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                **source_meta,
                "packs": packs,
                "missing": missing,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    reverse_domains: dict[str, list[str]] = {}
    for domain, icon_list in packs.items():
        for icon in icon_list:
            reverse_domains.setdefault(icon, []).append(domain)

    index = [
        {
            "name": icon,
            "tokens": tokens_for(icon),
            "domains": reverse_domains.get(icon, []),
            "resource_svg": icon in reverse_domains,
        }
        for icon in icons
    ]
    (RESOURCE_DIR / "index.json").write_text(
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                **source_meta,
                "count": len(index),
                "icons": index,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    curated_icons = sorted(reverse_domains)
    for icon in curated_icons:
        (SVG_DIR / f"{icon}.svg").write_text(lucide_svg(icon, lucide_dir=lucide_dir), encoding="utf-8")

    print(f"icons indexed: {len(index)}")
    print(f"semantic packs: {len(packs)}")
    print(f"curated svg assets: {len(curated_icons)}")
    if missing:
        print("missing curated icons:", missing)


if __name__ == "__main__":
    main()
