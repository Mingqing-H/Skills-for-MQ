---
name: wechat-article-production
description: End-to-end WeChat Official Account article production for Chinese content workflows. Use when the user gives a topic and wants a publishable 微信公众号 article package, 爆款文, 选题深挖, writing in an optional style, image/storyboard planning, real downloaded assets, data-backed charts, cover and article images, review scoring, or optional HTML layout. Produces dated Markdown drafts, image material folders, material lists, and review reports; all external skills and image tools are optional enhancements, never hard dependencies.
---

# WeChat Article Production

## Purpose

Produce a complete WeChat Official Account article package from a topic: research, style-aware writing, visual planning, real/downloaded assets, data charts, review, iteration, and optional HTML. Keep the workflow usable even when helper skills, AI news skills, layout skills, or image-generation tools are missing.

## Default Deliverables

- Article Markdown: `文案创作/（YYYYMMDD）标题.md`
- Image folder: `图片素材/YYYYMMDD/`
- Material list: `图片素材/YYYYMMDD/素材清单.md`
- Review report: `文案创作/（YYYYMMDD）标题-评审报告.md`
- Optional HTML only when requested: `文案创作/（YYYYMMDD）标题-公众号导入版.html`

## Core Workflow

1. **Clarify only high-impact preferences.** A topic is enough. Infer date from current date. Ask only for missing choices that materially change the output, such as a required style, forbidden sources, generated-image mode, or whether HTML is required.
   - Treat one-off topics, user test cases, and acceptance examples as runtime inputs. Do not write them into this skill unless the user explicitly asks to update the reusable skill itself.
2. **Research before writing.** For recent AI, company, model, price, policy, people, legal, or product claims, verify specific dates and sources. If specialized news skills are unavailable, use ordinary web search, official sources, primary documents, and reliable media. If facts remain uncertain, downgrade the wording.
3. **Choose or infer style.** If a style profile exists, read it. If a style-learning skill is available and the user asks to learn a new style, it may be used. Otherwise follow `references/style-analysis-fallback.md`.
4. **Create a visual storyboard before drafting.** Use `references/visual-storyboard.md`, `references/image-policy.md`, and when charts are needed `references/data-chart-policy.md` to decide image count, real proof images, downloaded assets, code-rendered charts, cover, generated-image mode, and generated-image prompts.
5. **Write the article.** Use original expression. Do not copy reference samples. Include real Markdown image references when assets exist; otherwise include explicit pending placeholders and prompts.
6. **Build assets.** Try real downloads/screenshots first, create custom data charts from saved data with task-specific code, then handle generated images according to the selected mode: directly generate image files, or insert professional prompt-only placeholders in Markdown. Always create a cover plan. Store all assets and prompt records under the dated image folder and document source/use in the material list.
7. **Review and iterate.** Use `references/review-prompts.md`. Default gate is 85/100; if below 85, iterate up to 3 rounds unless the user stops.
8. **Generate HTML only on request.** Prefer any available layout skill. If unavailable, use `scripts/render_wechat_html.py` with `references/html-layout-fallback.md`. Preserve visible text.

## Optional Enhancements, Not Dependencies

- `writing-style-learner`: use only if available and helpful. Missing it is not an error.
- `aihot`: use only if available for recent AI news. Missing it is not an error.
- `wechat-article-layout`: use only if available for HTML layout. Missing it is not an error.
- Image generation tools: use only if available, permitted, and the selected mode is direct generation. Missing them is not an error; provide professional prompts and alternatives.

## Resource Routing

- Full workflow and file naming: `references/workflow.md`
- Research fallback and source hierarchy: `references/research-fallback.md`
- Style fallback: `references/style-analysis-fallback.md`
- Image rules, cover, and source tracking: `references/image-policy.md`
- Image count and storyboard rules: `references/visual-storyboard.md`
- Data chart rules and flexible chart-coding guidance: `references/data-chart-policy.md`
- Professional image prompt patterns: `references/image-prompt-patterns.md`
- Review agents and scoring: `references/review-prompts.md`
- Artifact format standards: `references/artifact-standards.md`
- HTML fallback rules: `references/html-layout-fallback.md`
- HTML fallback renderer: `scripts/render_wechat_html.py`

## Required Quality Gates

- Dates, source names, model/product names, prices, laws, financing, and claims of "latest" must be checked.
- Image count must match article length; long articles cannot be mostly text.
- Final images should not be dominated by source cards or generic SVG-style cards; prefer real downloaded/screenshotted assets and code-rendered data charts when possible.
- Data-backed charts must be rendered from saved data files and cited sources; illustrative charts must be labeled as such.
- At least one cover image or cover prompt is required.
- Generated-image mode must be explicit when generated images are planned: direct-generate image files, or prompt-only placeholders for the user to generate later.
- Material list must say filename, type, source, purpose, article position, and whether it is cover.
- Review report must include scores, issues, changes, and final status.
- HTML, if produced, must not rewrite visible article text.




