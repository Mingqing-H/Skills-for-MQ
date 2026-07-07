#!/usr/bin/env python3
"""Validate poster template metadata and required sections."""
from __future__ import annotations
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ("id", "name", "family", "version")
REQUIRED_HEADINGS = ("## 适用场景", "## 必填变量", "## 设计机制", "## 提示词骨架", "## 质量检查")
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")

def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("\"'")
    return result

def main() -> int:
    skill_dir = Path(__file__).resolve().parent.parent
    paths = [p for p in sorted((skill_dir / "references").glob("template-*.md")) if p.name != "template-schema.md"]
    errors = []
    seen_ids = set()
    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    if not paths:
        errors.append("no template files found")
    for path in paths:
        if f"references/{path.name}" not in skill_text:
            errors.append(f"{path.name}: not linked directly from SKILL.md")
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text)
        for field in REQUIRED_FIELDS:
            if not metadata.get(field):
                errors.append(f"{path.name}: missing field '{field}'")
        template_id = metadata.get("id", "")
        expected_id = path.stem.removeprefix("template-")
        if template_id and not ID_PATTERN.fullmatch(template_id):
            errors.append(f"{path.name}: invalid id '{template_id}'")
        if template_id and template_id != expected_id:
            errors.append(f"{path.name}: id must match filename ('{expected_id}')")
        if template_id in seen_ids:
            errors.append(f"{path.name}: duplicate id '{template_id}'")
        seen_ids.add(template_id)
        version = metadata.get("version", "")
        if version and not VERSION_PATTERN.fullmatch(version):
            errors.append(f"{path.name}: version must be semantic x.y.z")
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                errors.append(f"{path.name}: missing heading '{heading}'")
        if "{{" not in text or "}}" not in text:
            errors.append(f"{path.name}: no template variables found")
    if errors:
        print("\n".join(f"ERROR: {e}" for e in errors), file=sys.stderr)
        return 1
    print(f"OK: validated {len(paths)} poster templates")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())