# kids-pages · 孩子数学/算法互动学习页托管

一个独立的静态 HTML 托管项目，把为孩子准备的图文/互动算法教程（GESP 六级系列）
部署到 **Cloudflare Pages** 公网上，方便随时分享给孩子用手机/平板打开。

方案沿用 ad-newsletter 的成熟托管方式：
本地 `public/` 目录 → `wrangler pages deploy` → 固定公网域名 `https://kids-pages-1pw.pages.dev/...`。

> ⚠️ 注意：Cloudflare Pages 为项目分配的子域名实际为 **`kids-pages-1pw.pages.dev`**。若日后绑定自定义域名，按需替换下方所有链接。

## 目录结构

```
kids-pages/
├── public/                      # Cloudflare Pages 构建输出目录（唯一上线的根）
│   ├── index.html              # 首页导航（列出所有教程入口）
│   ├── gesp6-p11962-tutorial.html  # P11962 树上漫步 · 图文动画（千问）
│   ├── gesp6-dfs-bfs.html          # 深搜广搜通关站（千问）
│   ├── p11962-tree-walk.html       # P11962 树上漫步 · 互动教学（WorkBuddy）
│   ├── dsfs-bfs-walkthrough.html   # DFS/BFS 走查教程（WorkBuddy）
│   ├── dfs-bfs/                    # DFS/BFS 互动教程（TRAE，含 JS+字体依赖）
│   └── tree-stroll/                # 树上漫步互动教程（TRAE，含 JS+字体依赖）
├── sources/                     # 各 agent 产出的原始 HTML（按来源归档，不做整理/改名）
│   ├── qwen/                    #      千问 原始产出
│   ├── workbuddy/               #      WorkBuddy 原始产出
│   └── trae/                    #      TRAE 原始产出（完整包）
├── core/deploy_cf_pages.py     # CF Pages 部署脚本（回车一次全量部署）
├── wrangler.toml               # wrangler 配置（pages_build_output_dir="public"）
├── cloudflare_config.json      # CF API Token / Account ID / 项目名（已被 .gitignore 排除）
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
- DFS/BFS 互动版（TRAE）：`https://kids-pages-1pw.pages.dev/dfs-bfs/`
- 树上漫步互动版（TRAE）：`https://kids-pages-1pw.pages.dev/tree-stroll/`

## 内容来源

发布到 `public/` 的页面，原始产出统一归档在 `sources/`（按 agent 分子文件夹，保留原始文件名与结构）。

| public 页面 | 来源 agent | sources/ 归档 |
|------|---------|---------|
| gesp6-p11962-tutorial.html | 千问 | `sources/qwen/GESP六级-P11962树上漫步.html` |
| gesp6-dfs-bfs.html | 千问 | `sources/qwen/GESP六级-深搜广搜通关站.html` |
| p11962-tree-walk.html | WorkBuddy | `sources/workbuddy/p11962_tutorial.html` |
| dsfs-bfs-walkthrough.html | WorkBuddy | `sources/workbuddy/dfs_bfs_tutorial.html` |
| dfs-bfs/ | TRAE | `sources/trae/dfs-bfs-tutorial/`（完整包） |
| tree-stroll/ | TRAE | `sources/trae/tree-stroll/`（完整包） |

## 维护笔记

- `public/` 是唯一上线根目录。新增页面直接放 `public/` 下，重跑部署脚本即可。
- `sources/` 是各 agent 原始产出的备份区，保持原样留存，方便日后对比或重新整理；发布版如有定制改名，改动都在 `public/` 进行。
- `tree-stroll/` 与 `dfs-bfs/` 用了相对路径引用 `assets/tutorial.js` 与 `_shared/fonts`，需整目录一起拷贝，勿单独拆文件。
- CF 凭证由 `cloudflare_config.json` 或环境变量 `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` 提供；**严禁把 Token 硬编码进代码**（GitHub secret scanning 会拦截，且 public 仓库会泄露）。