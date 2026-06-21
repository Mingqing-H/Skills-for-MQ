# Image Policy

## Purpose

Images are evidence, scene, explanation, data, or emotional rhythm. Do not use irrelevant decoration.

## Priority

1. Directly downloaded or captured real materials: official announcements, product pages, screenshots, interfaces, news headlines, official photos, press kits.
2. Code-rendered data charts from verified data. See `data-chart-policy.md`.
3. Real data visualizations from primary or reliable sources, with source/date preserved.
4. Generated images for cover, vivid scene, metaphor, or emotional pause.
5. Source cards only as fallback evidence, not as the main visual strategy.

## Download-First Rule

- For every major case, first try to obtain a real visual: official image, product page screenshot, press image, chart, report table, or news headline screenshot.
- If downloading or screenshotting is blocked, record the failed attempt in `素材清单.md` and provide a manual source URL.
- A long article should not rely mostly on source cards. Source cards are acceptable only when real visuals are unavailable or legally risky.

## Source Cards

- Do not put visible labels like `自制信息图`, `来源卡`, `本文整理`, or `AI 生成` inside the image unless required for legal clarity.
- Use natural editorial copy: a short headline, 2-4 concrete facts, source/date in a small footer.
- Keep text human and specific. Avoid generic AI-sounding phrases such as `重塑未来`, `赋能行业`, `全流程闭环`, `智能化升级` unless they are quoted from a source.
- Source cards must be exported to PNG for final delivery.

## Cover Image

- Always prepare one cover image or cover prompt.
- Prefer 16:9 and include a 1:1 crop or square version.
- Make generated covers vivid, concrete, and visually surprising: show objects, people, scenes, or conflict, not generic glowing brains or abstract networks.
- Do not use real company logos in generated covers unless the user has rights and specifically requests it.
- If no generation tool is available, provide a professional prompt and a fallback web-image plan.

## Data Charts

- Do not invent precise data.
- Real charts must be code-rendered from saved data or directly downloaded from a source.
- Label charts as `示意图` when using qualitative or illustrative values.
- Real charts must include title, units, source, and date range.
- Prefer line charts, bar charts, histograms, scatter plots, timelines, and small multiples over decorative infographics.


## Generated Image Mode

When the storyboard needs generated images, identify or ask for one of two modes:

- `direct-generate`: generate image files when tools and permissions are available, save them under `图片素材/YYYYMMDD/`, and reference them with Markdown image syntax.
- `prompt-only`: do not generate image files. Put a clear prompt placeholder at the exact Markdown image position, and record the prompt in `素材清单.md`.

If the user explicitly asks for finished image assets, use `direct-generate`. If the user says they will insert or generate images themselves, use `prompt-only`. If unclear and generated images materially affect the output, ask once. Real downloaded/screenshotted images, code-rendered charts, and official assets should still be created or referenced as files whenever possible; this choice only controls generated images.

Prompt-only Markdown format:

`[生图提示词：用途/位置；Prompt: ...；建议比例：16:9 或 1:1；风格：...；负面约束：...]`

Do not use broken Markdown image references for prompt-only generated images, because no local file exists yet.
## Generated Images

- Use generated images for cover, scene, metaphor, or emotional pause, not as proof that an event occurred.
- Prompt for specificity: concrete subject, environment, action, camera/framing, visual style, palette, lighting, aspect ratio, and negative constraints.
- Avoid fake news screenshots, fake UI, fake logos, fake documents, and fake charts.
- Generated images should feel publishable: high resolution, strong composition, plausible details, no unreadable text.

## WeChat editor compatibility

- For final WeChat Markdown/HTML packages, prefer PNG/JPG/WebP references. Keep SVG as editable source files only unless the user explicitly wants SVG.
- When self-made infographics are built as SVG, export them to PNG and update Markdown references before final delivery.

