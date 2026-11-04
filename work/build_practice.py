# coding: utf-8
from pathlib import Path
import html,json,zipfile
root=Path('public');dest=root/'practice';dest.mkdir(exist_ok=True)
head='import turtle as t\nimport math\nimport random\n\nt.setup(900, 700)\nt.speed(0)\nt.tracer(False)\nt.ht()\n\n'
end='\nt.update()\nt.done()\n'
programs={
'branch':'''def tree(length, depth):
    if depth == 0:
        return
    t.forward(length)
    t.left(25)
    tree(length * .7, depth - 1)
    t.right(50)
    tree(length * .7, depth - 1)
    t.left(25)
    t.backward(length)  # 回到进入本次调用的位置

t.penup()
t.goto(0, -220)
t.setheading(90)
t.pendown()
tree(110, 7)
''',
'natural':'''random.seed(7)  # 固定种子，方便重复观察

def tree(length, depth):
    if depth == 0:
        return
    width = max(1, depth)
    color = "forestgreen" if depth <= 2 else "saddlebrown"
    t.pensize(width)
    t.pencolor(color)
    t.forward(length)
    angle = random.randint(15, 40)
    t.left(angle)
    tree(length * .7, depth - 1)
    t.right(angle * 2)
    tree(length * .7, depth - 1)
    t.left(angle)
    # 子树会修改颜色和粗细，返回后恢复再画回程
    t.pensize(width)
    t.pencolor(color)
    t.backward(length)

t.penup()
t.goto(0, -220)
t.setheading(90)
t.pendown()
tree(100, 7)
''',
'koch':'''def koch(length, depth):
    if depth == 0:
        t.forward(length)
        return
    koch(length / 3, depth - 1)
    t.left(60)
    koch(length / 3, depth - 1)
    t.right(120)
    koch(length / 3, depth - 1)
    t.left(60)
    koch(length / 3, depth - 1)

t.penup()
t.goto(-300, -90)
t.pendown()
koch(600, 4)
''',
'snowflake':'''def koch(length, depth):
    if depth == 0:
        t.forward(length)
        return
    for angle in [60, -120, 60, 0]:
        koch(length / 3, depth - 1)
        t.left(angle)

t.penup()
t.goto(-200, 120)
t.pendown()
for i in range(3):
    koch(400, 3)
    t.right(120)
''',
'sierpinski':'''def triangle(x, y, size, depth):
    if depth == 0:
        t.penup()
        t.goto(x, y)
        t.setheading(0)
        t.pendown()
        for i in range(3):
            t.forward(size)
            t.left(120)
        return
    half = size / 2
    triangle(x, y, half, depth - 1)
    triangle(x + half, y, half, depth - 1)
    triangle(x + half / 2, y + half * math.sqrt(3) / 2,
             half, depth - 1)

triangle(-260, -220, 520, 4)
''',
'htree':'''def line(x1, y1, x2, y2):
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.goto(x2, y2)

def htree(x, y, size, depth):
    if depth == 0:
        return
    half = size / 2
    line(x - half, y, x + half, y)
    line(x - half, y - half, x - half, y + half)
    line(x + half, y - half, x + half, y + half)
    for dx in [-half, half]:
        for dy in [-half, half]:
            htree(x + dx, y + dy, size / 2, depth - 1)

htree(0, 0, 270, 4)
''',
'carpet':'''def carpet(x, y, size, depth):
    if depth == 0:
        t.penup()
        t.goto(x, y)
        t.setheading(0)
        t.pendown()
        for i in range(4):
            t.forward(size)
            t.left(90)
        return
    third = size / 3
    for row in range(3):
        for col in range(3):
            if row == 1 and col == 1:
                continue  # 中间留空
            carpet(x + col * third, y + row * third,
                   third, depth - 1)

carpet(-240, -240, 480, 3)
''',
'hilbert':'''def hilbert(depth, angle, step):
    if depth == 0:
        return
    t.left(angle)
    hilbert(depth - 1, -angle, step)
    t.forward(step)
    t.right(angle)
    hilbert(depth - 1, angle, step)
    t.forward(step)
    hilbert(depth - 1, angle, step)
    t.right(angle)
    t.forward(step)
    hilbert(depth - 1, -angle, step)
    t.left(angle)

depth = 4
t.penup()
t.goto(-240, -240)
t.pendown()
hilbert(depth, 90, 480 / (2 ** depth - 1))
'''}
R='https://runestone.academy/ns/books/published/httlacs/intro-recursion_programming-exercises.html'
U='https://www.cs.utexas.edu/~novak/cs307asg06.html'
C='https://www.cs.cornell.edu/courses/cs1110/2009fa/assignments/a5/a5.html'
M='https://www.cs.middlebury.edu/~cs101/homework/hw04.html'
tasks=[
('branch','二叉分形树','基础','画出7层树：每次分两支，长度变为0.7倍，左右各偏转25°。','先画主干；递归完成后必须回到原来的位置和方向。','把角度改成15°和35°，比较树冠宽度。',U),
('natural','会变色的自然树','基础进阶','把末端两层变成绿色，主干较粗，分叉角度在15°—40°之间随机变化。','返回父树枝时，恢复画笔粗细和颜色。','换一个随机种子，保持停止条件不变。',R),
('koch','科赫曲线','中等','将每条线替换成四段等长小线，形成三角凸起；绘制0—4层。','每段是原长的三分之一；转向依次为左60°、右120°、左60°。','第4层应有256条最小线段。',U),
('snowflake','科赫雪花','中等','将三条科赫曲线连接成一个闭合雪花，默认递归3层。','每画完一条大边向右转120°，总共三条大边。','检查起点与终点重合；三层共192条小线段。',U),
('sierpinski','谢尔宾斯基三角形','中等','只画三个角上的半尺寸三角形，中心留空，递归4层。','先解决0层的等边三角形，再确定三个小三角形的起点。','4层有81个最小三角形。',C),
('htree','H 树','中等','先画一个H，在四个端点递归画半尺寸H，共4层。','用中心坐标和尺寸定义每个H，三个线段就能画一个。','4层有85个H，共255条线段。',C),
('carpet','谢尔宾斯基地毯','拓展','把正方形分成九宫格，跳过中心，在其他8格递归，共3层。','用两层for循环枚举行列；0层画正方形轮廓。本版用轮廓表示保留方块。','3层有512个最小正方形。',M),
('hilbert','希尔伯特曲线','挑战','用递归画4层连续折线；不抬笔，所有转向都是90°。','递归有4次调用，子调用角度有正有负；先观察1层和2层。','4层有255条线段。',R)]

