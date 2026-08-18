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
#kg-nav .kg-home{color:#0284c7;font-weight:700;text-decoration:none;font-size:15px;white-space:nowrap;}
#kg-nav .kg-topics{display:flex;gap:6px;}
#kg-nav .kg-topics a{color:#475569;text-decoration:none;padding:4px 10px;border-radius:999px;font-size:12px;white-space:nowrap;transition:background .15s,color .15s;}
#kg-nav .kg-topics a:hover{background:#e0f2fe;color:#0284c7;}
#kg-nav .kg-topics a.kg-active{background:#0ea5e9;color:#fff;}
body{padding-top:46px;}
@media(max-width:520px){#kg-nav .kg-home{font-size:13px;}#kg-nav .kg-topics a{padding:3px 7px;font-size:11px;}}
#kg-eggy{position:fixed;right:20px;bottom:20px;width:64px;height:72px;z-index:99998;cursor:pointer;transition:transform .3s cubic-bezier(.34,1.56,.64,1);user-select:none;}
#kg-eggy.kg-bounce{animation:kg-eggy-bounce .5s ease;}
@keyframes kg-eggy-bounce{0%{transform:translateY(0) scale(1);}40%{transform:translateY(-18px) scale(1.08,.92);}70%{transform:translateY(0) scale(.95,1.05);}100%{transform:translateY(0) scale(1);}}
#kg-eggy:hover{transform:scale(1.06);}
#kg-eggy .kg-egg-body{transition:fill .3s;}
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
        f'  <a class="kg-home" href="{home_path}">秘密基地</a>\n'
        f'  <div class="kg-topics">{topics_html}</div>\n'
        "</nav>\n"
        "<!-- kg-nav-end -->"
    )


EGGY_JS = """<script>
(function(){
  var eggy=document.getElementById('kg-eggy');
  if(!eggy) return;
  var pl=document.getElementById('kg-pupil-l');
  var pr=document.getElementById('kg-pupil-r');
  var mouth=document.getElementById('kg-eggy-mouth');
  var body=eggy.querySelector('.kg-egg-body');
  var faces=[["#fde047","M24 48 Q32 54 40 48"],["#fca5a5","M24 50 Q32 44 40 50"],["#86efac","M24 47 Q32 56 40 47"],["#93c5fd","M24 52 Q32 48 40 52"]];
  var fi=0;
  function mp(p,cx,cy,mx,my){var r=eggy.getBoundingClientRect();var dx=mx-(r.left+cx+32),dy=my-(r.top+cy+40);var d=Math.sqrt(dx*dx+dy*dy)||1,max=2.5;p.setAttribute('cx',cx+Math.min(max,dx/d*max));p.setAttribute('cy',cy+Math.min(max,dy/d*max));}
  document.addEventListener('mousemove',function(e){mp(pl,24,36,e.clientX,e.clientY);mp(pr,42,36,e.clientX,e.clientY);});
  document.addEventListener('touchmove',function(e){if(e.touches[0]){mp(pl,24,36,e.touches[0].clientX,e.touches[0].clientY);mp(pr,42,36,e.touches[0].clientX,e.touches[0].clientY);}},{passive:true});
  eggy.addEventListener('click',function(){fi=(fi+1)%faces.length;body.setAttribute('fill',faces[fi][0]);mouth.setAttribute('d',faces[fi][1]);eggy.classList.remove('kg-bounce');void eggy.offsetWidth;eggy.classList.add('kg-bounce');});
})();
</script>"""

EGGY_HTML = """<!-- kg-eggy-start -->
<div id="kg-eggy" title="点我玩！">
  <svg width="64" height="72" viewBox="0 0 64 72">
    <ellipse class="kg-egg-body" cx="32" cy="40" rx="28" ry="30" fill="#fde047" stroke="#0ea5e9" stroke-width="3"/>
    <g id="kg-eggy-eyes">
      <circle cx="24" cy="36" r="6" fill="#fff"/><circle cx="42" cy="36" r="6" fill="#fff"/>
      <circle id="kg-pupil-l" cx="24" cy="36" r="3" fill="#1e293b"/>
      <circle id="kg-pupil-r" cx="42" cy="36" r="3" fill="#1e293b"/>
    </g>
    <path id="kg-eggy-mouth" d="M24 48 Q32 54 40 48" stroke="#1e293b" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <circle cx="18" cy="44" r="3" fill="#fb7185" opacity=".5"/>
    <circle cx="48" cy="44" r="3" fill="#fb7185" opacity=".5"/>
  </svg>
</div>
<!-- kg-eggy-end -->"""


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
    # 清除旧注入的蛋仔 HTML
    html = re.sub(r"<!-- kg-eggy-start -->.*?<!-- kg-eggy-end -->", "", html, flags=re.S)
    # 清除旧注入的蛋仔 JS
    html = re.sub(r"<!-- kg-eggy-js-start -->.*?<!-- kg-eggy-js-end -->", "", html, flags=re.S)

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

    # 注入互动蛋仔 HTML+JS 到 </body> 前
    eggy_block = EGGY_HTML + "\n" + "<!-- kg-eggy-js-start -->\n" + EGGY_JS + "\n<!-- kg-eggy-js-end -->"
    if "</body>" in html:
        html = html.replace("</body>", eggy_block + "\n</body>", 1)
    else:
        print(f"  ⚠ 无 </body>，跳过蛋仔注入: {rel_path}")

    fpath.write_text(html, encoding="utf-8")
    print(f"  ✔ 注入完成: {rel_path} (主题={topic}, home={home})")


def main():
    print("=== 注入全局导航栏 ===")
    for rel_path, topic in PAGES.items():
        inject_page(rel_path, topic)
    print("=== 完成 ===")


if __name__ == "__main__":
    main()
