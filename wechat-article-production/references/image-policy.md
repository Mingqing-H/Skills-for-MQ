# Image Policy

## Purpose

Images are evidence, scene, explanation, data, or emotional rhythm. Do not use irrelevant decoration.

## Priority

1. Verified online visual assets: stable direct image downloads first, then source-page extracted images (`og:image`, `twitter:image`, `srcset`, JSON-LD, visible `img` assets), official media/press-kit/report assets, and browser/page screenshots of the relevant online source when original image URLs are hidden or blocked. A saved asset counts only if it validates as an actual image, not an HTML/error/redirect page.
2. Generated image files for remaining slots where online acquisition cannot produce a suitable verified asset after direct download, source-page extraction, official asset search, and page-capture routes have been tried or judged unsuitable, and the user chooses generation.
3. Professional generation prompts only for remaining slots where online acquisition fails and generation is unavailable or the user chooses prompt-only.

Data charts from verified data remain allowed as article visuals when the article needs them; save the rendered chart file and cite the data source. Source cards are fallback evidence only, not a main visual strategy. Python/code rendering is allowed only for data-backed charts, not for ordinary article images.

## Online Acquisition Ladder

Use this order for ordinary article images and covers before generation:

1. **Stable direct image URL.** Prefer official image files, CDN assets with image headers, press-kit images, report chart images, and other URLs that can be saved and validated directly.
2. **Source-page extraction.** When the visible page has the right image but direct download gives HTML, inspect the page for `og:image`, `twitter:image`, `meta[property]`, `srcset`, JSON-LD, embedded media URLs, public CDN paths, and visible `img` elements. Try extracted candidates and validate them.
3. **Official or reliable asset alternatives.** Search the same source, official newsroom, media kit, product page, PDF report, documentation, or reliable image index for an equivalent visual. Use image search only as a way to locate source pages or stable asset URLs, not as an uncited black box.
4. **Browser/page capture.** If the online page itself is the evidence or the original image URL is hidden by scripts/hotlink protection, capture a clean screenshot of the relevant page area, interface, chart, headline, or announcement. Save it as an image file, cite the page URL, and mark the route as `page-capture` in the material list.
5. **Grouped fallback.** Only after the above online routes fail or are unsuitable should unresolved slots move to generated images or prompt-only placeholders.

## Download Validation Rule

- Direct download is an attempt to save a real image file, not a webpage. Prefer URLs whose path, headers, or source context indicate an actual image asset. Be cautious with hotlink blockers, CDN redirectors, anti-bot pages, and article pages that require scripts to expose image URLs; when this happens, move to source-page extraction or page capture instead of repeatedly downloading the same page.
- After every download, validate the saved file before treating it as usable. Check content type when available and inspect the file signature/first bytes or use an image-identification command when practical. Valid examples include PNG, JPG/JPEG, WebP, GIF, and other browser-usable image formats.
- Invalid examples include HTML, JSON, XML, text, redirect pages, access-denied pages, login pages, 1x1 tracking pixels, tiny placeholders, or files whose extension says image but whose content is not an image.
- Delete invalid files immediately from `图片素材/YYYYMMDD/`, record the failed URL and reason in `素材清单.md`, and keep the slot unresolved.
- If several attempts for the same article produce HTML/error pages or no stable image URL can be isolated, stop spending time on forced downloads. Summarize the unresolved slots and switch to the grouped generated-image fallback when tooling is available.

## Two-Route Image Acquisition Rule

There are two final resolution routes for ordinary article images and covers, applied after the online acquisition ladder:

