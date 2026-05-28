---
name: html-beautiful-output
description: Generate beautiful, self-contained HTML artifacts instead of plain Markdown when the user asks for visual AI output, reports, plans, code explanations, PR reviews, prototypes, diagrams, dashboards, custom editors, or shareable reading artifacts. Use this skill to turn dense information into readable, interactive, browser-viewable HTML with warm Claude/Anthropic-inspired editorial styling.
---

# HTML Beautiful Output

Create a polished, self-contained HTML artifact when the output would be easier to understand as a designed page than as a wall of Markdown.

This skill is inspired by Thariq Shihipar's "Using Claude Code: The Unreasonable Effectiveness of HTML" and by a self-contained warm editorial design system captured in this skill. The goal is not "HTML for everything"; the goal is to keep the human in the loop by making complex output more readable, visual, shareable, and interactive.

## Core Decision Rule

Use HTML when the task benefits from at least one of these:

- Side-by-side comparison, option exploration, or decision matrices.
- Dense reports, research synthesis, implementation plans, incident reviews, weekly summaries.
- Code review, PR explanation, module maps, annotated diffs, architecture diagrams.
- Design systems, component variants, interaction prototypes, animation tuning.
- Explainers that need diagrams, tabs, collapsible sections, glossaries, examples, or FAQs.
- Temporary custom editors where the user should manipulate data and export the result.
- Anything the user may want to open in a browser, send as a link, or review on mobile.

Keep Markdown when the answer is short, mostly textual, or the user needs easy manual editing/version diffs.

## Output Contract

When this skill triggers:

1. Produce a single `.html` file unless the user explicitly asks for inline code or another format.
2. Make the file self-contained: inline CSS and JS; no build step; no external framework dependency.
3. Prefer readable semantic HTML over cleverness: `header`, `main`, `section`, `article`, `aside`, `nav`, `figure`, `table`, `details`.
4. Include responsive layout. The artifact must remain usable on mobile.
5. Add interactions only when they clarify or tighten the human-AI loop.
6. If the artifact is interactive, always include an export action such as `Copy as Markdown`, `Copy JSON`, `Copy diff`, `Copy prompt`, or `Download data`.
7. Preserve source traceability: include a compact "Sources / Inputs" or "Files read" block when the artifact is based on code, notes, web pages, or datasets.
8. Validate basic HTML integrity before finalizing: title, viewport meta, accessible labels, no broken obvious IDs, no console-breaking script syntax.

## Visual Direction

Use a warm editorial Claude-like style:

- Canvas: warm cream, never pure white as the page background.
- Accent: restrained coral for primary actions, important markers, and occasional full-width callouts.
- Depth: color-blocking and hairline borders first; shadows are rare and subtle.
- Typography: serif display headlines + humanist sans body + monospace code.
- Rhythm: generous whitespace, clear section numbers, cards, summary strips, and dark code/product surfaces.
- Personality: calm, literary, precise; not neon, not glassmorphism, not generic SaaS blue.

### Design Tokens

Use these CSS custom properties as the default starting point:

```css
:root {
  color-scheme: light;

  --canvas: #faf9f5;
  --surface-soft: #f5f0e8;
  --surface-card: #efe9de;
  --surface-strong: #e8e0d2;
  --surface-white: #ffffff;

  --ink: #141413;
  --body: #3d3d3a;
  --body-strong: #252523;
  --muted: #6c6a64;
  --muted-soft: #8e8b82;
  --hairline: #e6dfd8;
  --hairline-strong: #d1cfc5;

  --primary: #cc785c;
  --primary-active: #a9583e;
  --primary-soft: #f3ded6;
  --accent-teal: #5db8a6;
  --accent-amber: #e8a55a;
  --success: #5db872;
  --warning: #d4a017;
  --error: #c64545;

  --surface-dark: #181715;
  --surface-dark-elevated: #252320;
  --surface-dark-soft: #1f1e1b;
  --on-dark: #faf9f5;
  --on-dark-soft: #a09d96;

  --serif: "Copernicus", "Tiempos Headline", "Cormorant Garamond", "EB Garamond", Georgia, serif;
  --sans: "StyreneB", Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", "SF Mono", Consolas, ui-monospace, monospace;

  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-pill: 999px;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-7: 48px;
  --space-section: 96px;
}
```

