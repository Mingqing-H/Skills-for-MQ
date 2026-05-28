# Mingqing Skills

这是我为 AI Agent / Codex 工作流开发的一组自定义 Skills。它们不是简单的提示词集合，而是把“任务触发条件、处理流程、脚本工具、参考规范、输出质量标准”打包成可复用能力模块，让 Agent 在真实工作中更稳定地完成内容处理、视觉输出、学习卡片、语音生成、图片生成、网页素材抓取等任务。

## 亮点

- **面向真实任务设计**：每个 Skill 都有明确触发场景、处理步骤和输出要求，减少 Agent 临场发挥造成的不稳定。
- **脚本 + Prompt 协同**：需要确定性执行的部分交给 Python 脚本，判断、规划、解释和生成交给 Agent。
- **强调产物质量**：不仅能“完成任务”，还关注可读性、可复用性、移动端适配、交互体验和用户反馈。
- **覆盖多模态工作流**：文本清洗、写作风格学习、HTML 可视化、记忆卡片、图片生成、语音合成、壁纸数据抓取。
- **安全意识**：仓库不应提交真实密钥；需要 API 的 Skill 使用本地 `config.json` 或环境变量配置。

## Skills 一览

| Skill | 适用场景 | 能力关键词 |
| --- | --- | --- |
| [`extract-md`](./extract-md) | 从网页、公众号复制内容中提取正文并保存为 Markdown | 内容清洗、正文识别、Markdown 输出 |
| [`writing-style-learner`](./writing-style-learner) | 分析作者写作风格，生成风格画像，并用于仿写/改写 | 文风分析、风格迁移、结构化诊断 |
| [`html-beautiful-output`](./html-beautiful-output) | 把复杂报告、计划、解释、评审转成精美自包含 HTML | 信息设计、可视化输出、交互式阅读 |
| [`memory-learning-cards`](./memory-learning-cards) | 把知识材料转成便于理解和记忆的学习卡片 | 记忆法、学习体验、HTML 卡片 |
| [`image-gen-moda`](./image-gen-moda) | 调用 ModelScope 文生图模型生成本地图片 | API 集成、异步轮询、图片生成 |
| [`mimo-tts`](./mimo-tts) | 调用小米 MiMo V2.5 TTS 生成语音、设计声音、克隆声音 | TTS、音频生成、OpenAI-compatible API |
| [`haowallpaper-direct`](./haowallpaper-direct) | 无浏览器抓取 HaoWallpaper 壁纸信息和公开媒体链接 | SSR 解析、数据抽取、批量下载 |

## 如何下载和安装

### 下载全部 Skills

```bash
git clone https://github.com/Mingqing-H/Skills-for-MQ.git
cd Skills-for-MQ
```

