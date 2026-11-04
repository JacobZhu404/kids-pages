# 教学改编；CSV为自编模拟数据，非真实乘客或环境观测。
# pandas读取、筛选并排序国家数据表。
import pandas as pd
# pyplot绘制按年份变化的折线。
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei", "PingFang SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# 将CSV记录读入DataFrame。
df = pd.read_csv("countries.csv")
# 只保留年份为2010的行。
selected = df[df["年份"] == 2010]
# 选取指标列，计算2010年的平均值。
print("2010年平均", selected["人均指标"].mean())
# 在2010年的数据中筛选数值最大的一行。
print("最大记录", selected[selected["人均指标"] == selected["人均指标"].max()])
# 先筛选一个国家，再按年份排序后绘图。
country = df[df["国家"] == "甲国"].sort_values("年份")
print(country)
# 根据已有年份记录绘制折线。
plt.plot(country["年份"], country["人均指标"], marker="o")
plt.xlabel("年份")
plt.ylabel("模拟人均指标")
plt.title("甲国历年记录")

plt.grid()
plt.tight_layout()
# 显示绘制完成的图表。
plt.show()
