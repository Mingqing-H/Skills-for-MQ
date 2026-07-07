#!/usr/bin/env python3
"""Collect public hot-list/news signals and rank WeChat article topic ideas."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Callable, Iterable

USER_AGENT = "Mozilla/5.0 (compatible; WechatTopicRadar/1.0; +https://openai.com)"
MOMOYU_CACHE = None
MOMOYU_ERROR = None


@dataclass
class SourceItem:
    source: str
    title: str
    url: str = ""
    summary: str = ""
    rank: int = 999
    heat: float = 0.0
    category: str = "news"
    lang: str = "zh"


@dataclass
class SourceStatus:
    source: str
    ok: bool
    count: int
    message: str = ""


def fetch_text(url: str, timeout: int = 15, accept: str = "*/*") -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": accept,
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.7",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, "ignore")


def clean_text(value: str) -> str:
    value = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    return re.sub(r"\s+", " ", value).strip()


def parse_rss(source: str, url: str, category: str, limit: int = 25, lang: str = "zh") -> list[SourceItem]:
    xml_text = fetch_text(url, accept="application/rss+xml,application/xml,text/xml")
    root = ET.fromstring(xml_text)
    items: list[SourceItem] = []
    for rank, node in enumerate(root.findall(".//item")[:limit], start=1):
        title = clean_text(node.findtext("title", ""))
        if not title:
            continue
        link = clean_text(node.findtext("link", ""))
        desc = clean_text(node.findtext("description", ""))
        items.append(SourceItem(source, title, link, desc[:240], rank, max(1, limit - rank + 1), category, lang))
    return items



def parse_atom(source: str, url: str, category: str, limit: int = 25, lang: str = "en") -> list[SourceItem]:
    xml_text = fetch_text(url, accept="application/atom+xml,application/xml,text/xml")
    root = ET.fromstring(xml_text)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    items: list[SourceItem] = []
    for rank, node in enumerate(root.findall("a:entry", ns)[:limit], start=1):
        title = clean_text(node.findtext("a:title", "", ns))
        if not title:
            continue
        link_node = node.find("a:link", ns)
        link = link_node.get("href", "") if link_node is not None else ""
        desc = clean_text(node.findtext("a:content", "", ns) or node.findtext("a:summary", "", ns))
        items.append(SourceItem(source, title, link, desc[:240], rank, max(1, limit - rank + 1), category, lang))
    return items

def fetch_baidu() -> list[SourceItem]:
    text = fetch_text("https://top.baidu.com/board?tab=realtime", accept="text/html")
    match = re.search(r"<!--s-data:(.*?)-->", text, re.S)
    if not match:
        raise ValueError("Baidu embedded hot-list JSON not found")
    data = json.loads(match.group(1))
    content = []
    for card in data.get("data", {}).get("cards", []):
        if card.get("component") == "hotList":
            content = card.get("content", [])
            break
    items = []
    for rank, row in enumerate(content[:30], start=1):
        title = clean_text(row.get("word") or row.get("query") or "")
        if not title:
            continue
        url = row.get("appUrl") or row.get("rawUrl") or ""
        heat = float(row.get("hotScore") or row.get("hotIndex") or max(1, 31 - rank))
        summary = clean_text(row.get("desc") or row.get("show") or "")
        items.append(SourceItem("百度热搜", title, url, summary[:240], rank, heat, "hotlist", "zh"))
    return items


def fetch_toutiao() -> list[SourceItem]:
    url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
    data = json.loads(fetch_text(url, accept="application/json"))
    items = []
    for rank, row in enumerate(data.get("data", [])[:30], start=1):
        title = clean_text(row.get("Title") or row.get("title") or "")
        if not title:
            continue
        link = row.get("Url") or row.get("url") or ""
        heat = float(row.get("HotValue") or row.get("hot_value") or max(1, 31 - rank))
        label = clean_text(row.get("Label") or row.get("label") or "")
        if label in {"recentProgress", "word", "tag"}:
            label = ""
        items.append(SourceItem("今日头条热榜", title, link, label, rank, heat, "hotlist", "zh"))
    return items


def fetch_hacker_news(limit: int = 20) -> list[SourceItem]:
    ids = json.loads(fetch_text("https://hacker-news.firebaseio.com/v0/topstories.json", accept="application/json"))
    items = []
    for rank, item_id in enumerate(ids[:limit], start=1):
        data = json.loads(fetch_text(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json", accept="application/json"))
        title = clean_text(data.get("title", ""))
        if not title:
            continue
        score = float(data.get("score") or max(1, limit - rank + 1))
        url = data.get("url") or f"https://news.ycombinator.com/item?id={item_id}"
        items.append(SourceItem("Hacker News", title, url, "", rank, score, "tech", "en"))
        time.sleep(0.03)
    return items




def fetch_52vmy_weibo() -> list[SourceItem]:
    text = fetch_text("https://api.52vmy.cn/api/wl/hot?type=weibo", accept="application/json,text/plain,*/*")
    start = text.find("{")
    if start > 0:
        text = text[start:]
    data = json.loads(text)
    items = []
    for rank, row in enumerate((data.get("data") or [])[:50], start=1):
        title = clean_text(row.get("title") or "")
        if not title:
            continue
        items.append(SourceItem("微博热搜-52vmy聚合", title, row.get("url") or row.get("mobilUrl") or "", clean_text(row.get("hot") or ""), rank, max(1, 51 - rank), "hotlist", "zh"))
    return items


def fetch_bilibili_popular() -> list[SourceItem]:
    data = json.loads(fetch_text("https://api.bilibili.com/x/web-interface/popular?ps=30&pn=1", accept="application/json"))
    items = []
    for rank, row in enumerate(data.get("data", {}).get("list", [])[:30], start=1):
        title = clean_text(row.get("title") or "")
        if not title:
            continue
        url = f"https://www.bilibili.com/video/{row.get('bvid')}" if row.get("bvid") else ""
        stat = row.get("stat", {}) or {}
        heat = float(stat.get("view") or max(1, 31 - rank))
        summary = clean_text(row.get("desc") or row.get("tname") or "")
        items.append(SourceItem("B站热门", title, url, summary[:240], rank, heat, "community", "zh"))
    return items


def fetch_sspai() -> list[SourceItem]:
    return parse_rss("少数派 RSS", "https://sspai.com/feed", "tech", 25, "zh")


def fetch_ithome() -> list[SourceItem]:
    return parse_rss("IT之家 RSS", "https://www.ithome.com/rss/", "tech", 25, "zh")

def fetch_zhihu_hot() -> list[SourceItem]:
    data = json.loads(fetch_text("https://api.zhihu.com/topstory/hot-list", accept="application/json"))
    items = []
    for rank, row in enumerate(data.get("data", [])[:30], start=1):
        target = row.get("target", {})
        title = clean_text(target.get("title") or row.get("title") or "")
        if not title:
            continue
        url = target.get("url") or ""
        if url.startswith("https://api.zhihu.com/questions/"):
            url = url.replace("https://api.zhihu.com/questions/", "https://www.zhihu.com/question/")
        summary = clean_text(target.get("excerpt") or row.get("detail_text") or "")
        heat = float(target.get("follower_count") or max(1, 31 - rank))
        items.append(SourceItem("知乎热榜", title, url, summary[:240], rank, heat, "hotlist", "zh"))
    return items


def fetch_reddit_rss() -> list[SourceItem]:
    return parse_atom("Reddit r/all RSS", "https://www.reddit.com/r/all/hot/.rss", "community", 25, "en")


def fetch_momoyu_data() -> dict:
    global MOMOYU_CACHE, MOMOYU_ERROR
    if MOMOYU_CACHE is not None:
        return MOMOYU_CACHE
    if MOMOYU_ERROR is not None:
        raise ValueError(MOMOYU_ERROR)
    try:
        MOMOYU_CACHE = json.loads(fetch_text("https://momoyu.cc/api/hot/list", timeout=8, accept="application/json"))
        return MOMOYU_CACHE
    except Exception as exc:
        MOMOYU_ERROR = f"Momoyu unavailable: {type(exc).__name__}: {str(exc)[:120]}"
        raise ValueError(MOMOYU_ERROR) from exc


def fetch_momoyu_platform(source_key: str, source_name: str, category: str = "hotlist") -> list[SourceItem]:
    data = fetch_momoyu_data()
    for block in data.get("data", []):
        if block.get("source_key") == source_key:
            items = []
            for rank, row in enumerate(block.get("data", [])[:50], start=1):
                title = clean_text(row.get("title") or "")
                if not title:
                    continue
                items.append(SourceItem(source_name, title, row.get("link") or "", clean_text(row.get("extra") or ""), rank, max(1, 51 - rank), category, "zh"))
            return items
    raise ValueError(f"Momoyu source not found: {source_key}")


def fetch_momoyu_weibo() -> list[SourceItem]:
    return fetch_momoyu_platform("weibo", "微博热搜-Momoyu聚合")


def fetch_momoyu_douban() -> list[SourceItem]:
    return fetch_momoyu_platform("douban", "豆瓣热话-Momoyu聚合", "community")


def fetch_momoyu_bilibili() -> list[SourceItem]:
    return fetch_momoyu_platform("bilibili", "B站热榜-Momoyu聚合", "community")


def fetch_momoyu_huxiu() -> list[SourceItem]:
    return fetch_momoyu_platform("huxiu", "虎嗅热榜-Momoyu聚合", "business")


def fetch_momoyu_zhidemai() -> list[SourceItem]:
    return fetch_momoyu_platform("zhidemai", "值得买热门-Momoyu聚合", "consumer")


def fetch_momoyu_juejin() -> list[SourceItem]:
    return fetch_momoyu_platform("juejin", "掘金热榜-Momoyu聚合", "tech")

def fetch_google_news() -> list[SourceItem]:
    return parse_rss("Google News", "https://news.google.com/rss?hl=zh-CN&gl=CN&ceid=CN:zh-Hans", "world", 30, "zh")


def fetch_bbc_world() -> list[SourceItem]:
    return parse_rss("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml", "world", 20, "en")


def fetch_36kr() -> list[SourceItem]:
    return parse_rss("36氪", "https://36kr.com/feed", "business", 25, "zh")


def fetch_ifanr() -> list[SourceItem]:
    return parse_rss("爱范儿", "https://www.ifanr.com/feed", "tech", 20, "zh")


def fetch_solidot() -> list[SourceItem]:
    return parse_rss("Solidot", "https://www.solidot.org/index.rss", "tech", 20, "zh")


def probe_blocked_source(url: str) -> list[SourceItem]:
    fetch_text(url)
    return []


FETCHERS: list[tuple[str, Callable[[], list[SourceItem]]]] = [
    ("百度热搜", fetch_baidu),
    ("今日头条热榜", fetch_toutiao),
    ("微博热搜-52vmy聚合", fetch_52vmy_weibo),
    ("知乎热榜", fetch_zhihu_hot),
    ("B站热门", fetch_bilibili_popular),
    ("Reddit r/all RSS", fetch_reddit_rss),
    ("少数派 RSS", fetch_sspai),
    ("IT之家 RSS", fetch_ithome),
    ("Google News", fetch_google_news),
    ("BBC World", fetch_bbc_world),
    ("36氪", fetch_36kr),
    ("爱范儿", fetch_ifanr),
    ("Solidot", fetch_solidot),
    ("Hacker News", fetch_hacker_news),
    ("微博热搜-官方直连探测", lambda: probe_blocked_source("https://weibo.com/ajax/side/hotSearch")),
]

STOPWORDS = {"的", "了", "和", "与", "在", "对", "是", "有", "为", "将", "被", "从", "到", "中", "后", "this", "that", "with", "from", "into", "over", "after", "about", "says", "will", "news"}
VALUE_TERMS = {
    "职场": ["裁员", "招聘", "就业", "工资", "打工", "老板", "公司", "职场", "员工", "上班", "job", "work", "worker", "employee"],
    "金钱": ["房价", "消费", "降价", "涨价", "赚钱", "收入", "理财", "存款", "经济", "补贴", "price", "money", "revenue"],
    "家庭": ["孩子", "父母", "教育", "高考", "中考", "婚姻", "家庭", "养老", "生育"],
    "科技AI": ["AI", "人工智能", "模型", "芯片", "机器人", "OpenAI", "苹果", "华为", "数据", "Deno", "Python", "JavaScript", "GitHub", "software", "desktop", "browser", "app", "掘金", "代码", "开发者"],
    "健康": ["医院", "医生", "医保", "药", "健康", "食品", "安全", "睡眠"],
    "消费": ["手机", "汽车", "新能源", "品牌", "外卖", "电商", "旅游", "酒店", "值得买", "平替", "优惠", "购物"],
}
EMOTION_TERMS = ["争议", "回应", "曝光", "调查", "冲突", "道歉", "焦虑", "离谱", "突然", "首次", "真相", "暴雷", "热议", "担心"]
RISK_TERMS = ["传言", "网传", "未证实", "敏感", "涉政", "死亡", "自杀", "刑事", "医疗事故", "谣言"]
SENSITIVE_TERMS = ["总书记", "习近平", "党中央", "中央八项规定", "八项规定", "六项规定", "老党员", "党员", "求是", "党纪", "干部作风", "强国建设", "民族复兴"]


def tokenize(title: str) -> list[str]:
    ascii_words = re.findall(r"[A-Za-z][A-Za-z0-9+\-.]{1,}", title)
    zh_chunks = re.findall(r"[\u4e00-\u9fff]{2,}", title)
    return [t for t in ascii_words + zh_chunks if t.lower() not in STOPWORDS and len(t) >= 2]


def classify(title: str) -> tuple[str, list[str]]:
    hits = []
    lower = title.lower()
    for label, words in VALUE_TERMS.items():
        if any(word.lower() in lower for word in words):
            hits.append(label)
    return (hits[0] if hits else "社会观察", hits)


def canonical_key(title: str) -> str:
    tokens = tokenize(title)
    return "|".join(tokens[:3]).lower() if tokens else title[:12].lower()


def score_item(item: SourceItem, source_counts: Counter[str]) -> tuple[float, dict]:
    category, tags = classify(item.title)
    heat_score = min(30.0, 30.0 / max(1, item.rank)) + (8 if item.source in {"百度热搜", "今日头条热榜"} else 0)
    proximity = 8 * len(tags)
    emotion = sum(4 for term in EMOTION_TERMS if term.lower() in item.title.lower())
    practical = 8 if category in {"职场", "金钱", "家庭", "科技AI", "健康", "消费"} else 3
    international = 5 if item.lang == "en" or item.category == "world" else 0
    repetition = min(10, source_counts[canonical_key(item.title)] * 3)
    risk_text = (item.title + " " + item.summary).lower()
    risk = sum(6 for term in RISK_TERMS if term.lower() in risk_text)
    risk += sum(12 for term in SENSITIVE_TERMS if term.lower() in risk_text)
    score = heat_score + proximity + emotion + practical + international + repetition - risk
    return score, {"category": category, "tags": tags, "heat_score": round(heat_score, 1), "reader_value": proximity + practical, "emotion": emotion, "international": international, "risk_penalty": risk}


def topic_seed(title: str, max_len: int = 34) -> str:
    title = title.strip(" -_")
    title = title.replace("氪星晚报｜", "").replace("氪星晚报：", "")
    title = re.sub(r"^(早报|晚报|焦点分析)[：:｜|丨]", "", title)
    title = re.split(r"[；;]", title)[0]
    title = re.split(r"[｜|丨]", title)[0]
    if len(title) <= max_len:
        return title
    return title[:max_len].rstrip("，。；、：: ") + "..."


def make_wechat_title(item: SourceItem, meta: dict, profile: str) -> str:
    title = topic_seed(item.title)
    category = str(meta["category"])
    if item.lang == "en":
        return f"国外正在热议的「{title}」，和我们的工作/生活有什么关系？"
    if category == "职场":
        return f"「{title}」背后，打工人最该警惕什么？"
    if category == "金钱":
        return f"「{title}」：普通人开始重新计算安全感"
    if category == "家庭":
        return f"「{title}」刺中的，是每个家庭的长期焦虑"
    if category == "科技AI":
        return f"「{title}」：AI真正改变的，可能是你的工作方式"
    if category == "消费":
        return f"「{title}」：这届消费者不再轻易为体面买单"
    if category == "健康":
        return f"「{title}」提醒我们：真正贵的是忽视风险"
    return f"「{title}」：热搜背后，普通人为什么会在意？"


def style_for(item: SourceItem, meta: dict) -> str:
    category = str(meta["category"])
    if item.lang == "en" or item.category == "world":
        return "严谨解释 + 本土化转译，语气克制，少用夸张判断。"
    if category in {"职场", "金钱"}:
        return "第一人称场景开头 + 犀利但克制的社会观察，结尾给读者一个可执行判断。"
    if category == "家庭":
        return "温和共情 + 具体家庭场景，避免说教，保留复杂性。"
    if category == "科技AI":
        return "体验型/解释型结合，用具体工具或岗位变化切入，避免技术黑话。"
    if category == "健康":
        return "严谨提醒型，事实核查优先，不制造恐慌。"
    return "故事化开头 + 观点评论，语气可以略带惊讶，但不要标题党过度。"


def angle_for(item: SourceItem, meta: dict) -> str:
    category = str(meta["category"])
    if category == "职场":
        return "从一个普通员工/求职者的具体处境切入，写清楚它改变了什么预期。"
    if category == "金钱":
        return "从一次消费、存钱或资产选择切入，讨论安全感和风险排序。"
    if category == "家庭":
        return "从父母、孩子或伴侣之间的一次小冲突切入，讨论长期压力。"
    if category == "科技AI":
        return "从亲测、案例或岗位任务切入，写技术如何影响普通人的效率和边界。"
    if category == "消费":
        return "从一次不下单/换平替/退订切入，写消费者心理变化。"
    if item.lang == "en":
        return "先解释海外事件是什么，再转译成国内读者能用的趋势判断。"
    return "不要复述新闻，抓住它引发的一个具体生活问题。"


def risk_note(item: SourceItem, meta: dict) -> str:
    if float(meta.get("risk_penalty", 0)) > 0:
        return "涉及争议或可能未完全证实的信息，写作前需要二次核查权威来源，避免下定论。"
    if item.lang == "en" or item.category == "world":
        return "海外来源需要核对中文语境适配，避免过度类比。"
    return "注意补充事实来源，避免只凭热搜情绪写成泛泛评论。"


def reason_for(item: SourceItem, meta: dict) -> str:
    category = str(meta["category"])
    if category == "社会观察":
        return "有公共讨论度，适合从热搜情绪继续下钻到具体生活经验，避免只做新闻复述。"
    return f"兼具{category}相关性和即时热度，容易把大事件转译成读者关心的自身利益、焦虑或行动判断。"


def target_reader_for(category: str, profile: str) -> str:
    if profile:
        return f"优先匹配账号定位：{profile}"
    mapping = {
        "职场": "25-40岁城市白领、管理者、求职者。",
        "金钱": "关注收入、消费、资产安全感的城市读者。",
        "家庭": "年轻父母、已婚读者、承担家庭责任的中青年。",
        "科技AI": "知识工作者、内容从业者、产品/运营/技术相关读者。",
        "消费": "关注品牌、性价比和生活方式变化的城市消费者。",
        "健康": "关注家庭健康、食品安全和公共风险的普通读者。",
    }
    return mapping.get(category, "对公共议题、社会情绪和生活变化敏感的泛知识型读者。")


def collect_sources() -> tuple[list[SourceItem], list[SourceStatus]]:
    all_items: list[SourceItem] = []
    statuses: list[SourceStatus] = []
    for name, fetcher in FETCHERS:
        try:
            items = fetcher()
            all_items.extend(items)
            statuses.append(SourceStatus(name, True, len(items), "ok"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, ET.ParseError, json.JSONDecodeError) as exc:
            statuses.append(SourceStatus(name, False, 0, f"{type(exc).__name__}: {str(exc)[:120]}"))
    return all_items, statuses


def rank_topics(items: Iterable[SourceItem], top_n: int, profile: str) -> list[dict]:
    item_list = [item for item in items if len(item.title) >= 4]
    source_counts = Counter(canonical_key(item.title) for item in item_list)
    scored = []
    seen = set()
    for item in item_list:
        key = canonical_key(item.title)
        if key in seen:
            continue
        seen.add(key)
        score, meta = score_item(item, source_counts)
        if float(meta.get("risk_penalty", 0)) >= 18:
            continue
        scored.append((score, item, meta))
    scored.sort(key=lambda row: row[0], reverse=True)

    topics = []
    category_quota = Counter()
    for score, item, meta in scored:
        category = str(meta["category"])
        if category_quota[category] >= 3 and len(topics) < top_n - 2:
            continue
        category_quota[category] += 1
        topics.append({
            "title": make_wechat_title(item, meta, profile),
            "raw_topic": item.title,
            "score": round(score, 1),
            "category": category,
            "details": item.summary or f"来自{item.source}的实时热点/新闻信号，榜单排名第 {item.rank}。",
            "source_basis": f"{item.source}，排名/序号 {item.rank}" + (f"，链接：{item.url}" if item.url and len(item.url) < 180 else ""),
            "recommendation_reason": reason_for(item, meta),
            "target_reader": target_reader_for(category, profile),
            "writing_angle": angle_for(item, meta),
            "style": style_for(item, meta),
            "risk_note": risk_note(item, meta),
        })
        if len(topics) >= top_n:
            break
    return topics


def render_markdown(topics: list[dict], statuses: list[SourceStatus]) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    ok = [s for s in statuses if s.ok and s.count > 0]
    failed = [s for s in statuses if not s.ok]
    lines = [f"# 今日公众号选题 Top {len(topics)}", "", f"生成时间：{now}", "", "可用来源：" + "、".join(f"{s.source}({s.count})" for s in ok)]
    if failed:
        lines.append("降级/不可直连来源：" + "、".join(s.source for s in failed))
    lines.append("")
    for idx, topic in enumerate(topics, start=1):
        lines.extend([
            f"### {idx}. 标题：{topic['title']}", "",
            f"详情：{topic['details']}", "",
            f"来源依据：{topic['source_basis']}", "",
            f"推荐原因：{topic['recommendation_reason']}（评分：{topic['score']}，类型：{topic['category']}）", "",
            f"目标读者：{topic['target_reader']}", "",
            f"写作角度：{topic['writing_angle']}", "",
            f"推荐风格：{topic['style']}", "",
            f"风险提醒：{topic['risk_note']}", "",
        ])
    return "\n".join(lines).strip() + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", type=int, default=10, help="number of topic ideas to output")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--profile", default="", help="account positioning and target reader profile")
    args = parser.parse_args(argv)

    items, statuses = collect_sources()
    topics = rank_topics(items, args.top, args.profile)
    payload = {"generated_at": dt.datetime.now().isoformat(timespec="seconds"), "source_status": [asdict(s) for s in statuses], "topics": topics}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(topics, statuses))
    return 0 if topics else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
