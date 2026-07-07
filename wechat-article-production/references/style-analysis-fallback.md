# Style Analysis Fallback

Use this after the user selects a writing style, or when a dedicated writing-style skill is unavailable.

## Inputs

- Selected style from `style-selection.md`: use it as the primary constraint.
- Reference links chosen by the user: inspect accessible originals when available.
- Existing style profile: read and use it.
- Multiple samples: inspect at least 3 when possible.
- Single sample: warn internally that confidence is lower and avoid overfitting.

## Analyze

- Topic selection: what kinds of stories does the style favor?
- Opening: daily-life hook, direct news hook, question, anecdote, or contradiction.
- Structure: list, essay, narrative, argument, problem-solution.
- Paragraph rhythm: short/long mix, sentence density, transitions.
- Language: colloquial/formal mix, humor, questions, metaphors.
- Evidence: how facts, quotes, screenshots, and data are introduced.
- Ending: summary, open question, call to action, punchline, or quiet leave-behind.

## Use

- Imitate method, not wording.
- Preserve the new article's facts and argument.
- Avoid copying distinctive sentences, jokes, metaphors, or rhythm that is too recognizable.
- If style conflicts with factual clarity, factual clarity wins.

## Output Notes

When reporting style use, summarize:

- `selected_style`
- `style_source`
- `reference_links_used`
- `usable_traits`
- `traits_to_avoid`
- `adaptation_decision`
