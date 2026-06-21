#!/usr/bin/env python3
"""Help users configure AGNES_API_KEY safely."""

from __future__ import annotations

import argparse
import getpass
import os
from pathlib import Path
import platform
import stat
import sys


ENV_NAME = "AGNES_API_KEY"


def mask_key(value: str | None) -> str:
    if not value:
        return "<missing>"
    if len(value) <= 8:
        return value[:2] + "..." + value[-2:]
    return value[:4] + "..." + value[-4:]


def print_guide() -> None:
    print(
        """Agnes API key setup / Agnes API Key 配置

Get a key / 获取 Key:
1. Open https://agnes-ai.com/ and sign in or create an account.
2. Open the developer console or platform dashboard.
3. Go to Settings -> API Keys -> Create new secret key.
4. Copy the key and keep it private.

Docs / 文档:
- https://agnes-ai.com/doc
- https://agnes-ai.com/doc/quick-start

Temporary use / 临时使用:
  python scripts/agnes_image.py --api-key "YOUR_KEY" --prompt "..."

Persistent user-level setup / 持续使用:
  python scripts/agnes_key.py --set-user --stdin

Check / 检查:
  python scripts/agnes_key.py --check
"""
    )


def set_windows_user_env(name: str, value: str) -> None:
    import winreg

    key_path = r"Environment"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)


def choose_unix_profile() -> Path:
    shell = Path(os.environ.get("SHELL", "")).name
    home = Path.home()
    if shell == "zsh":
        return home / ".zshrc"
    if shell == "bash":
        return home / ".bashrc"
    return home / ".profile"


def shell_quote_single(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def set_unix_user_env(name: str, value: str, profile_path: Path | None) -> Path:
    profile = profile_path or choose_unix_profile()
    profile.parent.mkdir(parents=True, exist_ok=True)
    line = f"\nexport {name}={shell_quote_single(value)}\n"
    with profile.open("a", encoding="utf-8") as handle:
        handle.write(line)
    try:
        current_mode = profile.stat().st_mode
        profile.chmod(current_mode & ~(stat.S_IRWXG | stat.S_IRWXO))
    except OSError:
        pass
    return profile


def read_key(args: argparse.Namespace) -> str:
    if args.value:
        return args.value.strip()
    if args.stdin:
        return sys.stdin.read().strip()
    return getpass.getpass("Agnes API key: ").strip()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Configure AGNES_API_KEY for Agnes AI. 配置 Agnes AI 的 AGNES_API_KEY。"
    )
    parser.add_argument("--guide", action="store_true", help="Print setup instructions.")
    parser.add_argument("--check", action="store_true", help="Check whether AGNES_API_KEY is set.")
    parser.add_argument("--set-user", action="store_true", help="Persist AGNES_API_KEY at user level.")
    parser.add_argument("--value", help="API key value. Prefer --stdin to avoid command history.")
    parser.add_argument("--stdin", action="store_true", help="Read API key from stdin.")
    parser.add_argument("--profile", help="Unix shell profile path for --set-user.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.guide or (not args.check and not args.set_user):
        print_guide()
        return 0

    if args.check:
        value = os.environ.get(ENV_NAME)
        if value:
            print(f"{ENV_NAME} is set / 已配置: {mask_key(value)}")
            return 0
        print(f"{ENV_NAME} is not set / 尚未配置")
        return 1

    if args.set_user:
        value = read_key(args)
        if not value:
            print("No API key provided. 未提供 API Key。", file=sys.stderr)
            return 2
        system = platform.system().lower()
        if system == "windows":
            set_windows_user_env(ENV_NAME, value)
            print(f"Stored user environment variable {ENV_NAME}: {mask_key(value)}")
            print("Open a new terminal for the value to appear in the environment.")
        else:
            profile = set_unix_user_env(ENV_NAME, value, Path(args.profile).expanduser() if args.profile else None)
            print(f"Appended {ENV_NAME} to {profile}: {mask_key(value)}")
            print("Open a new terminal or source the profile for the value to appear.")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
