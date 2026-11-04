# 教学改编练习，非赛事真题
# turtle用来绘制连续的希尔伯特曲线。
import turtle as t
import math
import random

t.setup(900, 700)
t.speed(0)
t.tracer(False)
t.ht()

# depth是递归层数，angle是转向角度，step是每段长度。
def hilbert(depth, angle, step):
    # 递归出口：第0层不再绘制曲线。
    if depth == 0:
        # 结束这一支递归，回到上一层调用。
        return
    # 转向，确定第一段子曲线的朝向。
    t.left(angle)
    # 反转转向方向，递归绘制较小曲线。
    hilbert(depth - 1, -angle, step)
    # 画一条直线，把相邻的子曲线连接起来。
    t.forward(step)
    t.right(angle)
    # 保持当前朝向，递归绘制下一段子曲线。
    hilbert(depth - 1, angle, step)
    # 画一条直线，把相邻的子曲线连接起来。
    t.forward(step)
    # 保持当前朝向，递归绘制下一段子曲线。
    hilbert(depth - 1, angle, step)
    t.right(angle)
    # 画一条直线，把相邻的子曲线连接起来。
    t.forward(step)
    # 反转转向方向，递归绘制较小曲线。
    hilbert(depth - 1, -angle, step)
    # 转向，确定第一段子曲线的朝向。
    t.left(angle)

# 设置4层递归，图形较完整且仍容易观察。
depth = 4
# 开始绘图前先抬笔移动到起点。
t.penup()
t.goto(-240, -240)
# 落笔，开始绘制曲线。
t.pendown()
hilbert(depth, 90, 480 / (2 ** depth - 1))

t.update()
t.done()
