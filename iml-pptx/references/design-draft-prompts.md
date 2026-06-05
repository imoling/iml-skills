# Design Draft Prompts

Use this reference when writing prompts for rich professional PPT content pages. A good image prompt should first be a page design draft, then a copyable image-generation prompt.

## Design Draft First

Before the final image prompt, create a compact design draft with these fields:

```text
PPT页面设计稿
- 页面标题：
- 副标题：
- 核心表达落点：
- 页面逻辑：概念定义 -> 运行机制 -> 业务落地 -> 平台价值
- 整体布局：顶部标题区15% / 主体内容区75% / 底部价值区10%
- 主体三栏：左侧28% / 中间38% / 右侧30%
- 左侧模块：
- 中间模块：
- 右侧模块：
- 底部价值条：
- 视觉风格：白底、科技蓝、线性图标、蓝色标题条、卡片化、干净留白
- 文本安全：短句、分组、所有文字在容器内
```

The design draft is not optional for `executive` content pages. It makes the image model understand the slide as a composed business page, not a loose set of cards.

## Reusable Executive Prompt Logic

Use these as generic prompt structures. Do not copy their topic wording; adapt them to the user's actual domain, product, concept or source material.

### Mechanism Explanation Page

Use when explaining how a concept, framework, system or method works.

```text
页面逻辑：概念定义 -> 运行机制 -> 应用场景 -> 价值总结
整体布局：左侧机制解释 + 中间核心流程/闭环/模型 + 右侧应用示例 + 底部价值总结
左侧：01 | 核心机制，放一个公式/判断/定义，下面放三句“不是A，而是B”式短句
中间：02 | 运行机制，用环形闭环、流程引擎、分层模型或输入-处理-输出结构展示关键步骤
右侧：03 | 典型应用，用“问题/任务输入 -> 执行过程 -> 输出结果”的场景卡说明落地
底部：4个价值点，每个价值点=标题+一句短说明
```

Preferred visual devices:

- process loop;
- section numbering;
- scenario card;
- bottom value band;
- blue card system with one central loop.

### Capability Packaging Page

Use when explaining reusable capabilities, product modules, tool libraries, service catalogs, platform assets, APIs, plugins or capability markets.

```text
页面逻辑：概念定义 -> 封装/生产机制 -> 分类沉淀 -> 平台价值
整体布局：左侧定义解释 + 中间能力封装/生产模型 + 右侧能力库/模块库/服务目录 + 底部价值总结
左侧：01 | 核心定义，放一个“X = 可复用/可调用/可治理的Y能力”式表达，下面放三句对比短句
中间：02 | 标准化封装模型，左侧输入资源 -> 中心标准模块/能力包 -> 右侧输出能力
右侧：03 | 能力库示例，展示4-6个分类卡片，每类2-4个短关键词
底部：4个价值点，例如资产沉淀、跨场景复用、安全治理、持续扩展
```

Preferred visual devices:

- input-output model;
- central hexagon/core module;
- capability library;
- section numbering;
- bottom value band.

### Scenario Application Page

Use when showing how a product, method or platform solves real tasks.

```text
页面逻辑：业务背景 -> 任务流程 -> 场景示例 -> 输出价值
整体布局：左侧场景/角色/痛点 + 中间操作流程或任务编排 + 右侧结果样例/截图/清单 + 底部价值总结
左侧：01 | 场景定义，说明谁在什么情况下遇到什么任务
中间：02 | 任务执行路径，用步骤条、泳道、流程卡或工具调用链表达
右侧：03 | 结果输出，用结果卡、截图证据、指标或交付物清单表达
底部：4个价值点，强调效率、质量、协同、可追溯等真实收益
```

Preferred visual devices:

- screenshot/evidence panel;
- process lane or swimlane;
- scenario card;
- output checklist;
- bottom value band.

### Comparison Or Decision Page

Use when comparing options, old/new approaches, before/after states, products or strategies.

```text
页面逻辑：比较对象 -> 关键维度 -> 差异判断 -> 选择建议
整体布局：左侧背景/判断标准 + 中间对比矩阵或天平结构 + 右侧结论/推荐路径 + 底部价值总结
左侧：01 | 比较背景，说明为什么要比较
中间：02 | 对比维度，用矩阵、双栏、雷达或评分卡展示差异
右侧：03 | 决策结论，给出推荐、适用边界或下一步动作
底部：4个价值点或注意事项
```

Preferred visual devices:

- comparison matrix;
- split-screen contrast;
- scorecard;
- decision checklist;
- bottom value band.

## Writing Rules

- Use concrete module copy, not abstract placeholders.
- Use short business phrases. Avoid long paragraphs inside small cards.
- Include a page-level core message so the visual hierarchy knows what to emphasize.
- Include layout percentages when the page is dense.
- Include visual tone, color, icon style and density.
- Include a compact ASCII layout sketch only when the structure is complex.
- Keep generated page prompts copyable; do not bury the final prompt under long explanation.

## Prompt Shape

After the design draft, produce the final image prompt like this:

```text
请生成一页16:9中文PPT内容页图片。

页面主题：【主题】
页面标题：【标题】
副标题：【副标题】
核心表达：【客户看完这页要形成的认知】

整体布局：
- 顶部标题区约15%，左上蓝色标题条，右上Logo区
- 主体区约75%，三栏布局：左侧28%，中间38%，右侧30%
- 底部价值条约10%，横向4个价值点

主体内容：
01｜【左侧模块标题】
【左侧核心公式/判断】
【三句短文案】
【说明框短文】

02｜【中间模块标题】
【中心模型/闭环/输入输出结构】
【节点或标签】

03｜【右侧模块标题】
【场景卡/能力库/示例清单】

底部价值条：
【4个价值点，每个价值点=标题+一句短说明】

视觉要求：
- executive级科技企业路演/咨询汇报PPT
- 白底、科技蓝、浅蓝卡片、细描边、轻微投影、统一线性图标
- 信息丰富但结构清晰，像正式汇报材料，不像普通模板
- 所有中文文字必须完整位于对应容器内，保留内边距，不得压线、越界、出框
```
