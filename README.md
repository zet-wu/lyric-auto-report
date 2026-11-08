# 歌词自动对齐研究

本仓库记录 [Lazulite](https://github.com/wuchenyanmo/Lazulite) 与 [Lazulite Studio](https://github.com/zet-wu/Lazulite-studio) 的歌词工作流实验，为 Studio 当前采用的 **Demucs 人声分离＋人声活动 core 拼接＋NextFire 日语对齐**路线提供可复核的效果与成本依据。这条路线以较低的本地推理成本生成准确的时间轴初稿，并保留读音校对和局部编辑入口。

测试集包含 13 段录音、14 份人工 TTML；11 首日语歌曲组成主比较组，日语／粤语混合歌曲及潮汕语转写单列。源码、配置、输入和逐条件预测随仓库发布，模型及第三方运行环境由脚本下载。

## 为什么 Studio 采用这条路线

**core 拼接提高了严格端点精度，同时减少对人工行时间的依赖。**固定人工读音和 Demucs 人声时，NextFire 的双端 100 ms 歌曲宏平均命中率为：完整人声 75.00%、人工行窗口 80.40%、core 拼接 **83.91%**。core 拼接由音频活动检测生成，波形分块计算概率后，对整条歌词链解码并映射回原时间轴。[后端与窗口对照](reports/alignment-backends.md)

**Demucs 提供了有实际收益的速度与质量平衡。**同一模块对照中，换用 BS Karaoke 可把 NextFire core 的命中率提高到 86.05%，比 Demucs 高 2.14 个百分点；本机串行资源测试中，分离调用平均耗时为 21.09 秒对 3.99 秒，约为 **5.29 倍**，权重为 194.97 MiB 对 80.24 MiB。准确率来自 11 首歌，耗时来自同一首歌的两次独立进程测量。历史六模型测试中，Demucs 在五曲 GPU 总耗时和指定 CPU 短片段上也最快。这支持 Studio 优先采用 Demucs，并把更昂贵的分离配置留作质量取舍。[当前资源](reports/resources.md) · [历史资源](reports/separation-performance.md)

**简单解码已取得主要收益，附加处理需要证明增益。**MiliKara 模块实验中，core 标准 CTC 为 4107/4871 个日语单元命中，活动代价提高到 4120，原混音重试提高到 4150；分隔符折叠明显降低命中。新测的异常行局部重算只让 core 基线净增 2 个命中，同时带来局部退化。当前结果支持以 core 首轮作为稳定基线，按具体收益选择后处理。[MiliKara 消融](reports/milikara.md) · [局部重算](reports/local-refinement.md)

**注音校对和链路容错直接影响实际可用性。**Studio 自动注音的共同片段匹配率为 94.52%，Terra／Luna 修正候选后分别为 97.65%／97.43%。对齐实验固定人工读音，注音实验单独衡量与人工 Ruby 的书写一致性。Timing 当前固定版本的原生链路在日语主组完成 4/11 首，失败涉及前置读音转换、粗定位及对齐后的文本映射；Studio 人工读音路径在 11/11 首返回可评分的部分结果。这体现了读音确认与保留可用输出的工作流价值。[自动注音](reports/auto-reading.md) · [Timing 失败分析](reports/timing.md)

## 对照如何理解

这里评价的是 Studio 路线在当前日语测试集上的整体取舍。TIFA 在相同人工读音、人工行窗口下达到 82.71%，高于同条件 NextFire 的 80.41%；它具备良好的端点能力，可靠定位和输入处理决定这项能力能否转化为完整输出。其他分离器和部分 MiliKara 配置也有更高的准确率，具体收益与运行成本分别报告。

完整链路、固定人工读音和人工行窗口诊断分别比较；各报告注明评分单元与分母。自动对齐的结果作为待校对初稿，人工参考用于衡量端点偏差。

## 阅读顺序

| 报告 | 内容 |
| --- | --- |
| [测试集](datasets/README.md)与[方法](reports/methods.md) | 歌曲、人工标注、分母、失败处理和条件诊断 |
| [分离模型选择](reports/separation-survey.md) | 候选、权重身份和工作流目标 |
| [历史分离性能](reports/separation-performance.md) | 六模型五曲 GPU 与短片段 CPU 资源记录 |
| [当前分离资源](reports/resources.md) | Demucs、BS Karaoke、Kim 串行测量 |
| [对齐后端与窗口](reports/alignment-backends.md) | 1092 个模块条件、延音和窗口覆盖 |
| [六模型下游对齐](reports/separation-alignment.md) | 432 个条件、两条保存路径、人工读音 |
| [Timing 完整链路](reports/timing.md) | 三种输入、失败分析、受控与混合链路 |
| [MiliKara 模块](reports/milikara.md) | 固定目标的 252 种配置及消融 |
| [自动读音](reports/auto-reading.md) | Studio、词典规则及 Terra／Luna 注音准确率 |
| [异常行局部重算](reports/local-refinement.md) | 人工读音，整曲与 core 两种基线 |
| [复现说明](reports/reproduce.md) | 环境、下载、推理与独立评分 |

## 快速复核

只重算已发布预测的评分，无需 GPU 或模型：

```sh
python3.13 -m venv .venvs/scoring
.venvs/scoring/bin/pip install -r requirements/scoring.txt
.venvs/scoring/bin/python scripts/score.py
python3.13 scripts/verify.py
python3.13 scripts/verify_results.py
```

完整推理需要 Linux、Python 3.13、NVIDIA GPU，以及 Git、FFmpeg、Node.js 和 npm：

```sh
python3.13 scripts/setup.py --models
.venvs/research/bin/python scripts/run.py all --fresh
```

四组 LLM 注音由独立模型代理按公开提示生成，完整重跑后需单独生成或导入，步骤见复现说明。

--fresh 将已有 results 与 .cache 移入被忽略的 .runs/run-001 等编号备份，再重新推理。中断后去掉 --fresh 续跑；分阶段入口见[复现说明](reports/reproduce.md)。

## 目录

```text
datasets/       原始音频、TTML、哈希清单
reports/        重写后的报告
results/        当前测试集的预测、决策、评分、表格和图
historical/     历史分离资源记录
configs/        源码提交、模型身份和实验协议
scripts/        下载、输入准备、推理、评分、压缩与校验
requirements/   研究环境、附加依赖和轻量评分依赖
licenses/       代码改编对应的第三方许可
```

Git 跟踪测试音频、标注、实验代码和压缩预测；.deps、.models、.cache、.venvs 均被忽略。所有运行路径从仓库根目录派生，公开上游提交固定在 [sources.json](configs/sources.json)，不需要其他本地项目目录。

代码采用 [AGPL-3.0](LICENSE)。第三方代码、权重、录音和歌词的归属见 [来源与许可](THIRD_PARTY.md)。
