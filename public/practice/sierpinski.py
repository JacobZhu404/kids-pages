# 教学改编练习，非赛事真题
# turtle用来绘制三角形的边。
import turtle as t
# math.sqrt(3)用于计算等边三角形的高度比例。
import math
import random

t.setup(900, 700)
t.speed(0)
t.tracer(False)
t.ht()

# x、y指定左下角位置，size和depth控制大小与层数。
def triangle(x, y, size, depth):
    # 到达递归出口时，画出一个完整的小三角形。
    if depth == 0:
        # 移动到起点时抬起画笔，避免留下多余连线。
        t.penup()
        t.goto(x, y)
        t.setheading(0)
        # 放下画笔，开始绘制三条边。
        t.pendown()
        for i in range(3):
            t.forward(size)
            t.left(120)
        return
    # 每个子三角形的边长是父三角形的一半。
    half = size / 2
    # 递归绘制左下方的子三角形。
    triangle(x, y, half, depth - 1)
    # 递归绘制右下方的子三角形。
    triangle(x + half, y, half, depth - 1)
    # 递归绘制上方的子三角形。
    triangle(x + half / 2, y + half * math.sqrt(3) / 2,
             # 递归绘制上方的子三角形。
             half, depth - 1)

triangle(-260, -220, 520, 4)

t.update()
t.done()
