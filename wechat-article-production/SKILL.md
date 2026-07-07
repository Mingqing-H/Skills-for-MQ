---
name: wechat-article-production
description: End-to-end WeChat Official Account article production for Chinese content workflows. Use when the user gives a topic and wants a publishable 寰俊鍏紬鍙?article package, 鐖嗘鏂? 閫夐娣辨寲, pre-writing style selection with reference article links, writing in a selected style, image/storyboard planning, real downloaded assets, data-backed charts, cover and article images, review scoring, or optional HTML layout. Produces dated Markdown drafts, image material folders, material lists, and review reports; all external skills and image tools are optional enhancements, never hard dependencies.
---

# WeChat Article Production

## Purpose

Produce a complete WeChat Official Account article package from a topic: research, topic-aware style selection, style-aware writing, visual planning, real/downloaded assets, data charts, review, iteration, and optional HTML. Keep the workflow usable even when helper skills, AI news skills, layout skills, or image-generation tools are missing.

## Default Deliverables

- Article Markdown: `鏂囨鍒涗綔/锛圷YYYMMDD锛夋爣棰?md`
- Image folder: `鍥剧墖绱犳潗/YYYYMMDD/`
- Material list: `鍥剧墖绱犳潗/YYYYMMDD/绱犳潗娓呭崟.md`
- Review report: `鏂囨鍒涗綔/锛圷YYYMMDD锛夋爣棰?璇勫鎶ュ憡.md`
- Optional HTML only when requested: `鏂囨鍒涗綔/锛圷YYYMMDD锛夋爣棰?鍏紬鍙峰鍏ョ増.html`

## Core Workflow

1. **Clarify only high-impact preferences.** A topic is enough. Infer date from current date. Ask only for missing choices that materially change the output before research, such as forbidden sources, required audience, or whether HTML is required. Do not ask for writing style here unless the user already has a required style.
   - Treat one-off topics, user test cases, and acceptance examples as runtime inputs. Do not write them into this skill unless the user explicitly asks to update the reusable skill itself.
2. **Research before writing.** For recent AI, company, model, price, policy, people, legal, or product claims, verify specific dates and sources. Build a source-rich material pack with enough reader-visible anchors: source quotes, dated facts, charts, page captures, product/interface visuals, report excerpts, tables, or case links. If specialized news skills are unavailable, use ordinary web search, official sources, primary documents, and reliable media. If facts remain uncertain, downgrade the wording.
3. **Run the style selection gate.** After topic analysis and before drafting, use `references/style-selection.md` to present 4-6 suitable writing styles, preferably with verified original reference links. Use a UI choice prompt when available; otherwise ask with a concise numbered list. Do not draft until the user selects a style or explicitly delegates the choice.
4. **Analyze the selected style.** If a style profile exists, read it. If a style-learning skill is available and the user asks to learn a new style, it may be used. Otherwise follow `references/style-analysis-fallback.md`.
5. **Create a visual storyboard before drafting.** Use `references/visual-storyboard.md`, `references/image-policy.md`, and when charts are needed `references/data-chart-policy.md` to decide a source-rich visual rhythm: image/material-callout count, real proof images, source quotes, online asset acquisition routes, page-capture fallbacks, code-rendered charts, cover, and any unresolved fallback slots that may need generated images or prompts after online acquisition fails.
6. **Write the article.** Use original expression. Do not copy reference samples. Every planned image position must resolve to a real Markdown image reference whenever a downloaded, generated, or chart file exists. Prompt-only placeholders are allowed only for unresolved fallback slots after the whole-article download pass fails to find suitable images and the user chooses prompt-only.
7. **Build assets.** First complete a whole-article online image acquisition pass for all planned image slots. Prefer verified direct image downloads, but when direct image URLs are hidden or blocked, try source-page extraction (`og:image`, `twitter:image`, `srcset`, JSON-LD, visible `img` assets, official media/press kits, report PDFs, or search-result image previews) and browser/page screenshots of the relevant online source before declaring the slot unresolved. Verify every saved file is a real image, delete failed HTML/error-page files immediately, and record the route used. After the pass, summarize remaining missing slots together, for example "10 planned images, 6 online assets captured, 4 missing". For unresolved slots, ask the user in a popup/choice UI when available whether to direct-generate images or use prompt-only placeholders. If online acquisition repeatedly returns HTML/error pages and page capture is unsuitable, treat the online route as failed for those slots, clean failed files, and move them to direct generation when tooling is available. If the user chooses generation, first discover available image-generation skills and let the user choose one when multiple exist; if no skill exists, check for direct image-generation capability/tooling; if neither exists, tell the user generation is unavailable and fall back to prompt-only placeholders. Generated files must be saved and referenced with Markdown image syntax. Prompt-only placeholders are allowed only for unresolved slots after this process. Do not use Python/code scripts to create ordinary illustrations, covers, source cards, or decorative infographics. Use task-specific code only for data-backed charts from saved data. Always create a cover plan and document source/use in the material list.
8. **Review and iterate.** Use `references/review-prompts.md`. Default gate is 90/100 for every required review; if any required review is below 90, keep iterating and re-reviewing until all pass or the user explicitly stops.
9. **Generate HTML only on request.** Prefer any available layout skill. If unavailable, use `scripts/render_wechat_html.py` with `references/html-layout-fallback.md`. Preserve visible text.

