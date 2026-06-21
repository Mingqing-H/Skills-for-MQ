---
name: wechat-article-layout
description: Turn source articles such as .md, .txt, or .html into polished WeChat Official Account HTML fragments, restyle existing article HTML, choose or extend layout style presets, and regenerate layouts while preserving the source article's visible text exactly. Use when the user asks for 微信公众号排版, WeChat article layout, HTML 排版, 文章美化, editor-ready HTML, or a style-preserving re-layout of an article.
---

# WeChat Article Layout

## Purpose

Create WeChat-ready HTML fragments from article drafts without changing the article's visible text. Improve typography, spacing, visual hierarchy, rhythm, colors, borders, backgrounds, and image placeholder presentation.

## Non-Negotiables

- Preserve all source visible text exactly: do not rewrite, summarize, expand, compress, reorder, translate, or add visible wording unless the user explicitly requests content changes.
- Preserve paragraph order, heading order, list order, quotes, code blocks, image placeholders, and source notes.
- Do not add visible labels such as "导语", "小结", "重点", or captions unless those words already exist in the source or the user asks for them.
- Do not remove source URLs, attribution lines, dates, disclaimers, or image placeholders.
- If the source contains facts that look outdated or risky, mention the issue outside the HTML instead of editing the article text.

## Workflow

1. Read the source article and identify its structural units: title, headings, paragraphs, lists, quotes, code blocks, links, images, dividers, and notes.
2. Ask for style preference only if the user has not provided one and the intended style is not obvious. Otherwise choose a suitable preset.
3. Read `references/style-presets.md` when selecting, adapting, or saving a reusable style.
4. Generate a single HTML fragment suitable for pasting into a WeChat editor.
5. Use inline CSS on elements or section wrappers. Avoid external CSS, JavaScript, forms, iframes, tracking pixels, and remote font dependencies.
6. Validate visible text preservation before claiming completion.

## HTML Rules

- Use a top-level `<section>` wrapper with conservative `max-width`, `margin`, `font-family`, `line-height`, and text color.
- Prefer nested `<section>`, `<p>`, `<h1>`-`<h3>`, `<blockquote>`, `<ul>`, `<ol>`, `<li>`, `<pre>`, `<code>`, `<img>`, and `<hr>` elements.
- Keep WeChat compatibility in mind: use simple inline styles, avoid complex selectors, CSS variables, fixed positioning, scripts, and layout tricks that may be stripped.
- Keep mobile readability: paragraph line height around `1.75` to `2`, body font size around `15px` to `16px`, and generous vertical spacing.
- Use visual design to clarify the existing text, not to create new editorial meaning.
- For image placeholders such as `[图片：...]`, preserve the placeholder text exactly. You may wrap it in a visually distinct block, but do not turn it into a different caption.

### Default visual treatment (apply unless user overrides)

These are default visual conventions learned from iterative refinement. Apply them automatically on new articles; the user can override any of them per-article.

- **Images**: wrap in a container with rounded corners and subtle shadow. Use generous border-radius (12px or above) for a soft, modern feel. Never output bare `<img>` with sharp corners.
- **Section headings**: make headings visually prominent — use accent bars, gradient backgrounds, tinted containers, or decorative wrappers so headings stand out clearly from body text. Bare `h2` with only a left border is not sufficient; aim for a "label bar" or "badge" effect.
- **Emphasis blocks**: for key viewpoints, data highlights, or reader-facing insights, wrap in a colored container with accent border and tinted background. Use different accent colors to distinguish semantic moods (e.g. blue for structure/definitions, orange for reader impact, green for operational data, purple for cost/billing). Bold key phrases inline to draw the eye.
- **Gradients**: use `linear-gradient` backgrounds on heading wrappers, decorative bars, and accent sections to add visual depth. Gradients can fade from a tinted color to transparent for a subtle, non-flat look.
- **Blur / frosted-glass effects**: use `backdrop-filter: blur()` on overlay panels or floating elements where supported, to create a modern layered look. Provide a solid-color fallback for WeChat clients that strip the filter.
- **SVG interaction layer**: when the article contains data points (numbers, percentages, growth comparisons), proactively apply SVG-driven animations — digit counters, keyword tag float-in, bar chart animations, comparison diagrams — even if the user does not explicitly request SVG. Data-heavy articles benefit from animated number displays and visual charts. Refer to `references/svg-interactions.md` for implementation patterns.

## Style Selection

Use an existing preset from `references/style-presets.md` when the user names a style or provides only a vague direction such as "简洁", "科技感", "杂志感", or "公众号精排".

When the user provides a screenshot or describes a new style:

- Extract reusable choices: palette, heading treatment, paragraph spacing, quote block style, divider style, image placeholder style, and accent components.
- Apply the style while preserving visible text.
- If the style will be reused, add a concise preset to `references/style-presets.md`.

## SVG Interaction Layer

In addition to the static style presets above, an optional SVG interaction layer can be applied on top of any preset. SVG interactions are defined in `references/svg-interactions.md` and add motion, reveal, or simulated UI to the article without changing visible text.

### When to use SVG interactions

- User explicitly asks for "SVG效果", "交互效果", "动效", "动画排版", or names a specific SVG interaction type.
- User wants a data report, AI tool review, annual recap, or product demo that benefits from animated numbers, chat simulation, or scroll-triggered reveals.
- User references a specific WeChat SVG article as a style target.

### SVG interaction rules

- SVG interactions are purely decorative and must not alter, hide, or reorder any source visible text.
- All SVG animations must use inline `<svg>` with `<animate>`, `<animateTransform>`, or CSS `@keyframes` via inline `style`. No external JS files.
- Auto-play interactions (no user tap required) are preferred for simplicity. Tap-triggered interactions require `onclick` on a wrapper `<section>` with `cursor: pointer`.
- Each SVG interaction preset specifies its own trigger mechanism (auto / tap / scroll-simulated).
- When combining an SVG interaction with a static style preset, apply the static preset first, then wrap relevant sections with SVG interaction markup.
- Always validate visible text preservation after applying SVG interactions.

### Preset naming convention

- Static presets: lowercase hyphen-case (e.g. `clean-editorial`, `campus-pink`).
- SVG interaction presets: prefixed with `svg-` (e.g. `svg-data-report`, `svg-chat-sim`).

## Validation

Before finalizing:

1. Compare the source visible text with the HTML visible text in order.
2. Confirm punctuation, numbers, names, URLs, emoji, brackets, and image placeholder text are unchanged.
3. Confirm no new visible words were introduced by decorative labels, captions, buttons, or section names.
4. If exact preservation cannot be guaranteed, state the uncertainty and list the risky areas.

## Output

Return:

- The HTML fragment in a fenced `html` code block, or write it to a file if the user asks for a file.
- A short note naming the chosen style preset or style direction.
- If SVG interactions were applied, name the SVG preset and describe the trigger mechanism.
- A preservation note only after validation, for example: "已按可见文本逐段自查，未改写正文。"
