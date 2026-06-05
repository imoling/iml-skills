#!/usr/bin/env python3
"""Search and recommend local lucide icons for PPT semantics."""

from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path

from runtime_paths import DEFAULT_LUCIDE, resolve_lucide_dir


SKILL_DIR = Path(__file__).resolve().parents[1]
RESOURCE_DIR = SKILL_DIR / "resources" / "icons"
RESOURCE_INDEX = RESOURCE_DIR / "index.json"
RESOURCE_PACKS = RESOURCE_DIR / "semantic_packs.json"

DOMAIN_MAP = {
    "ai": [
        "bot", "brain-circuit", "brain", "cpu", "sparkles", "route", "workflow",
        "network", "blocks", "messages-square", "scan-eye", "wand-sparkles",
    ],
    "tool": [
        "plug", "cable", "code-xml", "terminal", "wrench", "hammer", "package",
        "puzzle", "settings", "square-function", "webhook",
    ],
    "data": [
        "database", "files", "file-text", "book-open", "library", "table",
        "folder-search", "chart-network", "hard-drive", "server-cog",
    ],
    "workflow": [
        "workflow", "git-branch", "route", "split", "merge", "shuffle",
        "repeat", "list-check", "arrow-right-left", "waypoints",
    ],
    "governance": [
        "shield-check", "lock-keyhole", "scale", "badge-check", "file-lock",
        "landmark", "scan-eye", "clipboard-check", "book-check",
    ],
    "risk": [
        "triangle-alert", "circle-x", "shield-alert", "bug", "siren",
        "octagon-alert", "badge-alert", "file-warning", "circle-alert",
    ],
    "market": [
        "coins", "badge-dollar-sign", "tag", "chart-no-axes-column-increasing",
        "chart-no-axes-column-decreasing", "receipt", "trending-up", "globe",
    ],
    "people": [
        "users", "user-round-cog", "contact", "id-card", "handshake",
        "building-2", "briefcase-business", "user-check", "presentation",
    ],
    "ecosystem": [
        "network", "share-2", "layers", "boxes", "blocks", "component",
        "waypoints", "combine", "gallery-horizontal-end",
    ],
    "industry": [
        "factory", "hospital", "school", "truck", "train-front", "ship",
        "utility-pole", "fuel", "hard-hat", "building-2",
    ],
    "quality": [
        "clipboard-check", "list-checks", "gauge", "ruler", "microscope",
        "scan-search", "badge-check", "circle-check-big",
    ],
    "time": [
        "clock", "history", "calendar-days", "refresh-cw", "rotate-cw",
        "milestones", "timer", "calendar-clock",
    ],
}

ZH_HINTS = {
    "智能": "ai",
    "智能体": "ai",
    "工具": "tool",
    "插件": "tool",
    "数据": "data",
    "知识": "data",
    "流程": "workflow",
    "编排": "workflow",
    "治理": "governance",
    "合规": "governance",
    "安全": "governance",
    "风险": "risk",
    "问题": "risk",
    "成本": "market",
    "收益": "market",
    "市场": "market",
    "人员": "people",
    "组织": "people",
    "运营": "people",
    "生态": "ecosystem",
    "平台": "ecosystem",
    "集成": "ecosystem",
    "行业": "industry",
    "场景": "industry",
    "评测": "quality",
    "质量": "quality",
    "时间": "time",
    "演进": "time",
}


def available_icons(lucide_dir: Path) -> list[str]:
    if RESOURCE_INDEX.exists():
        data = json.loads(RESOURCE_INDEX.read_text(encoding="utf-8"))
        icons = data.get("icons", [])
        if icons and isinstance(icons[0], dict):
            return sorted(icon["name"] for icon in icons if "name" in icon)
        return sorted(icons)
    if not lucide_dir.exists():
        raise FileNotFoundError(f"lucide directory not found: {lucide_dir}")
    return sorted(p.stem for p in lucide_dir.glob("*.js") if not p.name.endswith(".map"))


def load_domain_map() -> dict[str, list[str]]:
    if RESOURCE_PACKS.exists():
        data = json.loads(RESOURCE_PACKS.read_text(encoding="utf-8"))
        packs = data.get("packs", data)
        if isinstance(packs, dict):
            return {k: list(v) for k, v in packs.items()}
    return DOMAIN_MAP


def normalize(text: str) -> str:
    return text.lower().replace("_", "-").replace(" ", "-")


def infer_domains(query: str) -> list[str]:
    domains: list[str] = []
    for hint, domain in ZH_HINTS.items():
        if hint in query and domain not in domains:
            domains.append(domain)
    domain_map = load_domain_map()
    for domain in domain_map:
        if domain in query.lower() and domain not in domains:
            domains.append(domain)
    return domains


def score_icons(query: str, icons: list[str], limit: int) -> list[tuple[float, str, str]]:
    q = normalize(query)
    tokens = [normalize(t) for t in query.replace("/", " ").replace(",", " ").split() if t.strip()]
    domains = infer_domains(query)
    domain_map = load_domain_map()
    preferred: set[str] = set()
    for domain in domains:
        preferred.update(domain_map.get(domain, []))

    rows: list[tuple[float, str, str]] = []
    for icon in icons:
        score = 0.0
        reason = []
        icon_norm = normalize(icon)
        if icon in preferred:
            score += 3.0
            reason.append("domain")
        for token in tokens:
            if token and token in icon_norm:
                score += 2.0
                reason.append(f"match:{token}")
        score += difflib.SequenceMatcher(None, q, icon_norm).ratio()
        if score > 0.35:
            rows.append((score, icon, ",".join(reason) or "fuzzy"))
    return sorted(rows, reverse=True)[:limit]


def main() -> None:
    parser = argparse.ArgumentParser(description="Pick richer lucide icons for PPT semantics.")
    parser.add_argument("query", nargs="*", help="Search query, Chinese or English.")
    parser.add_argument("--lucide-dir", default=str(DEFAULT_LUCIDE), help="Local lucide icon directory. Defaults to IML_PPTX_LUCIDE_DIR or Codex runtime.")
    parser.add_argument("--limit", type=int, default=24, help="Maximum candidates.")
    domain_map = load_domain_map()
    parser.add_argument("--list-domain", choices=sorted(domain_map), help="List curated icons for a semantic domain.")
    args = parser.parse_args()

    icons = available_icons(Path(args.lucide_dir))
    if args.list_domain:
        for icon in domain_map[args.list_domain]:
            marker = "" if icon in icons else " (missing)"
            svg_marker = " [svg]" if (RESOURCE_DIR / "svg" / f"{icon}.svg").exists() else ""
            print(f"{icon}{marker}{svg_marker}")
        return

    query = " ".join(args.query).strip()
    if not query:
        raise SystemExit("Provide a query or --list-domain.")

    domains = infer_domains(query)
    if domains:
        print("inferred domains:", ", ".join(domains))
    for score, icon, reason in score_icons(query, icons, args.limit):
        svg_marker = "\tresource-svg" if (RESOURCE_DIR / "svg" / f"{icon}.svg").exists() else ""
        print(f"{icon}\tscore={score:.2f}\t{reason}{svg_marker}")


if __name__ == "__main__":
    main()
