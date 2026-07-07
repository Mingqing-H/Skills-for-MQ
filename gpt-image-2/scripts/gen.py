#!/usr/bin/env python3
"""Generate images through Codex CLI's imagegen tool.

This cross-platform entrypoint mirrors gen.sh but avoids Unix-only tools and
the Windows PowerShell codex.ps1 execution-policy trap.
"""

from __future__ import annotations

import argparse
import base64
import os
import pathlib
import shutil
import subprocess
import sys
from datetime import datetime

sys.dont_write_bytecode = True

from extract_image import find_image_blobs, validate_output_path


EXIT_BAD_ARGS = 2
EXIT_MISSING_COMMAND = 3
EXIT_REF_NOT_FOUND = 4
EXIT_CODEX_FAILED = 5
EXIT_NO_SESSION = 6
EXIT_NO_IMAGE = 7


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate or edit images through Codex CLI imagegen."
    )
    parser.add_argument("--prompt", help="Raw user image prompt.")
    parser.add_argument(
        "--prompt-file",
        help="Path to a UTF-8 encoded text file containing the prompt.",
    )
    parser.add_argument(
        "--out",
        help=(
            "Output image path. With --count > 1, use {index} or a printf-style "
            "integer placeholder, or the script appends -001, -002, ..."
        ),
    )
    parser.add_argument(
        "--out-dir",
        help="Directory for batch outputs. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of images to generate. Defaults to 1.",
    )
    parser.add_argument(
        "--ref",
        action="append",
        default=[],
        help="Reference image path. Repeat for multiple references.",
    )
    parser.add_argument("--timeout-sec", type=int, default=300)
    parser.add_argument(
        "--keep-session",
        action="store_true",
        help="Keep the Codex session rollout files created by this run.",
    )
    return parser.parse_args(argv)


def validate_count(count: int) -> int:
    if count < 1:
        raise ValueError("--count must be 1 or greater")
    return count


def resolve_output_dir(raw_out_dir: str | None) -> pathlib.Path:
    if raw_out_dir:
        return pathlib.Path(raw_out_dir).expanduser().resolve()
    return pathlib.Path.cwd().resolve()


def has_index_placeholder(template: str) -> bool:
    return "{index" in template or "%" in pathlib.Path(template).name


def format_indexed_template(template: str, index: int) -> str:
    if "{index" in template:
        return template.format(index=index)
    if "%" in pathlib.Path(template).name:
        try:
            return template % index
        except TypeError as err:
            raise ValueError(f"invalid printf-style --out template: {template}") from err

    candidate = pathlib.Path(template)
    return str(candidate.with_name(f"{candidate.stem}-{index:03d}{candidate.suffix}"))


def resolve_output_paths(
    raw_out: str | None,
    raw_out_dir: str | None,
    count: int,
) -> list[pathlib.Path]:
    if count == 1:
        if raw_out:
            return [validate_output_path(raw_out)]
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_dir = resolve_output_dir(raw_out_dir)
        return [validate_output_path(str(out_dir / f"image-{stamp}.png"))]

    out_dir = resolve_output_dir(raw_out_dir)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    if raw_out:
        raw_template = pathlib.Path(raw_out)
        if raw_template.is_absolute():
            template = str(raw_template)
        else:
            template = str(out_dir / raw_template)
        paths = [validate_output_path(format_indexed_template(template, index)) for index in range(1, count + 1)]
    else:
        paths = [validate_output_path(str(out_dir / f"image-{stamp}-{index:03d}.png")) for index in range(1, count + 1)]

    if len({path.resolve() for path in paths}) != len(paths):
        raise ValueError("batch output paths must be unique")
    return paths


def find_codex_command() -> list[str] | None:
    """Return a subprocess argv prefix for codex, preferring Windows .cmd."""
    if os.name == "nt":
        for name in ("codex.cmd", "codex.exe", "codex.bat"):
            found = shutil.which(name)
            if found:
                suffix = pathlib.Path(found).suffix.lower()
                if suffix in {".cmd", ".bat"}:
                    comspec = os.environ.get("ComSpec") or "cmd.exe"
                    return [comspec, "/d", "/c", found]
                return [found]

    found = shutil.which("codex")
    if found:
        return [found]
    return None


def snapshot_sessions(sessions_root: pathlib.Path) -> set[pathlib.Path]:
    if not sessions_root.exists():
        return set()
    return {
        path.resolve()
        for path in sessions_root.rglob("rollout-*.jsonl")
        if path.is_file()
    }


def get_sessions_root() -> pathlib.Path:
    raw_codex_home = os.environ.get("CODEX_HOME")
    if raw_codex_home:
        codex_home = pathlib.Path(os.path.expandvars(raw_codex_home)).expanduser()
    else:
        codex_home = pathlib.Path.home() / ".codex"
    return codex_home / "sessions"


