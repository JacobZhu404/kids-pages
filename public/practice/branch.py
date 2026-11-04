# 教学改编练习，非赛事真题
# turtle是Python自带的绘图模块；起别名t后，后面可以用t调用它。
import turtle as t
# math提供sqrt等数学函数。
import math
# random提供随机数和随机选择功能。
import random

# 设置绘图窗口的宽度和高度。
t.setup(900, 700)
# 使用最快绘图速度。
t.speed(0)
# 暂停逐笔刷新，减少递归绘图等待。
t.tracer(False)
# 隐藏海龟图标，让图形更清楚。
t.ht()

# length表示当前枝长，depth表示还要画几层。
def tree(length, depth):
    # 递归出口：层数用完后停止。
    if depth == 0:
        # return结束本次函数，并回到上一层调用的位置。
        return
    # 海龟沿当前朝向画出这一段树枝。
    t.forward(length)
    t.left(25)
    # 递归画更短的树枝，同时把层数减1。
    tree(length * .7, depth - 1)
    t.right(50)
    # 递归画更短的树枝，同时把层数减1。
    tree(length * .7, depth - 1)
    t.left(25)
    # 沿原路退回分叉点，接着绘制另一根树枝。
    t.backward(length)  # 回到进入本次调用的位置

t.penup()
t.goto(0, -220)
t.setheading(90)
t.pendown()
tree(110, 7)

# 一次性显示已经完成的图形。
t.update()
# 保持绘图窗口打开，直到手动关闭。
t.done()
