# Data Chart Policy

Use this whenever the article needs a line chart, bar chart, histogram, scatter plot, timeline with numeric values, or any professional data visualization. This is the only place where Python/code-rendered visual output is allowed.

## Non-negotiable Rules

- A professional chart must be backed by a saved data table and source notes. Do not draw numbers from memory.
- Save chart data in the dated asset folder, for example `图片素材/YYYYMMDD/chart-data-ai-adoption.csv`, and save or record the code/command used to render the chart when practical.
- Render final charts as PNG for WeChat. SVG may be kept only as an editable source. Do not use this chart workflow to create covers, source cards, generic infographics, or decorative images.
- Include title, unit, date range, and source note on the chart or in the material list.
- If values are qualitative or invented for explanation, label the visual as `示意图` and do not count it as a data-backed chart.

## Chart Selection

- Line chart: trend over time, adoption rate, price/revenue/user count changes.
- Bar chart: compare industries, companies, models, costs, or case metrics.
- Histogram: distribution of many values, such as funding sizes or latency buckets.
- Scatter plot: relationship between two numeric dimensions.
- Timeline: use only when exact event dates matter.
- 3D chart: use sparingly; only when a real third dimension helps. Do not use 3D merely for decoration.

## Workflow

1. Identify the claim the chart will support.
2. Find source data from official reports, filings, datasets, papers, product docs, or reliable media tables.
3. Store a small CSV with columns, units, source, and notes where practical.
4. Write task-specific chart code to render PNG only for the verified data visualization. Choose the library and visual style for the article instead of using a fixed template.
5. Verify the chart does not exaggerate the claim: axis baseline, units, labels, and source note must be honest.
6. Record filename, chart type, data file, source URL, date range, and caveats in `素材清单.md`.

## Minimum Expectations

- Analytical articles over 3000 Chinese characters should include at least one data-backed chart when any numeric claim is central.
- Long industry roundups should prefer 1-2 data-backed charts over many generic source cards.
- Source cards, covers, decorative diagrams, and illustrative concept images are not data charts and must not be generated with Python/code under this policy.

