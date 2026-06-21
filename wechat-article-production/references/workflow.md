# Workflow

## 1. Input Handling

- Accept a topic as sufficient input.
- Infer date from current date and use `YYYYMMDD`.
- Optional inputs: target style, sample files, audience, word count, HTML requirement, generated-image mode (`direct-generate` or `prompt-only`), source preferences.
- If the user asks for "latest", "today", "recent", "刚刚", or modern company/model facts, research before writing.

## 2. Research

- Build a source pack before drafting: official pages, primary docs, reliable media, papers, product pages, and user-provided files.
- Record source title, URL, publisher, publication date, accessed date, and the exact claim supported.
- Separate confirmed facts, reported claims, expert opinions, and your analysis.
- Do not use unverified rumors as hard facts.

## 3. Article Plan

- Define the article promise in one sentence.
- Decide title direction, target reader, emotional arc, and visual rhythm.
- Draft a section outline and a visual storyboard together.
- For list-style topics, justify why each item is included and why other candidates were excluded.

## 4. Writing

- Use original expression.
- Learn style from structure, rhythm, opening, transitions, paragraph density, humor, and ending strategy.
- Do not copy sentences, distinctive metaphors, or recognizable phrases from style samples.
- Use short paragraphs for WeChat reading.
- Make every image either evidence, understanding aid, emotional pause, or summary.

## 5. Assets

- Create `图片素材/YYYYMMDD/`.
- Add cover image or cover prompt according to generated-image mode.
- Download real assets and render data charts when possible. For generated images, either generate files directly or insert prompt-only placeholders, depending on the selected mode.
- Keep filenames descriptive: `openai-pricing-page.png`, `industry-overview-chart.png`, not `1.png`.
- Write `素材清单.md`.

## 6. Review and Iteration

- Run fact review, mass-reader review, and image review.
- Default score gate: 85/100.
- Iterate up to 3 rounds when below 85.
- Stop early only when score reaches 85 or the user asks to stop.

## 7. Optional HTML

- Generate HTML only when requested.
- Prefer an installed layout skill if available.
- Otherwise run the fallback renderer.
- Validate visible text preservation after HTML generation.

