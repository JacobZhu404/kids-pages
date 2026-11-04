# coding: utf-8
from pathlib import Path
p=Path('work/build_practice.py');s=p.read_text()
insert='''
# Add beginner-friendly comments to generated reference scripts. Match whole
# source lines and preserve their indentation so comments never alter blocks.
EXPLANATIONS = {
'branch.py': {
'import turtle as t':'# turtle is Python’s built-in drawing module; t is a short alias.',
'def tree(length, depth):':'# length is this branch length; depth is the number of levels left.',
'    if depth == 0:':'    # Base case: stop when no branch levels remain.',
'        return':'        # Return to the caller instead of making more recursive calls.',
't.forward(length)':'    # Draw the current branch in the turtle’s heading direction.',
'tree(length * .7, depth - 1)':'    # Recurse with a shorter branch and one fewer level.',
't.backward(length)  # 回到进入本次调用的位置':'    # Retrace the branch so the turtle returns to this branch point.'},
'natural.py': {
'import turtle as t':'# turtle provides the pen, movement, and turning commands.',
'import random':'# random chooses a slightly different split angle for each branch.',
'random.seed(7)  # 固定种子，方便重复观察':'# A fixed seed makes the random tree repeatable for comparison.',
'def tree(length, depth):':'# Each call draws one branch and then its two smaller child branches.',
'    if depth == 0:':'    # Stop at the last level; this is the recursion base case.',
'    width = max(1, depth)':'    # Make higher branches thicker and keep the minimum width at 1.',
'    color = "forestgreen" if depth <= 2 else "saddlebrown"':'    # Color the last two levels green and the larger branches brown.',
'    angle = random.randint(15, 40)':'    # randint includes both endpoints: 15 and 40 degrees.',
'tree(length * .7, depth - 1)':'    # Child branches are 70% as long and one level shallower.',
't.backward(length)':'    # Return to the branch point before the parent call continues.'},
'koch.py': {
'import turtle as t':'# turtle is the built-in module used to draw the curve.',
'def koch(length, depth):':'# Replace one segment recursively; length and depth describe its size.',
'    if depth == 0:':'    # At depth zero, draw a straight line and stop.',
'        t.forward(length)':'        # Draw the smallest segment.',
'        return':'        return  # No smaller curve is needed.',
'    koch(length / 3, depth - 1)':'    # Each child segment is one third as long and one level shallower.',
't.left(60)':'    # Turn to make the outward triangular bump.'},
'snowflake.py': {
'import turtle as t':'# turtle supplies the drawing pen and movement commands.',
'def koch(length, depth):':'# Draw one recursively divided side of the snowflake.',
'    if depth == 0:':'    # The base case is a straight segment.',
'        t.forward(length)':'        t.forward(length)  # Draw the smallest edge.',
'        return':'        return  # Stop this recursive branch.',
'    for angle in [60, -120, 60, 0]:':'    # Four child curves and their turns form one Koch segment.',
'        koch(length / 3, depth - 1)':'        # Shrink the edge to one third and reduce the recursion depth.',
'for i in range(3):':'# Three equal Koch sides close the snowflake.',
't.right(120)':'    # Turn the same amount at each corner of the outer triangle.'},
'sierpinski.py': {
'import turtle as t':'# turtle draws the triangle outlines.',
'import math':'# math.sqrt(3) gives the height ratio of an equilateral triangle.',
'def triangle(x, y, size, depth):':'# x,y locate the lower-left corner; size and depth define the shape.',
'    if depth == 0:':'    # Draw a full small triangle at the recursion base case.',
'        t.penup()':'        # Lift the pen while moving to the triangle’s starting point.',
'        t.pendown()':'        # Put the pen down so the three sides are visible.',
'    half = size / 2':'    # Each child triangle has half the parent side length.',
'    triangle(x, y, half, depth - 1)':'    # Recursively draw the lower-left child.',
'    triangle(x + half, y, half, depth - 1)':'    # Recursively draw the lower-right child.',
'             half, depth - 1)':'             half, depth - 1)  # Draw the top child.'},
'htree.py': {
'import turtle as t':'# turtle is used to draw each H segment.',
'def line(x1, y1, x2, y2):':'# Draw one segment between two coordinates.',
't.goto(x1, y1)':'    # Move to the start without drawing a connecting line.',
't.goto(x2, y2)':'    # Draw from the start coordinate to the end coordinate.',
'def htree(x, y, size, depth):':'# x,y is the H center; size and depth control its scale and recursion.',
'    if depth == 0:':'    # Stop when there are no smaller H shapes left to draw.',
'    half = size / 2':'    # Each end point is half a size away from the center.',
'    for dx in [-half, half]:':'    # Visit the left and right sides of this H.',
'        for dy in [-half, half]:':'        # At each side, recurse from the top and bottom end point.'},
'carpet.py': {
'import turtle as t':'# turtle draws the outlines of the retained carpet squares.',
'def carpet(x, y, size, depth):':'# x,y is the square lower-left corner; size and depth set scale.',
'    if depth == 0:':'    # The smallest retained square is drawn at the base case.',
'        t.penup()':'        # Move to the square corner without leaving a line.',
'        t.pendown()':'        # Draw the four square edges.',
'    third = size / 3':'    # Divide the parent square into nine equal cells.',
'    for row in range(3):':'    # row and col identify each cell in the 3-by-3 grid.',
'        for col in range(3):':'        for col in range(3):',
'            if row == 1 and col == 1:':'            # Skip the center cell to leave the carpet hole.',
'            carpet(x + col * third, y + row * third,':'            # Recurse into each of the other eight cells.'},
'hilbert.py': {
'import turtle as t':'# turtle draws the continuous Hilbert curve.',
'def hilbert(depth, angle, step):':'# depth is recursion level; angle sets turn direction; step is segment length.',
'    if depth == 0:':'    # Base case: no curve is drawn at level zero.',
'        return':'        return  # End this branch of the recursion.',
'    t.left(angle)':'    # Rotate to orient the first smaller curve.',
'    hilbert(depth - 1, -angle, step)':'    # Draw a smaller curve with its turn direction reversed.',
't.forward(step)':'    # Connect neighboring smaller curves with a straight segment.',
'    hilbert(depth - 1, angle, step)':'    # Draw the next smaller curve at the current orientation.',
'depth = 4':'# Four recursive levels create a detailed but manageable curve.',
't.penup()':'# Position the turtle before drawing, without leaving a line.',
't.pendown()':'# Start drawing the curve.'},
'passenger_stats.py': {
'import pandas as pd':'# pandas reads CSV tables and provides DataFrame operations.',
'import matplotlib.pyplot as plt':'# pyplot creates and displays charts.',
'df = pd.read_csv("passengers.csv")':'# Read the CSV beside this script into a DataFrame named df.',
'print(df.head())':'# Show the first five rows to check the data and column names.',
'print("平均年龄", df["年龄"].mean())':'# Select the age column, then calculate its average with mean().',
'print("最高票价", df["票价"].max())':'# max() returns the largest value in the fare column.',
'print(df[df["票价"] == df["票价"].max()])':'# Filter rows whose fare equals the maximum; == compares values.',
'plt.plot(df["编号"], df["票价"], marker="o")':'# Plot fare against passenger number; marker adds a dot at each record.',
'plt.xlabel("编号")':'# Label the horizontal axis.',
'plt.ylabel("票价")':'# Label the vertical axis.',
'plt.show()':'# Open the chart window.'},
'air_stats.py': {
'import pandas as pd':'# pandas reads and summarizes the station table.',
'import matplotlib.pyplot as plt':'# pyplot draws the two station lines.',
'df = pd.read_csv("air.csv")':'# Read the CSV into a DataFrame; each row is one time point.',
'for station in ["A站", "B站"]:':'# Repeat the same summary and plot steps for both station columns.',
'    print(station, "均值", df[station].mean(), "最大值", df[station].max())':'    # Select a column by name, then calculate its mean and maximum.',
'print(df[df["A站"] == df["A站"].max()])':'# Filter the table to find when station A reaches its maximum.',
'    plt.plot(df["时刻"], df[station], marker="o", label=station)':'    # x is time and y is the station reading; label names the line.',
'plt.legend()':'# Show the labels for both station lines.'},
'air_compare.py': {
'import pandas as pd':'# pandas handles the CSV table and column calculations.',
'import matplotlib.pyplot as plt':'# pyplot draws the difference chart.',
'df = pd.read_csv("air.csv")':'# Load the station readings into a DataFrame.',
'df["差值"] = df["A站"] - df["B站"]':'# Subtract matching rows to create a difference column.',
'df["比值"] = df["A站"] / df["B站"]':'# Divide matching rows; the divisor must not be zero.',
'df["绝对差"] = df["差值"].abs()':'# abs() removes the sign so we can compare difference size.',
'print(df)':'# Display the original and newly calculated columns.',
'print("最大差值记录", df[df["差值"] == df["差值"].max()])':'# Find the row whose signed difference is largest.',
'print("最大绝对差记录", df[df["绝对差"] == df["绝对差"].max()])':'# Find the row with the largest gap regardless of direction.',
'plt.plot(df["时刻"], df["差值"], marker="o")':'# Plot the difference over time.',
'plt.show()':'# Display the finished chart.'},
'country_stats.py': {
'import pandas as pd':'# pandas reads, filters, and sorts the country table.',
'import matplotlib.pyplot as plt':'# pyplot draws a time-series line.',
'df = pd.read_csv("countries.csv")':'# Read the CSV records into a DataFrame.',
'selected = df[df["年份"] == 2010]':'# Keep only rows where the year equals 2010.',
'print("2010年平均", selected["人均指标"].mean())':'# Select the metric column and calculate the mean for 2010.',
'print("最大记录", selected[selected["人均指标"] == selected["人均指标"].max()])':'# Filter the 2010 subset to the row with its largest value.',
'country = df[df["国家"] == "甲国"].sort_values("年份")':'# Filter one country, then sort by year before plotting.',
'plt.plot(country["年份"], country["人均指标"], marker="o")':'# Plot existing recorded values by year.',
'plt.show()':'# Display the chart.'},
'group_stats.py': {
'import pandas as pd':'# pandas groups rows and calculates statistics.',
'import matplotlib.pyplot as plt':'# pyplot draws the summary bar chart.',
'df = pd.read_csv("passengers.csv")':'# Load passenger records into a DataFrame.',
'summary = df.groupby("舱位")["票价"].agg(["count", "mean"])':'# groupby splits rows by class; count and mean summarize each group.',
'print(summary)':'# Print the per-class counts and average fares.',
'print("平均票价最高的舱位", summary[summary["mean"] == summary["mean"].max()])':'# Select the group whose mean equals the largest group mean.',
'plt.bar(summary.index.astype(str), summary["mean"])':'# Bar height is average fare; the x labels are class names.',
'plt.show()':'# Display the chart.'}
}
def explain(filename, text):
    rules=EXPLANATIONS.get(filename,{})
    out=[]
    for line in text.splitlines():
        key=line.strip()
        comment=rules.get(key)
        if comment:
            out.append(line[:len(line)-len(line.lstrip())] + comment)
        out.append(line)
    return "\\n".join(out) + "\\n"
'''
needle='for key,body in programs.items():'
assert needle in s
s=s.replace(needle,insert+'\n'+needle,1)
s=s.replace("write_text('# 教学改编练习，非赛事真题\\n'+head+body+end)","write_text(explain(key + '.py', '# 教学改编练习，非赛事真题\\n'+head+body+end))")
s=s.replace("write_text(dhead+body+'\\nplt.grid()\\nplt.tight_layout()\\nplt.show()\\n')","write_text(explain(key + '.py', dhead+body+'\\nplt.grid()\\nplt.tight_layout()\\nplt.show()\\n'))")
p.write_text(s)
