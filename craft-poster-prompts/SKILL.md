---
name: craft-poster-prompts
description: Create, adapt, and maintain professional AI image prompts for poster design. Use when the user asks to design a poster, choose a composition, turn a brief into visual key art, generate a poster prompt, analyze a reference poster without copying it, or add reusable prompt templates. Includes eight composition systems—rule of thirds, symmetry, dynamic diagonal, dual focus, diamond, visual rhyme, radial, and density contrast—plus scenario modules for products, food, editorial portraits, events, culture, typography, and brands.
---

# Craft Poster Prompts

Turn a topic, product, event, slogan, or reference into a production-ready poster prompt. Build the prompt on two independent axes:

1. **Composition axis:** decide where visual weight, anchors, paths, and text zones sit.
2. **Scenario axis:** decide subject behavior, materials, photography/illustration language, and domain-specific failure controls.

Always select the composition first. Reuse mechanisms, not source-specific brands, copy, characters, logos, or exact layouts.

## Workflow

1. Extract purpose, audience, mandatory copy, subject, channel, aspect ratio, emotion, prohibited elements, and model if specified.
2. Choose one primary composition template from the eight-template table. State why it fits the message.
3. Optionally choose one scenario module. The composition template controls spatial structure; the scenario module supplies content and finish.
4. Fill every required variable. Infer low-risk visual choices; ask only when a missing fact would materially change the result.
5. Write the final prompt in this order:
   - task, medium, and aspect ratio
   - composition name and explicit geometry
   - anchor point or visual path
   - subject, action, and relationships
   - reserved text zone and exact copy
   - color, light, material, and finish
   - likely-failure constraints
6. Run the quality gate and deliver the selected templates, final copy-ready prompt, negative constraints, and optional variations.

If the user asks to generate the image, use the available image-generation route after the prompt is approved or when generation is already authorized.

## Composition routing: source eight

| Composition | One-sentence logic | Best for | Read |
| --- | --- | --- | --- |
| Rule of thirds | Put the subject on a named intersection; use the opposite quiet zone for text | travel, property, lifestyle | [template-rule-of-thirds.md](references/template-rule-of-thirds.md) |
| Symmetry | Build mirrored weight around an explicit axis | launches, luxury, architecture, tradition | [template-symmetry.md](references/template-symmetry.md) |
| Dynamic diagonal | Lead the eye from a stated start to endpoint along one directional path | sports, music, technology | [template-dynamic-diagonal.md](references/template-dynamic-diagonal.md) |
| Dual focus | Balance two focal points and connect them visually | comparison, collaboration, relationships | [template-dual-focus.md](references/template-dual-focus.md) |
| Diamond | Center the hero and use diagonal vertices for controlled echoes | jewelry, fragrance, premium packaging | [template-diamond.md](references/template-diamond.md) |
| Visual rhyme | Repeat and vary shape, color, or direction across regions | visual systems, series, cultural events | [template-visual-rhyme.md](references/template-visual-rhyme.md) |
| Radial | Expand energy from a precisely located origin while preserving a static text zone | promotions, festivals, openings | [template-radial.md](references/template-radial.md) |
| Density contrast | Make one region truly dense and another strictly sparse | exhibitions, minimal brands, editorial | [template-density-contrast.md](references/template-density-contrast.md) |

Do not choose by topic alone. Choose by communication intent:

- Need calm balance and breathing room → rule of thirds.
- Need order, ceremony, or authority → symmetry.
- Need speed, progress, or impact → dynamic diagonal.
- Need comparison or dialogue → dual focus.
- Need precious central focus → diamond.
- Need cohesion across varied elements → visual rhyme.
- Need explosive energy or expansion → radial.
- Need tension between information and silence → density contrast.

## Scenario modules

Use one only when it adds domain-specific value:

| Scenario | Read |
| --- | --- |
| Conceptual word or visual metaphor | [template-concept-metaphor.md](references/template-concept-metaphor.md) |
| Beverage, cosmetics, device, packaged product | [template-product-campaign.md](references/template-product-campaign.md) |
| Restaurant offer or food hero | [template-food-promotion.md](references/template-food-promotion.md) |
| Fashion, beauty, or portrait editorial | [template-fashion-editorial.md](references/template-fashion-editorial.md) |
| Match, concert, conference, or festival | [template-sports-event.md](references/template-sports-event.md) |
| Photography with oversized block type | [template-kinetic-type.md](references/template-kinetic-type.md) |
| City, heritage, seasonal, or regional illustration | [template-cultural-illustration.md](references/template-cultural-illustration.md) |
| Premium minimal brand campaign | [template-minimal-brand.md](references/template-minimal-brand.md) |

When combining, never paste two full skeletons together. Keep the composition geometry from the first and import only subject/material/quality controls from the second.

## Non-negotiable composition rules

Read [design-principles.md](references/design-principles.md) when the brief is ambiguous or text-heavy.

- Say coordinates and directions, not feelings. Replace “dynamic” with “from lower-left to upper-right at roughly 30 degrees.”
- Name the anchor and path. Specify an intersection, center axis, two focal points, vertices, radial origin, or dense/sparse boundary.
- Reserve the text zone before adding details. State its position, size, contrast, and maximum information load.
- Establish an explicit first, second, and third visual read.
- Use one dominant composition. A secondary mechanism may decorate but must not compete structurally.
- Treat required text as exact content. Quote it and prohibit invented dates, prices, sponsors, claims, or microcopy.
- Preserve 3–5 invariants for a series: grid, anchor, text position, color roles, crop, or texture.

## Quality gate

Verify that:

- The selected composition can be recognized from geometry alone.
- All anchors, directions, focal points, or region proportions are explicit.
- The title and information have a planned quiet zone.
- The first three visual reads are clear.
- Anatomy, product geometry, light direction, and shadows are coherent.
- Mandatory copy is exact; no fake text or unsupported claims are requested.
- Color, camera, material, and illustration instructions do not conflict.
- The poster remains legible as a thumbnail.

## Add or update templates

Read [template-schema.md](references/template-schema.md) before changing the library. Read [source-composition-notes.md](references/source-composition-notes.md) when tracing the original eight-template abstraction.

```bash
python scripts/new_template.py --id spiral --name "螺旋构图" --family composition
python scripts/validate_templates.py
```

When learning from a new source, extract its repeatable geometry, reading order, image-text relationship, palette logic, and failure controls. Remove source-specific brands, copy, protected characters, and artist imitation. Add a new template only when an existing composition or scenario module cannot absorb the mechanism cleanly.