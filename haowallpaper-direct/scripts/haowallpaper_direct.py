#!/usr/bin/env python3
"""Fetch haowallpaper metadata and public image links without a browser."""

from __future__ import annotations

import argparse
import gzip
import html
import json
import mimetypes
import re
import sys
import time
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, urlopen


BASE_URL = "https://haowallpaper.com"
LINK_BASE = BASE_URL + "/link"
DETAIL_PATHS = ("homeViewLook", "mobileViewLook")
DETAIL_RE = re.compile(r"(?:(?P<kind>homeViewLook|mobileViewLook)/)?(?P<id>\d{8,})")
FILE_ID_RE = re.compile(r"/(?:previewFileImg|getCroppingImg|getVideoReduce)/(?P<id>[A-Za-z0-9]{8,})")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
)

CN = {
    "category": "\u6240\u5c5e\u5206\u7c7b",
    "resolution": "\u5206\u8fa8\u7387",
    "color": "\u8272\u7cfb",
    "size": "\u5927\u5c0f",
    "publisher": "\u53d1\u5e03\u4eba",
    "publish_time": "\u53d1\u5e03\u65f6\u95f4",
    "created_at": "\u521b\u5efa\u4e8e",
    "downloads": "\u4e0b\u8f7d\u91cf",
    "favorites": "\u6536\u85cf\u91cf",
    "category_short": "\u5206\u7c7b",
}


@dataclass
class FetchResult:
    body: bytes
    url: str
    content_type: str = ""


@dataclass
class Wallpaper:
    id: str
    kind: str = "homeViewLook"
    source: str = ""
    title: str = ""
    detail_url: str = ""
    file_id: str = ""
    image_url: str = ""
    video_url: str = ""
    preview_url: str = ""
    crop_url: str = ""
    tags: list[str] = field(default_factory=list)
    category: str = ""
    resolution: str = ""
    color: str = ""
    size: str = ""
    publisher: str = ""
    publish_time: str = ""
    downloads: int | None = None
    favorites: int | None = None
    description: str = ""
    local_path: str = ""

    def key(self) -> str:
        return f"{self.kind}:{self.id}"

    def as_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v not in ("", [], None)}


def fetch(url: str, *, binary: bool = False, retries: int = 2) -> FetchResult:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "*/*" if binary else "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "identity",
        "Referer": BASE_URL + "/",
    }
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=25) as response:
                body = response.read()
                encoding = response.headers.get("content-encoding", "").lower()
                if encoding == "gzip" or body.startswith(b"\x1f\x8b"):
                    body = gzip.decompress(body)
                elif encoding == "deflate":
                    body = zlib.decompress(body)
                return FetchResult(body=body, url=response.geturl(), content_type=response.headers.get("content-type", ""))
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(0.7 * (attempt + 1))
    raise RuntimeError(f"failed to fetch {url}: {last_error}")


def fetch_text(url: str) -> str:
    return fetch(url).body.decode("utf-8", errors="replace")


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        item = clean_text(item)
        if item and item not in seen:
            result.append(item)
            seen.add(item)
    return result