# 给参考代码加适合初学者的中文注释。按完整代码行匹配，并保留原缩进。
EXPLANATIONS = {
'branch.py': {
'import turtle as t':'# turtle是Python自带的绘图模块；起别名t后，后面可以用t调用它。',
'import math':'# math提供sqrt等数学函数。',
'import random':'# random提供随机数和随机选择功能。',
'import pandas as pd':'# pandas提供DataFrame表格和CSV处理功能。',
'import matplotlib.pyplot as plt':'# pyplot提供折线图、柱状图等绘图命令。',
't.setup(900, 700)':'# 设置绘图窗口的宽度和高度。',
't.speed(0)':'# 使用最快绘图速度。',
't.tracer(False)':'# 暂停逐笔刷新，减少递归绘图等待。',
't.ht()':'# 隐藏海龟图标，让图形更清楚。',
't.update()':'# 一次性显示已经完成的图形。',
't.done()':'# 保持绘图窗口打开，直到手动关闭。',
'def tree(length, depth):':'# length表示当前枝长，depth表示还要画几层。',
'    if depth == 0:':'    # 递归出口：层数用完后停止。',
'        return':'        # return结束本次函数，并回到上一层调用的位置。',
't.forward(length)':'    # 海龟沿当前朝向画出这一段树枝。',
'tree(length * .7, depth - 1)':'    # 递归画更短的树枝，同时把层数减1。',
't.backward(length)  # 回到进入本次调用的位置':'    # 沿原路退回分叉点，接着绘制另一根树枝。'},
'natural.py': {
'import turtle as t':'# turtle模块提供画笔、移动和转向命令。',
'import random':'# random模块为每次分叉随机选择角度。',
'random.seed(7)  # 固定种子，方便重复观察':'# 固定随机种子，让每次生成的树都一样，方便比较。',
'def tree(length, depth):':'# 每次调用先画当前树枝，再递归画左右两根小树枝。',
'    if depth == 0:':'    # 到达最后一层时停止，这是递归出口。',
'    width = max(1, depth)':'    # 层数越高，树枝画得越粗；最细仍保留1像素。',
'    color = "forestgreen" if depth <= 2 else "saddlebrown"':'    # 最末两层用绿色，较粗的树枝用棕色。',
'    angle = random.randint(15, 40)':'    # randint会包含两个端点，所以角度可能是15度或40度。',
'tree(length * .7, depth - 1)':'    # 子枝长度缩到原来的70%，递归层数减1。',
't.backward(length)':'    # 画完子枝后回到分叉点，让上一层继续绘图。'},
'koch.py': {
'import turtle as t':'# turtle是Python自带的绘图模块。',
'def koch(length, depth):':'# 递归地替换一段线；length和depth分别表示长度和层数。',
'    if depth == 0:':'    # depth为0时画一条直线，然后停止。',
'        t.forward(length)':'        # 画出最小的一段线。',
'        return':'# 当前线段画完，return回到调用它的位置。',
'    koch(length / 3, depth - 1)':'    # 子线段长度缩为三分之一，递归层数减1。',
't.left(60)':'    # 转向，画出向外凸起的三角形部分。'},
'snowflake.py': {
'import turtle as t':'# turtle提供画笔和移动命令。',
'def koch(length, depth):':'# 递归绘制雪花的一条边。',
'    if depth == 0:':'    # 递归出口是一条直线段。',
'        t.forward(length)':'# 画出最短的边。',
'        return':'# 停止这一支递归，并返回调用位置。',
'    for angle in [60, -120, 60, 0]:':'    # 四段较小曲线和对应转向组成一段科赫曲线。',
'        koch(length / 3, depth - 1)':'        # 边长缩为三分之一，层数减1后继续递归。',
'for i in range(3):':'# 三条相同的科赫曲线组成封闭雪花。',
't.right(120)':'    # 每到一个外角，就按相同角度转向。'},
'sierpinski.py': {
'import turtle as t':'# turtle用来绘制三角形的边。',
'import math':'# math.sqrt(3)用于计算等边三角形的高度比例。',
'def triangle(x, y, size, depth):':'# x、y指定左下角位置，size和depth控制大小与层数。',
'    if depth == 0:':'    # 到达递归出口时，画出一个完整的小三角形。',
'        t.penup()':'        # 移动到起点时抬起画笔，避免留下多余连线。',
'        t.pendown()':'        # 放下画笔，开始绘制三条边。',
'    half = size / 2':'    # 每个子三角形的边长是父三角形的一半。',
'    triangle(x, y, half, depth - 1)':'    # 递归绘制左下方的子三角形。',
'    triangle(x + half, y, half, depth - 1)':'    # 递归绘制右下方的子三角形。',
'    triangle(x + half / 2, y + half * math.sqrt(3) / 2,':'    # 递归绘制上方的子三角形。',
'             half, depth - 1)':'# 递归绘制上方的子三角形。'},
'htree.py': {
'import turtle as t':'# turtle用来绘制H形线段。',
'def line(x1, y1, x2, y2):':'# 根据起点和终点坐标画一条线段。',
't.goto(x1, y1)':'    # 抬笔移动到线段起点，不画连接线。',
't.goto(x2, y2)':'    # 从起点落笔，画到终点。',
'def htree(x, y, size, depth):':'# x、y是H的中心，size和depth控制大小与递归层数。',
'    if depth == 0:':'    # 没有更小的H要画时，停止递归。',
'    half = size / 2':'    # H的每个端点距离中心都是边长的一半。',
'    for dx in [-half, half]:':'    # 依次处理这个H的左端和右端。',
'        for dy in [-half, half]:':'        # 在每一端的上方和下方继续递归画小H。'},
'carpet.py': {
'import turtle as t':'# turtle用来绘制地毯中保留的正方形轮廓。',
'def carpet(x, y, size, depth):':'# x、y是正方形左下角坐标；size和depth控制大小与层数。',
'    if depth == 0:':'    # 到达递归出口时，画出最小的保留正方形。',
'        t.penup()':'        # 抬笔移动到正方形角点，不留下线。',
'        t.pendown()':'        # 依次画出正方形的四条边。',
'    third = size / 3':'    # 把父正方形分成九个大小相同的小格。',
'    for row in range(3):':'    # row和col分别表示九宫格中的行号和列号。',
'        for col in range(3)':'# Visit each of the three columns in this row.',
'            if row == 1 and col == 1:':'            # 跳过正中间的小格，留下地毯的空洞。',
'            carpet(x + col * third, y + row * third,':'            # 对其余八个小格继续递归。'},
'hilbert.py': {
'import turtle as t':'# turtle用来绘制连续的希尔伯特曲线。',
'def hilbert(depth, angle, step):':'# depth是递归层数，angle是转向角度，step是每段长度。',
'    if depth == 0:':'    # 递归出口：第0层不再绘制曲线。',
'        return':'# 结束这一支递归，回到上一层调用。',
'    t.left(angle)':'    # 转向，确定第一段子曲线的朝向。',
'    hilbert(depth - 1, -angle, step)':'    # 反转转向方向，递归绘制较小曲线。',
't.forward(step)':'    # 画一条直线，把相邻的子曲线连接起来。',
'    hilbert(depth - 1, angle, step)':'    # 保持当前朝向，递归绘制下一段子曲线。',
'depth = 4':'# 设置4层递归，图形较完整且仍容易观察。',
't.penup()':'# 开始绘图前先抬笔移动到起点。',
't.pendown()':'# 落笔，开始绘制曲线。'},
'passenger_stats.py': {
'import pandas as pd':'# pandas读取CSV表格，并提供DataFrame数据操作。',
'import matplotlib.pyplot as plt':'# pyplot负责创建和显示图表。',
'df = pd.read_csv("passengers.csv")':'# 读取同文件夹中的CSV，并保存为DataFrame变量df。',
'print(df.head())':'# 显示前5行，检查数据和列名是否正确。',
'print("平均年龄", df["年龄"].mean())':'# 先选取年龄列，再用mean()计算平均值。',
'print("最高票价", df["票价"].max())':'# max()返回票价列中的最大值。',
'print(df[df["票价"] == df["票价"].max()])':'# 筛选票价等于最大值的行；==用于比较是否相等。',
'plt.plot(df["编号"], df["票价"], marker="o")':'# 横轴为乘客编号、纵轴为票价；marker为每条记录加圆点。',
'plt.xlabel("编号")':'# 设置横轴标签。',
'plt.ylabel("票价")':'# 设置纵轴标签。',
'plt.show()':'# 打开图表窗口。'},
'air_stats.py': {
'import pandas as pd':'# pandas读取监测站表格并进行统计。',
'import matplotlib.pyplot as plt':'# pyplot绘制两个监测站的折线。',
'df = pd.read_csv("air.csv")':'# 把CSV读入DataFrame；每行对应一个时刻。',
'for station in ["A站", "B站"]:':'# 用循环依次处理两个监测站的数据列。',
'    print(station, "均值", df[station].mean(), "最大值", df[station].max())':'    # 按列名取一列，再计算平均值和最大值。',
'print(df[df["A站"] == df["A站"].max()])':'# 筛选表格，找出A站达到最大值的时刻。',
'    plt.plot(df["时刻"], df[station], marker="o", label=station)':'    # x轴是时刻，y轴是读数；label设置曲线名称。',
'plt.legend()':'# 显示两条曲线的图例。'},
'air_compare.py': {
'import pandas as pd':'# pandas读取CSV并计算数据列。',
'import matplotlib.pyplot as plt':'# pyplot绘制差值图。',
'df = pd.read_csv("air.csv")':'# 将监测站读数载入DataFrame。',
'df["差值"] = df["A站"] - df["B站"]':'# 对应行相减，创建差值列。',
'df["比值"] = df["A站"] / df["B站"]':'# 对应行相除；除数不能为0。',
'df["绝对差"] = df["差值"].abs()':'# abs()取绝对值，比较差距大小时不看正负方向。',
'print(df)':'# 显示原始列和新计算的列。',
'print("最大差值记录", df[df["差值"] == df["差值"].max()])':'# 找出带正负方向的差值中最大的一行。',
'print("最大绝对差记录", df[df["绝对差"] == df["绝对差"].max()])':'# 找出不考虑方向时差距最大的一行。',
'plt.plot(df["时刻"], df["差值"], marker="o")':'# 绘制差值随时间变化的折线。',
'plt.show()':'# 显示完成的图表。'},
'country_stats.py': {
'import pandas as pd':'# pandas读取、筛选并排序国家数据表。',
'import matplotlib.pyplot as plt':'# pyplot绘制按年份变化的折线。',
'df = pd.read_csv("countries.csv")':'# 将CSV记录读入DataFrame。',
'selected = df[df["年份"] == 2010]':'# 只保留年份为2010的行。',
'print("2010年平均", selected["人均指标"].mean())':'# 选取指标列，计算2010年的平均值。',
'print("最大记录", selected[selected["人均指标"] == selected["人均指标"].max()])':'# 在2010年的数据中筛选数值最大的一行。',
'country = df[df["国家"] == "甲国"].sort_values("年份")':'# 先筛选一个国家，再按年份排序后绘图。',
'plt.plot(country["年份"], country["人均指标"], marker="o")':'# 根据已有年份记录绘制折线。',
'plt.show()':'# 显示绘制完成的图表。'},
'group_stats.py': {
'import pandas as pd':'# pandas对行分组并计算统计结果。',
'import matplotlib.pyplot as plt':'# pyplot绘制统计结果柱状图。',
'df = pd.read_csv("passengers.csv")':'# 将乘客记录载入DataFrame。',
'summary = df.groupby("舱位")["票价"].agg(["count", "mean"])':'# groupby按舱位分组；count计数，mean计算每组平均票价。',
'print(summary)':'# 打印每个舱位的人数和平均票价。',
'print("平均票价最高的舱位", summary[summary["mean"] == summary["mean"].max()])':'# 筛选平均票价等于各组最高均价的舱位。',
'plt.bar(summary.index.astype(str), summary["mean"])':'# 柱高表示平均票价，横轴标签表示舱位。',
'plt.show()':'# 显示绘制完成的图表。'}
}
def explain(filename, text):
    rules={key.strip(): value.lstrip() for key, value in EXPLANATIONS.get(filename,{}).items()}
    out=[]
    for line in text.splitlines():
        key=line.strip()
        comment=rules.get(key)
        if comment:
            assert comment.lstrip().startswith("#"), (filename, key, comment)
            out.append(line[:len(line)-len(line.lstrip())] + comment)
        out.append(line)
    return "\n".join(out) + "\n"

