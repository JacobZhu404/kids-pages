from pathlib import Path
import html,json,csv,io
root=Path('/Users/jacob/personal/kids-pages/public');p=root/'digital-literacy.html';s=p.read_text()
tree='''import turtle as t
import random
import math

def draw(x, y, size, angle, depth):
    # 停止条件：层数用完就返回
    if depth == 0:
        return
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    # 正方形四个顶点
    A = (x, y)
    B = (x + size * ux, y + size * uy)
    D = (x + size * vx, y + size * vy)
    C = (B[0] + size * vx, B[1] + size * vy)
    t.pu()
    t.goto(A)
    t.pd()
    t.color(random.random(), random.random(), random.random())
    for point in [B, C, D, A]:
        t.goto(point)
    # 直角三角形的两条直角边：0.6s 与 0.8s
    P = (D[0] + .36 * size * ux + .48 * size * vx,
         D[1] + .36 * size * uy + .48 * size * vy)
    draw(D[0], D[1], size * .6,
         angle + math.degrees(math.atan2(4, 3)), depth - 1)
    draw(P[0], P[1], size * .8,
         angle - math.degrees(math.atan2(3, 4)), depth - 1)

t.setup(900, 700)
t.tracer(False)
t.ht()
draw(-60, -250, 120, 0, 7)
t.update()
t.done()
'''
data='''import pandas as pd
import matplotlib.pyplot as plt

# 文件和本程序放在同一目录；在 IDLE 中打开并按 F5
plt.rcParams["font.sans-serif"] = ["SimHei", "PingFang SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("house_price.csv")
print("前5行：")
print(df.head())
print("平均房间数：", df["房间数"].mean())
print("最大房龄：", df["房龄(年)"].max())

# 本练习面积都大于0；其他数据应先检查缺失值和零面积
 df_placeholder
maximum = df["每平米价格"].max()
print("最高每平米价格：", maximum)
print("对应房屋（并列最高时全部显示）：")
print(df[df["每平米价格"] == maximum])

ordered = df.sort_values("房屋面积(㎡)")
plt.plot(ordered["房屋面积(㎡)"], ordered["房价(万元)"], marker="o")
plt.title("房屋面积与房价关系图")
plt.xlabel("房屋面积（㎡）")
plt.ylabel("房价（万元）")
plt.grid()
plt.tight_layout()
plt.show()
'''.replace(' df_placeholder','df["每平米价格"] = df["房价(万元)"] / df["房屋面积(㎡)"]')
csvtext='房屋编号,房屋面积(㎡),房间数,房龄(年),房价(万元)\n1,120,3,5,450\n2,90,2,10,320\n3,150,4,2,680\n4,80,2,15,280\n5,100,3,8,400\n'
assets={'pythagoras_tree.py':tree,'house_analysis.py':data,'house_price.csv':csvtext}
for name,value in assets.items(): (root/name).write_text(value,encoding='utf-8-sig' if name.endswith('.csv') else 'utf-8')
section='''<section class="section" id="complete"><h2>进阶跟做：真正的毕达哥拉斯树</h2><p class="lead">观察正方形、直角三角形和两个较小正方形的递归关系。</p><div class="card"><canvas id="squareTree" style="width:100%;height:400px" aria-label="毕达哥拉斯树分层动画"></canvas><div class="controls"><button id="sqNext">长一层</button><button id="sqPlay">自动演示</button><button id="sqReset">重来</button><span id="sqStatus" aria-live="polite"></span></div><p>把大正方形的边长当作 5，两个小正方形的边长就是 3 和 4：3² + 4² = 5²。因此分支长度分别是原来的 0.6 和 0.8。动画中的虚线表示三角形的两条直角边。</p><p>按顺序试：①只画一层；②改成两层，找到两个小正方形；③观察每次调用的长度和层数都在变小。下面代码用坐标直接画四个顶点，递归返回后无需恢复海龟方向。</p></div>'''
for title,name in [('完整画树代码（教学改编）','pythagoras_tree.py'),('完整数据分析代码（教学改编）','house_analysis.py')]:
 section+=f'<div class="card"><h3>{title}</h3><p><a href="{name}" download>下载 {name}</a></p><details><summary>展开完整代码</summary><pre class="code">{html.escape(assets[name])}</pre></details></div>'
