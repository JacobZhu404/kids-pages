# pandas读取CSV并执行表格操作。
import pandas as pd
# pyplot负责绘制最终图表。
import matplotlib.pyplot as plt

# 文件和本程序放在同一目录；在 IDLE 中打开并按 F5
# 选择常见中文字体，让图表标签能显示中文。
plt.rcParams["font.sans-serif"] = ["SimHei", "PingFang SC", "Arial Unicode MS"]
# 确保负号能和所选字体一起正常显示。
plt.rcParams["axes.unicode_minus"] = False

# 将同文件夹中的CSV读入DataFrame变量df。
df = pd.read_csv("house_price.csv")
print("前5行：")
# 显示前5行，检查数据是否读入正确。
print(df.head())
# 显示列名，确认后续代码使用的名称准确。
print("列名：", list(df.columns))
# 选取房间数这一列，并计算平均值。
print("平均房间数：", df["房间数"].mean())
# max()返回房龄列中的最大值。
print("最大房龄：", df["房龄(年)"].max())

# 本练习的面积都大于0；其他数据应先检查缺失值和零面积。
# 将对应行的数值相除，生成新的计算列。
df["每平米价格"] = df["房价(万元)"] / df["房屋面积(㎡)"]
# 找出新列中的最大值。
maximum = df["每平米价格"].max()
print("最高每平米价格：", maximum)
print("对应房屋（并列最高时全部显示）：")
# 筛选所有并列最大值对应的记录。
print(df.loc[df["每平米价格"] == maximum])

# 按面积排序，让折线图沿面积递增方向连接。
ordered = df.sort_values("房屋面积(㎡)")
plt.plot(ordered["房屋面积(㎡)"], ordered["房价(万元)"], marker="o")
plt.title("房屋面积与房价关系图")
plt.xlabel("房屋面积（㎡）")
plt.ylabel("房价（万元）")
plt.grid()
plt.tight_layout()
# 显示绘制完成的图表。
plt.show()