for key,body in programs.items(): (dest/(key+'.py')).write_text(explain(key + '.py', '# 教学改编练习，非赛事真题\n'+head+body+end))
# 小型自编数据，沿用公开教程主题，不冒充真实观测记录。
(dest/'passengers.csv').write_text('编号,年龄,票价,舱位\n1,12,20,3\n2,36,80,1\n3,28,35,2\n4,45,90,1\n5,16,25,3\n6,33,40,2\n7,60,100,1\n8,22,30,3\n9,40,50,2\n10,18,30,3\n',encoding='utf-8-sig')
(dest/'air.csv').write_text('时刻,A站,B站\n8,20,25\n9,25,20\n10,30,28\n11,35,30\n12,40,32\n13,30,25\n14,25,22\n15,20,18\n16,15,15\n17,10,12\n',encoding='utf-8-sig')
(dest/'countries.csv').write_text('国家,年份,人均指标\n甲国,2000,1000\n甲国,2005,1200\n甲国,2010,1500\n乙国,2000,2000\n乙国,2005,2100\n乙国,2010,2400\n丙国,2000,800\n丙国,2005,1100\n丙国,2010,1800\n丁国,2000,1500\n丁国,2005,1600\n丁国,2010,1900\n',encoding='utf-8-sig')
dhead='''# 教学改编；CSV为自编模拟数据，非真实乘客或环境观测。
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei", "PingFang SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

'''
P='https://pandas.pydata.org/docs/getting_started/intro_tutorials/'
dtasks=[
('passenger_stats','乘客年龄与票价','基础','passengers.csv','显示前5行；求平均年龄和最高票价；找出最高票价记录；筛选年龄大于35的记录；画编号与票价折线图。','平均年龄31；最高票价100；对应编号7；大于35岁的编号为2、4、7、9。',P+'06_calculate_statistics.html','''df = pd.read_csv("passengers.csv")
print(df.head())
print("平均年龄", df["年龄"].mean())
print("最高票价", df["票价"].max())
print(df[df["票价"] == df["票价"].max()])
print("年龄大于35", df[df["年龄"] > 35])
plt.plot(df["编号"], df["票价"], marker="o")
plt.xlabel("编号")
plt.ylabel("票价")
plt.title("各乘客票价")
'''),
('air_stats','空气质量观察','基础','air.csv','显示前5行；分别求A站、B站均值和最大值；找出A站最大值的时刻；画两站观测值折线图。','A站平均25、最大40；B站平均22.7、最大32；A站最高出现在12时。',P+'04_plotting.html','''df = pd.read_csv("air.csv")
print(df.head())
for station in ["A站", "B站"]:
    print(station, "均值", df[station].mean(), "最大值", df[station].max())
print(df[df["A站"] == df["A站"].max()])
for station in ["A站", "B站"]:
    plt.plot(df["时刻"], df[station], marker="o", label=station)
plt.legend()
plt.xlabel("时刻")
plt.ylabel("模拟浓度")
plt.title("两站观测记录")
'''),
('air_compare','监测站差值与比值','中等','air.csv','新增差值=A站−B站、比值=A站÷B站；求差值最大记录；另求绝对差最大的记录；画差值折线图。','最大差值8，出现在12时；最大绝对差也是8。8时差值为−5，不要把差值与绝对差混淆。',P+'05_add_columns.html','''df = pd.read_csv("air.csv")
# 除法前确认分母不为0；本模拟数据无缺失值
assert df["B站"].notna().all() and (df["B站"] != 0).all()
df["差值"] = df["A站"] - df["B站"]
df["比值"] = df["A站"] / df["B站"]
df["绝对差"] = df["差值"].abs()
print(df)
print("最大差值记录", df[df["差值"] == df["差值"].max()])
print("最大绝对差记录", df[df["绝对差"] == df["绝对差"].max()])
plt.plot(df["时刻"], df["差值"], marker="o")
plt.xlabel("时刻")
plt.ylabel("A站减B站")
plt.title("两站差值")
'''),
('country_stats','国家历年数据统计','中等','countries.csv','筛选2010年记录；求当年平均值和最大值，找出对应国家；再筛选甲国并按年份排序，画其历年折线图。','2010年平均1900、最大2400，对应乙国；甲国依次是1000、1200、1500。','https://swcarpentry.github.io/python-novice-gapminder/08-data-frames.html','''df = pd.read_csv("countries.csv")
selected = df[df["年份"] == 2010]
print("2010年平均", selected["人均指标"].mean())
print("最大记录", selected[selected["人均指标"] == selected["人均指标"].max()])
country = df[df["国家"] == "甲国"].sort_values("年份")
print(country)
plt.plot(country["年份"], country["人均指标"], marker="o")
plt.xlabel("年份")
plt.ylabel("模拟人均指标")
plt.title("甲国历年记录")
'''),
('group_stats','按舱位分类汇总','进阶','passengers.csv','按舱位统计人数和平均票价；找出平均票价最高的舱位；绘制各舱位平均票价柱状图。','1舱3人、均价90；2舱3人、均价约41.67；3舱4人、均价26.25。',P+'06_calculate_statistics.html','''df = pd.read_csv("passengers.csv")
summary = df.groupby("舱位")["票价"].agg(["count", "mean"])
print(summary)
print("平均票价最高的舱位", summary[summary["mean"] == summary["mean"].max()])
plt.bar(summary.index.astype(str), summary["mean"])
plt.xlabel("舱位")
plt.ylabel("平均票价")
plt.title("各舱位平均票价")
''')]
for key,title,level,file,task,answer,source,body in dtasks:(dest/(key+'.py')).write_text(explain(key + '.py', dhead+body+'\nplt.grid()\nplt.tight_layout()\nplt.show()\n'))
style=(root/'digital-literacy.html').read_text().split('<style>')[1].split('</style>')[0]
s='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>数智素养练习库｜小萝卜的秘密花园</title><style>'+style+'''img{width:100%;height:280px;object-fit:contain;background:#f7fbff;border-radius:12px}details{margin:12px 0}summary{cursor:pointer;font-weight:700}a{color:#3456c5}.card{margin:18px 0}pre{max-height:460px} .hero a{color:white}h4{font-size:1.05rem;color:#3456c5;margin:22px 0 8px}.explanation{border-left:3px solid #45b7a4;padding-left:16px}.explanation li{margin:8px 0}</style><header class="hero"><div class="wrap"><a href="/">← 小萝卜的秘密花园</a> · <a href="digital-literacy.html">考试准备教程</a><h1>数智素养练习库</h1><p>8道递归绘图 + 5道数据统计。每题按“题目 → 解析 → 参考答案”学习。根据公开教学材料改编，非赛事真题。</p><a href="practice/practice-pack.zip" download>下载全部练习代码与CSV →</a></div></header><nav class="nav"><div class="wrap"><a href="#turtle">递归绘图</a><a href="#data">数据处理</a><a href="#how">怎么运行</a></div></nav><main class="wrap"><section id="how" class="section"><h2>怎么练</h2><div class="card"><p>解压下载包，在IDLE中打开对应.py，按F5运行。数据程序与CSV放在同一文件夹；需要pandas和matplotlib，绘图题使用标准库turtle。网页下方是参考程序运行轨迹生成的静态预览，动画入门请看原教程。</p></div></section><section class="section" id="turtle"><h2>一、turtle 递归绘图</h2>'''
stars = {'branch':1,'natural':2,'koch':2,'snowflake':3,'sierpinski':3,'htree':3,'carpet':4,'hilbert':5,'passenger_stats':1,'air_stats':2,'air_compare':2,'country_stats':3,'group_stats':4}
analysis = {
'branch': ['停止条件是depth等于0，表示没有下一层。', '当前调用先画一根枝，再左右各调用一次；长度乘0.7，层数减1。', '每次返回前后退同样的长度，并恢复方向，这样另一支才能从分叉点开始。'],
'natural': ['递归结构与二叉树相同，先保证位置与方向能恢复。', '用depth决定粗细和颜色，越接近末端越细，最后两层用绿色。', '每次选一个随机角度，左右转动保持配对。子调用会改变画笔，所以回程前恢复父枝的样式。'],
'koch': ['0层只画直线；更高层把长度分成三份。', '一次调用依次画四段小科赫曲线，中间按左60°、右120°、左60°转向。', '四次子调用长度均为原来的三分之一，depth都减1；结束后方向与进入时相同。'],
'snowflake': ['先把一条科赫曲线封装成函数，与上一题共用递归规则。', '外层循环重复三次，每次画一条大边后向右转120°。', '先用0层检查等边三角形闭合，再增加层数；不闭合时优先检查大边转向。'],
'sierpinski': ['0层画一个完整等边三角形。', '其他层不画大三角形，只在左下、右下和上方放三个半尺寸子三角形。', '上方起点比左下向右移动原边长的四分之一、向上移动原边长乘√3再除以4。每个子调用都减一层。'],
'htree': ['用中心(x,y)、尺寸size和剩余层数定义一个H。0层返回。', '一个H由一条横线和两条竖线组成，先确定四个端点。', '在四个端点分别调用自己，尺寸减半、层数减1。坐标定位避免依赖上一次画线的方向。'],
'carpet': ['0层画保留小方块的轮廓。', '把尺寸除以3，行列各枚举0、1、2，得到九宫格起点。', '行列同时等于1时跳过，剩余八格递归。位置每次移动一格尺寸，depth减1；轮廓之间的空白形成地毯。'],
'hilbert': ['先用1层观察一个U形，0层不画线直接返回。', '每个更高层由四个低一层的子图和三条连接线组成；子图之间转90°。', '角度的正负控制子图朝向。层数变化时，用480÷(2的depth次方−1)计算步长，保持图形总宽约480。']}
danalysis = {
'passenger_stats': ['read_csv读表，head查看列名和前5行。', '选年龄列求mean，选票价列求max；用票价等于最大值的条件筛选整行，可保留并列最高记录。', '年龄大于35的条件也返回布尔序列，用它筛选df。最后把编号与票价两列交给plot，并补齐标题与轴名。'],
'air_stats': ['先确认每行对应一个时刻，A站与B站是两列数值。', '分别选列求mean和max，不要把时刻列一起算进去；再按A站最大值筛选整行，找到时刻。', '两次plot使用相同横轴，再用legend区分监测站。本练习无缺失值；真实数据应先检查缺失情况。'],
'air_compare': ['差值有正负，表示A站比B站高多少；绝对差只表示相差大小。', '先确认B站不缺失且不为0，再逐列相减、相除，结果直接赋给新列。', '分别用差值最大和绝对差最大的条件筛选记录；画差值随时刻变化图，横轴用时刻而不是行号。'],
'country_stats': ['先用年份等于2010的条件得到子表，再在子表上求平均值和最大值。', '求最大记录也必须使用2010年的子表，避免误选其他年份。', '另选甲国所有记录，按年份排序后画折线图；这展示已有历史数据，不推算未来。'],
'group_stats': ['groupby按舱位把记录分组，再选票价列。', 'count统计每组有效票价数量，mean统计平均票价；本题票价没有缺失，所以count也等于人数。', '比较汇总表的mean列找出最高组；用舱位作分类横轴、平均票价作柱高，不能把不同舱位的记录直接当成均价。']}
def explain(lines):
 return '<ol>' + ''.join('<li>'+html.escape(line)+'</li>' for line in lines) + '</ol>'
