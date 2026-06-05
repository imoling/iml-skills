# Page Planning

Use this reference before prompt writing, image generation, or full PPTX production. Its job is to prevent repetitive decks and force page type selection from content.

## Required Output: Page Decision Cards

Before creating prompts or PPTX, write one compact decision card per page:

```text
P01
- 内容意图：
- 核心结论：
- 内容关系：并列 / 递进 / 对比 / 因果 / 时间 / 层级 / 证据 / 操作 / 决策
- 页面类型：
- 版式家族：
- 视觉野心：standard / polished / executive
- 版面装置：branded title strip / section numbering / central model / input-output model / bottom value band / other
- 视觉锚点：截图 / 数据 / 图标系统 / 流程线 / 案例图 / 无
- 图标/连接线策略：
- 文本密度策略：
- 为什么不是套模板：
```

Do not start from a reusable visual template. Start from the content relationship.

## Page Type Selection

Choose page type by content intent:

| Intent | Page Type | Good Layout Families |
| --- | --- | --- |
| introduce a topic, scope or thesis | `总览页` / `概念页` | thesis + evidence, framework map, hero + satellites |
| define a concept or judgment | `概念页` | definition card + implications, 2x2 meaning map, before/after |
| compare options, competitors or choices | `对比页` | comparison matrix, split-screen contrast, scorecard |
| explain steps or lifecycle | `流程页` | process lane, staircase, timeline, swimlane |
| teach rules, principles or playbooks | `方法论页` | rule cards, pyramid, checklist system, operating model |
| show applications or user scenarios | `场景页` | scenario grid, role-based cards, screenshot walkthrough |
| diagnose mistakes, blockers or risks | `问题页` | risk heatmap, symptom-cause-fix, issue tree |
| present numbers or indicators | `数据页` | metric dashboard, trend + callouts, quadrant with metrics |
| prove with examples or product evidence | `案例页` | case evidence panel, screenshot + callout rail, thumbnail grid |
| close with action or takeaways | `总结页` | action roadmap, takeaway cards, decision checklist |

## Layout Families

Use layout families deliberately. Do not let every page become three cards plus a screenshot.

- `thesis + evidence`: one strong claim plus supporting proof or screenshot.
- `framework map`: a central concept with grouped surrounding modules.
- `comparison matrix`: rows and columns for explicit tradeoffs.
- `split-screen contrast`: left/right or top/bottom contrast.
- `process lane`: horizontal steps with short arrows.
- `timeline`: dated or staged progression.
- `swimlane`: roles, systems, or phases with handoffs.
- `screenshot walkthrough`: 2-4 screenshots with editable numbered callouts.
- `screenshot + callout rail`: one large screenshot plus side annotations.
- `metric dashboard`: 3-6 key metrics with explanation.
- `risk heatmap`: severity/likelihood or impact/control matrix.
- `pyramid`: hierarchy, maturity or priority stack.
- `decision tree`: branching choices and outcomes.
- `case evidence panel`: real visual on one side, editable findings on the other.
- `action roadmap`: now/next/later or short/mid/long actions.
- `executive capability page`: branded title strip + numbered three-zone body + central model/input-output logic + right capability library + bottom value band. Best for rich professional technology/business content pages.

## Diversity Rules

- No more than two adjacent pages should use the same layout family.
- In a deck with 6+ slides, no single layout family should dominate more than 40% of pages unless the source is a repeated training exercise or data table.
- Consecutive pages should vary at least one of: visual anchor, content relationship, module count, reading direction, or diagram type.
- Product/software decks should alternate between explanation pages and screenshot evidence pages.
- Dense business decks should mix framework, table, flow, evidence and action pages instead of repeating card grids.

If a page plan violates these rules, revise the page type or layout family before writing prompts.

## Visual Ambition Rule

- For full production and important user-facing decks, default to `executive`.
- For internal quick drafts, use `polished`.
- Use `standard` only when the user explicitly wants a rough skeleton or low-density page.
- A page with `executive` ambition must include at least one strong composition device: central model, input-output model, process loop, screenshot evidence panel, comparison matrix, capability library, or bottom value band.
- For important content pages, prefer the `executive capability page` archetype unless the content is purely data/table/process. It should be richer and more professional than a sparse card page.
- If the deck starts to look repetitive, vary the composition device before changing colors.

For detailed image-generation quality rules, read `image2-visual-quality.md`.

## Visual-First Full Production

For full production from topic/source to editable PPTX, use this chain:

1. Distill the source into page decision cards.
2. Write image prompts from the decision cards.
3. Generate or obtain page images.
4. Inspect the images for layout, text readability, icon logic and visual variety.
5. Replicate the accepted page images into editable PPTX.
6. Run screenshot QA on the PPTX.

Do not skip from outline directly to a coded PPTX unless:

- the user explicitly asks for code-native PPT without generated images;
- image generation is unavailable;
- the task is a low-stakes draft where the user only needs a rough editable skeleton.

When skipping page images, say so in the final response and label the output as a fallback or skeleton rather than the full iML-PPTX chain.

## Prompt Integration

Every PPT image prompt should include:

- page type;
- layout family;
- why this layout fits the content;
- visual anchor;
- icon/connector strategy;
- anti-repetition note, for example `本页采用流程泳道，不沿用上一页三卡片布局`.

This keeps the image model from returning the same generic card layout repeatedly.
