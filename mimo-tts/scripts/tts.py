#!/usr/bin/env python3
"""MiMo V2.5 TTS - Text-to-Speech via Xiaomi MiMo API.

Usage:
  python tts.py --text "你好世界" --voice 冰糖 --output hello.wav
  python tts.py --text "Hello world" --model voicedesign --style "young male tone" --output hello.wav
  python tts.py --text "你好" --model voiceclone --voice-file sample.mp3 --output hello.wav
  python tts.py --text "(开心)今天天气真好呀" --voice 冰糖 --output happy.wav
"""

import argparse
import base64
import json
import os
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_api_key():
    # 1. Environment variable
    key = os.environ.get("MIMO_API_KEY")
    if key:
        return key
    # 2. config.json in skill directory
    config_path = os.path.join(SKILL_DIR, "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            key = config.get("api_key", "")
            if key and key != "YOUR_API_KEY_HERE":
                return key
    print("Error: No API key found. Set MIMO_API_KEY env var or edit config.json", file=sys.stderr)
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="MiMo V2.5 TTS")
    parser.add_argument("--text", required=True, help="Text to synthesize (role: assistant content)")
    parser.add_argument("--style", default=None, help="Style instruction (role: user content, for natural language control)")
    parser.add_argument("--model", default="tts", choices=["tts", "voicedesign", "voiceclone"],
                        help="Model variant: tts (preset voice), voicedesign (text-described voice), voiceclone")
    parser.add_argument("--voice", default="mimo_default", help="Preset voice ID (for tts model)")
    parser.add_argument("--voice-file", default=None, help="Audio file for voice cloning (mp3/wav)")
    parser.add_argument("--output", default="output.wav", help="Output file path")
    parser.add_argument("--format", default="wav", choices=["wav", "pcm16"], help="Audio format")
    args = parser.parse_args()

    api_key = get_api_key()

    try:
        from openai import OpenAI
    except ImportError:
        print("Error: 'openai' package not installed. Run: pip install openai", file=sys.stderr)
        sys.exit(1)

    model_map = {
        "tts": "mimo-v2.5-tts",
        "voicedesign": "mimo-v2.5-tts-voicedesign",
        "voiceclone": "mimo-v2.5-tts-voiceclone",
    }
    model_id = model_map[args.model]

    # Build messages
    messages = []

    # user message
    if args.model == "voicedesign":
        if not args.style:
            print("Error: --style is required for voicedesign model (describes the voice)", file=sys.stderr)
            sys.exit(1)
        messages.append({"role": "user", "content": args.style})
    elif args.style:
        messages.append({"role": "user", "content": args.style})
    else:
        messages.append({"role": "user", "content": ""})

    messages.append({"role": "assistant", "content": args.text})

    # Build audio config
    audio_config = {"format": args.format}

    if args.model == "voiceclone":
        if not args.voice_file:
            print("Error: --voice-file is required for voiceclone model", file=sys.stderr)
            sys.exit(1)
        mime_map = {".mp3": "audio/mpeg", ".wav": "audio/wav"}
        ext = os.path.splitext(args.voice_file)[1].lower()
        mime = mime_map.get(ext, "audio/mpeg")
        with open(args.voice_file, "rb") as f:
            voice_b64 = base64.b64encode(f.read()).decode("utf-8")
        audio_config["voice"] = f"data:{mime};base64,{voice_b64}"
    else:
        audio_config["voice"] = args.voice

    client = OpenAI(api_key=api_key, base_url="https://api.xiaomimimo.com/v1")

    print(f"Calling {model_id}...")
    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,
        audio=audio_config,
    )

    message = completion.choices[0].message
    if not hasattr(message, "audio") or message.audio is None:
        print("Error: No audio data in response", file=sys.stderr)
        sys.exit(1)

    audio_bytes = base64.b64decode(message.audio.data)

    # For pcm16, convert to wav for easy playback
    if args.format == "pcm16" and args.output.endswith(".wav"):
        try:
            import numpy as np
            import soundfile as sf
            import io
            pcm_data = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            sf.write(args.output, pcm_data, samplerate=24000)
        except ImportError:
            # Fallback: save raw pcm
            pcm_path = args.output.replace(".wav", ".pcm")
            with open(pcm_path, "wb") as f:
                f.write(audio_bytes)
            print(f"Note: numpy/soundfile not installed. Saved raw PCM to {pcm_path}")
            print("Install with: pip install numpy soundfile")
            return
    else:
        with open(args.output, "wb") as f:
            f.write(audio_bytes)

    print(f"Audio saved to {args.output}")

if __name__ == "__main__":
    main()
