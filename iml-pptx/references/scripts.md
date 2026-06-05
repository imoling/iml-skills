# Scripts

Invoke Python scripts with `python3`. Prefer running examples from the skill root directory so relative paths resolve cleanly.

Runtime path overrides for icon rendering/indexing:

- `IML_PPTX_LUCIDE_DIR`: lucide ESM icon directory.
- `IML_PPTX_NODE_BIN`: Node executable used for PNG rendering.
- `IML_PPTX_NODE_MODULES`: node_modules directory containing `sharp`.

The scripts default to the Codex bundled runtime under `~/.cache/codex-runtimes/...` when these variables are not set.


## `scripts/smoke_test.py`

Run a non-destructive smoke test for the skill scripts. It validates SKILL.md frontmatter and exercises brief generation, icon search, icon narrative, connector narrative, single icon rendering and manifest rendering in a temporary directory.

```bash
python3 scripts/smoke_test.py
```

## `scripts/start_brief.py`

Create a production brief template.

```bash
python3 scripts/start_brief.py --topic "央国企AI培训" --audience "央企数科公司管理者" --mode full --style "白底科技蓝商务培训"
```

## `scripts/icon_picker.py`

Search offline icon resources first, then local lucide icons. Use before choosing icons.

```bash
python3 scripts/icon_picker.py "治理 风险 合规"
python3 scripts/icon_picker.py "agent workflow tools"
python3 scripts/icon_picker.py --list-domain ai
python3 scripts/icon_picker.py "治理 风险" --lucide-dir "$IML_PPTX_LUCIDE_DIR"
```

## `scripts/icon_narrative.py`

Draft a page-level icon narrative and PPT design pattern plan.

```bash
python3 scripts/icon_narrative.py --page-type 流程页 --title "AI应用演进路线" --modules "对话助手|知识增强|流程智能体|AI原生运营"
```

## `scripts/connector_narrative.py`

Draft connector strategy from page design pattern and module count.

```bash
python3 scripts/connector_narrative.py --pattern "Hero + satellites" --modules "中心|模型底座|工具生态|治理审计|业务接入|数字员工"
```

If output says `connector_required=false`, do not add decorative lines.

## `scripts/render_lucide_icon.py`

Render one lucide icon to SVG and optionally PNG.

```bash
python3 scripts/render_lucide_icon.py target --color "#0057C8" --out icons/target --png
python3 scripts/render_lucide_icon.py target --out icons/target --png --node-bin "$IML_PPTX_NODE_BIN" --node-modules "$IML_PPTX_NODE_MODULES"
```

## `scripts/render_icon_manifest.py`

Render a manifest into colored SVG/PNG assets.

```json
[
  {"name": "risk", "role": "contrast_right", "semantic": "风险提示", "icon": "triangle-alert", "color": "#E65100"},
  {"name": "governance", "role": "contrast_left", "semantic": "治理合规", "icon": "shield-check", "color": "#0057C8"}
]
```

```bash
python3 scripts/render_icon_manifest.py icon_manifest.json --out page_icons --png
python3 scripts/render_icon_manifest.py icon_manifest.json --out page_icons --png --lucide-dir "$IML_PPTX_LUCIDE_DIR"
```

The PPT build script should insert `page_icons/png/<name>.png`.

## `scripts/build_icon_resources.py`

Rebuild offline icon resources under `resources/icons/` after changing semantic packs or updating lucide.

```bash
python3 scripts/build_icon_resources.py
python3 scripts/build_icon_resources.py --lucide-dir "$IML_PPTX_LUCIDE_DIR"
```

Do not pre-render all icons to PNG by default.

## `scripts/ppt_replicate_helpers.py`

Shared OOXML helpers for simple editable PPT builders: slide sizing, `PingFang SC` text runs, text boxes, rounded cards, lines, ovals, pictures and relationship XML. This is an importable helper module, not a command-line script; use it from a page/deck builder script instead of running it directly.

## `scripts/layout_guard.py`

Heuristic overlap preflight. Not a visual preview substitute.

```bash
python3 scripts/layout_guard.py output/page02.pptx --min-area-ratio 0.08
```

Use `--include-containers` only when debugging labels/badges colliding with card containers.

## `scripts/text_fit_guard.py`

Heuristic text-density preflight. It estimates whether editable text is likely too dense for its text box. It does not understand the intended parent card, so screenshot QA is still mandatory.

```bash
python3 scripts/text_fit_guard.py output/deck.pptx
python3 scripts/text_fit_guard.py output/deck.pptx --threshold 0.85
```

Repair warnings by shortening copy, adding line breaks, increasing card height, widening the text box inside the card, or reducing font size slightly.

## `scripts/connector_guard.py`

Scan PPTX line shapes for likely accidental diagonal or unstable connector lines.

```bash
python3 scripts/connector_guard.py deck.pptx
python3 scripts/connector_guard.py deck.pptx --allow-slide 2
```

If it reports negative extents, fix PPT code regardless of whether the diagonal is intentional. Use positive `w/h` plus `flipH`/`flipV`.

## `scripts/preview_pptx.sh`

Create Quick Look preview PNGs for visual QA.

```bash
scripts/preview_pptx.sh output/page01.pptx preview/page01
```

Always preview before reporting a replicated slide as complete.
