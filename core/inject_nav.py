"""
全局导航栏注入脚本

给 public/ 下所有教程页面注入一个固定顶栏，方便随时返回主页或切换主题。
可重复运行：再次执行会先清除旧注入再重新注入。

用法：python3 core/inject_nav.py
"""

import re
from pathlib import Path

PUBLIC_DIR = Path(__file__).parent.parent / "public"

# 当前正在注入的页面（build_sidebar_html 高亮用）
CURRENT_PAGE = ""

# 页面 → 所属主题（dfs / tree / p11962 / cbt / full）
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
    "gesp6-full-tree-counter.html": "full",
    "digital-literacy.html": "digital",
    "digital-practice.html": "digital",
    "python-fun-competition.html": "python-fun",
}

TOPIC_LABELS = {
    "dfs": ("① DFS/BFS", "topic-dfs"),
    "tree": ("② 树基础", "topic-tree"),
    "p11962": ("③ 树上漫步", "topic-p11962"),
    "cbt": ("④ 完全二叉树", "topic-cbt"),
    "full": ("⑤ 满二叉树", "topic-full"),
    "digital": ("⑥ 数智素养", "digital-literacy.html"),
    "python-fun": ("3.2 python趣味编程 2026", "topic-python-fun"),
}

# 每个页面在侧边栏里显示的名字（短名）
PAGE_SHORT_NAMES = {
    "gesp6-dfs-bfs.html": "千问 · 深搜广搜通关站",
    "dsfs-bfs-walkthrough.html": "WorkBuddy · 深搜广搜",
    "dfs-bfs/index.html": "TRAE · 深搜广搜互动",
    "gesp6-tree-intro.html": "千问 · 树入门",
    "gesp6-tree-basics.html": "WorkBuddy · 树基础",
    "tree-basics/index.html": "TRAE · 树基础互动",
    "gesp6-p11962-tutorial.html": "千问 · 树上漫步",
    "p11962-tree-walk.html": "WorkBuddy · 树上漫步",
    "tree-stroll/index.html": "TRAE · 树上漫步互动",
    "gesp6-cbt-counter.html": "千问 · 完全二叉计数",
    "cbt-counter-tutorial.html": "WorkBuddy · 完全二叉计数",
    "cbt-counter/index.html": "TRAE · 完全二叉计数互动",
    "gesp6-full-tree-counter.html": "千问 · 满二叉子树计数",
    "digital-literacy.html": "数智素养 · 考试准备",
    "digital-practice.html": "数智素养 · 练习库",
    "python-fun-competition.html": "python趣味编程 2026",
}

NAV_CSS = """<style id="kg-nav-style">
#kg-nav{position:fixed;top:0;left:0;right:0;z-index:99999;background:#fff;box-shadow:0 1px 6px rgba(0,0,0,.12);display:flex;align-items:center;justify-content:space-between;padding:0 14px;height:46px;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;font-size:14px;box-sizing:border-box;}
#kg-nav .kg-home{color:#0284c7;font-weight:700;text-decoration:none;font-size:15px;white-space:nowrap;}
#kg-nav.kg-nav-standalone{justify-content:flex-start;gap:16px;}
#kg-nav.kg-nav-standalone~#kg-sidebar{display:none;}
#kg-nav .kg-back{color:#475569;text-decoration:none;padding:4px 10px;border-radius:999px;font-size:12px;white-space:nowrap;}
#kg-nav .kg-back:hover{background:#e0f2fe;color:#0284c7;}
#kg-nav .kg-topics{display:flex;gap:6px;}
#kg-nav .kg-topics a{color:#475569;text-decoration:none;padding:4px 10px;border-radius:999px;font-size:12px;white-space:nowrap;transition:background .15s,color .15s;}
#kg-nav .kg-topics a:hover{background:#e0f2fe;color:#0284c7;}
#kg-nav .kg-topics a.kg-active{background:#0ea5e9;color:#fff;}
body{padding-top:46px;}
@media(max-width:520px){#kg-nav .kg-home{font-size:13px;}#kg-nav .kg-topics a{padding:3px 7px;font-size:11px;}}

/* 左侧目录：默认收起，悬停把手/移入滑出 */
#kg-sidebar{position:fixed;left:0;top:46px;bottom:0;width:248px;background:#f8faff;border-right:1px solid #dce6f1;box-shadow:8px 0 28px rgba(32,48,71,.12);z-index:99990;overflow-y:auto;padding:30px 12px 28px;box-sizing:border-box;font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;transform:translateX(-102%);transition:transform .24s cubic-bezier(.2,.7,.25,1);}
body.kg-sb-open #kg-sidebar{transform:translateX(0);}
#kg-sidebar::-webkit-scrollbar{width:6px;}
#kg-sidebar::-webkit-scrollbar-thumb{background:#bae6fd;border-radius:3px;}
#kg-sidebar .kg-sb-home{display:block;font-weight:800;font-size:14px;color:#3147b9;text-decoration:none;padding:9px 11px;border-radius:11px;background:#eaf0ff;margin-bottom:12px;transition:background .15s,transform .15s;}
#kg-sidebar .kg-sb-home:hover{background:#dfe7ff;transform:translateY(-1px);}
#kg-sidebar .kg-sb-topic{font-weight:800;font-size:12px;color:#50617a;padding:13px 10px 5px;letter-spacing:.02em;}
#kg-sidebar a.kg-sb-page{display:block;font-size:13px;color:#35445b;text-decoration:none;padding:7px 10px;border-radius:8px;margin:2px 0;line-height:1.45;transition:background .15s,color .15s;}
#kg-sidebar a.kg-sb-page:hover{background:#edf1ff;color:#344bc2;}
#kg-sidebar a.kg-sb-page.kg-sb-active{background:#4263eb;color:#fff;font-weight:700;box-shadow:0 3px 10px #4263eb33;}
#kg-sidebar a:focus-visible,#kg-sidebar button:focus-visible,#kg-sb-toggle:focus-visible{outline:3px solid #f0a323;outline-offset:2px;}
/* ✕ 收起按钮 */
#kg-sidebar #kg-sb-x{position:sticky;top:0;float:right;margin:-24px 0 0;width:22px;height:22px;border:none;border-radius:6px;background:#e0f2fe;color:#0369a1;font-size:12px;line-height:1;cursor:pointer;z-index:2;}
#kg-sidebar #kg-sb-x:hover{background:#fecaca;color:#b91c1c;}
/* ☰ 展开把手：收起时留在左缘 */
#kg-sb-toggle{position:fixed;left:0;top:46px;bottom:0;width:20px;z-index:99989;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;background:transparent;}
#kg-sb-toggle .kg-sb-tg-ic{display:block;writing-mode:vertical-rl;font-size:14px;color:#4058d8;background:rgba(255,255,255,.94);padding:10px 4px;border:1px solid #dce6f1;border-left:0;border-radius:0 9px 9px 0;box-shadow:0 3px 12px rgba(32,48,71,.14);transition:background .15s,color .15s;}
#kg-sb-toggle:hover .kg-sb-tg-ic{background:#4263eb;color:#fff;}
/* 半透明遮罩：展开时盖在内容上，点击可收起 */
.kg-sb-mask{position:fixed;left:0;top:46px;right:0;bottom:0;background:rgba(15,23,42,.25);z-index:99988;opacity:0;pointer-events:none;transition:opacity .26s;}
body.kg-sb-open .kg-sb-mask{opacity:1;pointer-events:auto;}
/* 内容永远不左右移动：padding 固定，sidebar 覆盖在内容上方 */
body{padding-left:24px;}
@media(max-width:860px){#kg-sidebar{display:none;}#kg-sb-toggle{display:none;}.kg-sb-mask{display:none;}body{padding-left:0!important;}}
</style>"""

