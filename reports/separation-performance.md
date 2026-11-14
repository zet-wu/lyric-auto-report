# 十种人声分离配置的资源实测

GPU 使用固定五首整曲，每首先以最多 30 秒预热，再重复三次；CPU 使用《Rainbow Flower》30–60 秒片段，预热一次后重复三次。十种配置共 180 次正式测量（GPU 150 次、CPU 30 次）。GPU 耗时与能量先逐曲取三次中位数，再对五曲求和；CPU 耗时取片段三次中位数，两种输入范围不用于计算设备加速比。内存与显存取全部运行的峰值。资源测量串行执行，与质量计算错开。

| 配置 | 五曲 GPU s | 30 秒片段 CPU s | GPU 板卡能量 kJ |
| --- | --- | --- | --- |
| Demucs htdemucs | 15.67 | 10.20 | 3.20 |
| SCNet Small | 38.31 | 33.12 | 7.13 |
| DTTNet | 24.67 | 72.26 | 6.79 |
| BS-RoFormer viperx | 73.53 | 318.01 | 28.16 |
| MelBand RoFormer Kim | 38.57 | 119.56 | 13.35 |
| Windowed RoFormer | 19.13 | 44.83 | 6.39 |
| BS Karaoke | 114.00 | 228.16 | 41.61 |
| MDX-Net Inst HQ 3 | 72.04 | 14.18 | 8.33 |
| MelBand RoFormer ep_3005 | 65.58 | 83.35 | 26.36 |
| HybridDemucs MUSDB Plus | 7.87 | 3.32 | 1.54 |

板卡能量按约 20 ms 间隔采样积分，包含空闲功耗。

| 配置 | CPU RSS GiB | GPU RSS GiB | Torch allocated GiB | ONNX 进程显存 GiB |
| --- | --- | --- | --- | --- |
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

RSS（Resident Set Size，驻留集大小）统计进程树的物理内存驻留量，共享页可能重复计入。Torch allocated 为框架张量分配峰值；ONNX 进程显存包含运行时和设备上下文，两列分别呈现，不能直接排名。破折号表示不适用。

## 固定条件与计时

硬件为 NVIDIA GeForce RTX 4090（49140 MiB，驱动 595.58.03）与双路 AMD EPYC 7502。输入统一解码为 44.1 kHz 双声道；随机种子为 0，Torch 使用 8 线程，ONNX 使用 8 个计算线程与 1 个调度线程，有效 batch=1。保留各权重的分块、重叠和归一化；CPU 关闭 CUDA 混合精度并禁用 GPU。

计时包含输入搬运、推理及结果返回 CPU，排除解码、模型加载、编码和写盘。文件入口通过内存适配调用相同算法，并与原生输出核验。BS Karaoke 的 CPU 路径沿用同一底层算法，仅适配设备与混合精度开关。

| 配置 | 参数量／百万 | Torch | audio-separator |
| --- | --- | --- | --- |
| Demucs htdemucs | 41.984 | 2.14.0+cu130 | — |
| SCNet Small | 10.579 | 2.14.0+cu130 | — |
| DTTNet | 4.958 | 2.14.0+cu130 | — |
| BS-RoFormer viperx | 159.758 | 2.14.0+cu130 | — |
| MelBand RoFormer Kim | 228.203 | 2.14.0+cu130 | — |
| Windowed RoFormer | 228.387 | 2.14.0+cu130 | — |
| BS Karaoke | 51.049 | 2.14.0+cu130 | — |
| MDX-Net Inst HQ 3 | 16.684 | 2.14.0+cu130 | 0.47.0 |
| MelBand RoFormer ep_3005 | 251.870 | 2.14.0+cu130 | 0.30.2 |
| HybridDemucs MUSDB Plus | 83.639 | 2.14.0+cu130 | — |

MDX-Net Inst HQ 3 按 ONNX 文件初始化张量的元素总量统计，包含归一化运行统计量；其他配置按 Torch 模型参数元素量统计。

权重、配置、环境和逐次数据见[模型清单](../configs/separation-models.json)、[原始记录](../results/separation-resources)及[五曲输入](../configs/separation-resources-inputs.json)与 [CPU 片段](../configs/separation-cpu-inputs.json)。原生适配核验与人声来源见[下游数据目录](../results/separation-alignment)。单曲实际入口成本见[入口资源报告](resources.md)，固定下游端点见[分离与对齐](separation-alignment.md)。
