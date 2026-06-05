# Workflow Recipes

Use this reference when the request is common but broad. Pick one recipe, then load only the additional references it names.

## Recipe 1: PPT Image Prompts Only

Use when the user asks for `PPT图片提示词`, `提示词`, prompt templates, or a multi-page prompt plan.

1. Create or infer a short production brief.
2. Read `page-planning.md`, `design-draft-prompts.md`, `image2-visual-quality.md`, then `prompt-writing.md`.
3. Decide page rhythm from content intent, such as `总览 / 场景 / 方法论 / 治理 / 行动路径`.
4. Create page decision cards before writing prompt blocks.
5. For executive content pages, write a compact `PPT页面设计稿` before the final image prompt.
6. For each page, output page type, layout family, visual ambition, composition devices, decision rationale, title, core conclusion, modules, layout, visual system, icon/image strategy, text safety rules and avoid-list.
7. Keep prompts copyable. Do not generate images unless the user asks.

Output shape:

```text
制作简报
- 主题：
- 受众：
- 交付模式：prompt
- 样式主题：
- 页面节奏：
- 页面类型策略：
- 版式多样性约束：
- 视觉野心：
- 图片策略：
- 可编辑边界：

P01｜【标题】
页面决策卡：
- 内容意图：
- 页面类型：
- 版式家族：
- 视觉野心：
- 版面装置：
- 视觉锚点：

PPT页面设计稿：
- 页面标题：
- 副标题：
- 页面逻辑：
- 整体布局：
- 左侧模块：
- 中间模块：
- 右侧模块：
- 底部价值条：

【可直接复制的图片提示词】
```

## Recipe 2: Direct PPT Page Image Generation

Use when the user says `直接生成图片`, `生成一页PPT图片`, or asks to continue generating page images.

1. Read `page-planning.md`, `design-draft-prompts.md`, `image2-visual-quality.md` and `prompt-writing.md`.
2. Create page decision cards and a compact design draft; confirm layout variety, visual ambition and composition devices before image generation.
3. If named public products, sites, people, objects or places are central, read `external-visuals.md` and collect useful visuals first.
4. Generate one image per page prompt.
5. Save stable page-numbered filenames such as `P01_标题.png`.
6. Inspect each image for readable Chinese text, text containment, correct aspect ratio, page-like layout, relevant icons/images, clean connectors, visual ambition and visual variety versus adjacent pages.
7. Regenerate before reporting completion when text escapes boxes, visual logic fails, pages repeat the same layout without reason, or the result is visually weaker than the requested ambition level.

Final response should list generated image files and any inspected/retried pages.

## Recipe 3: Editable PPT Replication From Image/PDF/Screenshot

Use when the user asks for `可编辑PPT`, `复刻`, `转成PPTX`, `完全按照图片`, or gives page images/PDF pages.

1. Read `editable-replication.md` and `qa.md`.
2. Inspect or render the source page first.
3. Extract title, modules, layout grid, editable objects, icons/logos, screenshots/photos and connector lines.
4. Build PPT page by page; do one confirmation page first if the page is complex or sets the deck style.
5. Recreate text, boxes, tables, lines, arrows, labels and callouts as editable objects.
6. Insert icons/logos/photos/screenshots as high-quality image assets only where appropriate.
7. Run layout and connector guards when applicable.
8. Produce and inspect a preview screenshot before reporting completion.

Final response should include PPTX path, preview path/status, completed pages, editable objects, non-editable assets and known limits.

## Recipe 4: Product Or Software Training PPT

Use when the deck teaches a product, software, SaaS, app, website workflow, connector, authorization, installation or UI operation.

1. Read `external-visuals.md` before designing the slide.
2. Prefer official docs/site screenshots, user-provided screenshots or verified public visuals.
3. Use screenshot walkthrough, screenshot card or screenshot + callout rail.
4. Keep callouts, arrows, labels, step numbers and captions editable.
5. Do not rely only on icons or abstract diagrams when the audience needs to learn the interface.
6. If converting to PPTX, also read `editable-replication.md` and `qa.md`.

## Recipe 5: Full Topic/Source To Editable PPTX

Use when the user asks for a finished PPTX from a topic, article, source material, product, PDF or loose brief.

1. Read `page-planning.md`, `design-draft-prompts.md`, `image2-visual-quality.md`, `prompt-writing.md`, `editable-replication.md` and `qa.md`; load `external-visuals.md` when real entities matter.
2. Distill the source into page decision cards. Each card must include page type, layout family, visual ambition, composition devices and visual anchor.
3. Check layout diversity. Revise if three adjacent pages share the same structure or if one layout family dominates the deck.
4. Write page design drafts, then page image prompts from the decision cards.
5. Generate or obtain page images and inspect them for visual quality and text containment.
6. Accept page images as the visual source of truth.
7. Replicate accepted images into editable PPTX page by page.
8. Run screenshot QA and report the preview path.

Do not skip steps 4-6 unless the user explicitly asks for a code-native PPT skeleton or the image-generation tool is unavailable. If skipped, report that the output is a fallback and not the full prompt-to-image-to-editable-PPT chain.

## Recipe 6: Icon/Connector Heavy Framework Page

Use when a page has many cards, modules, steps, hub-and-spoke relations, process arrows or semantic icons.

1. Read `icons-connectors.md`.
2. Choose one page design pattern: `Hero + satellites`, `Step progression`, `Contrast pair`, `Metric anchors`, `Group headers` or `Sparse accent`.
3. Create an icon manifest when there are 3+ modules/cards/steps unless intentionally text-only.
4. Create a connector manifest when there are more than two lines.
5. Render selected icons before PPT insertion.
6. Run `connector_guard.py` when PPTX lines are present and inspect the preview.

## Final Report Template

Use this shape for image/PPT production tasks:

```text
已完成。
输出文件：
- 【PPTX或图片路径】

预览检查：
- 【预览图路径 / 检查了哪一页】

可编辑对象：
- 【文字、卡片、表格、线条、箭头、标签等】

非编辑资产：
- 【图标PNG、logo、截图、照片等】

已知限制：
- 【没有则写“无明显限制”】
```
