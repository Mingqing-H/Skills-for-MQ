---
name: memory-learning-cards
description: Use when the user wants to learn, memorize, review, or deeply understand concepts, articles, book chapters, exam materials, professional knowledge, vocabulary, procedures, or any educational content. Creates flexible memory-optimized learning cards, usually as a beautiful self-contained HTML study artifact, with vivid mnemonic techniques and adaptive UI rather than a fixed template.
---

# Memory Learning Cards

## Core Intent

Turn learning material into an artifact that helps the learner understand, remember, and review. The visible interface is a means to that end. Choose the layout, density, components, and style that best fit the content, learner, device, and requested output.

The skill succeeds when the learner can:

- Identify what each card is asking.
- Understand the answer without needing the source text beside it.
- Recall the key point through a vivid mnemonic scene or exact analogy.
- Review cards comfortably without overlap, clipped text, or awkward fixed panels.
- Use the artifact on common desktop and mobile widths.

## Workflow

### 1. Read the Learning Need

Infer the topic, learner level, purpose, and likely review scenario from the user request. If the user gives constraints such as exam prep, quick review, beginner explanation, mobile use, printable cards, or a specific visual style, let those constraints drive the artifact.

If the input is long, extract the most learnable units instead of forcing every paragraph into a card.

### 2. Extract Knowledge Points

Create discrete cards around concepts that are worth remembering. Each card should usually cover one of these types:

| Type | Good card focus |
| --- | --- |
| Definition | What it means and how to recognize it |
| Process | Steps, order, cause and effect |
| Comparison | Differences, tradeoffs, "why not X" |
| Principle | Rule, mechanism, consequence |
| Formula | Meaning of variables, use case, trap |
| Timeline | Sequence, turning point, significance |
| Case | What happened, why it matters |
| Vocabulary | Meaning, usage, pronunciation, mnemonic |

Merge tiny facts when they belong together. Split system-sized topics when one card would become dense.

### 3. Build the Memory Hook

Read `references/MEMORY.md` when creating mnemonics. This is the core value of the skill.

Every memory technique must give the learner a concrete mental image or exact mapping. Avoid generic advice such as "use association" unless the association itself is fully specified.

Preferred techniques:

- Vivid scene: absurd, visual, emotionally sticky.
- Analogy mapping: each abstract element maps to a familiar object or action.
- Contrast elimination: explain why the confusing alternative is wrong.
- Story chain: useful for ordered lists and processes.
- Number hook: useful for codes, dates, quantities, or ordered facts.

### 4. Choose the Output Form

Default to a single self-contained `.html` file named `learning-[topic-slug].html` in the current working directory. Use inline CSS and vanilla JavaScript. External fonts and images are optional enhancements, not requirements.

If the user asks for inline text, Markdown, Anki import, printable cards, or another format, use that format.

### 5. Choose the Layout From the Content

Do not force a fixed sidebar, fixed footer, fixed 100vh viewport, dashboard, carousel, or overlay. Pick a pattern that helps the content breathe.

Good default patterns:

- **Small set, 1-4 cards**: vertical cards or printable grid.
- **Medium set, 5-12 cards**: carousel, tabbed deck, or card list with progress chips.
- **Large set, 13+ cards**: scrollable study page with table of contents, search/filter, collapsible sections, or grouped decks.
- **Process-heavy material**: timeline, stepper, flow diagram, or before/after comparison.
- **Comparison-heavy material**: matrix/table plus cards for traps and examples.
- **Mobile-first request**: single-column cards, sticky lightweight controls, no wide sidebars.

Scrolling is allowed. For substantial content, scrolling is usually better than hiding, shrinking, or clipping text.

## Card Content

Each card should include the pieces that help the learner most. These are recommended, not mandatory in every case:

- **Prompt or concept**: the question, term, claim, or task the learner should recall.
- **Direct answer**: a concise, accurate explanation.
- **Key points**: 2-4 scannable bullets when useful.
- **Memory hook**: the vivid scene, analogy, elimination cue, or story chain.
- **Example**: one concrete use case when the idea is abstract.
- **Pitfall**: include only when there is a likely misconception.
- **Review action**: reveal, mark known, next card, retry, or copy/export.

Do not let a long original question become a giant heading that breaks the layout. Preserve the meaning, and keep the full original wording available when it matters, for example in a smaller source line, details block, tooltip, or card back.

## Visual Direction

Read `references/DESIGN.md` when generating a polished HTML artifact. Treat it as a flexible design guide, not a mandatory brand template.

The default feel should be warm, clear, and editorial: generous spacing, readable type, restrained color, strong hierarchy, and calm interaction. Adapt the palette and layout when the subject or user request calls for something more technical, playful, dark, minimalist, or exam-focused.

Read `references/VISUALS.md` when the artifact would benefit from diagrams, icons, progress UI, card navigation, or other visual aids. Use visuals only when they improve comprehension or review.

## Interaction Guidance

For HTML artifacts, include only the controls that the learner will naturally use:

- Card reveal or front/back flip.
- Previous/next navigation when cards are sequential.
- Progress state when there are enough cards for it to matter.
- Keyboard support when using a deck/carousel.
- Local in-memory or `localStorage` progress if it adds value.
- Search/filter for large decks.
- Completion state only if it does not block continued review.

Keep controls visible and understandable, but do not let controls compete with the learning content.

## Responsive and Anti-Overlap Rules

These rules are more important than any aesthetic preference:

- Use normal document flow, CSS grid, and flex layouts before fixed positioning.
- Allow `body` or main content to scroll for long material.
- Avoid `overflow: hidden` on the whole page unless the content is guaranteed to fit.
- Avoid fixed heights for text-heavy cards. Use `min-height`, `max-width`, and responsive spacing instead.
- Keep modals and celebration screens dismissible.
- Do not place persistent fixed bars over card content.
- Use `box-sizing: border-box`, `min-width: 0`, and `overflow-wrap: anywhere` where long terms or Chinese/English mixed text may appear.
- Check common widths mentally or with a browser when possible: 360px, 768px, 1280px.
- If content overflows, redesign the layout; do not hide core learning text.

## Quality Bar

Before finalizing, verify:

- Each card has a clear recall target.
- Each mnemonic creates a specific picture or exact mapping.
- The interface does not require the learner to fight the layout.
- Long text wraps cleanly and remains readable.
- No visible element covers another element.
- The page has enough visual polish to feel intentionally designed, not just functional.
- Optional features were omitted when they would add clutter.

## Anti-Patterns

- Rigidly applying a sidebar/dashboard/carousel template to every topic.
- Forcing everything into one viewport and clipping content.
- Turning every card into the same dense structure even when a section is not useful.
- Using generic memory advice without a concrete scene.
- Making progress UI more visually important than the learning content.
- Using decorative visuals that do not teach, clarify, or aid recall.
- Letting fixed headers, footers, sidebars, arrows, dots, or overlays cover text.
- Treating a style guide as more important than readability and learning outcomes.