1. **Online acquired asset.** For every planned image slot, first use the online acquisition ladder: direct image URL, source-page extraction, official/reliable asset alternatives, then browser/page capture when appropriate. Save validated files into `图片素材/YYYYMMDD/`. Record source URL, publisher/page, accessed date, purpose, article position, acquisition route (`direct-url`, `extracted-url`, `official-alternative`, `pdf/report`, or `page-capture`), validation result, and any failure reason in `素材清单.md`. The acquired file must be referenced in the article Markdown immediately after it is available. Complete this acquisition pass before asking about prompts or generation, but do not keep retrying URLs that only save HTML/error pages.
2. **Grouped fallback: generated image or prompt.** After the download pass, summarize unresolved slots together, for example: `planned: 10; downloaded: 6; unresolved: 4`. Ask the user once, preferably in a popup/choice UI, whether unresolved slots should become directly generated images or prompt-only placeholders. If the user chooses direct generation, generate image files, save them, and reference them with Markdown image syntax. If the user chooses prompt-only, put the required prompt placeholder at each unresolved Markdown position.

- If direct downloading is blocked, unsuitable, legally risky, too low quality, or validates as non-image content, delete any failed local file, record the failed URL/attempt and reason in `素材清单.md`, and continue with extraction, official alternatives, or page capture before declaring the slot unresolved.
- A final article must not contain silent missing-image gaps. Every visual slot must have a downloaded file, generated file, chart file, or an explicitly user-approved prompt-only placeholder. Prompt-only placeholders should appear only for unresolved slots after the download pass and generation-capability check, not for slots where suitable online images were found.
- A long article should not rely mostly on source cards. Source cards are acceptable only when direct-download images and generated alternatives are unsuitable for that slot.
- Evidence assets should be edited with taste: crop to the meaningful region, prefer clear hero areas over full-page clutter, use clean margins, and avoid showing tiny text that readers cannot inspect.
- Pair evidence-heavy sections with occasional creative visuals from `image-prompt-patterns.md` so the article has rhythm, surprise, and visual memory, not only documentation.

## No Python Artwork Rule

- Do not use Python, SVG templates, PIL, matplotlib, browser canvas scripts, or ad hoc drawing code to generate ordinary article illustrations, covers, source cards, or decorative infographics.
- Route 2 means a real image generation model or a professional prompt placeholder, not a local Python drawing script.
- The only visual asset Python/code may render is a data-backed chart built from saved data, following `data-chart-policy.md`.
- If no suitable online image URL exists and no image-generation skill/tool is available, tell the user generation is unavailable and ask/confirm before using the prompt-only placeholder format; do not silently turn all images into prompts.

## Source Cards

- Do not put visible labels like `自制信息图`, `来源卡`, `本文整理`, or `AI 生成` inside the image unless required for legal clarity.
- Use natural editorial copy: a short headline, 2-4 concrete facts, source/date in a small footer.
- Keep text human and specific. Avoid generic AI-sounding phrases such as `重塑未来`, `赋能行业`, `全流程闭环`, `智能化升级` unless they are quoted from a source.
- Source cards are discouraged and must not be produced with ad hoc Python artwork. If a source card is unavoidable, keep it simple, editorial, and explicitly record why direct-download and generation routes were unsuitable.

## Cover Image

- Always prepare one cover image or cover prompt.
- First try online acquisition for the cover: direct image URL, extracted social preview image, official media asset, report/product image, or clean page capture. Validate the saved file as a real image. If online acquisition cannot produce a suitable cover, delete failed files, record failed attempts, and prefer direct generation. Use a prompt-only cover placeholder only if the user declines generation or no generation tool is available.
- Prefer 16:9 and include a 1:1 crop or square version.
- Make generated covers vivid, concrete, and visually surprising: show objects, people, scenes, or conflict, not generic glowing brains or abstract networks.
- Do not use real company logos in generated covers unless the user has rights and specifically requests it.
- If no generation tool is available, provide a professional prompt and a fallback web-image plan.

## Data Charts

- Do not invent precise data.
- Real charts may be code-rendered from saved data or directly downloaded from a source. This is the only approved use of Python/code for visual output.
- Label charts as `示意图` when using qualitative or illustrative values.
- Real charts must include title, units, source, and date range.
- Prefer line charts, bar charts, histograms, scatter plots, timelines, and small multiples over decorative infographics.


## Grouped Fallback Choice

