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
#kg-flash{position:fixed;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:99996;opacity:0;background:radial-gradient(circle at 88% 90%, #fff8e1 0%, #ffd54f 18%, #ff7043 40%, transparent 65%);}
#kg-flash.kg-on{animation:kg-flash-in .7s ease-out forwards;}
@keyframes kg-flash-in{0%{opacity:0;}12%{opacity:1;}100%{opacity:0;}}
#kg-eggy .kg-smoke{opacity:0;transition:opacity .4s;}
#kg-eggy .kg-dirt{opacity:0;transition:opacity .3s;}
#kg-eggy .kg-hat{transition:opacity .3s, transform .3s;}
#kg-eggy .kg-leg{transition:fill .3s;}
#kg-eggy.kg-blasted .kg-smoke{opacity:1;}
#kg-eggy.kg-blasted .kg-egg-body{fill:#3f3f3f !important;stroke:#27272a !important;}
#kg-eggy.kg-blasted .kg-dirt{opacity:.85;}
#kg-eggy.kg-blasted .kg-hat{opacity:.35;transform:translateY(-6px) rotate(-8deg);}
#kg-eggy.kg-blasted .kg-leg{fill:#27272a !important;}
@keyframes kg-fly{0%{transform:translateY(0);}45%{transform:translateY(-26px);}100%{transform:translateY(12px);opacity:0;}}
#kg-eggy.kg-blasted{animation:kg-fly .5s ease-in;}
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
  var clickCount=0;
  function fireExplosion(){
    var flash=document.getElementById('kg-flash');
    if(!flash){flash=document.createElement('div');flash.id='kg-flash';document.body.appendChild(flash);}
    flash.classList.remove('kg-on');void flash.offsetWidth;flash.classList.add('kg-on');
    setTimeout(function(){flash.classList.remove('kg-on');},750);
    var box=document.getElementById('kg-confetti');
    if(!box){box=document.createElement('div');box.id='kg-confetti';document.body.appendChild(box);}
    var cx=window.innerWidth-55, cy=window.innerHeight-50;
    function blob(){
      var p=document.createElement('div');p.className='kg-cf';
      var roll=Math.random();
      if(roll<0.62){p.style.background=['#fb923c','#f97316','#ef4444','#fde047','#ffedd5','#fbbf24'][Math.floor(Math.random()*6)];p.style.width='10px';p.style.height='10px';p.style.boxShadow='0 0 12px rgba(249,115,22,.9),0 0 24px rgba(255,176,0,.6)';}
      else if(roll<0.85){p.style.background=['#fca5a5','#fed7aa','#fde68a'][Math.floor(Math.random()*3)];p.style.width=Math.random()<0.5?'6px':'9px';p.style.height='3px';p.style.borderRadius='2px';}
      else {p.style.background='#57534e';p.style.width='16px';p.style.height='16px';p.style.boxShadow='0 0 10px rgba(87,83,78,.5)';}
      p.style.left=cx+'px';p.style.top=cy+'px';
      var ang=Math.random()*Math.PI*2, sp=90+Math.random()*240;
      var dx=Math.cos(ang)*sp, dy=Math.sin(ang)*sp-70;
      p.style.transition='transform 1.4s cubic-bezier(.15,.55,.3,1),opacity 1.4s ease';
      box.appendChild(p);
      requestAnimationFrame(function(el,xx,yy){return function(){
        el.style.opacity='1';el.style.transform='translate('+xx+'px,'+yy+'px) scale('+(0.6+Math.random()*1.1)+') rotate('+(Math.random()*540)+'deg)';
      };}(p,dx,dy));
      setTimeout(function(el){return function(){el.style.opacity='0';};}(p),500+Math.random()*700);
    }
    for(var i=0;i<110;i++) blob();
    setTimeout(function(){if(box.parentNode)box.parentNode.removeChild(box);},1700);
    eggy.classList.add('kg-blasted');
    pl.setAttribute('r','2.8');pr.setAttribute('r','2.8');
    pl.setAttribute('cy','67');pr.setAttribute('cy','67');
    eyeL.setAttribute('r','12.5');eyeR.setAttribute('r','12.5');
    eyeL.setAttribute('cx','35');eyeR.setAttribute('cx','65');
    mouth.setAttribute('d','M44 84 Q50 91 56 84');
    eggy.style.filter='brightness(.85) saturate(.6)';
    setTimeout(function(){
      eggy.classList.remove('kg-blasted');
      pl.setAttribute('r','5.5');pr.setAttribute('r','5.5');
      pl.setAttribute('cy','68');pr.setAttribute('cy','68');
      eyeL.setAttribute('r','11');eyeR.setAttribute('r','11');
      eyeL.setAttribute('cx','36');eyeR.setAttribute('cx','64');
      mouth.setAttribute('d',faces[fi][1]);
      eggy.style.filter='';
    },3500);
  }
  var eyeL=document.getElementById('kg-eye-l'), eyeR=document.getElementById('kg-eye-r');
  eggy.addEventListener('click',function(){fi=(fi+1)%faces.length;body.setAttribute('fill',faces[fi][0]);mouth.setAttribute('d',faces[fi][1]);eggy.classList.remove('kg-bounce');void eggy.offsetWidth;eggy.classList.add('kg-bounce');clickCount++;if(clickCount>=30){clickCount=0;fireExplosion();}});
})();
</script>"""

EGGY_HTML = """<!-- kg-eggy-start -->
<div id="kg-eggy" title="点我玩！连点30次有惊喜……">
  <svg width="70" height="84" viewBox="0 0 100 120">
    <ellipse class="kg-hat" cx="50" cy="30" rx="26" ry="18" fill="#0ea5e9" stroke="#0284c7" stroke-width="2"/>
    <path class="kg-hat" d="M20 30 Q50 22 80 30 L74 34 Q50 28 26 34 Z" fill="#0284c7"/>
    <ellipse class="kg-hat" cx="50" cy="30" rx="42" ry="6" fill="#0ea5e9" opacity=".9"/>
    <ellipse class="kg-hat" cx="50" cy="28" rx="26" ry="16" fill="#38bdf8" opacity=".4"/>
    <circle class="kg-hat" cx="50" cy="12" r="5" fill="#fbbf24" stroke="#f59e0b" stroke-width="1.5"/>
    <ellipse class="kg-egg-body" cx="50" cy="74" rx="40" ry="42" fill="#fde047" stroke="#0ea5e9" stroke-width="3.5"/>
    <ellipse cx="36" cy="50" rx="12" ry="8" fill="#fef9c3" opacity=".6"/>
    <g id="kg-eggy-eyes">
      <circle id="kg-eye-l" cx="36" cy="66" r="11" fill="#fff" stroke="#0284c7" stroke-width="2.5"/>
      <circle id="kg-eye-r" cx="64" cy="66" r="11" fill="#fff" stroke="#0284c7" stroke-width="2.5"/>
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
    <rect class="kg-leg" x="37" y="106" width="7" height="8" fill="#fde047"/>
    <rect class="kg-leg" x="56" y="106" width="7" height="8" fill="#fde047"/>
    <rect x="34" y="112" width="13" height="8" rx="3" fill="#1e293b"/>
    <rect x="53" y="112" width="13" height="8" rx="3" fill="#1e293b"/>
    <g class="kg-dirt"><circle cx="26" cy="72" r="5" fill="#292524" opacity=".8"/><circle cx="46" cy="82" r="4" fill="#292524" opacity=".7"/><circle cx="64" cy="80" r="5.5" fill="#292524" opacity=".75"/><circle cx="33" cy="88" r="3.5" fill="#292524" opacity=".6"/><circle cx="72" cy="70" r="4" fill="#292524" opacity=".65"/></g>
    <g class="kg-smoke"><circle cx="50" cy="12" r="7" fill="#9ca3af" opacity=".5"/><circle cx="62" cy="6" r="5" fill="#9ca3af" opacity=".35"/><circle cx="40" cy="4" r="4" fill="#9ca3af" opacity=".3"/></g>
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
