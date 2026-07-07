# Image Prompt Patterns

Use professional, varied prompts. Do not default to anime, cartoon, generic AI glow, abstract networks, or one fixed cover style.

## Prompt Selection Workflow

For every direct-generated image slot, choose a `prompt_style_route` before writing the prompt:

1. Identify the image intent: joke/metaphor, authority action, data analysis, future vision, emotional pause, source-adjacent explanation, product/interface context, or closing mood.
2. Match the intent to one style route from the table below. Do not use the same route for every image in a long article unless the article deliberately needs one coherent visual system.
3. Fill the route template with concrete article-specific subject matter, composition, palette, text language, and negative constraints. Prefer parameterized visual language over vague praise: camera angle, lens or perspective, material texture, lighting type, color ratio, layout density, and output format.
4. If the image needs evidence, do not generate fake evidence. Use generated images only for metaphor, explanation, atmosphere, or non-evidence scenes.
5. Save the generated file and record the route, prompt, tool, visible-text language choice, and any public inspiration source category in the material list.

## Prompt Components

Always include:

- image intent
- subject
- composition
- visual style route
- color palette
- lighting or material texture
- aspect ratio
- text strategy and visible-text language preference for direct generation
- negative constraints

## Generated Text Language Rule

This rule applies only when directly generating image files. It does not affect downloaded images, page captures, source charts, or prompt-only placeholders.

- First decide whether generated visible text is needed. Prefer `visible text: none` when labels or titles can be added later.
- If visible text is needed, choose the language according to article language, audience, source context, and image purpose.
- For Chinese WeChat articles, default to Simplified Chinese or Chinese-first bilingual text unless the image depicts an English-native source context such as product UI, code, papers, conferences, or international posters.
- Always include one explicit language line in direct-generation prompts: `visible text: none`, `visible text language: Simplified Chinese`, `visible text language: Chinese-first bilingual`, or `visible text language: English for UI fragments only`.
- Add negative constraints for language drift, such as `no random English words`, `no garbled Chinese characters`, `no unreadable pseudo-text`.

## Public Prompt Inspiration Policy

Public prompt libraries can be used for inspiration, but do not copy complete prompts verbatim into final generation prompts. Extract reusable structure instead: subject, medium, composition, lighting, lens/perspective, texture, palette, text strategy, negative constraints, and output format. Avoid relying on living artist names, current creator names, private brand styles, or overused cultural shortcuts as the main style engine. Prefer original compound style routes tailored to the article.

Reference-derived principles used by this file:
Public inspiration checked while designing these routes:

- `jau123/nanobanana-trending-prompts` (GitHub): category structure such as Photography, Illustration & 3D, Product & Brand, Poster Design, UI & Graphic, and prompt principles such as quantified parameters, professional terminology, negative constraints, and content-type grouping.
- `altryne/awesome-ai-art-image-synthesis` (GitHub): broad ecosystem reference for AI image synthesis resources.
- `thinkingjimmy/Learning-Prompt` (GitHub): method-oriented prompt learning reference rather than a copy-paste prompt bank.
- DiffusionDB research: large-scale prompt galleries are useful for understanding prompt patterns, but final prompts should remain article-specific and original.
- Public reporting on repetitive prompt references: avoid overusing the same famous artist/director/brand names as shortcuts because it can homogenize outputs.

- Replace vague adjectives with concrete parameters: lens, perspective, material, lighting, palette ratio, texture, format.
- Replace feeling words with professional visual terminology.
- Keep negative constraints explicit.
- Group prompts by content type before writing the final prompt.
- Preserve originality by varying route, composition, and palette rather than repeating the same famous style cues.

## Style Route Table