for i,(key,title,level,task,hint,challenge,source) in enumerate(tasks,1):
 code=(dest/(key+'.py')).read_text()
 s+=f'<article class="card"><span class="badge" aria-label="难度{stars[key]}星，共5星">{"★" * stars[key]}{"☆" * (5-stars[key])} · {level}</span><h3>{i}. {title}</h3><section class="problem"><h4>一、题目</h4><p>{task}</p><img src="practice/{key}.svg" alt="{title}目标图形"></section><section class="explanation"><h4>二、解析</h4>{explain(analysis[key])}</section><section class="solution"><h4>三、参考答案</h4><details><summary>展开完整代码与核对说明</summary><p><b>核对与变式：</b>{challenge}</p><a href="practice/{key}.py" download>下载Python代码</a><pre class="code">{html.escape(code)}</pre></details></section><p class="small"><a href="{source}">原始教学题目来源</a> · 本版已改写为Python标准库turtle。</p></article>'
s+='</section><section class="section" id="data"><h2>二、数据处理与统计</h2>'
for i,(key,title,level,file,task,answer,source,body) in enumerate(dtasks,1):
 code=(dest/(key+'.py')).read_text()
 s+=f'<article class="card"><span class="badge" aria-label="难度{stars[key]}星，共5星">{"★" * stars[key]}{"☆" * (5-stars[key])} · {level}</span><h3>{i}. {title}</h3><section class="problem"><h4>一、题目</h4><p>{task}</p><p><a href="practice/{file}" download>下载 {file}</a></p><details><summary>查看题目数据（模拟）</summary><pre class="code">{html.escape((dest/file).read_text(encoding="utf-8-sig"))}</pre></details></section><section class="explanation"><h4>二、解析</h4>{explain(danalysis[key])}</section><section class="solution"><h4>三、参考答案</h4><details><summary>展开完整代码与核对结果</summary><p><b>预期结果：</b>{answer}</p><a href="practice/{key}.py" download>下载Python代码</a><pre class="code">{html.escape(code)}</pre></details></section><p class="small"><a href="{source}">技能与题型来源</a> · 本题为简化改编，数据自编。</p></article>'
s+='</section></main></html>'; (root/'digital-practice.html').write_text(s)
