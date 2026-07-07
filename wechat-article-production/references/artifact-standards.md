# Artifact Standards

## Article Markdown

Filename:

`鏂囨鍒涗綔/锛圷YYYMMDD锛夋爣棰?md`

Requirements:

- Title at top.
- Short paragraphs.
- Markdown image references with relative paths for every downloaded, generated, or chart image file.
- Final publishable Markdown should reference PNG/JPG/WebP, not SVG, unless the user explicitly wants SVG.
- Prompt-only generated-image slots must be explicit at the exact intended position and mirrored in the material list; they are allowed only after the whole-article download pass leaves unresolved slots and the user explicitly chooses prompt-only for those slots. Do not leave generic pending-image notes.
- For explicitly chosen prompt-only fallback slots, place the full prompt at the intended image position using `[鐢熷浘鎻愮ず璇嶏細...]`; do not use Markdown image syntax unless a real file exists.
- Facts and sources noted at bottom when useful, plus inline reader-visible anchors where they improve trust and reading momentum.

## Image Folder

Path:

`鍥剧墖绱犳潗/YYYYMMDD/`

Must include:

- cover image downloaded from a suitable online URL, generated cover file, or cover prompt file.
- article images downloaded directly from online URLs, generated image files, chart files, or explicitly user-approved prompt-only generated-image placeholders for unresolved slots after the download pass.
- direct-download attempt notes for each image slot, including successful downloads, failed or unsuitable URLs, and the final planned/downloaded/unresolved counts.
- chart data CSV/JSON files when code-rendered charts are used.
- editable SVG/source files only when helpful; final references should point to exported PNG.
- `绱犳潗娓呭崟.md`.

## Material List

Use this schema:

| filename | type | source/prompt | purpose | article position | cover | visible anchor | status | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Set `visible anchor` to `yes` when the material appears in the article as an image, chart, quote card, source callout, page capture, table, or excerpt; set it to `background` for sources used only to verify claims. For code-rendered charts, include the data file, source URL, unit, date range, and caveat in `note`. For direct URL downloads, include the source URL and accessed date. For failed direct-download attempts, record the URL or search source and reason in `note`. For directly generated images, record the `prompt_style_route`, prompt, generated filename, skill/tool used, and visible-text language choice such as `none`, `Simplified Chinese`, `Chinese-first bilingual`, or `English source context`. For prompt-only generated images, set `filename` to `pending` or a planned filename, `type` to `prompt-only`, `status` to `pending-user-generation`, and note the grouped user choice that allowed prompt-only.

## Review Report

Filename:

`鏂囨鍒涗綔/锛圷YYYMMDD锛夋爣棰?璇勫鎶ュ憡.md`

Include:

- topic and final title
- selected writing style, selection reason, and reference links used
- source summary, including how many sources are reader-visible anchors versus background-only citations
- image and material-anchor strategy summary, including direct-download vs page-capture vs generated/prompt-only/source-card/chart/quote/table mix
- direct-download pass summary: planned count, downloaded count, unresolved count, fallback choice, and fallback reasons for generated/prompt-only slots
- review rounds with scores by fixed reviewer name and reviewer_id: 青天案牍 (`fact_review`), 哪吒巡街 (`mass_reader_review`), 马良神笔 (`image_review`), 太史公烛照 (`narrative_credibility_review`), and 雪芹总校 (`final_human_expression_review`)
- must-fix issues and changes made
- final score, pass/fail status for each fixed reviewer, and remaining risks

## HTML

Filename:

`鏂囨鍒涗綔/锛圷YYYMMDD锛夋爣棰?鍏紬鍙峰鍏ョ増.html`

Only when requested. Visible text must match the Markdown.


