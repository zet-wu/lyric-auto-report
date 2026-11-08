# 来源与许可

研究运行时从以下公开仓库下载固定版本，提交记录见 [configs/sources.json](configs/sources.json)。

| 项目 | 用途 |
| --- | --- |
| [Lazulite](https://github.com/wuchenyanmo/Lazulite) | 人声活动分析、音频准备、NextFire 与 MMS_FA |
| [Lazulite Studio](https://github.com/zet-wu/Lazulite-studio) | TTML 投影、注音与罗马字转换 |
| [Timing](https://github.com/Zennmn/Timing) | 项目链路、MMS 定位、TIFA 与分离适配 |
| [MiliKara](https://github.com/BilyHurington/MiliKara) | CTC 解码、活动代价、窗口、重试与尾点处理 |
| [MSST](https://github.com/ZFTurbo/Music-Source-Separation-Training) | SCNet、DTTNet 和 RoFormer 推理 |
| [pyopenjtalk](https://github.com/r9y9/pyopenjtalk) | OpenJTalk 日语发音前端，包版本与词典下载身份固定 |
| [Windowed RoFormer](https://github.com/smulelabs/windowed-roformer) | 局部注意力人声分离 |

[scripts/milikara/fast_ctc.py](scripts/milikara/fast_ctc.py) 改编自 MiliKara 的 CTC 递推，保留上游评分、回溯和并列路径选择。对应 MIT 许可见 [licenses/MiliKara-MIT.txt](licenses/MiliKara-MIT.txt)。

模型权重和词典使用各自发布方的许可；下载清单给出来源与身份。仓库源码的许可不向音乐录音、歌词、模型或词典授予额外权利。音乐和歌词的权利归相应权利人。
