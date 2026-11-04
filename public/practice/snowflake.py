# 教学改编练习，非赛事真题
# turtle提供画笔和移动命令。
import turtle as t
import math
import random

t.setup(900, 700)
t.speed(0)
t.tracer(False)
t.ht()

# 递归绘制雪花的一条边。
def koch(length, depth):
    # 递归出口是一条直线段。
    if depth == 0:
        # 画出最短的边。
        t.forward(length)
        # 停止这一支递归，并返回调用位置。
        return
    # 四段较小曲线和对应转向组成一段科赫曲线。
    for angle in [60, -120, 60, 0]:
        # 边长缩为三分之一，层数减1后继续递归。
        koch(length / 3, depth - 1)
        t.left(angle)

t.penup()
t.goto(-200, 120)
t.pendown()
# 三条相同的科赫曲线组成封闭雪花。
for i in range(3):
    koch(400, 3)
    # 每到一个外角，就按相同角度转向。
    t.right(120)

t.update()
t.done()
