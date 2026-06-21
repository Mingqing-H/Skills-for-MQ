# SVG Interaction Presets

These presets add motion and interactivity to WeChat article HTML via inline `<svg>` and CSS animations. They layer on top of any static style preset from `style-presets.md`. All visible article text must remain unchanged.

## Trigger mechanisms

- **auto**: Animation plays automatically on page load. No user action required. Simplest to implement, highest compatibility.
- **tap**: User taps a region to trigger the next animation step. Requires `onclick` on a wrapper element with `cursor: pointer`.
- **scroll-reveal**: Content animates in as the user scrolls past it. Simulated via CSS `animation-delay` staggered timers (true IntersectionObserver is not available in WeChat).

---

## svg-data-report

Use for data-heavy articles, annual recaps, industry reports, model benchmarks, and metric-driven storytelling.

### Number counter animation

- Target: key statistics (e.g. "1750亿参数", "97.3%准确率").
- Technique: wrap each digit sequence in a `<span>` with CSS `@keyframes` that rapidly cycles through digits 0-9 before landing on the final value.
- Duration: 1.5-2s, `animation-fill-mode: forwards`.
- Stagger: each number group delayed by 0.2-0.3s for a cascade effect.
- Implementation:

```html
<section style="text-align:center; margin:20px 0;">
  <span style="display:inline-block; font-size:48px; font-weight:700; color:#2563EB; font-family:'DIN Alternate',monospace;">
    <span style="display:inline-block; animation:digit-roll 1.8s forwards;">1</span><span style="display:inline-block; animation:digit-roll 1.8s 0.1s forwards;">7</span><span style="display:inline-block; animation:digit-roll 1.8s 0.2s forwards;">5</span><span style="display:inline-block; animation:digit-roll 1.8s 0.3s forwards;">0</span><span style="display:inline-block; margin-left:4px; font-size:24px;">亿参数</span>
  </span>
</section>
<style>
@keyframes digit-roll {
  0% { opacity:0.3; transform:translateY(8px); }
  50% { opacity:0.7; }
  100% { opacity:1; transform:translateY(0); }
}
</style>
```

### Keyword tag float-in

- Target: key terms, model names, feature labels.
- Technique: tags slide in from alternating sides (left/right) with slight rotation, then settle.
- Stagger: 0.15s between each tag.
- Style: pill-shaped badges with accent background, white text, `border-radius:20px; padding:4px 14px;`.

### Section title entrance

- Target: h2/h3 section headings.
- Technique: title slides up from below with fade-in, gradient underline expands from 0% to 100% width.
- Duration: 0.8s title, 0.6s underline (delayed 0.3s).

### Trigger

All animations are **auto**-play, staggered by `animation-delay`. No user interaction needed.

---

## svg-ambient-float

Use for narrative essays, seasonal content, lifestyle stories, and atmospheric pieces where gentle motion enhances mood without demanding attention.

### Floating elements

- Target: decorative icons, small illustrations, leaf/petal shapes, geometric accents.
- Technique: CSS `@keyframes` with slow sinusoidal motion — combine `translateX`, `translateY`, and `rotate` at different periods to avoid mechanical repetition.
- Duration: 6-12s per cycle, `animation-iteration-count: infinite`.
- Opacity: 0.3-0.7 to keep elements subordinate to content.
- Count: 3-8 floating elements per screen, positioned via absolute positioning within a relative wrapper.

### Gentle sway

- Target: section dividers, decorative borders, accent lines.
- Technique: slow `rotate` oscillation (±3-5deg) around center origin.
- Duration: 4-6s, infinite loop.

### Breathing pulse

- Target: accent dots, small circles, indicator lights.
- Technique: `scale(1)` → `scale(1.15)` → `scale(1)` with ease-in-out timing.
- Duration: 3-4s, infinite loop.

### Implementation pattern

```html
<section style="position:relative; overflow:hidden; min-height:200px;">
  <!-- Floating leaf 1 -->
  <section style="position:absolute; top:15%; left:8%; opacity:0.5; animation:float-a 8s ease-in-out infinite;">
    <svg width="24" height="24" viewBox="0 0 24 24"><path d="M17 8C8 10 5.9 16.17 3.82 21.34l1.89.66 .95-2.3c.48.17.98.3 1.34.3C19 20 22 3 22 3c-1 2-8 2.25-13 3.25S2 11.5 2 13.5s1.75 3.75 1.75 3.75" fill="#4ADE80" stroke="none"/></svg>
  </section>
  <!-- Floating circle 2 -->
  <section style="position:absolute; top:40%; right:12%; opacity:0.4; animation:float-b 10s ease-in-out infinite;">
    <svg width="16" height="16"><circle cx="8" cy="8" r="8" fill="#60A5FA"/></svg>
  </section>
  <!-- Article content here -->
</section>
<style>
@keyframes float-a {
  0%,100% { transform:translate(0,0) rotate(0deg); }
  25% { transform:translate(12px,-8px) rotate(5deg); }
  50% { transform:translate(-6px,10px) rotate(-3deg); }
  75% { transform:translate(8px,4px) rotate(2deg); }
}
@keyframes float-b {
  0%,100% { transform:translate(0,0) scale(1); }
  50% { transform:translate(-10px,12px) scale(1.1); }
}
</style>
```

### Trigger

All animations are **auto**-play, continuous loop. No user interaction needed.

---

## svg-chat-sim

