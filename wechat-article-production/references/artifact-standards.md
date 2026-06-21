# Artifact Standards

## Article Markdown

Filename:

`文案创作/（YYYYMMDD）标题.md`

Requirements:

- Title at top.
- Short paragraphs.
- Markdown image references with relative paths when assets exist.
- Final publishable Markdown should reference PNG/JPG/WebP, not SVG, unless the user explicitly wants SVG.
- Pending images must be explicit and mirrored in素材清单.
- In prompt-only generated-image mode, place the full prompt at the intended image position using `[生图提示词：...]`; do not use Markdown image syntax unless a real file exists.
- Facts and sources noted at bottom when useful.

## Image Folder

Path:

`图片素材/YYYYMMDD/`

Must include:

- cover image or cover prompt file.
- article images or pending placeholders, including prompt-only generated-image placeholders when selected.
- downloaded real assets when available.
- chart data CSV/JSON files when code-rendered charts are used.
- editable SVG/source files only when helpful; final references should point to exported PNG.
- `素材清单.md`.

## Material List

Use this schema:

| filename | type | source/prompt | purpose | article position | cover | status | note |
| --- | --- | --- | --- | --- | --- | --- | --- |

For code-rendered charts, include the data file, source URL, unit, date range, and caveat in 
ote`. For prompt-only generated images, set `filename` to `pending` or a planned filename, `type` to `prompt-only`, and `status` to `pending-user-generation`.

## Review Report

Filename:

`文案创作/（YYYYMMDD）标题-评审报告.md`

Include:

- topic and final title
- source summary
- image strategy summary, including real/downloaded vs generated/source-card/chart mix
- review rounds with scores
- must-fix issues and changes made
- final score and remaining risks

## HTML

Filename:

`文案创作/（YYYYMMDD）标题-公众号导入版.html`

Only when requested. Visible text must match the Markdown.


