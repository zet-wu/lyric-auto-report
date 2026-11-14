# 复现实验

音频模型实验使用 Linux、Python 3.13、NVIDIA GPU，以及 Git、FFmpeg、Node.js、npm 和 C/C++ 编译工具链。音频模型推理使用 CUDA；文本注音与评分无需 GPU。SUG WinRT 自动注音实验在独立 Windows 环境中进行，使用系统日语注音引擎。

## 安装与版本

在仓库根目录执行：

```sh
python3.13 scripts/setup.py --models
```

源码提交见 [sources.json](../configs/sources.json) 和 [comparison-sources.json](../configs/comparison-sources.json)。源码保存在 .deps，权重保存在 .models 与 .deps/timing/models，运行缓存保存在 .cache；这些目录不纳入 Git。模型、音频和标注均按固定身份读取。

八路线实验通过固定源码接口调用模型、对齐、结果采用和导出，不测试官方安装包或 GUI 操作。Lazulite Studio 包含当前固定管线与智能延长实现。各路线实际运行环境见 [environment.json](../results/comparison/environment.json)，模型文件身份见 [model-files.json](../results/comparison/model-files.json)。

| 环境 | 用途 | 核心版本 |
| --- | --- | --- |
| .venvs/research | Lazulite Studio、固定环境的模块诊断、评分 | Transformers 4.57.6；完整依赖见 comparison-research-lock.txt |
| .venvs/milikara | MiliKara 原生服务、默认分离与注音 | audio-separator 0.30.2、UniDic Lite；见 comparison-native-lock.txt |
| .venvs/sug | SUG 对齐与指定 UVR 分离 | Transformers 5.15.0、audio-separator 0.47.0、librosa 0.10.2.post1 |
| .venvs/native5 | 主比较中的 Timing、yohane | Transformers 5.15.0；见 comparison-native5-lock.txt |
| .venvs/fakara | FA-Kara MMS_FA 路径 | librosa 0.11.0；见 comparison-fakara-lock.txt |

SUG、native5 和 FA-Kara 环境优先加载自己的依赖，并共享研究环境的 CUDA 基础运行库。FA-Kara 的本次 MMS_FA 路径不调用 Transformers。Linux 源码适配使用本机固定的 Torch／torchaudio，而非复刻 FA-Kara 的 Windows 冻结环境或 yohane 的 CLI 可选依赖组合；Timing 源码接口在 Python 3.13 实测，其应用元数据声明的 Python 范围为 3.12。这些适配与实际版本均应随复现结果保留。

仅补装比较环境可执行：

```sh
.venvs/research/bin/python scripts/comparison/setup.py
```

## 完整重跑与续跑

```sh
.venvs/research/bin/python scripts/run.py all --fresh
```

--fresh 将已有 results 和 .cache 移入被忽略的 .runs 编号备份，再重新生成质量实验。中断后去掉 --fresh 续跑。源码、依赖和权重可以继续使用。修改输入、模型、源码或参数后须重新开始，不能把旧声学缓存混入新条件。

阶段依次为 prepare、separate、matrix、pipeline、milikara、reading、local-refinement、mms-gap-fill、comparison、additional、separation-alignment、resources。例如：

```sh
.venvs/research/bin/python scripts/run.py comparison
.venvs/research/bin/python scripts/run.py milikara --start-at run_runner
```

comparison 执行八条路线的三组实验，运行 264 个歌曲条件，输出 22 个组别／路线条件，每个条件分别汇总正文与读音两层，共 44 行指标。Timing 与 FA-Kara 的第一、二组复用相同 BS Karaoke 输出。智能延长只在 Lazulite Studio MMS_FA 条件开启，两条 Lazulite Studio 路线都关闭间隙合并。背景歌词不作为对齐目标；音频叠唱保留。

matrix 使用共用研究环境诊断三种后端与窗口，comparison 使用各路线记录的运行环境进行产品输出比较，两者分别计分。mms-gap-fill 只处理已有端点，不重新声学推理。资源阶段应在其他 GPU 任务结束后串行运行，质量实验日志中的耗时不用于速度排名。

原始输出与失败状态保存在 results；中间音频、项目、概率缓存与日志保存在 .cache。输入准备、原生导出与共同边界评分的说明见[方法](methods.md)及[八路线报告](comparison.md)。

## 自动注音范围与生成

独立报告使用全部 12 首日语主组，另列 s11 前 10 行日语部分。范围、固定源码、输入及 Lazulite Studio 候选哈希见 [reading.json](../configs/reading.json)。初次生成七种本地方法与两种 Terra 条件；SUG 的原 Linux Sudachi 回退结果保留为 sug，在独立 Windows 环境中进行的 WinRT 注音实验结果另列为 sug-winrt，共十种方法。其他预测保持冻结。

本地方法由 reading/prepare.py、reading/local.py 和 reading/sug.py 依次生成；前两者使用研究环境，SUG Sudachi 回退使用 .venvs/sug/bin/python，输出到 predictions/sug；该入口显式选择 SudachiAnalyzer。随后运行 reading/score.py 与 reading/report.py。scripts/run.py reading 已包含这些步骤。

Linux 阶段入口生成 SUG Sudachi 回退条件；报告中的独立 WinRT 条件须在 Windows 生成或保留已发布预测。在独立 Windows 环境中进行该实验时，于仓库根目录执行以下 PowerShell 命令；要求系统日语注音接口可用，且 .deps/comparison/sug 已检出 comparison-sources.json 中的固定提交。

