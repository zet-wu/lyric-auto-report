# 歌词自动对齐管线探索

本仓库记录 [Lazulite](https://github.com/wuchenyanmo/Lazulite) 与 [Lazulite Studio](https://github.com/zet-wu/Lazulite-studio) 开发过程中的歌词工作流实验，主要的比较对象是 [Milikara](https://github.com/BilyHurington/MiliKara) 和 [Timing](https://github.com/Zennmn/Timing)，希望对有兴趣于歌曲自动打轴的读者有所帮助和启发。

测试集包含 13 段录音、14 份人工 TTML（均为笔者对着频谱图手动精调过的）；11 首为参与主要比较的日语歌曲，另有一首日语／粤语混合歌曲及潮汕话歌曲。源码、配置、输入和逐条件预测随仓库发布，模型及第三方运行环境由脚本下载。

## 总体结论

针对日语歌曲，在本测试集上，综合表现最好的就是 [Lazulite Studio](https://github.com/zet-wu/Lazulite-studio) 目前所使用的路线：用 Demucs 人声分离后，用人声相对能量分片，把所有分片拼接起来整体送入模型（在 Wav2Vec 阶段，实际的实现是 20 s 分片逐片推理），模型使用 [NextFire/mms-300m-ForcedAligner-karaoke-ja-Latn](https://huggingface.co/NextFire/mms-300m-ForcedAligner-karaoke-ja-Latn)，将输出映射回原曲时间，即 **Demucs 人声分离 + 人声片段整体拼接 + NextFire mms 模型**。以下从几个方面说明：

### 人声分离模型

Demucs 提供了有实际收益的速度与质量平衡。尽管换用 BS-RoFormer Karaoke 可把目前路线的 100 ms 命中率提高到 86.05%，比 Demucs 高 2.14 个百分点，但是其分离 GPU 耗时达到 Demucs 的五倍以上，在 CPU 推理情况下更甚。在本项目测试的数个人声分离模型中，Demucs 在 GPU 和 CPU 上都有极其显著的性能优势。

### 对齐模型

- `NextFire-karaoke-ja-Latn`：这个模型对于日语歌的效果极好，对于独唱、歌唱清晰的歌曲，完全自动化可以交付相当准确的轴（平均误差 50-70 ms，绝对误差上 95 分位数小于 200 ms），主要的出错点出现在连续两个相同读音的时候，两个词的分隔点会找得不太好。其他的错误集中在日语歌中经常出现的长音缩成一个音拍，促音被省略等情况，但这属于歌词和音频本身不匹配了，可以说是非战之过。

- `MMS_FA`：即 `torchaudio` 自带的 `MMS_FA`，这个模型的优势是跨语言通用。NextFire 毕竟是用日语做的后训练，实测发现，对于日语中不存在的元音、闭音节（如汉语方言中的入声、英语中的辅音尾）表现很差。`MMS_FA` 的问题是普遍的结束时间过早，不止出现在刻意延长的尾音上，即使在行内正常时长或者略长一点的词也会给一个很早的结束时间，留下大量空隙，这可能还是歌唱和平时说话的区别导致的，不过，它给出的起始时间还是挺准的，所以在行内，可以用把空隙并入前一个词的方式来优化结果（相当于拿后一个词的起始来校正前词的结束）

 > 这两个 `mms` 系模型的特点只能接受英文字母输入，意味着要做拉丁化，多音字的存在决定了无法完全脱离人工（即使调用在线 LLM 来注音，在不听实际音频的情况下还是会存在错误），完全自动化的实现我认为当前阶段完全依赖本地声学模型是很难的

- `TIFA`：`TIFA` 的问题在于它的路线不同，出于模型上下文的限制，动辄 3-4 分钟的歌曲音频都是无法一次性送入模型的，`mms` 系的可以只在 Wav2Vec 阶段分片，然后拿整曲声学概率和整曲歌词做对齐。`TIFA` 需要把歌词也一起分片，那么问题就陷入如何在对齐之前就得到较可靠的行级时间，排除人工对齐的话，还是需要用 `mms` 模型来做粗对齐，这不仅要做两次完整推理，而且实际效果并不佳。事实上，使用这一路线的 [Timing](https://github.com/Zennmn/Timing) 只有在预先提供准确的行级时间的情况下，对齐效果才能达到或超过 Lazulite Studio 当前路线的水平，而且其超过 Lazulite 的部分也是因为人声分离模型（Timing 使用 BS-RoFormer Karaoke）的差异带来的。

三个模型后端的结果见 [后端与窗口对照](reports/alignment-backends.md)

### 对齐策略

一个反直觉的结果是，使用 `mms` 系模型时，将歌曲和歌词按行分片，每行分别对齐并不能带来收益。在测试集上，逐行对齐的准确率甚至稍低于人声片段整体拼接，而且，逐行对齐依赖人工提供的行级时间，如果使用整曲结果自动粗分行级时间，那么最终准确率更低。见 [后端与窗口对照](reports/alignment-backends.md)。

**复杂的对齐算法并不能带来显著收益**。以当前路线作为基线，对 [Milikara](https://github.com/BilyHurington/MiliKara) 所使用的算法模块进行消融实验，结果显示这些看似漂亮的 trick 并没有多少实际提升。见 [MiliKara 消融](reports/milikara.md) 和 [局部重算](reports/local-refinement.md)。

### 自动注音

Lazulite Studio 的“智能日文注音”使用 Sudachi + JmdictFurigana，以行作为单位处理，以充分利用上下文，这一技术路线的注音准确率（94.52%）以及整行完全匹配率（89.09%）做到了不依赖 LLM 的最佳，超过了 MiliKara 和 Timing 使用的 MeCab／UniDic 或 pykakasi 路线。而仅靠文本的情况下，LLM 也无法做到完全正确，最好的结果仅做到注音准确率 97.65% 和整行完全匹配率 95.10%。见 [自动注音](reports/auto-reading.md)。

## 目录

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
