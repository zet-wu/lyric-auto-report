# 实验复现说明

本仓库已随 Git 保存了全部 26 首测试集音频、26 份人工 TTML 标注（共 52 个数据文件）、M1–M9 全部逐条件预测结果（`.json` / `.json.gz`）、汇总指标（`results/M1..M9/summary.json` 与 `*.csv`）以及统一实验索引 [`results/EXPERIMENT_INDEX.json`](../results/EXPERIMENT_INDEX.json)。读者既可以在无 GPU、无模型权重的环境中直接复算所有评分并校验仓库完整性，也可以在配备 NVIDIA GPU 的 Linux 环境中从头重跑声学推理。

## 1. 轻量评分复核与完整性校验（无需 GPU 或模型权重）

`scripts/score.py` 严格只读取仓库内已保存的预测结果与参考标注，绝不触发任何模型推理；`scripts/verify.py` 则使用 Python 标准库对数据集 SHA256、代码与 JSON 语法、无本机绝对路径泄露、Markdown 相对链接及 41 项必需输出产物进行静态校验。

在已配置 `.venvs/research`（或安装了 [`requirements/scoring.txt`](../requirements/scoring.txt) 及 `ffprobe` 的本地环境）中执行：

```sh
.venvs/research/bin/python scripts/score.py
python3 scripts/verify.py
```

- **`scripts/score.py`**：
  1. 调用 `scripts/reading/score.py` 汇总 20 首日语主组的自动注音准确率并发布至 `results/M9/`；
  2. 对照 [`configs/phase2.json`](../configs/phase2.json) 与 `scripts/phase2_jobs.py` 检查所有计划实验产物是否齐全；
  3. 统一重算并发布 `results/M1/` 至 `results/M8/` 的 `summary.json`、`metrics.csv` 及专题附表（如 `surface.csv`、`reading-units.csv`、`phonetic-groups.csv`、`cohorts.csv`、`core-boundaries.csv`、`duration-bins.csv`、`correlations.csv`、`resources-summary.csv`）；
  4. 生成顶层数据索引 [`results/EXPERIMENT_INDEX.json`](../results/EXPERIMENT_INDEX.json)（当前状态为 `stage: "complete"`）。
- **`scripts/verify.py`**：
  - 校验 [`datasets/files.json`](../datasets/files.json) 中全部 **52 个音频与 TTML 标注文件**的字节数与 SHA256；
  - 校验全仓库所有 `.py`、`.json`、`.json.gz` 文件的语法合法性及无宿主机绝对路径残留；
  - 校验 `README.md`、`datasets/README.md`、`reports/*.md`、`THIRD_PARTY.md` 中的所有相对链接与图片路径存在；
  - 校验 M1–M9 全部 41 项必需汇总输出文件存在且非空。

## 2. 完整推理环境与模型权重准备

从头运行人声分离与声学对齐推理需要：
- **操作系统与硬件**：Linux（x86_64）、NVIDIA GPU（实验基准为 NVIDIA GeForce RTX 4090，49,140 MiB 显存）；
- **系统工具**：Python 3.11+ / 3.13、Git、FFmpeg（含 `ffprobe`）、Node.js、npm 及 C/C++ 编译工具链。

在仓库根目录执行以下命令，自动创建本地虚拟环境（`.venvs/`）、检出固定提交的上游源码（`.deps/`）并下载校验全部模型权重（`.models/`）：

```sh
python3 scripts/setup.py --models
```

上游仓库的固定提交记录在 [`configs/sources.json`](../configs/sources.json) 与 [`configs/comparison-sources.json`](../configs/comparison-sources.json)（并同步固化于 [`results/EXPERIMENT_INDEX.json`](../results/EXPERIMENT_INDEX.json) 的 `sources` 字段），模型权重地址与 SHA256 记录在 [`configs/models.json`](../configs/models.json) 与 [`configs/separation-models.json`](../configs/separation-models.json)。

为隔离不同开源工具对 `transformers`、`audio-separator` 和 `librosa` 的版本需求，`setup.py` 会自动配置五个本地虚拟环境：

