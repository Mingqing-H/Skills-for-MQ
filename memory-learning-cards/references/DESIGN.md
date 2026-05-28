# Claude DESIGN

> 来源：[awesome-design-md](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/claude)
> 设计关键词：**温暖编缉 · 奶油画布 · 珊瑚色 CTA · 衬线标题**

## 概述

Claude 的设计语言是所有 AI 产品中最温暖、最具编缉感的。奶油色画布（`#faf9f5`）刻意避开其他 AI 品牌使用的冷灰白色，衬线标题使用 Copernicus 字体以 weight 400 渲染，配合负字间距。珊瑚色（`#cc785c`）是 Anthropic 的标志性强调色——温暖、微微收敛，刻意不使用青色或蓝色。三种表面模式交替：奶油色画布、浅奶油卡片、深海军蓝产品表面。

**核心特征：**
- 奶油画布 + 珊瑚 CTA 的暖色调组合，与 AI 行业蓝灰主流刻意不同
- 衬线标题（Copernicus / Tiempos Headline）+ 无衬线正文（StyreneB / Inter）
- 三种表面交替：画布 → 卡片 → 深色，形成视觉节奏
- 尖刺标记（spike-mark）作为 wordmark 前缀和内容标记

## 颜色系统

```yaml
primary:         "#cc785c"  # 珊瑚色 — 标志性 CTA
primary-active:  "#a9583e"
primary-disabled:"#e6dfd8"
ink:             "#141413"  # 标题
body:            "#3d3d3a"  # 正文
body-strong:     "#252523"
muted:           "#6c6a64"
muted-soft:      "#8e8b82"
hairline:        "#e6dfd8"
hairline-soft:   "#ebe6df"
canvas:          "#faf9f5"  # 奶油画布
surface-soft:    "#f5f0e8"
surface-card:    "#efe9de"
surface-cream-strong: "#e8e0d2"
surface-dark:    "#181715"  # 深色表面
surface-dark-elevated: "#252320"
surface-dark-soft: "#1f1e1b"
on-primary:      "#ffffff"
on-dark:         "#faf9f5"
on-dark-soft:    "#a09d96"
accent-teal:     "#5db8a6"  # 辅助蓝绿
accent-amber:    "#e8a55a"  # 辅助琥珀
success:         "#5db872"
warning:         "#d4a017"
error:           "#c64545"
```

**使用规则：**
- 珊瑚色仅用于主 CTA 和全宽 callout 卡片
- 蓝绿色（teal）少量用于次级产品表面
- 琥珀色用于分类标签和内联高亮
- 文字层级：ink → body-strong → body → muted → muted-soft

## 字体系统

| 层级 | 字体 | 大小 | 字重 | 用途 |
|------|------|------|------|------|
| display-xl | Copernicus, Tiempos Headline, serif | 64px | 400 | -1.5px 字间距 |
| display-lg | 同上 | 48px | 400 | -1px |
| display-md | 同上 | 36px | 400 | -0.5px |
| display-sm | 同上 | 28px | 400 | -0.3px |
| title-lg | StyreneB, Inter, sans-serif | 22px | 500 | 卡片标题 |
| title-md | 同上 | 18px | 500 | |
| title-sm | 同上 | 16px | 500 | |
| body-md | 同上 | 16px | 400 | 正文 |
| body-sm | 同上 | 14px | 400 | |
| caption | 同上 | 13px | 500 | |
| button | 同上 | 14px | 500 | |
| code | JetBrains Mono | 14px | 400 | 1.6 行高 |

**字体原则：**
- display 级别用 weight 400（regular），绝不加粗
- 负字间距（-0.3 到 -1.5px）是核心特征
- 开源替代：Cormorant Garamond (weight 500) 或 EB Garamond 替代衬线；Inter 或 Söhne 替代无衬线

## 关键组件

| 组件 | 特征 |
|------|------|
| button-primary | bg `#cc785c`, 白字, rounded-md, 12×20px, 40px 高 |
| button-secondary | canvas 背景, ink 文字, hairline 边框 |
| top-nav | canvas 背景, 64px 高 |
| hero-band | canvas, display-xl, 96px padding |
| feature-card | surface-card (#efe9de), rounded-lg, 32px padding |
| product-mockup-card-dark | surface-dark, rounded-lg, 32px padding |
| code-window-card | surface-dark, code 字体, rounded-lg, 24px padding |
| pricing-tier-card | canvas, rounded-lg, 32px；featured 版反转深色 |
| callout-card-coral | primary 填充, 白字, rounded-lg, 48px padding |
| cta-band-coral | primary 填充, display-sm, 64px padding |
| cta-band-dark | surface-dark, display-sm, 64px padding |
| footer | surface-dark, on-dark-soft 文字, 64px padding |

## 布局与深度

- **基础单位**：4px
- **段间距**：96px
- **卡片内边距**：32px
- **最大内容宽**：~1200px 居中
- **Hero**：6/6 分栏
- **Feature 卡片**：桌面端 3-up
- **深度策略**：色彩块优先，阴影极少——深度通过奶油 vs 深色对比实现

## Do's and Don'ts

✅ **Do：**
- 锚定奶油画布
- display 标题使用衬线 + 负字间距
- 珊瑚色仅用于主 CTA 和全宽 callout
- 在深色 mockup 中展示真实产品 chrome
- 交替奶油/深色 band 制造节奏

❌ **Don't：**
- 不要用冷灰色
- 不要把衬线标题加粗
- 不要用冷蓝色 accent
- 不要过度使用珊瑚色
- 不要用无衬线做 display
- 不要在连续 band 中重复同一种表面模式

## 断点

| 名称 | 宽度 | 变化 |
|------|------|------|
| Mobile | < 768px | 汉堡菜单，单列 |
| Tablet | 768–1024px | 2-up 网格 |
| Desktop | 1024–1440px | 完整导航，3-up/4-up |
| Wide | > 1440px | 1200px 上限 |

---

*Claude 的设计系统定义了 AI 产品中最温暖的界面语言——通过奶油+珊瑚的组合刻意与行业主流的蓝色+灰色形成反差。*
