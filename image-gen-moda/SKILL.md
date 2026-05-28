---
name: image-gen-moda
description: "Generate images from text prompts using ModelScope API. Use when the user asks to create, generate, draw, or produce an image, picture, illustration, or artwork from a text description. Supports two models: turbo (fast) and zimage (standard)."
---

# Image Generation

Generate images via ModelScope's text-to-image API.

## Prerequisites

`config.json` in this skill's directory stores the API token:

```json
{"api_key": "your-token-here"}
```

## Models

| Short Name | Full Model ID | Description |
|------------|---------------|-------------|
| turbo | Tongyi-MAI/Z-Image-Turbo | Faster generation |
| zimage | Tongyi-MAI/Z-Image | Standard quality |

## Workflow

1. **Ask user which model to use** (if not specified): present the two options as `turbo` and `zimage`.
2. Determine the user's prompt and any size preferences.
3. Run `scripts/generate.py` with appropriate arguments:

```bash
python scripts/generate.py "prompt text" -m <model_id> -o output.jpg
```

4. The script submits the task, polls for completion, and saves the image.
5. Show the saved image path to the user.

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o`, `--output` | Output file path | `result.jpg` |
| `-m`, `--model` | ModelScope model ID | Tongyi-MAI/Z-Image-Turbo |
| `-W`, `--width` | Image width | model default |
| `-H`, `--height` | Image height | model default |

### Examples

```bash
# turbo model
python scripts/generate.py "a futuristic city at sunset" -m Tongyi-MAI/Z-Image-Turbo

# zimage model with custom size
python scripts/generate.py "watercolor painting of mountains" -m Tongyi-MAI/Z-Image -o mountain.jpg -W 1024 -H 768
```

## Notes

- Generation is async — the script polls every 5 seconds until complete
- Output is always a local file; no external hosting
- The script reads `config.json` from the skill directory automatically
