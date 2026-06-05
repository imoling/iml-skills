#!/usr/bin/env python3
"""Draft a page-level icon narrative plan for PPT pages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent

PATTERN_BY_PAGE_TYPE = {
    "总览页": "hero_satellites",
    "概念页": "hero_satellites",
    "流程页": "step_progression",
    "方法论页": "step_progression",
    "对比页": "contrast_pair",
    "问题页": "contrast_pair",
    "数据页": "metric_anchors",
    "案例页": "group_headers",
    "场景页": "group_headers",
    "总结页": "sparse_accent",
}

PATTERN_DESC = {
    "hero_satellites": "一个中心主图标表达页面核心判断，周围模块使用小图标辅助解释。",
    "step_progression": "每个步骤使用同一风格但语义递进的图标，形成从左到右/从上到下的演进。",
    "contrast_pair": "左右两侧或正反两组使用相反语义图标，强调机会与风险、旧路与新路等对照。",
    "metric_anchors": "只给关键数字/指标卡配置图标，减少装饰感，突出证据。",
    "group_headers": "图标放在分组标题或大类入口，不机械填满每个小格。",
    "sparse_accent": "只在结论、提醒或行动建议处放一两个高辨识图标。",
}

DESIGN_PATTERN = {
    "hero_satellites": {
        "display": "Hero + satellites",
        "best_for": "总览页、框架图、概念页",
        "layout": "中心主节点/主卡片承载页面核心判断，周围用3-6个卫星模块环绕；可用径向、四象限或hub-and-spoke。",
        "icon_hierarchy": "中心主图标最大；卫星图标更小、更轻；连接线服务关系而非装饰。",
        "editable_objects": ["central_node", "satellite_cards", "connector_lines", "module_labels"],
        "avoid": "不要做成等权重卡片网格，否则主图标失去意义。",
    },
    "step_progression": {
        "display": "Step progression",
        "best_for": "流程页、演进路线、路线图、成熟度阶梯",
        "layout": "水平/垂直路径、时间线、阶梯、泳道或上升路线；每一步是图标+标题+简短说明。",
        "icon_hierarchy": "所有步骤图标同风格但语义递进；编号和箭头承担顺序关系。",
        "editable_objects": ["path_line", "step_cards", "number_badges", "arrows", "captions"],
        "avoid": "不要做成彼此断开的卡片，必须有可见进展方向。",
    },
    "contrast_pair": {
        "display": "Contrast pair",
        "best_for": "对比页、取舍页、机会/风险、旧路/新路、控制/灵活",
        "layout": "左右分屏、上下分屏、镜像卡片、天平或中轴对照；两侧空间和层级保持均衡。",
        "icon_hierarchy": "左右图标语义相反，颜色可形成对照，例如蓝色机会、橙色风险。",
        "editable_objects": ["split_bands", "comparison_cards", "center_axis", "side_labels"],
        "avoid": "不要两侧使用相似图标，否则对比关系会变弱。",
    },
    "metric_anchors": {
        "display": "Metric anchors",
        "best_for": "数据页、市场规模、KPI、证据页",
        "layout": "大数字卡片为主，图标作为指标类型锚点；来源脚注保持轻量。",
        "icon_hierarchy": "图标辅助数字，不抢数字；不同指标使用不同语义图标。",
        "editable_objects": ["metric_cards", "number_text", "unit_labels", "source_notes", "separators"],
        "avoid": "不要过度图标化密集数据，图标不能和数字抢视觉焦点。",
    },
    "group_headers": {
        "display": "Group headers",
        "best_for": "密集表格、能力地图、矩阵、分类体系",
        "layout": "图标放在行标题、列标题或分组标题；子项以清晰文字和网格承载。",
        "icon_hierarchy": "图标用于分类，不进入每个小单元格。",
        "editable_objects": ["table_grid", "header_bands", "row_labels", "section_cards", "cell_text"],
        "avoid": "不要每个小格都放图标，会造成噪音和错位。",
    },
    "sparse_accent": {
        "display": "Sparse accent",
        "best_for": "总结页、建议页、提醒页、收尾判断",
        "layout": "一个强结论条/结论卡为主体，配1-2个强调图标，其余靠排版完成。",
        "icon_hierarchy": "强调图标只服务决策或提醒，不重复解释所有内容。",
        "editable_objects": ["conclusion_band", "emphasis_text", "divider", "supporting_note"],
        "avoid": "不要把总结页塞成多图标卡片页。",
    },
}

ROLE_CANDIDATES = {
    "ai": ["bot", "brain-circuit", "cpu", "sparkles"],
    "agent": ["bot", "workflow", "route", "network"],
    "workflow": ["workflow", "route", "git-branch", "waypoints"],
    "data": ["database", "book-open", "library", "files"],
    "knowledge": ["book-open", "library", "file-text", "database"],
    "risk": ["triangle-alert", "shield-alert", "circle-alert", "bug"],
    "governance": ["shield-check", "scale", "file-lock", "badge-check"],
    "market": ["chart-no-axes-column-increasing", "coins", "globe", "tag"],
    "cost": ["coins", "tag", "receipt", "chart-no-axes-column-decreasing"],
    "people": ["users", "user-round-cog", "handshake", "contact"],
    "platform": ["layers", "server-cog", "blocks", "network"],
    "tool": ["plug", "wrench", "code-xml", "package"],
    "time": ["clock", "history", "calendar-days", "refresh-cw"],
    "quality": ["clipboard-check", "gauge", "scan-search", "badge-check"],
    "industry": ["factory", "building-2", "hard-hat", "landmark"],
}

ZH_HINTS = {
    "智能体": "agent",
    "智能": "ai",
    "AI": "ai",
    "流程": "workflow",
    "编排": "workflow",
    "数据": "data",
    "知识": "knowledge",
    "风险": "risk",
    "问题": "risk",
    "治理": "governance",
    "合规": "governance",
    "市场": "market",
    "规模": "market",
    "成本": "cost",
    "支出": "cost",
    "收益": "market",
    "活跃": "people",
    "人员": "people",
    "组织": "people",
    "平台": "platform",
    "生态": "platform",
    "工具": "tool",
    "插件": "tool",
    "时间": "time",
    "演进": "time",
    "评测": "quality",
    "质量": "quality",
    "行业": "industry",
    "场景": "industry",
}


def infer_domain(text: str) -> str:
    for hint, domain in ZH_HINTS.items():
        if hint in text:
            return domain
    lower = text.lower()
    for domain in ROLE_CANDIDATES:
        if domain in lower:
            return domain
    return "ai"


def choose_pattern(page_type: str, module_count: int) -> str:
    pattern = PATTERN_BY_PAGE_TYPE.get(page_type, "hero_satellites")
    if module_count >= 6 and pattern == "hero_satellites":
        return "group_headers"
    return pattern


def role_for(pattern: str, index: int, total: int) -> str:
    if pattern == "hero_satellites":
        return "hero" if index == 0 else f"satellite_{index}"
    if pattern == "step_progression":
        return f"step_{index + 1}"
    if pattern == "contrast_pair":
        if total <= 2:
            return "contrast_left" if index == 0 else "contrast_right"
        return f"contrast_item_{index + 1}"
    if pattern == "metric_anchors":
        return f"metric_anchor_{index + 1}"
    if pattern == "group_headers":
        return f"group_header_{index + 1}"
    return f"accent_{index + 1}"


def build_plan(page_type: str, title: str, modules: list[str], color: str, accent: str) -> dict:
    pattern = choose_pattern(page_type, len(modules))
    design = DESIGN_PATTERN[pattern]
    icons = []
    for i, module in enumerate(modules):
        domain = infer_domain(module)
        candidates = ROLE_CANDIDATES.get(domain, ROLE_CANDIDATES["ai"])
        icon = candidates[min(i, len(candidates) - 1)]
        icons.append(
            {
                "name": f"icon_{i + 1}",
                "role": role_for(pattern, i, len(modules)),
                "semantic": module,
                "domain": domain,
                "icon": icon,
                "color": accent if pattern == "contrast_pair" and ("风险" in module or "问题" in module or i == 1) else color,
                "reason": f"{module} maps to {domain}; pattern={pattern}",
            }
        )
    return {
        "title": title,
        "page_type": page_type,
        "narrative_pattern": pattern,
        "pattern_description": PATTERN_DESC[pattern],
        "page_design_pattern": design["display"],
        "design_decision": {
            "best_for": design["best_for"],
            "layout_skeleton": design["layout"],
            "icon_hierarchy": design["icon_hierarchy"],
            "editable_objects": design["editable_objects"],
            "avoid": design["avoid"],
        },
        "icons": icons,
        "review_rules": [
            "图标是否解释了页面逻辑，而不是只装饰卡片",
            "页面构图是否符合所选设计模式",
            "主图标与辅助图标是否有大小/位置层级",
            "同一页图标是否过度重复",
            "图标是否与标题、流程、对比或数据证据形成关系",
            "可编辑对象是否覆盖该模式的核心结构",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Draft icon narrative plan.")
    parser.add_argument("--page-type", default="总览页", help="Chinese page type.")
    parser.add_argument("--title", default="", help="Slide title.")
    parser.add_argument("--modules", required=True, help="Modules separated by |.")
    parser.add_argument("--color", default="#0057C8", help="Primary icon color.")
    parser.add_argument("--accent", default="#E65100", help="Contrast/risk accent color.")
    parser.add_argument("--out", default="", help="Optional JSON output path.")
    args = parser.parse_args()

    modules = [m.strip() for m in args.modules.split("|") if m.strip()]
    if not modules:
        raise SystemExit("No modules provided.")
    plan = build_plan(args.page_type, args.title, modules, args.color, args.accent)
    text = json.dumps(plan, ensure_ascii=False, indent=2)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
