# Style Presets

Use these presets as starting points for WeChat Official Account article HTML. Adapt colors and spacing to the article topic, but keep visible article text unchanged.

## clean-editorial

Use for analytical essays, AI product observations, and serious commentary.

- Palette: warm white background, charcoal text, muted gray secondary rules, one restrained accent color.
- Headings: bold, compact, with a left border or small top rule.
- Paragraphs: 15-16px, line-height 1.85, margin 0 0 1em.
- Quotes: pale background, left accent border, no added quote label.
- Image placeholders: dashed border block with the original placeholder text unchanged.
- Dividers: thin line with generous vertical spacing.

## tech-brief

Use for AI news, product updates, model releases, tool reviews, and data-heavy articles.

- Palette: white or very light cool background, dark text, blue/cyan accent used sparingly.
- Headings: clear hierarchy, small accent bar, optional subtle background for section headings.
- Paragraphs: slightly tighter than editorial, line-height 1.75-1.85.
- Lists: compact spacing, clear bullets, no invented labels.
- Quotes/data notes: light blue-gray panel with border.
- Code or command text: monospace, light gray background, rounded 4-6px.

## magazine-feature

Use for narrative essays, culture commentary, internet phenomena, and more emotional pieces.

- Palette: paper-like background, rich dark text, one deep accent color.
- Headings: larger, more spacious, with understated divider treatment.
- Paragraphs: airy rhythm, line-height around 1.9.
- Pull quotes: only style existing quote text; do not create new pull quotes from ordinary paragraphs unless the user explicitly allows visible duplication.
- Image placeholders: full-width quiet frame, original placeholder text unchanged.

## compact-feed

Use for short updates, newsletters, multi-item roundups, and quick reads.

- Palette: clean white, dark text, one bright but restrained accent.
- Headings: small and scannable.
- Paragraphs: 15px, line-height 1.75, reduced margins.
- Item blocks: subtle background or border, no nested decorative cards.
- Lists: preserve original order and wording.

## campus-pink

Use for campus event recaps, lifestyle stories, emotional narratives, activity summaries, and warm-toned community content.

- Palette: light gray-white background `#F7F7F7`, dark gray text `#505050`, rose-pink accent `#F6C0C3`, coral-pink secondary `#F39C9C`, white for card/image borders.
- Part labels: rose-pink capsule badge with white text, `background-color: #F6C0C3; border-radius: 10px; padding: 0 10px; color: #fff; font-size: 20px`.
- Section titles: 24px bold, letter-spacing 1px, with a 4px gradient underline that fades from `#F6C0C3` to transparent, width ~61%.
- Subsection titles: coral-pink text `#F39C9C`, letter-spacing 2px, line-height 2, bottom border 2px solid `#F39C9C`, centered layout with decorative icon to the right.
- Paragraphs: 14px, line-height 2, letter-spacing 1px, text-align justify, margins 0 30px with 23px vertical padding.
- Intro/quote text: 14px, centered, letter-spacing 1px, one sentence per line for poetic rhythm.
- Image placeholders: full-width centered at 67-87% width, with optional rose-pink 5px border (`border: 5px solid #F6C0C3`) or white 5px border with soft shadow (`border: 5px solid #fff; box-shadow: #A0A0A0 1px 1px 5px`). Double-image rows use 50/50 flex layout with 12px gap.
- Item cards (numbered): icon (20px) + bold title + number (`01/` format) in 3-column flex; 14px centered description below; thin line divider between items.
- Dividers: rose-pink gradient fade line (`linear-gradient(90deg, #F6C0C3 13%, rgba(246,192,195,0) 88%)`), 4px height, generous vertical spacing.
- Decorative touches: subtle texture background images, tilted decorative elements at edges, rose-pink shadow accents on image corners.
- Caution: This style is originally produced by visual editors (Xiumi/135) with complex grid overlays and SVG decorations. The simplified preset above extracts the reusable design language without replicating editor-specific positioning. Preserve all visible text exactly; do not add decorative labels.

## SVG Interaction Layer

In addition to the static presets above, SVG interaction presets can be layered on top of any style to add motion and interactivity. See `references/svg-interactions.md` for full details.

Available SVG interaction presets:

| Preset | Description | Trigger | Best paired with |
|--------|-------------|---------|-----------------|
| `svg-data-report` | Number counters, keyword float-in, title entrance | auto | `tech-brief`, `clean-editorial` |
| `svg-ambient-float` | Floating elements, gentle sway, breathing pulse | auto | `magazine-feature`, `campus-pink` |
| `svg-chat-sim` | Simulated chat bubbles with staggered reveal | auto | any (AI tool reviews) |
| `svg-scroll-reveal` | Progressive content reveal with timed delays | auto | `clean-editorial`, long-form |
| `svg-3d-parallax` | Depth layers with tap-to-advance parallax | tap | product launches, brand |

Usage: name both the static preset and the SVG preset when generating, e.g. "用 tech-brief + svg-data-report 排版".

## Saving New Presets

When adding a static preset, include:

- Preset name in lowercase hyphen-case.
- Best-fit content types.
- Palette, heading style, paragraph rhythm, quote treatment, image placeholder treatment, and divider rules.
- Any strict cautions needed to preserve visible text.

When adding an SVG interaction preset, follow the naming and documentation rules in `svg-interactions.md`.