When the whole-article online acquisition pass leaves unresolved slots, ask the user to choose for those unresolved slots together. Prefer a popup/choice UI when the runtime supports it; otherwise use a concise numbered question. Show the count and positions, for example: `Planned 10 images; downloaded 6; unresolved 4: section A, section C, section F, closing.`

Options:

- `direct-generate`: before generating, discover available image-generation skills. If one or more are available, list them and let the user choose which skill to use. If no image-generation skill exists, check whether a direct image-generation tool/capability is available. If a capability exists, ask for permission/choice when required, generate files, save them under `图片素材/YYYYMMDD/`, and reference them with Markdown image syntax.
- `prompt-only`: do not generate image files. Put a clear prompt placeholder at each unresolved Markdown image position, and record each prompt in `素材清单.md`.

If the user chooses `direct-generate` but no image-generation skill or capability is available, say generation is unavailable and use prompt-only placeholders for the unresolved slots. Direct URL downloads and code-rendered charts must still be created or referenced as files whenever possible; this choice never applies to slots where a suitable downloadable image exists.

Prompt-only Markdown format:

`[生图提示词：用�?位置；Prompt: ...；建议比例：16:9 �?1:1；风格：...；负面约束：...]`

Do not use broken Markdown image references for prompt-only generated images, because no local file exists yet. If direct generation is chosen, do not leave a prompt placeholder; create the file and use a normal Markdown image reference.

## Generated Image Text Language

This rule applies only to directly generated image files. It does not constrain downloaded/online-acquired assets, page captures, charts copied from sources, or prompt-only placeholders.

- Before generating an image, decide whether the image should contain visible text at all. Prefer no baked-in text when the text can be added later in Markdown, HTML, the WeChat editor, or a design tool.
- When generated visible text is needed, choose the text language from the article context, target reader, source domain, and image purpose. For a Chinese WeChat article, default generated text should usually be Chinese or bilingual Chinese-first, especially for covers, section cards, explanatory scenes, and article-native labels.
- Use English when the generated image intentionally depicts an English product interface, paper title, model name environment, international conference/poster style, code screen, or source context where English is natural.
- Mixed Chinese and English is allowed when the article itself uses bilingual terms or when English product/model names need to remain recognizable beside Chinese explanatory text.
- Put the chosen language preference explicitly in each direct-generation prompt, for example: `visible text: none`, `visible text language: Simplified Chinese`, `visible text language: Chinese-first bilingual`, or `visible text language: English for UI fragments only`.
- Add a negative constraint against unwanted language drift, such as `no random English words`, `no garbled Chinese characters`, or `do not invent unreadable text`, based on the chosen language.
## Interesting Image Rule

Generated and curated visuals should be interesting, not merely decorative. Before finalizing the image plan, check whether the article includes a mix of visual roles: proof, explanation, humor/metaphor, data beauty, emotional pause, and closing resonance. If all planned visuals are screenshots, source cards, or generic tech images, revise the storyboard with stronger style routes from `image-prompt-patterns.md`.

## Generated Images

- Use generated images for cover, scene, metaphor, or emotional pause, not as proof that an event occurred.
- Before writing a direct-generation prompt, choose a `prompt_style_route` from `image-prompt-patterns.md` based on image intent. Prompt for specificity: concrete subject, environment, action, camera/framing, route-specific visual style, palette, lighting or texture, aspect ratio, visible-text language preference, and negative constraints.
- Avoid fake news screenshots, fake UI, fake logos, fake documents, fake charts, random English words in Chinese-context images, and garbled visible text in any language.
- Generated images should feel publishable: high resolution, strong composition, route-appropriate style, plausible details, no unreadable text. Do not use one generic style for every generated image when the article needs varied visual functions.

## WeChat editor compatibility

- For final WeChat Markdown/HTML packages, prefer PNG/JPG/WebP references. Keep SVG as editable source files only unless the user explicitly wants SVG.
- When self-made infographics are built as SVG, export them to PNG and update Markdown references before final delivery.

