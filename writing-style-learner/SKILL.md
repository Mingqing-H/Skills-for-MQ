---
name: writing-style-learner
description: "Analyze writing style from multiple markdown documents by the same author and generate a reusable style profile. Use when: (1) user provides a folder or multiple .md files and asks to learn/analyze writing style, (2) user wants to mimic a specific author's style for new content, (3) user wants to rewrite existing content to match a target style, (4) user mentions learn style, analyze writing style, style profile, mimic writing, 模仿写作风格, 学习写作风格, 风格分析"
---

# Writing Style Learner

Analyze writing style from multiple documents by the same author, generate a comprehensive style profile, and use it to create new content or rewrite existing content.

## Workflow

### 1. Determine Task Type

**Analyzing style?** → Follow "Analysis workflow" below
**Generating new content with a style?** → Follow "Generation workflow" below
**Rewriting content to match a style?** → Follow "Rewrite workflow" below

### 2. Analysis Workflow

1. **Collect source documents**: Use Glob to find all `.md` files in the user-specified folder, or accept explicit file list
2. **Read documents**: Read all source documents (use Read tool, read in parallel when possible)
3. **Analyze style**: Follow the analysis dimensions in [references/style-dimensions.md](references/style-dimensions.md) to systematically analyze the author's writing style
4. **Generate style profile**: Write `style-profile.md` using the template below

### 3. Generation Workflow

1. **Load style profile**: Read the existing `style-profile.md` file (ask user for path if not specified)
2. **Understand requirements**: Clarify what content to generate (topic, length, purpose)
3. **Generate content**: Write new content strictly following the style profile's characteristics
4. **Self-check**: Verify the output matches the style profile before presenting

### 4. Rewrite Workflow

1. **Load style profile**: Read the existing `style-profile.md` file
2. **Read source content**: Read the content to be rewritten
3. **Rewrite**: Transform the content to match the target style while preserving the original meaning
4. **Self-check**: Verify the output matches the style profile

## Style Profile Template

Generate `style-profile.md` with this structure:

```markdown
# 写作风格分析报告

## 作者概况
- **分析样本**: [N] 篇文档，共 [M] 字
- **写作类型**: [技术博客/随笔/教程/...]
- **整体印象**: [一句话概括]

## 句式特征
- **平均句长**: [短句为主/长句为主/长短交替]
- **句式偏好**: [陈述句/疑问句/感叹句的比例]
- **复合句使用**: [简单/适中/复杂]
- **典型句式**: [列举 2-3 个典型句式模板]

## 用词习惯
- **词汇层次**: [口语化/书面化/混合]
- **专业术语**: [密集/适中/稀少]
- **形容词偏好**: [列举常用形容词]
- **动词偏好**: [列举常用动词]
- **特色用词**: [作者独特的用词或口头禅]

## 段落结构
- **段落长度**: [短段落/长段落/混合]
- **段落组织**: [总分总/递进/并列/...]
- **过渡方式**: [词语过渡/句子过渡/无明显过渡]

## 修辞手法
- **比喻**: [频率和风格]
- **排比**: [频率和风格]
- **反问/设问**: [频率]
- **引用**: [频率和来源偏好]
- **其他手法**: [列举]

## 标点与格式
- **标点偏好**: [列举特殊标点使用习惯]
- **列表使用**: [有序/无序/混合，频率]
- **代码块**: [频率，语言偏好]
- **强调方式**: [粗体/斜体/大写/...]
- **标题风格**: [层级结构，命名习惯]

## 篇章结构
- **开头方式**: [直接切入/提问/故事/引用/...]
- **结尾方式**: [总结/展望/提问/戛然而止/...]
- **逻辑线索**: [时间线/因果/问题-解决/...]
- **节奏感**: [快节奏/慢节奏/张弛有度]

## 情感与语气
- **整体语气**: [正式/轻松/幽默/严肃/...]
- **情感表达**: [直接/含蓄/克制/...]
- **读者互动**: [频繁/偶尔/无]

## 典型表达模式
[列举 3-5 个该作者最典型的表达模式，每个配一个原文示例]

1. **[模式名称]**: [示例]
2. **[模式名称]**: [示例]
3. **[模式名称]**: [示例]

## 写作建议
[基于分析，给出 3-5 条模仿该风格的关键建议]
```

## Important Notes

- Read at least 3 documents for reliable analysis; more is better
- Use Chinese for the style profile if the source documents are primarily in Chinese
- Include concrete examples from the source documents in the profile
- When generating or rewriting, prioritize the "典型表达模式" and "写作建议" sections
- If the user provides fewer than 2 documents, warn that the analysis may not be representative
