# Visual Storyboard

## Image Count by Length

- 1500 Chinese characters or fewer: cover + 3-4 article images or material callouts.
- 1500-3000 Chinese characters: cover + 5-7 article images or material callouts.
- 3000-5000 Chinese characters: cover + 8-11 article images or material callouts.
- 5000-7000 Chinese characters: cover + 11-14 article images or material callouts.
- 7000+ Chinese characters: cover + 14-18 article images or material callouts, or recommend splitting into two articles.

Default rhythm: one visual or material break every 350-600 Chinese characters or every 3-5 short paragraphs. Use denser visual support for research-heavy, case-heavy, list-style, or data-backed articles.

## Required Mix

- Cover image downloaded from a suitable online URL, or generated cover file after direct download is unsuitable. Use a cover prompt only if generation is unavailable or declined.
- Opening downloaded real visual, or generated scene image after direct download is unsuitable. Use an opening prompt-only placeholder only if generation is unavailable or declined.
- At least one framework/overview graphic or source-backed structure card.
- At least one real proof image, page capture, report/table screenshot, product/interface screenshot, or cited material callout for every major case or section when available.
- At least one code-rendered data chart for analytical articles over 3000 Chinese characters when numeric claims are central.
- One closing or summary visual for long essays.
- For every major argument, include at least one reader-visible anchor: source quote, data point, screenshot, chart, page capture, report excerpt, product/interface visual, or generated non-evidence metaphor.
- Every article must include at least 2-3 visually interesting moments, not only utilitarian evidence: a strong cover, a clever metaphor, a memorable generated scene, a beautiful data visual, a poetic pause, or a sharp editorial collage.

## Mix Guardrails

- Every image/material slot must first attempt online acquisition when it needs source-backed visuals, following `image-policy.md`, and record the outcome.
- Directly downloaded, extracted, captured, or source-backed materials should usually account for at least 50% of正文图片/material callouts in research-heavy articles, unless sources are unavailable or legally risky.
- Generated images are the preferred fallback after direct download is unsuitable. Prompt-only placeholders require explicit user choice after the download pass and should stay rare, limited to unresolved slots, and usually below 20% of正文图片.
- Source cards and material callouts should supplement evidence and improve scanability. Do not let generic source cards dominate the article, but do use concise cited callouts when a paragraph would otherwise be unsupported opinion.
- Evidence visuals still need editorial taste: crop page captures to the relevant area, avoid tiny unreadable screenshots, group related materials into a clean collage when useful, and alternate source-heavy anchors with visually fresh generated metaphors or diagrams.
- Do not satisfy the image quota with boring screenshots alone. The visual plan should create curiosity, surprise, clarity, or emotional pacing.
- SVG may be used during design, but final Markdown should reference PNG/JPG/WebP.

## Generated Image Style Routing

When a slot may become directly generated after online acquisition fails, assign a provisional `prompt_style_route` from `image-prompt-patterns.md` during storyboard planning. Choose the route from image intent, not personal habit. Examples: pun or light satire -> `inspirational_comic_pun`; public crackdown or justice impact -> `mythic_justice_impact`; data/trend concept -> `data_analysis_beauty`; future-facing closing -> `open_grand_horizon`; poetic pause -> `minimal_eastern_digital_watercolor` or `oriental_ink_xiaopin`; cultural/hot-topic punch -> `magazine_halftone`; mechanism explanation -> `premium_3d_concept`, `technical_teardown_isometric`, or `clean_explainer_frame`; product/tool focus -> `product_brand_still_life`; process/change -> `storyboard_sequence`; multi-case summary -> `social_card_collage`; ordinary-life observation -> `warm_lifestyle_observation`; abstract risk/metaphor -> `surreal_object_metaphor`.

## Material Anchor Types

Use a mix of anchor types so the article feels researched and visually alive:

- `proof_image`: official image, product photo, interface screenshot, announcement image, page capture.
- `source_quote`: short cited quote or excerpt from a primary/reliable source.
- `data_chart`: code-rendered or source-downloaded chart from verified data.
- `report_table`: table/report excerpt, preferably with source/date visible or cited nearby.
- `case_card`: concise source-backed card for a case, person, product, policy, or timeline point.
- `generated_metaphor`: non-evidence visual used for mood, explanation, humor, or transition.

## Storyboard Table

Use this planning table before writing:

| position | section | anchor type | evidence grade | purpose | source/generation/data plan | prompt_style_route | filename/prompt | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Evidence grade examples: `direct-url downloaded`, `source chart downloaded`, `code-rendered chart`, `generated scene direct`, `prompt-only unresolved fallback`, `source-card fallback`.

## For 5-Industry Articles

- Cover: concrete visual metaphor for five industries, not generic AI abstraction.
- Overview: one industry map or matrix.
- Per industry: first try one direct-download proof image URL, such as official page image, product photo, news title image/screenshot source, report chart, or interface image. If unavailable after the whole-article download pass, include it in the grouped fallback choice; for major proof slots, prefer downloaded evidence, downloaded source charts, or a generated non-evidence scene rather than prompt-only.
- Data/structure: at least one code-rendered line chart, bar chart, histogram, timeline, or workflow diagram. Prefer data-backed charts over decorative SVG.
- Closing: one summary quote/card or future map.