EGGY_CSS = """<style id="kg-eggy-style">
#kg-eggy{position:fixed;right:20px;bottom:20px;width:70px;height:84px;z-index:99998;cursor:pointer;transition:transform .3s cubic-bezier(.34,1.56,.64,1);user-select:none;display:block!important;visibility:visible!important;opacity:1!important;}
@media(max-width:860px){#kg-eggy{display:block!important;visibility:visible!important;opacity:1!important;right:12px;bottom:12px;width:56px;height:68px;}#kg-eggy svg{width:56px;height:68px;}}
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
#kg-eggy .kg-tear{opacity:0;transform-box:fill-box;transform-origin:center;}
#kg-eggy.kg-crying .kg-tear{opacity:.9;animation:kg-tear-wobble .62s ease-in-out infinite alternate;}
@keyframes kg-tear-wobble{from{transform:translateY(-1px);}to{transform:translateY(3px);}}
#kg-eggy.kg-blasted .kg-smoke{opacity:1;}
#kg-eggy.kg-blasted .kg-egg-body{fill:#3f3f3f !important;stroke:#27272a !important;}
#kg-eggy.kg-blasted .kg-dirt{opacity:.85;}
#kg-eggy.kg-blasted .kg-hat{opacity:.35;transform:translateY(-6px) rotate(-8deg);}
#kg-eggy.kg-blasted .kg-leg{fill:#27272a !important;}
@keyframes kg-fly{0%{transform:translateY(0);}45%{transform:translateY(-26px);}100%{transform:translateY(12px);opacity:0;}}
#kg-eggy.kg-blasted{animation:kg-fly .5s ease-in;}
/* 蛋仔拖动 + 右下角隐形栅栏 */
#kg-eggy{cursor:grab;touch-action:none;}
#kg-eggy.kg-dragging{cursor:grabbing;transition:none!important;}
#kg-eggy.kg-flying{pointer-events:none;transition:none!important;filter:drop-shadow(0 0 12px #38bdf8);}
#kg-eggy.kg-fallen{transform-origin:50% 100%;}
#kg-spring{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:99997;overflow:hidden;}
#kg-spring path{fill:none;stroke-linecap:round;filter:drop-shadow(0 0 7px #22d3ee) drop-shadow(0 0 14px #a78bfa);}
#kg-spring text{font:600 12px sans-serif;fill:#0369a1;stroke:white;stroke-width:3px;paint-order:stroke;}
@keyframes kg-wall-shake{0%{transform:translateX(0);}30%{transform:translateX(-3px);}60%{transform:translateX(2.5px);}100%{transform:translateX(0);}}
#kg-eggy svg.kg-wall-shake{animation:kg-wall-shake .22s ease;}
#kg-dustbox{position:fixed;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:99996;overflow:hidden;}
.kg-dust{position:absolute;width:6px;height:6px;border-radius:50%;background:#cbd5e1;box-shadow:0 0 5px rgba(148,163,184,.9);opacity:0;transition:transform .55s ease-out,opacity .55s ease-out;}
</style>"""


def build_nav_html(current_topic: str, home_path: str) -> str:
    if current_topic == "digital":
        # This is a standalone long-form topic. Keep its authored sticky section nav;
        # provide a compact site/home switcher instead of duplicating all anchors.
        prefix = home_path[:-len("index.html")] if home_path.endswith("index.html") else ""
        return (
            "<!-- kg-nav-start -->\n"
            '<nav id="kg-nav" class="kg-nav-standalone">'
            f'<a class="kg-home" href="{home_path}">🏠 秘密基地</a>'
            f'<a class="kg-back" href="{prefix}digital-literacy.html">考试准备教程</a>'
            f'<a class="kg-back" href="{prefix}digital-practice.html">13题练习库</a>'
            "</nav>\n<!-- kg-nav-end -->"
        )
    prefix = home_path[:-len("index.html")] if home_path.endswith("index.html") else ""
    topics_html = ""
    for key, (label, anchor) in TOPIC_LABELS.items():
        active = ' class="kg-active"' if key == current_topic else ""
        target = f"{prefix}digital-literacy.html" if anchor == "digital-literacy.html" else f"{home_path}#{anchor}"
        topics_html += f'<a href="{target}"{active}>{label}</a>'
    return (
        "<!-- kg-nav-start -->\n"
        '<nav id="kg-nav">\n'
        f'  <a class="kg-home" href="{home_path}">秘密基地</a>\n'
        f'  <div class="kg-topics">{topics_html}</div>\n'
        "</nav>\n"
        "<!-- kg-nav-end -->"
    )


def build_sidebar_html(current_topic: str, prefix: str) -> str:
    """左侧目录（覆盖式自动隐藏）。prefix: 相对当前页回到 public 根的路径（如 "" 或 "../"）。"""
    if current_topic == "digital":
        return "<!-- kg-sb-start --><!-- kg-sb-end -->"
    parts = ["<!-- kg-sb-start -->"]
    # ☰ 展开把手：始终留在左侧边缘
    parts.append('<button id="kg-sb-toggle" title="展开目录" aria-label="展开目录"><span class="kg-sb-tg-ic">☰</span></button>')
    # 半透明遮罩：点击收起（覆盖内容但不挡住 sidebar）
    parts.append('<div class="kg-sb-mask" id="kg-sb-mask"></div>')
    parts.append('<aside id="kg-sidebar">')
    # ✕ 收起按钮
    parts.append('<button id="kg-sb-x" title="收起目录" aria-label="收起目录">✕</button>')
    home = prefix + "index.html"
    parts.append(f'<a class="kg-sb-home" href="{home}">🏠 秘密基地</a>')
    for key, (label, anchor) in TOPIC_LABELS.items():
        parts.append(f'<div class="kg-sb-topic">📍 {label}</div>')
        # 主题下的所有页面
        page_list = [p for p, t in PAGES.items() if t == key]
        for rel in page_list:
            active = ' kg-sb-active' if rel == CURRENT_PAGE else ""
            url = prefix + rel
            short = PAGE_SHORT_NAMES.get(rel, rel)
            parts.append(f'<a class="kg-sb-page{active}" href="{url}">· {short}</a>')
    parts.append("</aside>")
    parts.append("<!-- kg-sb-end -->")
    return "\n".join(parts)


TOC_JS = """<!-- kg-toc-js-start -->
<script>
/* 左侧目录：自动收起 / 悬停展开 */
(function(){
  var sb=document.getElementById('kg-sidebar');
  var tg=document.getElementById('kg-sb-toggle');
  var x=document.getElementById('kg-sb-x');
  var mask=document.getElementById('kg-sb-mask');
  if(!sb||!tg) return;
  var open = document.body.classList.contains('kg-sb-open');
  function setOpen(v){
    open=v;
    if(v){document.body.classList.add('kg-sb-open');}
    else{document.body.classList.remove('kg-sb-open');}
  }
  tg.addEventListener('mouseenter',function(){setOpen(true);});
  tg.addEventListener('focus',function(){setOpen(true);});
  tg.addEventListener('click',function(e){e.stopPropagation();setOpen(!open);});
  if(x){x.addEventListener('click',function(e){e.stopPropagation();setOpen(false);});}
  if(mask){mask.addEventListener('click',function(){setOpen(false);});}
  sb.addEventListener('mouseenter',function(){setOpen(true);});
  sb.addEventListener('mouseleave',function(){setOpen(false);});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')setOpen(false);});
})();
</script>
<!-- kg-toc-js-end -->"""


