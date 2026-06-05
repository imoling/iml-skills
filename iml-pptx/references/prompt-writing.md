# Prompt Writing

Use this reference in Prompt mode, Image mode, or the prompt stage of Full production mode.

Before writing prompts, read `page-planning.md`, `design-draft-prompts.md` and `image2-visual-quality.md`, then create page decision cards. For executive content pages, write a compact PPT page design draft before the final image prompt. Do not write prompts from a generic deck template.

## Required Prompt Fields

Write prompts in Chinese unless the user asks otherwise. Every PPT image prompt must specify:

1. `16:9 中文PPT内容页图片`;
2. page type;
3. layout family;
4. why the layout fits this page's content relationship;
5. visual ambition level;
6. composition devices;
7. title;
8. core conclusion;
9. content modules;
10. layout idea;
11. visual system;
12. icon/image asset strategy;
13. text safety rules;
14. avoid-list;
15. anti-repetition note when this page follows a visually similar page.

Use concise, directly copyable prompts.

## Design Draft Requirement

For `executive` content pages, output two layers:

1. `PPT页面设计稿`: page title, subtitle, core message, page logic, layout ratio, left/middle/right modules, bottom value band, visual style and text safety.
2. `可直接复制的图片提示词`: the final concise prompt for image generation.

This mirrors high-quality manual prompt practice: clarify slide logic and design first, then ask image2 to render it.

## Base Prompt

```text
请生成一页16:9中文PPT内容页图片。

主题：【主题】
页面类型：【总览页 / 概念页 / 方法论页 / 流程页 / 对比页 / 场景页 / 问题页 / 数据页 / 案例页 / 总结页】
版式家族：【thesis + evidence / framework map / comparison matrix / split-screen contrast / process lane / timeline / swimlane / screenshot walkthrough / screenshot + callout rail / metric dashboard / risk heatmap / pyramid / decision tree / case evidence panel / action roadmap】
页面决策依据：【说明内容关系，以及为什么该版式适合这页】
视觉野心：【standard / polished / executive，重要正式材料默认 executive】
版面装置：【branded title strip / section numbering / central model / input-output model / process loop / capability library / bottom value band / screenshot evidence panel / comparison matrix / executive capability page 等】
标题：【标题】
核心结论：【一句话说明这页最想表达什么】

内容包含：
1. 【模块1】
2. 【模块2】
3. 【模块3】
4. 【模块4，可选】

版式要求：
- 根据内容选择最合适的版式，不要套固定模板
- 本页版式必须服务页面决策依据，不要沿用上一页的相同卡片结构，除非内容确实需要
- 充分发挥 image2 的页面设计能力：要有清晰的主视觉逻辑、分区编号、中心模型/证据面板/底部价值带等明确版面装置
- 页面效果要接近高质量科技企业路演PPT或咨询公司业务PPT，而不是普通代码生成PPT骨架
- 内容页要丰富且专业：信息密度适合正式汇报，优先采用“顶部标题横条 + 01/02/03编号分区 + 中心模型/输入输出链路 + 右侧能力库/分类清单 + 底部价值带”的高级内容页结构
- 标题清晰，层级明确，留白合理
- 图示要服务内容，不要只是装饰
- 页面要像正式培训课件或企业汇报PPT的一页
- 重要文本必须清晰可读，适合投屏展示
- 图标要形成一套逻辑系统，不要机械堆砌
- 如页面需要场景感、产品感或案例真实感，加入相关图片/截图/生成图作为视觉锚点，但必须服务内容
- 图片应有明确裁切方式，如右侧竖图、顶部窄幅、圆角场景图、截图卡片、设备/界面截图

文字安全要求：
- 所有中文文字必须完整位于对应卡片、标题栏、说明条、表格单元格或标注框内部
- 每个文字容器保留清晰内边距，不要让文字压线、越界、穿出圆角框或落到卡片外
- 小卡片正文控制在1-2行，底部说明条只放一个短句；内容过长时优先缩短文案或增大容器，不要缩小到不可读字号
- 任何卡片、说明框、底部横条中的文本都不能越过容器底边或右边

统一视觉风格：
- 白底
- 深灰文字
- 科技蓝主色
- 极简、专业、理性、可信
- 扁平信息图、线性图标、弱装饰
- 中文排版清晰

注意避免：
- 不要做成海报、网页首页或宣传长图
- 不要大面积渐变和炫光
- 不要文字拥挤
- 不要让图示变成无关装饰
- 不要生成难以复刻为PPT对象的复杂纹理背景
- 不要让标签、按钮、页签、徽章压到卡片边框或正文
- 不要让连线、趋势线、箭头穿过正文、标题、图标或关键数字
- 不要让卡片之间的间距小于视觉安全距离
- 不要使用无关图库照片
- 不要让图片遮挡文字、表格、数字或流程线
- 不要让连续页面呈现相同的三卡片/四卡片模板感
- 不要为了可编辑复刻而牺牲页面图的设计质量；页面图应先达到高质量视觉参考，再进行PPTX复刻
```

