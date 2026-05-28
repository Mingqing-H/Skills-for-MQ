#!/usr/bin/env python3
"""Generate images via ModelScope API."""

import requests
import time
import json
import sys
import os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")

DEFAULT_MODEL = "Tongyi-MAI/Z-Image-Turbo"
BASE_URL = "https://api-inference.modelscope.cn/"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"ERROR: config.json not found at {CONFIG_PATH}")
        print('Create it with: {"api_key": "your-modelscope-token"}')
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    if not config.get("api_key"):
        print("ERROR: api_key is empty in config.json")
        sys.exit(1)
    return config


def generate(prompt, output="result.jpg", model=None, width=None, height=None):
    config = load_config()
    api_key = config["api_key"]
    model = model or config.get("default_model", DEFAULT_MODEL)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-ModelScope-Async-Mode": "true",
    }

    body = {"model": model, "prompt": prompt}
    if width:
        body["width"] = width
    if height:
        body["height"] = height

    print(f"Submitting: \"{prompt}\" (model: {model})")
    resp = requests.post(
        f"{BASE_URL}v1/images/generations",
        headers=headers,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
    )
    resp.raise_for_status()
    task_id = resp.json()["task_id"]
    print(f"Task ID: {task_id}")

    poll_headers = {
        "Authorization": f"Bearer {api_key}",
        "X-ModelScope-Task-Type": "image_generation",
    }

    while True:
        result = requests.get(
            f"{BASE_URL}v1/tasks/{task_id}", headers=poll_headers
        )
        result.raise_for_status()
        data = result.json()
        status = data["task_status"]

        if status == "SUCCEED":
            img_url = data["output_images"][0]
            img_data = requests.get(img_url).content
            with open(output, "wb") as f:
                f.write(img_data)
            print(f"Saved: {output}")
            return output
        elif status == "FAILED":
            print(f"FAILED: {data.get('error', 'unknown error')}")
            sys.exit(1)

        time.sleep(5)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate images via ModelScope")
    parser.add_argument("prompt", help="Image description")
    parser.add_argument("-o", "--output", default="result.jpg", help="Output file path")
    parser.add_argument("-m", "--model", default=None, help=f"Model ID (default: {DEFAULT_MODEL})")
    parser.add_argument("-W", "--width", type=int, default=None, help="Image width")
    parser.add_argument("-H", "--height", type=int, default=None, help="Image height")
    args = parser.parse_args()

    generate(args.prompt, args.output, args.model, args.width, args.height)
