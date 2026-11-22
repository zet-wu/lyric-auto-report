# 十种人声分离模型的配置与性能实测

人声分离是歌词自动打轴的前置环节：一方面需要尽可能剥离伴奏与背景和声，为下游声学对齐提供干净的人声；另一方面，桌面端打轴工具需要兼顾有独显（GPU）与仅靠 CPU 运行时的耗时和内存开销。

本实验选取了当前主流打轴工具默认采用的分离模型及 MSST（Music-Source-Separation-Training）中的代表性架构，共 **10 种人声分离配置**，在统一硬件环境下实测其 GPU／CPU 推理速度、内存／显存占用与板卡能耗。这 10 种分离器对下游歌词对齐准确率的具体影响见 [模型下游对齐](separation-alignment.md)。

## 核心发现

1. **Demucs（`htdemucs`）在速度、资源开销与下游对齐收益之间取得了最佳平衡**：
   - 五首整曲 GPU 推理仅需 **15.67 s**（单曲约 3 s，板卡能耗仅 3.20 kJ），30 秒片段 CPU 推理仅需 **10.20 s**，内存与显存峰值均在 **2 GiB** 以内；同时在下游对齐中能达到 **83.89%** 的双端 100 ms 命中率，非常适合作为桌面端默认分离器。
2. **RoFormer 系模型（尤其是 BS Karaoke）虽然能带来约 1–2 个百分点的下游精度提升，但计算代价极高**：
   - 下游表现最好的 `BS Karaoke`（85.83%）在 GPU 上耗时是 Demucs 的 **7.28 倍**（114.00 s，能耗 41.61 kJ），在 CPU 上更是达到 **22.37 倍**（30 秒片段耗时 228.16 s，整曲在 CPU 上将超过 30 分钟）；`BS-RoFormer viperx` 在 CPU 上甚至高达 **31.17 倍**。因此 `BS Karaoke` 更适合在具备高性能独显、或处理存在复杂副歌叠唱的曲目时作为高质量可选方案。
3. **更快的轻量／旧架构模型在下游对齐上存在明显妥协**：
   - yohane 使用的 `HybridDemucs MUSDB Plus` 速度最快（GPU 仅 7.87 s，约为 Demucs 的一半），但下游双端 100 ms 命中率跌至 **81.32%**；小参数量的 `SCNet Small`（10.58 M）既比 Demucs 慢（GPU 2.45 倍），下游命中率也仅 **81.30%**；SUG 使用的 `MDX-Net Inst HQ 3` 在 CPU 上较快（14.18 s），但在 GPU 上反而比 Demucs 慢 4.6 倍，且下游命中率（82.57%）低于 Demucs。

---

## 1. 十种候选分离配置与参数量

配置由模型架构、固定权重及推理分块设置共同确定（模型下载地址与 SHA256 见 [`configs/separation-models.json`](../configs/separation-models.json)）：

| 配置名称 | 权重来源与实现 | 参数量 (M) | 运行框架 | 在本实验中的比较定位 |
| --- | --- | ---: | --- | --- |
| **Demucs htdemucs** | Lazulite 适配器（官方 `htdemucs`） | 41.984 | Torch 2.14.0+cu130 | Lazulite Studio 默认配置与速度基线 |
| **SCNet Small** | MSST，`musdb18` checkpoint | 10.579 | Torch 2.14.0+cu130 | 考察小参数量模型的实际推理速度 |
| **DTTNet** | MSST，`vocalsg32 ep4082` | 4.958 | Torch 2.14.0+cu130 | 极小参数量专用人声分离模型 |
| **BS-RoFormer viperx** | MSST，`ep_317_sdr_12.9755` | 159.758 | Torch 2.14.0+cu130 | 高 SDR 通用人声分离代表 |
| **MelBand RoFormer Kim** | MSST，`KimberleyJSN MelBandRoformer` | 228.203 | Torch 2.14.0+cu130 | Timing 通用人声分离采用的权重 |
| **Windowed RoFormer** | 作者实现，`mbr-win10-sink8` | 228.387 | Torch 2.14.0+cu130 | 局部窗口注意力与 8 秒无重叠分块推理 |
| **BS Karaoke** | Timing，`frazer/becruily` | 51.049 | Torch 2.14.0+cu130 | 主唱提取模型（Timing 默认，FA-Kara 与 G2 采用） |
| **MDX-Net Inst HQ 3** | SUG，`UVR-MDX-NET-Inst_HQ_3.onnx` | 16.684 | ONNX Runtime (`audio-separator` 0.47.0) | SUG 默认采用的 ONNX 分离配置 |
| **MelBand RoFormer ep_3005** | MiliKara，`ep_3005_sdr_11.4360` | 251.870 | Torch (`audio-separator` 0.30.2) | MiliKara 默认采用的分离权重 |
| **HybridDemucs MUSDB Plus** | yohane，`HDEMUCS_HIGH_MUSDB_PLUS` | 83.639 | Torch / torchaudio 2.14.0+cu130 | yohane 默认采用的分离配置 |

注：`MDX-Net Inst HQ 3` 的参数量按 ONNX 初始化张量的元素总数统计（包含归一化统计量），其余模型按 PyTorch `model.parameters()` 元素总数统计。

---

## 2. 预热后纯推理耗时、内存、显存与能耗

### 2.1 测试条件

