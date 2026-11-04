# 教学改编；CSV为自编模拟数据，非真实乘客或环境观测。
# pandas对行分组并计算统计结果。
import pandas as pd
# pyplot绘制统计结果柱状图。
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei", "PingFang SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# 将乘客记录载入DataFrame。
df = pd.read_csv("passengers.csv")
# groupby按舱位分组；count计数，mean计算每组平均票价。
summary = df.groupby("舱位")["票价"].agg(["count", "mean"])
# 打印每个舱位的人数和平均票价。
print(summary)
# 筛选平均票价等于各组最高均价的舱位。
print("平均票价最高的舱位", summary[summary["mean"] == summary["mean"].max()])
# 柱高表示平均票价，横轴标签表示舱位。
plt.bar(summary.index.astype(str), summary["mean"])
plt.xlabel("舱位")
plt.ylabel("平均票价")
plt.title("各舱位平均票价")

plt.grid()
plt.tight_layout()
# 显示绘制完成的图表。
plt.show()
