---
name: wechat-topic-radar
description: Find and rank WeChat public account topic ideas from current hot lists, Chinese and international news, and audience-interest signals. Use when the user asks for today's/this week's 公众号选题, 微信公众号选题, 爆款选题, 热搜选题, 热点追踪, content planning from 百度热搜/微博热搜/知乎热榜/微信热文/国内外新闻, or wants 10 recommended article topics with reasons, angles, and writing style.
---

# WeChat Topic Radar

## Workflow

1. Ask for account positioning only when it is missing and the user has not requested immediate execution. Otherwise use the default profile: Chinese WeChat public account, 25-40 year-old urban readers, social observation + career + business + AI + consumer life, medium risk tolerance.
2. Run `scripts/topic_radar.py` to collect current public hot-list/news signals and produce ranked WeChat topic ideas.
3. Treat failed sources as source-status notes, not as a task failure. Continue with available sources and mention unavailable sources in the final answer.
4. Select the best 10 ideas by user-view value, not raw heat. Prefer topics with concrete audience anxiety, identity, money/time impact, fresh conflict, and WeChat shareability.
5. For each idea, include title, short details, source basis, recommendation reason, target reader, writing angle, recommended voice/style, and risk/verification notes.

## Quick Run

```powershell
python wechat-topic-radar\scripts\topic_radar.py --top 10 --format markdown
```

Use account parameters when available:

```powershell
python wechat-topic-radar\scripts\topic_radar.py --top 10 --format markdown --profile "AI职场公众号，读者是一二线城市25-38岁白领，偏实用、克制、略犀利"
```

Use JSON when another tool needs structured data:

```powershell
python wechat-topic-radar\scripts\topic_radar.py --top 10 --format json
```

## Ranking Principles

Score topics with these heuristics:

- Heat: appears in ranked hot lists, repeated sources, or major outlets.
- Freshness: likely published or discussed in the last 24-72 hours.
- Reader proximity: affects work, money, family, identity, health, education, consumption, or social status.
- Emotional force: anxiety, surprise, anger, relief, pride, sadness, curiosity, or self-recognition.
- Practical value: helps readers decide, avoid loss, talk about the issue, or understand themselves.
- Differentiation: avoid generic "what should ordinary people do" topics unless there is a precise scene or crowd.
- Safety: downgrade rumor-like, private-person, medical/legal/financial certainty, or highly sensitive political topics.

## Output Requirements

Return exactly 10 topics unless the user asks for another count. Each topic should use this shape:

```markdown
### 1. 标题：...

详情：...

来源依据：...

推荐原因：...

目标读者：...

写作角度：...

推荐风格：...

风险提醒：...
```

Prefer concrete WeChat-style titles over news headlines. Convert big events into a user-view question:

- Not: `某公司宣布裁员`
- Better: `这届打工人最怕的不是裁员，而是“努力也没用”的感觉`

## Source Strategy

The script includes direct fetchers for sources that are public and currently testable, plus fallback status for sources that often block automated access:

- Direct hot lists/news: Baidu realtime hot board, Toutiao hot board, Hacker News, Google News RSS, BBC RSS, 36Kr RSS, iFanr RSS, Solidot RSS.
- Often blocked or unstable: Weibo hot search, Zhihu hot list, Reddit, WeChat 24h hot articles. When these fail, report them and use search/news/RSS alternatives to preserve useful output.

When the user explicitly requires a blocked source, try current public endpoints or web search for that source first, then disclose whether the source was directly fetched or approximated.
