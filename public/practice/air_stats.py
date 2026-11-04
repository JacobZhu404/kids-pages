# 教学改编；CSV为自编模拟数据，非真实乘客或环境观测。
# pandas读取监测站表格并进行统计。
import pandas as pd
# pyplot绘制两个监测站的折线。
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei", "PingFang SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# 把CSV读入DataFrame；每行对应一个时刻。
df = pd.read_csv("air.csv")
print(df.head())
# 用循环依次处理两个监测站的数据列。
for station in ["A站", "B站"]:
    # 按列名取一列，再计算平均值和最大值。
    print(station, "均值", df[station].mean(), "最大值", df[station].max())
# 筛选表格，找出A站达到最大值的时刻。
print(df[df["A站"] == df["A站"].max()])
# 用循环依次处理两个监测站的数据列。
for station in ["A站", "B站"]:
    # x轴是时刻，y轴是读数；label设置曲线名称。
    plt.plot(df["时刻"], df[station], marker="o", label=station)
# 显示两条曲线的图例。
plt.legend()
plt.xlabel("时刻")
plt.ylabel("模拟浓度")
plt.title("两站观测记录")

plt.grid()
plt.tight_layout()
plt.show()
