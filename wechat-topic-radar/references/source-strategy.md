# Source Strategy

Use direct public endpoints first, then disclose blocked sources clearly.

Direct sources currently implemented in `scripts/topic_radar.py`:

- Baidu realtime hot board: parses embedded JSON from `https://top.baidu.com/board?tab=realtime`.
- Toutiao hot board: reads JSON from `https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc`.
- Google News RSS: broad Chinese news feed for international and domestic trend signals.
- BBC World RSS: international news for cross-border topic localization.
- 36Kr RSS: Chinese business/venture/technology signal.
- iFanr RSS: consumer technology signal.
- Solidot RSS: technology/community signal.
- Hacker News Firebase API: global technology/startup developer signal.

Known unstable or frequently blocked sources:

- Weibo hot search public AJAX endpoint often returns 403.
- Zhihu hot-list API often returns 401 without authorized browser context.
- Reddit JSON often returns 403 to automated requests.
- WeChat 24h hot articles lack a stable official public endpoint. TopHub has a `/c/wxmp` category page but does not expose individual account cards without widget/subscription/API access in this environment; use search, commercial APIs, or manually supplied links when this source is required.

When blocked sources matter, try a fresh web search or browser session, then state whether the result is direct, approximate, or unavailable.