section+='''<div class="card"><h3>下载数据，亲自运行</h3><p><a href="house_price.csv" download>下载 house_price.csv（自编练习数据，5条）</a>，与 house_analysis.py 放在同一文件夹。用装好 pandas、matplotlib 的 Python 在 IDLE 打开程序，按 F5 运行。网页动画是 JavaScript 演示；Python 代码需要在电脑上运行。</p><p>核对结果：平均房间数 <b>2.8</b>；最大房龄 <b>15</b>；最高每平米价格约 <b>4.5333 万元/㎡</b>，对应编号 <b>3</b>。原教程四行示意数据的平均值是 2.75，下载版增加了第5行。</p><p>再挑战：把编号5的房价改成500，再运行。它的单价会变为5万元/㎡，最高记录应该变成编号5。</p><p>遇到 KeyError：先 print(df.columns)，逐字核对列名和括号。遇到 FileNotFoundError：检查文件名及程序与 CSV 是否在同一文件夹。中文变成方框：换成电脑上已安装的中文字体。</p><p class="small">资料线索：<a href="https://www.cnblogs.com/kkman2000/p/23242753">kkman2000 的赛事整理</a>。该文称样题来自官方任务书；此处未独立核验附件来源。海淀信息不能代替西城区正式规则。</p></div></section>'''
s=s.replace('<section class="section" id="practice">',section+'<section class="section" id="practice">')
s=s.replace('<a href="#practice">','<a href="#complete">完整跟做</a><a href="#practice">')
js='''
(()=>{const c=document.getElementById('squareTree'),g=c.getContext('2d');let n=1,clock=null;
function build(x,y,s,a,d,out){if(d===0)return;let u=[Math.cos(a),Math.sin(a)],v=[-u[1],u[0]],B=[x+s*u[0],y+s*u[1]],D=[x+s*v[0],y+s*v[1]],C=[B[0]+s*v[0],B[1]+s*v[1]],P=[D[0]+.36*s*u[0]+.48*s*v[0],D[1]+.36*s*u[1]+.48*s*v[1]];out.push({points:[[x,y],B,C,D],roof:[D,P,C],d});build(...D,s*.6,a+Math.atan2(4,3),d-1,out);build(...P,s*.8,a-Math.atan2(3,4),d-1,out)}
function paint(){let all=[];build(0,0,100,0,n,all);let pts=all.flatMap(q=>[...q.points,...q.roof]),xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]),loX=Math.min(...xs),hiX=Math.max(...xs),loY=Math.min(...ys),hiY=Math.max(...ys),w=c.clientWidth,h=c.clientHeight,ratio=devicePixelRatio||1;c.width=w*ratio;c.height=h*ratio;g.setTransform(ratio,0,0,ratio,0,0);g.clearRect(0,0,w,h);let scale=Math.min((w-40)/(hiX-loX),(h-40)/(hiY-loY));function path(pts,close){g.beginPath();pts.forEach((p,i)=>g[i?'lineTo':'moveTo']((w-(hiX-loX)*scale)/2+(p[0]-loX)*scale,h-20-(p[1]-loY)*scale));if(close)g.closePath()}all.forEach(q=>{g.setLineDash([]);path(q.points,true);g.fillStyle=`hsl(${145+(n-q.d)*17} 55% 80%)`;g.fill();g.strokeStyle='#245b54';g.stroke();g.setLineDash([3,4]);path(q.roof,false);g.stroke();});g.setLineDash([]);document.getElementById('sqStatus').textContent=`${n} 层 · ${all.length} 个正方形（每层画面会自动缩放）`;}
document.getElementById('sqNext').onclick=()=>{n=Math.min(7,n+1);paint()};document.getElementById('sqReset').onclick=()=>{clearInterval(clock);clock=null;n=1;paint()};document.getElementById('sqPlay').onclick=()=>{clearInterval(clock);if(n===7)n=1;paint();clock=setInterval(()=>{n++;paint();if(n===7){clearInterval(clock);clock=null}},900)};window.addEventListener('resize',paint);paint();})();
'''
s=s.replace('</script>',js+'</script>');p.write_text(s)
