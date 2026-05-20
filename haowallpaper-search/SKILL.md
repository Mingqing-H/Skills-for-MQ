---
name: haowallpaper-search
description: >
  使用 Playwright 浏览器自动化从 haowallpaper.com 搜索壁纸资源，
  按热度排序提取高质量结果，并从详情页获取直链图片。
  适用于用户请求找指定角色/主题的高热度壁纸场景。
---

## haowallpaper.com 壁纸搜索工作流

### 工具准备
使用 Playwright MCP 工具：
- `browser_navigate` — 页面导航
- `browser_snapshot` — 获取页面快照（可见内容）
- `browser_evaluate` — 执行 JavaScript 提取 meta/数据

### URL 模式

| 类型 | 模式 |
|------|------|
| 搜索页 | `https://haowallpaper.com/?page=1&search={关键词}&sortType=3&rows=9` |
| 详情页 | `https://haowallpaper.com/homeViewLook/{id}` |
| 直链图片 | `https://haowallpaper.com/link/common/file/previewFileImg/{id}` |

> `sortType=3` 表示按热度/下载量排序

### 工作流步骤

#### Step 1 — 搜索并提取结果
1. `browser_navigate` 打开搜索 URL（关键词中文即可）
2. `browser_snapshot` 获取页面快照
3. 从快照中解析每个结果的：
   - **详情页 ID**（从链接 `homeViewLook/{id}` 提取）
   - **下载量**（用于衡量热度）
   - **标题/分辨率**（用于确认质量）

#### Step 2 — 按热度排序选取
- 将结果按下载量降序排列
- 选取前 N 个（如用户要求 3 张或 5 张）
- 记录每个的 ID 和下载量

#### Step 3 — 访问详情页获取直链
对每个选中的 ID：
1. `browser_navigate` 到 `https://haowallpaper.com/homeViewLook/{id}`
2. `browser_evaluate` 执行：
   ```js
   () => document.querySelector('meta[property="og:image"]')?.content ||
         document.querySelector('meta[name="twitter:image"]')?.content ||
         'not found'
   ```
3. 若返回 `favicon.ico` 或无效值，尝试 `twitter:image`
4. 将 `{id}` 替换进直链模板：`https://haowallpaper.com/link/common/file/previewFileImg/{id}`

#### Step 4 — 输出结果
提供：
- 排名、详情页链接、直链图片链接、分辨率、下载量
- 当用户明确要求预览时候，加入会话内图片预览（markdown）： ![{title}]({image_url})
### 注意事项
- 搜索结果页的快照中直接有下载量字段（下载量：xxxx），这是热度指标
- 直链图片 ID 可能与页面 ID 不同，需以 `og:image` 返回的实际 ID 为准
- 部分页面 `og:image` 可能返回网站 favicon，此时回退到 `twitter:image`
- 进程结束前可用 `browser_close` 关闭浏览器

### 适用场景
- 用户请求"找 X 张某角色/主题的高热度壁纸"
- 需要获取直链而非仅来源页
- 结果需按热度排序
