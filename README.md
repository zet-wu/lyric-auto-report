# 歌词自动对齐管线探索

本仓库记录 [Lazulite](https://github.com/wuchenyanmo/Lazulite) 与 [Lazulite Studio](https://github.com/zet-wu/Lazulite-studio) 开发过程中的歌词工作流实验，主要的比较对象是 [MiliKara](https://github.com/BilyHurington/MiliKara)、[Timing](https://github.com/Zennmn/Timing)、[StrangeUtaGame](https://github.com/karaoke-studio/StrangeUtaGame)（简称 SUG）、[yohane](https://github.com/Japan7/yohane) 和 [FA-Kara](https://github.com/moriwx/FA-Kara)，希望对有兴趣于歌曲自动打轴的读者有所帮助和启发。

测试集包含 14 段录音、15 份人工 TTML（均为笔者对着频谱图手动精调过的）；其中 12 首为参与主要比较的日语歌曲，另有 1 首日语／粤语混合歌曲及 1 首潮汕话歌曲（其中一份使用日语假名对潮汕话发音做转写标注）。源码、配置、输入和逐条件预测随仓库发布，模型及第三方运行环境由脚本下载。

## 总体结论

针对日语歌曲，在本测试集上，综合表现最好的就是 [Lazulite Studio](https://github.com/zet-wu/Lazulite-studio) 目前所使用的路线：先通过 Demucs 分离人声，再按人声相对能量切出活跃片段并拼接起来整体送入模型（在 Wav2Vec2 阶段，实际的实现是 20 s 分片逐片推理），模型使用 [NextFire/mms-300m-ForcedAligner-karaoke-ja-Latn](https://huggingface.co/NextFire/mms-300m-ForcedAligner-karaoke-ja-Latn)（下称 NextFire），最后将输出映射回原曲时间，即 **Demucs 人声分离 + 人声片段整体拼接 + NextFire 模型**。与其他对齐路线相比，Lazulite Studio 的多项指标均做到最佳，如下图。具体比较结果见 [八条路线对齐比较](reports/comparison.md)。

人工读音 + 各自分离器：共同正文边界的误差指标：
![人工读音 + 各自分离器：共同正文边界的误差指标](results/figures/g1-comparison.png)

由于某些路线在对齐时会将某些读音单元合并（如长音、促音等），因此输出的总单元数量，即准确率的分母会不一致。共同正文边界即指将所有路线的结果的单元边界取交集，仅计算这些共同边界的准确率。
图中 `*` 标记各指标最佳值：命中率越高越好，平均绝对误差与绝对误差 P95 越低越好，以下两图相同，不再赘述。

人工读音 + 统一 BS Karaoke 分离器：共同正文边界的误差指标，此组衡量剔除人声分离器的差异后的各路线对齐效果：
![人工读音 + 统一 BS Karaoke 分离器：共同正文边界的误差指标](results/figures/g2-comparison.png)

自动分词注音 + 各自分离器：人工读音边界的误差指标。此组衡量在完全自动化情形下，从无注音、无分词的歌词正文开始进行分词、注音、对齐的最终效果；这里展示人工读音边界（以参考标注的 5,370 个读音单元为固定分母，合并或漏掉的内部边界直接记为未命中），以同时衡量自动分词注音过程中的粒度损失与错误：
![自动分词注音 + 各自分离器：人工读音边界的误差指标](results/figures/g3-comparison.png)

以下从几个方面说明：

### 人声分离模型

Demucs 提供了有实际收益的速度与质量平衡。尽管 BS Karaoke 的双端 100 ms 命中率为 85.83%，比 Demucs 的 83.89% 高 1.94 个百分点，但代价是耗时的大幅增加。在本项目测试的十种人声分离配置中，综合参数量、CPU 与 GPU 性能及下游任务表现，Demucs 是较优选择。

| 配置 | GPU 相对耗时 | CPU 相对耗时 | 参数量 | 下游对齐任务双端 100 ms 命中率 |
| --- | ---: | ---: | ---: | ---: |
| Demucs htdemucs | 1.00 | 1.00 | 41.984 M | 83.89% |
| SCNet Small | 2.45 | 3.25 | 10.579 M | 81.30% |
| DTTNet | 1.57 | 7.08 | 4.958 M | 84.26% |
| BS-RoFormer viperx | 4.69 | 31.17 | 159.758 M | 84.90% |
| MelBand RoFormer Kim | 2.46 | 11.72 | 228.203 M | 84.75% |
| Windowed RoFormer | 1.22 | 4.39 | 228.387 M | 84.90% |
| BS Karaoke | 7.28 | 22.37 | 51.049 M | 85.83% |
| MDX-Net Inst HQ 3 | 4.60 | 1.39 | 16.684 M | 82.57% |
| MelBand RoFormer ep_3005 | 4.19 | 8.17 | 251.870 M | 84.47% |
| HybridDemucs MUSDB Plus | 0.50 | 0.33 | 83.639 M | 81.32% |

完整方法和数据见 [模型分离性能](reports/separation-performance.md) 和 [模型下游对齐](reports/separation-alignment.md)。

### 对齐模型

- `NextFire`：这个模型对于日语歌的效果极好，对于独唱、歌唱清晰的歌曲，完全自动化可以交付相当准确的轴（平均误差 50–70 ms，绝对误差上 95 分位数小于 200 ms），主要的出错点出现在连续两个相同读音的时候，两个词的分隔点会找得不太好。其他的错误集中在日语歌中经常出现的长音缩成一个音拍、促音被省略等情况，但这严格来讲属于歌词和音频本身不匹配的问题。

- `MMS_FA`：即 `torchaudio` 自带的 `MMS_FA`，这个模型的优势是跨语言通用。NextFire 毕竟是用日语做的后训练，实测发现，对于日语中不存在的元音、闭音节（如汉语方言中的入声、英语中的辅音尾）表现很差。`MMS_FA` 的问题是结束时间普遍偏早，不止出现在刻意延长的尾音上，即使在行内正常时长或者略长一点的词也会给一个很早的结束时间，留下大量空隙，这可能还是歌唱和平时说话的区别导致的。不过，它给出的起始时间还是挺准的，所以在行内，可以用把空隙并入前一个词的方式来优化结果（相当于拿后一个词的起始来校正前词的结束）。

 > 这两个 `mms` 系模型的特点是只能接受英文字母输入，意味着要做拉丁化。多音字的存在决定了仅靠文本无法完全脱离人工（即使调用在线 LLM 来注音，在不听实际音频的情况下还是会存在错误），完全自动化的实现在当前阶段完全依赖本地声学模型是很难的。

- `TIFA`：`TIFA` 的问题在于它的路线不同，出于模型上下文的限制，动辄 3–4 分钟的歌曲音频无法一次性送入模型。`mms` 系模型可以只在 Wav2Vec2 阶段分片，然后拿整曲声学概率和整曲歌词做对齐；而 `TIFA` 需要把歌词也一起分片，那么问题就陷入如何在对齐之前就得到较可靠的行级时间。排除人工对齐的话，还是需要用 `mms` 模型来做粗对齐，这不仅要做两次完整推理，而且实际效果并不佳。事实上，使用这一路线的 [Timing](https://github.com/Zennmn/Timing) 只有在预先提供准确的行级时间的情况下，对齐效果才能达到或超过 Lazulite Studio 当前路线的水平，而且其超过 Lazulite 的部分也是因为人声分离模型（Timing 使用 BS Karaoke）的差异带来的。

三个模型后端的结果见 [对齐后端与窗口](reports/alignment-backends.md)。

### 对齐策略

一个反直觉的结果是，使用 `NextFire` 模型时，将歌曲和歌词按行分片、每行分别对齐并不能带来收益。在测试集上，逐行对齐的准确率甚至稍低于人声片段整体拼接；而且逐行对齐依赖人工提供的行级时间，如果使用整曲结果自动粗分行级时间，最终准确率会更低。见 [对齐后端与窗口](reports/alignment-backends.md)。

**复杂的对齐算法并不能带来显著收益**。以当前路线作为基线，对 [MiliKara](https://github.com/BilyHurington/MiliKara) 所使用的算法模块进行消融实验，结果显示这些看似漂亮的 trick 并没有多少实际提升。见 [MiliKara 消融](reports/milikara.md) 和 [异常行局部重算](reports/local-refinement.md)。

`MMS_FA` 模型的过早结束可以通过适当的后处理大幅改进。事实上，[FA-Kara](https://github.com/moriwx/FA-Kara) 以及借鉴了其算法的 Lazulite Studio，使用静音搜索和下一单元起始共同限定的方式，就将 `MMS_FA` 模型的对齐结果改进到了接近 `NextFire` 的水平。

### 自动注音

Lazulite Studio 的“智能日文注音”使用 Sudachi + JmdictFurigana，以行作为单位处理以充分利用上下文。在跨平台方案中，基于 Sudachi 这一技术路线的 Lazulite Studio 和 SUG 的注音准确率以及整行完全匹配率做到了不依赖 Windows 和 LLM 的最佳，超过了 MiliKara 和 Timing 使用的 MeCab／UniDic 或 pykakasi 路线；在 Windows 平台上，SUG 调用系统原生 WinRT 接口可进一步提升至 96.49%。而在仅靠文本的情况下，LLM 也无法做到完全正确，最好的结果仅做到注音准确率 97.63% 和整行完全匹配率 95.10%。见 [自动注音](reports/auto-reading.md)。

## 报告目录

| 报告 | 内容说明 |
| --- | --- |
| [八条路线对齐比较](reports/comparison.md) | 对比 8 条主流工具路线在人工读音（各自分离器／统一 BS Karaoke）与自动分词注音三组条件下的对齐准确率及叠唱表现 |
| [测试集](datasets/README.md)与[评价方法](reports/methods.md) | 14 段录音与 15 份标注说明；共同正文边界与人工读音边界的构造方法及评价指标定义 |
| [模型分离性能](reports/separation-performance.md) | 10 种人声分离模型的候选配置、参数量，以及 GPU 整曲与 CPU 片段的耗时、内存、显存和能耗实测 |
| [模型下游对齐](reports/separation-alignment.md) | 10 种人声分离模型在完整人声、片段拼接、带缓冲拼接以及浮点／24 位 FLAC 保存路径下的下游对齐表现 |
| [对齐后端与窗口](reports/alignment-backends.md) | NextFire、TIFA、MMS_FA 三种对齐后端在整曲拼接与逐行窗口下的对比，以及 MMS_FA 行内空隙填补实验 |
| [Timing 完整链路](reports/timing.md) | Timing 两阶段管线（MMS 粗定位 + TIFA 细对齐）在正文输入、人工行窗口及二次细化下的专项诊断 |
| [MiliKara 消融](reports/milikara.md) | 对 MiliKara 的 CTC 解码改动（分隔符处理、停顿与静音软代价、自由尾部）及原曲混音重试机制的消融分析 |
| [自动注音](reports/auto-reading.md) | 对比 Lazulite Studio、SUG（Sudachi／WinRT）、MiliKara、Timing、OpenJTalk 与 GPT-6.1 Terra 的日语自动注音准确率 |
| [异常行局部重算](reports/local-refinement.md) | 检验对首轮对齐中的异常行做局部概率裁剪重解码或局部声学重算能否带来实际收益 |
| [复现说明](reports/reproduce.md) | 独立评分校验与完整实验环境配置、分阶段重跑指南 |

## 快速复核

只重算已发布预测的评分并验证仓库完整性，无需 GPU 或模型权重：

```sh
python3.13 -m venv .venvs/scoring
.venvs/scoring/bin/pip install -r requirements/scoring.txt
.venvs/scoring/bin/python scripts/score.py
python3.13 scripts/verify.py
```

完整推理需要 Linux、Python 3.13、NVIDIA GPU，以及 Git、FFmpeg、Node.js 和 npm，环境安装与分阶段运行步骤见 [复现说明](reports/reproduce.md)。

## 仓库结构

```text
datasets/       原始音频、TTML 标注与文件校验清单
reports/        各专题实验报告
results/        测试集预测、评分汇总与结果图表
configs/        上游源码版本、模型清单与实验配置
scripts/        环境安装、数据准备、模型推理、评分与静态校验脚本
requirements/   研究环境、各工具适配环境与轻量评分依赖锁定清单
licenses/       代码改编对应的第三方许可
```

Git 跟踪测试音频、标注、实验脚本和压缩预测；`.deps`、`.models`、`.cache`、`.venvs` 均被忽略。所有运行路径从仓库根目录派生，公开上游提交固定在 [sources.json](configs/sources.json) 与 [comparison-sources.json](configs/comparison-sources.json)。

代码采用 [AGPL-3.0](LICENSE)。第三方代码、权重、录音和歌词的归属见 [来源与许可](THIRD_PARTY.md)。
