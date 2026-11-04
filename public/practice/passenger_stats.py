# 教学改编；CSV为自编模拟数据，非真实乘客或环境观测。
# pandas读取CSV表格，并提供DataFrame数据操作。
import pandas as pd
# pyplot负责创建和显示图表。
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei", "PingFang SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# 读取同文件夹中的CSV，并保存为DataFrame变量df。
df = pd.read_csv("passengers.csv")
# 显示前5行，检查数据和列名是否正确。
print(df.head())
# 先选取年龄列，再用mean()计算平均值。
print("平均年龄", df["年龄"].mean())
# max()返回票价列中的最大值。
print("最高票价", df["票价"].max())
# 筛选票价等于最大值的行；==用于比较是否相等。
print(df[df["票价"] == df["票价"].max()])
print("年龄大于35", df[df["年龄"] > 35])
# 横轴为乘客编号、纵轴为票价；marker为每条记录加圆点。
plt.plot(df["编号"], df["票价"], marker="o")
# 设置横轴标签。
plt.xlabel("编号")
# 设置纵轴标签。
plt.ylabel("票价")
plt.title("各乘客票价")

plt.grid()
plt.tight_layout()
# 打开图表窗口。
plt.show()
