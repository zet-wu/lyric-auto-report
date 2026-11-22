# 实验复现说明

本仓库已随 Git 保存了全套测试集音频、人工 TTML 标注、逐条件预测结果（`.json` / `.json.gz`）以及汇总指标。读者既可以在无 GPU、无模型权重的轻量环境中直接复算所有评分，也可以在配备 NVIDIA GPU 的 Linux 环境中从头重跑声学推理。

## 1. 轻量评分复核（无需 GPU 或模型权重）

仅需 Python 3.13 及 `NumPy`、`Matplotlib`（定义在 [`requirements/scoring.txt`](../requirements/scoring.txt)），即可从已发布的预测文件重新计算全部实验指标并校验仓库数据与链接完整性：

```sh
python3.13 -m venv .venvs/scoring
.venvs/scoring/bin/pip install -r requirements/scoring.txt
.venvs/scoring/bin/python scripts/score.py
python3.13 scripts/verify.py
```

- `scripts/score.py`：依次调用各专题的独立评分脚本，从 `results/` 下的预测文件重新汇总生成各目录的 `metrics.json`、`metrics.csv`、`summary.json` 以及消融热力图 `results/ablation/matrix.png`。
- `scripts/verify.py`：校验 [`datasets/files.json`](../datasets/files.json) 中 29 个音频与标注文件的 SHA256、所有 Python/JSON 文件语法、无本机绝对路径残留、所有 Markdown 报告的相对链接有效性，以及核心汇总文件完整性。

## 2. 完整推理环境与模型准备

从头运行人声分离与声学对齐推理需要：
- **操作系统与硬件**：Linux（x86_64）、NVIDIA GPU（实验基准为 RTX 4090）；
- **系统工具**：Python 3.13、Git、FFmpeg（含 `ffprobe`）、Node.js、npm 及 C/C++ 编译工具链。

在仓库根目录执行以下命令，自动创建本地虚拟环境（`.venvs/`）、检出固定提交的上游源码（`.deps/`）并下载校验全部模型权重（`.models/`）：

```sh
python3.13 scripts/setup.py --models
```

上游仓库的固定提交记录在 [`configs/sources.json`](../configs/sources.json) 与 [`configs/comparison-sources.json`](../configs/comparison-sources.json)，模型权重地址与 SHA256 记录在 [`configs/models.json`](../configs/models.json) 与 [`configs/separation-models.json`](../configs/separation-models.json)。

為隔离不同开源工具对 `transformers`、`audio-separator` 和 `librosa` 的版本需求，`setup.py` 会自动配置五个本地虚拟环境：

| 虚拟环境路径 | 用途 | 关键依赖版本 |
| --- | --- | --- |
| `.venvs/research` | Lazulite Studio、共用环境模块消融与统一评分 | Transformers 4.57.6（详见 `requirements/linux-cuda-lock.txt`） |
| `.venvs/milikara` | MiliKara 原生服务、默认分离与注音 | `audio-separator` 0.30.2、`unidic-lite` |
| `.venvs/sug` | SUG 对齐与 UVR MDX-Net 分离 | Transformers 5.15.0、`audio-separator` 0.47.0、`librosa` 0.10.2.post1 |
| `.venvs/native5` | 八路线比较中的 Timing 与 yohane | Transformers 5.15.0 |
| `.venvs/fakara` | FA-Kara 的 `MMS_FA` 与静音后处理路径 | `librosa` 0.11.0 |

## 3. 重跑实验与分阶段执行

### 3.1 全量重跑

```sh
.venvs/research/bin/python scripts/run.py all --fresh
```

`--fresh` 会将当前已有的 `results/` 和 `.cache/` 移入被忽略的 `.runs/run-001` 等编号备份目录，然后按依赖顺序从头执行全部实验。若中途中断，去掉 `--fresh` 即可从断点续跑。

### 3.2 按专题阶段单独运行

`scripts/run.py` 支持指定单个专题阶段（或使用 `--start-at <脚本名>` 从阶段内某一步恢复）：

```sh
# 运行八条路线三组对比实验（G1 / G2 / G3）
.venvs/research/bin/python scripts/run.py comparison

# 运行三大对齐后端与行窗口消融矩阵
.venvs/research/bin/python scripts/run.py matrix

# 运行 MiliKara 解码机制消融或异常行局部重算
.venvs/research/bin/python scripts/run.py milikara
.venvs/research/bin/python scripts/run.py local-refinement

# 运行十种人声分离模型的下游对齐或串行资源测试
.venvs/research/bin/python scripts/run.py separation-alignment
.venvs/research/bin/python scripts/run.py resources

# 运行跨平台本地自动注音实验
.venvs/research/bin/python scripts/run.py reading
```

若需要重新绘制 `README.md` 中的三组横向对比柱状图（`results/figures/g{1,2,3}-comparison.png`），可执行：

```sh
for g in G1 G2 G3; do
  .venvs/research/bin/python scripts/plot_readme_comparison.py --group "$g"
done
```

## 4. 补充实验说明（Windows WinRT 注音与在线 LLM 注音）

1. **Windows 下的 SUG `WinRT` 自动注音**：
   - Linux 下运行 `scripts/run.py reading` 会生成 SUG 的跨平台 `Sudachi` 注音结果（`predictions/sug`），并保留仓库中已冻结的 Windows `WinRT` 预测（`predictions/sug-winrt`）。
   - 如需在 Windows 机器上重新生成 `sug-winrt` 预测，可在检出固定 SUG 源码并确保系统日语组件可用后，在 PowerShell 中执行：
     ```powershell
     py -3.11 -m venv .venvs/sug-winrt
     .venvs/sug-winrt/Scripts/python.exe -X utf8 -m pip install -r requirements/reading-sug-winrt-lock.txt
     .venvs/sug-winrt/Scripts/python.exe -X utf8 scripts/reading/sug.py --require-winrt
     .venvs/sug-winrt/Scripts/python.exe -X utf8 scripts/reading/score.py --method sug-winrt
     ```
2. **GPT-6.1 Terra 自动注音对照**：
   - 自动注音报告中的两组在线 LLM 预测（`terra-direct` 与 `terra-corrected`）已随仓库冻结在 `results/reading/predictions/` 中，重跑 `reading` 阶段时若输入正文与 Studio 候选哈希未变，`scripts/reading/reuse_llm.py` 会自动复用已保存的 LLM 输出。