### Base CSS Skeleton

Start from this structure and adapt to the task:

```css
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--canvas);
  color: var(--body);
  font-family: var(--sans);
  font-size: 16px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}
.page {
  width: min(1180px, calc(100% - 40px));
  margin: 0 auto;
  padding: 56px 0 96px;
}
.eyebrow {
  font-family: var(--mono);
  font-size: 12px;
  letter-spacing: .11em;
  text-transform: uppercase;
  color: var(--muted);
}
h1, h2, h3 {
  color: var(--ink);
  font-family: var(--serif);
  font-weight: 400;
  letter-spacing: -0.025em;
}
h1 {
  max-width: 900px;
  margin: 12px 0 18px;
  font-size: clamp(42px, 7vw, 76px);
  line-height: .98;
}
h2 {
  margin: 0;
  font-size: clamp(28px, 3.2vw, 44px);
  line-height: 1.08;
}
h3 {
  margin: 0 0 8px;
  font-size: 22px;
  line-height: 1.2;
}
a { color: var(--primary); }
.lead {
  max-width: 760px;
  color: var(--body-strong);
  font-size: clamp(18px, 2vw, 22px);
  line-height: 1.45;
}
.section {
  margin-top: var(--space-section);
}
.section-head {
  display: flex;
  align-items: baseline;
  gap: 14px;
  margin-bottom: 24px;
}
.section-num {
  font-family: var(--mono);
  font-size: 12px;
  color: var(--ink);
  background: var(--surface-strong);
  border-radius: var(--radius-md);
  padding: 4px 10px;
}
.card {
  background: var(--surface-card);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
}
.white-card {
  background: var(--surface-white);
  border: 1px solid var(--hairline-strong);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
}
.dark-card {
  background: var(--surface-dark);
  color: var(--on-dark);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
}
.dark-card p, .dark-card li { color: var(--on-dark-soft); }
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: var(--radius-pill);
  background: var(--surface-card);
  color: var(--ink);
  font-family: var(--mono);
  font-size: 12px;
  padding: 5px 12px;
}
.badge-coral {
  background: var(--primary);
  color: white;
}
.button {
  border: 0;
  border-radius: var(--radius-md);
  background: var(--primary);
  color: white;
  cursor: pointer;
  font: 600 14px/1 var(--sans);
  padding: 12px 18px;
}
.button:hover { background: var(--primary-active); }
.button.secondary {
  background: var(--surface-white);
  color: var(--ink);
  border: 1px solid var(--hairline-strong);
}
.grid-2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; }
.grid-3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; }
.summary-strip {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin: 36px 0 64px;
}
.metric {
  background: var(--surface-white);
  border: 1px solid var(--hairline-strong);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
}
.metric-label {
  color: var(--muted);
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.metric-value {
  margin-top: 6px;
  color: var(--ink);
  font-size: 22px;
  font-weight: 650;
}
pre, code { font-family: var(--mono); }
.code-window {
  background: var(--surface-dark);
  color: var(--on-dark);
  border-radius: var(--radius-lg);
  overflow: hidden;
}
.code-window .bar {
  display: flex;
  gap: 7px;
  padding: 12px 16px;
  background: var(--surface-dark-elevated);
}
.code-window .dot { width: 10px; height: 10px; border-radius: 50%; background: var(--muted-soft); }
.code-window pre {
  margin: 0;
  padding: 20px;
  overflow-x: auto;
  color: #e8e6de;
  font-size: 13px;
  line-height: 1.65;
}
.callout-coral {
  background: var(--primary);
  color: white;
  border-radius: var(--radius-lg);
  padding: clamp(32px, 6vw, 64px);
}
.callout-coral h2 { color: white; }
@media (max-width: 900px) {
  .page { width: min(100% - 28px, 1180px); padding-top: 36px; }
  .grid-2, .grid-3, .summary-strip { grid-template-columns: 1fr; }
  .section { margin-top: 64px; }
  .card, .white-card, .dark-card { padding: 22px; }
}
```

