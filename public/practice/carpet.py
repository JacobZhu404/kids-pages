# 教学改编练习，非赛事真题
# turtle用来绘制地毯中保留的正方形轮廓。
import turtle as t
import math
import random

t.setup(900, 700)
t.speed(0)
t.tracer(False)
t.ht()

# x、y是正方形左下角坐标；size和depth控制大小与层数。
def carpet(x, y, size, depth):
    # 到达递归出口时，画出最小的保留正方形。
    if depth == 0:
        # 抬笔移动到正方形角点，不留下线。
        t.penup()
        t.goto(x, y)
        t.setheading(0)
        # 依次画出正方形的四条边。
        t.pendown()
        for i in range(4):
            t.forward(size)
            t.left(90)
        return
    # 把父正方形分成九个大小相同的小格。
    third = size / 3
    # row和col分别表示九宫格中的行号和列号。
    for row in range(3):
        for col in range(3):
            # 跳过正中间的小格，留下地毯的空洞。
            if row == 1 and col == 1:
                continue  # 中间留空
            # 对其余八个小格继续递归。
            carpet(x + col * third, y + row * third,
                   third, depth - 1)

carpet(-240, -240, 480, 3)

t.update()
t.done()