| prompt_style_route | use when | visual direction | avoid |
| --- | --- | --- | --- |
| `inspirational_comic_pun` | 谐音梗、反差梗、轻讽刺、概念突然被点醒 | 启发性漫画图，简洁场景，表情和动作带一点聪明的幽默，像高级专栏插画 | 低幼卡通、表情包廉价感、密集文字 |
| `mythic_justice_impact` | 官方出手、打击犯罪、监管落锤、正义介入 | 神话/史诗隐喻，例如巨大的光明拳头击中老虎、黑影、锁链或迷雾；强冲击但不血腥 | 真实暴力、真实机构 logo、血腥、具体嫌疑人肖像 |
| `data_analysis_beauty` | 数据、趋势、对比、榜单、结构分析 | 高级数据分析图、干净网格、发光节点、抽象柱线图；如无真实数据则只做概念背景 | 假数字、假标签、伪造精确图表 |
| `open_grand_horizon` | 远方、使命、长期主义、行业未来、价值感收束 | 开阔宏伟的空间，远景、地平线、云层、道路、海面或城市晨光，人物/物体很小 | 空泛宇宙脑、廉价励志海报、过饱和 |
| `minimal_eastern_digital_watercolor` | 安静、治愈、诗意、东方意境、柔软过渡段 | 极简东方意境数字水彩插画，大面积留白，低饱和青绿/蓝绿，柔和倒影、纸面颗粒 | 写实摄影、卡通、复杂背景、强线稿、高饱和 |
| `oriental_ink_xiaopin` | 国风幽默、禅意小品、轻巧收束、中文题字适合时 | 东方水墨小品画，宣纸纹理，大面积留白，小主体，淡彩点染，简短中文题字 | 商业插画感、复杂写实、鲜艳颜色、乱字 |
| `magazine_halftone` | 热点、消费文化、互联网议题、带一点复古或流行感 | 杂志半调网点，高级编辑插画，粗颗粒印刷质感，强构图，有限色盘 | 廉价波普、过密网点、低清晰度 |
| `cinematic_editorial_scene` | 人物/组织/产品处在真实场景，需要高级叙事感 | 电影感编辑摄影，真实光影，浅景深，克制色彩，强氛围 | 假新闻截图、假 UI、过度摆拍 |
| `premium_3d_concept` | 抽象机制、技术架构、复杂流程、产业链 | 高级 3D 概念图，清晰层级，材质精致，适合后期加标注 | 玩具感、塑料感、无意义发光 |
| `clean_explainer_frame` | 需要解释概念但不应伪造数据 | 极简解释性画面、留白、模块化形状、可后期加中文标签 | 假标签、文字太多、PPT 模板感 |
| `technical_teardown_isometric` | 硬件、产品、AI 系统、工具链、设备拆解 | 45 度等距技术拆解图，透明切面、组件层级、少量彩色功能箭头，像工程展板 | 伪造具体参数、过多小字、乱标签 |
| `product_brand_still_life` | 产品发布、工具推荐、品牌/物件作为隐喻 | 高级产品静物摄影，真实材质，克制布景，商业大片但不套真实品牌 | 假 logo、廉价电商图、过度反光 |
| `poster_typographic_layout` | 文章封面、观点宣言、活动/趋势主题 | 高级海报排版，强网格、留白、标题区域，图文关系明确 | 生成大量不可读文字、山寨电影海报 |
| `social_card_collage` | 多案例、多角色、多观点、清单型文章 | 社媒卡片拼贴，模块化信息区，剪贴/纸张/屏幕层叠，适合微信长文节奏 | 信息过密、像模板库封面 |
| `storyboard_sequence` | 流程、阶段、前后变化、政策执行过程 | 电影分镜/连环画序列，3-5 个清晰画格，动作递进 | 小字对白、复杂剧情、低幼漫画 |
| `warm_lifestyle_observation` | 普通人场景、消费、职场、家庭、城市观察 | 温暖生活方式摄影/插画，真实空间，自然手势，柔和环境光 | 摆拍广告感、过度完美人物 |
| `surreal_object_metaphor` | 抽象观点、悖论、风险、压力、系统性问题 | 超现实物件隐喻，单一强物体，安静背景，视觉谜题感 | 无意义怪图、恐怖猎奇、过度复杂 |

## Route Templates

### inspirational_comic_pun

`Enlightening editorial comic illustration for a Chinese WeChat article about [topic]. Pun/metaphor: [pun or contrast]. Subject: [small cast or object]. Composition: one clear visual joke, readable silhouette, subtle expression, generous negative space. Style: refined magazine comic, intelligent humor, clean shapes, soft shadows. Palette: [specific restrained palette]. Visible text language: [none / Simplified Chinese for one short caption]. Negative: no childish cartoon, no meme clutter, no cheap stickers, no random English words, no garbled Chinese characters.`

### mythic_justice_impact

`Mythic justice impact illustration for [topic]. Scene: [authority/justice metaphor] strikes [criminal-force metaphor such as tiger, shadow, chain, black market maze] with a powerful symbolic gesture, no gore. Composition: dramatic diagonal impact, large heroic force from above, small collapsing threat below, dust and light rays, cinematic scale. Style: epic editorial poster, mythological energy, modern Chinese public-affairs visual. Palette: deep ink black, gold light, restrained crimson accents. Visible text: none. Negative: no real agency logos, no real suspect face, no blood, no graphic violence, no random English text.`

### data_analysis_beauty