```powershell
py -3.11 -m venv .venvs/sug-winrt
.venvs/sug-winrt/Scripts/python.exe -X utf8 -m pip install --cache-dir .cache/pip -r requirements/reading-sug-winrt-lock.txt
.venvs/sug-winrt/Scripts/python.exe -X utf8 scripts/reading/verify_sug_winrt.py --baseline .cache/sug-winrt-before --capture
.venvs/sug-winrt/Scripts/python.exe -X utf8 scripts/reading/sug.py --require-winrt
.venvs/sug-winrt/Scripts/python.exe -X utf8 scripts/reading/score.py --method sug-winrt
.venvs/sug-winrt/Scripts/python.exe -X utf8 scripts/reading/verify_sug_winrt.py --baseline .cache/sug-winrt-before
.venvs/sug-winrt/Scripts/python.exe -X utf8 scripts/reading/report.py
```

--require-winrt 将结果独立写入 predictions/sug-winrt 和 runtime/sug-winrt.json，并核对源码提交、正文输入哈希及实际分析器，WinRT 不可用时终止，禁止静默回退。原生 pykakasi 单字参考依赖也必须可用。--output-dir 可将预测与运行记录先写入被忽略的临时目录；评分固定读取 results/reading。--capture 保存实验运行前的核验快照，目录已存在时须换一个未使用的目录名。UTF-8 模式用于避免 Windows 默认编码改变歌词或依赖清单。此环境仅安装文本路径所需依赖，不安装声学模型、分离器或 GUI。

本次 Windows 版本、Python 与依赖版本、输入和预测哈希见[运行环境](../results/reading/sug-winrt-environment.json)，WinRT 实际分析器与未决单元见[运行记录](../results/reading/runtime/sug-winrt.json)。[独立 Windows 实验核验](../results/reading/sug-winrt-audit.json)记录共同边界、其他方法评分及时间对齐文件的不变性。WinRT 依赖系统日语组件，跨系统版本复现时应重新核对输出哈希。时间对齐实验仍使用原 Linux 注音与声学结果。

外部 LLM（大语言模型）模拟使用 gpt-6.1-terra、high 推理强度，按协议分为三个隔离批次。每批先只读正文直接注音，再在相同代理上下文中读取新生成的 Lazulite Studio 候选并修正；不读取人工参考、音频、时间、其他模型结果、网络或词典。26 份新输出及其哈希记录在 results/reading/llm-execution.json。

发布预测已冻结。后续完整重跑的 reuse_llm.py 仅在正文和 Lazulite Studio 候选哈希一致时复用本次两种 Terra 预测，不自动请求外部模型；改变输入时必须重新生成。这个复现入口不代表本轮复用了旧实验输出。

## Lazulite Studio 智能延长更新

固定实现为 5d3183e。智能延长取 FA-Kara 静音搜索、全部片段核心区终点 core_end（含连续长片段寻谷形成的分界）、下一有效单元起点中的最早候选，末尾以音频终点封顶；两条路线都关闭间隙合并，仅 MMS_FA 开启延长。

本轮核对源码后确认声学推理与解码未变，复用已有 GPU 声学结果及经哈希核验的人声，使用 scripts/comparison/refresh_studio_postprocessing.py 重新调用产品后处理，再执行原生前端采用与评分。72 个 Lazulite Studio 条件全部复核，其中 36 个 MMS_FA 条件使用新终点，36 个 NextFire 条件保持一致。原始推理耗时不视为本轮耗时。记录见 [后处理核验](../results/comparison/studio-postprocessing-audit.json)。完整新推理仍通过 run_studio.py 调用相同实现，并传入准备阶段的全部片段。

## 独立评分与验证

只复核已发布的预测，无需源码依赖、模型或 GPU：

```sh
python3.13 -m venv .venvs/scoring
.venvs/scoring/bin/pip install -r requirements/scoring.txt
.venvs/scoring/bin/python scripts/comparison/test_scoring.py
.venvs/scoring/bin/python scripts/score.py
python3.13 scripts/verify.py
python3.13 scripts/verify_results.py
python3.13 scripts/comparison/verify.py
```

verify 检查输入哈希、相对路径、语法与文档链接；verify_results 检查全部预定条件和分母；comparison/verify 检查组内正文分区、固定读音分母、合并缺失及原生时间端点，并使用独立的统计实现重算命中、MAE（Mean Absolute Error，平均绝对误差）、绝对误差 P95（第 95 百分位数）、缺失与超过 1 秒的项数。缺失保留在命中分母，误差分布只统计有效端点。

预测可无损压缩为 .json.gz，评分同时支持两种形式。报告由 scripts/refresh_reports.py、scripts/comparison/report.py 和 scripts/reading/report.py 从当前指标生成。README 的结论表述按作者要求保留，只更新数据与目录。

原 Linux 发布结果曾在不含 .deps 与 .models 的独立发布目录中，使用仅安装 NumPy 和 Matplotlib 的评分环境重新计分。23 份指标对象逐项一致，29 份输入文件、全部实验条件与文档链接通过检查；指标语义哈希和检查范围见[复核记录](../results/reproducibility.json)。该记录中的自动注音指标哈希对应纳入独立 Windows 实验结果之前的快照，当前自动注音结果以[独立 Windows 实验核验](../results/reading/sug-winrt-audit.json)为准。

SUG 按原生 .sug 项目评分。已有冻结模型结果可通过 `.venvs/sug/bin/python scripts/comparison/sug_project.py` 重新执行采用、保存与加载校验；此步骤不重新运行声学模型。项目里的节奏点和句末点是正文与读音两层评分的时间来源。
