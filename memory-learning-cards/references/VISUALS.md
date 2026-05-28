# Visual and Interaction Reference

Use visuals to make knowledge easier to understand or remember. Do not add visual components simply because this skill has a reference file for them.

## Visual Priority

1. Clarify the knowledge.
2. Strengthen memory.
3. Support review flow.
4. Add polish without clutter.

If a visual does not serve one of those purposes, omit it.

## Icons

Icons are optional. Use them for scanability when they clarify section purpose:

- Memory hook: sparkle, image, anchor, or lightbulb.
- Pitfall: warning triangle or exclamation.
- Process: arrows or numbered steps.
- Comparison: split columns, balance, or versus mark.
- Formula: sigma, calculator, or variable mark.
- Timeline: clock or line with nodes.

Inline SVG is reliable for standalone HTML. Text labels are also fine. Do not force icons into every heading.

Simple SVG style:

- `18px-22px` size.
- `1.5px-2px` stroke.
- Use the page palette.
- Add `aria-hidden="true"` for decorative icons, or a text label for meaningful icons.

## Diagrams

Use diagrams when they reduce cognitive load:

- **Flow**: steps, protocols, workflows, lifecycles.
- **Timeline**: historical or developmental order.
- **Comparison matrix**: confusing pairs, tradeoffs, alternatives.
- **Hierarchy**: layers, taxonomy, architecture.
- **Cycle**: feedback loops and recurring processes.
- **Map/scene**: mnemonic locations or story chains.

Keep diagrams responsive:

```css
.diagram {
  width: 100%;
  max-width: 720px;
  overflow-x: auto;
}
.diagram svg {
  max-width: 100%;
  height: auto;
}
```

If an SVG would become cramped on mobile, use a vertical list or collapsible steps instead.

## Navigation Patterns

Choose navigation by card count and content type:

- **Reveal card**: best for a single concept or short practice set.
- **Vertical cards**: best for reading and comparing multiple cards.
- **Carousel**: best for 5-12 cards when one-at-a-time review matters.
- **Tabs/groups**: best when cards naturally cluster by chapter or topic.
- **Search/filter/index**: best for large decks.
- **Printable grid**: best when the user wants offline or paper review.

Carousel requirements if used:

- Previous and next controls.
- Keyboard left/right support.
- Dots or count indicator if there are more than three cards.
- A non-overlapping layout on mobile.
- No hidden core text inside a fixed-height slide.

Do not use a carousel for long explanatory cards unless each slide can scroll naturally.

## Progress UI

Progress is useful when there are enough cards to review over time. Keep it proportional to the task.

Good options:

- Small mastered count: `3 / 12 mastered`.
- Progress bar or chips above the deck.
- Per-card status buttons: `Need review`, `Learning`, `Known`.
- Optional `localStorage` persistence.
- Reset progress button.

Use a full dashboard only when it genuinely helps, such as large study sets or deliberate practice sessions. Avoid permanent side dashboards for small decks.

## Memory Visuals

The memory hook can be visualized in several ways:

- A short "mental image" paragraph.
- A small scene card with highlighted objects.
- A numbered story chain.
- A compact analogy map: concept element -> familiar element.
- A "wrong choice" mini-scene for contrast elimination.

The learner should be able to close their eyes and reconstruct the scene.

## Overlays and Celebration

Completion celebrations are optional. If used:

- Show only after the learner completes the set.
- Make it dismissible.
- Do not erase progress state.
- Keep it lightweight and readable.

Avoid overlays for routine information. Prefer inline status messages.

## Media

Use images only when they materially improve understanding:

- Physical objects, places, anatomy, art, historical artifacts, or real-world equipment.
- Complex concepts where a real diagram is more useful than a decorative illustration.

Images must have meaningful alt text and responsive sizing. Avoid broken external URLs and purely atmospheric stock images.

## Visual QA

Before finishing:

- Every visual has a learning purpose.
- Text remains readable without the visual.
- Controls do not cover text.
- Mobile layout stacks cleanly.
- Large decks have a way to navigate without endless hunting.
- No decorative layer competes with the card content.
