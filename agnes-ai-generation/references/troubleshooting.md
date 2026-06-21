# Agnes Troubleshooting

Use this reference when an Agnes API call fails, times out, or returns an unexpected response.

## Common Errors

| Symptom | Likely cause | Action |
|---|---|---|
| Missing `AGNES_API_KEY` | No key configured | Read `api-key-setup.md`; guide the user to get a key or choose temporary/persistent setup |
| `401` or unauthorized | Missing/invalid API key | Check `AGNES_API_KEY`; never print the key |
| `400` on image generation | Parameter placement or invalid JSON | Ensure `response_format` is under `extra_body`; retry image placement fallback |
| Image-to-image says missing image | `image` not in expected location | Retry with top-level `image`, then `extra_body.image` |
| Input image cannot be read | Private URL, login, hotlink protection, or local path not encoded | Use public HTTPS URL or Data URI Base64 |
| Request timeout | Generation can take seconds to minutes | Use timeout 60-360 seconds for images; poll videos |
| Image-to-video returns `500` during task creation | Often caused by unsupported image input format or brittle server-side parameter handling | Use a public direct HTTPS image URL; run `agnes_video.py --dry-run`; let the script try fallback payloads; avoid local file/Data URI inputs for video |
| `429` or rate/rpm message | Free account RPM limit | Wait and retry later; do not bypass limits |
| Video stays `queued`/`in_progress` | Normal async generation | Keep polling every 5 seconds or return status and sidecar |
| Video `failed` | Prompt/input/queue/model issue | Report `error`, keep sidecar, suggest prompt/input simplification |
| No `url`, no `b64_json` | Unexpected response shape | Save raw response in sidecar and report the missing field |

## Image Fallback

Official docs conflict on where image inputs should be placed.

Preferred request:

```json
{
  "model": "agnes-image-2.1-flash",
  "prompt": "...",
  "size": "1024x768",
  "image": ["data:image/png;base64,..."],
  "extra_body": {
    "response_format": "url"
  }
}
```

Fallback request:

```json
{
  "model": "agnes-image-2.1-flash",
  "prompt": "...",
  "size": "1024x768",
  "extra_body": {
    "image": ["data:image/png;base64,..."],
    "response_format": "url"
  }
}
```

## JSON Commas in Examples

Some official examples are missing commas around `size` and `extra_body`. Scripts must generate valid JSON rather than copying examples literally.

## Safe Reporting

- Do not include Authorization headers in final output.
- Include status code, short error body, and the attempted mode (`top-level image` or `extra_body.image`).
- Keep generated sidecar JSON for debugging.
- If a task partially succeeds, report IDs such as `task_id` and `video_id`.

## Video 500 Debug Path

For image-to-video 500 errors:

1. Confirm the input image is a public direct HTTPS URL ending in a common image format or serving a valid image content type.
2. Do not use a local file path for video. The video API docs only guarantee URL image input.
3. Run `python scripts/agnes_video.py --prompt "..." --image "https://..." --dry-run` and inspect the planned attempts.
4. Try the default script behavior first; it attempts multiple request shapes for single-image video.
5. If all fallback attempts return 500, treat it as a server-side Agnes failure and report the sidecar JSON path plus the masked request shape, not the API key.
