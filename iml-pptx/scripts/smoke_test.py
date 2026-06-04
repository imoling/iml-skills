#!/usr/bin/env python3
"""Smoke test the iml-pptx skill scripts without modifying skill outputs."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(args))
    result = subprocess.run(args, cwd=SKILL_DIR, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    if result.returncode != 0:
        raise SystemExit(result.returncode)
    return result


def validate_skill_file() -> None:
    skill = SKILL_DIR / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit("SKILL.md missing YAML frontmatter")
    frontmatter = text.split("---", 2)[1]
    if "name: iml-pptx" not in frontmatter or "description:" not in frontmatter:
        raise SystemExit("SKILL.md frontmatter missing name or description")
    print("skill frontmatter: ok")


def main() -> None:
    validate_skill_file()
    py = "python3"

    run([py, "scripts/start_brief.py", "--topic", "企业AI培训", "--audience", "管理者", "--mode", "prompt"])
    run([py, "scripts/icon_picker.py", "治理 风险 合规"])
    run([py, "scripts/icon_narrative.py", "--page-type", "流程页", "--title", "AI应用演进路线", "--modules", "对话助手|知识增强|流程智能体|AI原生运营"])
    run([py, "scripts/connector_narrative.py", "--pattern", "Hero + satellites", "--modules", "中心|模型底座|工具生态|治理审计"])

    with tempfile.TemporaryDirectory(prefix="iml-pptx-smoke-") as tmp:
        tmp_path = Path(tmp)
        run([py, "scripts/render_lucide_icon.py", "target", "--color", "#0057C8", "--out", str(tmp_path / "target"), "--png"])

        manifest = tmp_path / "manifest.json"
        manifest.write_text(
            json.dumps(
                [
                    {"name": "risk", "role": "contrast_right", "semantic": "风险提示", "icon": "triangle-alert", "color": "#E65100"},
                    {"name": "governance", "role": "contrast_left", "semantic": "治理合规", "icon": "shield-check", "color": "#0057C8"},
                ],
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        run([py, "scripts/render_icon_manifest.py", str(manifest), "--out", str(tmp_path / "manifest_out"), "--png"])

        expected = [tmp_path / "target.png", tmp_path / "manifest_out" / "png" / "risk.png", tmp_path / "manifest_out" / "png" / "governance.png"]
        missing = [str(path) for path in expected if not path.exists()]
        if missing:
            raise SystemExit("missing smoke outputs: " + ", ".join(missing))

    print("smoke test: ok")


if __name__ == "__main__":
    main()
