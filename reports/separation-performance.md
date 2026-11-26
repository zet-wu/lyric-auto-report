# 十种人声分离模型的配置与性能实测

人声分离是歌词自动打轴的前置环节：一方面需要尽可能剥离伴奏与背景和声，为下游声学对齐提供干净的人声；另一方面，桌面端打轴工具需要兼顾有独立显卡（GPU）与仅靠 CPU 运行时的耗时、内存开销和能耗。

为了给默认分离器选型提供依据，我们选取了当前主流打轴工具默认采用的分离模型及 MSST（Music-Source-Separation-Training）中的代表性架构，共 **10 种人声分离配置**，在统一硬件环境下实测其 5 首代表曲目的 GPU 整曲推理性能与 `j03` 30 秒片段的 CPU 推理性能。这 10 种分离器对下游歌词对齐准确率的具体影响见 [模型下游对齐与音频持久化](separation-alignment.md)。原始测量记录保存在 [`results/M5/resources.csv`](../results/M5/resources.csv)、[`results/M5/resources-summary.csv`](../results/M5/resources-summary.csv) 及 [`results/M5/summary.json`](../results/M5/summary.json)。

## 核心发现

1. **Demucs（`htdemucs`）在速度、资源开销与下游对齐准确率之间取得了最佳平衡**：
   - 在时长从 175.6 秒到 448.7 秒的 5 首代表曲目（总时长 1,411.23 秒，约 23 分半）上，Demucs 跑完 5 首代表曲目 GPU 耗时仅需 **13.53 s**（平均每首歌 **2.71 s**，实时率 RTF 低至 **0.0096**，5 首曲目 GPU 整卡能耗仅 **2.75 kJ**）；30 秒片段 CPU 推理仅需 **9.04 s**，内存与 Torch 张量显存峰值均在 **1.8 GiB** 以内。同时它在 20 首日语歌下游对齐中达到 **84.51%** 的双端 100 ms 命中率，非常适合作为桌面端默认分离器。
2. **RoFormer 系模型（尤其是 `BS Karaoke`）虽然能带来约 1–2 个百分点的下游精度提升，但计算代价很高**：
   - 下游表现最好的 `BS Karaoke`（86.59%）在 5 首代表曲目上的单轮 GPU 耗时达 **212.04 s**（平均每首 **42.41 s**），是 Demucs 的 **15.67 倍**，单轮 GPU 整卡能耗达 **89.52 kJ**；在 CPU 上跑 30 秒片段耗时 **208.43 s**（是 Demucs 的 **23.06 倍**，跑一首整曲需要半小时以上）。`BS-RoFormer viperx` 在 CPU 上更是达到 Demucs 的 **30.55 倍**（276.05 s）。因此 `BS Karaoke` 更适合在配有独显、或处理有复杂副歌叠唱的曲目时作为高质量可选档位。
3. **`Windowed RoFormer` 将 RoFormer 架构的 GPU 耗时降到了接近 Demucs 的水平，但主机内存占用较高**：
   - 依托局部窗口注意力与 8 秒无重叠分块，`Windowed RoFormer` 的 5 首代表曲目 GPU 耗时仅 **18.02 s**（是 Demucs 的 **1.33 倍**），下游对齐命中率达 **85.04%**；不过它在 GPU 推理期间的主机内存 RSS 峰值达到 **15.32 GiB**（源于分块拼接缓存）。
4. **更小参数量或旧架构模型在速度与下游准确率上未能同时占优**：
   - yohane 使用的 `HybridDemucs MUSDB Plus` 速度最快（5 首曲目 GPU 耗时仅 **6.97 s**，约为 Demucs 的一半），但下游双端 100 ms 命中率跌至 **81.47%**；小参数量的 `SCNet Small`（10.58 M）既比 Demucs 慢（GPU 2.14 倍、CPU 3.66 倍），下游命中率也只有 **81.75%**；SUG 使用的 `MDX-Net Inst HQ 3` 在 CPU 上较快（**15.09 s**，1.67 倍），但在 GPU 上反而比 Demucs 慢 **5.21 倍**（70.51 s）。

---

## 1. 十种候选分离配置与参数量