- **测试硬件**：NVIDIA GeForce RTX 4090（49,140 MiB 显存，驱动 595.58.03）与双路 AMD EPYC 7502 CPU。
- **输入范围**：
  - **GPU 测试**：使用固定的 5 首整曲（`s01`、`s02`、`s03`、`s04`、`s05`，详见 [`separation-resources-inputs.json`](../configs/separation-resources-inputs.json)），每首歌先以最多 30 秒音频预热一次，再正式重复测量 3 次（先对单曲 3 次取中位数，再对 5 首歌曲求和）。
  - **CPU 测试**：因部分 RoFormer 模型在 CPU 上跑整曲耗时过长，统一使用《Rainbow Flower》（`s03`）的 **30–60 秒片段（共 30 秒）**，预热一次后重复测量 3 次取中位数。
- **计时与线程边界**：输入音频统一预先解码为 44.1 kHz 双声道浮点数组；Torch 与 ONNX 均固定使用 8 个计算线程、有效 `batch_size=1`。计时覆盖“输入张量搬运至设备 + 模型推理 + 结果返回 CPU 内存”，不包含音频文件解码、模型权重加载与结果编码写盘。

### 2.2 耗时与 GPU 能耗对比

| 配置 | 五曲整曲 GPU 耗时 (s) | GPU 相对耗时 | 30 秒片段 CPU 耗时 (s) | CPU 相对耗时 | 五曲 GPU 板卡能耗 (kJ) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Demucs htdemucs | 15.67 | 1.00 | 10.20 | 1.00 | 3.20 |
| SCNet Small | 38.31 | 2.45 | 33.12 | 3.25 | 7.13 |
| DTTNet | 24.67 | 1.57 | 72.26 | 7.08 | 6.79 |
| BS-RoFormer viperx | 73.53 | 4.69 | 318.01 | 31.17 | 28.16 |
| MelBand RoFormer Kim | 38.57 | 2.46 | 119.56 | 11.72 | 13.35 |
| Windowed RoFormer | 19.13 | 1.22 | 44.83 | 4.39 | 6.39 |
| BS Karaoke | 114.00 | 7.28 | 228.16 | 22.37 | 41.61 |
| MDX-Net Inst HQ 3 | 72.04 | 4.60 | 14.18 | 1.39 | 8.33 |
| MelBand RoFormer ep_3005 | 65.58 | 4.19 | 83.35 | 8.17 | 26.36 |
| HybridDemucs MUSDB Plus | 7.87 | 0.50 | 3.32 | 0.33 | 1.54 |

注：GPU 板卡能耗通过 NVML 按约 20 ms 间隔对显卡功率采样积分得到（包含推理期间的板卡基础功耗）。

### 2.3 内存与显存峰值对比

| 配置 | CPU 进程内存峰值 RSS (GiB) | GPU 进程内存峰值 RSS (GiB) | Torch 张量显存峰值 (GiB) | ONNX 进程显存峰值 (GiB) |
| --- | ---: | ---: | ---: | ---: |
| Demucs htdemucs | 1.81 | 1.96 | 1.64 | — |
| SCNet Small | 1.29 | 2.63 | 1.50 | — |
| DTTNet | 1.38 | 2.10 | 0.93 | — |
| BS-RoFormer viperx | 2.41 | 2.17 | 1.49 | — |
| MelBand RoFormer Kim | 2.61 | 2.10 | 1.73 | — |
| Windowed RoFormer | 2.83 | 14.90 | 1.39 | — |
| BS Karaoke | 2.87 | 1.79 | 2.00 | — |
| MDX-Net Inst HQ 3 | 3.68 | 3.28 | — | 2.71 |
| MelBand RoFormer ep_3005 | 2.79 | 3.05 | 1.75 | — |
| HybridDemucs MUSDB Plus | 2.23 | 2.04 | 1.72 | — |

说明：RSS（Resident Set Size）为进程树的物理内存驻留峰值；Torch 张量显存峰值由 `torch.cuda.max_memory_allocated()` 统计，而 `MDX-Net Inst HQ 3` 运行于 ONNX Runtime，其显存按进程级 CUDA 显存占用（包含运行时上下文）统计。`Windowed RoFormer` 在 GPU 下出现 14.90 GiB 的主机内存峰值，源于其推理实现中较大规模的块拼接缓存。

---

## 3. 单曲冷启动端到端入口耗时（含加载与解码）

除上述预热后的纯模型推理计时外，在实际命令行或桌面单次任务中，用户感知的耗时还包括**音频解码、模型权重从磁盘加载到显存、推理分离以及结果写出**。以下在单曲 `s01`（时长 218.52 秒）上以独立新进程串行测试两次，对比 Lazulite（Demucs）与 Timing 原生封装（BS Karaoke、Kim Vocals）的完整单曲入口成本：

| 入口路径 | 第一次耗时 (s) | 第二次耗时 (s) | 平均耗时 (s) | 平均实时因子 (RTF) | Torch 显存峰值 (GiB) | 进程总显存峰值 (MiB) | 权重文件大小 (MiB) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Demucs htdemucs** | 3.96 | 4.05 | 4.01 | 0.0183 | 1.01 | 1974 | 80.24 |
| **BS Karaoke** | 21.56 | 21.58 | 21.57 | 0.0987 | 1.77 | 2666 | 194.97 |
| **MelBand RoFormer Kim** | 13.31 | 13.22 | 13.27 | 0.0607 | 2.17 | 2784 | 870.81 |

可以看到，即便算上音频解码、模型加载和 WAV 写出，`Demucs` 处理一首 3 分 38 秒的歌曲端到端也仅需 **4.01 秒**（实时因子 0.0183，权重仅 80.24 MiB），在启动响应与分发体积上均具明显优势。

逐次测量的原始数据保存在 [`results/separation-resources/`](../results/separation-resources/) 与 [`results/ablation/resource-benchmark/`](../results/ablation/resource-benchmark/)。