## Page Decision Discipline

- Every prompt should be traceable to a page decision card.
- If two adjacent prompts have the same page type and layout family, explicitly justify why repetition is intentional.
- If no justification exists, change one page's layout family before generating images.
- In full production, accepted page images become the visual source for editable PPTX replication. Do not replace them with a different coded layout during PPTX building.
- If the generated page is visually flat or weaker than the chosen ambition level, rewrite the prompt with stronger composition devices from `image2-visual-quality.md`.
- If generated text escapes its box, shorten the copy and regenerate before PPTX replication.

## Icon Prompt Rules

- If a page contains cards, modules, steps, comparison items, metrics or conclusions, define an icon system.
- First choose the icon narrative pattern: hero icon, section icons, step icons, comparison icons, metric icons, group header icons, or sparse accent icons.
- Each major module should have visual-semantic support unless the source style is intentionally text-only.
- Name icon semantics directly, for example `治理风险使用盾牌/天平类线性图标`, `流程编排使用workflow/route类线性图标`.
- Specify icon placement, size and semantic mapping; do not merely say `use icons`.
- If generated image lacks required icons or icons look pasted-on, treat it as a failed visual logic pass and regenerate or redesign.

## Image Asset Prompt Rules

- Decide whether a raster image improves comprehension before requesting one.
- For public products/software/platforms/websites, collect real visuals first when possible; see `external-visuals.md`.
- Product screenshots should show the actual UI state being taught: home/workbench, install/login, task creation, input box, sidebar/navigation, result area, settings/permissions, connector setup, automation state, error/confirmation state, or generated output.
- Preserve enough surrounding UI context for orientation; avoid over-cropping to one button unless the slide is specifically about that control.
- Use images for scenario realism, product inspection, industry context, human/workplace context, cover mood, or case evidence.
- Do not add images merely to fill empty space.
- Keep text/data in editable PPT objects when the image will later be replicated.

## Layout Safety In Prompts

- Reserve a fixed header area; do not place content cards inside it.
- Use a grid; cards in the same row should share top and bottom alignment.
- Keep at least 16-24 px visual spacing between independent elements in a 1280 x 720 design.
- Place tabs, badges and small labels fully inside a parent header or fully above the card with enough clearance.
- Route connectors through gutters and away from text, icons and key numbers.
- For hub-and-spoke layouts, use a pale central relation field and short edge rails before trying long spokes.
- Diagonal spokes are acceptable only when short, thin, lightly colored, anchored to object edges, mirrored, and placed behind cards/text.

## Image Generation QA

After generating each page image, inspect it. Regenerate or adjust the prompt if it has unreadable Chinese text, severe crowding, wrong aspect ratio, poster/webpage style, missing required module icons, unrelated images, or connector lines crossing content.
