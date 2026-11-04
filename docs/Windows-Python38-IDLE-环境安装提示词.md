# Windows Python 3.8 考试环境安装提示词

把下面整段交给 Windows 电脑上的 Agent：

```text
请在这台 Windows 电脑上自动准备“Python 3.8 + IDLE”的离线编程练习环境，并完成检查。请直接执行，不要把常规选择题交给我；只有遇到必须由我输入的 Windows 管理员凭据、官方安装器安全确认，或无法自动解决的兼容性阻断时才暂停，并清楚说明卡在哪里。

目标：
1. 安装官方 64 位 CPython 3.8（优先使用 Python 3.8.10 官方 Windows installer），安装到当前用户目录。安装器中包含 IDLE、pip、标准库 turtle；如已安装合适的 Python 3.8，则先检查并复用，不要重复安装。
2. 确认 IDLE 可由这个 Python 3.8 启动，并能运行 .py 文件；同时确认 `py -3.8`、`python --version`、`python -m pip --version` 指向或能明确调用到目标解释器。不要误用 Microsoft Store 的 python 别名或其他版本。
3. 安装考试大纲列出的第三方库，并尽量让它们在 Python 3.8 64 位和 Windows 上可用。用目标解释器的 `python -m pip` 安装，不要用不确定指向的裸 `pip` 命令。先检查发行包支持的 Python 版本和 Windows wheel；为 Python 3.8 选择仍兼容的版本，记录实际安装的版本。

需要安装的模块（包名与导入名可能不同）：
- numpy
- matplotlib
- seaborn
- pandas
- scipy
- sympy
- jieba
- wordcloud
- psutil
- Pillow（导入名 PIL）
- pygame
- easygui
- scikit-learn（导入名 sklearn；GridSearchCV 是 sklearn.model_selection 中的类，不是单独 pip 包）
- xgboost
- shap
- transformers
- tensorflow
- torch（PyTorch）
- nltk
- spacy

`turtle`、`idlelib`、`pathlib` 是 Python 3.8 标准库/随安装器提供的组件，不要执行 `pip install turtle`、`pip install idlelib` 或 `pip install pathlib`。`GridSearchCV` 由 scikit-learn 提供，也不要当作独立包安装。自动处理上述名称映射。

执行要求：
- 仅从 python.org 官方 Python 3.8 Windows 安装器或本机已有的可信安装源获取 Python；pip 包从配置的 PyPI 源获取。不要关闭 TLS/证书校验，不要运行来源不明的脚本，不要更改系统安全策略，也不要卸载或覆盖其他 Python。
- 尽量安装到当前用户范围。需要管理员权限时先尝试 per-user 安装；若仍必须提升权限则停下来说明，不要绕过 UAC。
- Python 3.8 已较旧，部分最新版库可能不再支持它。根据包元数据/wheel 选择各库最后可用且彼此兼容的 Python 3.8 版本；优先官方兼容 wheel，CPU 版本即可。不得为了装上最新版而换成更新的 Python，也不得静默跳过库。若某库没有可用的 Python 3.8 Windows 版本，记录包名、兼容性证据和实际状态，继续安装其他兼容库。
- 先准备安装清单和版本约束，再安装。保留一份 `requirements-py38-windows.txt` 和执行日志到当前用户文档下的 `Python38ExamSetup` 文件夹；不要把下载的安装包或大型缓存散落到桌面。
- 处理失败时，对单个包最多重试一次；检查依赖冲突后再决定是否调整版本。不要无止境循环安装。

完成后自动逐项检查：
1. Python 版本为 3.8.x、64 位，IDLE 能启动，`turtle` 能导入。
2. 对每个上述第三方库做导入检查；对 scikit-learn 检查 `from sklearn.model_selection import GridSearchCV`。逐项报告成功版本或失败原因。
3. 用 pandas 读一个小 CSV，演示 DataFrame 列访问、`.loc` 行列访问、两列相加、新列创建、`groupby(...).sum()`；用 matplotlib 生成并显示一张小图。
4. 用 IDLE 实际打开并运行一份临时 turtle 小图（画正方形），确认窗口能正常出现和关闭。
5. 保存完整安装清单、实际版本、验证结果和需要人工处理的问题到 `安装报告.txt`。最后给我一段简洁总结，写明 IDLE 启动方式和报告位置。
```
