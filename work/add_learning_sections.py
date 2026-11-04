# coding: utf-8
from pathlib import Path
import re, zipfile
root=Path('public'); page=root/'digital-literacy.html';s=page.read_text()
# Python fundamentals section, placed between warm-up and data analysis.
python_part='''<section class="section" id="python-basics"><h2>Python 基本操作</h2><p class="lead">用 IDLE 打开 .py 文件，按 F5 运行；Shell 窗口显示 print 的结果。Python 用换行分隔语句，用冒号和缩进表示代码块。</p><div class="grid"><article class="card"><h3>导入、打印和赋值</h3><pre class="code"># import 把需要的工具模块载入程序
import turtle
import pandas as pd

# print 把文字或计算结果显示在 Shell
print("开始练习")
score = 90
print(score)</pre><p><code>import pandas as pd</code> 给 pandas 起简短别名 <code>pd</code>；<code>score = 90</code> 把数值保存到变量里。</p></article><article class="card"><h3>if、冒号和缩进</h3><pre class="code">score = 90

# if 后面写条件；冒号表示下面开始一个代码块
if score >= 60:
    # 代码块必须缩进，通常是4个空格
    print("通过")
else:
    print("继续练习")</pre><p>冒号后换行，并把属于 if 或 else 的语句缩进。缩进层级对齐，Python 才知道哪些语句属于同一块。</p></article></div><div class="card"><h3>函数、return 与 while</h3><pre class="code">def double(number):
    # return 把结果交还给调用函数的位置，并结束本次函数
    return number * 2

count = 0
while count < 3:
    # while 条件为真时重复执行缩进的代码
    print(double(count))
    count = count + 1  # 更新变量，避免循环一直不结束</pre><p>在 IDLE 编辑器中保存为 .py，再按 F5 运行。报错时先看 Shell 最后一行错误提示，再检查冒号、缩进、括号和变量名。</p></div></section>'''
assert '<section class="section" id="data">' in s
s=s.replace('<section class="section" id="data">',python_part+'<section class="section" id="data">',1)
# Add navigation links without duplicating existing links.
s=s.replace('<a href="#python">Python 热身</a>','<a href="#python">Python 热身</a><a href="#python-basics">Python 基本操作</a><a href="#pandas-basics">pandas 行列与运算</a><a href="#turtle-basics">turtle 与递归</a>',1)
# Add pandas core concepts to the start of data task section.
pandas_part='''<div class="card" id="pandas-basics"><h3>pandas：表格、行列和计算</h3><p>pandas 是处理表格数据的工具。<code>DataFrame</code> 可以理解成一张表：每一列有列名，每一行是一条记录。下面用小表演示常用操作。</p><pre class="code">import pandas as pd

# 字典中的每个列表代表一列；相同位置的数据组成一行
scores = pd.DataFrame({
    "姓名": ["小明", "小红", "小刚"],
    "语文": [80, 92, 75],
    "数学": [90, 88, 85]
})

# 用列名访问整列
print(scores["数学"])

# .loc[行标签, 列名] 访问指定行和列；这里行标签0是第一行
print(scores.loc[0, "姓名"])

# 用切片选取多行、多列；: 表示该方向取全部
print(scores.loc[0:1, ["姓名", "语文"]])

# 两列可以逐行相加，结果保存为新列
scores["总分"] = scores["语文"] + scores["数学"]

# groupby 按班级分组；sum 对每组的数值列求和
scores["班级"] = ["一班", "一班", "二班"]
print(scores.groupby("班级")["总分"].sum())</pre><p><b>记住：</b><code>表["列名"]</code>取列；<code>表.loc[行标签, "列名"]</code>取行列交叉处；<code>新列 = 列A + 列B</code>逐行计算；<code>groupby(...).sum()</code>先分组再求和。读取 CSV 后得到的 <code>df</code> 也是 DataFrame。</p></div>'''
s=s.replace('<section class="section" id="data"><h2>任务二：从表格里找到线索</h2>', '<section class="section" id="data"><h2>任务二：从表格里找到线索</h2>'+pandas_part,1)
# Turtle guide inside tree section before the recursive code card.
turtle_part='''<div class="card" id="turtle-basics"><h3>turtle 画笔、重复与递归</h3><p><code>turtle</code> 是 Python 自带的绘图模块。先把海龟想成拿着画笔的小车：它有当前位置、朝向和落下或抬起的画笔。</p><div class="grid"><div><p><b>常用动作</b></p><ul><li><code>t.forward(80)</code>：向前画80步</li><li><code>t.left(90)</code> / <code>t.right(90)</code>：转向</li><li><code>t.penup()</code> / <code>t.pendown()</code>：移动时不画 / 开始画</li><li><code>t.goto(x, y)</code>：移动到坐标</li><li><code>t.color("green")</code>：设置颜色</li></ul></div><div><p><b>while 控制重复</b></p><pre class="code"># 重复画正方形的四条边
for i in range(4):
    t.forward(80)
    t.left(90)

# while 也可以按条件重复
count = 0
while count < 4:
    t.forward(40)
    t.left(90)
    count = count + 1</pre></div></div><div class="callout good"><b>递归的三步：</b>①检查停止条件；②画当前这一段；③调用自己画更小的部分。比如 <code>if length &lt; 10: return</code> 表示枝条够短就停止；每次把长度缩小，递归才会走向出口。函数走到 <code>return</code> 后，会回到刚才调用它的位置，继续执行后面的语句。</div><p><code>print()</code> 可以帮助观察递归：在函数里打印 <code>depth</code> 或 <code>length</code>，运行时就能看到每一层如何变小。复杂图形可以用 <code>t.tracer(False)</code> 暂停逐笔刷新，画完后用 <code>t.update()</code> 一次显示。</p></div>'''
