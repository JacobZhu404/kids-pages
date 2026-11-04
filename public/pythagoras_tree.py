# turtle用可移动的画笔绘图。
import turtle as t
# random随机选择树枝颜色。
import random
# math用于角度换算和三角函数计算。
import math

# 先画一个正方形，再递归画上方的小正方形。
def draw(x, y, size, angle, depth):
    # 停止条件：层数用完就返回。
    if depth == 0:
        return
    # 将角度换成sin和cos函数使用的弧度。
    a = math.radians(angle)
    # 底边的单位方向向量。
    ux, uy = math.cos(a), math.sin(a)
    # 与底边垂直的边方向向量。
    vx, vy = -uy, ux
    # 正方形四个顶点
    A = (x, y)
    B = (x + size * ux, y + size * uy)
    D = (x + size * vx, y + size * vy)
    C = (B[0] + size * vx, B[1] + size * vy)
    # 抬笔移动到角点，不画连接线。
    t.pu()
    t.goto(A)
    # 落笔，开始绘制正方形。
    t.pd()
    # 随机选择红、绿、蓝三个颜色分量。
    t.color(random.random(), random.random(), random.random())
    # 依次经过四个顶点，回到起点闭合正方形。
    for point in [B, C, D, A]:
        t.goto(point)
    # 直角三角形的两条直角边：0.6s 与 0.8s
    # 根据3、4、5直角三角形的比例计算屋顶顶点。
    P = (D[0] + .36 * size * ux + .48 * size * vx,
         D[1] + .36 * size * uy + .48 * size * vy)
    # 左侧子正方形边长为父正方形的3/5。
    draw(D[0], D[1], size * .6,
         angle + math.degrees(math.atan2(4, 3)), depth - 1)
    # 右侧子正方形边长为父正方形的4/5。
    draw(P[0], P[1], size * .8,
         angle - math.degrees(math.atan2(3, 4)), depth - 1)

# 设置合适大小的绘图窗口。
t.setup(900, 700)
# 暂停逐笔刷新，加快绘图速度。
t.tracer(False)
# 隐藏海龟光标。
t.ht()
draw(-60, -250, 120, 0, 7)
# 图形画完后刷新屏幕。
t.update()
# 保持绘图窗口打开，直到手动关闭。
t.done()