Use for AI tool reviews, chatbot demos, product walkthroughs, and any article that benefits from a simulated conversation UI.

### Chat bubble reveal

- Target: simulated message exchanges between user and AI/system.
- Technique: each message bubble starts with `max-height:0; opacity:0; overflow:hidden` and animates to `max-height:200px; opacity:1` with staggered delays.
- Stagger: 1-2s between messages to simulate typing delay.
- Layout: alternating left (system/AI) and right (user) alignment with avatar circles.

### Typing indicator

- Target: "..." typing dots before each AI response.
- Technique: three dots with staggered `opacity` animation (0→1→0) cycling at 0.6s intervals.
- Duration: show for 1-1.5s before the actual message reveals.

### Implementation pattern

```html
<section style="max-width:360px; margin:20px auto; font-family:-apple-system,sans-serif;">
  <!-- AI message -->
  <section style="display:flex; align-items:flex-start; margin-bottom:16px; animation:msg-in 0.5s 0.5s both;">
    <section style="width:36px; height:36px; border-radius:50%; background:#2563EB; flex-shrink:0;"></section>
    <section style="margin-left:10px; background:#F3F4F6; padding:10px 14px; border-radius:0 12px 12px 12px; max-width:260px;">
      <p style="margin:0; font-size:14px; line-height:1.6; color:#1F2937;">你好！我是 AI 助手，有什么可以帮你的？</p>
    </section>
  </section>
  <!-- User message -->
  <section style="display:flex; align-items:flex-start; justify-content:flex-end; margin-bottom:16px; animation:msg-in 0.5s 2s both;">
    <section style="margin-right:10px; background:#2563EB; padding:10px 14px; border-radius:12px 0 12px 12px; max-width:260px;">
      <p style="margin:0; font-size:14px; line-height:1.6; color:#FFFFFF;">帮我分析一下这段代码</p>
    </section>
    <section style="width:36px; height:36px; border-radius:50%; background:#E5E7EB; flex-shrink:0;"></section>
  </section>
</section>
<style>
@keyframes msg-in {
  from { opacity:0; transform:translateY(12px); max-height:0; }
  to { opacity:1; transform:translateY(0); max-height:200px; }
}
</style>
```

### Trigger

All animations are **auto**-play with staggered delays simulating real-time conversation. No user interaction needed.

---

## svg-scroll-reveal

Use for long-form storytelling, step-by-step guides, timeline narratives, and any article where content should appear progressively as the reader scrolls.

### Simulated scroll reveal

- True IntersectionObserver is not available in WeChat's webview. Instead, simulate progressive reveal using timed `animation-delay` that approximates reading speed.
- Estimate: average reader scrolls ~1 screen per 3-5 seconds. Set delays accordingly for each section.
- Technique: each content block starts with `opacity:0; transform:translateY(30px)` and animates to `opacity:1; transform:translateY(0)`.

### Staggered content blocks

```html
<section>
  <section style="opacity:0; animation:reveal-up 0.8s 1s both;">
    <p>第一段内容...</p>
  </section>
  <section style="opacity:0; animation:reveal-up 0.8s 4s both;">
    <p>第二段内容...</p>
  </section>
  <section style="opacity:0; animation:reveal-up 0.8s 7s both;">
    <p>第三段内容...</p>
  </section>
</section>
<style>
@keyframes reveal-up {
  from { opacity:0; transform:translateY(30px); }
  to { opacity:1; transform:translateY(0); }
}
</style>
```

### Trigger

**auto**-play with timed delays. This is a best-effort simulation — actual scroll position cannot be detected in WeChat.

---

## svg-3d-parallax

Use for product showcases, brand storytelling, immersive narratives, and articles that need a "wow factor" first screen.

### Depth layers

- Technique: stack 3-5 layers of images/elements at different `z-index` levels within a perspective container.
- Each layer moves at a different speed on tap (closest moves most, background moves least).
- Use CSS `transform: translateZ()` and `perspective` for depth effect.

### Tap-to-advance

- User taps the screen to advance through parallax frames.
- Each tap triggers a CSS transition on all layers simultaneously.
- Implementation uses hidden radio inputs (`<input type="radio" id="f1">` + `<label for="f1">`) to control state without JavaScript.

### Caution

- Complex to implement inline. Consider using E2 editor or Xiumi for production use.
- WeChat may strip `perspective` on some devices. Always provide a graceful fallback with static layout.
- Keep file size under 50KB total for the SVG section to ensure fast loading.

---

## Combining presets

SVG interaction presets can be combined with static style presets:

| Static preset | Recommended SVG interaction | Use case |
|---------------|---------------------------|----------|
| `tech-brief` | `svg-data-report` | AI model comparison, benchmark data |
| `magazine-feature` | `svg-ambient-float` | Narrative essays, culture pieces |
| `clean-editorial` | `svg-scroll-reveal` | Long-form analysis, step-by-step |
| `campus-pink` | `svg-ambient-float` | Event recaps, lifestyle content |
| any | `svg-chat-sim` | AI tool reviews, chatbot demos |
| any | `svg-3d-parallax` | Product launches, brand showcases |

## Saving new SVG presets

When adding a new SVG interaction preset, include:

- Preset name prefixed with `svg-` in lowercase hyphen-case.
- Best-fit content types.
- Trigger mechanism (auto / tap / scroll-reveal).
- Implementation pattern with inline `<svg>` and CSS `@keyframes`.
- Caution notes for WeChat compatibility.
- Example code snippet.
