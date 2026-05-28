# MiMo V2.5 TTS API Details

## API Endpoint

- Base URL: `https://api.xiaomimimo.com/v1`
- Endpoint: `POST /chat/completions`
- Auth header: `api-key: $MIMO_API_KEY`

## Models

| Model ID | Capability | Notes |
|----------|-----------|-------|
| `mimo-v2.5-tts` | Preset voice synthesis | Supports singing mode; no voice design/clone |
| `mimo-v2.5-tts-voicedesign` | Text-described voice design | No singing, no preset voices, no clone |
| `mimo-v2.5-tts-voiceclone` | Voice cloning from audio | No singing, no preset voices, no design |

## Preset Voices

| Voice ID | Language | Gender |
|----------|----------|--------|
| `mimo_default` | Auto (冰糖 in CN cluster, Mia elsewhere) | - |
| `冰糖` | Chinese | Female |
| `茉莉` | Chinese | Female |
| `苏打` | Chinese | Male |
| `白桦` | Chinese | Male |
| `Mia` | English | Female |
| `Chloe` | English | Female |
| `Milo` | English | Male |
| `Dean` | English | Male |

## Audio Formats

- `wav` — full audio file, returned as base64
- `pcm16` — raw PCM16LE, 24kHz mono, returned as base64 (recommended for streaming concatenation)

## Style Control

### Natural Language Control (role: user)

Place style instructions in `role: user` content. The model interprets natural language descriptions.

Examples:
- "用轻快上扬的语调向领导报喜，语速稍快，带着查到成绩后压抑不住的激动与小骄傲"
- "Bright, bouncy, slightly sing-song tone — like you're bursting with good news"

**Director mode** — structured format for complex performances:
```
角色：百年门阀岑家的现任大当家。自出生便被过继给祖庙的守门老人抚养...
场景：在祠堂的阴影里，看着那个不顾一切冲破保安防线来找她的男人...
指导：冰冷、慵懒却极具威压的低音御姐。发声通道非常松弛...
```

### Audio Tag Control (role: assistant)

Embed tags directly in the synthesis text. Place style tag at the beginning, fine-grained tags inline.

**Opening style tag**: `(风格名)文本内容`
- Supported bracket types: `()`, `（）`, `[]`
- Multiple styles: `(风格1 风格2)文本`

**Style categories**:

| Category | Examples |
|----------|---------|
| Basic emotion | 开心/悲伤/愤怒/恐惧/惊讶/兴奋/委屈/平静/冷漠 |
| Compound emotion | 怅然/欣慰/无奈/愧疚/释然/嫉妒/厌倦/忐忑/动情 |
| Tone | 温柔/高冷/活泼/严肃/慵懒/俏皮/深沉/干练/凌厉 |
| Voice quality | 磁性/醇厚/清亮/空灵/稚嫩/苍老/甜美/沙哑/醇雅 |
| Character | 夹子音/御姐音/正太音/大叔音/台湾腔 |
| Dialect | 东北话/四川话/河南话/粤语 |
| Roleplay | 孙悟空/林黛玉 |
| Singing | 唱歌 (must be first tag, format: `(唱歌)歌词`) |

**Inline fine-grained tags** (placed anywhere in text):

| Category | Examples |
|----------|---------|
| Breathing | 吸气/深呼吸/叹气/长叹一口气/喘息/屏息 |
| Emotion state | 紧张/害怕/激动/疲惫/委屈/撒娇/心虚/震惊/不耐烦 |
| Voice feature | 颤抖/声音颤抖/变调/破音/鼻音/气声/沙哑 |
| Laughter/Cry | 笑/轻笑/大笑/冷笑/抽泣/呜咽/哽咽/嚎啕大哭 |

**Tag examples**:
- `(怅然)这么多年过去了，再走过那条街，心里一下子空了一块。`
- `(慵懒)再让我睡五分钟……就五分钟，真的，最后一次。`
- `(东北话)哎呀妈呀，这天儿也忒冷了吧！`
- `(唱歌)原谅我这一生不羁放纵爱自由`
- `（紧张，深呼吸）呼……冷静，冷静。（语速加快）自我介绍已经背了五十遍了。`

## Voice Design (voicedesign model)

The `role: user` content IS the voice description. Key dimensions:

| Dimension | Examples |
|-----------|---------|
| Gender/Age | "young woman in her mid-20s", "五十多岁的中年男性" |
| Voice quality | "deep and gravelly", "丝滑醇厚、带着磁性" |
| Mood/tone | "warm and confident", "温柔但带着一丝疲惫" |
| Pace | "slow and deliberate", "语速极快，像连珠炮" |
| Character | narrator, podcast host, 深夜电台DJ |
| Style | casual and colloquial, 一本正经地 |
| Scene | narrating a nature documentary, 在给投资人路演 |

Tips:
- 1-4 sentences, be specific
- Avoid conflicting traits (e.g., "稚嫩的童声 + CEO气场")
- Avoid audio effect words (reverb, echo, EQ)
- Avoid vague words ("普通的", "正常的")
- Chinese or English both work

## Voice Clone (voiceclone model)

- Pass audio sample as `data:{MIME_TYPE};base64,{BASE64_AUDIO}` in `audio.voice`
- Supported MIME: `audio/mpeg` (or `audio/mp3`), `audio/wav`
- Max base64 size: 10MB
- `role: user` content is optional (for style control)
