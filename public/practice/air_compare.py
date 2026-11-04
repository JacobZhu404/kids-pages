# 教学改编；CSV为自编模拟数据，非真实乘客或环境观测。
# pandas读取CSV并计算数据列。
import pandas as pd
# pyplot绘制差值图。
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei", "PingFang SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# 将监测站读数载入DataFrame。
df = pd.read_csv("air.csv")
# 除法前确认分母不为0；本模拟数据无缺失值
assert df["B站"].notna().all() and (df["B站"] != 0).all()
# 对应行相减，创建差值列。
df["差值"] = df["A站"] - df["B站"]
# 对应行相除；除数不能为0。
df["比值"] = df["A站"] / df["B站"]
# abs()取绝对值，比较差距大小时不看正负方向。
df["绝对差"] = df["差值"].abs()
# 显示原始列和新计算的列。
print(df)
# 找出带正负方向的差值中最大的一行。
print("最大差值记录", df[df["差值"] == df["差值"].max()])
# 找出不考虑方向时差距最大的一行。
print("最大绝对差记录", df[df["绝对差"] == df["绝对差"].max()])
# 绘制差值随时间变化的折线。
plt.plot(df["时刻"], df["差值"], marker="o")
plt.xlabel("时刻")
plt.ylabel("A站减B站")
plt.title("两站差值")

plt.grid()
plt.tight_layout()
# 显示完成的图表。
plt.show()