EGGY_JS = """<script>
(function(){
  var eggy=document.getElementById('kg-eggy');
  if(!eggy) return;
  var svg=eggy.querySelector('svg');
  var pl=document.getElementById('kg-pupil-l');
  var pr=document.getElementById('kg-pupil-r');
  var mouth=document.getElementById('kg-eggy-mouth');
  var body=eggy.querySelector('.kg-egg-body');
  var eyeL=document.getElementById('kg-eye-l'), eyeR=document.getElementById('kg-eye-r');
  var faces=[["#fde047","M42 84 Q50 90 58 84"],["#fca5a5","M42 86 Q50 80 58 86"],["#86efac","M42 82 Q50 92 58 82"],["#93c5fd","M42 88 Q50 84 58 88"]];
  var fi=0;
  var desktopW=70,desktopH=84;
  function viewportMetrics(){var v=window.visualViewport;return v?{left:v.offsetLeft||0,top:v.offsetTop||0,width:v.width,height:v.height}:{left:0,top:0,width:window.innerWidth,height:window.innerHeight};}
  var initialViewport=viewportMetrics();
  var W=Math.min(desktopW,Math.max(48,initialViewport.width<=860?56:70));
  var H=Math.round(desktopH*W/desktopW);
  function mp(p,cx,cy,mx,my){var r=eggy.getBoundingClientRect();var dx=mx-(r.left+cx*0.7+35),dy=my-(r.top+cy*0.7+42);var d=Math.sqrt(dx*dx+dy*dy)||1,max=4;p.setAttribute('cx',cx+Math.min(max,dx/d*max));p.setAttribute('cy',cy+Math.min(max,dy/d*max));}
  document.addEventListener('mousemove',function(e){if(flying)return;mp(pl,36,68,e.clientX,e.clientY);mp(pr,64,68,e.clientX,e.clientY);});
  document.addEventListener('touchmove',function(e){if(flying)return;if(e.touches[0]){mp(pl,36,68,e.touches[0].clientX,e.touches[0].clientY);mp(pr,64,68,e.touches[0].clientX,e.touches[0].clientY);}},{passive:true});
  var clickCount=0;
  function fireConfetti(){var box=document.getElementById('kg-confetti');if(!box){box=document.createElement('div');box.id='kg-confetti';document.body.appendChild(box);}var colors=['#0ea5e9','#fde047','#fb7185','#86efac','#fbbf24','#a78bfa','#f97316','#38bdf8'];var v=viewportMetrics(),cx=v.left+v.width-55,cy=v.top+v.height-50;for(var i=0;i<60;i++){var p=document.createElement('div');p.className='kg-cf';p.style.background=colors[i%colors.length];p.style.left=cx+'px';p.style.top=cy+'px';var ang=Math.random()*Math.PI*2,sp=60+Math.random()*120;var dx=Math.cos(ang)*sp,dy=Math.sin(ang)*sp-80;p.style.transition='transform 1.2s cubic-bezier(.2,.6,.4,1),opacity 1.2s ease';box.appendChild(p);requestAnimationFrame(function(el,xx,yy){return function(){el.style.opacity='1';el.style.transform='translate('+xx+'px,'+yy+'px) scale('+(0.5+Math.random())+') rotate('+(Math.random()*720)+'deg)';};}(p,dx,dy));setTimeout(function(el){return function(){el.style.opacity='0';};}(p),900);}setTimeout(function(){if(box.parentNode)box.parentNode.removeChild(box);},1500);}
  function fireExplosion(){
    var flash=document.getElementById('kg-flash');
    if(!flash){flash=document.createElement('div');flash.id='kg-flash';document.body.appendChild(flash);}
    flash.classList.remove('kg-on');void flash.offsetWidth;flash.classList.add('kg-on');
    setTimeout(function(){flash.classList.remove('kg-on');},750);
    var box=document.getElementById('kg-confetti');
    if(!box){box=document.createElement('div');box.id='kg-confetti';document.body.appendChild(box);}
    var v=viewportMetrics(),cx=v.left+v.width-55,cy=v.top+v.height-50;
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
  /* ==== 拖动 + 右下角隐形栅栏（墙在网页右下角 1/5 处）==== */
  var homeL=0, homeT=0;
  function bounds(){var v=viewportMetrics(),vw=v.width,vh=v.height;var rw=Math.max(vw/5,150),rh=Math.max(vh/5,120);return {L:v.left+vw-rw,T:v.top+vh-rh,R:v.left+vw,B:v.top+vh};}
  function setHome(){
    var v=viewportMetrics();W=Math.min(desktopW,Math.max(48,v.width<=860?56:70));H=Math.round(desktopH*W/desktopW);
    eggy.style.width=W+'px';eggy.style.height=H+'px';if(svg){svg.setAttribute('width',W);svg.setAttribute('height',H);}
    homeL=Math.max(v.left+8,v.left+v.width-W-20);homeT=Math.max(v.top+8,v.top+v.height-H-20);
    eggy.style.left=homeL+'px';eggy.style.top=homeT+'px';eggy.style.right='auto';eggy.style.bottom='auto';
  }
  function resetAppearance(){
    eggy.classList.remove('kg-blasted','kg-flying','kg-fallen','kg-crying','kg-dragging');svg.classList.remove('kg-wall-shake');svg.style.transform='';
    eggy.style.transform='';eggy.style.filter='';eggy.style.transition='';eggy.style.opacity='1';body.setAttribute('fill',faces[fi][0]);
    pl.setAttribute('cx','36');pr.setAttribute('cx','64');pl.setAttribute('cy','68');pr.setAttribute('cy','68');pl.setAttribute('r','5.5');pr.setAttribute('r','5.5');
    eyeL.setAttribute('cx','36');eyeR.setAttribute('cx','64');eyeL.setAttribute('r','11');eyeR.setAttribute('r','11');mouth.setAttribute('d',faces[fi][1]);mouth.setAttribute('fill','none');
    var dirt=eggy.querySelector('.kg-dirt');if(dirt)dirt.style.opacity='0';var smoke=eggy.querySelector('.kg-smoke');if(smoke)smoke.style.opacity='0';var dustbox=document.getElementById('kg-dustbox');if(dustbox)dustbox.remove();
  }
  resetAppearance();setHome();
  function updateViewportHome(){if(down||flying)return;var v=viewportMetrics(),r=eggy.getBoundingClientRect();if(r.right>v.left+v.width||r.left<v.left||r.bottom>v.top+v.height||r.top<v.top)setHome();}
  window.addEventListener('resize',function(){abortFlight();resetCharge();if(down)release({type:'pointercancel'});setHome();});
  if(window.visualViewport){window.visualViewport.addEventListener('resize',updateViewportHome);window.visualViewport.addEventListener('scroll',updateViewportHome);}
  window.addEventListener('load',updateViewportHome,{once:true});[0,100,350,900].forEach(function(ms){setTimeout(updateViewportHome,ms);});
  var down=null, dragging=false, wallOn=false, lastDust=0, suppress=0, retTimer=null;
  // Continuous corner pressure arms the spring even when the pointer stops moving.
  var chargeTimer=null, chargeRAF=0, chargeSince=0, ready=false, spring=null, tension=0, chargeProgress=0, launchAngle=Math.PI/4;
  var flying=false, flightRAF=0, flightTimer=null, activePointer=null;
  function resetCharge(){
    if(chargeTimer) clearTimeout(chargeTimer);
    cancelAnimationFrame(chargeRAF);chargeRAF=0;
    chargeTimer=null;chargeSince=0;ready=false;chargeProgress=0;
    if(!flying)eggy.style.filter="";
    if(spring){spring.remove();spring=null;}
  }
  function drawSpring(recoil){
    if(!spring){
      spring=document.createElementNS('http://www.w3.org/2000/svg','svg');spring.id='kg-spring';
      spring.innerHTML='<path stroke="#a78bfa" stroke-width="9" opacity=".4"/><path stroke="#67e8f9" stroke-width="4"/><path stroke="white" stroke-width="1.3"/><polyline class="kg-aim" fill="none" stroke="#0ea5e9" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><text text-anchor="end"/><rect class="kg-charge-track" rx="4" fill="#cbd5e1" opacity=".6"/><rect class="kg-charge-fill" rx="4" fill="#22d3ee"/>';
      document.body.appendChild(spring);
    }
    var w=window.innerWidth,h=window.innerHeight;
    spring.setAttribute('viewBox','0 0 '+w+' '+h);
    var span=Math.min(145,w*.28,h*.28), pull=recoil===undefined?10+chargeProgress*(14+tension*38):recoil;
    // Two anchors form a diagonal trampoline facing the upper-left launch direction.
    var x=w-12,y=h-12;
    var d='M '+(x-span)+' '+y+' Q '+(x-span/2+pull)+' '+(y-span/2+pull)+' '+x+' '+(y-span);
    spring.querySelectorAll('path').forEach(function(path){path.setAttribute('d',d);});
    var originX=parseFloat(eggy.style.left)+W/2,originY=parseFloat(eggy.style.top)+H/2;
    var ux=-Math.cos(launchAngle),uy=-Math.sin(launchAngle),length=75+25*chargeProgress;
    var tipX=originX+ux*length,tipY=originY+uy*length;
    var aim=spring.querySelector('.kg-aim');
    aim.setAttribute('points',(tipX-ux*12-uy*7)+','+(tipY-uy*12+ux*7)+' '+tipX+','+tipY+' '+(tipX-ux*12+uy*7)+','+(tipY-uy*12-ux*7)+' '+tipX+','+tipY+' '+originX+','+originY);
    aim.style.opacity=recoil===undefined?'0.85':'0';
    var label=spring.querySelector('text');label.setAttribute('x',w-20);label.setAttribute('y',h-span-24);
    var pulse=.5+.5*Math.sin(Date.now()/140);
    spring.querySelectorAll('path').forEach(function(path,i){
      path.style.opacity=String((i===0?.2+.25*pulse:.4+.6*chargeProgress));
    });
    label.textContent=recoil!==undefined?'':ready?'瞄准 '+Math.round(launchAngle*180/Math.PI)+'° · 松手起飞！':'蓄力 '+Math.floor(chargeProgress*100)+'% · 继续按住';
    var track=spring.querySelector('.kg-charge-track'),fill=spring.querySelector('.kg-charge-fill');
    [track,fill].forEach(function(bar){bar.setAttribute('x',w-140);bar.setAttribute('y',h-span-14);bar.setAttribute('height',6);});
    track.setAttribute('width',120);fill.setAttribute('width',120*chargeProgress);
    eggy.style.filter='drop-shadow(0 0 '+(3+chargeProgress*10+pulse*3)+'px rgba(34,211,238,'+(.2+chargeProgress*.7)+'))';
  }
  function cornerPressure(ox,oy){
    if(!chargeSince&&(ox<8||oy<8))return;
    // Once engaged, aiming remains latched until release or cancellation.
    if(ox>0||oy>0)launchAngle=Math.max(Math.PI/12,Math.min(Math.PI*5/12,Math.atan2(Math.max(0,oy),Math.max(0,ox))));
    tension=Math.min(1,Math.hypot(ox,oy)/150);
    if(ready){drawSpring();return;}
    if(chargeTimer) return;
    chargeSince=Date.now();
    function charging(){
      if(!down||!dragging)return;
      chargeProgress=Math.min(1,(Date.now()-chargeSince)/1500);
      drawSpring();chargeRAF=requestAnimationFrame(charging);
    }
    charging();
    chargeTimer=setTimeout(function(){
      chargeTimer=null;
      if(!down||!dragging) return;
      ready=true;drawSpring();
    },1500);
  }
  function abortFlight(){
    cancelAnimationFrame(flightRAF);flightRAF=0;
    if(flightTimer)clearTimeout(flightTimer);flightTimer=null;
    flying=false;eggy.classList.remove('kg-flying','kg-fallen','kg-crying');
    svg.style.transform='';eggy.style.transition='';eggy.style.transform='';eggy.style.filter='';
    setScaredFace(false);
  }
  function launch(){
    var x=parseFloat(eggy.style.left),y=parseFloat(eggy.style.top);
    var started=performance.now(),last=started;
    var speed=Math.hypot((window.innerWidth-W)*2.1,(window.innerHeight-H)*2.55);
    var vx=-Math.cos(launchAngle)*speed,vy=-Math.sin(launchAngle)*speed;
    cancelAnimationFrame(chargeRAF);chargeRAF=0;
    flying=true;suppress=Date.now()+3100;
    eggy.classList.remove('kg-bounce');eggy.classList.add('kg-flying');
    eggy.style.transform='';eggy.style.transition='none';wallOn=false;setScaredFace(true);
    if(spring){drawSpring(-35);spring.style.transition='opacity .3s';spring.style.opacity='0';}
    function finish(){
      abortFlight();resetCharge();setHome();squashFace(false);
    }
    // Gravity and inelastic collisions dissipate energy; land before walking home.
    var phase='air',phaseAt=0,fallAngle=0,walkStart=0,rollStart=0,rollEnd=0,rollDirection=1,scared=true;
    var gravity=Math.max(450,window.innerHeight*.95),impulse=0;
    // A safety cleanup only; normal completion is driven by landing, not a deadline.
    flightTimer=setTimeout(finish,20000);
    function ease(t){return t*t*(3-2*t);}
    function frame(now){
      if(!flying)return;
      var elapsed=now-started,dt=Math.min((now-last)/1000,.04);last=now;
      if(scared&&(elapsed>720||phase!=='air')){setScaredFace(false);scared=false;}
      var maxX=Math.max(0,window.innerWidth-W),floor=Math.max(0,window.innerHeight-H);
      var energy=Math.max(0,Math.min(1,Math.hypot(vx,vy)/Math.hypot((window.innerWidth-W)*2.1,(window.innerHeight-H)*2.55)));
      var angle=0,sx=1,sy=1;
      if(phase==='air'){
        vx*=Math.exp(-.10*dt);vy+=gravity*dt;
        x+=vx*dt;y+=vy*dt;
        if(x<0||x>maxX){x=Math.max(0,Math.min(x,maxX));vx=-vx*.72;impulse=1;dust(vx>0?-1:1,0);}
        if(y<0){y=0;vy=Math.abs(vy)*.68;impulse=1;dust(0,-1);}
        if(y>=floor){
          y=floor;
          if(Math.abs(vy)<200&&elapsed>1200){
            phase='roll';phaseAt=now;rollStart=x;
            rollDirection=vx<0?-1:1;
            var distance=Math.min(220,Math.max(130,Math.abs(vx)*.85));
            if((rollDirection<0?x:maxX-x)<distance*.65)rollDirection=-rollDirection;
            rollEnd=Math.max(0,Math.min(maxX,x+rollDirection*distance));
            fallAngle=rollDirection*24;vx=0;vy=0;
            eggy.classList.add('kg-fallen','kg-crying');mouth.setAttribute('d','M42 88 Q50 81 58 88');dust(0,1);
          }else{vy=-Math.abs(vy)*.66;vx*=.94;impulse=1;dust(0,1);}
        }
        impulse=Math.max(0,impulse-dt*5);
        sx=1+impulse*.18;sy=1-impulse*.16;
        angle=Math.sin(elapsed/150)*16*energy;
      }
      if(phase==='roll'){
        var rt=Math.min(1,(now-phaseAt)/950),rp=1-Math.pow(1-rt,2);
        x=rollStart+(rollEnd-rollStart)*rp;
        // Keep the rotating 70x84 box above the floor throughout the tumble.
        angle=rollDirection*360*rp;
        var radians=angle*Math.PI/180;
        var extent=(Math.abs(Math.sin(radians))*W+Math.abs(Math.cos(radians))*H)/2;
        y=floor-Math.max(0,extent-H/2)-Math.sin(rt*Math.PI)*7;
        if(rt>=1){phase='fallen';phaseAt=now;}
      }
      if(phase==='fallen'){
        var t=Math.min(1,(now-phaseAt)/800);
        y=floor;
        // Stay upright, cry briefly, then gently get up.
        sx=1;sy=1;
        angle=fallAngle*Math.sin(Math.min(1,t*4)*Math.PI/2)*(1-ease(Math.max(0,(t-.45)/.55)));
        angle+=Math.sin(t*28)*5*(1-t);
        if(t>=1){phase='walk';phaseAt=now;walkStart=x;squashFace(false);eggy.classList.remove('kg-fallen','kg-crying');}
      }
      if(phase==='walk'){
        var duration=Math.max(900,Math.abs(homeL-walkStart)/280*1000);
        var t=Math.min(1,(now-phaseAt)/duration),travel=ease(t);
        x=walkStart+(homeL-walkStart)*travel;
        var step=Math.sin((now-phaseAt)/65);
        var gait=Math.min(1,t*6,(1-t)*6);
        y=floor-Math.abs(step)*5*gait;angle=step*5*gait;
        if(t>=1){phase='settle';phaseAt=now;}
      }
      if(phase==='settle'){
        var t=Math.min(1,(now-phaseAt)/450);
        x=homeL;y=floor+(homeT-floor)*ease(t);angle=0;
        if(t>=1){finish();return;}
      }
      eggy.style.left=x+'px';eggy.style.top=y+'px';
      eggy.style.transform='scale('+sx+','+sy+')';
      var glow=phase==='air'?energy:0;
      eggy.style.filter='drop-shadow(0 0 '+(12*glow)+'px rgba(56,189,248,'+glow+'))';
      svg.style.transform='rotate('+angle+'deg)';
      flightRAF=requestAnimationFrame(frame);
    }
    flightRAF=requestAnimationFrame(frame);
  }
  document.addEventListener('visibilitychange',function(){if(document.hidden){if(down)release({type:'pointercancel'});abortFlight();resetCharge();setHome();}});
  window.addEventListener('blur',function(){if(down)release({type:'pointercancel'});});
  eggy.addEventListener('lostpointercapture',function(){if(down)release({type:'pointercancel'});});
  function squashFace(on){
    if(on){mouth.setAttribute('d','M42 87 Q50 81 58 87');pl.setAttribute('r','6.8');pr.setAttribute('r','6.8');}
    else{mouth.setAttribute('d',faces[fi][1]);pl.setAttribute('r','5.5');pr.setAttribute('r','5.5');}
  }
  function setScaredFace(on){
    if(on){
      eyeL.setAttribute('r','12');eyeR.setAttribute('r','12');
      pl.setAttribute('r','4.7');pr.setAttribute('r','4.7');
      pl.setAttribute('cx','37');pr.setAttribute('cx','63');
      pl.setAttribute('cy','65');pr.setAttribute('cy','65');
      mouth.setAttribute('d','M47 86 Q50 82 53 86 Q50 90 47 86');
      mouth.setAttribute('fill','#1e293b');
    }else{
      eyeL.setAttribute('r','11');eyeR.setAttribute('r','11');
      pl.setAttribute('r','5.5');pr.setAttribute('r','5.5');
      pl.setAttribute('cx','36');pr.setAttribute('cx','64');
      pl.setAttribute('cy','68');pr.setAttribute('cy','68');
      mouth.setAttribute('d',faces[fi][1]);mouth.setAttribute('fill','none');
    }
  }
  function dust(ox,oy){
    var box=document.getElementById('kg-dustbox');
    if(!box){box=document.createElement('div');box.id='kg-dustbox';document.body.appendChild(box);}
    var r=eggy.getBoundingClientRect();
    var px=Math.abs(ox)>Math.abs(oy)?(ox>0?r.right-3:r.left+3):r.left+W/2+(Math.random()*12-6);
    var py=Math.abs(oy)>=Math.abs(ox)?(oy>0?r.bottom-3:r.top+3):r.top+H/2+(Math.random()*12-6);
    var dxdir=ox>0?1:-1, dydir=oy>0?1:-1;
    for(var i=0;i<7;i++){
      var d=document.createElement('span'); d.className='kg-dust';
      d.style.left=px+'px'; d.style.top=py+'px';
      var tx=(ox?dxdir*(12+Math.random()*28):(Math.random()*34-17));
      var ty=(oy?dydir*(10+Math.random()*22):(Math.random()*34-17))+16;
      var s=4+Math.random()*4;
      d.style.width=s+'px'; d.style.height=s+'px';
      box.appendChild(d);
      requestAnimationFrame(function(el,xx,dy){return function(){el.style.opacity='.85';el.style.transform='translate('+xx+'px,'+dy+'px) scale(.25)';};}(d,tx,ty));
      setTimeout(function(el){return function(){el.style.opacity='0';};}(d),300);
      setTimeout(function(el){return function(){if(el.parentNode)el.parentNode.removeChild(el);};}(d),620);
    }
  }
  eggy.addEventListener('pointerdown',function(e){
    if(flying||down||eggy.classList.contains('kg-blasted')) return;
    if(e.pointerType==='mouse'&&e.button!==0) return;
    if(retTimer){clearTimeout(retTimer);retTimer=null;}
    resetCharge();activePointer=e.pointerId;
    eggy.classList.remove('kg-bounce');eggy.style.transition='';
    var r=eggy.getBoundingClientRect();
    down={x:e.clientX,y:e.clientY,ox:r.left-e.clientX,oy:r.top-e.clientY};
    dragging=false;
    try{eggy.setPointerCapture(e.pointerId);}catch(err){}
  });
  window.addEventListener('pointermove',function(e){
    if(!down||e.pointerId!==activePointer) return;
    var dx=e.clientX-down.x, dy=e.clientY-down.y;
    if(!dragging && dx*dx+dy*dy<36) return;
    if(!dragging){dragging=true;eggy.classList.add('kg-dragging');}
    var b=bounds();
    var lx=down.ox+e.clientX, ly=down.oy+e.clientY;
    var cl=Math.max(b.L,Math.min(lx,b.R-W)), ct=Math.max(b.T,Math.min(ly,b.B-H));
    var ox=lx-cl, oy=ly-ct;
    cornerPressure(ox,oy);
    if(chargeSince){
      eggy.style.left=(b.R-W)+'px';eggy.style.top=(b.B-H)+'px';
      eggy.style.transform='scale(1,1)';wallOn=false;squashFace(false);
      svg.classList.remove('kg-wall-shake');
      return;
    }
    eggy.style.left=cl+'px'; eggy.style.top=ct+'px';
    var hit=(ox!==0||oy!==0), now=Date.now();
    if(hit){
      var ax=Math.min(24,Math.abs(ox)), ay=Math.min(24,Math.abs(oy));
      var scx=Math.max(0.62,Math.min(1.35,1-ax*0.014+ay*0.011));
      var scy=Math.max(0.62,Math.min(1.35,1-ay*0.014+ax*0.011));
      eggy.style.transform='scale('+scx.toFixed(3)+','+scy.toFixed(3)+')';
      if(!wallOn){wallOn=true;squashFace(true);svg.classList.remove('kg-wall-shake');void svg.offsetWidth;svg.classList.add('kg-wall-shake');dust(ox,oy);lastDust=now;}
      else if(now-lastDust>320){dust(ox,oy);lastDust=now;}
    }else if(wallOn){
      wallOn=false;squashFace(false);eggy.style.transform='';
    }
  },{passive:true});
  function release(e){
    if(!down||(e&&e.pointerId!==undefined&&e.pointerId!==activePointer)) return;
    var wasDrag=dragging, shouldLaunch=ready&&e&&e.type==='pointerup';
    down=null;activePointer=null;
    if(shouldLaunch){dragging=false;eggy.classList.remove('kg-dragging');launch();return;}
    resetCharge();
    if(wasDrag){
      dragging=false;eggy.classList.remove('kg-dragging');
      suppress=Date.now()+400;
      eggy.style.transition='left .4s cubic-bezier(.34,1.56,.64,1), top .4s cubic-bezier(.34,1.56,.64,1), transform .32s ease';
      eggy.style.left=homeL+'px'; eggy.style.top=homeT+'px'; eggy.style.transform='';
      retTimer=setTimeout(function(){eggy.style.transition='';retTimer=null;if(wallOn){wallOn=false;squashFace(false);}},460);
    }
  }
  window.addEventListener('pointerup',release);
  window.addEventListener('pointercancel',release);
  eggy.addEventListener('click',function(e){
    if(flying||Date.now()<suppress) return;
    fi=(fi+1)%faces.length;body.setAttribute('fill',faces[fi][0]);mouth.setAttribute('d',faces[fi][1]);eggy.classList.remove('kg-bounce');void eggy.offsetWidth;eggy.classList.add('kg-bounce');clickCount++;if(clickCount>=30){clickCount=0;fireExplosion();}else if(clickCount%10===0){fireConfetti();}
  });
})();
</script>"""