## Artifact Patterns

### 1. Exploration / Planning

Use for uncertain directions, implementation plans, and tradeoff comparison.

Include:

- Hero with user goal and decision context.
- Summary strip: effort, risk, recommendation, affected surfaces.
- Side-by-side option cards or a timeline.
- Inline mockups or SVG data-flow diagrams.
- Risk table with severity badges.
- Open questions / decision log.

Best components: `.summary-strip`, `.grid-3`, timeline, SVG diagram, risk table, open-question cards.

### 2. Code Review / Understanding

Use for PRs, diffs, module maps, unfamiliar code paths, or architecture explanation.

Include:

- Files read and commit/PR context.
- TL;DR with review verdict.
- Annotated diff or key snippets in `.code-window` blocks.
- Severity-coded findings: high / medium / low.
- Module map or flow diagram using inline SVG.
- "Where to focus review" checklist.

Rules:

- Keep code horizontally scrollable; do not wrap long lines if it harms legibility.
- Use margin notes or callout cards next to code when possible.
- Never invent code changes; label inferred behavior as inference.

### 3. Research / Learning Explainer

Use for teaching a concept or summarizing a feature.

Include:

- Sticky or compact table of contents.
- TL;DR card near the top.
- Step-by-step path, preferably with `details` or tabs.
- Diagram first, long prose second.
- Glossary / gotchas / FAQ near the end.

Useful interactions: tabs, collapsible sections, hover-linked glossary, simple sliders for conceptual demos.

### 4. Reports / Dashboards

Use for weekly reports, incident reports, status updates, audits, or leadership summaries.

Include:

- Executive summary.
- Metrics strip.
- Timeline or grouped cards.
- Small SVG charts instead of screenshot-like fake charts.
- Risks, blockers, next actions, owners.

Keep it skimmable: every section should answer "what changed, why it matters, what next".

### 5. Design System / Component Sheet

Use for visual design directions, tokens, component variants, UI reviews, or prototypes.

Include:

- Color swatches with hex labels.
- Type scale samples.
- Spacing and radius samples.
- Component contact sheet: states, sizes, variants.
- Copyable tokens or snippets.

Respect the warm editorial style unless the user provides another brand reference.

### 6. Prototype / Playground

Use when motion, parameters, or interaction need to be felt.

Include:

- A live demo area.
- Controls: sliders, toggles, segmented buttons.
- Current parameter readout.
- Copy/export button for the chosen parameters.
- Minimal explanatory text.

Keep JS small and readable. Prefer vanilla JS.

### 7. Custom Editing Interface

Use when the user needs to sort, label, triage, approve/reject, annotate, or tune structured data.

Include:

- Purpose-built UI for the exact dataset.
- Pre-filled best-guess state when useful.
- Drag/drop, filters, forms, toggles, or live preview as needed.
- Export button that returns the user's edits as Markdown/JSON/diff/prompt.
- Reset button.

This pattern is for "use once, export, continue the agent loop" — not for building a durable product.

## Interaction Snippets

### Copy Button

Use this pattern for export actions:

```html
<button class="button" id="copyBtn">Copy as Markdown</button>
<script>
function copyText(text, btn) {
  const done = () => {
    const old = btn.textContent;
    btn.textContent = "Copied ✓";
    btn.classList.add("copied");
    setTimeout(() => { btn.textContent = old; btn.classList.remove("copied"); }, 1200);
  };
  if (navigator.clipboard?.writeText) navigator.clipboard.writeText(text).then(done, done);
  else {
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (_) {}
    ta.remove();
    done();
  }
}
</script>
```

### Tabs

