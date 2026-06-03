# Icons And Connectors

Use this reference whenever a page has multiple modules/cards/steps, semantic icons, connector lines, hub-and-spoke layouts, process arrows, route lines or dense information diagrams.

## Icon Strategy

Use offline icon resources under `resources/icons/` first, then the local lucide library. Render SVG icons to high-resolution transparent PNG before insertion if direct SVG embedding does not preview correctly.

Before building a slide, create an icon narrative plan. Icon placement should explain page logic, not decorate cards.

### Icon Narrative Patterns

- `Hero + satellites`: one central/hero icon explains the page thesis; smaller icons annotate surrounding modules. Best for overview/framework pages.
- `Step progression`: each step uses related icons that evolve left-to-right or top-to-bottom. Best for process/evolution pages.
- `Contrast pair`: opposing icon semantics on left/right or top/bottom. Best for comparison, tradeoff, opportunity/risk.
- `Metric anchors`: only key metric cards get icons. Best for data-heavy pages.
- `Group headers`: icons appear on section headers, not every sub-card. Best for dense tables or capability maps.
- `Sparse accent`: one or two icons support a recommendation, warning or closing judgment.

Choose one primary pattern per page.

Write a one-line page design decision before prompt/image/PPT production:

```text
页面设计模式：【Hero + satellites / Step progression / Contrast pair / Metric anchors / Group headers / Sparse accent】
原因：【为什么这个页面适合该模式】
图标层级：【主图标 / 辅助图标 / 分组图标 / 指标锚点 / 强调图标】
```

### Mandatory Icon Gate

- For every slide with 3 or more modules/cards/steps, create an icon manifest before building the PPT unless the source is intentionally text-only.
- The manifest must include `narrative_pattern` and `role`, not only `icon` and `color`.
- Run `python3 scripts/icon_picker.py` unless the source image contains clear exact icons to replicate.
- Use `python3 scripts/icon_narrative.py` when a page needs more than three icons or the first result feels stiff.
- Render selected icons with `python3 scripts/render_icon_manifest.py` or `python3 scripts/render_lucide_icon.py`.
- Insert rendered icon assets into the PPT; do not leave placeholder circles or empty icon areas.

### Icon Semantics Guide

- `AI/智能体`: bot, brain-circuit, cpu, sparkles, route, workflow, network, blocks.
- `工具/插件/API`: plug, cable, code-xml, terminal, wrench, package, puzzle.
- `数据/知识`: database, files, book-open, library, table, chart-network, folder-search.
- `流程/编排`: workflow, git-branch, route, split, merge, shuffle, repeat, list-check.
- `治理/安全/合规`: shield-check, lock-keyhole, scale, badge-check, file-lock, landmark, scan-eye.
- `风险/问题`: triangle-alert, circle-x, shield-alert, bug, siren, octagon-alert.
- `成本/收益/市场`: coins, badge-dollar-sign, tag, chart-no-axes-column-increasing, receipt.
- `组织/人员/运营`: users, user-round-cog, contact, id-card, handshake, building-2, briefcase-business.
- `生态/平台/集成`: network, share-2, layers, boxes, blocks, component, waypoints.
- `行业/场景`: factory, hospital, school, truck, train-front, ship, utility-pole, fuel, hard-hat.
- `评测/质量`: clipboard-check, list-checks, gauge, ruler, microscope, scan-search, badge-check.
- `时间/演进`: clock, history, calendar-days, refresh-cw, rotate-cw, milestones.

## Connector Design

Treat connectors as narrative objects. Before drawing one, answer:

```text
连接线目的：【层级关系 / 流程方向 / 归属关系 / 对比关系 / 数据趋势 / 装饰】
是否必要：【必要 / 可省略】
连接线类型：【relation field + short edge rails / straight radial spoke / orthogonal elbow / short arrow / bracket / axis / background guide】
锚点：【from object edge -> to object edge】
避让对象：【标题 / 正文 / 图标 / 数字 / 页码】
层级：【behind cards / between cards and icons / above cards】
```

### Default Connector Choices

- `Hero + satellites`: prefer a pale central relation field with short edge rails when satellite cards sit in a regular grid. Use radial spokes only when the layout is open and lines do not cross text/icons/cards. No arrowheads unless direction matters.
- `Step progression`: use short arrows between cards or a path lane above/below cards. Avoid slash separators.
- `Contrast pair`: use center divider, balance axis or short opposing arrows. Avoid diagonal lines across either side.
- `Metric anchors`: usually no connectors; use separators.
- `Group headers`: use table grid lines and header bands.
- `Sparse accent`: usually no connectors; use a subtle divider if needed.

### Connector Hard Rules

- Never route a line through body text, title, key numbers, icons or page numbers.
- Never use a foreground diagonal line across multiple cards.
- Intentional diagonal spokes should sit behind cards or between cards and icons, not on the same visual layer as text.
- Never use dashed lines unless they express weak/indirect relationship.
- Do not use connectors if spatial grouping already explains the relationship.
- Do not remove a semantic connector only because its first version looks bad; repair route, anchors, layer, arrowhead and weight first.
- Use arrowheads only for explicit direction: process, dependency or handoff.
- For hub pages, lines should terminate at the central relation field boundary or central node edge.
- In PPT code, avoid negative `cx`/`cy` or negative width/height for lines. Normalize to positive `w/h`, then use `flipH`/`flipV` if needed.
- Lines should be thinner than card borders unless they are the primary route of a process page.

## Repair Notes

When icons feel stiff:

1. Do not add more icons first.
2. Identify the page's icon narrative pattern and design pattern.
3. Remove icons that do not explain a relationship.
4. Promote one primary icon if the page needs a central thesis.
5. Move repeated card icons into group headers if the page is dense.
6. Use color only to encode semantic difference.
7. Regenerate/rerender the icon manifest after the narrative is fixed.

When connectors look wrong:

- Tabs overlap cards: create a separate tab row or make tabs part of the card header, then push cards down.
- Diagonal line crosses text: move it behind opaque cards, shorten to edge anchors, remove arrowheads, lower weight/color; if it still reads as a slash, replace with a stepped connector or elbow in whitespace.
- Diagonal spokes have inconsistent angles: adjust center-halo anchors and mirror top/bottom slopes.
- Foreground line cuts multiple cards: lower z-order and ensure card fills are opaque, or remove it if decorative.
- Hub-and-spoke lines still feel wrong: switch to a pale relation field plus short edge rails.
- Slash separators in a step page: replace with short arrows or an explicit staircase/path lane.