EGGY_HTML = """<!-- kg-eggy-start -->
<div id="kg-eggy" title="按住向右下角拉满1.5秒，松手起飞！轻点10次放烟花，30次大惊喜">
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
    <ellipse class="kg-tear" cx="27" cy="83" rx="2.8" ry="4.2" fill="#38bdf8"/>
    <ellipse class="kg-tear" cx="73" cy="83" rx="2.8" ry="4.2" fill="#38bdf8"/>
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


def eggy_asset_tags() -> str:
    """Shared site-wide eggy files keep 16 copies of its runtime in sync."""
    return '<link rel="stylesheet" href="/assets/eggy.css">'


def eggy_script_tag() -> str:
    return '<!-- kg-eggy-js-start -->\n<script src="/assets/eggy.js" defer></script>\n<!-- kg-eggy-js-end -->'


def ensure_page_meta(html: str, rel_path: str) -> str:
    """Add useful browser theme and social-preview metadata without overwriting authored tags."""
    title_match = re.search(r"<title>(.*?)</title>", html, flags=re.I | re.S)
    title_overrides = {"digital-practice.html": "数智素养练习库｜小萝卜的秘密花园"}
    title = title_overrides.get(rel_path) or (re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else "小萝卜的宝藏大陆")
    if rel_path == "digital-practice.html" and title_match:
        html = html[:title_match.start()] + f"<title>{title}</title>" + html[title_match.end():]
    descriptions = {
        "index.html": "小萝卜的宝藏大陆：收集错题本、C++ 编程教程、树与搜索算法互动课，以及数智素养考试练习。",
        "digital-literacy.html": "用 turtle 递归画树、用 pandas 分析 CSV：小萝卜的数智素养考试准备互动教程。",
        "digital-practice.html": "递归绘图与数据统计练习库：13 道 Python 练习，附解析、答案、CSV 与下载代码。",
    }
    description = descriptions.get(rel_path, f"{title}：小萝卜的宝藏大陆互动学习教程，配有图解、动画和练习。")
    page_path = "" if rel_path == "index.html" else rel_path
    if page_path.endswith("index.html"):
        page_path = page_path[:-len("index.html")]
    page_url = "https://kids-pages-1pw.pages.dev/" + page_path
    tags = [
        f'<meta name="description" content="{description}">',
        '<meta name="theme-color" content="#287e82">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{description}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:url" content="{page_url}">',
        '<meta name="twitter:card" content="summary">',
    ]
    additions = []
    if not re.search(r'<meta\s+charset=', html, re.I): additions.append('<meta charset="UTF-8">')
    if not re.search(r'<meta\s+name=["\']viewport["\']', html, re.I): additions.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    if not re.search(r'<title\b', html, re.I): additions.append(f"<title>{title}</title>")
    if not re.search(r'<meta\s+name=["\']description["\']', html, re.I): additions.append(tags[0])
    if not re.search(r'<meta\s+name=["\']theme-color["\']', html, re.I): additions.append(tags[1])
    if not re.search(r'<meta\s+property=["\']og:title["\']', html, re.I): additions.extend(tags[2:6])
    if not re.search(r'<meta\s+name=["\']twitter:card["\']', html, re.I): additions.append(tags[6])
    if additions:
        html = re.sub(r"</head>", "\\n" + "\\n".join(additions) + "\\n</head>", html, count=1, flags=re.I)
    if not re.search(r'<link[^>]+rel=["\']icon["\']', html, re.I):
        html = re.sub(r"</head>", '\\n<link rel="icon" type="image/svg+xml" href="/favicon.svg">\\n</head>', html, count=1, flags=re.I)
    return html


def ensure_eggy_assets() -> None:
    """Emit the canonical shared assets from injector source constants."""
    assets = PUBLIC_DIR / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    css = re.sub(r"^<style[^>]*>|</style>$", "", EGGY_CSS.strip(), flags=re.S)
    js = re.sub(r"^<script[^>]*>|</script>$", "", EGGY_JS.strip(), flags=re.S)
    js = js.replace("(function(){\n  var eggy=document.getElementById('kg-eggy');", "(function(){\n  if(window.__KG_EGGY_INIT__) return;\n  window.__KG_EGGY_INIT__=true;\n  var eggy=document.getElementById('kg-eggy');", 1)
    (assets / "eggy.css").write_text(css.strip() + "\n", encoding="utf-8")
    (assets / "eggy.js").write_text(js.strip() + "\n", encoding="utf-8")


def ensure_explicit_body(html: str) -> str:
    """Repair older implicit-head/body documents before adding shared navigation."""
    if re.search(r"<body\b", html, re.I):
        # Recovery of metadata after </head> belongs only to the original malformed practice page.
        if "數智素養練習庫" in html and re.search(r"</head>\s*<body\b", html, re.I):
            body_start = re.search(r"<body\b[^>]*>", html, re.I)
            tail = html[body_start.end():]
            match = re.match(r"\s*((?:<meta\b[^>]*>|<title\b.*?</title>|<style\b.*?</style>)+)", tail, re.I | re.S)
            if match:
                html = html[:body_start.start()] + match.group(1) + html[body_start.start():body_start.end()] + tail[match.end():]
        return html
    head = re.search(r"<head\b[^>]*>(.*?)</head>", html, re.I | re.S)
    if not head:
        html = re.sub(r"(<html\b[^>]*>)", r"\1\n<head>", html, count=1, flags=re.I)
        head = re.search(r"<head\b[^>]*>(.*?)</head>", html, re.I | re.S)
    if head:
        # If the original omitted </head>, absorb metadata/styles through the first CSS close.
        if head.group(1).strip() == "":
            start = head.end()
            style_end = re.search(r"</style>", html[start:], re.I)
            if style_end:
                end = start + style_end.end()
                html = html[:head.start(1)] + html[head.start(1):end] + "</head><body>" + html[end:]
            else:
                html = html[:head.end()] + "<body>" + html[head.end():]
        else:
            html = html[:head.end()] + "<body>" + html[head.end():]
    else:
        raise ValueError("HTML page has no <html> element")
    if not re.search(r"</body>", html, re.I):
        html = re.sub(r"</html>", "</body>\n</html>", html, count=1, flags=re.I)
    # The old practice page placed metadata and styles after </head>. Pull that
    # leading head-only material back into the head before wrapping body content.
    body_start = re.search(r"<body\b[^>]*>", html, re.I)
    if body_start:
        tail = html[body_start.end():]
        match = re.match(r"\s*((?:<meta\b[^>]*>|<title\b.*?</title>|<style\b.*?</style>)+)", tail, re.I | re.S)
        if match:
            html = html[:body_start.start()] + match.group(1) + html[body_start.start():body_start.end()] + tail[match.end():]
    return html


def normalize_slots(html: str) -> str:
    """把三个注入槽位周围的空白归一化，保证重复注入逐字节稳定。"""
    html = re.sub(r"\n+</head>", "\n</head>", html, count=1)
    html = re.sub(r"(<body[^>]*>)\n+", r"\1\n", html, count=1)
    html = re.sub(r"\n+</body>", "\n</body>", html, count=1)
    return html


def inject_page(rel_path: str, topic: str):
    global CURRENT_PAGE
    CURRENT_PAGE = rel_path
    fpath = PUBLIC_DIR / rel_path
    if not fpath.exists():
        print(f"  ✘ 缺失: {rel_path}")
        return
    ensure_eggy_assets()
    # Only actual folder nesting affects relative home URL; a tutorial slug has no slash.
    depth = rel_path.count("/")
    home = "../" * depth + "index.html" if depth > 0 else "index.html"

    html = ensure_explicit_body(fpath.read_text(encoding="utf-8"))
    html = re.sub(r'<style id="kg-eggy-style">.*?</style>', '', html, flags=re.S)
    html = re.sub(r'<link rel="stylesheet" href="/assets/eggy.css">', '', html)
    html = re.sub(r'<script src="/assets/eggy.js" defer></script>', '', html)
    html = re.sub(r'<!-- kg-eggy-start -->.*?<!-- kg-eggy-end -->', '', html, flags=re.S)
    html = re.sub(r'<!-- kg-eggy-js-start -->.*?<!-- kg-eggy-js-end -->', '', html, flags=re.S)

    # 清除旧注入的 CSS
    html = re.sub(r'<style id="kg-nav-style">.*?</style>', "", html, flags=re.S)
    # 清除旧注入的导航栏
    html = re.sub(r"<!-- kg-nav-start -->.*?<!-- kg-nav-end -->", "", html, flags=re.S)
    # 清除旧注入的蛋仔 HTML
    html = re.sub(r"<!-- kg-eggy-start -->.*?<!-- kg-eggy-end -->", "", html, flags=re.S)
    # 清除旧注入的蛋仔 JS
    html = re.sub(r"<!-- kg-eggy-js-start -->.*?<!-- kg-eggy-js-end -->", "", html, flags=re.S)
    # 清除旧注入的目录交互 JS
    html = re.sub(r"<!-- kg-toc-js-start -->.*?<!-- kg-toc-js-end -->", "", html, flags=re.S)
    # 清除旧注入的侧边栏
    html = re.sub(r"<!-- kg-sb-start -->.*?<!-- kg-sb-end -->", "", html, flags=re.S)
    html = normalize_slots(html)

    # Add baseline icon/theme metadata even to pages originally lacking head metadata.
    if "</head>" in html:
        html = ensure_page_meta(html, rel_path)

    # 注入 CSS 到 </head> 前
    if "</head>" in html:
        html = html.replace("</head>", NAV_CSS + "\n</head>", 1)
        if "/assets/eggy.css" not in html:
            html = html.replace("</head>", eggy_asset_tags() + "\n</head>", 1)
    else:
        print(f"  ⚠ 无 </head>，跳过 CSS 注入: {rel_path}")

    # 注入导航栏 + 左侧目录 HTML 到 <body ...> 后
    nav_html = build_nav_html(topic, home)
    side_html = build_sidebar_html(topic, "../" * depth)
    m = re.search(r"<body[^>]*>", html)
    if m:
        pos = m.end()
        html = html[:pos] + "\n" + nav_html + "\n" + side_html + "\n" + html[pos:]
    else:
        print(f"  ⚠ 无 <body> 标签，跳过导航栏/侧边栏注入: {rel_path}")

    # 注入互动蛋仔 HTML+JS 到 </body> 前（先注入侧边栏交互脚本）
    if "</body>" in html:
        html = html.replace("</body>", TOC_JS + "\n" + EGGY_HTML + "\n" + eggy_script_tag() + "\n</body>", 1)
    else:
        print(f"  ⚠ 无 </body>，跳过蛋仔注入: {rel_path}")

    html = ensure_page_meta(html, rel_path)
    # Tutorial pages use external shared assets; never duplicate eggy CSS/JS inline.
    html = html.replace(EGGY_CSS, eggy_asset_tags())
    html = html.replace(EGGY_JS, eggy_script_tag())
    fpath.write_text(html, encoding="utf-8")
    print(f"  ✔ 注入完成: {rel_path} (主题={topic}, home={home})")


def inject_home():
    """首页 index.html：注入左侧目录 + 蛋仔；已存在的 kg-sb 区块与 body 标签原样保留。"""
    global CURRENT_PAGE
    fpath = PUBLIC_DIR / "index.html"
    if not fpath.exists():
        print("  ✘ 缺失: index.html")
        return
    ensure_eggy_assets()
    html = ensure_explicit_body(fpath.read_text(encoding="utf-8"))
    html = re.sub(r'<style id="kg-eggy-style">.*?</style>', '', html, flags=re.S)
    html = re.sub(r'<link rel="stylesheet" href="/assets/eggy.css">', '', html)
    html = re.sub(r'<script src="/assets/eggy.js" defer></script>', '', html)
    html = re.sub(r'<!-- kg-eggy-start -->.*?<!-- kg-eggy-end -->', '', html, flags=re.S)
    html = re.sub(r'<!-- kg-eggy-js-start -->.*?<!-- kg-eggy-js-end -->', '', html, flags=re.S)
    # 首页侧边栏由人工维护（宝藏大陆的 1./2./3. 导航），原样保留，不重新生成。
    existing_sb = re.search(r"<!-- kg-sb-start -->.*?<!-- kg-sb-end -->", html, flags=re.S)
    existing_sb = existing_sb.group(0) if existing_sb else None
    # 清除旧注入
    html = re.sub(r'<style id="kg-sb-style">.*?</style>', "", html, flags=re.S)
    html = re.sub(r'<link rel="stylesheet" href="/assets/eggy.css">', "", html)
    html = re.sub(r'<script src="/assets/eggy.js" defer></script>', "", html)
    html = re.sub(r"<!-- kg-sb-start -->.*?<!-- kg-sb-end -->", "", html, flags=re.S)
    html = re.sub(r"<!-- kg-toc-js-start -->.*?<!-- kg-toc-js-end -->", "", html, flags=re.S)
    html = normalize_slots(html)

    has_home_directory = 'id="home-directory"' in html or 'id="home-directory"' in (existing_sb or "")
    sb_css = """<style id="kg-sb-style">
