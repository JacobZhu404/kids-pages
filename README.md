# kids-pages · 孩子数学/算法互动学习页托管

一个独立的静态 HTML 托管项目，把为孩子准备的图文/互动算法教程（GESP 六级系列）
部署到 **Cloudflare Pages** 公网上，方便随时分享给孩子用手机/平板打开。

方案沿用 ad-newsletter 的成熟托管方式：
本地 `public/` 目录 → `wrangler pages deploy` → 固定公网域名 `https://kids-pages-1pw.pages.dev/...`。

> ⚠️ 注意：Cloudflare Pages 为项目分配的子域名实际为 **`kids-pages-1pw.pages.dev`**（非 `kids-pages-1pw.pages.dev`）。若日后绑定自定义域名，按需替换下方所有链接。

## 目录结构

```
kids-pages/
├── public/                      # Cloudflare Pages 构建输出目录（唯一上线的根）
│   ├── index.html              # 首页导航（列出所有教程入口）
│   ├── gesp6-p11962-tutorial.html  # P11962 树上漫步 · 图文动画精讲（自包含）
│   ├── gesp6-dfs-bfs.html          # 深搜广搜通关站（自包含）
│   ├── p11962-tree-walk.html       # P11962 树上漫步 · 互动教学（自包含）
│   ├── dsfs-bfs-walkthrough.html   # DFS/BFS 走查教程（自包含）
│   └── tree-stroll/                # 树上漫步互动教程（含 JS + 字体依赖）
│       ├── index.html
│       ├── assets/tutorial.js
│       └── _shared/fonts/*.ttf
├── core/deploy_cf_pages.py     # CF Pages 部署脚本（回车一次全量部署）
├── wrangler.toml               # wrangler 配置（pages_build_output_dir="public"）
├── cloudflare_config.json      # CF API Token / Account ID / 项目名
└── README.md
```

## 快速开始

### 本地预览
```bash
cd public && python3 -m http.server 8000
# 浏览器打开 http://localhost:8000/
```

### 部署到公网
```bash
python3 core/deploy_cf_pages.py
# 成功后在 https://kids-pages-1pw.pages.dev/ 查看
```

部署后各页面固定 URL：

- 首页：`https://kids-pages-1pw.pages.dev/`
- P11962 树上漫步·图文动画：`https://kids-pages-1pw.pages.dev/gesp6-p11962-tutorial.html`
- 深搜广搜通关站：`https://kids-pages-1pw.pages.dev/gesp6-dfs-bfs.html`
- P11962 互动教学：`https://kids-pages-1pw.pages.dev/p11962-tree-walk.html`
- DFS/BFS 走查教程：`https://kids-pages-1pw.pages.dev/dsfs-bfs-walkthrough.html`
- 树上漫步互动版：`https://kids-pages-1pw.pages.dev/tree-stroll/`

## 内容来源

| 页面 | 来源文件 | 说明 |
|------|---------|------|
| gesp6-p11962-tutorial.html | `.qwenworkcn/.../GESP六级-P11962树上漫步.html` | 自包含 |
| gesp6-dfs-bfs.html | `.qwenworkcn/.../GESP六级-深搜广搜通关站.html` | 自包含 |
| p11962-tree-walk.html | `WorkBuddy/.../p11962_tutorial.html` | 自包含 |
| dsfs-bfs-walkthrough.html | `WorkBuddy/.../dfs_bfs_tutorial.html` | 自包含 |
| tree-stroll/ | `TRAE .../tree-stroll/` | 含 assets + fonts 依赖 |

## 维护笔记

- `public/` 是唯一上线根目录。新增页面直接放 `public/` 下，重跑部署脚本即可。
- `tree-stroll/` 用了相对路径引用 `assets/tutorial.js` 与 `_shared/fonts`，需整目录一起拷贝，勿单独拆文件。
- CF 凭证集中在 `cloudflare_config.json`，部署脚本会自动读取（缺失时回退到脚本内硬编码默认值）。