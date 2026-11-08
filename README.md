# 歌词自动对齐研究

本仓库汇总 [Lazulite](https://github.com/wuchenyanmo/Lazulite) 与 [Lazulite Studio](https://github.com/zet-wu/Lazulite-studio) 开发中的人声分离、歌词自动读音和强制对齐实验，比较 NextFire、MMS_FA、Timing/TIFA 与 MiliKara 的具体模块和调用路径。

测试集包含 13 段录音、14 份人工 TTML；11 首日语歌曲组成主比较组，日语/粤语混合歌曲及潮汕语转写单列。对齐结果均在这套输入上重新生成。源码、配置、输入和逐条件预测随仓库发布，模型及第三方运行环境由脚本下载。

## 主要发现

- 固定人工读音时，NextFire 配合 BS Karaoke 的 core 拼接取得 86.05% 双端 100 ms 宏平均命中率。TIFA 在准确行窗口中明显改善；MMS_FA 的延音尾点普遍偏早。
- 六模型下游比较中，浮点 core 路径的 Windowed 为 84.94%，PCM24 路径的 DTTNet 为 84.88%；保存与活动检测路径会改变排名。
- MiliKara 的分隔符折叠在本测试集降低命中，停顿代价的收益较小。自动读音实验中，一次局部声学重算把日语 100 ms 命中从 70.99% 提升至 76.00%，DP 分组未超过这一简单对照。
- Timing 原生链路在每种输入条件下完成 6/14 份标注，其中日语主组为 4/11；未完成项与部分输出保留在评分分母中。

以上数字对应不同输入与评分单元，比较范围见各报告。完整链路、固定人工读音、人工行窗口三个层次分别呈现。

## 阅读顺序

| 报告 | 内容 |
| --- | --- |
| [测试集](datasets/README.md)与[方法](reports/methods.md) | 歌曲、人工标注、分母、失败处理和条件诊断 |
| [分离模型选择](reports/separation-survey.md) | 候选、权重身份和工作流目标 |
| [历史分离性能](reports/separation-performance.md) | 六模型五曲 GPU 与短片段 CPU 资源记录 |
| [当前分离资源](reports/resources.md) | Demucs、BS Karaoke、Kim 串行测量 |
| [对齐后端与窗口](reports/alignment-backends.md) | 1092 个模块条件、延音和窗口覆盖 |
| [六模型下游对齐](reports/separation-alignment.md) | 828 个条件、两条保存路径、人工与自动读音 |
| [Timing 完整链路](reports/timing.md) | 三种输入、失败分析、受控与混合链路 |
| [MiliKara 模块](reports/milikara.md) | 固定目标的 264 种配置及消融 |
| [自动读音与迭代](reports/auto-reading.md) | 6 种终态及 4 种候选对照 |
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
