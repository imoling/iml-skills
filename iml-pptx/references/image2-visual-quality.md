# Image2 Visual Quality

Use this reference before writing prompts for GPT Image / image2-style PPT page images. Its job is to preserve image-generation quality while keeping the page replicable as editable PPTX later.

## Visual Ambition Levels

Choose one level per page:

- `standard`: clean business PPT, simple cards, low density. Use for drafts or minor pages.
- `polished`: stronger hierarchy, section labels, icons, subtle shadows, one clear visual device. Use for normal deliverables.
- `executive`: boardroom/consulting style, high information density, branded title strip, structured diagrams, premium icon system, evidence panels and bottom value band. Use for important decks by default.

Default: `executive` for full production unless the user asks for a quick draft. Content pages should feel rich and professional: enough information density for a real business meeting, but still clearly structured and readable.

## Preferred Content Page Archetype

For normal Chinese business/technology content pages, prefer this archetype unless the page content clearly calls for another structure:

```text
高质量内容页原型：
- 顶部：深蓝标题横条或标签 + 大标题 + 一句副标题，右上角可放品牌/logo区
- 主体：三段式编号结构（01 / 02 / 03），每段有清晰标题
- 中心：一个主视觉逻辑装置，如六边形中心模型、流程闭环、输入-标准化-输出模型、能力地图或决策矩阵
- 左侧：定义、输入、背景、问题或资源来源
- 右侧：能力库、分类结果、应用场景、输出清单或案例证据
- 底部：3-5个价值点组成的横向价值带，配统一线性图标和短句
```

Use this archetype for pages like capability maps, methodology pages, industry solution pages, AI/agent architecture pages, product capability pages, and skill/library explanations.

The page should look like a polished technology-company roadshow or consulting report slide, not a sparse template. It may use dense but organized information architecture, consistent icon systems, soft card shadows, pale blue panels, semantic accent colors and precise section labels.

## High-Quality Composition Devices

Use specific devices instead of vague words like "professional":

- `branded title strip`: blue top label or header band, optional logo area, strong H1 and subtitle.
- `section numbering`: `01 |`, `02 |`, `03 |` headings for multi-zone layouts.
- `central model`: hexagon, loop, hub, stack, pyramid or core engine in the middle.
- `input-output model`: left inputs, center standardization/model, right outputs.
- `case/evidence panel`: screenshot or product proof with editable callouts.
- `bottom value band`: 3-5 value cards with icons and concise captions.
- `capability library`: right-side category list with colored icon chips.
- `process loop`: circular arrows around a core concept.
- `swimlane`: role/system/stage rows with handoff arrows.
- `comparison matrix`: columns, tags and score markers.
- `scenario card`: real workflow example with question, process and output.

Good image2 prompts should name the chosen devices directly.

## What "Better PPT Image" Means

A strong generated PPT page should have:

- clear title hierarchy and enough white space;
- visible section architecture, not just loose cards;
- one dominant visual logic device;
- rich but disciplined information density, suitable for formal business presentation;
- consistent icon style and semantic colors;
- subtle depth: pale panels, light borders, soft shadows, restrained gradients;
- strong blue business palette with small green/orange/purple semantic accents;
- realistic page density for consulting/business training slides;
- clean readable Chinese, with body copy short enough to render.

Avoid over-flattening into a code-native skeleton. The generated image is allowed to be more visually expressive than the final editable PPT objects, as long as the layout can still be reconstructed.

## Text Safety For Image Generation

Generated images can fail before PPTX replication if the prompt asks for too much text. Before generating:

- Compress each card body to 1-2 short lines when possible.
- Keep small card body text under about 24 Chinese characters.
- Keep medium card body text under about 48 Chinese characters.
- Do not put long paragraphs inside narrow cards.
- For bottom bands, use a bold label plus one short sentence only.
- If a module needs a long explanation, convert it into a larger evidence panel, table row, or callout rail.

Prompt must include:

```text
所有中文文字必须完整位于对应卡片、标题栏、说明条、表格单元格或标注框内部；
每个文字容器保留清晰内边距；
不要让文字压线、越界、穿出圆角框或落到卡片外；
如果内容过长，优先缩短文案或增大容器，而不是缩小到不可读字号。
```

## Reference-Caliber Prompt Add-On

Append this when the page should use image2's visual strength:

```text
视觉质量要求：
- 参考高质量咨询公司/科技企业路演PPT的信息架构，而不是普通代码生成PPT
- 使用明确的版面装置：【填写 branded title strip / section numbering / central model / input-output model / bottom value band 等】
- 页面要有主视觉逻辑：中心模型、流程闭环、能力地图、案例证据或对比矩阵之一
- 使用白底科技蓝，配合浅蓝信息面板、细描边、轻微投影、统一线性图标
- 允许适度高级感：顶部蓝色标签、编号分区、中心渐变模型块、底部价值带、局部语义色
- 保持正式商务PPT，不要做成海报、网页首页、长图或过度装饰
```

## Regeneration Triggers

Regenerate or rewrite the prompt when:

- body text escapes card boundaries;
- section headings collide with logos, borders or tags;
- small cards contain paragraph-length text;
- the page repeats a plain 3-card or 4-card template without a central visual idea;
- icon styles are inconsistent or decorative;
- the visual result is flatter than the requested ambition level;
- the generated page looks less polished than a hand-designed consulting PPT reference.