各配置由模型架构、固定权重及推理分块设置共同确定（模型下载地址与 SHA256 见 [`configs/separation-models.json`](../configs/separation-models.json)）：

| 配置名称 | 代码标识 | 权重来源与实现 | 参数量 (M) | 运行框架 | 在本实验中的比较定位 |
| --- | --- | --- | ---: | --- | --- |
| **Demucs htdemucs** | `demucs` | Lazulite 适配器（官方 `htdemucs`） | 41.984 | Torch 2.11.0+cu130 | Lazulite Studio 默认配置与速度基线 |
| **HybridDemucs MUSDB Plus** | `yohane` | yohane（`HDEMUCS_HIGH_MUSDB_PLUS`） | 83.639 | Torch / torchaudio | yohane 默认采用的快速分离配置 |
| **Windowed RoFormer** | `windowed` | 作者实现（`mbr-win10-sink8`） | 228.387 | Torch 2.11.0+cu130 | 局部窗口注意力与 8 秒无重叠分块推理 |
| **DTTNet** | `dttnet` | MSST（`vocalsg32 ep4082`） | 4.958 | Torch 2.11.0+cu130 | 极小参数量专用人声分离模型 |
| **SCNet Small** | `scnet` | MSST（`musdb18` checkpoint） | 10.579 | Torch 2.11.0+cu130 | 考察小参数量模型的实际推理速度 |
| **MelBand RoFormer Kim** | `mel_roformer` | MSST（`KimberleyJSN MelBandRoformer`） | 228.203 | Torch 2.11.0+cu130 | Timing 通用人声分离采用的权重 |
| **MelBand RoFormer ep_3005** | `milikara` | MiliKara（`ep_3005_sdr_11.4360`） | 251.870 | Torch (`audio-separator`) | MiliKara 默认采用的分离权重 |
| **MDX-Net Inst HQ 3** | `sug` | SUG（`UVR-MDX-NET-Inst_HQ_3.onnx`） | 16.684 | ONNX Runtime (`audio-separator`) | SUG 默认采用的 ONNX 分离配置 |
| **BS-RoFormer viperx** | `bs_roformer` | MSST（`ep_317_sdr_12.9755`） | 159.758 | Torch 2.11.0+cu130 | 高 SDR 通用人声分离代表 |
| **BS Karaoke** | `bs` | Timing / Studio 高质量档（`frazer/becruily`） | 51.049 | Torch 2.11.0+cu130 | 主唱提取模型（抑制背景和声，Studio 高质量档、Timing 与 FA-Kara 采用） |

---

## 2. 预热后纯推理耗时、实时率（RTF）与 GPU 整卡能耗

### 2.1 测试条件

- **测试硬件**：NVIDIA GeForce RTX 4090（49,140 MiB 显存）与双路 AMD EPYC 7502 CPU。
- **测试曲目**：
  - **GPU 整曲测试**：选取覆盖短、中、长时长的 5 首代表曲目——`t01`（175.57 s）、`y02`（211.26 s）、`j06`（247.25 s）、`j11`（328.43 s）、`j02`（448.73 s），单轮 5 首总时长为 **1,411.23 s**。每个模型先预热，随后对 5 首歌曲各重复测量 **3 轮**（共 15 次测量，累计处理音频 **4,233.68 s**）。
  - **CPU 片段测试**：因部分 RoFormer 模型在 CPU 上跑整曲耗时过长，统一使用《Rainbow Flower》（`j03`）的 **30.00 秒片段**，预热后重复测量 **3 轮**（累计处理音频 **90.00 s**）。
- **能耗采集**：GPU 推理期间通过 NVML 按 20 ms 间隔对显卡整卡功率采样积分。宿主机 Linux 内核对非特权用户限制了 CPU RAPL 能耗计数器读取（`/sys/class/powercap/intel-rapl:0/energy_uj` 返回 `PermissionError`），因此 CPU 能耗在 JSON 中记为 `null`。

### 2.2 耗时与 GPU 能耗对比

