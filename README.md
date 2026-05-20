# Mingqing Skills

5 个为 AI Agent 设计的 Skill，覆盖文本处理、图像生成、语音合成、壁纸搜索、写作风格分析。

> 适用于 Claude Code、Cursor、Copilot 等支持 Skill / 自定义指令的 AI Agent。

## Skills 一览

| Skill | 功能 | 依赖 |
|-------|------|------|
| **extract-md** | 从网页/公众号内容中提取正文，去除广告评论，生成干净 Markdown | 无 |
| **image-gen-moda** | 通过 ModelScope API 文生图，支持 turbo/zimage 两个模型 | Python, `requests` |
| **mimo-tts** | 小米 MiMo TTS 语音合成，支持预设音色、声音设计、声音克隆 | Python, `openai` |
| **haowallpaper-search** | 从 haowallpaper.com 按热度搜索壁纸，获取直链 | Playwright MCP |
| **writing-style-learner** | 分析多篇文档的写作风格，生成风格画像，用于模仿写作或改写 | 无 |

## 安装

### 方式一：AI Agent 一键安装（推荐）

复制下方提示词粘贴给你的 AI Agent，即可自动完成安装。

#### 安装全部 Skill

```
请从 https://github.com/Mingqing-H/mingqing_skills 克隆仓库，将所有 skill 安装到我的 Agent 技能目录。步骤：
1. git clone https://github.com/Mingqing-H/mingqing_skills.git 到临时目录
2. 解压 image-gen-moda.skill 和 mimo-tts.skill（它们是 zip 格式）
3. 将 extract-md、haowallpaper-search、writing-style-learner、image-gen-moda、mimo-tts 这 5 个目录复制到 ~/.claude/skills/（全局）或当前项目的 .claude/skills/ 下
4. 删除临时克隆目录
5. 完成后告诉我已安装了哪些 skill
```

#### 按需安装单个 Skill

按需复制对应提示词，只装你需要的：

**extract-md** — 网页/公众号正文提取

```
请从 https://github.com/Mingqing-H/mingqing_skills 克隆仓库，将 extract-md skill 安装到 ~/.claude/skills/（全局）或当前项目的 .claude/skills/ 下，然后删除临时克隆目录。
```

**image-gen-moda** — ModelScope 文生图

```
请从 https://github.com/Mingqing-H/mingqing_skills 克隆仓库，将 image-gen-moda.skill 解压（zip 格式），把解压后的 image-gen-moda 目录安装到 ~/.claude/skills/（全局）或当前项目的 .claude/skills/ 下，然后删除临时克隆目录。
```

**mimo-tts** — MiMo 语音合成

```
请从 https://github.com/Mingqing-H/mingqing_skills 克隆仓库，将 mimo-tts.skill 解压（zip 格式），把解压后的 mimo-tts 目录安装到 ~/.claude/skills/（全局）或当前项目的 .claude/skills/ 下，然后删除临时克隆目录。
```

**haowallpaper-search** — 壁纸搜索

```
请从 https://github.com/Mingqing-H/mingqing_skills 克隆仓库，将 haowallpaper-search skill 安装到 ~/.claude/skills/（全局）或当前项目的 .claude/skills/ 下，然后删除临时克隆目录。注意：此 skill 需要 Playwright MCP 服务。
```

**writing-style-learner** — 写作风格分析

```
请从 https://github.com/Mingqing-H/mingqing_skills 克隆仓库，将 writing-style-learner skill 安装到 ~/.claude/skills/（全局）或当前项目的 .claude/skills/ 下，然后删除临时克隆目录。
```

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/Mingqing-H/mingqing_skills.git
cd mingqing_skills

# 解压 .skill 文件（zip 格式）
python -c "
import zipfile
for f in ['image-gen-moda.skill', 'mimo-tts.skill']:
    zipfile.ZipFile(f).extractall('.')
"

# 复制到 Claude Code 全局技能目录
# macOS / Linux:
cp -r extract-md haowallpaper-search writing-style-learner image-gen-moda mimo-tts ~/.claude/skills/

# Windows (PowerShell):
Copy-Item -Recurse extract-md,haowallpaper-search,writing-style-learner,image-gen-moda,mimo-tts ~/.claude/skills/
```

## 配置

部分 Skill 需要 API Key，请在对应目录下创建或编辑 `config.json`：

**image-gen-moda** — ModelScope API Token:

```json
{
  "api_key": "your-modelscope-token"
}
```

获取方式：前往 [ModelScope](https://modelscope.cn) 注册并创建 API Token。

**mimo-tts** — 小米 MiMo TTS API Key:

```json
{
  "api_key": "your-mimo-api-key"
}
```

获取方式：前往 [小米 MiMo 开放平台](https://mimodel.xiaomi.com) 申请 API Key。

> 也可以通过环境变量 `MIMO_API_KEY` 传入，优先级高于 `config.json`。

## Skill 详细说明

### extract-md

从粘贴的网页/公众号原始内容中提取正文，自动去除评论区、广告、引导关注等杂讯，输出干净的 `.md` 文件。

**触发方式：** "帮我提取正文"、"把这段内容整理成 md"、"去掉评论和广告"

**特点：**
- 保留文章标题和完整正文，不改动原文
- 自动过滤评论、打赏、公众号引导关注等噪音
- 保留元信息（题图说明、创作者信息等）

---

### image-gen-moda

通过 ModelScope 文生图 API 将文字描述转为图片。

**触发方式：** "帮我画一张..."、"生成一张图片..."、"draw/generate an image..."

**支持模型：**

| 模型 | 说明 |
|------|------|
| `turbo` (Z-Image-Turbo) | 快速生成 |
| `zimage` (Z-Image) | 标准质量 |

**用法：**

```bash
python scripts/generate.py "赛博朋克风格的城市夜景" -m Tongyi-MAI/Z-Image-Turbo -o city.jpg
```

---

### mimo-tts

小米 MiMo V2.5 语音合成，支持三种模式：

| 模式 | 说明 |
|------|------|
| **预设音色** | 晓晓、云健、Mia 等内置音色 |
| **声音设计** | 用文字描述想要的声音特征 |
| **声音克隆** | 从一段音频样本克隆音色 |

**触发方式：** "把这段文字转语音"、"TTS"、"语音合成"、"用 XX 的声音读出来"

**支持风格控制：** 可通过自然语言或音频标签控制语气（开心/悲伤/愤怒/耳语等）

**用法：**

```bash
python scripts/tts.py --text "你好世界" --voice 晓晓 --output hello.wav
```

---

### haowallpaper-search

从 haowallpaper.com 搜索高质量壁纸，按热度排序，获取直链下载地址。

**触发方式：** "找几张 XX 的壁纸"、"搜索 XX 主题的高清壁纸"

**特点：**
- 按下载量/热度排序
- 提供直链图片地址（非页面链接）
- 支持指定数量和分辨率

> 需要安装 [Playwright MCP](https://github.com/anthropics/claude-code/blob/main/docs/mcp.md) 服务。

---

### writing-style-learner

分析多篇文档的写作风格，生成结构化风格画像，可用于模仿写作或改写现有内容。

**触发方式：** "分析这些文章的写作风格"、"学习 XX 的写作风格"、"模仿这个风格写一篇..."

**三种工作流：**

1. **分析** — 输入多篇文档，输出 `style-profile.md` 风格画像
2. **生成** — 基于风格画像生成新内容
3. **改写** — 将已有内容改写为目标风格

**分析维度：** 句式特征、用词习惯、段落结构、修辞手法、标点格式、篇章结构、情感语气、读者互动等 10 个维度。

## 许可

MIT
