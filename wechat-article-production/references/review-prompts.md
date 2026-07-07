# Review Prompts

## Fixed Review Panel

Use these fixed reviewer names in every review round and review report. Do not rename them per article.

| reviewer_id | fixed name | name cue | responsibility |
| --- | --- | --- | --- |
| fact_review | 青天案牍 | Bao Gong / courtroom-drama allusion: fair judgment over evidence. | Fact accuracy, dates, names, source support, claims, caveats. |
| mass_reader_review | 哪吒巡街 | Myth and animation allusion: lively street-level sensing. | Reader completion, share intent, virality, dropout points. |
| image_review | 马良神笔 | Folk-tale and animation allusion: images must become real on the page. | Image count, online acquisition, validation, Markdown references, material list. |
| narrative_credibility_review | 太史公烛照 | Shiji / historian allusion: illuminate whether the story can stand. | Psychological realism, staged-feeling anecdotes, boastful or fabricated-feeling scenes. |
| final_human_expression_review | 雪芹总校 | Dream of the Red Chamber allusion: final polish for human texture. | Natural flow, human voice, tone fit, final editorial pass. |

Each reviewer output must start with: `Reviewer: <fixed name> (<reviewer_id>)`.

## 青天案牍 (fact_review)

Ask:

> Reviewer: 青天案牍 (fact_review). Review the article for factual accuracy. Check dates, company/model names, source support, overclaiming, missing caveats, and unsupported "latest/first/confirmed" language. Output: score 0-100, must-fix issues, optional improvements, and source gaps. Do not rewrite the article.

## 哪吒巡街 (mass_reader_review)

Ask:

> Reviewer: 哪吒巡街 (mass_reader_review). Simulate 5 WeChat reader types: ordinary AI user, practitioner, entrepreneur, nontechnical white-collar reader, and headline-driven reader. For each, estimate completion rate, share intent 0-10, biggest hook, biggest dropout point. Output overall virality score 0-100 and top 5 improvements. Do not rewrite the article.

## 马良神笔 (image_review)

Ask:

> Reviewer: 马良神笔 (image_review). Review image strategy. Check image count vs article length, whether every major section has visual or material support, whether the article includes enough reader-visible evidence anchors to make readers want to keep reading, whether the visual plan also contains interesting/memorable moments rather than boring screenshots only, whether images/materials are evidence/explanation/data/pause/humor/metaphor rather than decoration, whether every image slot attempted online acquisition before generation: stable direct image URLs, source-page extraction (`og:image`, `twitter:image`, `srcset`, JSON-LD, visible `img` assets), official/reliable asset alternatives, and browser/page capture when original image URLs were hidden or blocked; whether every saved online asset was validated as a real image rather than HTML/JSON/XML/redirect/access-denied content or a tiny error placeholder, whether failed HTML/error-page files were deleted from the material folder, whether failed URLs, acquisition routes, and reasons were recorded, whether downloaded/captured/generated/chart files are referenced in Markdown, whether the full image/material-anchor count was planned, whether a whole-article online acquisition pass was completed before any prompt/generation fallback, whether direct downloads were used wherever suitable URLs existed, whether repeated HTML/error-page download failures led to extraction/page-capture attempts before grouped generated-image fallback, whether unresolved slots were summarized together with counts such as planned/downloaded/unresolved, whether prompt-only was avoided as a global/default mode, whether the user was asked in a popup/choice UI when available to choose prompt-only or direct generation for unresolved slots, whether direct-generation choices first checked available image-generation skills/tools and produced actual image files with Markdown references rather than prompt placeholders, whether code/Python rendering is limited to data-backed charts, whether code-rendered charts have saved data and sources, whether route-2 fallback decisions are grouped for unresolved slots (`direct-generate` files or explicitly chosen `prompt-only` placeholders), whether prompt-only placeholders contain complete professional prompts and remain rare, whether every directly generated image records a `prompt_style_route` from `image-prompt-patterns.md`, whether the chosen route fits the image intent rather than using one generic style everywhere, whether directly generated images explicitly chose a visible-text language preference based on article context and image purpose, whether Chinese WeChat generated images avoid unintended English text unless an English-native UI/paper/code/product/source context justifies it, whether generated images are vivid but not fake evidence, whether source cards are overused or too generic, whether evidence visuals are cropped/organized well enough to be readable, whether important claims lack visible citations/materials, whether the cover is strong, and whether素材清单 is complete. Output score 0-100 and fixes.

## 太史公烛照 (narrative_credibility_review)

Ask:

> Reviewer: 太史公烛照 (narrative_credibility_review). Review whether the article feels realistically grounded to a skeptical WeChat reader. This is not only fact-checking: judge whether personal scenes, anecdotes, emotional turns, coincidences, career stories, cafe/reflection moments, interview stories, dialogue, and self-discovery arcs feel over-staged, too convenient, too dramatic, too polished, or like "big talk" that readers may perceive as fabricated. Flag passages that may be literally possible but psychologically unbelievable, such as a neat story where "I recently attended an interview, then went to Starbucks to reflect" if it feels inserted only to create atmosphere. Output score 0-100, suspicious/overwritten passages, why they feel unrealistic, and concrete revision guidance: make it more specific, more modest, more externally grounded, or remove the scene. Do not rewrite the article unless asked.

## 雪芹总校 (final_human_expression_review)

Ask:

> Reviewer: 雪芹总校 (final_human_expression_review). Review the final article as a senior human editor. Judge whether the reading flow is natural, whether transitions feel smooth, whether the voice sounds like it came from a real human writer rather than a model, whether any phrasing is inappropriate, exaggerated, stiff, empty, cliche, or mismatched with the intended WeChat audience, and whether any paragraph breaks the promised tone. Output score 0-100, must-fix lines or sections, suggested direction for edits, and final pass/fail. Do not rewrite the article unless asked.

## Iteration Rule

- Default gate: 90/100 for every required reviewer.
- Required reviewers: 青天案牍, 哪吒巡街, 马良神笔, 太史公烛照, and 雪芹总校.
- If 青天案牍 finds a factual must-fix, fix before judging virality.
- If 太史公烛照 finds scenes, claims, or emotional turns that feel over-staged, unrealistic, boastful, or fabricated, revise before final delivery even when facts are technically possible.
- If 雪芹总校 finds stiff, inappropriate, non-human, or tone-mismatched language, revise before final delivery even when other scores pass.
- Continue iterating until every required reviewer reaches at least 90/100, unless the user explicitly stops. Do not mark the article final while any required reviewer remains below 90.
- Record each round in the review report using the fixed reviewer names and reviewer_id values.