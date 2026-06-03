#!/usr/bin/env python3
"""Create a concise PPT production brief for this skill.

The brief is intentionally lightweight: it forces theme, audience, style,
editable boundaries and confirmation checkpoints to be named before making
prompts, images or editable PPT slides.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def build_brief(args: argparse.Namespace) -> str:
    style = args.style or "白底、深灰文字、科技蓝主色、商务培训信息图风格"
    font = args.font or "PingFang SC / 苹果苹方"
    icon_strategy = args.icon_strategy or "优先使用清晰图标库资产；小logo可用高清图片资产；避免低清截图裁切"
    editable = args.editable or "文字、框体、线条、表格、箭头和主要图形可编辑；图标/logo可为图片资产"
    confirm = args.confirm or "复杂任务先做第一页/第一张确认，再继续后续页面"
    rhythm = args.rhythm or "统一风格但页面节奏变化，按内容选择总览、对比、流程、数据、案例、总结等版式"

    return f"""制作简报
- 主题：{args.topic or "待补充"}
- 受众：{args.audience or "待补充"}
- 交付模式：{args.mode}
- 样式主题：{style}
- 页面节奏：{rhythm}
- 图标/logo策略：{icon_strategy}
- 字体：{font}
- 来源约束：{args.source or "待补充：PDF / 图片 / 截图 / 用户内容 / 品牌素材"}
- 可编辑边界：{editable}
- 首个确认页：{confirm}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a PPT production brief.")
    parser.add_argument("--topic", default="", help="Deck or page topic.")
    parser.add_argument("--audience", default="", help="Target audience.")
    parser.add_argument("--mode", default="full", choices=["prompt", "image", "editable-ppt", "full"], help="Production mode.")
    parser.add_argument("--style", default="", help="Visual style theme.")
    parser.add_argument("--rhythm", default="", help="Page rhythm / density guidance.")
    parser.add_argument("--source", default="", help="Source constraints.")
    parser.add_argument("--font", default="", help="Font rule.")
    parser.add_argument("--icon-strategy", default="", help="Icon/logo strategy.")
    parser.add_argument("--editable", default="", help="Editable boundary.")
    parser.add_argument("--confirm", default="", help="First confirmation checkpoint.")
    parser.add_argument("--out", default="", help="Optional output markdown path.")
    args = parser.parse_args()

    text = build_brief(args)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