```html
<div class="tabs" data-tabs>
  <div class="tab-list" role="tablist">
    <button class="on" data-tab="0">Overview</button>
    <button data-tab="1">Details</button>
  </div>
  <section class="tab-panel on">...</section>
  <section class="tab-panel">...</section>
</div>
<script>
document.querySelectorAll("[data-tabs]").forEach(box => {
  const buttons = [...box.querySelectorAll("[data-tab]")];
  const panels = [...box.querySelectorAll(".tab-panel")];
  buttons.forEach(btn => btn.addEventListener("click", () => {
    buttons.forEach(b => b.classList.remove("on"));
    panels.forEach(p => p.classList.remove("on"));
    btn.classList.add("on");
    panels[Number(btn.dataset.tab)].classList.add("on");
  }));
});
</script>
```

Add matching CSS:

```css
.tab-list { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.tab-list button {
  border: 1px solid var(--hairline-strong);
  border-radius: var(--radius-pill);
  background: var(--surface-white);
  color: var(--muted);
  padding: 8px 13px;
  cursor: pointer;
}
.tab-list button.on { background: var(--surface-dark); color: var(--on-dark); border-color: var(--surface-dark); }
.tab-panel { display: none; }
.tab-panel.on { display: block; }
```

## Quality Bar

Before delivering the artifact, check:

- Is the page more readable than the equivalent Markdown?
- Does the first screen communicate the point immediately?
- Are sections navigable and visually distinct?
- Are charts/diagrams actual SVG/HTML, not ASCII art?
- Are colors warm and restrained, with coral used intentionally?
- Is code readable on dark surfaces with horizontal scroll?
- Does mobile collapse gracefully?
- Does every interactive editor/playground have export?
- Are assumptions, sources, and limitations visible?
- Is the file self-contained and easy to open locally?

## Do / Don't

Do:

- Use HTML to increase information density and human comprehension.
- Use inline SVG for diagrams, flowcharts, timelines, and small charts.
- Use tables for structured data, but style them into cards when mobile readability matters.
- Use `details` for optional depth.
- Use a warm cream/coral/dark rhythm: cream page, cream cards, dark code/product surfaces, rare coral moments.
- Prefer one strong designed artifact over many half-styled fragments.

Don't:

- Don't dump raw generated HTML in chat if a file can be created.
- Don't rely on external CDNs unless the user explicitly wants them.
- Don't use pure white page backgrounds, generic blue SaaS palettes, neon gradients, or heavy glassmorphism.
- Don't overuse coral; it should feel like an accent, not paint spilled everywhere.
- Don't make fake controls that look interactive but do nothing.
- Don't hide crucial conclusions inside collapsed sections.
- Don't create a complex SPA when a single static HTML file is enough.

## Suggested File Naming

Use descriptive names:

- `implementation-plan-[topic].html`
- `pr-review-[branch-or-pr].html`
- `feature-explainer-[topic].html`
- `incident-report-[date-or-topic].html`
- `design-system-reference.html`
- `prototype-[interaction].html`
- `editor-[task].html`

When working inside an Obsidian vault, save generated HTML in a clear relative path such as `html-artifacts/` unless the user specifies another location.

## Minimal HTML Template

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title><!-- concise artifact title --></title>
  <style>
    /* Paste/adapt the design tokens and base CSS skeleton here. */
  </style>
</head>
<body>
  <main class="page">
    <header>
      <div class="eyebrow"><!-- artifact type / context --></div>
      <h1><!-- main conclusion or topic --></h1>
      <p class="lead"><!-- what this artifact helps the user decide/understand/do --></p>
    </header>

    <section class="summary-strip" aria-label="Key metrics or summary">
      <!-- metric cards -->
    </section>

    <section class="section">
      <div class="section-head"><span class="section-num">01</span><h2><!-- section title --></h2></div>
      <!-- designed content -->
    </section>
  </main>

  <script>
    // Add only the vanilla JS needed for tabs, filters, copy/export, or demos.
  </script>
</body>
</html>
```

