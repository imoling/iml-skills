---
name: iml-pptx
description: Create Chinese PPT pages through a prompt-to-image-to-editable-PPT workflow. Use when the user wants 中文PPT图片提示词, PPT image prompts, 16:9中文PPT页面图片, 直接生成PPT图片, 根据提示词生成图片, 把图片/PDF/截图复刻成可编辑PPT, 转成可编辑PPTX, 按图片完全复刻PPT, or full production from topic/source material to generated page images and editable PowerPoint slides with editable text, cards, tables, lines, callouts and high-quality icon/image assets.
---

# IML PPTX

## Production Goal

Use this skill to make real Chinese PPT pages through any part of this chain:

1. write prompts for Chinese 16:9 PPT page images;
2. generate the corresponding PPT page images;
3. convert generated or supplied images into visually matched editable PPT slides;
4. assemble or continue a deck page by page.

Core rules:

- Treat a supplied/generated page image as the visual source of truth.
- Do not redesign a different deck when the user asks for replication.
- Keep text, boxes, tables, lines, arrows, labels, callouts and layout frames editable whenever practical.
- Icons, small logos, photos, screenshots and generated bitmap visuals may be non-editable high-resolution assets.
- Preserve the page image's layout, hierarchy, density and business-PPT style.

Default visual system unless the user provides another style: 16:9 Chinese business-training content page, white background, dark gray/black text, technology blue accent, minimal formal infographic style, readable Chinese typography, `PingFang SC` / 苹果苹方 for recreated PPT.


## Reference Index

Load only the references needed for the current task:

| Task | References |
| --- | --- |
| Write PPT image prompts | `references/prompt-writing.md`, optional `references/examples.md` |
| Generate PPT page images | `references/prompt-writing.md`, optional `references/external-visuals.md` |
| Replicate image/PDF/screenshot into editable PPT | `references/editable-replication.md`, `references/qa.md` |
| Product/software/website training PPT | `references/external-visuals.md`, `references/prompt-writing.md`, `references/editable-replication.md` if making PPTX |
| Icon-heavy or connector-heavy page | `references/icons-connectors.md` |
| Unsure how to execute a common request | `references/workflow-recipes.md` |
| Need command examples | `references/scripts.md` |

## Start Brief

Before choosing a mode, create or infer a short production brief unless current context already contains one. Include:

```text
制作简报
- 主题：
- 受众：
- 交付模式：prompt / image / editable-ppt / full
- 样式主题：
- 页面节奏：
- 图标/logo策略：
- 图片策略：
- 外部取材策略：
- 字体：
- 来源约束：
- 可编辑边界：
- 首个确认页：
```

Use `python3 scripts/start_brief.py ...` when a generated checklist would help.

Default choices:

- `样式主题`: white background, dark text, technology blue accent, business-training infographic.
- `字体`: `PingFang SC`.
- `图片策略`: use photos/screenshots/generated visuals only when they clarify the subject, scenario, product, industry or evidence.
- `外部取材策略`: when a public product, software, website, company, person, place, device or real object is central, acquire official/verified visuals unless forbidden or sensitive.
- `可编辑边界`: text/cards/tables/lines/diagrams editable; icons/logos/screenshots/photos may be image assets.

For detailed external visual acquisition rules, read `references/external-visuals.md`.

## Mode Router

Decide the user's real intent from the latest request:

- `Prompt mode`: user asks for 提示词, prompt library, page image prompts, or reusable prompt rules. Read `references/prompt-writing.md`.
- `Image mode`: user asks to 根据提示词生成图片, 直接生成图片, or continue generating PPT page images. Read `references/prompt-writing.md`; if real visuals are needed, also read `references/external-visuals.md`.
- `Editable PPT mode`: user asks to turn images/photos/PDF pages/screenshots into editable PPT, 复刻, 转成可编辑PPT, or continue later pages. Read `references/editable-replication.md`, `references/qa.md`, and `references/icons-connectors.md` when icons/lines are present.
- `Full production mode`: user asks to go from topic/PDF/source to prompts, images and editable PPT. Read all relevant references as the workflow reaches each phase.

When the user says `不是重新构建一套PPT`, `完全按照刚刚的图片`, `图片对应的PPT复刻`, or `先执行一张我确定下`, switch to `Editable PPT mode` and treat the page image as canonical.

## Workflow

1. Identify topic, audience, slide count, page type, source constraints and delivery mode.
2. Identify public visual entities that may require screenshots/photos/logos. If present, run the External Visual Acquisition Gate in `references/external-visuals.md` before final prompts or PPT layout.
3. If source is PDF/image, render or inspect pages first. Extract title, core conclusion, modules, diagram type, visual hierarchy, icon/logo needs, image asset needs and likely editable objects.
4. If writing prompts, create concise copyable Chinese prompts with page type, title, core conclusion, modules, layout, visual system, icon/image strategy and avoid-list.
5. If generating images, create one image per prompt, save with stable page numbers such as `P01_标题.png`, inspect each image, and regenerate if text/layout/icons/connectors fail.
6. If replicating to PPT, rebuild page by page or in small similar batches. Recreate editable objects first; insert high-quality icons/photos/screenshots as image assets only where appropriate.
7. Run mandatory QA before reporting completion.

