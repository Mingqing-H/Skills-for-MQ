---
name: agnes-ai-generation
description: Use only when the user explicitly asks to use Agnes, Agnes AI, or the Agnes API for generation or integration tasks. Supports Agnes-powered text-to-image, image-to-image, multi-image composition, text-to-video, image-to-video, keyframe video, prompt optimization, and adding Agnes API support to a project. Trigger phrases include use Agnes, call Agnes, Agnes API, Agnes text-to-image, Agnes image-to-image, Agnes video, 使用 Agnes, 调用 Agnes, Agnes 文生图, Agnes 图生图, and Agnes 视频. Do not use for generic image or video generation requests that do not mention Agnes.
---

# Agnes AI Generation

Use this skill only when the user explicitly mentions Agnes, Agnes AI, or Agnes API. Do not use it for generic image generation, image editing, or video generation requests unless the user specifically asks to use Agnes.

## Core Rules

- Prefer the bundled scripts over handwritten API calls for direct media generation.
- Use `AGNES_API_KEY` by default. If it is missing, read `references/api-key-setup.md` and guide the user to get or configure a key.
- If the user sends an Agnes API key in chat, offer two choices before configuring it: temporary use for this request, or persistent user-level configuration for future requests.
- For temporary use, pass the key directly to the generation script with `--api-key` only for the current command, and do not save it.
- For persistent setup, ask for explicit confirmation before writing a user-level environment variable, then use `scripts/agnes_key.py --set-user --stdin` or an equivalent OS command.
- Never write API keys into source files, committed config, screenshots, or public output.
- Never echo the full key back to the user; show only a masked form such as `sk-...abcd`.
- Run generation scripts with the user's active project/workspace as the working directory, or pass an absolute `--output-dir` inside that project.
- Never use the skill installation directory as the working directory for generation commands.
- Save generated media locally, then show local absolute paths in the final response.
- After successful image generation, display the saved local image with Markdown image syntax using an absolute path.
- After successful video generation, provide a Markdown link to the saved MP4 path; include the absolute path even if inline playback is not available.
- Do not create JSON sidecars by default. Add `--write-json` (alias: `--metadata`) only when the user asks for reproducibility metadata, troubleshooting detail, or follow-up reuse of an Agnes source URL.
- When chaining a newly generated Agnes image into image-to-video, reuse the source_url printed by gnes_image.py; do not regenerate the image just to obtain a JSON sidecar.

## Task Selection

- **Text-to-image, image-to-image, multi-image composition, image editing**: run `scripts/agnes_image.py`.
- **Text-to-video, image-to-video, multi-image video, keyframe animation**: run `scripts/agnes_video.py`.
- **Missing API key, key setup, or user sends a key**: read `references/api-key-setup.md`; optionally run `scripts/agnes_key.py --check` or `scripts/agnes_key.py --guide`.
- **Project integration or custom client code**: read `references/api-reference.md`.
- **Vague creative prompt or quality improvement request**: read `references/prompting-guide.md`.
- **API error, timeout, parameter mismatch, or RPM limit**: read `references/troubleshooting.md`.

## Image Workflow

Run from the user's project/workspace directory and pass the script path explicitly:

```bash
python path/to/agnes-ai-generation/scripts/agnes_image.py --prompt "A luminous floating city above a misty canyon at sunrise" --size 1024x768
```

For image-to-image:

```bash
python path/to/agnes-ai-generation/scripts/agnes_image.py --prompt "Make the object matte black while preserving the original composition" --image input.png --size 1024x768
```

For multi-image composition, pass `--image` multiple times:

```bash
python path/to/agnes-ai-generation/scripts/agnes_image.py --prompt "Place the person from the first image beside the robot from the second image" --image person.png --image robot.png
```

Defaults:

- Model: `agnes-image-2.1-flash`
- Output directory: the user's current project/workspace directory, unless `--output`, `--output-dir`, or `AGNES_OUTPUT_DIR` is set
- API key env var: `AGNES_API_KEY`
- Response format: `url`, then download locally

The script accepts local image paths, public URLs, and Data URI Base64 inputs. Local image paths are converted to Data URI Base64 automatically.

Use `--output ./name.png` when the user wants a specific file path. When Agnes returns a hosted image URL, the script also prints `source_url` in stdout so a follow-up image-to-video step can reuse it without writing JSON. Use `--write-json` only when metadata is useful; normal image generation should return just the image file.

## Video Workflow

Run:

```bash
python path/to/agnes-ai-generation/scripts/agnes_video.py --prompt "A cinematic shot of a cat walking on the beach at sunset" --num-frames 121 --frame-rate 24
```

For image-to-video:

```bash
python path/to/agnes-ai-generation/scripts/agnes_video.py --prompt "Animate the character with subtle breathing motion" --image https://example.com/input.png
```

For keyframes:

```bash
python path/to/agnes-ai-generation/scripts/agnes_video.py --prompt "Create a smooth transition between the two keyframes" --image https://example.com/start.png --image https://example.com/end.png --keyframes
```

Defaults:

- Model: `agnes-video-v2.0`
- Output directory: the user's current project/workspace directory, unless `--output`, `--output-dir`, or `AGNES_OUTPUT_DIR` is set
- Poll interval: 5 seconds
- Query mode: use `video_id`
- Recommended frame counts: `81`, `121`, `241`, `441`

The script validates `num_frames <= 441` and `num_frames = 8n + 1`.

For video image inputs, prefer public HTTPS image URLs. If the image was just generated by `agnes_image.py`, pass the `source_url` from that command output to `--image`; do not regenerate the image. Unlike image generation, Agnes video docs only guarantee image URL inputs, so local image files still need a public URL unless the API adds upload support. Passing a prior Agnes JSON sidecar remains supported as a compatibility shortcut when it contains a reusable source URL, but it is not required for image-to-video. Use `--dry-run` to inspect the planned image-to-video payload and fallback attempts without calling the API.

## Display Results

In the final response:

- For images, include `![Agnes generated image](/absolute/path/to/image.png)` and the saved path.
- For videos, include `[Agnes generated video](/absolute/path/to/video.mp4)` and the saved path.
- Mention the sidecar JSON path only if `--write-json` was used.
- If generation is still queued or in progress, report `status`, `progress`, and `video_id` instead of claiming completion. Include the sidecar path only if `--write-json` was used.

## References

- Read `references/api-key-setup.md` when the user needs to obtain, provide, temporarily use, or persist an Agnes API key.
- Read `references/api-reference.md` for exact endpoints, models, parameters, and response fields.
- Read `references/prompting-guide.md` for bilingual prompt templates and quality patterns.
- Read `references/troubleshooting.md` for known Agnes API failure modes and fallback behavior.




