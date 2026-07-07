#!/usr/bin/env python3
"""Create a poster-template scaffold in the skill's references directory."""
from __future__ import annotations
import argparse
import re
from pathlib import Path

ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, dest="template_id")
    parser.add_argument("--name", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if not ID_PATTERN.fullmatch(args.template_id):
        parser.error("--id must use lowercase letters, digits, and hyphens")
    skill_dir = Path(__file__).resolve().parent.parent
    output_dir = args.output_dir or skill_dir / "references"
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / f"template-{args.template_id}.md"
    if target.exists():
        parser.error(f"template already exists: {target}")
    content = f"""---
id: {args.template_id}
name: {args.name}
family: {args.family}
version: 1.0.0
---

# {args.name}

## 适用场景

[列出至少三个可复用场景]

## 必填变量

`{{{{主题}}}}`、`{{{{主标题}}}}`、`{{{{画幅}}}}`

## 设计机制

- [描述第一视觉和阅读顺序]
- [描述图文空间关系]
- [描述系列化不变量]

## 提示词骨架

```text
设计一张{{{{画幅}}}}的海报，主题为{{{{主题}}}}。

[构图、主体、图文、色彩、光线、材质和限制]

避免：[最可能出现的具体失败]
```

## 质量检查

- [检查视觉论点]
- [检查信息层级]
- [检查物理与文字准确性]
"""
    target.write_text(content, encoding="utf-8")
    print(target)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())