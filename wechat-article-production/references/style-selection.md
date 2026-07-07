# Style Selection

Use this after topic analysis and before drafting. Do not write the article until the user has selected a style, unless the user explicitly says to choose for them.

## Timing

1. Analyze the topic, audience, freshness, evidence type, and likely reader motivation.
2. Build a short style menu that fits the topic.
3. Present the menu to the user as a choice interface when the runtime supports it. If no UI choice tool is available, ask in a concise numbered list.
4. Wait for the user's selection before drafting.

## Style Menu Requirements

Offer 4-6 choices. Each choice should include:

- `style_name`: short Chinese label.
- `best_for`: when this style fits the topic.
- `reader_feel`: what the reader should feel while reading.
- `writing_traits`: opening, structure, paragraph rhythm, evidence style, ending.
- `reference_links`: 1-3 original article links or public author/homepage links that can help the user recognize the style.
- `risk`: what can go wrong if this style is overused.

Prefer real public original links from WeChat public pages, media sites, newsletters, blogs, or publisher archives. Search the web for current accessible examples when needed. Do not fabricate URLs or claim a link is an original article unless it was verified. If a good original link cannot be found, write `reference_links: not found` and explain the search gap briefly.

## Recommended Style Pool

Use these as defaults, then adapt to the topic:

1. `深度分析型`: calm, structured, evidence-heavy, suitable for industry analysis, policy, company, model, or market topics.
2. `故事叙事型`: scene-first, character or conflict driven, suitable for case studies, founder stories, product journeys, and social observation.
3. `爆款观点型`: strong hook, clear stance, dense turns, suitable for hot topics and debate, but must avoid exaggeration.
4. `科普解释型`: approachable, analogy-rich, suitable for nontechnical readers and complex concepts.
5. `商业拆解型`: framework, numbers, business logic, suitable for founders, operators, investors, and workplace readers.
6. `人文评论型`: reflective, restrained, language-focused, suitable for AI and society, culture, education, and individual experience.

## Reference Link Search

When reference links would help the user choose, search for examples with queries like:

- `[topic/domain] 微信公众号 深度分析 原文`
- `[topic/domain] 公众号 爆款 观点 原文`
- `[publication/author] 文章 原文`
- `[style archetype] [topic] article`

Use links as reference material only. Do not copy distinctive phrases, metaphors, paragraph rhythm too closely, or article structure that would make the output recognizable as imitation.

## Choice Interface Text

Use this compact pattern:

`我先根据选题给你几个写作风格方向。选一个后我再正式写正文。`

For each option, show:

`A. 风格名 - 一句话适用说明。参考：link1, link2。风险：...`

Include a final option:

`让系统推荐：我根据选题自动选择，并说明理由。`

If using a UI choice tool, make the recommended option first only when one style is clearly best for the analyzed topic.

## After Selection

Record the selected style in the article plan and review report:

- `selected_style`
- `why_this_style`
- `reference_links_used`
- `traits_to_use`
- `traits_to_avoid`
