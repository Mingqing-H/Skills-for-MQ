---
name: gpt-image-2
description: Generate and edit images with GPT Image 2 through the user's local Codex CLI and ChatGPT subscription. Use when the user explicitly asks for GPT Image 2, gpt-image-2, ChatGPT Images 2.0, Image 2, or asks to generate/edit/restyle/compose images through their ChatGPT plan. Supports text-to-image, image-to-image editing, style transfer, and multiple reference images.
---

# GPT Image 2

Generate images with GPT Image 2 through the local `codex` CLI, reusing the user's existing ChatGPT Plus or Pro subscription. This skill is a local wrapper; it does not provide OpenAI API credentials or image access by itself. It supports single-image generation and batch generation via repeated Codex CLI calls.

## Triggering

Use this skill only when the user explicitly asks for this route, such as:

- "use GPT Image 2"
- "use gpt-image-2"
- "use ChatGPT Images 2.0"
- "use Image 2"
- "generate this through my ChatGPT plan"
- "edit/restyle this reference image with GPT Image 2"

Do not auto-trigger for a plain image-generation request unless the user names GPT Image 2, Image 2, ChatGPT Images 2.0, or their ChatGPT subscription/Codex CLI route. If the user specified this skill, do not silently substitute another image model or an HTML/screenshot mockup.

## Prerequisites

- A working local `codex` CLI login with a ChatGPT plan that includes Image 2 access.
- Python 3.10 or newer on PATH. On Windows, use `python`; on macOS/Linux, `python3` or `python`.
- Network access for the `codex` CLI call to OpenAI.

On Windows, prefer `scripts/gen.py`; it avoids the common PowerShell execution-policy failure where `codex` resolves to `codex.ps1` instead of `codex.cmd`.

## How To Invoke

Prefer the cross-platform Python entrypoint:

```bash
python scripts/gen.py --prompt "<user's raw prompt>" --out "<absolute/path/to/output.png>"
```

For batch generation, use `--count`. The script prints one output path per generated image:

```bash
python scripts/gen.py --prompt "<user's raw prompt>" --count 4 --out-dir "/absolute/path/to/outputs"
```

You can also provide an indexed output template:

```bash
python scripts/gen.py --prompt "<user's raw prompt>" --count 4 --out "/absolute/path/to/image-{index:02d}.png"
```

For image-to-image, repeat `--ref` for each reference image:

```bash
python scripts/gen.py \
  --prompt "<user's raw prompt, for example: repaint in watercolor>" \
  --ref "/absolute/path/to/reference.png" \
  --out "/absolute/path/to/output.png"
```

On Unix-like shells, `scripts/gen.sh` remains available as a thin wrapper around `gen.py`:

```bash
bash scripts/gen.sh --prompt "<user's raw prompt>" --out "/absolute/path/to/output.png"
```

Optional flags:

- `--count 1` (default: 1) generates one or more images. Counts above 1 are run serially to avoid Codex session rollout races.
- `--out-dir <directory>` writes default batch names into a directory.
- `--out <path-or-template>` can include `{index}` formatting, such as `image-{index:02d}.png`; without a placeholder, batch mode appends `-001`, `-002`, etc.
- `--timeout-sec 300` (default: 300).
- `--keep-session` keeps the temporary Codex session rollout files for debugging. By default, the script deletes rollout files created by its own run before exiting.

## Default Behavior

- Pass the user's prompt through raw. Do not translate, polish, or add style modifiers unless the user asks.
- If the user does not specify an output path, choose `image-<YYYYMMDD-HHMMSS>.png` for one image, or `image-<YYYYMMDD-HHMMSS>-001.png`, `-002.png`, etc. for batch output.
- After successful generation, display or attach the output image(s). Do not stop at only reporting paths.
- Text-heavy layouts are acceptable. Do not warn just because the prompt includes text.

## Hard Constraints

- Do not switch routes without permission. If the user asked for GPT Image 2, do not substitute DALL-E, Midjourney, another hosted image model, or a manual browser screenshot workflow.
- Do not rewrite the prompt unless asked.
- Do not imply this skill works without a local `codex` login and a valid ChatGPT subscription with image-generation entitlement.
- Do not use `codex exec --ephemeral`; the script needs the persisted session rollout to extract the generated image payload.

## Exit Codes

| Code | Meaning |
| ---- | ------- |
| 0 | Success; one output path per generated image printed on stdout. |
| 2 | Bad arguments or invalid output path. |
| 3 | Required local command missing, usually `codex` or Python. |
| 4 | A `--ref` image does not exist. |
| 5 | `codex exec` failed or timed out. |
| 6 | No new Codex session rollout file was detected. |
| 7 | No image payload was found in the new session rollout files. |

On failure, summarize the failed layer in one sentence for the user instead of dumping full stderr.

## How It Works

The script:

1. Snapshots `$CODEX_HOME/sessions/`, or `~/.codex/sessions/` when `CODEX_HOME` is unset.
2. Runs `codex exec --enable image_generation --sandbox read-only` and sends the image request through stdin.
3. Adds `-i <file>` for each reference image.
4. Diffs the session directory after the run.
5. Scans every new `rollout-*.jsonl` file for base64 PNG, JPEG, or WebP image payloads.
6. Writes matching image payloads to the requested output path(s), largest first when multiple payloads appear in a rollout.
7. For `--count > 1`, repeats the Codex call serially until the requested number of images has been written.
8. Deletes the new rollout files created by each run before exiting, unless `--keep-session` is set.

The important CLI details are:

- `--enable image_generation` is required because image generation may be feature-gated in the CLI.
- `--ephemeral` must not be used because ephemeral sessions are not persisted.

## Data Handling

- The script reads only new session rollout files created after its own `codex exec` invocation.
- It writes only the requested output image(s).
- Runs delete their own newly created rollout files by default, including most failure paths. Pass `--keep-session` when the session is needed for debugging.
- It does not request credentials or call any service directly. The outbound request is made by the local `codex` CLI using the user's existing login.