def cleanup_sessions(session_paths: list[pathlib.Path], sessions_root: pathlib.Path) -> None:
    root = sessions_root.resolve()
    for session_path in session_paths:
        resolved = session_path.resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            print(f"skipping cleanup outside sessions root: {resolved}", file=sys.stderr)
            continue

        try:
            resolved.unlink(missing_ok=True)
        except OSError as err:
            print(f"warning: failed to remove session file {resolved}: {err}", file=sys.stderr)
            continue

        parent = resolved.parent
        while parent != root and root in parent.parents:
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent


def build_instruction(prompt: str, refs: list[pathlib.Path], image_number: int, total: int) -> str:
    instruction = "Use the imagegen tool to generate one image for the following request."
    if refs:
        instruction += " Use the attached image(s) as visual reference / input for image-to-image."
    if total > 1:
        instruction += f" This is image {image_number} of {total}; make it a distinct variation while preserving the user's request."
    instruction += (
        "\nRequirements: generate the image directly, return only the image, no explanation."
        "\n\nRequest:\n"
        + prompt
    )
    return instruction


def tail(text: str, lines: int = 30) -> str:
    return "\n".join(text.splitlines()[-lines:])


def run_codex(
    codex_prefix: list[str],
    instruction: str,
    refs: list[pathlib.Path],
    timeout_sec: int,
) -> subprocess.CompletedProcess[str]:
    args = [
        *codex_prefix,
        "exec",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--color",
        "never",
        "--enable",
        "image_generation",
    ]
    for ref in refs:
        args.extend(["-i", str(ref)])

    return subprocess.run(
        args,
        input=instruction,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout_sec,
        check=False,
    )


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        prompt_path = pathlib.Path(args.prompt_file).expanduser().resolve()
        if not prompt_path.is_file():
            raise ValueError(f"prompt file not found: {prompt_path}")
        return prompt_path.read_text(encoding="utf-8").strip()
    if args.prompt:
        return args.prompt
    raise ValueError("either --prompt or --prompt-file is required")


def write_images(blobs: list[tuple[str, str]], output_paths: list[pathlib.Path], start_index: int) -> int:
    written = 0
    for blob, _ext in blobs:
        if start_index + written >= len(output_paths):
            break
        out_path = output_paths[start_index + written]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(base64.b64decode(blob))
        print(out_path)
        written += 1
    return written


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        prompt = read_prompt(args)
        count = validate_count(args.count)
        output_paths = resolve_output_paths(args.out, args.out_dir, count)
    except (SystemExit, ValueError) as err:
        if isinstance(err, ValueError):
            print(f"invalid arguments: {err}", file=sys.stderr)
            return EXIT_BAD_ARGS
        raise

    refs = [pathlib.Path(raw).expanduser().resolve() for raw in args.ref]
    missing_refs = [str(ref) for ref in refs if not ref.is_file()]
    if missing_refs:
        print(f"reference image not found: {missing_refs[0]}", file=sys.stderr)
        return EXIT_REF_NOT_FOUND

    codex_prefix = find_codex_command()
    if codex_prefix is None:
        print("codex CLI not found. Install Codex CLI and run 'codex login' first.", file=sys.stderr)
        return EXIT_MISSING_COMMAND

    sessions_root = get_sessions_root()
    sessions_root.mkdir(parents=True, exist_ok=True)
    written = 0

    while written < count:
        before = snapshot_sessions(sessions_root)
        instruction = build_instruction(prompt, refs, written + 1, count)
        try:
            proc = run_codex(codex_prefix, instruction, refs, args.timeout_sec)
        except subprocess.TimeoutExpired:
            print(f"codex exec timed out after {args.timeout_sec} seconds", file=sys.stderr)
            if not args.keep_session:
                cleanup_sessions(sorted(snapshot_sessions(sessions_root) - before), sessions_root)
            return EXIT_CODEX_FAILED

        after = snapshot_sessions(sessions_root)
        new_sessions = sorted(after - before)

        if proc.returncode != 0:
            print(f"codex exec failed (exit={proc.returncode}). stderr tail:", file=sys.stderr)
            print(tail(proc.stderr), file=sys.stderr)
            if not args.keep_session:
                cleanup_sessions(new_sessions, sessions_root)
            return EXIT_CODEX_FAILED

        if not new_sessions:
            print(f"no new session rollout file under {sessions_root}", file=sys.stderr)
            if proc.stderr:
                print(tail(proc.stderr), file=sys.stderr)
            return EXIT_NO_SESSION

        blobs = find_image_blobs(new_sessions)
        if not blobs:
            print("image payload not found in any new session file", file=sys.stderr)
            if proc.stderr:
                print(tail(proc.stderr), file=sys.stderr)
            if not args.keep_session:
                cleanup_sessions(new_sessions, sessions_root)
            return EXIT_NO_IMAGE

        written += write_images(blobs, output_paths, written)
        if not args.keep_session:
            cleanup_sessions(new_sessions, sessions_root)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
