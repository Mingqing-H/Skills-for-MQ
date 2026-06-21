# Review Prompts

## Fact Review Agent

Ask:

> Review the article for factual accuracy. Check dates, company/model names, source support, overclaiming, missing caveats, and unsupported "latest/first/confirmed" language. Output: score 0-100, must-fix issues, optional improvements, and source gaps. Do not rewrite the article.

## Mass Reader Review Agent

Ask:

> Simulate 5 WeChat reader types: ordinary AI user, practitioner, entrepreneur, nontechnical white-collar reader, and headline-driven reader. For each, estimate completion rate, share intent 0-10, biggest hook, biggest dropout point. Output overall virality score 0-100 and top 5 improvements. Do not rewrite the article.

## Image Review Agent

Ask:

> Review image strategy. Check image count vs article length, whether every major section has visual support, whether images are evidence/explanation/data/pause rather than decoration, whether enough real downloaded/screenshotted materials are used, whether code-rendered charts have saved data and sources, whether generated images follow the selected mode (`direct-generate` files or `prompt-only` placeholders), whether prompt-only placeholders contain complete professional prompts, whether generated images are vivid but not fake evidence, whether source cards are overused, whether the cover is strong, whether素材清单 is complete, and whether Markdown image paths exist or pending states are explicit. Output score 0-100 and fixes.

## Iteration Rule

- Default gate: 85/100.
- If any review finds a factual must-fix, fix before judging virality.
- Iterate up to 3 rounds.
- Record each round in the review report.