/* 左侧目录：首页默认展开，可悬停/✕收起 */
#kg-sidebar{position:fixed;left:0;top:0;bottom:0;width:206px;background:#f0f9ff;border-right:1px solid #bae6fd;z-index:99990;overflow-y:auto;padding:34px 10px 30px;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;transform:translateX(-100%);transition:transform .26s cubic-bezier(.25,.7,.3,1);}
body.kg-sb-open #kg-sidebar{transform:translateX(0);}
#kg-sidebar .kg-sb-home{display:block;font-weight:800;font-size:14px;color:#0369a1;text-decoration:none;padding:8px 10px;border-radius:10px;background:#e0f2fe;margin-bottom:12px;transition:background .15s;}
#kg-sidebar .kg-sb-home:hover{background:#bae6fd;}
#kg-sidebar .kg-sb-topic{font-weight:700;font-size:12px;color:#0f766e;padding:10px 10px 4px;letter-spacing:.5px;}
#kg-sidebar a.kg-sb-page{display:block;font-size:12.5px;color:#334155;text-decoration:none;padding:5px 10px;border-radius:6px;margin:1px 0;line-height:1.45;}
#kg-sidebar a.kg-sb-page:hover{background:#e0f2fe;color:#0369a1;}
#kg-sidebar #kg-sb-x{position:sticky;top:0;float:right;margin:-24px 0 0;width:22px;height:22px;border:none;border-radius:6px;background:#e0f2fe;color:#0369a1;font-size:12px;line-height:1;cursor:pointer;z-index:2;}
#kg-sidebar #kg-sb-x:hover{background:#fecaca;color:#b91c1c;}
#kg-sb-toggle{position:fixed;left:0;top:0;bottom:0;width:20px;z-index:99989;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;background:transparent;}
#kg-sb-toggle .kg-sb-tg-ic{display:block;writing-mode:vertical-rl;font-size:14px;color:#0ea5e9;background:rgba(224,242,254,.85);padding:8px 3px;border-radius:0 8px 8px 0;box-shadow:0 1px 5px rgba(2,132,199,.18);transition:background .15s,color .15s;}
#kg-sb-toggle:hover .kg-sb-tg-ic{background:#0ea5e9;color:#fff;}
/* 半透明遮罩 */
.kg-sb-mask{position:fixed;left:0;top:0;right:0;bottom:0;background:rgba(15,23,42,.25);z-index:99988;opacity:0;pointer-events:none;transition:opacity .26s;}
body.kg-sb-open .kg-sb-mask{opacity:1;pointer-events:auto;}
/* 内容不左右移动 */
body{padding-left:24px;}
@media(max-width:860px){#kg-sidebar{display:none;}#kg-sb-toggle{display:none;}.kg-sb-mask{display:none;}body{padding-left:0!important;}}
</style>"""
    if "</head>" in html:
        if not has_home_directory:
            html = html.replace("</head>", sb_css + "\n</head>", 1)
        if eggy_asset_tags() not in html:
            html = html.replace("</head>", eggy_asset_tags() + "\n</head>", 1)
    else:
        print("  ⚠ 首页无 </head>，跳过 CSS")

    if existing_sb:
        sb_html = existing_sb
    else:
        # 首次注入才生成默认导航；之后以页面里的 kg-sb 区块为准（人工可改）。
        parts = ["<!-- kg-sb-start -->"]
        parts.append('<button id="kg-sb-toggle" title="展开目录" aria-label="展开目录"><span class="kg-sb-tg-ic">☰</span></button>')
        parts.append('<div class="kg-sb-mask" id="kg-sb-mask"></div>')
        parts.append('<aside id="kg-sidebar">')
        parts.append('<button id="kg-sb-x" title="收起目录" aria-label="收起目录">✕</button>')
        parts.append('<a class="kg-sb-home" href="#top">🏠 秘密基地</a>')
        for key, (label, anchor) in TOPIC_LABELS.items():
            parts.append(f'<div class="kg-sb-topic">📍 {label}</div>')
            parts.append(f'<a class="kg-sb-page" href="#{anchor}">· 查看主题</a>')
        parts.append("</aside>")
        parts.append("<!-- kg-sb-end -->")
        sb_html = "\n".join(parts)

    # body 标签保持原样（是否默认展开由首页自己决定，注入器不覆盖）。
    if existing_sb:
        html = re.sub(r"<!-- kg-sb-start -->.*?<!-- kg-sb-end -->", lambda _: existing_sb, html, count=1, flags=re.S)
    m = re.search(r"<body[^>]*>", html)
    if m:
        pos = m.end()
        if existing_sb:
            # Keep the editor-authored section exactly, but don't insert a duplicate.
            pass
        else:
            html = html[:pos] + "\n" + sb_html + "\n" + html[pos:]
    else:
        print("  ⚠ 首页无 <body>，跳过侧边栏注入")

    if "</body>" in html:
        html = html.replace("</body>", (TOC_JS + "\n" if not has_home_directory else "") + EGGY_HTML + "\n" + eggy_script_tag() + "\n</body>", 1)
    else:
        print("  ⚠ 首页无 </body>，跳过 TOC JS")

    html = ensure_page_meta(html, "index.html")
    html = html.replace(EGGY_CSS, eggy_asset_tags()).replace(EGGY_JS, eggy_script_tag())
    fpath.write_text(html, encoding="utf-8")
    print("  ✔ 注入完成: index.html (首页左侧目录)")


def main():
    print("=== 注入全局导航栏 + 左侧目录 ===")
    # Emit the shared runtime once, then inject its references everywhere.
    ensure_eggy_assets()
    for rel_path, topic in PAGES.items():
        inject_page(rel_path, topic)
    inject_home()
    print("=== 完成 ===")


if __name__ == "__main__":
    main()
