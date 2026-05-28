---
name: haowallpaper-direct
description: Fetch haowallpaper.com wallpaper metadata, tags, download counts, public image links, and optional local image files without browser automation. Use when the user provides a haowallpaper detail URL/id, asks to search desktop/mobile/community wallpapers by keyword/tag, or wants fast multi-page direct-link extraction/downloads without Playwright or page interaction.
---

# HaoWallpaper Direct

Use the bundled Python script first. It reads public SSR HTML and meta tags directly, so it is faster and cheaper than browser automation.

## Commands

Detail page or id:

```bash
python scripts/haowallpaper_direct.py detail https://haowallpaper.com/homeViewLook/18970557135113600
python scripts/haowallpaper_direct.py detail 18970557135113600 --download ./wallpapers
```

Keyword/tag search:

```bash
python scripts/haowallpaper_direct.py search "flower" --pages 3 --rows 30 --limit 20
python scripts/haowallpaper_direct.py search "flower" --sources home,mobile,forum --download ./wallpapers
python scripts/haowallpaper_direct.py search "flower" --sources mobile --media image
python scripts/haowallpaper_direct.py search "flower" --sources mobile --media video --download ./live-wallpapers
```

JSON output for downstream scripts:

```bash
python scripts/haowallpaper_direct.py search "flower" --sources all --format json
```

Search sources:

- `home`: desktop wallpapers from `/homeView`
- `mobile`: phone wallpapers from `/mobileView`
- `forum`: community-shared embedded wallpaper links from `/wallpaperForum`
- `all`: shorthand for `home,mobile,forum`

Use `--hydrate-detail` when search cards lack enough fields, especially mobile or forum results. It visits each detail page to fill title, tags, category, size, counts, and publish time.

Use `--media image`, `--media video`, or `--media all` to control whether static images, dynamic wallpapers/videos, or both are returned.

## What The Script Extracts

- Detail id, file id, title, canonical URL, public image URL, preview/cropping URLs
- Search source and detail type (`homeViewLook` or `mobileViewLook`)
- Static `image_url` and dynamic `video_url` when present
- Tags from `keywords` and card labels
- Category, resolution, color, size, publisher, publish time when available
- Download and favorite counts from SSR page/card HTML
- Local download paths when `--download DIR` is provided

## Notes

- Prefer `image_url` / `preview_url` from `og:image`, `twitter:image`, or JSON-LD `contentUrl`; these are public URLs present in page source.
- Do not use browser automation unless the static HTML no longer contains the needed data.
- Do not probe protected endpoints such as `getCompleteUrl` with fabricated tokens. If the user explicitly provides a legitimate cookie/token and asks for authenticated downloads, treat that as a separate authenticated scraping task.
