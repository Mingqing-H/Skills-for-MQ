# Agnes Prompting Guide

Use this reference when the user's prompt is vague, when quality matters, or when translating a creative request into a stronger Agnes prompt.

## Image Prompt Structure

English:

```text
[Main subject] + [Scene/background] + [Style] + [Lighting] + [Composition] + [Quality requirements]
```

中文：

```text
[主体] + [场景/背景] + [风格] + [光照] + [构图] + [质量要求]
```

Example:

```text
A luminous floating city above a misty canyon at sunrise, cinematic realism, wide-angle composition, rich architectural details, soft golden light, high visual density
```

中文示例：

```text
一座漂浮在晨雾峡谷上方的发光城市，电影级写实风格，广角构图，丰富建筑细节，柔和金色晨光，高信息密度，高质量
```

## Image Editing Prompt Structure

English:

```text
[Editing instruction] + [Elements to preserve] + [Target style/scene] + [Lighting] + [Composition] + [Quality requirements]
```

中文：

```text
[修改要求] + [需要保留的元素] + [目标风格/场景] + [光照] + [构图] + [质量要求]
```

Example:

```text
Change the daytime street scene into a cinematic cyberpunk night scene, add neon signs and wet road reflections, while preserving the original street layout, camera angle, and main building shapes.
```

中文示例：

```text
将白天街景改成电影感赛博朋克夜景，添加霓虹招牌和湿润路面反光，同时保留原始街道布局、镜头角度和主要建筑轮廓。
```

## Multi-Image Composition

Describe what each input image contributes and how they should relate.

English:

```text
Use the first image as [role A] and the second image as [role B]. Combine them into [scene], preserving [identity/composition/style constraints], with [lighting/style/quality].
```

中文：

```text
第一张图作为[角色/主体A]，第二张图作为[角色/主体B]。将它们组合到[场景]中，保留[身份/构图/风格约束]，使用[光照/风格/质量要求]。
```

Example:

```text
Use the first image as the main character and the second image as the companion robot. Place both in a cinematic sci-fi battle scene, preserving character identity, consistent scale, dramatic rim lighting, detailed background, high quality.
```

## Text-to-Video Prompt Structure

English:

```text
[Subject] + [Action] + [Scene] + [Camera movement] + [Lighting] + [Visual style]
```

中文：

```text
[主体] + [动作] + [场景] + [镜头运动] + [光照] + [视觉风格]
```

Example:

```text
A young astronaut walking across a red desert planet, dust blowing in the wind, slow cinematic tracking shot, dramatic sunset lighting, realistic sci-fi style.
```

中文示例：

```text
一名年轻宇航员走过红色沙漠星球，风中扬起尘土，缓慢电影感跟拍镜头，戏剧化日落光照，写实科幻风格。
```

## Image-to-Video Prompt Structure

Tell Agnes what should move and what must remain stable.

English:

```text
Animate [moving elements] with [motion style], while keeping [identity, face, outfit, composition, camera angle] consistent.
```

中文：

```text
让[运动元素]以[运动方式]动起来，同时保持[身份、脸部、服装、构图、镜头角度]稳定一致。
```

Example:

```text
Animate the character with subtle breathing motion, hair moving gently in the wind, background lights flickering softly, while keeping the face, outfit, and pose consistent.
```

## Keyframe Video

Describe transition direction and consistency constraints.

English:

```text
Create a smooth transition from the first keyframe to the second keyframe, maintaining [identity/style/camera angle], with [motion pacing].
```

中文：

```text
从第一张关键帧平滑过渡到第二张关键帧，保持[身份/风格/镜头角度]一致，使用[运动节奏]。
```

## Quality Checklist

- Be specific about subject, environment, style, lighting, camera angle, and composition.
- For edits, say both what to change and what to preserve.
- For high-density images, describe visual hierarchy and important secondary elements.
- For video, include motion and camera language, not just static scene description.
- Avoid contradictory style requests unless the user wants a hybrid.
