"""
全局导航栏注入脚本

给 public/ 下所有教程页面注入一个固定顶栏，方便随时返回主页或切换主题。
可重复运行：再次执行会先清除旧注入再重新注入。

用法：python3 core/inject_nav.py
"""

import re
from pathlib import Path

PUBLIC_DIR = Path(__file__).parent.parent / "public"

# 页面 → 所属主题（dfs / tree / p11962 / cbt）
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
    "gesp6-cbt-counter.html": "cbt",
    "cbt-counter-tutorial.html": "cbt",
    "cbt-counter/index.html": "cbt",
}

TOPIC_LABELS = {
    "dfs": ("① DFS/BFS", "topic-dfs"),
    "tree": ("② 树基础", "topic-tree"),
    "p11962": ("③ 树上漫步", "topic-p11962"),
    "cbt": ("④ 完全二叉树", "topic-cbt"),
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
#kg-eggy{position:fixed;right:20px;bottom:20px;width:70px;height:84px;z-index:99998;cursor:pointer;transition:transform .3s cubic-bezier(.34,1.56,.64,1);user-select:none;}
#kg-eggy.kg-bounce{animation:kg-eggy-bounce .5s ease;}
@keyframes kg-eggy-bounce{0%{transform:translateY(0) scale(1);}40%{transform:translateY(-18px) scale(1.08,.92);}70%{transform:translateY(0) scale(.95,1.05);}100%{transform:translateY(0) scale(1);}}
#kg-eggy:hover{transform:scale(1.06);}
#kg-eggy .kg-egg-body{transition:fill .3s;}
#kg-confetti{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:99997;overflow:hidden;}
.kg-cf{position:absolute;width:8px;height:8px;border-radius:50%;opacity:0;}
</style>"""


def build_nav_html(current_topic: str, home_path: str) -> str:
    topics_html = ""
    for key, (label, anchor) in TOPIC_LABELS.items():
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
  var faces=[["#fde047","M42 84 Q50 90 58 84"],["#fca5a5","M42 86 Q50 80 58 86"],["#86efac","M42 82 Q50 92 58 82"],["#93c5fd","M42 88 Q50 84 58 88"]];
  var fi=0;
  function mp(p,cx,cy,mx,my){var r=eggy.getBoundingClientRect();var dx=mx-(r.left+cx*0.7+35),dy=my-(r.top+cy*0.7+42);var d=Math.sqrt(dx*dx+dy*dy)||1,max=4;p.setAttribute('cx',cx+Math.min(max,dx/d*max));p.setAttribute('cy',cy+Math.min(max,dy/d*max));}
  document.addEventListener('mousemove',function(e){mp(pl,36,68,e.clientX,e.clientY);mp(pr,64,68,e.clientX,e.clientY);});
  document.addEventListener('touchmove',function(e){if(e.touches[0]){mp(pl,36,68,e.touches[0].clientX,e.touches[0].clientY);mp(pr,64,68,e.touches[0].clientX,e.touches[0].clientY);}},{passive:true});
  eggy.addEventListener('click',function(){fi=(fi+1)%faces.length;body.setAttribute('fill',faces[fi][0]);mouth.setAttribute('d',faces[fi][1]);eggy.classList.remove('kg-bounce');void eggy.offsetWidth;eggy.classList.add('kg-bounce');clickCount++;if(clickCount>=10){clickCount=0;fireConfetti();}});
  var clickCount=0;
  function fireConfetti(){var box=document.getElementById('kg-confetti')||document.createElement('div');box.id='kg-confetti';document.body.appendChild(box);var colors=['#0ea5e9','#fde047','#fb7185','#86efac','#fbbf24','#a78bfa','#f97316','#38bdf8'];var cx=window.innerWidth-55,cy=window.innerHeight-50;for(var i=0;i<60;i++){var p=document.createElement('div');p.className='kg-cf';p.style.background=colors[i%colors.length];p.style.left=cx+'px';p.style.top=cy+'px';var ang=Math.random()*Math.PI*2,sp=60+Math.random()*120;var dx=Math.cos(ang)*sp,dy=Math.sin(ang)*sp-80;p.style.transition='transform 1.2s cubic-bezier(.2,.6,.4,1),opacity 1.2s ease';box.appendChild(p);requestAnimationFrame(function(el,xx,yy){return function(){el.style.opacity='1';el.style.transform='translate('+xx+'px,'+yy+'px) scale('+(0.5+Math.random())+') rotate('+(Math.random()*720)+'deg)';};}(p,dx,dy));setTimeout(function(el){return function(){el.style.opacity='0';};}(p),900);}setTimeout(function(){if(box.parentNode)box.parentNode.removeChild(box);},1400);}
})();
</script>"""

EGGY_HTML = """<!-- kg-eggy-start -->
<div id="kg-eggy" title="点我玩！连点10次有彩蛋">
  <svg width="70" height="84" viewBox="0 0 100 120">
    <ellipse cx="50" cy="30" rx="26" ry="18" fill="#0ea5e9" stroke="#0284c7" stroke-width="2"/>
    <path d="M20 30 Q50 22 80 30 L74 34 Q50 28 26 34 Z" fill="#0284c7"/>
    <ellipse cx="50" cy="30" rx="42" ry="6" fill="#0ea5e9" opacity=".9"/>
    <ellipse cx="50" cy="28" rx="26" ry="16" fill="#38bdf8" opacity=".4"/>
    <circle cx="50" cy="12" r="5" fill="#fbbf24" stroke="#f59e0b" stroke-width="1.5"/>
    <ellipse class="kg-egg-body" cx="50" cy="74" rx="40" ry="42" fill="#fde047" stroke="#0ea5e9" stroke-width="3.5"/>
    <ellipse cx="36" cy="50" rx="12" ry="8" fill="#fef9c3" opacity=".6"/>
    <g id="kg-eggy-eyes">
      <circle cx="36" cy="66" r="11" fill="#fff" stroke="#0284c7" stroke-width="2.5"/>
      <circle cx="64" cy="66" r="11" fill="#fff" stroke="#0284c7" stroke-width="2.5"/>
      <circle id="kg-pupil-l" cx="36" cy="68" r="5.5" fill="#1e293b"/>
      <circle id="kg-pupil-r" cx="64" cy="68" r="5.5" fill="#1e293b"/>
      <circle cx="38" cy="65" r="2" fill="#fff"/>
      <circle cx="66" cy="65" r="2" fill="#fff"/>
    </g>
    <path d="M28 60 Q26 54 24 56" stroke="#1e293b" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    <path d="M33 58 Q33 52 35 53" stroke="#1e293b" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    <path d="M67 58 Q67 52 65 53" stroke="#1e293b" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    <path d="M72 60 Q74 54 76 56" stroke="#1e293b" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    <circle cx="22" cy="76" r="5.5" fill="#fb7185" opacity=".55"/>
    <circle cx="78" cy="76" r="5.5" fill="#fb7185" opacity=".55"/>
    <path id="kg-eggy-mouth" d="M42 84 Q50 90 58 84" stroke="#1e293b" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <rect x="37" y="106" width="7" height="8" fill="#fde047"/>
    <rect x="56" y="106" width="7" height="8" fill="#fde047"/>
    <rect x="34" y="112" width="13" height="8" rx="3" fill="#1e293b"/>
    <rect x="53" y="112" width="13" height="8" rx="3" fill="#1e293b"/>
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
