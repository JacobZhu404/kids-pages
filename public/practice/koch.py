# 教学改编练习，非赛事真题
# turtle是Python自带的绘图模块。
import turtle as t
import math
import random

t.setup(900, 700)
t.speed(0)
t.tracer(False)
t.ht()

# 递归地替换一段线；length和depth分别表示长度和层数。
def koch(length, depth):
    # depth为0时画一条直线，然后停止。
    if depth == 0:
        # 画出最小的一段线。
        t.forward(length)
        # 当前线段画完，return回到调用它的位置。
        return
    # 子线段长度缩为三分之一，递归层数减1。
    koch(length / 3, depth - 1)
    # 转向，画出向外凸起的三角形部分。
    t.left(60)
    # 子线段长度缩为三分之一，递归层数减1。
    koch(length / 3, depth - 1)
    t.right(120)
    # 子线段长度缩为三分之一，递归层数减1。
    koch(length / 3, depth - 1)
    # 转向，画出向外凸起的三角形部分。
    t.left(60)
    # 子线段长度缩为三分之一，递归层数减1。
    koch(length / 3, depth - 1)

t.penup()
t.goto(-300, -90)
t.pendown()
koch(600, 4)

t.update()
t.done()
