# Agnes AI API Reference

This reference is for Codex agents using Agnes only after the user explicitly asks for Agnes.

## General

Base URL:

```text
https://apihub.agnes-ai.com/v1
```

Headers:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Use the `AGNES_API_KEY` environment variable by default. Do not expose the key.

Current free-use boundary from the official docs: core models are free to use, including text, image, video, and multimodal models. Free accounts are RPM-limited. Do not promise this policy is permanent.

## Models

| Capability | Model | Notes |
|---|---|---|
| Text, multimodal understanding | `agnes-1.5-flash` | Low latency, text plus image URL input, 256K context, 65.5K max output |
| Text, agents, coding, image understanding | `agnes-2.0-flash` | Chat, streaming, tools, image URL input, Thinking, 256K context, 65.5K max output |
| Image generation/editing | `agnes-image-2.0-flash` | Text-to-image, image-to-image, multi-image composition |
| Image generation/editing | `agnes-image-2.1-flash` | Default image model; better for high-information-density images |
| Video generation | `agnes-video-v2.0` | Text-to-video, image-to-video, multi-image video, keyframes |

## Chat

Endpoint:

```text
POST https://apihub.agnes-ai.com/v1/chat/completions
```

Required: `model`, `messages`.

Useful optional fields: `temperature`, `top_p`, `max_tokens`, `stream`, `tools`, `tool_choice`, `chat_template_kwargs`, `thinking`.

Image URL input uses OpenAI-compatible content parts:

```json
{
  "model": "agnes-2.0-flash",
  "messages": [
    {
      "role": "user",
      "content": [
        { "type": "text", "text": "Describe this image." },
        {
          "type": "image_url",
          "image_url": { "url": "https://example.com/image.jpg" }
        }
      ]
    }
  ]
}
```

Thinking for OpenAI-compatible requests:

```json
{
  "chat_template_kwargs": {
    "enable_thinking": true
  }
}
```

Thinking for Anthropic-compatible requests:

```json
{
  "thinking": {
    "type": "enabled",
    "budget_tokens": 2048
  }
}
```

## Images

Endpoint:

```text
POST https://apihub.agnes-ai.com/v1/images/generations
```

Default model:

```text
agnes-image-2.1-flash
```

Parameters:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `model` | yes | string | `agnes-image-2.1-flash` or `agnes-image-2.0-flash` |
| `prompt` | yes | string | Generation or editing instruction |
| `size` | yes | string | Examples: `1024x768`, `1024x1024`, `768x1024` |
| `image` | image-to-image | string array | Public URL or Data URI Base64 |
| `return_base64` | no | boolean | Mainly for text-to-image Base64 output |
| `extra_body.response_format` | no | string | Use `url` or `b64_json` |

Important:

- Do not put `response_format` at the top level; put it under `extra_body`.
- Do not send `tags: ["img2img"]`.
- Official docs conflict on image placement: parameter tables say top-level `image`; some examples place `image` under `extra_body`. Prefer top-level `image`; if a 400-style parameter error occurs, retry with `extra_body.image`.
- Use public HTTPS image URLs or Data URI Base64. Local files must be converted before upload.
- Set client timeout around 60-360 seconds.

Text-to-image example:

```json
{
  "model": "agnes-image-2.1-flash",
  "prompt": "A luminous floating city above a misty canyon at sunrise, cinematic realism",
  "size": "1024x768",
  "extra_body": {
    "response_format": "url"
  }
}
```

Image-to-image example:

```json
{
  "model": "agnes-image-2.1-flash",
  "prompt": "Transform the scene into a rain-soaked cyberpunk night while preserving the original composition",
  "size": "1024x768",
  "image": [
    "https://example.com/input-image.png"
  ],
  "extra_body": {
    "response_format": "url"
  }
}
```

Image response:

```json
{
  "created": 1780000000,
  "data": [
    {
      "url": "https://storage.googleapis.com/agnes-aigc/xxx.png",
      "b64_json": null,
      "revised_prompt": null
    }
  ]
}
```

## Videos

Create endpoint:

```text
POST https://apihub.agnes-ai.com/v1/videos
```

Recommended query endpoint:

```text
GET https://apihub.agnes-ai.com/agnesapi?video_id=<VIDEO_ID>
```

Compatible legacy query endpoint:

```text
GET https://apihub.agnes-ai.com/v1/videos/{task_id}
```

Default model:

```text
agnes-video-v2.0
```

Create parameters:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `model` | yes | string | `agnes-video-v2.0` |
| `prompt` | yes | string | Video description |
| `image` | no | string or array | Single image-to-video input |
| `mode` | no | string | Example: `ti2vid` or `keyframes` |
| `height` | no | integer | Default 768 |
| `width` | no | integer | Default 1152 |
| `num_frames` | no | integer | Must be `<= 441` and `8n + 1` |
| `frame_rate` | no | number | 1-60 |
| `num_inference_steps` | no | integer | Inference steps |
| `seed` | no | integer | Reproducibility |
| `negative_prompt` | no | string | Avoided content |
| `extra_body.image` | no | array | Multi-image or keyframe inputs |
| `extra_body.mode` | no | string | Use `keyframes` for keyframe animation |

Video dimensions may be normalized by the service. Use returned `size` and `seconds` as authoritative.

Important for image-to-video:

- Use public HTTPS image URLs for `image` and `extra_body.image`.
- Do not assume local files or Data URI Base64 are accepted for video; the official video docs describe image URL inputs.
- For single-image video, the bundled script tries fallback request shapes because the docs are loose about `mode: ti2vid` and image placement: top-level `image` with `mode: ti2vid`, `extra_body.image` with `mode: ti2vid`, top-level `image` without auto mode, then `extra_body.image` without auto mode.
- For multi-image video and keyframes, use `extra_body.image`.
- If the server returns 500 for image-to-video, first verify that the image URL is public, direct, HTTPS, and does not require cookies or private headers.

Create response:

```json
{
  "id": "task_YOUR_TASK_ID",
  "task_id": "task_YOUR_TASK_ID",
  "video_id": "video_YOUR_VIDEO_ID",
  "object": "video",
  "model": "agnes-video-v2.0",
  "status": "queued",
  "progress": 0,
  "created_at": 1780457477,
  "seconds": "10.0",
  "size": "1280x768"
}
```

Completed query response:

```json
{
  "id": "task_YOUR_TASK_ID",
  "video_id": "video_YOUR_VIDEO_ID",
  "model": "agnes-video-v2.0",
  "object": "video",
  "status": "completed",
  "progress": 100,
  "seconds": "10.0",
  "size": "1280x768",
  "remixed_from_video_id": "https://storage.googleapis.com/agnes-aigc/aigc/videos/2026/06/03/video_xxxxxx.mp4",
  "error": null
}
```

Statuses: `queued`, `in_progress`, `completed`, `failed`.

Duration formula:

```text
seconds = num_frames / frame_rate
```

Common frame settings:

| Target | Settings |
|---|---|
| About 3s | `num_frames: 81`, `frame_rate: 24` |
| About 5s | `num_frames: 121`, `frame_rate: 24` |
| About 10s | `num_frames: 241`, `frame_rate: 24` |
| About 18s | `num_frames: 441`, `frame_rate: 24` |

Recommended polling interval: 5 seconds.
