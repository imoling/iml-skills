#!/usr/bin/env python3
"""Draft connector strategy for PPT page design patterns."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PATTERN_RULES = {
    "hero + satellites": {
        "connector_required": "optional",
        "type": "relation_field_edge_rails",
        "layer": "between relation field and cards; behind card/text layers",
        "anchor_logic": "satellite_card.inner_edge -> central_relation_field.boundary",
        "line_style": "short thin solid rails; no arrowheads for membership/association",
        "angle_rule": "if using diagonal spokes, keep shallow mirrored slopes; bottom spokes must not be visibly steeper than top spokes",
        "avoid": [
            "long diagonals across page",
            "lines crossing center text",
            "lines entering satellite card body text",
            "lines visually originating from inside the central text/icon card",
            "inconsistent spoke angles",
        ],
        "fallback": "use clean short radial spokes only when the layout is open; otherwise rely on relation field and spatial grouping",
    },
    "step progression": {
        "connector_required": "yes",
        "type": "short_arrow_or_path_lane",
        "layer": "between cards, never over text",
        "anchor_logic": "step_card.right_edge -> next_card.left_edge, or path lane outside cards",
        "line_style": "solid arrow, consistent length; no slash separators",
        "avoid": [
            "diagonal slash marks",
            "arrows crossing card interiors",
            "long trend line through steps",
        ],
        "fallback": "use numbered badges and short arrows between cards",
    },
    "contrast pair": {
        "connector_required": "optional",
        "type": "center_axis_or_opposing_arrows",
        "layer": "center gutter",
        "anchor_logic": "left_group.inner_edge <-> right_group.inner_edge",
        "line_style": "thin divider, balance axis, or two short arrows",
        "avoid": [
            "diagonal lines across either side",
            "lines through comparison text",
        ],
        "fallback": "use a vertical divider and color contrast only",
    },
    "metric anchors": {
        "connector_required": "no",
        "type": "separator",
        "layer": "inside cards or between cards",
        "anchor_logic": "none; use dividers only",
        "line_style": "subtle separators",
        "avoid": [
            "connectors between unrelated metrics",
            "decorative arrows implying false causality",
        ],
        "fallback": "no connectors",
    },
    "group headers": {
        "connector_required": "no",
        "type": "table_grid",
        "layer": "table/grid layer",
        "anchor_logic": "grid lines define structure",
        "line_style": "consistent row/column grid",
        "avoid": [
            "freeform connectors inside dense tables",
            "icons or arrows in every small cell",
        ],
        "fallback": "header bands and table grid only",
    },
    "sparse accent": {
        "connector_required": "no",
        "type": "divider",
        "layer": "inside conclusion band if needed",
        "anchor_logic": "none",
        "line_style": "short divider only",
        "avoid": [
            "multi-line connector systems",
            "decorative route lines",
        ],
        "fallback": "typographic emphasis only",
    },
}


ALIASES = {
    "hero_satellites": "hero + satellites",
    "hero": "hero + satellites",
    "step_progression": "step progression",
    "step": "step progression",
    "contrast_pair": "contrast pair",
    "contrast": "contrast pair",
    "metric_anchors": "metric anchors",
    "metric": "metric anchors",
    "group_headers": "group headers",
    "group": "group headers",
    "sparse_accent": "sparse accent",
    "sparse": "sparse accent",
}


def normalize_pattern(value: str) -> str:
    key = value.strip().lower().replace("_", " ")
    key = ALIASES.get(key.replace(" ", "_"), key)
    if key not in PATTERN_RULES:
        raise SystemExit(f"Unknown pattern: {value}. Expected one of: {', '.join(PATTERN_RULES)}")
    return key


def build_strategy(pattern: str, modules: list[str]) -> dict:
    key = normalize_pattern(pattern)
    rule = PATTERN_RULES[key]
    connectors = []
    if key == "hero + satellites" and len(modules) > 1:
        for module in modules[1:]:
            connectors.append({
                "purpose": "归属关系",
                "type": "short_edge_rail",
                "from_anchor": f"{module}.inner_edge",
                "to_anchor": f"{modules[0]}_relation_field.boundary",
                "layer": rule["layer"],
                "avoid": "body_text, icons, key_numbers, central_card_interior",
            })
    elif key == "step progression" and len(modules) > 1:
        for i in range(len(modules) - 1):
            connectors.append({
                "purpose": "流程方向",
                "type": "short_arrow",
                "from_anchor": f"{modules[i]}.right_edge",
                "to_anchor": f"{modules[i + 1]}.left_edge",
                "layer": rule["layer"],
                "avoid": "card_interiors, body_text",
            })
    elif key == "contrast pair" and len(modules) >= 2:
        connectors.append({
            "purpose": "对比轴",
            "type": "center_axis",
            "from_anchor": "top_gutter",
            "to_anchor": "bottom_gutter",
            "layer": rule["layer"],
            "avoid": "comparison_text",
        })
    return {
        "pattern": key,
        "connector_required": rule["connector_required"],
        "recommended_type": rule["type"],
        "anchor_logic": rule["anchor_logic"],
        "layer": rule["layer"],
        "line_style": rule["line_style"],
        "angle_rule": rule.get("angle_rule", ""),
        "avoid": rule["avoid"],
        "fallback": rule["fallback"],
        "connector_manifest": connectors,
        "qa": [
            "线条是否表达了明确关系",
            "线条是否只连接对象边缘而不是正文区域",
            "是否存在可删除的装饰线",
            "是否有斜线穿越多个模块",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Draft connector strategy for PPT layout.")
    parser.add_argument("--pattern", required=True, help="Page design pattern.")
    parser.add_argument("--modules", default="", help="Modules separated by |. First one is center for Hero + satellites.")
    parser.add_argument("--out", default="", help="Optional JSON output path.")
    args = parser.parse_args()

    modules = [m.strip() for m in args.modules.split("|") if m.strip()]
    strategy = build_strategy(args.pattern, modules)
    text = json.dumps(strategy, ensure_ascii=False, indent=2)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