| 分离模型 | 单曲 GPU 平均耗时 (s) | 5 首代表曲目 GPU 耗时 (s) | GPU 实时率 (RTF) | GPU 相对耗时 | 30 秒片段 CPU 耗时 (s) | CPU 实时率 (RTF) | CPU 相对耗时 | GPU 平均功率 (W) | 5 首曲目 GPU 整卡能耗 (kJ) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **HybridDemucs MUSDB Plus** (`yohane`) | **1.39 ± 0.49** | **6.97** | **0.0049** | **0.51x** | **3.09 ± 0.04** | **0.1031** | **0.34x** | 189.61 | **1.32** |
| **Demucs htdemucs** (`demucs`) | 2.71 ± 0.93 | 13.53 | 0.0096 | 1.00x | 9.04 ± 0.24 | 0.3012 | 1.00x | 203.15 | 2.75 |
| **Windowed RoFormer** (`windowed`) | 3.60 ± 1.30 | 18.02 | 0.0128 | 1.33x | 43.07 ± 0.37 | 1.4358 | 4.77x | 336.69 | 6.07 |
| **DTTNet** (`dttnet`) | 5.07 ± 3.43 | 25.36 | 0.0180 | 1.87x | 71.75 ± 1.02 | 2.3917 | 7.94x | 320.95 | 8.14 |
| **SCNet Small** (`scnet`) | 5.79 ± 1.94 | 28.94 | 0.0205 | 2.14x | 33.05 ± 0.13 | 1.1018 | 3.66x | 208.39 | 6.03 |
| **MelBand RoFormer Kim** (`mel_roformer`) | 6.96 ± 2.43 | 34.79 | 0.0247 | 2.57x | 106.40 ± 0.18 | 3.5467 | 11.77x | 354.89 | 12.35 |
| **MelBand RoFormer ep_3005** (`milikara`) | 12.67 ± 4.55 | 63.34 | 0.0449 | 4.68x | 79.79 ± 1.09 | 2.6597 | 8.83x | 404.61 | 25.63 |
| **MDX-Net Inst HQ 3** (`sug`) | 14.10 ± 4.94 | 70.51 | 0.0500 | 5.21x | 15.09 ± 0.22 | 0.5030 | 1.67x | **107.67** | 7.59 |
| **BS-RoFormer viperx** (`bs_roformer`) | 14.97 ± 4.50 | 74.84 | 0.0530 | 5.53x | 276.05 ± 4.12 | 9.2017 | 30.55x | 387.03 | 28.97 |
| **BS Karaoke** (`bs`) | 42.41 ± 13.40 | 212.04 | 0.1503 | 15.67x | 208.43 ± 1.59 | 6.9478 | 23.06x | 422.20 | 89.52 |

注：表中“5 首代表曲目 GPU 耗时”与“5 首曲目 GPU 整卡能耗”为单轮跑完 5 首整曲的合计值（15 次测量累计总耗时与累计能耗除以 3 轮；15 次累计总值见 [`results/M5/resources-summary.csv`](../results/M5/resources-summary.csv)）。

### 2.3 五首代表曲目的逐曲 GPU 推理耗时（3 次测量均值，单位 s）

| 分离模型 | `t01` (175.6 s) | `y02` (211.3 s) | `j06` (247.2 s) | `j11` (328.4 s) | `j02` (448.7 s) | 随音频时长变化特点 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| **HybridDemucs MUSDB Plus** (`yohane`) | **0.87** | **1.05** | **1.23** | **1.61** | **2.20** | 严格随音频时长线性增长（RTF 恒定 0.0049–0.0050） |
| **Demucs htdemucs** (`demucs`) | 1.71 | 2.04 | 2.39 | 3.14 | 4.24 | 严格随音频时长线性增长（RTF 恒定 0.0095–0.0098） |
| **Windowed RoFormer** (`windowed`) | 2.25 | 2.75 | 3.16 | 4.22 | 5.64 | 8 秒固定窗口线性增长（RTF 0.0126–0.0130） |
| **DTTNet** (`dttnet`) | 2.13 | 2.57 | 2.97 | 6.72 | 10.97 | 超过 300 秒的长曲目上耗时增长加快（RTF 从 0.012 升至 0.024） |
| **SCNet Small** (`scnet`) | 3.68 | 4.38 | 5.15 | 6.74 | 8.99 | 线性增长（RTF 恒定 0.0200–0.0210） |
| **MelBand RoFormer Kim** (`mel_roformer`) | 4.44 | 5.20 | 6.08 | 8.02 | 11.05 | 线性增长（RTF 恒定 0.0244–0.0253） |
| **MelBand RoFormer ep_3005** (`milikara`) | 7.90 | 9.39 | 10.94 | 14.59 | 20.52 | 线性增长（RTF 恒定 0.0443–0.0457） |
| **MDX-Net Inst HQ 3** (`sug`) | 8.85 | 10.50 | 12.16 | 16.34 | 22.65 | ONNX 固定步长分块线性增长（RTF 0.0492–0.0505） |
| **BS-RoFormer viperx** (`bs_roformer`) | 10.27 | 12.01 | 13.71 | 17.56 | 21.30 | 线性增长（RTF 0.0475–0.0585） |
| **BS Karaoke** (`bs`) | 28.10 | 32.35 | 38.49 | 49.40 | 63.70 | 高重叠精细滑动窗口，单曲 3–7.5 分钟需 28–64 秒 |

