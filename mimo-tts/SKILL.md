---
name: mimo-tts
description: >
  Generate speech audio using Xiaomi MiMo V2.5 TTS API. Supports preset voices,
  text-described voice design, and voice cloning. Use when the user asks to:
  (1) Convert text to speech / TTS / text-to-audio
  (2) Generate voiceover / narration / speech audio
  (3) Clone a voice from an audio sample
  (4) Design a custom voice from text description
  (5) Synthesize singing voice
  Trigger keywords: TTS, 语音合成, text to speech, voice, audio, 说话, 朗读, 唱歌
---

# MiMo V2.5 TTS Skill

Generate speech audio via Xiaomi MiMo's TTS API (OpenAI-compatible).

## Prerequisites

- API Key: already configured in `config.json` (优先级: 环境变量 `MIMO_API_KEY` > `config.json`)
- Python packages: `openai` (required), `numpy` + `soundfile` (optional, for pcm16-to-wav conversion)

```bash
pip install openai numpy soundfile
```

API Key 已写入 `<skill-dir>/config.json`，脚本会自动读取，无需设置环境变量。如需更换 key，编辑该文件即可。

## Quick Start

Run the bundled script:

```bash
python <skill-dir>/scripts/tts.py --text "你好世界" --voice 冰糖 --output hello.wav
```

## Three Models

| Mode | Flag | Model | When to use |
|------|------|-------|-------------|
| Preset voice | `--model tts` (default) | `mimo-v2.5-tts` | Use built-in voices like 冰糖, 苏打, Mia |
| Voice design | `--model voicedesign` | `mimo-v2.5-tts-voicedesign` | Describe voice in text, no audio sample needed |
| Voice clone | `--model voiceclone` | `mimo-v2.5-tts-voiceclone` | Clone from an audio file (mp3/wav) |

## Preset Voices (tts model only)

| Voice ID | Language | Gender |
|----------|----------|--------|
| mimo_default | Auto (冰糖 in CN) | - |
| 冰糖 | Chinese | Female |
| 茉莉 | Chinese | Female |
| 苏打 | Chinese | Male |
| 白桦 | Chinese | Male |
| Mia | English | Female |
| Chloe | English | Female |
| Milo | English | Male |
| Dean | English | Male |

## Style Control

Two methods — both go into the API call differently:

**Natural language style** → `--style` flag (maps to `role: user` content):
```bash
python tts.py --text "Hey boss, guess what!" --style "Bright, bouncy, excited tone" --voice Chloe
```

**Audio tag style** → embed directly in `--text` (role: assistant content):
```bash
python tts.py --text "(开心)今天天气真好呀" --voice 冰糖
```

Supported tag styles: 开心/悲伤/愤怒/温柔/磁性/慵懒/东北话/四川话/粤语/唱歌 etc.

See [references/api_details.md](references/api_details.md) for full style tag list and voice design guidance.

## Direct API Usage (without script)

For inline use or when the script doesn't fit, call the API directly with curl or OpenAI SDK:

```python
from openai import OpenAI
import base64, json, os

# 读取 config.json 中的 API Key
with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
    api_key = json.load(f)["api_key"]

client = OpenAI(api_key=api_key, base_url="https://api.xiaomimimo.com/v1")
completion = client.chat.completions.create(
    model="mimo-v2.5-tts",
    messages=[
        {"role": "user", "content": "用温柔的语气"},
        {"role": "assistant", "content": "你好，欢迎回来。"}
    ],
    audio={"format": "wav", "voice": "冰糖"}
)
audio_bytes = base64.b64decode(completion.choices[0].message.audio.data)
with open("output.wav", "wb") as f:
    f.write(audio_bytes)
```

Key rules:
- Synthesis text MUST be in `role: assistant` message
- `role: user` message is for style/voice instructions (optional for tts/voiceclone, required for voicedesign)
- Voice clone: pass `data:{mime};base64,{b64}` as `audio.voice`
- Audio sample max 10MB after base64 encoding; mp3 and wav only