`Beautiful data analysis visual for [topic]. Subject: [trend/comparison/system]. Composition: elegant dashboard-like scene with abstract charts, network lines, layered panels, clear hierarchy. If real data is not supplied, use conceptual shapes only: no exact numbers, no fake labels. Style: premium analytical editorial graphic, clean grid, glassy but restrained, high readability. Palette: [specific palette]. Visible text: none or Chinese labels added later. Negative: no fake statistics, no fabricated axis labels, no random English words, no clutter.`

### open_grand_horizon

`Open grand horizon illustration for [topic]. Subject: [person/object/industry symbol] facing a vast future landscape. Composition: wide-angle scene, strong horizon line, large sky or water surface, small foreground subject, path leading into distance, sense of scale and possibility. Style: cinematic editorial art, poetic, spacious, premium poster. Palette: low-saturation [colors], soft morning/evening light. Visible text: none. Negative: no generic sci-fi brain, no corporate stock-photo look, no over-saturated sunset, no random English words.`

### minimal_eastern_digital_watercolor

`Minimal Eastern poetic digital watercolor illustration. Subject: [subject] in [setting]. Composition: large negative space, small subject placed slightly low or off-center, mirror-like water or soft atmospheric distance, gentle reflections and tiny ripples. Palette: cyan-green and blue-green with low saturation, small warm golden accents. Texture: wet brush, semi-thick paint, soft edges, subtle paper grain. Mood: quiet, ethereal, poetic, healing, premium art poster. Visible text: none unless one short Chinese title is required. Negative: no realistic photography, no cartoon, no complex background, no strong line art, no high saturation, no random English words.`

### oriental_ink_xiaopin

`Small Eastern ink-wash vignette. Background: rough xuan paper texture with natural fibers, pale speckles, old paper traces. Subject: [main subject], very small, placed near lower or side area. Composition: minimalist, large blank space. Brushwork: concise ink lines, varied ink density, dry brush, bleeding, soft wash. Color: tiny pale accents of blue-green, light pink, or ochre, like watercolor sinking into paper. Optional upper-left Chinese inscription: [short inscription]. Mood: quiet, humorous, Zen, elegant, hand-painted guofeng vignette. Visible text language: Simplified Chinese only if inscription is used. Negative: no complex background, no realistic details, no commercial illustration, no vivid colors, no random English words, no garbled Chinese characters.`

### magazine_halftone

`Premium magazine halftone editorial illustration for [topic]. Subject: [subject/metaphor]. Composition: bold crop, strong figure-ground contrast, one focal object, dynamic editorial layout. Style: modern magazine illustration, halftone dot texture, risograph-inspired grain, sophisticated print design. Palette: [2-4 colors]. Visible text: none or one short Chinese headline area left blank for later. Negative: no cheap pop-art cliche, no messy dot patterns, no random English words, no unreadable text.`

### cinematic_editorial_scene

`Cinematic editorial scene for [topic]. Subject: [person/object/environment]. Composition: realistic but symbolic scene, layered depth, natural gestures, strong focal point, restrained background. Style: high-end editorial photography / cinematic still, believable lighting, subtle texture. Palette: [specific palette]. Visible text language: [none / English only if depicting an English-native UI or source]. Negative: no fake news screenshot, no fake UI text, no fake logos, no staged-smile stock photo, no random text.`

### premium_3d_concept

`Premium 3D concept visual for [topic]. Subject: [system/mechanism]. Composition: isometric or frontal layered structure, clear spatial hierarchy, elegant materials, large clean space for later labels. Style: high-end 3D editorial diagram, refined lighting, tactile surfaces, restrained glow. Palette: [specific palette]. Visible text: none, labels added later. Negative: no toy-like plastic, no meaningless neon, no fake labels, no clutter.`

### clean_explainer_frame

`Clean explanatory frame for [topic]. Subject: [concept/process]. Composition: simple modular shapes, one central metaphor, surrounding blank zones for later Chinese labels, high readability. Style: minimal editorial explainer, calm professional design, soft shadows or flat vector-like forms. Palette: [specific palette]. Visible text: none. Negative: no fake data, no small text, no PowerPoint template look, no random English words.`

### technical_teardown_isometric

`Technical isometric teardown illustration for [topic]. Subject: [object/system/device]. Composition: 45-degree isometric view, slightly tilted, partial transparent cutaway, layered internal components, a few color-coded arrows showing function flow. Style: precise engineering manual meets museum exhibit, black technical linework on clean background, 10-15% accent color density. Visible text: none or Chinese labels added later. Negative: no fake specifications, no unreadable micro labels, no fake brand logo, no clutter.`

### product_brand_still_life

`Premium product still-life visual for [topic]. Subject: [object/tool/metaphor]. Composition: hero object on refined surface, realistic material texture, carefully placed supporting props, shallow depth of field or controlled studio lighting. Style: high-end editorial product photography, tactile, calm, believable. Palette: [specific palette]. Visible text: none. Negative: no fake logo, no e-commerce clutter, no plastic look, no random text.`

