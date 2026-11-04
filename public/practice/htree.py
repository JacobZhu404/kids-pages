# 教学改编练习，非赛事真题
# turtle用来绘制H形线段。
import turtle as t
import math
import random

t.setup(900, 700)
t.speed(0)
t.tracer(False)
t.ht()

# 根据起点和终点坐标画一条线段。
def line(x1, y1, x2, y2):
    t.penup()
    # 抬笔移动到线段起点，不画连接线。
    t.goto(x1, y1)
    t.pendown()
    # 从起点落笔，画到终点。
    t.goto(x2, y2)

# x、y是H的中心，size和depth控制大小与递归层数。
def htree(x, y, size, depth):
    # 没有更小的H要画时，停止递归。
    if depth == 0:
        return
    # H的每个端点距离中心都是边长的一半。
    half = size / 2
    line(x - half, y, x + half, y)
    line(x - half, y - half, x - half, y + half)
    line(x + half, y - half, x + half, y + half)
    # 依次处理这个H的左端和右端。
    for dx in [-half, half]:
        # 在每一端的上方和下方继续递归画小H。
        for dy in [-half, half]:
            htree(x + dx, y + dy, size / 2, depth - 1)

htree(0, 0, 270, 4)

t.update()
t.done()
