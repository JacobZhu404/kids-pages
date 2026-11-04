# coding: utf-8
from pathlib import Path
p=Path('work/build_practice.py');s=p.read_text()
start=s.index('for i,(key,title,level,task,hint,challenge,source) in enumerate(tasks,1):')
s=s[:start]+'''analysis = {
'branch': ['停止条件是depth等于0，表示没有下一层。', '当前调用先画一根枝，再左右各调用一次；长度乘0.7，层数减1。', '每次返回前后退同样的长度，并恢复方向，这样另一支才能从分叉点开始。'],
'natural': ['递归结构与二叉树相同，先保证位置与方向能恢复。', '用depth决定粗细和颜色，越接近末端越细，最后两层用绿色。', '每次选一个随机角度，左右转动保持配对。子调用会改变画笔，所以回程前恢复父枝的样式。'],
'koch': ['0层只画直线；更高层把长度分成三份。', '一次调用依次画四段小科赫曲线，中间按左60°、右120°、左60°转向。', '四次子调用长度均为原来的三分之一，depth都减1；结束后方向与进入时相同。'],
'snowflake': ['先把一条科赫曲线封装成函数，与上一题共用递归规则。', '外层循环重复三次，每次画一条大边后向右转120°。', '先用0层检查等边三角形闭合，再增加层数；不闭合时优先检查大边转向。'],
'sierpinski': ['0层画一个完整等边三角形。', '其他层不画大三角形，只在左下、右下和上方放三个半尺寸子三角形。', '上方起点比左下向右移动原边长的四分之一、向上移动原边长乘√3再除以4。每个子调用都减一层。'],
'htree': ['用中心(x,y)、尺寸size和剩余层数定义一个H。0层返回。', '一个H由一条横线和两条竖线组成，先确定四个端点。', '在四个端点分别调用自己，尺寸减半、层数减1。坐标定位避免依赖上一次画线的方向。'],
'carpet': ['0层画保留小方块的轮廓。', '把尺寸除以3，行列各枚举0、1、2，得到九宫格起点。', '行列同时等于1时跳过，剩余八格递归。位置每次移动一格尺寸，depth减1；轮廓之间的空白形成地毯。'],
'hilbert': ['先用1层观察一个U形，0层不画线直接返回。', '每个更高层由四个低一层的子图和三条连接线组成；子图之间转90°。', '角度的正负控制子图朝向。层数变化时，用480÷(2的depth次方−1)计算步长，保持图形总宽约480。']}
danalysis = {
'passenger_stats': ['read_csv读表，head查看列名和前5行。', '选年龄列求mean，选票价列求max；用票价等于最大值的条件筛选整行，可保留并列最高记录。', '年龄大于35的条件也返回布尔序列，用它筛选df。最后把编号与票价两列交给plot，并补齐标题与轴名。'],
'air_stats': ['先确认每行对应一个时刻，A站与B站是两列数值。', '分别选列求mean和max，不要把时刻列一起算进去；再按A站最大值筛选整行，找到时刻。', '两次plot使用相同横轴，再用legend区分监测站。本练习无缺失值；真实数据应先检查缺失情况。'],
'air_compare': ['差值有正负，表示A站比B站高多少；绝对差只表示相差大小。', '先确认B站不缺失且不为0，再逐列相减、相除，结果直接赋给新列。', '分别用差值最大和绝对差最大的条件筛选记录；画差值随时刻变化图，横轴用时刻而不是行号。'],
'country_stats': ['先用年份等于2010的条件得到子表，再在子表上求平均值和最大值。', '求最大记录也必须使用2010年的子表，避免误选其他年份。', '另选甲国所有记录，按年份排序后画折线图；这展示已有历史数据，不推算未来。'],
'group_stats': ['groupby按舱位把记录分组，再选票价列。', 'count统计每组有效票价数量，mean统计平均票价；本题票价没有缺失，所以count也等于人数。', '比较汇总表的mean列找出最高组；用舱位作分类横轴、平均票价作柱高，不能把不同舱位的记录直接当成均价。']}
def explain(lines):
 return '<ol>' + ''.join('<li>'+html.escape(line)+'</li>' for line in lines) + '</ol>'
for i,(key,title,level,task,hint,challenge,source) in enumerate(tasks,1):
 code=(dest/(key+'.py')).read_text()
 s+=f'<article class="card"><span class="badge">{level}</span><h3>{i}. {title}</h3><section class="problem"><h4>一、题目</h4><p>{task}</p><img src="practice/{key}.svg" alt="{title}目标图形"></section><section class="explanation"><h4>二、解析</h4>{explain(analysis[key])}</section><section class="solution"><h4>三、参考答案</h4><details><summary>展开完整代码与核对说明</summary><p><b>核对与变式：</b>{challenge}</p><a href="practice/{key}.py" download>下载Python代码</a><pre class="code">{html.escape(code)}</pre></details></section><p class="small"><a href="{source}">原始教学题目来源</a> · 本版已改写为Python标准库turtle。</p></article>'
s+='</section><section class="section" id="data"><h2>二、数据处理与统计</h2>'
for i,(key,title,level,file,task,answer,source,body) in enumerate(dtasks,1):
 code=(dest/(key+'.py')).read_text()
 s+=f'<article class="card"><span class="badge">{level}</span><h3>{i}. {title}</h3><section class="problem"><h4>一、题目</h4><p>{task}</p><p><a href="practice/{file}" download>下载 {file}</a></p><details><summary>查看题目数据（模拟）</summary><pre class="code">{html.escape((dest/file).read_text(encoding="utf-8-sig"))}</pre></details></section><section class="explanation"><h4>二、解析</h4>{explain(danalysis[key])}</section><section class="solution"><h4>三、参考答案</h4><details><summary>展开完整代码与核对结果</summary><p><b>预期结果：</b>{answer}</p><a href="practice/{key}.py" download>下载Python代码</a><pre class="code">{html.escape(code)}</pre></details></section><p class="small"><a href="{source}">技能与题型来源</a> · 本题为简化改编，数据自编。</p></article>'
s+='</section></main></html>'; (root/'digital-practice.html').write_text(s)
'''
s=s.replace('先自己写，再看提示和答案。','每题按“题目 → 解析 → 参考答案”学习。').replace('每题顺序：读要求 → 自己尝试 → 展开提示 → 运行核对 → 修改参数。','每题顺序：读题目并尝试 → 看解析理解步骤 → 展开参考答案运行核对。')
s=s.replace('.hero a{color:white}', '.hero a{color:white}h4{font-size:1.05rem;color:#3456c5;margin:22px 0 8px}.explanation{border-left:3px solid #45b7a4;padding-left:16px}.explanation li{margin:8px 0}')
p.write_text(s)