### poster_typographic_layout

`Premium poster design for [topic]. Subject: [visual metaphor]. Composition: strong grid, bold central image, generous title-safe negative space, editorial hierarchy, suitable for WeChat cover crop. Style: contemporary cultural poster, refined typography area left blank or one short Chinese phrase if required. Palette: [specific palette]. Visible text language: Simplified Chinese only if text is needed. Negative: no unreadable generated paragraphs, no fake film credits, no random English words, no messy layout.`

### social_card_collage

`Editorial social-card collage for [topic]. Subject: [several cases/roles/viewpoints]. Composition: layered cards, paper snippets, UI-like panels, small symbolic images, clear modular rhythm, enough blank space for later Chinese annotations. Style: premium magazine layout, tactile collage, subtle shadows, organized density. Palette: [specific palette]. Visible text: none or Chinese labels added later. Negative: no clutter, no fake screenshots, no tiny unreadable text, no random English.`

### storyboard_sequence

`Storyboard sequence illustration for [topic]. Subject: [process/change]. Composition: 3 to 5 clean panels showing progression from [start] to [end], cinematic framing, simple actions, consistent characters or objects. Style: refined editorial storyboard, not childish, clear visual rhythm. Palette: [specific palette]. Visible text: none. Negative: no speech bubbles, no dense captions, no confusing panel order, no fake evidence.`

### warm_lifestyle_observation

`Warm lifestyle observation scene for [topic]. Subject: [ordinary person/group/object] in [realistic place]. Composition: candid moment, natural posture, environmental details that reveal context, soft window light or evening practical light. Style: high-end editorial lifestyle photography / painterly realism, humane and grounded. Palette: [specific palette]. Visible text: none unless real-world signage is essential. Negative: no stock-photo smile, no over-polished advertising, no fake brand logo, no random text.`

### surreal_object_metaphor

`Surreal object metaphor for [topic]. Subject: [one symbolic object] transformed by [abstract force/problem]. Composition: single strong object, quiet background, precise shadow, visual puzzle that reads instantly, minimal elements. Style: premium conceptual editorial art, subtle surrealism, elegant and restrained. Palette: [specific palette]. Visible text: none. Negative: no horror, no grotesque body distortion, no meaningless weirdness, no random English words.`
## Cover Prompt

Choose one route above for the cover. Do not default every cover to the same tech poster. Use the cover route that best matches the article promise:

- punchy or satirical cover: `inspirational_comic_pun` or `magazine_halftone`
- public action / crackdown: `mythic_justice_impact`
- analytical report: `data_analysis_beauty`, `technical_teardown_isometric`, or `clean_explainer_frame`
- product/tool-focused article: `product_brand_still_life` or `technical_teardown_isometric`
- future-facing essay: `open_grand_horizon`
- process/change explainer: `storyboard_sequence` or `social_card_collage`
- poetic / reflective essay: `minimal_eastern_digital_watercolor` or `oriental_ink_xiaopin`
- ordinary-people observation: `warm_lifestyle_observation`
- abstract dilemma or risk: `surreal_object_metaphor`

Base cover prompt skeleton:

`High-end editorial cover for a Chinese WeChat article about [topic]. Route: [prompt_style_route]. Main subject: [visual metaphor]. Composition: [route-specific composition], readable negative space for title, layered depth. Style: [route style]. Palette: [specific palette]. Lighting/texture: [specific]. Aspect ratio 16:9, also suitable for 1:1 crop. Visible text language: choose based on the article context, usually Simplified Chinese or Chinese-first bilingual for Chinese WeChat covers unless an English-native source context is intentional. Negative: no real company logos, no fake UI, no small unreadable text, no random English words, no garbled Chinese characters.`

## Data Chart Prompt

When real numeric data exists, prefer code-rendered charts from saved data according to `data-chart-policy.md`, not generated fake charts.

When generating only a conceptual data background:

`Route: data_analysis_beauty. Professional data visualization background for [topic], abstract line chart and bar chart motifs, visible text: none, no exact numbers, no fake labels, clean grid, editorial analytical style, high resolution, 16:9.`

## Variety Guardrails

- A long article should usually use 2-4 compatible style routes, not one route for all generated images.
- Keep a coherent palette across the article, but vary composition and route by image purpose.
- Use humorous/comic routes only where the article tone supports humor.
- Use mythic impact routes for symbolic conflict, not for real gore or real-person attacks.
- Use poetic routes for breathing room, transitions, and endings; do not use them for hard evidence.
- Record the selected `prompt_style_route` in the material list for every directly generated image.