| 虚拟环境路径 | 用途 | 关键依赖与隔离目的 |
| --- | --- | --- |
| `.venvs/research` | Lazulite Studio、MSST / Windowed 分离、M2–M8 共用推理与统一评分 | PyTorch + CUDA、Transformers 4.57.6（详见 `requirements/linux-cuda-lock.txt`） |
| `.venvs/milikara` | MiliKara 原生服务、默认 MelBand 分离与 `UniDic Lite` 注音 | `audio-separator` 0.30.2、`unidic-lite` |
| `.venvs/sug` | SUG 对齐、`Sudachi` 注音与 UVR `MDX-Net Inst HQ 3` ONNX 分离 | Transformers 5.15.0、`audio-separator` 0.47.0、`librosa` 0.10.2.post1 |
| `.venvs/native5` | Timing（`g2pflow` + MMS 粗定位 + `TIFA`）与 yohane 原生管线 | Transformers 5.15.0 |
| `.venvs/fakara` | FA-Kara 的 `MMS_FA` 与原生首尾静音修正路径 | `librosa` 0.11.0 |

## 3. 实验输入生成与分阶段推理执行

### 3.1 阶段 0：参考标注解析与统一输入生成

在运行任何声学推理前，先从 `datasets/annotations/*.ttml` 生成剥离时间戳的各工具标准化输入与参考时间表：

```sh
.venvs/research/bin/python scripts/phase2_prepare.py
.venvs/research/bin/python scripts/run.py prepare
```

查看全部计划执行的实验分区列表及其所属运行环境：

```sh
.venvs/research/bin/python scripts/run.py list
```

### 3.2 阶段 1：串行运行声学对齐、分离与资源基准任务

`scripts/run.py` 按 [`scripts/phase2_jobs.py`](../scripts/phase2_jobs.py) 定义的依赖顺序串行调度各虚拟环境，将每个任务的终端输出记录到 `.cache/phase2/logs/<job_id>.log`，并在单曲或单任务抛错时自动捕获异常类型、失败阶段与消息写入结构化 JSON，确保失败样本保留在统一分母中：

```sh
# 1. 运行除手动 GPU 资源基准外的全部 M1–M9 自动推理任务并汇总评分
.venvs/research/bin/python scripts/run.py all --gpu-confirmed

# 2. 在独占 GPU 的静默环境下运行 M5 的 10 种分离模型 GPU/CPU 耗时与 NVML 能耗基准
.venvs/research/bin/python scripts/run.py gpu-benchmarks --gpu-confirmed

# 3. 支持使用 --start-at <job_id> 从任意指定分区恢复执行
.venvs/research/bin/python scripts/run.py matrix --gpu-confirmed --start-at m6-backends

# 4. 全部推理完成后重新生成最终完整版评分与 EXPERIMENT_INDEX.json
.venvs/research/bin/python scripts/run.py score
```

## 4. 跨平台补充实验与结果图表生成

### 4.1 Windows 原生 `SUG WinRT` 自动注音（M9）

M9 中的 `sug-winrt` 方案依赖 Windows 操作系统的 `Windows.Globalization.JapanesePhoneticAnalyzer`（WinRT）组件。仓库已在 [`results/reading/predictions/sug-winrt/`](../results/reading/predictions/sug-winrt/) 中保存了全部 20 首日语主组在 Windows 下采集的冻结预测。

- 在 Linux 上若仅复算其余注音方法，可传入 `--allow-missing-winrt`；而在仓库已包含 `sug-winrt` 冻结预测时，直接运行 `.venvs/research/bin/python scripts/score.py` 即可完整校验全部 7 种方法。
- 如需在 Windows 机器上重新采集 `sug-winrt` 预测，可在检出固定 SUG 源码并启用系统日语语言包后，在 PowerShell 中执行：

```powershell
py -3.11 -m venv .venvs/sug-winrt
.venvs/sug-winrt/Scripts/python.exe -X utf8 -m pip install -r requirements/reading-sug-winrt-lock.txt
.venvs/sug-winrt/Scripts/python.exe -X utf8 scripts/reading/sug.py --require-winrt
.venvs/sug-winrt/Scripts/python.exe -X utf8 scripts/reading/score.py --method sug-winrt
```

### 4.2 重新生成全部报告图表（`results/figures/`）

仓库中的所有可视化图表均由纯绘图脚本直接读取 `results/M1..M8/summary.json` 动态绘制，同时导出 600 DPI `.png` 与可编辑文本 `.svg`：

```sh
# 生成 README.md 与 reports/comparison.md 中的 G1 / G2 / G3 三组横向对比图
for g in G1 G2 G3; do
  .venvs/research/bin/python scripts/plot_readme_comparison.py --group "$g"
done

# 生成 M2 多语言音节与分段图、M3 AAC-LC 持久化对比图、M4 音节时长分档图、M7 MiliKara 消融图与 M8 跨模型重算图
.venvs/research/bin/python scripts/plot_phase2_figures.py
```