---

## 3. 内存与显存峰值对比

| 分离模型 | GPU 测试主机内存 RSS 峰值 (MiB / GiB) | CPU 测试主机内存 RSS 峰值 (MiB / GiB) | Torch 张量显存峰值 (MiB / GiB) | 进程级 GPU 显存峰值 (MiB / GiB) |
| --- | ---: | ---: | ---: | ---: |
| **Demucs htdemucs** (`demucs`) | **1,741 MiB (1.70 GiB)** | 1,794 MiB (1.75 GiB) | 1,680 MiB (1.64 GiB) | 5,212 MiB (5.09 GiB) |
| **BS-RoFormer viperx** (`bs_roformer`) | 1,933 MiB (1.89 GiB) | 2,498 MiB (2.44 GiB) | 1,832 MiB (1.79 GiB) | 2,758 MiB (2.69 GiB) |
| **DTTNet** (`dttnet`) | 2,074 MiB (2.03 GiB) | **1,403 MiB (1.37 GiB)** | **957 MiB (0.93 GiB)** | **1,980 MiB (1.93 GiB)** |
| **MelBand RoFormer Kim** (`mel_roformer`) | 2,107 MiB (2.06 GiB) | 2,684 MiB (2.62 GiB) | 2,240 MiB (2.19 GiB) | 3,338 MiB (3.26 GiB) |
| **HybridDemucs MUSDB Plus** (`yohane`) | 2,172 MiB (2.12 GiB) | 2,330 MiB (2.28 GiB) | 1,755 MiB (1.71 GiB) | 5,558 MiB (5.43 GiB) |
| **BS Karaoke** (`bs`) | 2,255 MiB (2.20 GiB) | 2,806 MiB (2.74 GiB) | 1,925 MiB (1.88 GiB) | 3,094 MiB (3.02 GiB) |
| **MelBand RoFormer ep_3005** (`milikara`) | 2,841 MiB (2.77 GiB) | 2,904 MiB (2.84 GiB) | 1,797 MiB (1.75 GiB) | 2,774 MiB (2.71 GiB) |
| **SCNet Small** (`scnet`) | 3,024 MiB (2.95 GiB) | 1,451 MiB (1.42 GiB) | 1,545 MiB (1.51 GiB) | 5,194 MiB (5.07 GiB) |
| **MDX-Net Inst HQ 3** (`sug`) | 3,383 MiB (3.30 GiB) | 3,763 MiB (3.67 GiB) | — (ONNX Runtime) | 2,768 MiB (2.70 GiB) |
| **Windowed RoFormer** (`windowed`) | 15,690 MiB (15.32 GiB) | 2,916 MiB (2.85 GiB) | 1,420 MiB (1.39 GiB) | 2,516 MiB (2.46 GiB) |

说明：Torch 张量显存峰值由 `torch.cuda.max_memory_allocated()` 统计，直接反映模型权重与激活张量的实际显存需求（9 个 PyTorch 模型均在 **0.93–2.19 GiB** 之间，普通 4–6 GiB 显卡即可运行）；进程级 GPU 显存峰值由 NVML 统计，包含 CUDA 上下文、cuFFT 工作区及 PyTorch 显存缓存池。
