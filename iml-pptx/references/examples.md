# Examples

Micro end-to-end examples for the most common iml-pptx requests.

## 1. Prompt Mode: Multi-Page Business Training Deck

User: `帮我写5页央国企AI应用培训的PPT图片提示词，白底科技蓝风格。`

Read:

- `prompt-writing.md`
- optional `workflow-recipes.md` Recipe 1

Do:

1. Create a short production brief.
2. Choose page rhythm, for example `总览 / 场景 / 方法论 / 治理 / 行动路径`.
3. Output page-by-page copyable prompt blocks.
4. Include page type, title, core conclusion, modules, layout, visual system, icon/image strategy and avoid-list.

Output shape:

```text
制作简报
- 主题：央国企AI应用培训
- 受众：央国企管理者/业务骨干
- 交付模式：prompt
- 样式主题：白底、科技蓝、商务培训信息图
- 页面节奏：总览 / 场景 / 方法论 / 治理 / 行动路径
- 可编辑边界：为后续PPT复刻保留清晰框体、线条、图标和文字层级

P01｜AI应用全景总览
【可直接复制的图片提示词】
```

QA:

- Prompts are directly copyable.
- They do not drift into generic article outlines.
- They preserve the requested white/technology-blue business style.

## 2. Image Mode: Direct Generation

User: `生成一页 Hermes Agent 介绍的图片，直接生成图片。`

Read:

- `prompt-writing.md`
- `external-visuals.md` if the named subject needs public visuals

Do:

1. Treat this as final image delivery, not only prompt writing.
2. Generate a 16:9 Chinese PPT content page image.
3. Save with a stable name such as `P01_Hermes_Agent介绍.png`.
4. Inspect the generated image before reporting completion.
5. Regenerate if text is unreadable, layout is poster-like, icons are missing/irrelevant, or connectors cross content.

Final response shape:

```text
已完成。
输出文件：
- P01_Hermes_Agent介绍.png

预览检查：
- 已检查：中文可读、16:9、图标与模块语义一致
```

## 3. Editable PPT Mode: Replicate From Image

User: `把这张图片对应的PPT复刻成可编辑PPT，不是重新构建一套。先执行一张我确定下。`

Read:

- `editable-replication.md`
- `qa.md`
- `icons-connectors.md` if the page has many icons or relation lines

Do:

1. Switch to Editable PPT mode immediately.
2. Treat the image as the canonical source.
3. Recreate text, cards, tables, lines, arrows, labels and callouts as editable PPT objects.
4. Use high-quality image assets for icons/logos/screenshots when appropriate.
5. Produce one PPTX page first when the user asks to confirm.
6. Render and inspect a preview screenshot before asking for confirmation.

Final response shape:

```text
已完成第一页复刻。
输出文件：
- page01_replicated.pptx

预览检查：
- preview/page01.png，已检查无明显文字重叠或连接线穿正文

可编辑对象：
- 标题、正文、卡片、线条、箭头、标签

非编辑资产：
- 图标PNG / 截图区域
```

## 4. Product/Screenshot Training PPT

User: `做一页某产品的上手流程PPT，要能看懂界面怎么操作。`

Read:

- `external-visuals.md`
- `prompt-writing.md`
- `editable-replication.md` and `qa.md` if producing PPTX

Do:

1. Run the External Visual Acquisition Gate if the product is public and browsing is allowed.
2. Prefer official docs/site screenshots, live product screenshots, or user-provided screenshots.
3. Use screenshot walkthrough, screenshot card, or screenshot + callout rail.
4. Keep arrows, labels, step numbers, callouts and captions editable.
5. Do not rely only on abstract icons when the audience needs to learn the interface.

QA:

- Screenshot reveals actual UI location/state.
- Sensitive/private data is not exposed.
- Callouts and captions are editable PPT objects.
- Crop preserves enough UI context for orientation.
