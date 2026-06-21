#!/usr/bin/env python3
"""Render a Markdown article into a WeChat-friendly HTML file.

This is a fallback renderer for environments without a dedicated layout skill.
It intentionally supports a conservative Markdown subset used by this project.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


STYLE = """
<style>
  body { margin: 0; background: #f5f7f6; }
  .wx-article { max-width: 760px; margin: 0 auto; padding: 36px 18px 48px; background: #fffdf9; color: #263238; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif; font-size: 16px; line-height: 1.9; }
  .wx-inner { max-width: 660px; margin: 0 auto; }
  h1 { margin: 0 0 28px; padding: 22px 18px; border-radius: 12px; background: linear-gradient(135deg, #eaf5f3, #fff6ed); color: #102023; font-size: 28px; line-height: 1.35; font-weight: 800; }
  h2 { margin: 42px 0 18px; padding: 9px 12px 9px 16px; border-left: 5px solid #2f6f73; border-radius: 0 10px 10px 0; background: linear-gradient(90deg, rgba(47,111,115,.12), rgba(47,111,115,0)); color: #13272a; font-size: 21px; line-height: 1.45; }
  p { margin: 0 0 18px; text-align: justify; word-break: break-word; }
  blockquote { margin: 28px 0; padding: 18px 20px; border-left: 5px solid #d86b35; border-radius: 10px; background: #fff8ef; color: #172326; font-weight: 650; }
  .img-slot { margin: 30px 0 26px; padding: 10px; border-radius: 12px; background: #f7fbfa; border: 1px solid #e3ecea; }
  .img-box { min-height: 180px; display: flex; align-items: center; justify-content: center; border: 1px dashed #8fb3b4; border-radius: 10px; color: #557074; font-weight: 650; background: #f0f6f5; }
  .img-hint, .caption { margin: 8px 0 20px; color: #75808a; font-size: 13px; line-height: 1.65; text-align: center; }
  .table-wrap { margin: 26px 0 28px; overflow-x: auto; border: 1px solid #e7edf3; border-radius: 12px; }
  table { width: 100%; border-collapse: collapse; font-size: 14px; line-height: 1.65; background: #fff; }
  th { background: #e9f5f3; color: #17373b; font-weight: 760; }
  th, td { padding: 12px 14px; border-bottom: 1px solid #edf1f4; text-align: left; vertical-align: top; }
  tr:last-child td { border-bottom: none; }
  .bullet { margin: 0 0 12px; padding: 10px 12px; border-radius: 8px; background: #f8fafb; font-size: 14px; text-align: left; }
  hr { border: none; height: 1px; margin: 42px 0 26px; background: linear-gradient(90deg, transparent, #d8e4e5, transparent); }
</style>
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def flush_table(rows: list[str], out: list[str]) -> None:
    if not rows:
        return
    out.append('<section class="table-wrap"><table>')
    for i, row in enumerate(rows):
        if i == 1 and re.match(r"^\|\s*-", row):
            continue
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        tag = "th" if i == 0 else "td"
        out.append("<tr>" + "".join(f"<{tag}>{esc(c)}</{tag}>" for c in cells) + "</tr>")
    out.append("</table></section>")


def render(markdown: str) -> str:
    out: list[str] = []
    table_rows: list[str] = []
    for raw in markdown.splitlines():
        line = raw.strip()
        if re.match(r"^\|.*\|$", line):
            table_rows.append(line)
            continue
        flush_table(table_rows, out)
        table_rows = []
        if not line:
            continue
        if line.startswith("# "):
            out.append(f"<h1>{esc(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            out.append(f"<h2>{esc(line[3:].strip())}</h2>")
        elif re.match(r"^-{3,}$", line):
            out.append("<hr />")
        elif m := re.match(r"^!\[(.*?)\]\((.*?)\)$", line):
            alt = esc(m.group(1))
            path = esc(m.group(2))
            out.append(f'<section class="img-slot" data-src="{path}"><div class="img-box">插图位置</div><div class="img-hint">{alt}</div></section>')
        elif line.startswith("- "):
            out.append(f'<p class="bullet">• {esc(line[2:].strip())}</p>')
        elif line.startswith("> "):
            out.append(f"<blockquote>{esc(line[2:].strip())}</blockquote>")
        elif re.match(r"^(图\s*\d+：|来源：|题图标题：|创作者：)", line):
            out.append(f'<p class="caption">{esc(line)}</p>')
        else:
            out.append(f"<p>{esc(line)}</p>")
    flush_table(table_rows, out)
    return '<section class="wx-article">\n<section class="wx-inner">\n' + "\n".join(out) + "\n</section>\n</section>"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render project Markdown to WeChat-friendly HTML.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--fragment", action="store_true", help="Write HTML fragment without full document wrapper.")
    args = parser.parse_args()

    markdown = args.input.read_text(encoding="utf-8")
    fragment = STYLE + "\n" + render(markdown)
    if args.fragment:
        html_text = fragment
    else:
        html_text = '<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8" />\n<meta name="viewport" content="width=device-width, initial-scale=1" />\n' + STYLE + "\n</head>\n<body>\n" + render(markdown) + "\n</body>\n</html>\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