安装到 Codex 的本地 Skills 目录：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills"
Copy-Item -Recurse .\extract-md "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\writing-style-learner "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\html-beautiful-output "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\memory-learning-cards "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\image-gen-moda "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\mimo-tts "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\haowallpaper-direct "$env:USERPROFILE\.codex\skills\"
```

macOS / Linux 可使用：

```bash
mkdir -p ~/.codex/skills
cp -R extract-md writing-style-learner html-beautiful-output memory-learning-cards image-gen-moda mimo-tts haowallpaper-direct ~/.codex/skills/
```

### 只下载某一个 Skill

如果只想下载单个目录，推荐使用 Git sparse checkout。例如只下载 `memory-learning-cards`：

```bash
git clone --filter=blob:none --sparse https://github.com/Mingqing-H/Skills-for-MQ.git
cd Skills-for-MQ
git sparse-checkout set memory-learning-cards
```

然后复制到本地 Skills 目录：

```powershell
Copy-Item -Recurse .\memory-learning-cards "$env:USERPROFILE\.codex\skills\"
```

把命令里的 `memory-learning-cards` 换成任意 Skill 名称即可，例如：

```bash
git sparse-checkout set mimo-tts
git sparse-checkout set html-beautiful-output
git sparse-checkout set haowallpaper-direct
```

也可以在 GitHub 页面点击 **Code → Download ZIP** 下载整个仓库，解压后只保留自己需要的那个 Skill 文件夹。把对应 Skill 文件夹复制到该客户端要求的 Skills 目录中。核心原则是：一个 Skill 保持一个完整文件夹，里面的 `SKILL.md`、`scripts/`、`references/` 等文件不要拆开。

## 运行依赖速查

| Skill | 是否需要脚本依赖 | 说明 |
| --- | --- | --- |
| `extract-md` | 否 | 主要依赖 Agent 按规则清洗和保存 Markdown |
| `writing-style-learner` | 否 | 主要依赖 Agent 读取多篇文档并生成风格画像 |
| `html-beautiful-output` | 否 | 输出自包含 HTML，无构建步骤 |
| `memory-learning-cards` | 否 | 输出自包含 HTML，无构建步骤 |
| `image-gen-moda` | 是 | 需要 Python 和 `requests`，以及 ModelScope API Key |
| `mimo-tts` | 是 | 需要 Python 和 `openai`；`numpy`、`soundfile` 用于可选音频处理 |
| `haowallpaper-direct` | 是 | 使用 Python 标准库完成页面解析和下载，无浏览器自动化依赖 |

## Skill 说明

### extract-md

`extract-md` 用于从网页、微信公众号或其他复制来源中提取真正的正文内容，去掉评论区、广告、关注引导、推荐阅读、版权声明等杂讯，并保存为干净的 Markdown 文件。

它体现的是**内容工程和信息清洗能力**：Agent 不只是机械复制文本，而是按“识别正文 → 删除杂讯 → 保留元信息 → 输出文件 → 反馈处理结果”的流程执行，适合整理资料、沉淀文章、构建个人知识库。

典型请求：

```text
帮我把这段公众号内容提取成干净的 Markdown。
去掉广告、评论和关注引导，只保留正文。
```

### writing-style-learner

`writing-style-learner` 会读取同一作者的多篇 Markdown 文档，从句式、用词、段落结构、修辞、标题、篇章结构、语气、读者互动等维度生成 `style-profile.md`。之后可以用这个风格画像来生成新内容，或把已有文章改写成目标风格。

它体现的是**结构化分析和风格迁移能力**：我把“写作风格”拆成可观察、可复查、可复用的分析维度，让 Agent 不停留在“更像一点”这种模糊要求上，而是能基于证据做风格模仿。

典型请求：

```text
分析这个文件夹里所有 md 的写作风格，生成 style-profile.md。
用这个 style-profile 把下面这篇文章改写成同一个作者的风格。
```

### html-beautiful-output

`html-beautiful-output` 会在复杂信息更适合视觉化呈现时，让 Agent 生成单文件、自包含、可直接浏览的 HTML 产物。它适合报告、方案、代码解释、PR Review、架构图、交互原型、决策矩阵、学习说明等场景。

它体现的是**信息设计和前端表达能力**：Skill 内置了清晰的输出契约、视觉风格、组件模式和质量检查规则，要求页面具备响应式布局、语义结构、必要交互和可追溯输入，而不是把 Markdown 粗暴塞进网页。

典型请求：

```text
把这份技术方案整理成一个可分享的 HTML 页面。
给这个 PR 做一个带结构图和重点说明的 HTML Review。
```

### memory-learning-cards

`memory-learning-cards` 会把概念、文章、考试材料、专业知识、流程或词汇转成记忆友好的学习卡片，通常输出为自包含 HTML 学习页面。它强调具体、可视化的记忆钩子，例如谐音拆解、故事链、类比映射、对比排除、数字挂钩等。

它体现的是**学习科学和交互体验设计能力**：我没有把学习卡片做成固定模板，而是根据材料规模和知识类型选择卡片、时间线、矩阵、搜索过滤、翻卡、进度等交互。核心目标是让学习者真正理解、记住、复习，而不是得到一堆漂亮但无效的卡片。

典型请求：

```text
把这章内容做成适合复习的记忆卡片。
帮我把这些英文单词做成带谐音记忆和例句的 HTML 卡片。
```

### image-gen-moda

`image-gen-moda` 通过 ModelScope API 调用文生图模型，支持 `Tongyi-MAI/Z-Image-Turbo` 和 `Tongyi-MAI/Z-Image`。脚本会提交异步任务、轮询生成状态，并把结果保存为本地图片。

它体现的是**第三方模型 API 集成能力**：Skill 把模型选择、参数传递、异步任务轮询、本地文件保存这些容易出错的步骤封装起来，让 Agent 可以稳定地把文本描述转换成图片资产。

示例：

```bash
python scripts/generate.py "a futuristic city at sunset" -m Tongyi-MAI/Z-Image-Turbo -o city.jpg
python scripts/generate.py "watercolor painting of mountains" -m Tongyi-MAI/Z-Image -o mountain.jpg -W 1024 -H 768
```

使用前需要在该 Skill 目录中准备本地配置：

```json
{"api_key": "your-modelscope-token"}
```

### mimo-tts

`mimo-tts` 通过小米 MiMo V2.5 TTS API 生成语音，支持预设音色、自然语言声音设计、音频样本克隆，以及唱歌等风格控制。它提供了脚本封装，也保留了直接 API 调用说明。

它体现的是**多模态音频生成和 API 适配能力**：Skill 把 OpenAI-compatible 接口、音色参数、风格指令、音频格式、base64 解码、本地文件输出等流程整理成可执行规范，让 Agent 可以完成从文案到声音资产的闭环。

示例：

```bash
python scripts/tts.py --text "你好，欢迎回来。" --voice 冰糖 --output hello.wav
python scripts/tts.py --text "Hey boss, guess what!" --style "Bright, excited tone" --voice Chloe
```

使用前需要配置本地 API Key。推荐使用环境变量或本地 `config.json`，不要提交真实密钥。

### haowallpaper-direct

`haowallpaper-direct` 用于在不启动浏览器自动化的情况下，直接解析 HaoWallpaper 的 SSR HTML、Meta 标签和公开媒体链接，抓取壁纸标题、标签、分类、分辨率、下载量、收藏量、图片/视频链接，并可选择下载到本地。

它体现的是**网页解析、数据抽取和自动化效率优化能力**：相比直接用浏览器点页面，这个 Skill 更快、更轻量，也更适合批量搜索、JSON 输出和下游脚本处理。同时它明确避开受保护接口，不伪造 token。

示例：

```bash
python scripts/haowallpaper_direct.py detail https://haowallpaper.com/homeViewLook/18970557135113600
python scripts/haowallpaper_direct.py search "flower" --pages 3 --rows 30 --limit 20
python scripts/haowallpaper_direct.py search "flower" --sources home,mobile,forum --format json
python scripts/haowallpaper_direct.py search "flower" --sources mobile --media video --download ./live-wallpapers
```

## 目录结构

```text
.
├── extract-md/
│   └── SKILL.md
├── writing-style-learner/
│   ├── SKILL.md
│   └── references/
├── html-beautiful-output/
│   └── SKILL.md
├── memory-learning-cards/
│   ├── skill.md
│   └── references/
├── image-gen-moda/
│   ├── SKILL.md
│   ├── config.json
│   └── scripts/
├── mimo-tts/
│   ├── SKILL.md
│   ├── config.json
│   ├── references/
│   └── scripts/
└── haowallpaper-direct/
    ├── SKILL.md
    ├── agents/
    └── scripts/
```

## 配置和安全

- `image-gen-moda` 和 `mimo-tts` 需要 API Key。请使用自己的本地配置或环境变量。
- 不建议把真实密钥提交到公开仓库。公开作品集里应只保留占位符、示例配置或说明文档。
- `haowallpaper-direct` 只解析公开页面和公开媒体链接，不应尝试绕过受保护接口。

## 结语

我相信，未来的工程师不只是调用模型的人，而是能够把模型能力、软件工程、产品判断和人的真实需求连接起来的人。Skills 是我探索这件事的一种方式：把一次次临时的灵感沉淀成可复用的流程，把模糊的问题拆成稳定的系统，把 AI 的生成能力落到真实可用的产物里。

技术的价值不止在于写出更快的脚本、更漂亮的页面或更聪明的自动化，也在于不断扩大一个人解决问题的半径。今天写下的每一个 Skill，都是向更远处搭的一小段路：通向更高效的工作流，更自由的创造方式，也通向我想成为的那种工程师——既能扎进细节，也始终看得见远方。
