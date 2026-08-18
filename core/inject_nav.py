"""
全局导航栏注入脚本

给 public/ 下所有教程页面注入一个固定顶栏，方便随时返回主页或切换主题。
可重复运行：再次执行会先清除旧注入再重新注入。

用法：python3 core/inject_nav.py
"""

import re
from pathlib import Path

PUBLIC_DIR = Path(__file__).parent.parent / "public"

# 页面 → 所属主题（dfs / tree / p11962）
PAGES = {
    "gesp6-dfs-bfs.html": "dfs",
    "dsfs-bfs-walkthrough.html": "dfs",
    "dfs-bfs/index.html": "dfs",
    "gesp6-tree-intro.html": "tree",
    "gesp6-tree-basics.html": "tree",
    "tree-basics/index.html": "tree",
    "gesp6-p11962-tutorial.html": "p11962",
    "p11962-tree-walk.html": "p11962",
    "tree-stroll/index.html": "p11962",
}

TOPIC_LABELS = {
    "dfs": ("① DFS/BFS", "topic-dfs"),
    "tree": ("② 树基础", "topic-tree"),
    "p11962": ("③ 树上漫步", "topic-p11962"),
}

NAV_CSS = """<style id="kg-nav-style">
#kg-nav{position:fixed;top:0;left:0;right:0;z-index:99999;background:#fff;box-shadow:0 1px 6px rgba(0,0,0,.12);display:flex;align-items:center;justify-content:space-between;padding:0 14px;height:46px;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;font-size:14px;box-sizing:border-box;}
#kg-nav .kg-home{color:#6d28d9;font-weight:700;text-decoration:none;font-size:15px;white-space:nowrap;}
#kg-nav .kg-topics{display:flex;gap:6px;}
#kg-nav .kg-topics a{color:#475569;text-decoration:none;padding:4px 10px;border-radius:999px;font-size:12px;white-space:nowrap;transition:background .15s,color .15s;}
#kg-nav .kg-topics a:hover{background:#ede9fe;color:#6d28d9;}
#kg-nav .kg-topics a.kg-active{background:#7c3aed;color:#fff;}
body{padding-top:46px;}
@media(max-width:520px){#kg-nav .kg-home{font-size:13px;}#kg-nav .kg-topics a{padding:3px 7px;font-size:11px;}}
</style>"""


def build_nav_html(current_topic: str, home_path: str) -> str:
    topics_html = ""
    for key, (label, anchor) in [
        ("dfs", TOPIC_LABELS["dfs"]),
        ("tree", TOPIC_LABELS["tree"]),
        ("p11962", TOPIC_LABELS["p11962"]),
    ]:
        active = ' class="kg-active"' if key == current_topic else ""
        topics_html += f'<a href="{home_path}#{anchor}"{active}>{label}</a>'
    return (
        "<!-- kg-nav-start -->\n"
        '<nav id="kg-nav">\n'
        f'  <a class="kg-home" href="{home_path}">🌸 秘密花园</a>\n'
        f'  <div class="kg-topics">{topics_html}</div>\n'
        "</nav>\n"
        "<!-- kg-nav-end -->"
    )


def inject_page(rel_path: str, topic: str):
    fpath = PUBLIC_DIR / rel_path
    if not fpath.exists():
        print(f"  ✘ 缺失: {rel_path}")
        return
    # 子目录页面回首页用 ../，根目录用 ./
    depth = rel_path.count("/")
    home = "../" * depth + "index.html" if depth > 0 else "index.html"

    html = fpath.read_text(encoding="utf-8")

    # 清除旧注入的 CSS
    html = re.sub(r'<style id="kg-nav-style">.*?</style>', "", html, flags=re.S)
    # 清除旧注入的导航栏
    html = re.sub(r"<!-- kg-nav-start -->.*?<!-- kg-nav-end -->", "", html, flags=re.S)

    # 注入 CSS 到 </head> 前
    if "</head>" in html:
        html = html.replace("</head>", NAV_CSS + "\n</head>", 1)
    else:
        print(f"  ⚠ 无 </head>，跳过 CSS 注入: {rel_path}")

    # 注入导航栏 HTML 到 <body ...> 后
    nav_html = build_nav_html(topic, home)
    m = re.search(r"<body[^>]*>", html)
    if m:
        pos = m.end()
        html = html[:pos] + "\n" + nav_html + "\n" + html[pos:]
    else:
        print(f"  ⚠ 无 <body> 标签，跳过导航栏注入: {rel_path}")

    fpath.write_text(html, encoding="utf-8")
    print(f"  ✔ 注入完成: {rel_path} (主题={topic}, home={home})")


def main():
    print("=== 注入全局导航栏 ===")
    for rel_path, topic in PAGES.items():
        inject_page(rel_path, topic)
    print("=== 完成 ===")


if __name__ == "__main__":
    main()
