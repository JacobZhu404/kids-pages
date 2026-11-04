# 教学改编练习，非赛事真题
# turtle模块提供画笔、移动和转向命令。
import turtle as t
import math
# random模块为每次分叉随机选择角度。
import random

t.setup(900, 700)
t.speed(0)
t.tracer(False)
t.ht()

# 固定随机种子，让每次生成的树都一样，方便比较。
random.seed(7)  # 固定种子，方便重复观察

# 每次调用先画当前树枝，再递归画左右两根小树枝。
def tree(length, depth):
    # 到达最后一层时停止，这是递归出口。
    if depth == 0:
        return
    # 层数越高，树枝画得越粗；最细仍保留1像素。
    width = max(1, depth)
    # 最末两层用绿色，较粗的树枝用棕色。
    color = "forestgreen" if depth <= 2 else "saddlebrown"
    t.pensize(width)
    t.pencolor(color)
    t.forward(length)
    # randint会包含两个端点，所以角度可能是15度或40度。
    angle = random.randint(15, 40)
    t.left(angle)
    # 子枝长度缩到原来的70%，递归层数减1。
    tree(length * .7, depth - 1)
    t.right(angle * 2)
    # 子枝长度缩到原来的70%，递归层数减1。
    tree(length * .7, depth - 1)
    t.left(angle)
    # 子树会修改颜色和粗细，返回后恢复再画回程
    t.pensize(width)
    t.pencolor(color)
    # 画完子枝后回到分叉点，让上一层继续绘图。
    t.backward(length)

t.penup()
t.goto(0, -220)
t.setheading(90)
t.pendown()
tree(100, 7)

t.update()
t.done()
