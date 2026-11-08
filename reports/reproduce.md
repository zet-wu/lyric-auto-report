# 复现实验

完整推理使用 Linux、Python 3.13、NVIDIA GPU；系统需安装 Git、FFmpeg、Node.js 和 npm。已测 Python 依赖固定在 requirements/linux-cuda-lock.txt，TIFA 与六模型分离的附加依赖分别安装在独立目录。

## 安装和下载

在仓库根目录执行：

```sh
python3.13 scripts/setup.py --models
```

安装程序创建 .venvs/research，下载固定提交的公开源码，并校验模型资产。源码位于 .deps，权重位于 .models 和 .deps/timing/models，计算缓存位于 .cache。这些目录均被 Git 忽略。

已配置环境时，可以分别运行：

```sh
.venvs/research/bin/python scripts/download.py sources
.venvs/research/bin/python scripts/download.py models
```

Timing 的模块实验采用本仓库固定的 Transformers 4.57.6 研究环境，通过源码调用；上游完整应用的依赖声明另有版本要求。TIFA 的附加包通过固定上游清单安装到独立目录。六模型比较的 RotaryEmbedding 固定为 0.3.5，与 Timing 所用依赖分开。

## 完整重跑

```sh
.venvs/research/bin/python scripts/run.py all --fresh
```

--fresh 把已有 results 与 .cache 移入被忽略的 .runs 编号目录，保留备份后重新推理。中断后使用 all 续跑，不再加 --fresh。

已开始一次新运行时，各阶段也可依次执行：

```sh
.venvs/research/bin/python scripts/run.py prepare
.venvs/research/bin/python scripts/run.py separate
.venvs/research/bin/python scripts/run.py matrix
.venvs/research/bin/python scripts/run.py pipeline
.venvs/research/bin/python scripts/run.py milikara
.venvs/research/bin/python scripts/run.py reading
.venvs/research/bin/python scripts/run.py local-refinement
.venvs/research/bin/python scripts/run.py additional
.venvs/research/bin/python scripts/run.py separation-alignment
.venvs/research/bin/python scripts/run.py resources
```

prepare 提取标注、生成 Demucs 人声和产品基线，完成统一读音的窗口诊断；separate 生成 BS Karaoke 和 Kim Vocals 人声。matrix 完成三后端模块比较，pipeline 执行 Timing 完整链路。后四个质量阶段分别运行 MiliKara、其余分离器、两条持久化路径的下游对齐。reading 提取不含读音的歌词并运行六种词典／规则条件；local-refinement 固定人工读音运行两种首轮和两种异常行重算。resources 在其他推理结束后串行测量资源。

运行日志保存于 .cache/logs。脚本已保存的结果可供断点续跑；使用 --start-at 指定阶段内的脚本名称，例如：

```sh
.venvs/research/bin/python scripts/run.py milikara --start-at run_runner
```

更改输入、源码、模型或参数后，使用 all --fresh 开始新运行，确保输入与缓存一致。权重、依赖和源码目录可继续使用。

## LLM 注音复现

四组 LLM 输出保存在 results/reading/predictions 的 terra-direct、terra-corrected、luna-direct、luna-corrected。每组含 11 个歌曲 JSON，均使用 inputs 中的行 ID 和 words 顺序。公开结果可直接评分；生成新输出需要访问相应模型。

[reading.json](../configs/reading.json)保存模型名称、推理强度、统一提示和输入限制。分别启动 gpt-6.1-terra、gpt-6-luna 两个独立代理，每个先读取 results/reading/inputs，输出 direct，再读取 Studio 候选，输出 corrected。代理只能访问正文、Studio 候选和自身输出；人工参考、音频、其他模型结果与网络查询不提供给代理。生成后运行 scripts/score.py 和 scripts/verify_results.py。

这是代理模拟实验：同一模型的修正条件保留直接注音的会话上下文。仓库提供规范化输入、提示和最终输出；新一次模型生成会有差异。all --fresh 只自动运行本地可执行条件，四组 LLM 需按上述步骤另行生成。旧输出随原 results 保存在忽略的编号备份中，只有确认正文与协议一致时才可导入为已有输出，不应标记为新生成。

OpenJTalk 使用 pyopenjtalk 0.4.1 和固定哈希的 1.11 词典。setup --models 一并下载；单独准备可运行 scripts/download.py reading，资产见[清单](../configs/reading-assets.json)。

## 只复核已有结果

评分只需要 NumPy 和 Matplotlib：

```sh
python3.13 -m venv .venvs/scoring
.venvs/scoring/bin/pip install -r requirements/scoring.txt
.venvs/scoring/bin/python scripts/score.py
python3.13 scripts/verify.py
python3.13 scripts/verify_results.py
```

verify 核对输入哈希、相对路径和文档链接。verify_results 要求每个预定条件都有成功或失败记录，并核对评分分母。原始 JSON 预测可使用 gzip 压缩；评分入口同时读取两种格式。

质量实验的单次耗时用于追查执行过程。资源测量见独立报告和记录，包含具体计时边界。

## 复现检查结果

推理使用仓库内的固定公开源码、模型和研究环境，完成 42 个 Timing 链路条件、1092 个模块矩阵条件、432 个六模型下游条件，以及 MiliKara 的 252 种配置、3024 个歌曲条件。另有 66 个人工读音局部重算条件、110 个自动注音歌曲条件。三条分离路径各做两次串行资源测量。

另把 Git 发布清单复制到独立目录，只安装评分依赖，再运行 score.py、verify.py 和 verify_results.py。副本没有 .deps 或 .models，11 份指标 JSON 与推理环境中的结果逐项一致。27 个输入文件的哈希、全部预定条件、文档链接和仓库相对路径检查通过。

机器可读记录及指标语义哈希见 [reproducibility.json](../results/reproducibility.json)。
