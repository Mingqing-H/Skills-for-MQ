# Workflow

## 1. Input Handling

- Accept a topic as sufficient input.
- Infer date from current date and use `YYYYMMDD`.
- Optional inputs: user-required style, sample files, audience, word count, HTML requirement, source preferences. Do not ask for a global generated-image mode up front. Ask about generation vs prompt-only only after the whole-article online image acquisition pass is complete and unresolved slots are known. If the user does not provide a required style, select style after topic analysis.
- If the user asks for "latest", "today", "recent", "鍒氬垰", or modern company/model facts, research before writing.

## 2. Research

- Build a source-rich material pack before drafting: official pages, primary docs, reliable media, papers, product pages, user-provided files, and visual/material candidates that can become reader-visible anchors.
- Record source title, URL, publisher, publication date, accessed date, exact claim supported, and whether it should become a reader-visible anchor such as image, chart, page capture, quote, table, report excerpt, or case card.
- Separate confirmed facts, reported claims, expert opinions, and your analysis.
- Do not use unverified rumors as hard facts.

## 3. Style Selection Gate

- After research/topic analysis and before the article plan, read `style-selection.md`.
- Present 4-6 suitable writing style choices to the user, preferably with verified original article links or public author/publication links for reference.
- Use a UI choice prompt when available; otherwise use a concise numbered list.
- Include an automatic recommendation option with a reason.
- Do not draft until the user selects a style or explicitly delegates the choice.
- Record `selected_style`, `why_this_style`, `reference_links_used`, `traits_to_use`, and `traits_to_avoid`.

## 4. Article Plan

- Define the article promise in one sentence.
- Decide title direction, target reader, emotional arc, and visual rhythm.
- Draft a section outline and a visual/material storyboard together, ensuring each major argument has at least one reader-visible anchor.
- For list-style topics, justify why each item is included and why other candidates were excluded.

## 5. Writing

- Use original expression.
- Learn the selected style from structure, rhythm, opening, transitions, paragraph density, humor, evidence style, and ending strategy.
- Do not copy sentences, distinctive metaphors, or recognizable phrases from style samples.
- Use short paragraphs for WeChat reading.
- Make every image or material callout either evidence, understanding aid, emotional pause, source anchor, or summary.

## 6. Assets

- Create `鍥剧墖绱犳潗/YYYYMMDD/`.
- Add a cover image through online acquisition first: direct image URL, extracted `og:image`/social preview, official media asset, report/product image, or clean page capture. Validate that the saved file is a real image. If the download saves HTML, JSON, XML, a redirect page, an access-denied page, or a tiny error placeholder, delete it, record the failed attempt, and continue through the acquisition ladder. If no suitable verified online asset is available, prefer direct generation; use a prompt-only cover only if generation is unavailable or the user declines it.
- For every planned image slot, complete the online acquisition ladder before generation: stable direct image URL; source-page extraction from `og:image`, `twitter:image`, `srcset`, JSON-LD, embedded media URLs, and visible `img` elements; official or reliable alternatives such as newsroom/media-kit/product/report/PDF assets; then browser/page capture when the online page itself is a suitable visual. After each saved file, validate by content type and file signature/extension where possible; a file is valid only if it is an actual image usable in WeChat Markdown/HTML. If the result is HTML, JSON, XML, a redirect page, an access-denied page, or a tiny error placeholder, delete the file immediately and record the failed URL/reason. Complete the full acquisition pass before asking about generation or prompt-only placeholders. If direct downloads fail but extraction or page capture can produce useful online visuals, use those instead of jumping to generation. Then summarize the result, such as `10 planned / 6 online assets acquired / 4 unresolved`, and ask the user in a popup/choice UI when available whether unresolved slots should be direct-generated or prompt-only. If the user chooses direct generation, discover available image-generation skills first and let the user choose one; if no skill exists, check for direct image-generation capability/tooling; if neither exists, tell the user generation is unavailable and fall back to prompt-only placeholders. Route 2 must not be replaced by Python/code-drawn artwork. Downloaded/captured/generated files must be referenced with Markdown image syntax; prompt-only slots must use the required prompt placeholder at the exact article position.
- Render data-backed charts with code only when needed and reference the output files in Markdown.
- Keep filenames descriptive: `openai-pricing-page.png`, `industry-overview-chart.png`, not `1.png`.
- Write `绱犳潗娓呭崟.md`, including whether each material is a reader-visible anchor or background-only citation.

## 7. Review and Iteration

- Run the fixed review panel from `review-prompts.md`: 青天案牍 (`fact_review`), 哪吒巡街 (`mass_reader_review`), 马良神笔 (`image_review`), 太史公烛照 (`narrative_credibility_review`), and 雪芹总校 (`final_human_expression_review`).
- Default score gate: 90/100.
- Continue focused revision and re-review while any required reviewer is below 90/100; do not use a fixed round limit as a reason to ship a sub-90 article.
- Stop only when all fixed reviewers reach 90 or the user asks to stop.

## 8. Optional HTML

- Generate HTML only when requested.
- Prefer an installed layout skill if available.
- Otherwise run the fallback renderer.
- Validate visible text preservation after HTML generation.