anchor='<div class="card"><h3>递归程序里最重要的两句话</h3>'
assert anchor in s;s=s.replace(anchor,turtle_part+anchor,1)
page.write_text(s)
# Inject explanatory comments into every downloadable practice program.
comment_map={
'branch.py':{'import turtle as t':'# turtle 是 Python 自带绘图模块；as t 给模块起短名\nimport turtle as t','import math':'# math 提供数学函数，本题主算法不依赖它\nimport math','import random':'# random 用于随机数，本题主算法不依赖它\nimport random','def tree(length, depth):':'# length 是当前枝长；depth 是还要画的层数\ndef tree(length, depth):','if depth == 0:':'    # 停止条件：层数用完后立刻结束本次递归\n    if depth == 0:','return':'        # return 返回上一层调用，避免继续分叉\n        return','t.forward(length)':'    # 画当前主枝，海龟沿当前朝向前进\n    t.forward(length)','tree(length * .7, depth - 1)':'    # 递归：长度缩为0.7倍，层数减1\n    tree(length * .7, depth - 1)','t.backward(length)':'    # 回到分叉点，为另一条分支恢复起点\n    t.backward(length)'},
'natural.py':{'random.seed(7)':'# 固定随机种子，让每次生成的树形一致，方便比较\nrandom.seed(7)  # 固定种子，方便重复观察','width = max(1, depth)':'    # depth越小，画笔越细；最小宽度保持为1\n    width = max(1, depth)','color = "forestgreen" if depth <= 2 else "saddlebrown"':'    # 最末端两层画成绿色，其余枝条为棕色\n    color = "forestgreen" if depth <= 2 else "saddlebrown"','angle = random.randint(15, 40)':'    # 随机选分叉角度，范围包含15和40\n    angle = random.randint(15, 40)','tree(length * .7, depth - 1)':'    # 两个子枝都缩短并减少一层递归\n    tree(length * .7, depth - 1)','t.pencolor(color)':'    # 恢复当前枝的颜色，确保回到父层后样式正确\n    t.pencolor(color)'},
'koch.py':{'def koch(length, depth):':'# length 是当前线段长度；depth 是替换规则还要重复几层\ndef koch(length, depth):','if depth == 0:':'    # 递归出口：第0层直接画一条直线\n    if depth == 0:','return':'        return  # 直线画完，结束本次调用','koch(length / 3, depth - 1)':'    # 把当前边缩成三分之一，递归画四段之一\n    koch(length / 3, depth - 1)'},
'snowflake.py':{'def koch(length, depth):':'# 递归画一条科赫边，其他边重复调用这个函数\ndef koch(length, depth):','if depth == 0:':'    # 第0层是一条普通直线\n    if depth == 0:','for angle in [60, -120, 60, 0]:':'# 每次调用画四段子曲线，并在段间按规则转向\n    for angle in [60, -120, 60, 0]:','koch(length / 3, depth - 1)':'        # 子曲线长度缩为三分之一，层数减一\n        koch(length / 3, depth - 1)'},
'sierpinski.py':{'def triangle(x, y, size, depth):':'# x,y是三角形左下角；size是边长；depth是递归层数\ndef triangle(x, y, size, depth):','if depth == 0:':'    # 最底层画完整三角形，作为递归出口\n    if depth == 0:','half = size / 2':'    # 每个子三角形边长是父三角形的一半\n    half = size / 2','triangle(x, y, half, depth - 1)':'    # 左下角子三角形：起点不变，边长减半\n    triangle(x, y, half, depth - 1)','triangle(x + half, y, half, depth - 1)':'    # 右下角子三角形：向右移动半条边\n    triangle(x + half, y, half, depth - 1)'},
'htree.py':{'def line(x1, y1, x2, y2):':'# 用起点和终点坐标画一条直线，避免依赖海龟朝向\ndef line(x1, y1, x2, y2):','def htree(x, y, size, depth):':'# x,y是H中心；size控制大小；depth控制递归层数\ndef htree(x, y, size, depth):','if depth == 0:':'    # 没有剩余层时停止递归\n    if depth == 0:','half = size / 2':'    # 四个端点距中心各半个size\n    half = size / 2','for dx in [-half, half]:':'    # 横向和纵向各取左右/上下两个端点，共四个子H\n    for dx in [-half, half]:'},
'carpet.py':{'def carpet(x, y, size, depth):':'# x,y为正方形左下角；size为边长；depth为递归层数\ndef carpet(x, y, size, depth):','if depth == 0:':'    # 最小方块画出轮廓后停止\n    if depth == 0:','third = size / 3':'    # 九宫格每个小格边长为原正方形的三分之一\n    third = size / 3','for row in range(3):':'    # row和col分别枚举九宫格的行与列\n    for row in range(3):','if row == 1 and col == 1:':'            # 跳过正中间的小格，形成地毯的孔\n            if row == 1 and col == 1:'},
'hilbert.py':{'def hilbert(depth, angle, step):':'# depth是递归层数，angle控制转向，step是每段长度\ndef hilbert(depth, angle, step):','if depth == 0:':'    # 第0层不画，作为递归出口\n    if depth == 0:','return':'        return','hilbert(depth - 1, -angle, step)':'    # 子曲线层数减1；负角度让曲线反向转弯\n    hilbert(depth - 1, -angle, step)','t.forward(step)':'    # 画连接子曲线的直线段\n    t.forward(step)'},
'passenger_stats.py':{'import pandas as pd':'# pandas提供DataFrame表格处理功能\nimport pandas as pd','import matplotlib.pyplot as plt':'# pyplot负责创建和显示图表\nimport matplotlib.pyplot as plt','df = pd.read_csv("passengers.csv")':'# 读取同目录CSV文件，结果df是一个DataFrame\ndf = pd.read_csv("passengers.csv")','print(df.head())':'# head默认显示前5行，先确认读取和列名正确\nprint(df.head())','print("平均年龄", df["年龄"].mean())':'# 先按列名取年龄列，再用mean计算平均值\nprint("平均年龄", df["年龄"].mean())','print("最高票价", df["票价"].max())':'# max计算票价列的最大值\nprint("最高票价", df["票价"].max())','print(df[df["票价"] == df["票价"].max()])':'# 条件筛选整行；相等判断使用双等号==\nprint(df[df["票价"] == df["票价"].max()])'},
'air_stats.py':{'import pandas as pd':'# pandas用于读取CSV并按列统计\nimport pandas as pd','import matplotlib.pyplot as plt':'# pyplot用于画折线图\nimport matplotlib.pyplot as plt','df = pd.read_csv("air.csv")':'# 读取CSV为DataFrame，每行是一条时刻记录\ndf = pd.read_csv("air.csv")','for station in ["A站", "B站"]:':'# 循环处理两个监测站的列名\nfor station in ["A站", "B站"]:','print(station, "均值", df[station].mean(), "最大值", df[station].max())':'    # df[station]访问当前数值列；mean和max分别求均值、最大值\n    print(station, "均值", df[station].mean(), "最大值", df[station].max())','plt.plot(df["时刻"], df[station], marker="o", label=station)':'    # 横轴用时刻，纵轴用监测值；label供图例显示\n    plt.plot(df["时刻"], df[station], marker="o", label=station)'},
'air_compare.py':{'df = pd.read_csv("air.csv")':'# 读取两站监测表\ndf = pd.read_csv("air.csv")','df["差值"] = df["A站"] - df["B站"]':'# 两列按行相减，生成新列；正数表示A站更高\ndf["差值"] = df["A站"] - df["B站"]','df["比值"] = df["A站"] / df["B站"]':'# 两列逐行相除；要确保除数不为0\ndf["比值"] = df["A站"] / df["B站"]','df["绝对差"] = df["差值"].abs()':'# abs取绝对值，用来比较差异大小，不看正负方向\ndf["绝对差"] = df["差值"].abs()','print("最大差值记录", df[df["差值"] == df["差值"].max()])':'# 先求最大差值，再用条件筛选对应记录\nprint("最大差值记录", df[df["差值"] == df["差值"].max()])'},
'country_stats.py':{'df = pd.read_csv("countries.csv")':'# 读取国家、年份和指标组成的表格\ndf = pd.read_csv("countries.csv")','selected = df[df["年份"] == 2010]':'# 用条件表达式筛选出2010年的行\nselected = df[df["年份"] == 2010]','print("2010年平均", selected["人均指标"].mean())':'# 在筛出的子表上取指标列并求平均数\nprint("2010年平均", selected["人均指标"].mean())','country = df[df["国家"] == "甲国"].sort_values("年份")':'# 先按国家筛行，再按年份排序，保证折线按时间顺序连接\ncountry = df[df["国家"] == "甲国"].sort_values("年份")'},
'group_stats.py':{'df = pd.read_csv("passengers.csv")':'# 读入乘客记录表，df是DataFrame\ndf = pd.read_csv("passengers.csv")','summary = df.groupby("舱位")["票价"].agg(["count", "mean"])':'# groupby按舱位分组；count计数，mean算每组平均票价\nsummary = df.groupby("舱位")["票价"].agg(["count", "mean"])','print(summary)':'# 打印每组的统计汇总表\nprint(summary)','print("平均票价最高的舱位", summary[summary["mean"] == summary["mean"].max()])':'# 在汇总表中筛出平均票价等于最大均价的组\nprint("平均票价最高的舱位", summary[summary["mean"] == summary["mean"].max()])'}
}
# Avoid duplicate inline comments when regenerating: comment insertion works from raw source only.
for filename,mapping in comment_map.items():
 p=root/'practice'/filename;raw=p.read_text();
 for old,new in mapping.items():
  if old in raw and new not in raw: raw=raw.replace(old,new,1)
 p.write_text(raw)
# Rebuild the zip with all commented scripts and accompanying CSVs.
with zipfile.ZipFile(str(root/'practice'/'practice-pack.zip'),'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((root/'practice').iterdir()):
  if p.suffix in ['.py','.csv']:z.write(str(p),p.name)