## Mandatory Gates

### Visual Asset Gate

Use real or verified visuals when they materially improve a product, software, website, case, public person, place, device, UI or industry-context slide. Save selected assets and source notes in the project asset folder. Put useful visuals into the PPT, not only into notes or prompts. Details: `references/external-visuals.md`.

### Icon Gate

For every slide with 3 or more modules/cards/steps, create an icon plan or manifest before building the PPT unless the source image is intentionally text-only. Use `scripts/icon_picker.py`, `scripts/icon_narrative.py`, `scripts/render_icon_manifest.py`, or `scripts/render_lucide_icon.py` as needed. Details: `references/icons-connectors.md`.

### Connector Gate

Treat connectors as semantic objects. Before drawing lines, define purpose, necessity, type, anchors, avoid zones and layer. Use `scripts/connector_narrative.py` for complex pages and `scripts/connector_guard.py` after building decks with connector lines. Details: `references/icons-connectors.md`.

### Screenshot QA Gate

For every task that generates, edits, repairs or replicates a PPT/PPTX page, create and inspect a visual preview unless the user explicitly says not to preview.

Required:

1. Produce a screenshot/thumbnail after building the PPTX.
2. Inspect the screenshot with the available visual tool.
3. If only one page changed, preview that changed page.
4. If the preview tool only renders the first slide, create a temporary one-slide preview for the changed page or use another renderer.
5. Do not treat XML checks, file size, `layout_guard.py` or `connector_guard.py` as substitutes for visual preview.
6. In the final response, mention the preview path or which preview image was inspected.

In Codex desktop, prefer:

```bash
scripts/preview_pptx.sh output/deck.pptx output/preview
```

Detailed QA and repair rules: `references/qa.md`.

## Output Modes

- `Single Prompt`: short opening line plus one polished prompt block.
- `Prompt Library`: short system summary plus prompts grouped by page type.
- `Theme-Adapted Prompts`: state what visual system stays fixed; per-page prompts should say `统一风格，不统一死版`.
- `Generated Images`: generated image files, page numbers and filenames; no long prompt explanation unless requested.
- `Editable PPT From Images`: `.pptx` files, preview status, completed pages, and any non-editable icon/logo/photo/screenshot assets.
- `Full PPT Production`: prompt plan, generated page images, editable PPT replication, final checked PPTX or per-page PPTX files.

## Scripts

Use helper scripts when they reduce repeated manual work. Invoke Python scripts with `python3`.

- `scripts/smoke_test.py`: run a non-destructive smoke test for core helper scripts.
- `scripts/start_brief.py`: create a production brief template.
- `scripts/icon_picker.py`: search offline/lucide icon candidates by English or Chinese business meaning.
- `scripts/icon_narrative.py`: draft page-level icon logic and manifest skeleton.
- `scripts/connector_narrative.py`: draft connector strategy from design pattern and modules.
- `scripts/render_lucide_icon.py`: render one lucide icon to SVG/PNG.
- `scripts/render_icon_manifest.py`: render a page icon manifest to SVG/PNG assets.
- `scripts/build_icon_resources.py`: rebuild offline icon resources after pack/library changes.
- `scripts/ppt_replicate_helpers.py`: reusable low-level OOXML helpers for editable PPT builders.
- `scripts/layout_guard.py`: heuristic PPTX overlap preflight; inspect warnings manually.
- `scripts/connector_guard.py`: scan likely accidental diagonal/unstable connector lines.
- `scripts/preview_pptx.sh`: create Quick Look preview PNGs for visual QA.

See `references/scripts.md` for command examples and `references/workflow-recipes.md` for common end-to-end recipes.

## Page Types

Infer page type when missing:

- `总览页`: chapter overviews, frameworks, maps, taxonomy.
- `概念页`: defining a term or explaining a judgment.
- `对比页`: A/B, before/after, can/cannot, old/new.
- `流程页`: steps, methods, lifecycle, workflow.
- `方法论页`: rules, principles, practices, playbooks.
- `场景页`: applications, use cases, industry examples.
- `问题页`: common mistakes, risks, diagnosis.
- `数据页`: indicators, market size, metrics, trends.
- `案例页`: company examples, benchmark samples, implementation stories.
- `总结页`: chapter close, key takeaways, action points.

## Style And Boundaries

- Reply in concise Chinese for Chinese PPT workflows.
- When the user asks for action, produce files rather than only advice.
- Keep prompts copyable and avoid poster/webpage/marketing-page language for content slides.
- Do not drift into full slide copywriting unless requested.
- Do not assume every page uses the same left-right split.
- Do not claim every object is editable if icons/logos/photos/screenshots are inserted as image assets.
- Do not promise exact official brand logos unless actually sourced or available.
