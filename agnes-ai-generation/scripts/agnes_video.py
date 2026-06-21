#!/usr/bin/env python3
"""Generate videos with Agnes AI and download completed results.

No third-party dependencies are required.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import time
from typing import Any
from urllib import error, parse, request


CREATE_URL = "https://apihub.agnes-ai.com/v1/videos"
QUERY_BY_VIDEO_ID = "https://apihub.agnes-ai.com/agnesapi"
LEGACY_QUERY_BASE = "https://apihub.agnes-ai.com/v1/videos"
DEFAULT_MODEL = "agnes-video-v2.0"


class AgnesHTTPError(RuntimeError):
    def __init__(self, status: int, body: str):
        super().__init__(f"HTTP {status}: {body[:500]}")
        self.status = status
        self.body = body


def now_stamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def is_url(value: str) -> bool:
    return parse.urlparse(value).scheme.lower() in {"http", "https"}


def extract_source_url_from_sidecar(path: Path) -> str | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    media = data.get("media")
    if isinstance(media, dict) and is_url(str(media.get("source_url", ""))):
        return str(media["source_url"])
    response = data.get("response")
    if isinstance(response, dict):
        items = response.get("data")
        if isinstance(items, list) and items and isinstance(items[0], dict):
            url = items[0].get("url")
            if is_url(str(url)):
                return str(url)
    return None


def normalize_image_input(value: str, allow_data_uri: bool) -> str:
    if is_url(value):
        return value
    if value.startswith("data:"):
        if allow_data_uri:
            return value
        raise ValueError(
            "Agnes video docs only guarantee public image URLs. Data URI input is disabled by default; "
            "use --allow-data-uri-image only for experimental testing."
        )
    path = Path(value).expanduser().resolve()
    if path.suffix.lower() == ".json":
        source_url = extract_source_url_from_sidecar(path)
        if source_url:
            return source_url
    if path.exists():
        raise ValueError(
            "Agnes image-to-video requires a public HTTPS image URL. Local image files cannot be uploaded by this script. "
            "Provide a public URL. As a compatibility shortcut, you may also pass a JSON sidecar from a prior Agnes image generation if it contains a source URL."
        )
    raise FileNotFoundError(f"Input image not found or not a URL: {path}")


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
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise AgnesHTTPError(exc.code, body) from exc


def get_json(url: str, api_key: str, timeout: int) -> dict[str, Any]:
    req = request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise AgnesHTTPError(exc.code, body) from exc


def get_bytes(url: str, timeout: int) -> tuple[bytes, str | None]:
    req = request.Request(url, headers={"User-Agent": "codex-agnes-ai-generation/1.0"})
    with request.urlopen(req, timeout=timeout) as resp:
        return resp.read(), resp.headers.get("Content-Type")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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

    return output_dir / f"agnes-video-{now_stamp()}"


def validate_num_frames(value: int) -> None:
    if value > 441:
        raise ValueError("num_frames must be <= 441.")
    if (value - 1) % 8 != 0:
        raise ValueError("num_frames must satisfy 8n + 1, for example 81, 121, 241, or 441.")


def build_payload(args: argparse.Namespace, images: list[str], image_location: str, include_auto_ti2vid: bool) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": args.model,
        "prompt": args.prompt,
        "height": args.height,
        "width": args.width,
        "num_frames": args.num_frames,
        "frame_rate": args.frame_rate,
    }
    if args.num_inference_steps is not None:
        payload["num_inference_steps"] = args.num_inference_steps
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.negative_prompt:
        payload["negative_prompt"] = args.negative_prompt
    if args.mode:
        payload["mode"] = args.mode
    elif images and not args.keyframes and include_auto_ti2vid:
        payload["mode"] = "ti2vid"

    extra_body: dict[str, Any] = {}
    if args.keyframes:
        extra_body["mode"] = "keyframes"
    if images:
        if image_location == "top":
            payload["image"] = images[0]
        else:
            extra_body["image"] = images
    if extra_body:
        payload["extra_body"] = extra_body
    return payload


def query_status(api_key: str, video_id: str | None, task_id: str | None, model: str, timeout: int, legacy: bool) -> dict[str, Any]:
    if not legacy and video_id:
        params = parse.urlencode({"video_id": video_id, "model_name": model})
        return get_json(f"{QUERY_BY_VIDEO_ID}?{params}", api_key, timeout)
    if task_id:
        return get_json(f"{LEGACY_QUERY_BASE}/{parse.quote(task_id)}", api_key, timeout)
    raise RuntimeError("No video_id or task_id available for querying.")


def download_video(video_url: str, output: Path, timeout: int) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    final_output = output if output.suffix else output.with_suffix(".mp4")
    media, _content_type = get_bytes(video_url, timeout=timeout)
    final_output.write_bytes(media)
    return final_output


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Use Agnes AI to generate videos."
    )
    parser.add_argument("--prompt", required=True, help="Video prompt.")
    parser.add_argument("--image", action="append", default=[], help="Input image path, URL, or Data URI. Can be repeated.")
    parser.add_argument("--keyframes", action="store_true", help="Use images as keyframes via extra_body.mode=keyframes.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Agnes video model. Default: {DEFAULT_MODEL}")
    parser.add_argument("--height", type=int, default=768, help="Requested video height.")
    parser.add_argument("--width", type=int, default=1152, help="Requested video width.")
    parser.add_argument("--num-frames", type=int, default=121, help="Frame count; must be <= 441 and 8n + 1.")
    parser.add_argument("--frame-rate", type=float, default=24, help="Frame rate, 1-60.")
    parser.add_argument("--num-inference-steps", type=int, help="Optional inference step count.")
    parser.add_argument("--seed", type=int, help="Optional seed for reproducibility.")
    parser.add_argument("--negative-prompt", help="Optional negative prompt.")
    parser.add_argument("--mode", help="Optional Agnes mode, e.g. ti2vid.")
    parser.add_argument("--force-extra-body-image", action="store_true", help="Place even a single image under extra_body.image.")
    parser.add_argument("--allow-data-uri-image", action="store_true", help="Allow experimental Data URI image input for video requests.")
    parser.add_argument("--no-fallback", action="store_true", help="Disable image-to-video request-structure fallback attempts.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned request payloads without calling Agnes.")
    parser.add_argument("--output", help="Output MP4 file path.")
    parser.add_argument("--output-dir", help="Output directory when --output is omitted. Defaults to the current project/workspace directory.")
    parser.add_argument("--write-json", "--metadata", dest="write_json", action="store_true", help="Write a JSON sidecar for reproducibility, polling history, and troubleshooting.")
    parser.add_argument("--api-key-env", default="AGNES_API_KEY", help="Environment variable containing the API key.")
    parser.add_argument("--api-key", help="API key value. Prefer --api-key-env for safety.")
    parser.add_argument("--request-timeout", type=int, default=60, help="HTTP timeout per request in seconds.")
    parser.add_argument("--poll-interval", type=int, default=5, help="Polling interval in seconds.")
    parser.add_argument("--max-wait", type=int, default=1800, help="Maximum polling time in seconds.")
    parser.add_argument("--no-wait", action="store_true", help="Create task and exit without polling.")
    parser.add_argument("--legacy-query", action="store_true", help="Query with /v1/videos/{task_id} instead of video_id.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    validate_num_frames(args.num_frames)
    if args.frame_rate < 1 or args.frame_rate > 60:
        raise ValueError("frame_rate must be between 1 and 60.")

    images = [normalize_image_input(value, args.allow_data_uri_image) for value in args.image]
    output_base = resolve_output_base(args)
    sidecar = output_base.with_suffix(".mp4.json") if args.write_json and not output_base.suffix else (output_base.with_suffix(output_base.suffix + ".json") if args.write_json else None)

    if args.keyframes and len(images) < 2:
        raise ValueError("Keyframe video requires at least two --image URLs.")

    attempts: list[dict[str, Any]] = []
    if not images:
        attempt_plan = [("none", False)]
    elif args.keyframes:
        attempt_plan = [("extra", False)]
    elif len(images) > 1:
        attempt_plan = [("extra", True), ("extra", False)]
    elif args.force_extra_body_image:
        attempt_plan = [("extra", True), ("extra", False)]
    else:
        attempt_plan = [("top", True), ("extra", True), ("top", False), ("extra", False)]
    if args.no_fallback:
        attempt_plan = attempt_plan[:1]

    if args.dry_run:
        planned = []
        for image_location, include_auto_ti2vid in attempt_plan:
            planned.append({
                "image_location": image_location,
                "include_auto_ti2vid": include_auto_ti2vid,
                "payload": build_payload(args, images, image_location, include_auto_ti2vid),
            })
        print(json.dumps({
            "ok": True,
            "dry_run": True,
            "endpoint": CREATE_URL,
            "attempts": planned,
        }, ensure_ascii=False, indent=2))
        return 0

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

    created: dict[str, Any] | None = None
    payload: dict[str, Any] = {}
    for attempt_index, (image_location, include_auto_ti2vid) in enumerate(attempt_plan):
        payload = build_payload(args, images, image_location, include_auto_ti2vid)
        attempt_record: dict[str, Any] = {
            "image_location": image_location,
            "include_auto_ti2vid": include_auto_ti2vid,
            "has_image": bool(images),
        }
        attempts.append(attempt_record)
        try:
            created = post_json(CREATE_URL, payload, api_key, args.request_timeout)
            attempt_record["ok"] = True
            break
        except AgnesHTTPError as exc:
            attempt_record.update({"ok": False, "status": exc.status, "error": exc.body[:1000]})
            if exc.status not in {400, 422, 500, 503} or attempt_index == len(attempt_plan) - 1:
                maybe_write_json(sidecar, {
                    "ok": False,
                    "type": "video",
                    "model": args.model,
                    "prompt": args.prompt,
                    "images": args.image,
                    "normalized_images": images,
                    "attempts": attempts,
                    "created_at": int(time.time()),
                })
                if sidecar is not None:
                    print(f"Agnes video task creation failed. Sidecar: {sidecar}", file=sys.stderr)
                else:
                    print("Agnes video task creation failed.", file=sys.stderr)
                return 1

    if created is None:
        raise RuntimeError("Agnes video task creation failed without a response.")
    task_id = created.get("task_id") or created.get("id")
    video_id = created.get("video_id")

    state: dict[str, Any] = {
        "ok": False,
        "type": "video",
        "model": args.model,
        "prompt": args.prompt,
        "images": args.image,
        "normalized_image_count": len(images),
        "normalized_images": images,
        "attempts": attempts,
        "payload": {k: v for k, v in payload.items() if k not in {"image", "extra_body"}},
        "task_id": task_id,
        "video_id": video_id,
        "create_response": created,
        "created_at": int(time.time()),
    }
    maybe_write_json(sidecar, state)

    if args.no_wait:
        response_payload = {
            "ok": True,
            "status": created.get("status"),
            "task_id": task_id,
            "video_id": video_id,
        }
        if sidecar is not None:
            response_payload["sidecar_path"] = str(sidecar)
        print(json.dumps(response_payload, ensure_ascii=False, indent=2))
        return 0

    deadline = time.time() + args.max_wait
    last_status = created
    while time.time() <= deadline:
        status_value = str(last_status.get("status", "")).lower()
        if status_value == "completed":
            video_url = last_status.get("remixed_from_video_id") or last_status.get("video_url") or last_status.get("url")
            if not video_url:
                raise RuntimeError("Video completed but no video URL field was present.")
            output_path = download_video(str(video_url), output_base, args.request_timeout)
            state.update({
                "ok": True,
                "status": "completed",
                "progress": last_status.get("progress"),
                "seconds": last_status.get("seconds"),
                "size": last_status.get("size"),
                "video_url": video_url,
                "output_path": str(output_path),
                "final_response": last_status,
                "completed_at": int(time.time()),
            })
            if sidecar is not None:
                state["sidecar_path"] = str(sidecar)
            maybe_write_json(sidecar, state)
            response_payload = {
                "ok": True,
                "output_path": str(output_path),
                "task_id": task_id,
                "video_id": video_id,
            }
            if sidecar is not None:
                response_payload["sidecar_path"] = str(sidecar)
            print(json.dumps(response_payload, ensure_ascii=False, indent=2))
            return 0
        if status_value == "failed":
            state.update({"ok": False, "status": "failed", "final_response": last_status, "failed_at": int(time.time())})
            maybe_write_json(sidecar, state)
            if sidecar is not None:
                print(f"Agnes video task failed. Sidecar: {sidecar}", file=sys.stderr)
            else:
                print("Agnes video task failed.", file=sys.stderr)
            return 1

        time.sleep(args.poll_interval)
        last_status = query_status(api_key, str(video_id) if video_id else None, str(task_id) if task_id else None, args.model, args.request_timeout, args.legacy_query)
        state.update({
            "status": last_status.get("status"),
            "progress": last_status.get("progress"),
            "last_response": last_status,
            "updated_at": int(time.time()),
        })
        maybe_write_json(sidecar, state)

    state.update({"ok": False, "status": last_status.get("status"), "progress": last_status.get("progress"), "timed_out_at": int(time.time()), "last_response": last_status})
    maybe_write_json(sidecar, state)
    response_payload = {
        "ok": False,
        "status": last_status.get("status"),
        "progress": last_status.get("progress"),
        "task_id": task_id,
        "video_id": video_id,
        "message": "Timed out while waiting for completion.",
    }
    if sidecar is not None:
        response_payload["sidecar_path"] = str(sidecar)
    print(json.dumps(response_payload, ensure_ascii=False, indent=2), file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)





