# 对齐后端、窗口和人声输入

在固定人工读音的 11 首日语歌曲上，NextFire 配合 BS Karaoke 的 core 拼接取得 86.05% 的双端 100 ms 宏平均命中率。TIFA 依赖较准确的行窗口：同一 Demucs 人声下，整曲推理为 38.32%，人工行窗口为 82.71%。MMS_FA 的起点接近参考，但延音尾点普遍偏早。

主矩阵包含三种人声、三种后端和八种输入策略，共 897 个歌曲条件；补充五种分离器的 NextFire 对照包含 195 个条件。另存三种人声下的产品路径输出。以下主表分母固定为 4590 个纯假名配对单元，歌曲等权；它与保留独立长音符的 [MiliKara 表](milikara.md) 使用不同分母。

## 主要对照

| 后端与策略 | Demucs | BS Karaoke | Kim Vocals |
| --- | ---: | ---: | ---: |
| NextFire：完整人声 | 75.00% | 77.24% | 76.67% |
| NextFire：core 拼接 | 83.91% | 86.05% | 84.88% |
| NextFire：带缓冲拼接 | 83.10% | 85.36% | 83.85% |
| NextFire：自动 NextFire 行窗口 | 74.72% | 79.76% | 79.76% |
| NextFire：人工行窗口 | 80.40% | 84.25% | 83.87% |
| TIFA：完整人声 | 38.32% | 40.75% | 39.78% |
| TIFA：core 拼接 | 44.97% | 52.10% | 52.80% |
| TIFA：自动 NextFire 行窗口 | 77.97% | 79.06% | 79.09% |
| TIFA：人工行窗口 | 82.71% | 82.96% | 82.54% |
| MMS_FA：完整人声 | 22.92% | 22.58% | 22.71% |
| MMS_FA：core 拼接 | 21.97% | 22.19% | 22.34% |
| MMS_FA：人工行窗口 | 22.53% | 22.66% | 22.56% |

人工窗口是已知行位置的诊断条件。NextFire 的整链拼接优于逐行人工窗口，说明保留相邻歌词上下文有实际价值；TIFA 则在短行窗口中明显改善。对齐模型的排序取决于输入组织方式。

![三种后端与人声输入比较](../results/ablation/matrix.png)

NextFire 的 BS Karaoke core 条件命中 3969/4590 个单元，缺失 15 个，误差超过 1 秒的单元为 10 个；对应 Demucs 为 3873、33 和 36 个。把 BS 人声改用 Demucs 的 core 边界后，命中降为 3928、缺失增为 35；Kim 的固定 core 条件则从 3915 增为 3929。分离内容与活动边界共同影响结果。

## 粗定位后的尾点搜索

通用 MMS 粗定位常截短歌唱延音。Timing 静音搜索扩大行尾覆盖范围，但缺失窗口仍限制整条链路。

| 人声 | MMS 可用行/478 | 完整覆盖行 | 加静音搜索后完整覆盖行 | NextFire 自动窗口完整覆盖行 |
| --- | ---: | ---: | ---: | ---: |
| Demucs | 367 | 109 | 347 | 439 |
| BS Karaoke | 430 | 147 | 418 | 445 |
| Kim Vocals | 415 | 132 | 399 | 449 |

静音搜索后可用行分别为 368、431、416。Demucs 中截短尾点超过 200 ms 的行从 184 降为 13，BS 从 197 降为 8，Kim 从 201 降为 11。

在 Demucs 上，NextFire 使用 MMS 窗口的宏平均从 60.55% 提升至 62.98%，TIFA 从 62.97% 提升至 63.98%；两者仍有 908 个评分单元缺失。BS 上两后端分别从 71.19% 提升至 72.49%、从 70.25% 提升至 71.71%。这项修正改善了已定位行的尾点，未解决粗定位缺失。

## 延音与独立长音符

时长至少 600 ms 的 488 个参考单元作为延音代理组。Demucs、人工行窗口条件下，MMS_FA 的结束 MAE 为 902.60 ms，结束偏差为 −897.88 ms，预测/参考时长比中位数为 0.129，100 ms 命中为 0/488；NextFire 为 296/488，TIFA 为 268/488。MMS_FA 的主要问题集中在尾点，继续缩小行窗口不能消除这种偏差。

主表把独立「ー」并入前一单元，因此只评价合并包络。独立长音符内部边界另存在 [边界审计](../results/ablation/standalone-hold-boundaries.json)。[重复元音探针](../results/ablation/duplicate-vowel-probe.json) 进一步比较 8 行中的 10 个内部边界，覆盖三种人声及人工/自动窗口；它属于小样本诊断，不参与主表排序。相邻相同音素的边界记录见 [重复边界](../results/ablation/repeat-boundary-pairs.json)。

## 补充分离器

固定 NextFire 后，core 拼接的宏平均为 SCNet 82.62%、DTTNet 84.74%、BS-RoFormer Viperx 84.96%、MelBand 84.80%、Windowed 85.25%。这里的 BS-RoFormer Viperx 与主表 BS Karaoke 使用不同权重；Kim 与 MelBand 使用同一权重但推理路径不同。

六模型的原始叶级单元和持久化路径比较见 [分离与下游对齐](separation-alignment.md)。本表固定人工读音，不能直接代表正文输入后的完整自动化效果。

## 记录

[协议](../results/ablation/protocol.json)、[完整结果表](../results/ablation/tables.md)、[汇总 JSON](../results/ablation/metrics.json)、[CSV](../results/ablation/summary.csv) 和 [窗口审计](../results/ablation/window-audit.json) 保存全部条件。脚本、模型与评分定义见 [复现说明](reproduce.md) 和 [评价方法](methods.md)。