def parse_attrs(tag: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    pattern = re.compile(r"([:\w-]+)\s*=\s*(['\"])(.*?)\2", re.S)
    for key, _, value in pattern.findall(tag):
        attrs[key.lower()] = html.unescape(value)
    return attrs


def parse_meta(doc: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    for match in re.finditer(r"<meta\b[^>]*>", doc, re.I | re.S):
        attrs = parse_attrs(match.group(0))
        key = attrs.get("property") or attrs.get("name")
        content = attrs.get("content")
        if key and content is not None:
            meta[key.lower()] = content
    return meta


def parse_json_ld(doc: str) -> dict[str, Any]:
    for match in re.finditer(r"<script\b[^>]*application/ld\+json[^>]*>(.*?)</script>", doc, re.I | re.S):
        attrs = parse_attrs(match.group(0).split(">", 1)[0] + ">")
        raw = attrs.get("children") or match.group(1)
        raw = html.unescape(raw).strip()
        if not raw:
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return {}


def normalize_link_url(url: str) -> str:
    return (url or "").replace("/link//common/", "/link/common/")


def public_preview_url(file_id: str) -> str:
    return f"{LINK_BASE}/common/file/previewFileImg/{file_id}" if file_id else ""


def public_crop_url(file_id: str) -> str:
    return f"{LINK_BASE}/common/file/getCroppingImg/{file_id}" if file_id else ""


def public_video_url(file_id: str) -> str:
    return f"{LINK_BASE}/common/file/getVideoReduce/{file_id}" if file_id else ""


def file_id_from_url(url: str) -> str:
    match = FILE_ID_RE.search(url or "")
    return match.group("id") if match else ""


def media_from_block(block: str) -> tuple[dict[str, str], str, str, str]:
    img_match = re.search(r"<img\b[^>]*>", block, re.I | re.S)
    img_attrs = parse_attrs(img_match.group(0)) if img_match else {}
    image_src = normalize_link_url(urljoin(BASE_URL, img_attrs.get("src", ""))) if img_attrs.get("src") else ""

    video_match = re.search(r"<video\b[^>]*>", block, re.I | re.S)
    video_attrs = parse_attrs(video_match.group(0)) if video_match else {}
    video_src = normalize_link_url(urljoin(BASE_URL, video_attrs.get("src", ""))) if video_attrs.get("src") else ""

    file_id = file_id_from_url(image_src or video_src)
    return img_attrs, image_src, video_src, file_id


def detail_url(kind: str, detail_id: str) -> str:
    return f"{BASE_URL}/{kind}/{detail_id}"


def id_to_detail_url(value: str, default_kind: str = "homeViewLook") -> tuple[str, str, str]:
    value = value.strip()
    if value.startswith("http"):
        path = urlparse(value).path.strip("/")
        parts = path.split("/")
        if len(parts) >= 2 and parts[-2] in DETAIL_PATHS and re.fullmatch(r"\d{8,}", parts[-1]):
            return parts[-1], parts[-2], f"{BASE_URL}/{parts[-2]}/{parts[-1]}"
        match = DETAIL_RE.search(value)
        if not match:
            raise ValueError(f"not a haowallpaper detail URL/id: {value}")
        kind = match.group("kind") or default_kind
        return match.group("id"), kind, detail_url(kind, match.group("id"))
    match = DETAIL_RE.fullmatch(value)
    if not match:
        raise ValueError(f"not a haowallpaper detail URL/id: {value}")
    kind = match.group("kind") or default_kind
    return match.group("id"), kind, detail_url(kind, match.group("id"))


def parse_cn_description(description: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    label_patterns = {
        "category": rf"(?:{CN['category']}|{CN['category_short']})[:\uff1a][\u300c\"]?([^,\uff0c\u3001\u300d\"]+)",
        "resolution": rf"{CN['resolution']}[:\uff1a][\u300c\"]?([^,\uff0c\u3001\u300d\"]+)",
        "color": rf"{CN['color']}[:\uff1a]([^,\uff0c\u3001]+)",
        "size": rf"{CN['size']}[:\uff1a]([^,\uff0c\u3001]+)",
        "publisher": rf"{CN['publisher']}[:\uff1a]([^,\uff0c\u3001]+)",
        "publish_time": rf"(?:{CN['publish_time']}|{CN['created_at']})[:\uff1a]([0-9:-]+(?:\s+[0-9:]+)?)",
    }
    for key, pattern in label_patterns.items():
        match = re.search(pattern, description)
        if match:
            fields[key] = clean_text(match.group(1))
    return fields


def html_field(doc: str, label: str) -> str:
    pattern = rf"{re.escape(label)}\s*[:\uff1a]\s*<span[^>]*>(.*?)</span>"
    match = re.search(pattern, doc, re.I | re.S)
    return clean_text(match.group(1)) if match else ""


def int_field(doc: str, label: str) -> int | None:
    value = html_field(doc, label)
    return parse_int(value)


def tags_from_keywords(keywords: str) -> list[str]:
    tags = [part.strip() for part in re.split(r"[,\uff0c\u3001]", keywords or "") if part.strip()]
    site_words = {
        "\u58c1\u7eb8",
        "\u58c1\u7eb8\u7f51\u7ad9",
        "\u58c1\u7eb8\u793e\u533a",
        "wallpaper",
    }
    return [tag for tag in tags if tag not in site_words]


def parse_detail(value: str, default_kind: str = "homeViewLook") -> Wallpaper:
    detail_id, kind, url = id_to_detail_url(value, default_kind=default_kind)
    doc = fetch_text(url)
    meta = parse_meta(doc)
    ld = parse_json_ld(doc)

    title = meta.get("og:title") or meta.get("twitter:title") or ""
    if not title:
        title_match = re.search(r"<title>(.*?)</title>", doc, re.I | re.S)
        title = clean_text(title_match.group(1)) if title_match else ""

    image_url = meta.get("og:image") or meta.get("twitter:image") or str(ld.get("contentUrl") or "")
    if image_url and image_url.startswith("/"):
        image_url = urljoin(BASE_URL, image_url)
    image_url = normalize_link_url(image_url)
    if image_url.endswith("/favicon.ico"):
        image_url = ""

    video_match = re.search(r"<video\b[^>]*>", doc, re.I | re.S)
    video_attrs = parse_attrs(video_match.group(0)) if video_match else {}
    raw_video_url = normalize_link_url(urljoin(BASE_URL, video_attrs.get("src", ""))) if video_attrs.get("src") else ""

    file_id = file_id_from_url(image_url or raw_video_url)
    video_file_id = file_id_from_url(raw_video_url)
    video_url = raw_video_url if raw_video_url and (not image_url or video_file_id == file_id) else ""
    description = meta.get("description") or meta.get("og:description") or str(ld.get("description") or "")
    desc_fields = parse_cn_description(description)
    tags = tags_from_keywords(meta.get("keywords", ""))

    resolution = desc_fields.get("resolution") or html_field(doc, CN["resolution"])
    category = desc_fields.get("category") or html_field(doc, CN["category_short"])
    size = desc_fields.get("size") or html_field(doc, CN["size"])
    color = desc_fields.get("color") or html_field(doc, CN["color"])

    return Wallpaper(
        id=detail_id,
        kind=kind,
        source="detail",
        title=clean_text(title),
        detail_url=url,
        file_id=file_id,
        image_url=image_url or (public_preview_url(file_id) if not video_url else ""),
        video_url=video_url,
        preview_url=public_preview_url(file_id) if image_url else "",
        crop_url=public_crop_url(file_id),
        tags=unique(tags),
        category=category,
        resolution=resolution,
        color=color,
        size=size,
        publisher=desc_fields.get("publisher", ""),
        publish_time=desc_fields.get("publish_time", ""),
        downloads=int_field(doc, CN["downloads"]),
        favorites=int_field(doc, CN["favorites"]),
        description=clean_text(description),
    )


def parse_int(value: str) -> int | None:
    digits = re.sub(r"[^\d]", "", value or "")
    return int(digits) if digits else None


def split_cards(doc: str) -> list[str]:
    starts = [m.start() for m in re.finditer(r'<div class="card"', doc)]
    cards: list[str] = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else doc.find("</template>", start)
        if end == -1:
            end = min(len(doc), start + 9000)
        cards.append(doc[start:end])
    return cards


def parse_desktop_card(card: str, source: str) -> Wallpaper | None:
    id_match = re.search(r'href=["\']/homeViewLook/(?P<id>\d{8,})["\']', card)
    if not id_match:
        return None
    detail_id = id_match.group("id")
    attrs, image_src, video_src, file_id = media_from_block(card)
    label_block_match = re.search(r'<div class="labelDiv"[^>]*>(.*?)<div class="card--button"', card, re.I | re.S)
    label_block = label_block_match.group(1) if label_block_match else ""
    labels = re.findall(r"<span\b[^>]*>(.*?)</span>", label_block, re.I | re.S)
    bottom = card[card.find("card-bottom") :] if "card-bottom" in card else ""
    values = [
        clean_text(match)
        for match in re.findall(r"<div[^>]*>\s*<span[^>]*></span>\s*([^<]+)</div>", bottom, re.I | re.S)
    ][:4]

    return Wallpaper(
        id=detail_id,
        kind="homeViewLook",
        source=source,
        title=clean_text(attrs.get("alt") or attrs.get("title") or ""),
        detail_url=detail_url("homeViewLook", detail_id),
        file_id=file_id,
        image_url=public_preview_url(file_id),
        video_url=video_src,
        preview_url=public_preview_url(file_id),
        crop_url=image_src or public_crop_url(file_id),
        tags=unique(labels),
        favorites=parse_int(values[0]) if len(values) > 0 else None,
        downloads=parse_int(values[1]) if len(values) > 1 else None,
        resolution=values[2] if len(values) > 2 else "",
        size=values[3] if len(values) > 3 else "",
    )


def parse_mobile_cards(doc: str, source: str) -> list[Wallpaper]:
    pattern = re.compile(
        r'<a\b(?=[^>]*href=["\']/mobileViewLook/(?P<id>\d{8,})["\'])[^>]*>.*?</a>',
        re.I | re.S,
    )
    items: list[Wallpaper] = []
    for match in pattern.finditer(doc):
        block = match.group(0)
        attrs, image_src, video_src, file_id = media_from_block(block)
        detail_id = match.group("id")
        is_video = bool(video_src and not image_src)
        items.append(
            Wallpaper(
                id=detail_id,
                kind="mobileViewLook",
                source=source,
                title=clean_text(attrs.get("alt") or attrs.get("title") or ""),
                detail_url=detail_url("mobileViewLook", detail_id),
                file_id=file_id,
                image_url=public_preview_url(file_id) if not is_video else "",
                video_url=video_src,
                preview_url=public_preview_url(file_id) if not is_video else "",
                crop_url=image_src or public_crop_url(file_id),
            )
        )
    return items


def nearest_forum_title(doc: str, start: int) -> str:
    prefix = doc[max(0, start - 4000) : start]
    matches = list(re.finditer(r'<span class="title-text">(.*?)</span>', prefix, re.I | re.S))
    return clean_text(matches[-1].group(1)) if matches else ""


def parse_forum_embeds(doc: str) -> list[Wallpaper]:
    pattern = re.compile(
        r'<a\b(?=[^>]*href=["\']/(?P<kind>homeViewLook|mobileViewLook)/(?P<id>\d{8,})["\'])[^>]*>.*?</a>',
        re.I | re.S,
    )
    items: list[Wallpaper] = []
    for match in pattern.finditer(doc):
        block = match.group(0)
        attrs, image_src, video_src, file_id = media_from_block(block)
        kind = match.group("kind")
        detail_id = match.group("id")
        title = clean_text(attrs.get("alt") or attrs.get("title") or nearest_forum_title(doc, match.start()))
        is_video = bool(video_src and not image_src)
        items.append(
            Wallpaper(
                id=detail_id,
                kind=kind,
                source="forum",
                title=title,
                detail_url=detail_url(kind, detail_id),
                file_id=file_id,
                image_url=public_preview_url(file_id) if not is_video else "",
                video_url=video_src,
                preview_url=public_preview_url(file_id) if not is_video else "",
                crop_url=image_src or public_crop_url(file_id),
            )
        )
    return items


def parse_search_page(doc: str, source: str) -> list[Wallpaper]:
    items: list[Wallpaper] = []
    if source in {"home", "root"}:
        items.extend(item for item in (parse_desktop_card(card, source) for card in split_cards(doc)) if item)
    if source == "mobile":
        items.extend(parse_mobile_cards(doc, source))
    if source == "forum":
        items.extend(parse_forum_embeds(doc))
    return dedupe(items)


def source_url(source: str, keyword: str, page: int, rows: int, sort_type: int) -> str:
    paths = {
        "home": "/homeView",
        "root": "/",
        "mobile": "/mobileView",
        "forum": "/wallpaperForum",
    }
    params: dict[str, Any] = {"page": page, "search": keyword}
    if source != "forum":
        params.update({"sortType": sort_type, "rows": rows})
    else:
        params.update({"rows": rows})
    return f"{BASE_URL}{paths[source]}?{urlencode(params)}"


def parse_sources(value: str) -> list[str]:
    aliases = {
        "all": ["home", "mobile", "forum"],
        "desktop": ["home"],
        "pc": ["home"],
        "home": ["home"],
        "root": ["root"],
        "mobile": ["mobile"],
        "phone": ["mobile"],
        "forum": ["forum"],
        "community": ["forum"],
    }
    result: list[str] = []
    for part in re.split(r"[,，、\s]+", value.strip()):
        if not part:
            continue
        if part not in aliases:
            raise ValueError(f"unknown source {part!r}; use home,mobile,forum,root,all")
        result.extend(aliases[part])
    return unique(result)


def merge_item(old: Wallpaper, new: Wallpaper) -> Wallpaper:
    if new.source and new.source not in old.source.split(","):
        old.source = ",".join(filter(None, [old.source, new.source]))
    for field_name in (
        "title",
        "file_id",
        "image_url",
        "video_url",
        "preview_url",
        "crop_url",
        "category",
        "resolution",
        "color",
        "size",
        "publisher",
        "publish_time",
        "description",
    ):
        if not getattr(old, field_name) and getattr(new, field_name):
            setattr(old, field_name, getattr(new, field_name))
    old.tags = unique(old.tags + new.tags)
    if old.downloads is None and new.downloads is not None:
        old.downloads = new.downloads
    if old.favorites is None and new.favorites is not None:
        old.favorites = new.favorites
    if new.local_path and not old.local_path:
        old.local_path = new.local_path
    return old


def dedupe(items: list[Wallpaper]) -> list[Wallpaper]:
    seen: dict[str, Wallpaper] = {}
    for item in items:
        key = item.key()
        if key in seen:
            merge_item(seen[key], item)
        else:
            seen[key] = item
    return list(seen.values())


def hydrate_details(items: list[Wallpaper]) -> list[Wallpaper]:
    hydrated: list[Wallpaper] = []
    for item in items:
        try:
            detail = parse_detail(item.detail_url, default_kind=item.kind)
            detail.source = item.source
            hydrated.append(merge_item(item, detail))
        except Exception as exc:
            item.description = item.description or f"detail hydrate failed: {exc}"
            hydrated.append(item)
    return hydrated


def filter_media(items: list[Wallpaper], media: str) -> list[Wallpaper]:
    if media == "all":
        return items
    if media == "image":
        return [item for item in items if item.image_url or item.preview_url]
    if media == "video":
        return [item for item in items if item.video_url and not (item.image_url or item.preview_url)]
    raise ValueError(f"unknown media filter {media!r}")


def search(
    keyword: str,
    *,
    page: int = 1,
    pages: int = 1,
    rows: int = 30,
    sort_type: int = 3,
    sources: list[str] | None = None,
    limit: int = 0,
    hydrate_detail: bool = False,
    media: str = "all",
) -> list[Wallpaper]:
    sources = sources or ["home", "mobile", "forum"]
    results: list[Wallpaper] = []
    for source in sources:
        for page_num in range(page, page + pages):
            doc = fetch_text(source_url(source, keyword, page_num, rows, sort_type))
            page_items = parse_search_page(doc, source)
            results.extend(page_items)
    results = dedupe(results)
    if hydrate_detail:
        results = hydrate_details(results)
    results = filter_media(results, media)
    results.sort(key=lambda item: (item.downloads or 0, item.favorites or 0), reverse=True)
    return results[:limit] if limit > 0 else results


def safe_filename(value: str, fallback: str) -> str:
    value = clean_text(value) or fallback
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    value = re.sub(r"\s+", " ", value).strip(" .")
    return value[:120] or fallback


def guess_extension(content_type: str, body: bytes) -> str:
    if body.startswith(b"\x89PNG"):
        return ".png"
    if body.startswith(b"\xff\xd8"):
        return ".jpg"
    if body.startswith(b"RIFF") and body[8:12] == b"WEBP":
        return ".webp"
    if len(body) > 12 and body[4:8] == b"ftyp":
        return ".mp4"
    ctype = content_type.split(";", 1)[0].strip().lower()
    if ctype == "video/mp4":
        return ".mp4"
    ext = mimetypes.guess_extension(ctype) if ctype else ""
    if ext == ".jpe":
        return ".jpg"
    return ext or ".jpg"


def download_wallpaper(item: Wallpaper, directory: Path) -> Wallpaper:
    url = item.image_url or item.video_url or item.preview_url
    if not url:
        raise RuntimeError(f"no public media URL for {item.id}")
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise RuntimeError(f"cannot create download directory {directory}: {exc}") from exc
    result = fetch(url, binary=True)
    ext = guess_extension(result.content_type, result.body)
    name = safe_filename(item.title, item.id)
    path = directory / f"{name}-{item.file_id or item.id}{ext}"
    path.write_bytes(result.body)
    item.local_path = str(path.resolve())
    return item


def print_markdown(items: list[Wallpaper]) -> None:
    for index, item in enumerate(items, 1):
        fields = [f"source: {item.source}", f"type: {item.kind.replace('ViewLook', '')}"]
        if item.downloads is not None:
            fields.append(f"downloads: {item.downloads}")
        if item.favorites is not None:
            fields.append(f"favorites: {item.favorites}")
        if item.resolution:
            fields.append(f"resolution: {item.resolution}")
        if item.size:
            fields.append(f"size: {item.size}")
        print(f"{index}. {item.title or item.id}")
        print(f"   detail: {item.detail_url}")
        print(f"   media: {item.image_url or item.video_url or item.preview_url}")
        print(f"   meta: {', '.join(fields)}")
        if item.tags:
            print(f"   tags: {', '.join(item.tags)}")
        if item.local_path:
            print(f"   saved: {item.local_path}")


def emit(items: list[Wallpaper], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps([item.as_dict() for item in items], ensure_ascii=False, indent=2))
    else:
        print_markdown(items)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    detail = sub.add_parser("detail", help="parse one detail URL or id")
    detail.add_argument("value", help="detail URL or numeric id")
    detail.add_argument("--kind", choices=list(DETAIL_PATHS), default="homeViewLook", help="kind for bare numeric ids")
    detail.add_argument("--download", metavar="DIR", help="download the public image URL to DIR")
    detail.add_argument("--format", choices=["markdown", "json"], default="markdown")

    search_parser = sub.add_parser("search", help="search by keyword/tag across sources")
    search_parser.add_argument("keyword")
    search_parser.add_argument("--page", type=int, default=1, help="first page number")
    search_parser.add_argument("--pages", type=int, default=3, help="number of pages to collect per source")
    search_parser.add_argument("--rows", type=int, default=30)
    search_parser.add_argument("--sort-type", type=int, default=3, help="3 is site hot/download sorting where supported")
    search_parser.add_argument("--sources", default="home,mobile,forum", help="home,mobile,forum,root,all")
    search_parser.add_argument("--limit", type=int, default=0)
    search_parser.add_argument("--hydrate-detail", action="store_true", help="visit each detail page to fill metadata/stats")
    search_parser.add_argument("--media", choices=["all", "image", "video"], default="all", help="filter by public media type")
    search_parser.add_argument("--download", metavar="DIR", help="download each public image URL to DIR")
    search_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    try:
        if args.command == "detail":
            items = [parse_detail(args.value, default_kind=args.kind)]
        else:
            items = search(
                args.keyword,
                page=args.page,
                pages=max(1, args.pages),
                rows=max(1, args.rows),
                sort_type=args.sort_type,
                sources=parse_sources(args.sources),
                limit=args.limit,
                hydrate_detail=args.hydrate_detail,
                media=args.media,
            )

        if args.download:
            target = Path(args.download)
            for item in items:
                download_wallpaper(item, target)

        emit(items, args.format)
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
