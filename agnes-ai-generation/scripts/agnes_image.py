#!/usr/bin/env python3
"""Generate or edit images with Agnes AI.

No third-party dependencies are required.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
from pathlib import Path
import sys
import time
from typing import Any
from urllib import error, parse, request


API_URL = "https://apihub.agnes-ai.com/v1/images/generations"
DEFAULT_MODEL = "agnes-image-2.1-flash"


class AgnesHTTPError(RuntimeError):
    def __init__(self, status: int, body: str):
        super().__init__(f"HTTP {status}: {body[:500]}")
        self.status = status
        self.body = body


def now_stamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def is_url(value: str) -> bool:
    scheme = parse.urlparse(value).scheme.lower()
    return scheme in {"http", "https"}


def is_data_uri(value: str) -> bool:
    return value.startswith("data:")


def local_image_to_data_uri(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Input image not found: {path}")
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def normalize_image_input(value: str) -> str:
    if is_url(value) or is_data_uri(value):
        return value
    return local_image_to_data_uri(Path(value).expanduser().resolve())


def post_json(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise AgnesHTTPError(exc.code, body) from exc


def get_bytes(url: str, timeout: int) -> tuple[bytes, str | None]:
    req = request.Request(url, headers={"User-Agent": "codex-agnes-ai-generation/1.0"})
    with request.urlopen(req, timeout=timeout) as resp:
        return resp.read(), resp.headers.get("Content-Type")


def extension_from_url_or_type(url: str | None, content_type: str | None) -> str:
    if content_type:
        ctype = content_type.split(";", 1)[0].strip().lower()
        ext = mimetypes.guess_extension(ctype)
        if ext:
            return ".jpg" if ext == ".jpe" else ext
    if url:
        suffix = Path(parse.urlparse(url).path).suffix
        if suffix:
            return suffix
    return ".png"


def decode_base64_image(value: str) -> bytes:
    if value.startswith("data:"):
        value = value.split(",", 1)[1]
    return base64.b64decode(value)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def maybe_write_json(path: Path | None, data: dict[str, Any]) -> None:
    if path is not None:
        write_json(path, data)


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def resolve_output_base(args: argparse.Namespace) -> Path:
    if args.output:
        return Path(args.output).expanduser().resolve()

    script_skill_root = Path(__file__).resolve().parents[1]
    cwd = Path.cwd().resolve()
    output_dir_value = args.output_dir or os.environ.get("AGNES_OUTPUT_DIR")

    if output_dir_value:
        output_dir = Path(output_dir_value).expanduser().resolve()
    else:
        if cwd == script_skill_root or is_relative_to(cwd, script_skill_root):
            raise RuntimeError(
                "Refusing to write default outputs inside the Agnes skill directory. "
                "Run this script from the user's project/workspace directory, or pass --output-dir with a project path."
            )
        output_dir = cwd

    return output_dir / f"agnes-image-{now_stamp()}"


def build_payload(args: argparse.Namespace, images: list[str], image_location: str) -> dict[str, Any]:
    extra_body: dict[str, Any] = {}
    if args.response_format:
        extra_body["response_format"] = args.response_format
    payload: dict[str, Any] = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
    }
    if args.response_format == "b64_json" and not images:
        payload["return_base64"] = True
    if images:
        if image_location == "top":
            payload["image"] = images
        else:
            extra_body["image"] = images
    if extra_body:
        payload["extra_body"] = extra_body
    return payload


def save_result(result: dict[str, Any], output: Path, timeout: int) -> tuple[Path, dict[str, Any]]:
    data = result.get("data")
    if not isinstance(data, list) or not data:
        raise RuntimeError("Agnes response did not include data[0].")
    item = data[0]
    if not isinstance(item, dict):
        raise RuntimeError("Agnes response data[0] was not an object.")

    url = item.get("url")
    b64_json = item.get("b64_json")

    output.parent.mkdir(parents=True, exist_ok=True)
    if url:
        media, content_type = get_bytes(str(url), timeout=timeout)
        if output.suffix:
            final_output = output
        else:
            final_output = output.with_suffix(extension_from_url_or_type(str(url), content_type))
        final_output.write_bytes(media)
        return final_output, {"source_url": url, "content_type": content_type}

    if b64_json:
        if output.suffix:
            final_output = output
        else:
            final_output = output.with_suffix(".png")
        final_output.write_bytes(decode_base64_image(str(b64_json)))
        return final_output, {"source_url": None, "content_type": "base64"}

    raise RuntimeError("Agnes response did not include data[0].url or data[0].b64_json.")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Use Agnes AI to generate or edit images."
    )
    parser.add_argument("--prompt", required=True, help="Image prompt or edit instruction.")
    parser.add_argument("--image", action="append", default=[], help="Input image path, URL, or Data URI. Can be repeated.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Agnes image model. Default: {DEFAULT_MODEL}")
    parser.add_argument("--size", default="1024x768", help="Output size, e.g. 1024x768, 1024x1024, 768x1024.")
    parser.add_argument("--response-format", choices=["url", "b64_json"], default="url", help="Agnes response format.")
    parser.add_argument("--output", help="Output image file path.")
    parser.add_argument("--output-dir", help="Output directory when --output is omitted. Defaults to the current project/workspace directory.")
    parser.add_argument("--write-json", "--metadata", dest="write_json", action="store_true", help="Write a JSON sidecar for reproducibility and troubleshooting.")
    parser.add_argument("--api-key-env", default="AGNES_API_KEY", help="Environment variable containing the API key.")
    parser.add_argument("--api-key", help="API key value. Prefer --api-key-env for safety.")
    parser.add_argument("--timeout", type=int, default=180, help="HTTP timeout in seconds.")
    parser.add_argument("--no-fallback", action="store_true", help="Disable image placement fallback.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    api_key = args.api_key or os.environ.get(args.api_key_env)
    if not api_key:
        print(
            f"Missing {args.api_key_env}.\n"
            "Get a key: https://agnes-ai.com/ -> Settings -> API Keys -> Create new secret key\n"
            "Temporary use: add --api-key YOUR_KEY\n"
            "Persistent setup: python scripts/agnes_key.py --set-user --stdin",
            file=sys.stderr,
        )
        return 2

    images = [normalize_image_input(value) for value in args.image]
    output_base = resolve_output_base(args)

    attempts: list[dict[str, Any]] = []
    locations = ["top"] if not images else ["top", "extra"]
    if args.no_fallback:
        locations = locations[:1]

    result: dict[str, Any] | None = None
    used_location = locations[0]
    last_error: AgnesHTTPError | None = None

    for location in locations:
        payload = build_payload(args, images, location)
        attempts.append({"image_location": location, "payload": {k: v for k, v in payload.items() if k != "image"}})
        try:
            result = post_json(API_URL, payload, api_key, args.timeout)
            used_location = location
            break
        except AgnesHTTPError as exc:
            last_error = exc
            if not images or exc.status not in {400, 422} or location == locations[-1]:
                sidecar = output_base.with_suffix(".json") if args.write_json else None
                if sidecar is not None:
                    sidecar.parent.mkdir(parents=True, exist_ok=True)
                maybe_write_json(sidecar, {
                    "ok": False,
                    "model": args.model,
                    "prompt": args.prompt,
                    "size": args.size,
                    "images": args.image,
                    "attempts": attempts,
                    "status": exc.status,
                    "error": exc.body,
                    "created_at": int(time.time()),
                })
                if sidecar is not None:
                    print(f"Agnes image request failed: HTTP {exc.status}. Sidecar: {sidecar}", file=sys.stderr)
                else:
                    print(f"Agnes image request failed: HTTP {exc.status}.", file=sys.stderr)
                return 1

    if result is None:
        assert last_error is not None
        raise last_error

    output_path, media_meta = save_result(result, output_base, args.timeout)
    response_payload = {
        "ok": True,
        "output_path": str(output_path),
        "image_location": used_location,
    }
    source_url = media_meta.get("source_url")
    if source_url:
        response_payload["source_url"] = str(source_url)
    if args.write_json:
        sidecar = output_path.with_suffix(output_path.suffix + ".json")
        write_json(sidecar, {
            "ok": True,
            "type": "image",
            "model": args.model,
            "prompt": args.prompt,
            "size": args.size,
            "images": args.image,
            "normalized_image_count": len(images),
            "response_format": args.response_format,
            "image_location": used_location,
            "output_path": str(output_path),
            "sidecar_path": str(sidecar),
            "media": media_meta,
            "response": result,
            "created_at": int(time.time()),
        })
        response_payload["sidecar_path"] = str(sidecar)

    print(json.dumps(response_payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)