## Optional Enhancements, Not Dependencies

- `writing-style-learner`: use only if available and helpful. Missing it is not an error.
- `aihot`: use only if available for recent AI news. Missing it is not an error.
- `wechat-article-layout`: use only if available for HTML layout. Missing it is not an error.
- Image generation tools: use after the whole-article online image acquisition pass leaves unresolved slots, or after direct download, source-page extraction, and page-capture routes cannot produce usable online visuals. Python/code scripts are not image-generation tools for this skill. Missing image-generation tools is not an error; ask before falling back to prompt-only.

## Resource Routing

- Full workflow and file naming: `references/workflow.md`
- Research fallback and source hierarchy: `references/research-fallback.md`
- Style selection menu and reference-link rules: `references/style-selection.md`
- Style fallback: `references/style-analysis-fallback.md`
- Image rules, cover, and source tracking: `references/image-policy.md`
- Image count and storyboard rules: `references/visual-storyboard.md`
- Data chart rules and limited chart-coding guidance: `references/data-chart-policy.md`
- Professional image prompt patterns: `references/image-prompt-patterns.md`
- Review agents and scoring: `references/review-prompts.md`
- Artifact format standards: `references/artifact-standards.md`
- HTML fallback rules: `references/html-layout-fallback.md`
- HTML fallback renderer: `scripts/render_wechat_html.py`

## Required Quality Gates

- Dates, source names, model/product names, prices, laws, financing, and claims of "latest" must be checked.
- Personal scenes, anecdotes, reflections, and strong claims must pass narrative credibility review: avoid big talk, staged-feeling scenes, and anecdotes that feel psychologically fabricated even if technically possible.
- Image and material-anchor count must match article length; long articles cannot be mostly text or unsupported commentary. Use enough images, charts, source quotes, page captures, report excerpts, product/interface visuals, tables, and cited callouts to keep readers curious and grounded. These visuals must also be interesting: combine evidence with memorable metaphors, beautiful data visuals, poetic pauses, clever editorial collages, or route-specific generated scenes instead of filling the article with boring screenshots.
- Every image slot must first attempt online image acquisition before generation: stable direct image URL download when available, source-page extraction when direct URLs are hidden, official media/press-kit/report assets when applicable, and browser/page screenshot capture when the online page itself is the best available visual evidence. A saved file counts as acquired only after validation confirms it is an actual PNG/JPG/WebP/GIF or other browser-usable image, not HTML, JSON, XML, a redirect page, an access-denied page, or a tiny error placeholder. Prompt-only is never the default and must not be selected globally before the acquisition pass. Only after the whole-article online acquisition pass may unresolved slots be grouped and shown to the user for direct-generation vs prompt-only choice.
- If direct download repeatedly saves HTML/error pages or cannot expose stable image URLs, clean failed files from the material folder, record the failed attempts, then try source-page extraction and page capture. Switch those slots to grouped generated-image fallback only after these online acquisition routes are unsuitable or fail.
- Downloaded, generated, and chart images must be referenced in the final Markdown immediately after creation; generated images must not be represented only by prompts. A finished article should use downloaded images wherever suitable links were found.
- Directly generated images must choose a `prompt_style_route` from `references/image-prompt-patterns.md` based on the image intent, such as pun/comic, mythic justice impact, data analysis, grand horizon, Eastern watercolor, ink vignette, magazine halftone, cinematic editorial, 3D concept, clean explainer, technical teardown, product still life, poster layout, social-card collage, storyboard sequence, warm lifestyle observation, or surreal object metaphor. Do not use one generic prompt style for every generated image.
- Directly generated images must explicitly choose visible-text language based on article context and image purpose. For Chinese WeChat articles, prefer no baked-in text or Simplified Chinese/Chinese-first bilingual text unless the image intentionally depicts an English-native UI, paper, code, conference, product, or source context. This rule applies only to direct generation, not downloaded assets, page captures, charts from sources, or prompt-only placeholders.
- Final images should not be dominated by source cards, generic SVG-style cards, or Python-drawn decorative graphics; prefer real downloaded assets and data-backed charts when needed.
- Data-backed charts may be rendered with code from saved data files and cited sources; this is the only Python/code visual-generation exception. Illustrative charts must be labeled as such.
- A cover must be a downloaded or generated image file whenever tools permit; a cover prompt is allowed only after direct-download failure and unavailable/declined generation.
- Route-2 fallback decisions must be explicit for the grouped unresolved slots: direct-generate image files, or prompt-only placeholders for the user to generate later. If direct generation is chosen, image-generation skill/tool availability must be checked first and reported.
- Selected writing style must be chosen after topic analysis and before drafting, with reference links recorded when available.
- Material list must say filename, type, source, purpose, article position, whether it is cover, and whether the material is a reader-visible evidence anchor or background-only citation.
- Review report must include selected style, reference links used, scores, issues, changes, every iteration round, fixed reviewer names (`青天案牍`, `哪吒巡街`, `马良神笔`, `太史公烛照`, `雪芹总校`) with their reviewer_id values, and final status. Final status can be "pass" only when every required reviewer score is at least 90/100.
- HTML, if produced, must not rewrite visible article text.




