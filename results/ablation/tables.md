# 自动生成的消融结果表

主表为 12 首歌曲等权的双端 100 ms 命中率。MAE（Mean Absolute Error）为平均绝对端点误差。BS Karaoke 为主唱提取权重；后端代码 tifa 和 mms_fa 分别对应 TIFA 与 MMS_FA。策略 concat 为核心人声区间拼接，padded 为带缓冲拼接，full 为完整人声；auto_mms / auto_nf 为两种模型预测的自动行窗口，human 为人工行窗口。

## nextfire

| 策略 | Demucs | BS Karaoke | Kim |
| --- | ---: | ---: | ---: |
| concat | 83.68% | 85.80% | 84.78% |
| padded | 82.73% | 85.52% | 83.79% |
| full | 74.28% | 77.16% | 76.66% |
| auto_mms | 55.51% | 70.85% | 70.57% |
| auto_nf | 74.04% | 79.24% | 79.11% |
| human | 79.73% | 83.65% | 83.14% |

## tifa

| 策略 | Demucs | BS Karaoke | Kim |
| --- | ---: | ---: | ---: |
| concat | 43.62% | 51.82% | 51.17% |
| padded | 44.19% | 51.76% | 51.18% |
| full | 38.45% | 40.62% | 39.68% |
| auto_mms | 57.72% | 71.19% | 71.18% |
| auto_nf | 78.40% | 79.11% | 79.44% |
| human | 83.11% | 83.41% | 82.82% |

## mms_fa

| 策略 | Demucs | BS Karaoke | Kim |
| --- | ---: | ---: | ---: |
| concat | 23.14% | 23.51% | 23.53% |
| padded | 22.95% | 23.52% | 23.26% |
| full | 24.24% | 23.91% | 24.10% |
| auto_mms | 14.96% | 20.98% | 20.52% |
| auto_nf | 23.26% | 23.02% | 23.65% |
| human | 23.74% | 23.88% | 23.79% |

## 全部固定分母结果

| 分离 | 后端 | 策略 | 100 ms 数/固定分母 | 宏平均 | 200 ms 数 | 缺失 | >1s | 起/止 MAE ms |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| bs | mms_fa | auto_mms | 1087/5021 | 20.98% | 2499 | 374 | 159 | 38.84/261.45 |
| bs | mms_fa | auto_mms_pause | 1080/5021 | 20.87% | 2498 | 374 | 163 | 43.61/262.09 |
| bs | mms_fa | auto_nf | 1176/5021 | 23.02% | 2686 | 128 | 157 | 38.59/252.38 |
| bs | mms_fa | concat | 1201/5021 | 23.51% | 2688 | 2 | 208 | 62.93/279.04 |
| bs | mms_fa | fixed_cores | 1187/5021 | 23.26% | 2689 | 3 | 196 | 62.25/277.90 |
| bs | mms_fa | full | 1218/5021 | 23.91% | 2725 | 0 | 167 | 49.22/265.92 |
| bs | mms_fa | human | 1215/5021 | 23.88% | 2735 | 0 | 163 | 38.04/255.03 |
| bs | mms_fa | padded | 1204/5021 | 23.52% | 2695 | 1 | 211 | 70.43/286.66 |
| bs | nextfire | auto_mms | 3607/5021 | 70.85% | 4146 | 374 | 92 | 54.08/103.49 |
| bs | nextfire | auto_mms_pause | 3704/5021 | 72.85% | 4229 | 374 | 36 | 61.64/79.78 |
| bs | nextfire | auto_nf | 4005/5021 | 79.24% | 4550 | 128 | 17 | 43.68/55.70 |
| bs | nextfire | concat | 4327/5021 | 85.80% | 4765 | 18 | 13 | 40.07/50.35 |
| bs | nextfire | fixed_cores | 4283/5021 | 84.82% | 4742 | 37 | 19 | 49.20/58.75 |
| bs | nextfire | full | 3901/5021 | 77.16% | 4741 | 0 | 14 | 55.18/70.63 |
| bs | nextfire | human | 4217/5021 | 83.65% | 4745 | 0 | 8 | 38.65/49.94 |
| bs | nextfire | padded | 4314/5021 | 85.52% | 4782 | 4 | 18 | 39.84/49.34 |
| bs | tifa | auto_mms | 3623/5021 | 71.19% | 4250 | 374 | 87 | 53.33/103.16 |
| bs | tifa | auto_mms_pause | 3689/5021 | 72.50% | 4332 | 374 | 46 | 64.82/77.02 |
| bs | tifa | auto_nf | 3992/5021 | 79.11% | 4632 | 128 | 20 | 56.40/65.99 |
| bs | tifa | concat | 2599/5021 | 51.82% | 3159 | 244 | 1201 | 5526.90/5539.22 |
| bs | tifa | fixed_cores | 2655/5021 | 53.01% | 3225 | 204 | 1166 | 4646.21/4648.88 |
| bs | tifa | full | 2046/5021 | 40.62% | 2538 | 173 | 1943 | 11955.73/11889.91 |
| bs | tifa | human | 4198/5021 | 83.41% | 4826 | 0 | 11 | 46.37/55.42 |
| bs | tifa | padded | 2599/5021 | 51.76% | 3175 | 185 | 1255 | 5606.43/5591.06 |
| bs_roformer | nextfire | concat | 4282/5021 | 84.88% | 4721 | 8 | 45 | 47.42/57.15 |
| bs_roformer | nextfire | full | 3846/5021 | 76.04% | 4647 | 0 | 50 | 68.16/84.73 |
| bs_roformer | nextfire | padded | 4246/5021 | 84.22% | 4708 | 1 | 41 | 48.45/58.90 |
| demucs | mms_fa | auto_mms | 736/5021 | 14.96% | 1914 | 1339 | 122 | 40.52/267.70 |
| demucs | mms_fa | auto_mms_pause | 734/5021 | 14.92% | 1905 | 1339 | 124 | 44.32/267.70 |
| demucs | mms_fa | auto_nf | 1189/5021 | 23.26% | 2663 | 170 | 161 | 44.97/257.75 |
| demucs | mms_fa | concat | 1176/5021 | 23.14% | 2655 | 3 | 250 | 124.78/333.58 |
| demucs | mms_fa | full | 1236/5021 | 24.24% | 2729 | 0 | 188 | 76.74/289.15 |
| demucs | mms_fa | human | 1211/5021 | 23.74% | 2737 | 0 | 167 | 42.82/256.10 |
| demucs | mms_fa | padded | 1169/5021 | 22.95% | 2659 | 4 | 256 | 141.62/348.14 |
| demucs | nextfire | auto_mms | 2747/5021 | 55.51% | 3239 | 1339 | 88 | 70.60/118.90 |
| demucs | nextfire | auto_mms_pause | 2857/5021 | 57.73% | 3312 | 1339 | 53 | 78.48/97.06 |
| demucs | nextfire | auto_nf | 3739/5021 | 74.04% | 4422 | 170 | 61 | 75.15/88.10 |
| demucs | nextfire | concat | 4223/5021 | 83.68% | 4687 | 33 | 43 | 55.91/65.17 |
| demucs | nextfire | full | 3751/5021 | 74.28% | 4631 | 0 | 60 | 84.06/101.89 |
| demucs | nextfire | human | 4016/5021 | 79.73% | 4658 | 0 | 25 | 50.23/62.64 |
| demucs | nextfire | padded | 4176/5021 | 82.73% | 4692 | 6 | 41 | 65.63/75.83 |
| demucs | tifa | auto_mms | 2840/5021 | 57.72% | 3356 | 1339 | 67 | 55.55/104.85 |
| demucs | tifa | auto_mms_pause | 2884/5021 | 58.65% | 3418 | 1339 | 35 | 67.45/81.68 |
| demucs | tifa | auto_nf | 3957/5021 | 78.40% | 4564 | 170 | 39 | 64.33/73.36 |
| demucs | tifa | concat | 2174/5021 | 43.62% | 2705 | 302 | 1613 | 9291.70/9307.74 |
| demucs | tifa | full | 1934/5021 | 38.45% | 2403 | 187 | 1980 | 9132.33/9070.84 |
| demucs | tifa | human | 4186/5021 | 83.11% | 4807 | 0 | 15 | 49.13/58.29 |
| demucs | tifa | padded | 2203/5021 | 44.19% | 2728 | 256 | 1609 | 9721.90/9721.41 |
| dttnet | nextfire | concat | 4229/5021 | 83.94% | 4694 | 9 | 52 | 58.49/66.22 |
| dttnet | nextfire | full | 3954/5021 | 78.28% | 4642 | 0 | 62 | 83.79/99.02 |
| dttnet | nextfire | padded | 4225/5021 | 83.73% | 4703 | 1 | 61 | 87.96/93.73 |
| kim | mms_fa | auto_mms | 1012/5021 | 20.52% | 2410 | 506 | 156 | 37.16/263.98 |
| kim | mms_fa | auto_mms_pause | 1008/5021 | 20.44% | 2424 | 506 | 162 | 40.86/262.18 |
| kim | mms_fa | auto_nf | 1206/5021 | 23.65% | 2720 | 69 | 169 | 40.02/256.13 |
| kim | mms_fa | concat | 1197/5021 | 23.53% | 2677 | 2 | 228 | 92.27/309.70 |
| kim | mms_fa | fixed_cores | 1178/5021 | 23.13% | 2660 | 3 | 221 | 97.97/312.56 |
| kim | mms_fa | full | 1229/5021 | 24.10% | 2727 | 0 | 178 | 81.35/301.60 |
| kim | mms_fa | human | 1211/5021 | 23.79% | 2736 | 0 | 163 | 39.29/254.91 |
| kim | mms_fa | padded | 1184/5021 | 23.26% | 2688 | 1 | 212 | 75.44/294.55 |
| kim | nextfire | auto_mms | 3500/5021 | 70.57% | 4019 | 506 | 88 | 45.79/99.34 |
| kim | nextfire | auto_mms_pause | 3610/5021 | 72.82% | 4059 | 506 | 52 | 58.79/80.84 |
| kim | nextfire | auto_nf | 4003/5021 | 79.11% | 4545 | 69 | 58 | 57.76/69.55 |
| kim | nextfire | concat | 4276/5021 | 84.78% | 4717 | 7 | 48 | 45.50/56.37 |
| kim | nextfire | fixed_cores | 4281/5021 | 84.83% | 4706 | 36 | 39 | 52.23/62.15 |
| kim | nextfire | full | 3874/5021 | 76.66% | 4665 | 0 | 48 | 64.48/79.53 |
| kim | nextfire | human | 4194/5021 | 83.14% | 4703 | 0 | 10 | 42.05/53.57 |
| kim | nextfire | padded | 4228/5021 | 83.79% | 4698 | 2 | 57 | 76.54/86.38 |
| kim | tifa | auto_mms | 3513/5021 | 71.18% | 4102 | 506 | 80 | 52.30/102.20 |
| kim | tifa | auto_mms_pause | 3564/5021 | 72.21% | 4189 | 506 | 51 | 66.89/77.47 |
| kim | tifa | auto_nf | 4007/5021 | 79.44% | 4646 | 69 | 39 | 59.47/68.96 |
| kim | tifa | concat | 2558/5021 | 51.17% | 3117 | 166 | 1347 | 7582.80/7583.32 |
| kim | tifa | fixed_cores | 2606/5021 | 52.07% | 3184 | 209 | 1237 | 6420.96/6422.17 |
| kim | tifa | full | 1994/5021 | 39.68% | 2484 | 179 | 1922 | 9550.73/9486.38 |
| kim | tifa | human | 4169/5021 | 82.82% | 4797 | 0 | 26 | 51.11/58.67 |
| kim | tifa | padded | 2560/5021 | 51.18% | 3120 | 144 | 1340 | 7285.23/7282.49 |
| mel_roformer | nextfire | concat | 4276/5021 | 84.76% | 4722 | 8 | 41 | 45.19/55.81 |
| mel_roformer | nextfire | full | 3874/5021 | 76.67% | 4663 | 0 | 48 | 64.02/78.60 |
| mel_roformer | nextfire | padded | 4228/5021 | 83.81% | 4702 | 2 | 53 | 75.97/85.86 |
| scnet | nextfire | concat | 4110/5021 | 81.54% | 4639 | 46 | 63 | 81.06/92.52 |
| scnet | nextfire | full | 3935/5021 | 78.03% | 4654 | 0 | 57 | 82.19/89.19 |
| scnet | nextfire | padded | 4160/5021 | 82.50% | 4687 | 7 | 70 | 118.46/125.12 |
| windowed | nextfire | concat | 4282/5021 | 84.93% | 4712 | 7 | 51 | 48.47/58.38 |
| windowed | nextfire | full | 3840/5021 | 76.05% | 4648 | 0 | 45 | 66.09/81.19 |
| windowed | nextfire | padded | 4224/5021 | 83.77% | 4702 | 2 | 57 | 78.07/88.64 |
| demucs | product | concat | 4260/5021 | 84.44% | 4711 | 7 | 42 | 48.32/58.39 |
| bs | product | concat | 4317/5021 | 85.59% | 4774 | 6 | 12 | 35.34/45.67 |
| kim | product | concat | 4265/5021 | 84.59% | 4718 | 0 | 44 | 46.01/56.61 |

## sustained_600ms

| 分离 | 后端 | 策略 | 分母 | 100ms 命中 | 缺失 | 结束 MAE ms | 结束偏差 ms | 时长比中位数 | 塌缩 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| bs | mms_fa | auto_mms | 533 | 0 | 24 | 944.93 | -941.71 | 0.123 | 486 |
| bs | mms_fa | auto_mms_pause | 533 | 0 | 24 | 931.37 | -916.99 | 0.125 | 481 |
| bs | mms_fa | auto_nf | 533 | 1 | 16 | 921.59 | -917.69 | 0.125 | 490 |
| bs | mms_fa | concat | 533 | 0 | 1 | 948.36 | -941.68 | 0.123 | 516 |
| bs | mms_fa | fixed_cores | 533 | 0 | 2 | 982.69 | -886.52 | 0.123 | 517 |
| bs | mms_fa | full | 533 | 0 | 0 | 974.28 | -908.84 | 0.126 | 516 |
| bs | mms_fa | human | 533 | 4 | 0 | 937.89 | -937.51 | 0.122 | 505 |
| bs | mms_fa | padded | 533 | 0 | 1 | 999.51 | -930.28 | 0.122 | 514 |
| bs | nextfire | auto_mms | 533 | 144 | 24 | 497.67 | -470.62 | 0.690 | 69 |
| bs | nextfire | auto_mms_pause | 533 | 275 | 24 | 163.44 | -43.32 | 0.970 | 18 |
| bs | nextfire | auto_nf | 533 | 295 | 16 | 120.43 | -72.81 | 0.967 | 11 |
| bs | nextfire | concat | 533 | 357 | 3 | 114.22 | -69.57 | 0.987 | 9 |
| bs | nextfire | fixed_cores | 533 | 341 | 22 | 111.22 | -70.60 | 0.980 | 13 |
| bs | nextfire | full | 533 | 305 | 0 | 166.14 | -19.94 | 0.983 | 9 |
| bs | nextfire | human | 533 | 324 | 0 | 116.30 | -88.01 | 0.951 | 11 |
| bs | nextfire | padded | 533 | 345 | 0 | 117.04 | -39.18 | 0.988 | 9 |
| bs | tifa | auto_mms | 533 | 125 | 24 | 495.40 | -482.35 | 0.706 | 57 |
| bs | tifa | auto_mms_pause | 533 | 238 | 24 | 181.09 | -80.25 | 0.962 | 21 |
| bs | tifa | auto_nf | 533 | 260 | 16 | 138.21 | -91.71 | 0.978 | 11 |
| bs | tifa | concat | 533 | 147 | 59 | 7066.58 | -3018.65 | 0.792 | 163 |
| bs | tifa | fixed_cores | 533 | 136 | 68 | 7377.18 | -1704.10 | 0.770 | 156 |
| bs | tifa | full | 533 | 118 | 29 | 16694.38 | 14123.89 | 0.304 | 243 |
| bs | tifa | human | 533 | 310 | 0 | 116.18 | -96.89 | 0.980 | 8 |
| bs | tifa | padded | 533 | 145 | 34 | 7706.58 | 1411.19 | 0.772 | 184 |
| bs_roformer | nextfire | concat | 533 | 347 | 4 | 113.42 | -51.93 | 0.987 | 9 |
| bs_roformer | nextfire | full | 533 | 297 | 0 | 189.85 | -11.99 | 0.984 | 12 |
| bs_roformer | nextfire | padded | 533 | 333 | 1 | 116.61 | -56.21 | 0.984 | 10 |
| demucs | mms_fa | auto_mms | 533 | 0 | 94 | 907.50 | -905.38 | 0.128 | 413 |
| demucs | mms_fa | auto_mms_pause | 533 | 0 | 94 | 896.20 | -884.47 | 0.132 | 407 |
| demucs | mms_fa | auto_nf | 533 | 2 | 29 | 950.92 | -913.98 | 0.125 | 472 |
| demucs | mms_fa | concat | 533 | 0 | 0 | 1026.55 | -846.43 | 0.123 | 512 |
| demucs | mms_fa | full | 533 | 0 | 0 | 1060.62 | -781.78 | 0.126 | 506 |
| demucs | mms_fa | human | 533 | 0 | 0 | 933.54 | -929.21 | 0.123 | 495 |
| demucs | mms_fa | padded | 533 | 1 | 1 | 1066.88 | -793.54 | 0.123 | 503 |
| demucs | nextfire | auto_mms | 533 | 127 | 94 | 454.22 | -433.35 | 0.708 | 52 |
| demucs | nextfire | auto_mms_pause | 533 | 234 | 94 | 166.14 | -71.39 | 0.968 | 15 |
| demucs | nextfire | auto_nf | 533 | 281 | 29 | 178.06 | -48.50 | 0.955 | 22 |
| demucs | nextfire | concat | 533 | 329 | 19 | 147.23 | -18.06 | 0.984 | 12 |
| demucs | nextfire | full | 533 | 278 | 0 | 216.39 | -7.90 | 0.978 | 13 |
| demucs | nextfire | human | 533 | 316 | 0 | 124.00 | -100.21 | 0.955 | 18 |
| demucs | nextfire | padded | 533 | 324 | 2 | 154.24 | -38.75 | 0.982 | 12 |
| demucs | tifa | auto_mms | 533 | 106 | 94 | 458.63 | -451.64 | 0.726 | 40 |
| demucs | tifa | auto_mms_pause | 533 | 199 | 94 | 186.09 | -135.97 | 0.953 | 14 |
| demucs | tifa | auto_nf | 533 | 246 | 29 | 174.18 | -86.40 | 0.966 | 19 |
| demucs | tifa | concat | 533 | 118 | 51 | 10411.54 | -7246.02 | 0.658 | 175 |
| demucs | tifa | full | 533 | 103 | 36 | 11619.81 | 6506.32 | 0.196 | 259 |
| demucs | tifa | human | 533 | 298 | 0 | 127.34 | -108.93 | 0.972 | 11 |
| demucs | tifa | padded | 533 | 124 | 34 | 10496.43 | -5366.28 | 0.643 | 183 |
| dttnet | nextfire | concat | 533 | 333 | 4 | 119.95 | -63.15 | 0.979 | 12 |
| dttnet | nextfire | full | 533 | 293 | 0 | 271.33 | 50.94 | 0.976 | 17 |
| dttnet | nextfire | padded | 533 | 332 | 0 | 171.06 | -110.02 | 0.981 | 13 |
| kim | mms_fa | auto_mms | 533 | 2 | 28 | 945.39 | -944.76 | 0.122 | 482 |
| kim | mms_fa | auto_mms_pause | 533 | 2 | 28 | 927.63 | -913.63 | 0.123 | 478 |
| kim | mms_fa | auto_nf | 533 | 0 | 11 | 942.36 | -937.60 | 0.126 | 495 |
| kim | mms_fa | concat | 533 | 0 | 1 | 963.93 | -952.34 | 0.122 | 516 |
| kim | mms_fa | fixed_cores | 533 | 0 | 0 | 1023.21 | -857.40 | 0.121 | 518 |
| kim | mms_fa | full | 533 | 0 | 0 | 1086.14 | -782.53 | 0.125 | 513 |
| kim | mms_fa | human | 533 | 3 | 0 | 933.07 | -932.33 | 0.124 | 506 |
| kim | mms_fa | padded | 533 | 1 | 0 | 1002.69 | -934.78 | 0.123 | 513 |
| kim | nextfire | auto_mms | 533 | 144 | 28 | 491.13 | -466.74 | 0.690 | 67 |
| kim | nextfire | auto_mms_pause | 533 | 285 | 28 | 168.44 | -44.56 | 0.967 | 17 |
| kim | nextfire | auto_nf | 533 | 299 | 11 | 131.82 | -61.05 | 0.967 | 15 |
| kim | nextfire | concat | 533 | 343 | 4 | 122.26 | -43.96 | 0.987 | 10 |
| kim | nextfire | fixed_cores | 533 | 343 | 20 | 116.31 | -67.34 | 0.979 | 9 |
| kim | nextfire | full | 533 | 306 | 0 | 164.98 | -28.65 | 0.981 | 10 |
| kim | nextfire | human | 533 | 330 | 0 | 114.36 | -83.32 | 0.952 | 13 |
| kim | nextfire | padded | 533 | 343 | 0 | 161.27 | -97.48 | 0.986 | 10 |
| kim | tifa | auto_mms | 533 | 119 | 28 | 490.96 | -479.81 | 0.692 | 53 |
| kim | tifa | auto_mms_pause | 533 | 233 | 28 | 184.08 | -85.19 | 0.961 | 26 |
| kim | tifa | auto_nf | 533 | 262 | 11 | 152.45 | -91.55 | 0.975 | 18 |
| kim | tifa | concat | 533 | 146 | 26 | 10478.06 | -4387.28 | 0.793 | 177 |
| kim | tifa | fixed_cores | 533 | 134 | 66 | 9555.64 | -4347.88 | 0.744 | 168 |
| kim | tifa | full | 533 | 118 | 34 | 14709.74 | 12341.87 | 0.320 | 240 |
| kim | tifa | human | 533 | 305 | 0 | 120.50 | -99.79 | 0.978 | 13 |
| kim | tifa | padded | 533 | 147 | 25 | 9157.65 | -2867.10 | 0.795 | 181 |
| mel_roformer | nextfire | concat | 533 | 344 | 4 | 121.11 | -41.07 | 0.986 | 9 |
| mel_roformer | nextfire | full | 533 | 307 | 0 | 160.74 | -33.04 | 0.981 | 10 |
| mel_roformer | nextfire | padded | 533 | 342 | 0 | 162.28 | -96.71 | 0.986 | 10 |
| scnet | nextfire | concat | 533 | 327 | 16 | 155.84 | -80.04 | 0.967 | 10 |
| scnet | nextfire | full | 533 | 306 | 0 | 145.92 | -60.77 | 0.976 | 9 |
| scnet | nextfire | padded | 533 | 323 | 2 | 274.86 | -5.48 | 0.979 | 14 |
| windowed | nextfire | concat | 533 | 349 | 4 | 118.23 | -48.65 | 0.984 | 13 |
| windowed | nextfire | full | 533 | 297 | 0 | 169.22 | -31.16 | 0.984 | 11 |
| windowed | nextfire | padded | 533 | 337 | 0 | 162.73 | -101.83 | 0.986 | 13 |
| demucs | product | concat | 533 | 341 | 3 | 117.65 | -57.24 | 0.981 | 11 |
| bs | product | concat | 533 | 355 | 0 | 109.95 | -62.70 | 0.985 | 9 |
| kim | product | concat | 533 | 342 | 0 | 121.63 | -44.62 | 0.984 | 8 |

## written_long_mark

| 分离 | 后端 | 策略 | 分母 | 100ms 命中 | 缺失 | 结束 MAE ms | 结束偏差 ms | 时长比中位数 | 塌缩 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| bs | mms_fa | auto_mms | 13 | 0 | 0 | 388.85 | -388.85 | 0.231 | 7 |
| bs | mms_fa | auto_mms_pause | 13 | 0 | 0 | 385.77 | -385.77 | 0.277 | 5 |
| bs | mms_fa | auto_nf | 13 | 0 | 0 | 446.19 | -446.19 | 0.166 | 8 |
| bs | mms_fa | concat | 13 | 0 | 0 | 444.65 | -444.65 | 0.166 | 8 |
| bs | mms_fa | fixed_cores | 13 | 0 | 0 | 432.54 | -432.54 | 0.166 | 8 |
| bs | mms_fa | full | 13 | 0 | 0 | 416.54 | -416.54 | 0.231 | 7 |
| bs | mms_fa | human | 13 | 0 | 0 | 388.85 | -388.85 | 0.214 | 8 |
| bs | mms_fa | padded | 13 | 0 | 0 | 403.31 | -403.31 | 0.166 | 7 |
| bs | nextfire | auto_mms | 13 | 7 | 0 | 179.62 | -104.23 | 0.666 | 2 |
| bs | nextfire | auto_mms_pause | 13 | 8 | 0 | 112.54 | -88.85 | 0.825 | 1 |
| bs | nextfire | auto_nf | 13 | 9 | 0 | 130.88 | -113.88 | 0.825 | 1 |
| bs | nextfire | concat | 13 | 7 | 0 | 106.57 | -86.19 | 0.914 | 1 |
| bs | nextfire | fixed_cores | 13 | 9 | 0 | 99.22 | -78.70 | 0.929 | 1 |
| bs | nextfire | full | 13 | 8 | 0 | 104.69 | -84.23 | 0.942 | 1 |
| bs | nextfire | human | 13 | 8 | 0 | 132.54 | -108.85 | 0.825 | 1 |
| bs | nextfire | padded | 13 | 8 | 0 | 121.89 | -111.00 | 0.813 | 2 |
| bs | tifa | auto_mms | 13 | 13 | 0 | 39.15 | -36.54 | 0.994 | 0 |
| bs | tifa | auto_mms_pause | 13 | 13 | 0 | 39.15 | -36.54 | 0.994 | 0 |
| bs | tifa | auto_nf | 13 | 13 | 0 | 38.17 | -35.42 | 0.994 | 0 |
| bs | tifa | concat | 13 | 7 | 1 | 20378.21 | -20378.21 | 0.893 | 2 |
| bs | tifa | fixed_cores | 13 | 10 | 0 | 6761.28 | -5631.19 | 0.970 | 0 |
| bs | tifa | full | 13 | 7 | 1 | 2165.50 | 2012.16 | 0.875 | 3 |
| bs | tifa | human | 13 | 13 | 0 | 39.92 | -37.31 | 0.989 | 0 |
| bs | tifa | padded | 13 | 7 | 2 | 4516.31 | -3180.94 | 0.857 | 2 |
| bs_roformer | nextfire | concat | 13 | 8 | 0 | 118.90 | -102.66 | 0.875 | 2 |
| bs_roformer | nextfire | full | 13 | 7 | 0 | 151.77 | -124.23 | 0.952 | 2 |
| bs_roformer | nextfire | padded | 13 | 7 | 0 | 146.46 | -128.38 | 0.924 | 2 |
| demucs | mms_fa | auto_mms | 13 | 0 | 3 | 472.10 | -472.10 | 0.218 | 5 |
| demucs | mms_fa | auto_mms_pause | 13 | 0 | 3 | 472.10 | -472.10 | 0.218 | 5 |
| demucs | mms_fa | auto_nf | 13 | 0 | 0 | 415.75 | -415.75 | 0.254 | 6 |
| demucs | mms_fa | concat | 13 | 0 | 0 | 397.16 | -397.16 | 0.301 | 5 |
| demucs | mms_fa | full | 13 | 0 | 0 | 401.15 | -401.15 | 0.231 | 7 |
| demucs | mms_fa | human | 13 | 0 | 0 | 402.69 | -402.69 | 0.214 | 7 |
| demucs | mms_fa | padded | 13 | 0 | 0 | 405.28 | -405.28 | 0.231 | 7 |
| demucs | nextfire | auto_mms | 13 | 3 | 3 | 234.10 | -132.10 | 0.557 | 2 |
| demucs | nextfire | auto_mms_pause | 13 | 4 | 3 | 194.30 | -32.10 | 0.835 | 2 |
| demucs | nextfire | auto_nf | 13 | 5 | 0 | 223.28 | -171.14 | 0.970 | 2 |
| demucs | nextfire | concat | 13 | 5 | 0 | 102.51 | -57.16 | 0.970 | 2 |
| demucs | nextfire | full | 13 | 4 | 0 | 159.46 | -135.00 | 0.698 | 2 |
| demucs | nextfire | human | 13 | 7 | 0 | 128.69 | -79.62 | 0.875 | 1 |
| demucs | nextfire | padded | 13 | 7 | 0 | 124.81 | -94.51 | 0.812 | 1 |
| demucs | tifa | auto_mms | 13 | 10 | 3 | 43.50 | -40.10 | 1.014 | 0 |
| demucs | tifa | auto_mms_pause | 13 | 10 | 3 | 42.50 | -39.10 | 1.014 | 0 |
| demucs | tifa | auto_nf | 13 | 11 | 0 | 53.30 | -50.37 | 0.980 | 0 |
| demucs | tifa | concat | 13 | 4 | 1 | 20831.29 | -17032.71 | 1.031 | 1 |
| demucs | tifa | full | 13 | 7 | 0 | 2273.46 | 2110.38 | 0.956 | 5 |
| demucs | tifa | human | 13 | 13 | 0 | 42.23 | -39.62 | 0.980 | 0 |
| demucs | tifa | padded | 13 | 4 | 2 | 22673.02 | -21344.94 | 1.028 | 3 |
| dttnet | nextfire | concat | 13 | 6 | 0 | 161.33 | -143.56 | 0.875 | 2 |
| dttnet | nextfire | full | 13 | 7 | 0 | 167.00 | -136.54 | 0.687 | 2 |
| dttnet | nextfire | padded | 13 | 6 | 0 | 149.44 | -112.08 | 0.889 | 2 |
| kim | mms_fa | auto_mms | 13 | 0 | 0 | 418.08 | -418.08 | 0.166 | 8 |
| kim | mms_fa | auto_mms_pause | 13 | 0 | 0 | 407.31 | -407.31 | 0.231 | 7 |
| kim | mms_fa | auto_nf | 13 | 0 | 0 | 407.90 | -407.90 | 0.277 | 6 |
| kim | mms_fa | concat | 13 | 0 | 0 | 434.05 | -434.05 | 0.158 | 7 |
| kim | mms_fa | fixed_cores | 13 | 0 | 0 | 432.54 | -432.54 | 0.166 | 8 |
| kim | mms_fa | full | 13 | 0 | 0 | 436.54 | -436.54 | 0.158 | 8 |
| kim | mms_fa | human | 13 | 0 | 0 | 404.23 | -404.23 | 0.190 | 8 |
| kim | mms_fa | padded | 13 | 0 | 0 | 432.28 | -432.28 | 0.166 | 8 |
| kim | nextfire | auto_mms | 13 | 7 | 0 | 157.15 | -81.16 | 0.942 | 2 |
| kim | nextfire | auto_mms_pause | 13 | 6 | 0 | 191.00 | -71.93 | 0.813 | 3 |
| kim | nextfire | auto_nf | 13 | 7 | 0 | 91.04 | -64.83 | 0.970 | 1 |
| kim | nextfire | concat | 13 | 6 | 0 | 127.14 | -89.44 | 0.875 | 1 |
| kim | nextfire | fixed_cores | 13 | 8 | 0 | 110.67 | -83.31 | 0.950 | 1 |
| kim | nextfire | full | 13 | 6 | 0 | 151.62 | -133.46 | 0.970 | 1 |
| kim | nextfire | human | 13 | 8 | 0 | 128.23 | -98.08 | 0.714 | 1 |
| kim | nextfire | padded | 13 | 6 | 0 | 145.81 | -116.89 | 0.942 | 1 |
| kim | tifa | auto_mms | 13 | 12 | 0 | 38.38 | -35.77 | 0.999 | 0 |
| kim | tifa | auto_mms_pause | 13 | 12 | 0 | 41.46 | -38.85 | 0.994 | 0 |
| kim | tifa | auto_nf | 13 | 12 | 0 | 40.62 | -37.90 | 0.994 | 0 |
| kim | tifa | concat | 13 | 6 | 0 | 20130.23 | -20130.23 | 0.942 | 3 |
| kim | tifa | fixed_cores | 13 | 9 | 0 | 10834.64 | -10343.30 | 1.054 | 0 |
| kim | tifa | full | 13 | 7 | 4 | 1393.67 | 1328.78 | 1.054 | 1 |
| kim | tifa | human | 13 | 13 | 0 | 40.69 | -38.08 | 0.989 | 0 |
| kim | tifa | padded | 13 | 7 | 1 | 11304.41 | -10864.86 | 1.034 | 2 |
| mel_roformer | nextfire | concat | 13 | 5 | 0 | 118.06 | -81.46 | 0.970 | 2 |
| mel_roformer | nextfire | full | 13 | 6 | 0 | 151.62 | -133.46 | 0.970 | 1 |
| mel_roformer | nextfire | padded | 13 | 6 | 0 | 139.90 | -107.41 | 0.942 | 2 |
| scnet | nextfire | concat | 13 | 2 | 0 | 183.81 | -155.33 | 0.815 | 3 |
| scnet | nextfire | full | 13 | 5 | 0 | 174.69 | -153.46 | 0.871 | 2 |
| scnet | nextfire | padded | 13 | 6 | 0 | 153.11 | -140.98 | 0.878 | 2 |
| windowed | nextfire | concat | 13 | 6 | 0 | 125.54 | -99.46 | 0.938 | 1 |
| windowed | nextfire | full | 13 | 3 | 0 | 190.08 | -168.85 | 0.687 | 2 |
| windowed | nextfire | padded | 13 | 8 | 0 | 98.04 | -79.19 | 0.957 | 2 |
| demucs | product | concat | 13 | 8 | 0 | 98.75 | -56.12 | 0.970 | 2 |
| bs | product | concat | 13 | 9 | 0 | 92.47 | -72.59 | 0.871 | 1 |
| kim | product | concat | 13 | 7 | 0 | 115.21 | -52.78 | 0.950 | 1 |

## adjacent_identical_phones

| 分离 | 后端 | 策略 | 分母 | 100ms 命中 | 缺失 | 结束 MAE ms | 结束偏差 ms | 时长比中位数 | 塌缩 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| bs | mms_fa | auto_mms | 108 | 18 | 6 | 237.01 | -234.22 | 0.321 | 37 |
| bs | mms_fa | auto_mms_pause | 108 | 19 | 6 | 234.20 | -230.89 | 0.331 | 36 |
| bs | mms_fa | auto_nf | 108 | 14 | 6 | 204.63 | -201.60 | 0.348 | 33 |
| bs | mms_fa | concat | 108 | 16 | 0 | 235.56 | -235.56 | 0.308 | 37 |
| bs | mms_fa | fixed_cores | 108 | 22 | 0 | 231.56 | -210.43 | 0.324 | 34 |
| bs | mms_fa | full | 108 | 19 | 0 | 238.76 | -234.57 | 0.323 | 36 |
| bs | mms_fa | human | 108 | 18 | 0 | 236.83 | -234.20 | 0.321 | 41 |
| bs | mms_fa | padded | 108 | 21 | 0 | 240.83 | -231.74 | 0.318 | 36 |
| bs | nextfire | auto_mms | 108 | 65 | 6 | 113.37 | -85.01 | 0.998 | 13 |
| bs | nextfire | auto_mms_pause | 108 | 74 | 6 | 70.37 | -15.01 | 1.003 | 9 |
| bs | nextfire | auto_nf | 108 | 77 | 6 | 52.37 | -20.82 | 0.998 | 10 |
| bs | nextfire | concat | 108 | 84 | 1 | 47.86 | -15.22 | 1.015 | 6 |
| bs | nextfire | fixed_cores | 108 | 83 | 2 | 57.80 | -35.06 | 1.025 | 6 |
| bs | nextfire | full | 108 | 78 | 0 | 62.50 | -34.02 | 1.008 | 7 |
| bs | nextfire | human | 108 | 80 | 0 | 54.18 | -33.65 | 0.998 | 10 |
| bs | nextfire | padded | 108 | 82 | 0 | 57.47 | -15.81 | 1.017 | 8 |
| bs | tifa | auto_mms | 108 | 74 | 6 | 95.36 | -85.40 | 1.048 | 1 |
| bs | tifa | auto_mms_pause | 108 | 75 | 6 | 80.10 | -38.83 | 1.035 | 0 |
| bs | tifa | auto_nf | 108 | 75 | 6 | 76.18 | -52.88 | 1.048 | 0 |
| bs | tifa | concat | 108 | 48 | 10 | 8310.34 | -6495.02 | 0.996 | 14 |
| bs | tifa | fixed_cores | 108 | 53 | 7 | 3594.59 | -961.23 | 0.994 | 16 |
| bs | tifa | full | 108 | 36 | 2 | 18390.38 | 18250.52 | 0.732 | 34 |
| bs | tifa | human | 108 | 84 | 0 | 64.48 | -53.93 | 1.007 | 0 |
| bs | tifa | padded | 108 | 51 | 5 | 6368.15 | -1802.97 | 0.942 | 22 |
| bs_roformer | nextfire | concat | 108 | 84 | 0 | 71.36 | -28.34 | 1.038 | 6 |
| bs_roformer | nextfire | full | 108 | 73 | 0 | 75.02 | -44.57 | 1.005 | 8 |
| bs_roformer | nextfire | padded | 108 | 82 | 0 | 67.21 | -29.15 | 1.026 | 7 |
| demucs | mms_fa | auto_mms | 108 | 13 | 30 | 232.89 | -232.68 | 0.359 | 26 |
| demucs | mms_fa | auto_mms_pause | 108 | 14 | 30 | 217.22 | -201.91 | 0.368 | 24 |
| demucs | mms_fa | auto_nf | 108 | 18 | 8 | 267.83 | -266.16 | 0.326 | 33 |
| demucs | mms_fa | concat | 108 | 23 | 0 | 233.23 | -232.39 | 0.335 | 34 |
| demucs | mms_fa | full | 108 | 19 | 0 | 231.17 | -228.09 | 0.328 | 34 |
| demucs | mms_fa | human | 108 | 20 | 0 | 235.13 | -231.61 | 0.324 | 37 |
| demucs | mms_fa | padded | 108 | 16 | 0 | 236.06 | -231.39 | 0.335 | 35 |
| demucs | nextfire | auto_mms | 108 | 53 | 30 | 101.78 | -70.12 | 0.983 | 7 |
| demucs | nextfire | auto_mms_pause | 108 | 60 | 30 | 59.22 | -28.58 | 1.000 | 4 |
| demucs | nextfire | auto_nf | 108 | 64 | 8 | 281.41 | 137.04 | 0.942 | 12 |
| demucs | nextfire | concat | 108 | 80 | 2 | 239.48 | 145.18 | 1.000 | 8 |
| demucs | nextfire | full | 108 | 68 | 0 | 327.37 | 59.13 | 1.030 | 10 |
| demucs | nextfire | human | 108 | 78 | 0 | 85.43 | -8.46 | 0.974 | 12 |
| demucs | nextfire | padded | 108 | 74 | 0 | 248.52 | 147.36 | 1.000 | 11 |
| demucs | tifa | auto_mms | 108 | 55 | 30 | 73.27 | -69.61 | 1.045 | 0 |
| demucs | tifa | auto_mms_pause | 108 | 56 | 30 | 78.71 | -45.76 | 1.029 | 0 |
| demucs | tifa | auto_nf | 108 | 67 | 8 | 107.92 | -93.16 | 1.034 | 1 |
| demucs | tifa | concat | 108 | 29 | 10 | 10922.73 | -8372.07 | 0.969 | 25 |
| demucs | tifa | full | 108 | 34 | 1 | 9452.53 | 5076.75 | 0.694 | 39 |
| demucs | tifa | human | 108 | 82 | 0 | 64.26 | -54.67 | 1.024 | 1 |
| demucs | tifa | padded | 108 | 35 | 9 | 10994.29 | -9326.99 | 0.999 | 23 |
| dttnet | nextfire | concat | 108 | 77 | 0 | 65.69 | -12.42 | 1.024 | 5 |
| dttnet | nextfire | full | 108 | 70 | 0 | 145.91 | -102.54 | 1.026 | 9 |
| dttnet | nextfire | padded | 108 | 81 | 0 | 117.27 | -82.02 | 1.008 | 7 |
| kim | mms_fa | auto_mms | 108 | 17 | 14 | 222.14 | -221.97 | 0.321 | 33 |
| kim | mms_fa | auto_mms_pause | 108 | 17 | 14 | 210.01 | -209.84 | 0.323 | 31 |
| kim | mms_fa | auto_nf | 108 | 22 | 2 | 236.78 | -233.29 | 0.316 | 35 |
| kim | mms_fa | concat | 108 | 20 | 0 | 233.58 | -221.19 | 0.312 | 36 |
| kim | mms_fa | fixed_cores | 108 | 21 | 0 | 233.60 | -211.73 | 0.324 | 36 |
| kim | mms_fa | full | 108 | 18 | 0 | 235.43 | -232.72 | 0.320 | 38 |
| kim | mms_fa | human | 108 | 18 | 0 | 244.33 | -220.50 | 0.312 | 41 |
| kim | mms_fa | padded | 108 | 16 | 0 | 240.92 | -229.09 | 0.312 | 36 |
| kim | nextfire | auto_mms | 108 | 66 | 14 | 90.16 | -68.78 | 1.000 | 9 |
| kim | nextfire | auto_mms_pause | 108 | 76 | 14 | 48.54 | -24.74 | 1.000 | 6 |
| kim | nextfire | auto_nf | 108 | 75 | 2 | 65.38 | -31.59 | 1.003 | 8 |
| kim | nextfire | concat | 108 | 80 | 0 | 57.51 | -18.41 | 1.000 | 6 |
| kim | nextfire | fixed_cores | 108 | 80 | 2 | 58.41 | -14.49 | 1.011 | 6 |
| kim | nextfire | full | 108 | 72 | 0 | 74.24 | -45.69 | 1.037 | 8 |
| kim | nextfire | human | 108 | 83 | 0 | 66.06 | -38.46 | 0.984 | 7 |
| kim | nextfire | padded | 108 | 73 | 0 | 121.97 | -77.43 | 1.037 | 5 |
| kim | tifa | auto_mms | 108 | 70 | 14 | 73.46 | -63.46 | 1.029 | 0 |
| kim | tifa | auto_mms_pause | 108 | 67 | 14 | 73.97 | -43.99 | 1.026 | 2 |
| kim | tifa | auto_nf | 108 | 75 | 2 | 95.49 | -83.29 | 1.024 | 4 |
| kim | tifa | concat | 108 | 51 | 5 | 9431.21 | -8032.27 | 0.996 | 16 |
| kim | tifa | fixed_cores | 108 | 48 | 7 | 7608.84 | -6553.78 | 0.962 | 19 |
| kim | tifa | full | 108 | 35 | 3 | 12110.16 | 11012.65 | 0.705 | 33 |
| kim | tifa | human | 108 | 84 | 0 | 64.39 | -53.56 | 0.998 | 0 |
| kim | tifa | padded | 108 | 48 | 6 | 8822.85 | -7283.97 | 0.961 | 18 |
| mel_roformer | nextfire | concat | 108 | 81 | 0 | 59.67 | -19.71 | 1.000 | 7 |
| mel_roformer | nextfire | full | 108 | 72 | 0 | 74.43 | -45.13 | 1.037 | 8 |
| mel_roformer | nextfire | padded | 108 | 75 | 0 | 126.25 | -82.21 | 1.050 | 7 |
| scnet | nextfire | concat | 108 | 77 | 1 | 58.72 | -41.89 | 1.006 | 6 |
| scnet | nextfire | full | 108 | 79 | 0 | 79.57 | -46.24 | 1.030 | 9 |
| scnet | nextfire | padded | 108 | 74 | 0 | 110.49 | -87.81 | 1.022 | 7 |
| windowed | nextfire | concat | 108 | 78 | 0 | 62.35 | -26.25 | 1.000 | 6 |
| windowed | nextfire | full | 108 | 66 | 0 | 82.28 | -50.13 | 1.038 | 9 |
| windowed | nextfire | padded | 108 | 77 | 0 | 136.13 | -89.31 | 1.046 | 9 |
| demucs | product | concat | 108 | 78 | 1 | 91.97 | -9.40 | 1.000 | 6 |
| bs | product | concat | 108 | 84 | 0 | 53.65 | -21.18 | 1.007 | 6 |
| kim | product | concat | 108 | 84 | 0 | 57.48 | -16.58 | 1.011 | 6 |

## same_phone_at_next_boundary

| 分离 | 后端 | 策略 | 分母 | 100ms 命中 | 缺失 | 结束 MAE ms | 结束偏差 ms | 时长比中位数 | 塌缩 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| bs | mms_fa | auto_mms | 84 | 17 | 6 | 255.59 | -241.41 | 0.332 | 22 |
| bs | mms_fa | auto_mms_pause | 84 | 18 | 6 | 253.80 | -239.11 | 0.328 | 24 |
| bs | mms_fa | auto_nf | 84 | 17 | 2 | 251.30 | -243.70 | 0.338 | 23 |
| bs | mms_fa | concat | 84 | 16 | 0 | 271.99 | -260.53 | 0.322 | 23 |
| bs | mms_fa | fixed_cores | 84 | 19 | 0 | 250.64 | -250.64 | 0.324 | 24 |
| bs | mms_fa | full | 84 | 20 | 0 | 254.23 | -242.73 | 0.352 | 23 |
| bs | mms_fa | human | 84 | 19 | 0 | 254.06 | -237.01 | 0.322 | 25 |
| bs | mms_fa | padded | 84 | 17 | 0 | 273.31 | -255.45 | 0.324 | 25 |
| bs | nextfire | auto_mms | 84 | 32 | 6 | 211.05 | 5.25 | 1.079 | 8 |
| bs | nextfire | auto_mms_pause | 84 | 33 | 6 | 184.74 | 86.53 | 1.136 | 6 |
| bs | nextfire | auto_nf | 84 | 36 | 2 | 167.98 | 73.86 | 1.116 | 5 |
| bs | nextfire | concat | 84 | 39 | 0 | 172.37 | 78.52 | 1.077 | 4 |
| bs | nextfire | fixed_cores | 84 | 40 | 0 | 179.24 | 68.17 | 1.038 | 4 |
| bs | nextfire | full | 84 | 36 | 0 | 174.32 | 57.75 | 1.095 | 3 |
| bs | nextfire | human | 84 | 36 | 0 | 160.99 | 50.13 | 1.026 | 7 |
| bs | nextfire | padded | 84 | 32 | 0 | 183.17 | 79.79 | 1.073 | 5 |
| bs | tifa | auto_mms | 84 | 60 | 6 | 97.39 | -58.85 | 1.092 | 1 |
| bs | tifa | auto_mms_pause | 84 | 58 | 6 | 104.13 | -50.00 | 1.099 | 1 |
| bs | tifa | auto_nf | 84 | 63 | 2 | 98.74 | -55.04 | 1.099 | 1 |
| bs | tifa | concat | 84 | 35 | 4 | 8667.35 | -4482.34 | 0.798 | 17 |
| bs | tifa | fixed_cores | 84 | 38 | 3 | 5327.72 | -624.09 | 0.865 | 14 |
| bs | tifa | full | 84 | 28 | 3 | 11898.91 | 11504.59 | 0.629 | 36 |
| bs | tifa | human | 84 | 65 | 0 | 90.80 | -48.08 | 1.104 | 1 |
| bs | tifa | padded | 84 | 34 | 5 | 6630.17 | 378.80 | 0.786 | 18 |
| bs_roformer | nextfire | concat | 84 | 37 | 0 | 201.45 | 110.39 | 1.113 | 3 |
| bs_roformer | nextfire | full | 84 | 32 | 0 | 218.11 | 72.04 | 1.085 | 7 |
| bs_roformer | nextfire | padded | 84 | 33 | 0 | 203.30 | 112.30 | 1.095 | 4 |
| demucs | mms_fa | auto_mms | 84 | 13 | 21 | 284.86 | -282.45 | 0.322 | 18 |
| demucs | mms_fa | auto_mms_pause | 84 | 12 | 21 | 280.42 | -274.20 | 0.322 | 18 |
| demucs | mms_fa | auto_nf | 84 | 16 | 4 | 264.73 | -241.32 | 0.344 | 23 |
| demucs | mms_fa | concat | 84 | 20 | 0 | 263.19 | -254.92 | 0.342 | 27 |
| demucs | mms_fa | full | 84 | 20 | 0 | 250.06 | -242.25 | 0.355 | 24 |
| demucs | mms_fa | human | 84 | 17 | 0 | 264.73 | -229.39 | 0.324 | 25 |
| demucs | mms_fa | padded | 84 | 18 | 0 | 260.47 | -258.71 | 0.330 | 25 |
| demucs | nextfire | auto_mms | 84 | 24 | 21 | 202.76 | -9.12 | 0.927 | 7 |
| demucs | nextfire | auto_mms_pause | 84 | 26 | 21 | 178.54 | 74.06 | 1.079 | 4 |
| demucs | nextfire | auto_nf | 84 | 33 | 4 | 174.33 | 67.18 | 1.028 | 6 |
| demucs | nextfire | concat | 84 | 39 | 0 | 168.74 | 68.88 | 1.036 | 4 |
| demucs | nextfire | full | 84 | 31 | 0 | 177.92 | 41.56 | 1.136 | 6 |
| demucs | nextfire | human | 84 | 35 | 0 | 165.32 | 73.94 | 1.051 | 6 |
| demucs | nextfire | padded | 84 | 33 | 0 | 176.36 | 67.48 | 1.018 | 6 |
| demucs | tifa | auto_mms | 84 | 48 | 21 | 109.08 | -69.91 | 1.102 | 1 |
| demucs | tifa | auto_mms_pause | 84 | 50 | 21 | 98.19 | -64.67 | 1.111 | 0 |
| demucs | tifa | auto_nf | 84 | 60 | 4 | 114.15 | -39.07 | 1.107 | 0 |
| demucs | tifa | concat | 84 | 32 | 1 | 11826.83 | -8428.76 | 0.706 | 24 |
| demucs | tifa | full | 84 | 29 | 3 | 12739.58 | 8417.16 | 0.500 | 36 |
| demucs | tifa | human | 84 | 64 | 0 | 95.68 | -51.89 | 1.109 | 1 |
| demucs | tifa | padded | 84 | 34 | 1 | 12399.39 | -7855.71 | 0.769 | 24 |
| dttnet | nextfire | concat | 84 | 35 | 0 | 192.49 | 95.72 | 1.067 | 4 |
| dttnet | nextfire | full | 84 | 41 | 0 | 202.65 | 84.65 | 1.124 | 5 |
| dttnet | nextfire | padded | 84 | 36 | 0 | 240.75 | 48.88 | 1.132 | 5 |
| kim | mms_fa | auto_mms | 84 | 16 | 7 | 256.55 | -244.26 | 0.343 | 21 |
| kim | mms_fa | auto_mms_pause | 84 | 16 | 7 | 252.13 | -239.33 | 0.333 | 22 |
| kim | mms_fa | auto_nf | 84 | 19 | 1 | 252.93 | -235.33 | 0.326 | 24 |
| kim | mms_fa | concat | 84 | 20 | 0 | 281.08 | -280.96 | 0.322 | 24 |
| kim | mms_fa | fixed_cores | 84 | 20 | 0 | 252.18 | -245.64 | 0.330 | 25 |
| kim | mms_fa | full | 84 | 21 | 0 | 252.73 | -252.73 | 0.333 | 25 |
| kim | mms_fa | human | 84 | 20 | 0 | 247.39 | -226.54 | 0.326 | 23 |
| kim | mms_fa | padded | 84 | 20 | 0 | 255.13 | -254.79 | 0.324 | 25 |
| kim | nextfire | auto_mms | 84 | 30 | 7 | 198.88 | 1.71 | 1.071 | 9 |
| kim | nextfire | auto_mms_pause | 84 | 37 | 7 | 160.60 | 71.06 | 1.114 | 5 |
| kim | nextfire | auto_nf | 84 | 35 | 1 | 189.12 | 106.36 | 1.111 | 5 |
| kim | nextfire | concat | 84 | 34 | 0 | 181.30 | 102.13 | 1.144 | 3 |
| kim | nextfire | fixed_cores | 84 | 36 | 0 | 171.52 | 77.69 | 1.000 | 3 |
| kim | nextfire | full | 84 | 30 | 0 | 200.75 | 82.04 | 1.121 | 6 |
| kim | nextfire | human | 84 | 37 | 0 | 165.73 | 42.03 | 1.000 | 5 |
| kim | nextfire | padded | 84 | 30 | 0 | 207.79 | 60.92 | 1.157 | 2 |
| kim | tifa | auto_mms | 84 | 61 | 7 | 98.16 | -51.41 | 1.114 | 1 |
| kim | tifa | auto_mms_pause | 84 | 60 | 7 | 96.52 | -46.34 | 1.114 | 2 |
| kim | tifa | auto_nf | 84 | 64 | 1 | 101.12 | -52.80 | 1.115 | 2 |
| kim | tifa | concat | 84 | 35 | 4 | 8937.11 | -4274.83 | 0.854 | 18 |
| kim | tifa | fixed_cores | 84 | 37 | 6 | 7978.30 | -4654.29 | 0.903 | 12 |
| kim | tifa | full | 84 | 25 | 2 | 9815.60 | 9519.16 | 0.432 | 34 |
| kim | tifa | human | 84 | 64 | 0 | 91.94 | -43.92 | 1.119 | 1 |
| kim | tifa | padded | 84 | 34 | 4 | 9422.02 | -4916.13 | 0.815 | 20 |
| mel_roformer | nextfire | concat | 84 | 35 | 0 | 179.17 | 95.67 | 1.117 | 4 |
| mel_roformer | nextfire | full | 84 | 30 | 0 | 200.99 | 82.27 | 1.121 | 6 |
| mel_roformer | nextfire | padded | 84 | 31 | 0 | 209.37 | 54.61 | 1.147 | 4 |
| scnet | nextfire | concat | 84 | 35 | 0 | 197.17 | 91.83 | 1.049 | 4 |
| scnet | nextfire | full | 84 | 34 | 0 | 199.92 | 83.70 | 1.092 | 5 |
| scnet | nextfire | padded | 84 | 36 | 0 | 238.44 | 41.97 | 1.072 | 5 |
| windowed | nextfire | concat | 84 | 37 | 0 | 196.16 | 117.22 | 1.140 | 3 |
| windowed | nextfire | full | 84 | 33 | 0 | 210.30 | 94.18 | 1.200 | 5 |
| windowed | nextfire | padded | 84 | 38 | 0 | 236.91 | 61.30 | 1.116 | 5 |
| demucs | product | concat | 84 | 39 | 0 | 171.17 | 67.03 | 1.000 | 4 |
| bs | product | concat | 84 | 40 | 0 | 168.52 | 74.91 | 1.070 | 4 |
| kim | product | concat | 84 | 33 | 0 | 180.63 | 99.31 | 1.127 | 3 |

## 逐歌曲

| 分离 | 后端 | 策略 | 歌曲 | 语言子集 | 分母 | 100 ms | 200 ms | 缺失 | >1s |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| bs | mms_fa | auto_mms | 003 - 撃槍・ガングニール | primary | 401 | 161 | 289 | 0 | 4 |
| bs | mms_fa | auto_mms | POWDER SNOW (Live Ver.) | primary | 347 | 19 | 90 | 0 | 26 |
| bs | mms_fa | auto_mms | Rainbow Flower | primary | 374 | 0 | 0 | 374 | 0 |
| bs | mms_fa | auto_mms | TSU-BA-SA | primary | 359 | 121 | 237 | 0 | 7 |
| bs | mms_fa | auto_mms | The Brave Under The Summer Sky | primary | 398 | 30 | 187 | 0 | 18 |
| bs | mms_fa | auto_mms | Worlds Pain | primary | 507 | 144 | 287 | 0 | 7 |
| bs | mms_fa | auto_mms | 両翼のBrilliance | primary | 506 | 203 | 324 | 0 | 11 |
| bs | mms_fa | auto_mms | 光陰の海原 | primary | 373 | 30 | 145 | 0 | 10 |
| bs | mms_fa | auto_mms | 恋のルチはや♡ローリング | primary | 402 | 115 | 223 | 0 | 5 |
| bs | mms_fa | auto_mms | 恋桜開花前線 | primary | 496 | 52 | 291 | 0 | 19 |
| bs | mms_fa | auto_mms | 白い季節 | primary | 427 | 45 | 151 | 0 | 22 |
| bs | mms_fa | auto_mms | 036 - リトルミラクル -Grip it tight- | primary | 431 | 167 | 275 | 0 | 30 |
| bs | mms_fa | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | mms_fa | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | mms_fa | auto_mms | 骹车破尼-假名注音 | teochew_kana | 449 | 157 | 331 | 0 | 4 |
| bs | mms_fa | auto_mms_pause | 003 - 撃槍・ガングニール | primary | 401 | 158 | 285 | 0 | 4 |
| bs | mms_fa | auto_mms_pause | POWDER SNOW (Live Ver.) | primary | 347 | 22 | 92 | 0 | 26 |
| bs | mms_fa | auto_mms_pause | Rainbow Flower | primary | 374 | 0 | 0 | 374 | 0 |
| bs | mms_fa | auto_mms_pause | TSU-BA-SA | primary | 359 | 123 | 237 | 0 | 6 |
| bs | mms_fa | auto_mms_pause | The Brave Under The Summer Sky | primary | 398 | 28 | 185 | 0 | 17 |
| bs | mms_fa | auto_mms_pause | Worlds Pain | primary | 507 | 147 | 291 | 0 | 7 |
| bs | mms_fa | auto_mms_pause | 両翼のBrilliance | primary | 506 | 196 | 317 | 0 | 12 |
| bs | mms_fa | auto_mms_pause | 光陰の海原 | primary | 373 | 31 | 140 | 0 | 10 |
| bs | mms_fa | auto_mms_pause | 恋のルチはや♡ローリング | primary | 402 | 114 | 226 | 0 | 6 |
| bs | mms_fa | auto_mms_pause | 恋桜開花前線 | primary | 496 | 54 | 293 | 0 | 20 |
| bs | mms_fa | auto_mms_pause | 白い季節 | primary | 427 | 44 | 155 | 0 | 23 |
| bs | mms_fa | auto_mms_pause | 036 - リトルミラクル -Grip it tight- | primary | 431 | 163 | 277 | 0 | 32 |
| bs | mms_fa | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | mms_fa | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | mms_fa | auto_mms_pause | 骹车破尼-假名注音 | teochew_kana | 449 | 159 | 325 | 0 | 4 |
| bs | mms_fa | auto_nf | 003 - 撃槍・ガングニール | primary | 401 | 156 | 285 | 0 | 4 |
| bs | mms_fa | auto_nf | POWDER SNOW (Live Ver.) | primary | 347 | 24 | 92 | 0 | 26 |
| bs | mms_fa | auto_nf | Rainbow Flower | primary | 374 | 111 | 209 | 44 | 10 |
| bs | mms_fa | auto_nf | TSU-BA-SA | primary | 359 | 116 | 234 | 0 | 7 |
| bs | mms_fa | auto_nf | The Brave Under The Summer Sky | primary | 398 | 24 | 177 | 23 | 16 |
| bs | mms_fa | auto_nf | Worlds Pain | primary | 507 | 144 | 291 | 0 | 8 |
| bs | mms_fa | auto_nf | 両翼のBrilliance | primary | 506 | 196 | 319 | 13 | 10 |
| bs | mms_fa | auto_nf | 光陰の海原 | primary | 373 | 35 | 138 | 16 | 10 |
| bs | mms_fa | auto_nf | 恋のルチはや♡ローリング | primary | 402 | 100 | 223 | 0 | 5 |
| bs | mms_fa | auto_nf | 恋桜開花前線 | primary | 496 | 59 | 290 | 0 | 19 |
| bs | mms_fa | auto_nf | 白い季節 | primary | 427 | 50 | 156 | 0 | 22 |
| bs | mms_fa | auto_nf | 036 - リトルミラクル -Grip it tight- | primary | 431 | 161 | 272 | 32 | 20 |
| bs | mms_fa | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | mms_fa | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | mms_fa | auto_nf | 骹车破尼-假名注音 | teochew_kana | 449 | 155 | 306 | 23 | 5 |
| bs | mms_fa | concat | 003 - 撃槍・ガングニール | primary | 401 | 156 | 288 | 0 | 4 |
| bs | mms_fa | concat | POWDER SNOW (Live Ver.) | primary | 347 | 20 | 91 | 0 | 26 |
| bs | mms_fa | concat | Rainbow Flower | primary | 374 | 124 | 229 | 1 | 28 |
| bs | mms_fa | concat | TSU-BA-SA | primary | 359 | 118 | 233 | 0 | 7 |
| bs | mms_fa | concat | The Brave Under The Summer Sky | primary | 398 | 29 | 185 | 0 | 17 |
| bs | mms_fa | concat | Worlds Pain | primary | 507 | 137 | 283 | 0 | 7 |
| bs | mms_fa | concat | 両翼のBrilliance | primary | 506 | 212 | 311 | 1 | 11 |
| bs | mms_fa | concat | 光陰の海原 | primary | 373 | 34 | 139 | 0 | 9 |
| bs | mms_fa | concat | 恋のルチはや♡ローリング | primary | 402 | 100 | 213 | 0 | 31 |
| bs | mms_fa | concat | 恋桜開花前線 | primary | 496 | 58 | 287 | 0 | 20 |
| bs | mms_fa | concat | 白い季節 | primary | 427 | 49 | 160 | 0 | 22 |
| bs | mms_fa | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 164 | 269 | 0 | 26 |
| bs | mms_fa | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | mms_fa | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | mms_fa | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 164 | 321 | 1 | 5 |
| bs | mms_fa | fixed_cores | 003 - 撃槍・ガングニール | primary | 401 | 163 | 290 | 0 | 4 |
| bs | mms_fa | fixed_cores | POWDER SNOW (Live Ver.) | primary | 347 | 20 | 90 | 0 | 25 |
| bs | mms_fa | fixed_cores | Rainbow Flower | primary | 374 | 125 | 228 | 0 | 28 |
| bs | mms_fa | fixed_cores | TSU-BA-SA | primary | 359 | 114 | 230 | 0 | 7 |
| bs | mms_fa | fixed_cores | The Brave Under The Summer Sky | primary | 398 | 28 | 190 | 0 | 17 |
| bs | mms_fa | fixed_cores | Worlds Pain | primary | 507 | 141 | 287 | 0 | 7 |
| bs | mms_fa | fixed_cores | 両翼のBrilliance | primary | 506 | 202 | 311 | 1 | 16 |
| bs | mms_fa | fixed_cores | 光陰の海原 | primary | 373 | 28 | 140 | 0 | 9 |
| bs | mms_fa | fixed_cores | 恋のルチはや♡ローリング | primary | 402 | 103 | 215 | 1 | 14 |
| bs | mms_fa | fixed_cores | 恋桜開花前線 | primary | 496 | 51 | 285 | 0 | 20 |
| bs | mms_fa | fixed_cores | 白い季節 | primary | 427 | 49 | 158 | 1 | 23 |
| bs | mms_fa | fixed_cores | 036 - リトルミラクル -Grip it tight- | primary | 431 | 163 | 265 | 0 | 26 |
| bs | mms_fa | fixed_cores | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | mms_fa | fixed_cores | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | mms_fa | fixed_cores | 骹车破尼-假名注音 | teochew_kana | 449 | 173 | 333 | 3 | 4 |
| bs | mms_fa | full | 003 - 撃槍・ガングニール | primary | 401 | 161 | 293 | 0 | 4 |
| bs | mms_fa | full | POWDER SNOW (Live Ver.) | primary | 347 | 20 | 97 | 0 | 26 |
| bs | mms_fa | full | Rainbow Flower | primary | 374 | 133 | 230 | 0 | 11 |
| bs | mms_fa | full | TSU-BA-SA | primary | 359 | 117 | 235 | 0 | 6 |
| bs | mms_fa | full | The Brave Under The Summer Sky | primary | 398 | 29 | 186 | 0 | 17 |
| bs | mms_fa | full | Worlds Pain | primary | 507 | 141 | 288 | 0 | 7 |
| bs | mms_fa | full | 両翼のBrilliance | primary | 506 | 202 | 312 | 0 | 12 |
| bs | mms_fa | full | 光陰の海原 | primary | 373 | 29 | 139 | 0 | 10 |
| bs | mms_fa | full | 恋のルチはや♡ローリング | primary | 402 | 120 | 229 | 0 | 5 |
| bs | mms_fa | full | 恋桜開花前線 | primary | 496 | 54 | 287 | 0 | 20 |
| bs | mms_fa | full | 白い季節 | primary | 427 | 46 | 155 | 0 | 23 |
| bs | mms_fa | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 166 | 274 | 0 | 26 |
| bs | mms_fa | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | mms_fa | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | mms_fa | full | 骹车破尼-假名注音 | teochew_kana | 449 | 162 | 329 | 0 | 5 |
| bs | mms_fa | human | 003 - 撃槍・ガングニール | primary | 401 | 162 | 291 | 0 | 4 |
| bs | mms_fa | human | POWDER SNOW (Live Ver.) | primary | 347 | 21 | 93 | 0 | 27 |
| bs | mms_fa | human | Rainbow Flower | primary | 374 | 132 | 230 | 0 | 10 |
| bs | mms_fa | human | TSU-BA-SA | primary | 359 | 123 | 238 | 0 | 6 |
| bs | mms_fa | human | The Brave Under The Summer Sky | primary | 398 | 30 | 189 | 0 | 17 |
| bs | mms_fa | human | Worlds Pain | primary | 507 | 143 | 287 | 0 | 7 |
| bs | mms_fa | human | 両翼のBrilliance | primary | 506 | 196 | 317 | 0 | 11 |
| bs | mms_fa | human | 光陰の海原 | primary | 373 | 33 | 146 | 0 | 10 |
| bs | mms_fa | human | 恋のルチはや♡ローリング | primary | 402 | 112 | 221 | 0 | 5 |
| bs | mms_fa | human | 恋桜開花前線 | primary | 496 | 56 | 293 | 0 | 19 |
| bs | mms_fa | human | 白い季節 | primary | 427 | 46 | 153 | 0 | 21 |
| bs | mms_fa | human | 036 - リトルミラクル -Grip it tight- | primary | 431 | 161 | 277 | 0 | 26 |
| bs | mms_fa | human | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 4 | 36 | 0 | 15 |
| bs | mms_fa | human | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | mms_fa | human | 骹车破尼-假名注音 | teochew_kana | 449 | 162 | 326 | 0 | 3 |
| bs | mms_fa | padded | 003 - 撃槍・ガングニール | primary | 401 | 155 | 285 | 0 | 4 |
| bs | mms_fa | padded | POWDER SNOW (Live Ver.) | primary | 347 | 17 | 92 | 0 | 26 |
| bs | mms_fa | padded | Rainbow Flower | primary | 374 | 128 | 236 | 0 | 28 |
| bs | mms_fa | padded | TSU-BA-SA | primary | 359 | 114 | 227 | 0 | 7 |
| bs | mms_fa | padded | The Brave Under The Summer Sky | primary | 398 | 29 | 186 | 0 | 17 |
| bs | mms_fa | padded | Worlds Pain | primary | 507 | 149 | 293 | 0 | 7 |
| bs | mms_fa | padded | 両翼のBrilliance | primary | 506 | 211 | 306 | 1 | 11 |
| bs | mms_fa | padded | 光陰の海原 | primary | 373 | 33 | 141 | 0 | 10 |
| bs | mms_fa | padded | 恋のルチはや♡ローリング | primary | 402 | 105 | 212 | 0 | 33 |
| bs | mms_fa | padded | 恋桜開花前線 | primary | 496 | 59 | 286 | 0 | 20 |
| bs | mms_fa | padded | 白い季節 | primary | 427 | 45 | 162 | 0 | 22 |
| bs | mms_fa | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 159 | 269 | 0 | 26 |
| bs | mms_fa | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | mms_fa | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | mms_fa | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 164 | 325 | 0 | 4 |
| bs | nextfire | auto_mms | 003 - 撃槍・ガングニール | primary | 401 | 344 | 374 | 0 | 4 |
| bs | nextfire | auto_mms | POWDER SNOW (Live Ver.) | primary | 347 | 253 | 293 | 0 | 15 |
| bs | nextfire | auto_mms | Rainbow Flower | primary | 374 | 0 | 0 | 374 | 0 |
| bs | nextfire | auto_mms | TSU-BA-SA | primary | 359 | 286 | 336 | 0 | 4 |
| bs | nextfire | auto_mms | The Brave Under The Summer Sky | primary | 398 | 272 | 336 | 0 | 6 |
| bs | nextfire | auto_mms | Worlds Pain | primary | 507 | 431 | 469 | 0 | 8 |
| bs | nextfire | auto_mms | 両翼のBrilliance | primary | 506 | 384 | 455 | 0 | 6 |
| bs | nextfire | auto_mms | 光陰の海原 | primary | 373 | 255 | 322 | 0 | 4 |
| bs | nextfire | auto_mms | 恋のルチはや♡ローリング | primary | 402 | 340 | 375 | 0 | 4 |
| bs | nextfire | auto_mms | 恋桜開花前線 | primary | 496 | 422 | 462 | 0 | 12 |
| bs | nextfire | auto_mms | 白い季節 | primary | 427 | 331 | 356 | 0 | 12 |
| bs | nextfire | auto_mms | 036 - リトルミラクル -Grip it tight- | primary | 431 | 289 | 368 | 0 | 17 |
| bs | nextfire | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | nextfire | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | nextfire | auto_mms | 骹车破尼-假名注音 | teochew_kana | 449 | 234 | 339 | 0 | 4 |
| bs | nextfire | auto_mms_pause | 003 - 撃槍・ガングニール | primary | 401 | 344 | 375 | 0 | 0 |
| bs | nextfire | auto_mms_pause | POWDER SNOW (Live Ver.) | primary | 347 | 269 | 312 | 0 | 4 |
| bs | nextfire | auto_mms_pause | Rainbow Flower | primary | 374 | 0 | 0 | 374 | 0 |
| bs | nextfire | auto_mms_pause | TSU-BA-SA | primary | 359 | 288 | 327 | 0 | 0 |
| bs | nextfire | auto_mms_pause | The Brave Under The Summer Sky | primary | 398 | 268 | 347 | 0 | 3 |
| bs | nextfire | auto_mms_pause | Worlds Pain | primary | 507 | 435 | 466 | 0 | 7 |
| bs | nextfire | auto_mms_pause | 両翼のBrilliance | primary | 506 | 370 | 443 | 0 | 2 |
| bs | nextfire | auto_mms_pause | 光陰の海原 | primary | 373 | 268 | 344 | 0 | 0 |
| bs | nextfire | auto_mms_pause | 恋のルチはや♡ローリング | primary | 402 | 343 | 372 | 0 | 0 |
| bs | nextfire | auto_mms_pause | 恋桜開花前線 | primary | 496 | 434 | 465 | 0 | 1 |
| bs | nextfire | auto_mms_pause | 白い季節 | primary | 427 | 354 | 386 | 0 | 5 |
| bs | nextfire | auto_mms_pause | 036 - リトルミラクル -Grip it tight- | primary | 431 | 331 | 392 | 0 | 14 |
| bs | nextfire | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | nextfire | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | nextfire | auto_mms_pause | 骹车破尼-假名注音 | teochew_kana | 449 | 234 | 344 | 0 | 3 |
| bs | nextfire | auto_nf | 003 - 撃槍・ガングニール | primary | 401 | 343 | 384 | 0 | 0 |
| bs | nextfire | auto_nf | POWDER SNOW (Live Ver.) | primary | 347 | 268 | 316 | 0 | 4 |
| bs | nextfire | auto_nf | Rainbow Flower | primary | 374 | 232 | 285 | 44 | 6 |
| bs | nextfire | auto_nf | TSU-BA-SA | primary | 359 | 300 | 344 | 0 | 3 |
| bs | nextfire | auto_nf | The Brave Under The Summer Sky | primary | 398 | 263 | 333 | 23 | 0 |
| bs | nextfire | auto_nf | Worlds Pain | primary | 507 | 456 | 482 | 0 | 0 |
| bs | nextfire | auto_nf | 両翼のBrilliance | primary | 506 | 392 | 461 | 13 | 2 |
| bs | nextfire | auto_nf | 光陰の海原 | primary | 373 | 266 | 325 | 16 | 0 |
| bs | nextfire | auto_nf | 恋のルチはや♡ローリング | primary | 402 | 353 | 374 | 0 | 0 |
| bs | nextfire | auto_nf | 恋桜開花前線 | primary | 496 | 446 | 484 | 0 | 0 |
| bs | nextfire | auto_nf | 白い季節 | primary | 427 | 369 | 395 | 0 | 0 |
| bs | nextfire | auto_nf | 036 - リトルミラクル -Grip it tight- | primary | 431 | 317 | 367 | 32 | 2 |
| bs | nextfire | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | nextfire | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | nextfire | auto_nf | 骹车破尼-假名注音 | teochew_kana | 449 | 224 | 334 | 23 | 14 |
| bs | nextfire | concat | 003 - 撃槍・ガングニール | primary | 401 | 345 | 382 | 0 | 0 |
| bs | nextfire | concat | POWDER SNOW (Live Ver.) | primary | 347 | 287 | 317 | 0 | 1 |
| bs | nextfire | concat | Rainbow Flower | primary | 374 | 284 | 327 | 10 | 4 |
| bs | nextfire | concat | TSU-BA-SA | primary | 359 | 319 | 350 | 0 | 3 |
| bs | nextfire | concat | The Brave Under The Summer Sky | primary | 398 | 319 | 380 | 2 | 0 |
| bs | nextfire | concat | Worlds Pain | primary | 507 | 471 | 490 | 0 | 0 |
| bs | nextfire | concat | 両翼のBrilliance | primary | 506 | 428 | 481 | 1 | 2 |
| bs | nextfire | concat | 光陰の海原 | primary | 373 | 292 | 348 | 1 | 0 |
| bs | nextfire | concat | 恋のルチはや♡ローリング | primary | 402 | 375 | 399 | 0 | 0 |
| bs | nextfire | concat | 恋桜開花前線 | primary | 496 | 460 | 491 | 0 | 0 |
| bs | nextfire | concat | 白い季節 | primary | 427 | 389 | 403 | 1 | 0 |
| bs | nextfire | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 358 | 397 | 3 | 3 |
| bs | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | nextfire | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 310 | 371 | 2 | 7 |
| bs | nextfire | fixed_cores | 003 - 撃槍・ガングニール | primary | 401 | 352 | 378 | 5 | 0 |
| bs | nextfire | fixed_cores | POWDER SNOW (Live Ver.) | primary | 347 | 276 | 307 | 12 | 1 |
| bs | nextfire | fixed_cores | Rainbow Flower | primary | 374 | 288 | 336 | 0 | 0 |
| bs | nextfire | fixed_cores | TSU-BA-SA | primary | 359 | 321 | 350 | 0 | 3 |
| bs | nextfire | fixed_cores | The Brave Under The Summer Sky | primary | 398 | 303 | 374 | 6 | 0 |
| bs | nextfire | fixed_cores | Worlds Pain | primary | 507 | 469 | 491 | 2 | 0 |
| bs | nextfire | fixed_cores | 両翼のBrilliance | primary | 506 | 431 | 480 | 1 | 6 |
| bs | nextfire | fixed_cores | 光陰の海原 | primary | 373 | 263 | 341 | 2 | 0 |
| bs | nextfire | fixed_cores | 恋のルチはや♡ローリング | primary | 402 | 378 | 399 | 1 | 0 |
| bs | nextfire | fixed_cores | 恋桜開花前線 | primary | 496 | 458 | 484 | 1 | 0 |
| bs | nextfire | fixed_cores | 白い季節 | primary | 427 | 389 | 401 | 5 | 0 |
| bs | nextfire | fixed_cores | 036 - リトルミラクル -Grip it tight- | primary | 431 | 355 | 401 | 2 | 9 |
| bs | nextfire | fixed_cores | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | nextfire | fixed_cores | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | nextfire | fixed_cores | 骹车破尼-假名注音 | teochew_kana | 449 | 305 | 366 | 2 | 7 |
| bs | nextfire | full | 003 - 撃槍・ガングニール | primary | 401 | 319 | 379 | 0 | 0 |
| bs | nextfire | full | POWDER SNOW (Live Ver.) | primary | 347 | 256 | 314 | 0 | 1 |
| bs | nextfire | full | Rainbow Flower | primary | 374 | 270 | 340 | 0 | 0 |
| bs | nextfire | full | TSU-BA-SA | primary | 359 | 284 | 347 | 0 | 3 |
| bs | nextfire | full | The Brave Under The Summer Sky | primary | 398 | 262 | 372 | 0 | 0 |
| bs | nextfire | full | Worlds Pain | primary | 507 | 424 | 487 | 0 | 0 |
| bs | nextfire | full | 両翼のBrilliance | primary | 506 | 426 | 483 | 0 | 3 |
| bs | nextfire | full | 光陰の海原 | primary | 373 | 232 | 336 | 0 | 4 |
| bs | nextfire | full | 恋のルチはや♡ローリング | primary | 402 | 341 | 396 | 0 | 0 |
| bs | nextfire | full | 恋桜開花前線 | primary | 496 | 406 | 489 | 0 | 0 |
| bs | nextfire | full | 白い季節 | primary | 427 | 352 | 399 | 0 | 0 |
| bs | nextfire | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 329 | 399 | 0 | 3 |
| bs | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | nextfire | full | 骹车破尼-假名注音 | teochew_kana | 449 | 246 | 341 | 0 | 19 |
| bs | nextfire | human | 003 - 撃槍・ガングニール | primary | 401 | 351 | 382 | 0 | 0 |
| bs | nextfire | human | POWDER SNOW (Live Ver.) | primary | 347 | 286 | 319 | 0 | 2 |
| bs | nextfire | human | Rainbow Flower | primary | 374 | 309 | 349 | 0 | 0 |
| bs | nextfire | human | TSU-BA-SA | primary | 359 | 299 | 347 | 0 | 0 |
| bs | nextfire | human | The Brave Under The Summer Sky | primary | 398 | 287 | 367 | 0 | 0 |
| bs | nextfire | human | Worlds Pain | primary | 507 | 471 | 493 | 0 | 0 |
| bs | nextfire | human | 両翼のBrilliance | primary | 506 | 404 | 474 | 0 | 2 |
| bs | nextfire | human | 光陰の海原 | primary | 373 | 287 | 344 | 0 | 0 |
| bs | nextfire | human | 恋のルチはや♡ローリング | primary | 402 | 354 | 393 | 0 | 0 |
| bs | nextfire | human | 恋桜開花前線 | primary | 496 | 461 | 490 | 0 | 0 |
| bs | nextfire | human | 白い季節 | primary | 427 | 376 | 394 | 0 | 0 |
| bs | nextfire | human | 036 - リトルミラクル -Grip it tight- | primary | 431 | 332 | 393 | 0 | 4 |
| bs | nextfire | human | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 69 | 97 | 0 | 0 |
| bs | nextfire | human | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | nextfire | human | 骹车破尼-假名注音 | teochew_kana | 449 | 254 | 349 | 0 | 0 |
| bs | nextfire | padded | 003 - 撃槍・ガングニール | primary | 401 | 356 | 383 | 0 | 0 |
| bs | nextfire | padded | POWDER SNOW (Live Ver.) | primary | 347 | 279 | 315 | 0 | 2 |
| bs | nextfire | padded | Rainbow Flower | primary | 374 | 285 | 329 | 4 | 6 |
| bs | nextfire | padded | TSU-BA-SA | primary | 359 | 323 | 350 | 0 | 3 |
| bs | nextfire | padded | The Brave Under The Summer Sky | primary | 398 | 318 | 380 | 0 | 0 |
| bs | nextfire | padded | Worlds Pain | primary | 507 | 468 | 493 | 0 | 0 |
| bs | nextfire | padded | 両翼のBrilliance | primary | 506 | 428 | 481 | 0 | 2 |
| bs | nextfire | padded | 光陰の海原 | primary | 373 | 280 | 349 | 0 | 0 |
| bs | nextfire | padded | 恋のルチはや♡ローリング | primary | 402 | 370 | 397 | 0 | 0 |
| bs | nextfire | padded | 恋桜開花前線 | primary | 496 | 458 | 489 | 0 | 0 |
| bs | nextfire | padded | 白い季節 | primary | 427 | 373 | 407 | 0 | 0 |
| bs | nextfire | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 376 | 409 | 0 | 5 |
| bs | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | nextfire | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 255 | 353 | 0 | 11 |
| bs | tifa | auto_mms | 003 - 撃槍・ガングニール | primary | 401 | 367 | 389 | 0 | 4 |
| bs | tifa | auto_mms | POWDER SNOW (Live Ver.) | primary | 347 | 255 | 288 | 0 | 15 |
| bs | tifa | auto_mms | Rainbow Flower | primary | 374 | 0 | 0 | 374 | 0 |
| bs | tifa | auto_mms | TSU-BA-SA | primary | 359 | 311 | 342 | 0 | 4 |
| bs | tifa | auto_mms | The Brave Under The Summer Sky | primary | 398 | 230 | 361 | 0 | 6 |
| bs | tifa | auto_mms | Worlds Pain | primary | 507 | 442 | 481 | 0 | 4 |
| bs | tifa | auto_mms | 両翼のBrilliance | primary | 506 | 421 | 481 | 0 | 7 |
| bs | tifa | auto_mms | 光陰の海原 | primary | 373 | 236 | 325 | 0 | 4 |
| bs | tifa | auto_mms | 恋のルチはや♡ローリング | primary | 402 | 330 | 373 | 0 | 5 |
| bs | tifa | auto_mms | 恋桜開花前線 | primary | 496 | 357 | 460 | 0 | 12 |
| bs | tifa | auto_mms | 白い季節 | primary | 427 | 323 | 364 | 0 | 10 |
| bs | tifa | auto_mms | 036 - リトルミラクル -Grip it tight- | primary | 431 | 351 | 386 | 0 | 16 |
| bs | tifa | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | tifa | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | tifa | auto_mms | 骹车破尼-假名注音 | teochew_kana | 449 | 284 | 401 | 0 | 4 |
| bs | tifa | auto_mms_pause | 003 - 撃槍・ガングニール | primary | 401 | 365 | 390 | 0 | 0 |
| bs | tifa | auto_mms_pause | POWDER SNOW (Live Ver.) | primary | 347 | 265 | 309 | 0 | 3 |
| bs | tifa | auto_mms_pause | Rainbow Flower | primary | 374 | 0 | 0 | 374 | 0 |
| bs | tifa | auto_mms_pause | TSU-BA-SA | primary | 359 | 312 | 342 | 0 | 1 |
| bs | tifa | auto_mms_pause | The Brave Under The Summer Sky | primary | 398 | 237 | 361 | 0 | 1 |
| bs | tifa | auto_mms_pause | Worlds Pain | primary | 507 | 451 | 491 | 0 | 2 |
| bs | tifa | auto_mms_pause | 両翼のBrilliance | primary | 506 | 421 | 482 | 0 | 2 |
| bs | tifa | auto_mms_pause | 光陰の海原 | primary | 373 | 241 | 338 | 0 | 4 |
| bs | tifa | auto_mms_pause | 恋のルチはや♡ローリング | primary | 402 | 341 | 382 | 0 | 5 |
| bs | tifa | auto_mms_pause | 恋桜開花前線 | primary | 496 | 367 | 470 | 0 | 4 |
| bs | tifa | auto_mms_pause | 白い季節 | primary | 427 | 339 | 384 | 0 | 5 |
| bs | tifa | auto_mms_pause | 036 - リトルミラクル -Grip it tight- | primary | 431 | 350 | 383 | 0 | 19 |
| bs | tifa | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | tifa | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | tifa | auto_mms_pause | 骹车破尼-假名注音 | teochew_kana | 449 | 289 | 405 | 0 | 2 |
| bs | tifa | auto_nf | 003 - 撃槍・ガングニール | primary | 401 | 374 | 395 | 0 | 0 |
| bs | tifa | auto_nf | POWDER SNOW (Live Ver.) | primary | 347 | 264 | 312 | 0 | 1 |
| bs | tifa | auto_nf | Rainbow Flower | primary | 374 | 287 | 313 | 44 | 7 |
| bs | tifa | auto_nf | TSU-BA-SA | primary | 359 | 317 | 345 | 0 | 1 |
| bs | tifa | auto_nf | The Brave Under The Summer Sky | primary | 398 | 223 | 345 | 23 | 0 |
| bs | tifa | auto_nf | Worlds Pain | primary | 507 | 462 | 498 | 0 | 0 |
| bs | tifa | auto_nf | 両翼のBrilliance | primary | 506 | 422 | 475 | 13 | 0 |
| bs | tifa | auto_nf | 光陰の海原 | primary | 373 | 233 | 320 | 16 | 4 |
| bs | tifa | auto_nf | 恋のルチはや♡ローリング | primary | 402 | 340 | 383 | 0 | 2 |
| bs | tifa | auto_nf | 恋桜開花前線 | primary | 496 | 385 | 482 | 0 | 0 |
| bs | tifa | auto_nf | 白い季節 | primary | 427 | 342 | 390 | 0 | 3 |
| bs | tifa | auto_nf | 036 - リトルミラクル -Grip it tight- | primary | 431 | 343 | 374 | 32 | 2 |
| bs | tifa | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs | tifa | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs | tifa | auto_nf | 骹车破尼-假名注音 | teochew_kana | 449 | 274 | 384 | 23 | 9 |
| bs | tifa | concat | 003 - 撃槍・ガングニール | primary | 401 | 224 | 245 | 25 | 107 |
| bs | tifa | concat | POWDER SNOW (Live Ver.) | primary | 347 | 169 | 195 | 3 | 113 |
| bs | tifa | concat | Rainbow Flower | primary | 374 | 178 | 193 | 15 | 156 |
| bs | tifa | concat | TSU-BA-SA | primary | 359 | 292 | 331 | 1 | 3 |
| bs | tifa | concat | The Brave Under The Summer Sky | primary | 398 | 123 | 225 | 22 | 126 |
| bs | tifa | concat | Worlds Pain | primary | 507 | 285 | 322 | 22 | 138 |
| bs | tifa | concat | 両翼のBrilliance | primary | 506 | 268 | 324 | 7 | 91 |
| bs | tifa | concat | 光陰の海原 | primary | 373 | 124 | 184 | 65 | 95 |
| bs | tifa | concat | 恋のルチはや♡ローリング | primary | 402 | 291 | 339 | 1 | 18 |
| bs | tifa | concat | 恋桜開花前線 | primary | 496 | 245 | 318 | 4 | 118 |
| bs | tifa | concat | 白い季節 | primary | 427 | 190 | 232 | 15 | 133 |
| bs | tifa | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 210 | 251 | 64 | 103 |
| bs | tifa | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 62 | 91 | 3 | 3 |
| bs | tifa | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 24 | 37 | 40 | 68 |
| bs | tifa | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 262 | 372 | 19 | 3 |
| bs | tifa | fixed_cores | 003 - 撃槍・ガングニール | primary | 401 | 292 | 340 | 8 | 1 |
| bs | tifa | fixed_cores | POWDER SNOW (Live Ver.) | primary | 347 | 169 | 194 | 10 | 100 |
| bs | tifa | fixed_cores | Rainbow Flower | primary | 374 | 163 | 183 | 10 | 157 |
| bs | tifa | fixed_cores | TSU-BA-SA | primary | 359 | 291 | 331 | 2 | 3 |
| bs | tifa | fixed_cores | The Brave Under The Summer Sky | primary | 398 | 123 | 226 | 28 | 119 |
| bs | tifa | fixed_cores | Worlds Pain | primary | 507 | 282 | 321 | 23 | 136 |
| bs | tifa | fixed_cores | 両翼のBrilliance | primary | 506 | 264 | 314 | 4 | 123 |
| bs | tifa | fixed_cores | 光陰の海原 | primary | 373 | 127 | 184 | 62 | 103 |
| bs | tifa | fixed_cores | 恋のルチはや♡ローリング | primary | 402 | 293 | 336 | 5 | 17 |
| bs | tifa | fixed_cores | 恋桜開花前線 | primary | 496 | 234 | 300 | 15 | 150 |
| bs | tifa | fixed_cores | 白い季節 | primary | 427 | 193 | 225 | 24 | 138 |
| bs | tifa | fixed_cores | 036 - リトルミラクル -Grip it tight- | primary | 431 | 224 | 271 | 13 | 119 |
| bs | tifa | fixed_cores | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 56 | 81 | 7 | 2 |
| bs | tifa | fixed_cores | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 24 | 35 | 39 | 70 |
| bs | tifa | fixed_cores | 骹车破尼-假名注音 | teochew_kana | 449 | 273 | 376 | 21 | 3 |
| bs | tifa | full | 003 - 撃槍・ガングニール | primary | 401 | 236 | 261 | 6 | 88 |
| bs | tifa | full | POWDER SNOW (Live Ver.) | primary | 347 | 1 | 2 | 84 | 258 |
| bs | tifa | full | Rainbow Flower | primary | 374 | 207 | 236 | 1 | 120 |
| bs | tifa | full | TSU-BA-SA | primary | 359 | 235 | 266 | 12 | 62 |
| bs | tifa | full | The Brave Under The Summer Sky | primary | 398 | 96 | 187 | 2 | 172 |
| bs | tifa | full | Worlds Pain | primary | 507 | 226 | 260 | 21 | 177 |
| bs | tifa | full | 両翼のBrilliance | primary | 506 | 186 | 234 | 12 | 227 |
| bs | tifa | full | 光陰の海原 | primary | 373 | 127 | 185 | 14 | 128 |
| bs | tifa | full | 恋のルチはや♡ローリング | primary | 402 | 230 | 275 | 1 | 104 |
| bs | tifa | full | 恋桜開花前線 | primary | 496 | 197 | 256 | 5 | 194 |
| bs | tifa | full | 白い季節 | primary | 427 | 136 | 168 | 10 | 221 |
| bs | tifa | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 169 | 208 | 5 | 192 |
| bs | tifa | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 62 | 91 | 0 | 0 |
| bs | tifa | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 11 | 23 | 4 | 102 |
| bs | tifa | full | 骹车破尼-假名注音 | teochew_kana | 449 | 158 | 209 | 31 | 170 |
| bs | tifa | human | 003 - 撃槍・ガングニール | primary | 401 | 375 | 396 | 0 | 0 |
| bs | tifa | human | POWDER SNOW (Live Ver.) | primary | 347 | 281 | 319 | 0 | 0 |
| bs | tifa | human | Rainbow Flower | primary | 374 | 345 | 369 | 0 | 1 |
| bs | tifa | human | TSU-BA-SA | primary | 359 | 323 | 352 | 0 | 0 |
| bs | tifa | human | The Brave Under The Summer Sky | primary | 398 | 243 | 376 | 0 | 0 |
| bs | tifa | human | Worlds Pain | primary | 507 | 462 | 502 | 0 | 0 |
| bs | tifa | human | 両翼のBrilliance | primary | 506 | 438 | 495 | 0 | 0 |
| bs | tifa | human | 光陰の海原 | primary | 373 | 252 | 340 | 0 | 4 |
| bs | tifa | human | 恋のルチはや♡ローリング | primary | 402 | 354 | 387 | 0 | 2 |
| bs | tifa | human | 恋桜開花前線 | primary | 496 | 393 | 481 | 0 | 0 |
| bs | tifa | human | 白い季節 | primary | 427 | 351 | 395 | 0 | 2 |
| bs | tifa | human | 036 - リトルミラクル -Grip it tight- | primary | 431 | 381 | 414 | 0 | 2 |
| bs | tifa | human | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 74 | 103 | 0 | 0 |
| bs | tifa | human | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 104 | 141 | 0 | 0 |
| bs | tifa | human | 骹车破尼-假名注音 | teochew_kana | 449 | 320 | 419 | 0 | 0 |
| bs | tifa | padded | 003 - 撃槍・ガングニール | primary | 401 | 228 | 253 | 26 | 102 |
| bs | tifa | padded | POWDER SNOW (Live Ver.) | primary | 347 | 163 | 185 | 0 | 115 |
| bs | tifa | padded | Rainbow Flower | primary | 374 | 171 | 184 | 8 | 165 |
| bs | tifa | padded | TSU-BA-SA | primary | 359 | 289 | 334 | 1 | 3 |
| bs | tifa | padded | The Brave Under The Summer Sky | primary | 398 | 122 | 226 | 28 | 119 |
| bs | tifa | padded | Worlds Pain | primary | 507 | 281 | 317 | 25 | 136 |
| bs | tifa | padded | 両翼のBrilliance | primary | 506 | 264 | 320 | 9 | 119 |
| bs | tifa | padded | 光陰の海原 | primary | 373 | 127 | 184 | 67 | 87 |
| bs | tifa | padded | 恋のルチはや♡ローリング | primary | 402 | 285 | 335 | 0 | 15 |
| bs | tifa | padded | 恋桜開花前線 | primary | 496 | 254 | 326 | 0 | 129 |
| bs | tifa | padded | 白い季節 | primary | 427 | 189 | 237 | 18 | 125 |
| bs | tifa | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 226 | 274 | 3 | 140 |
| bs | tifa | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 63 | 92 | 0 | 2 |
| bs | tifa | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 24 | 37 | 36 | 72 |
| bs | tifa | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 274 | 381 | 0 | 5 |
| bs_roformer | nextfire | concat | 003 - 撃槍・ガングニール | primary | 401 | 347 | 380 | 0 | 0 |
| bs_roformer | nextfire | concat | POWDER SNOW (Live Ver.) | primary | 347 | 274 | 315 | 1 | 1 |
| bs_roformer | nextfire | concat | Rainbow Flower | primary | 374 | 277 | 311 | 1 | 12 |
| bs_roformer | nextfire | concat | TSU-BA-SA | primary | 359 | 328 | 349 | 0 | 3 |
| bs_roformer | nextfire | concat | The Brave Under The Summer Sky | primary | 398 | 329 | 385 | 2 | 0 |
| bs_roformer | nextfire | concat | Worlds Pain | primary | 507 | 467 | 490 | 0 | 0 |
| bs_roformer | nextfire | concat | 両翼のBrilliance | primary | 506 | 413 | 463 | 0 | 12 |
| bs_roformer | nextfire | concat | 光陰の海原 | primary | 373 | 267 | 343 | 2 | 0 |
| bs_roformer | nextfire | concat | 恋のルチはや♡ローリング | primary | 402 | 369 | 399 | 0 | 0 |
| bs_roformer | nextfire | concat | 恋桜開花前線 | primary | 496 | 459 | 489 | 1 | 0 |
| bs_roformer | nextfire | concat | 白い季節 | primary | 427 | 390 | 411 | 0 | 0 |
| bs_roformer | nextfire | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 362 | 386 | 1 | 17 |
| bs_roformer | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs_roformer | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs_roformer | nextfire | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 320 | 380 | 1 | 4 |
| bs_roformer | nextfire | full | 003 - 撃槍・ガングニール | primary | 401 | 326 | 372 | 0 | 0 |
| bs_roformer | nextfire | full | POWDER SNOW (Live Ver.) | primary | 347 | 245 | 312 | 0 | 1 |
| bs_roformer | nextfire | full | Rainbow Flower | primary | 374 | 241 | 307 | 0 | 12 |
| bs_roformer | nextfire | full | TSU-BA-SA | primary | 359 | 281 | 343 | 0 | 3 |
| bs_roformer | nextfire | full | The Brave Under The Summer Sky | primary | 398 | 272 | 375 | 0 | 0 |
| bs_roformer | nextfire | full | Worlds Pain | primary | 507 | 422 | 486 | 0 | 0 |
| bs_roformer | nextfire | full | 両翼のBrilliance | primary | 506 | 407 | 463 | 0 | 13 |
| bs_roformer | nextfire | full | 光陰の海原 | primary | 373 | 235 | 331 | 0 | 4 |
| bs_roformer | nextfire | full | 恋のルチはや♡ローリング | primary | 402 | 336 | 395 | 0 | 0 |
| bs_roformer | nextfire | full | 恋桜開花前線 | primary | 496 | 403 | 487 | 0 | 0 |
| bs_roformer | nextfire | full | 白い季節 | primary | 427 | 351 | 397 | 0 | 0 |
| bs_roformer | nextfire | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 327 | 379 | 0 | 17 |
| bs_roformer | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs_roformer | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs_roformer | nextfire | full | 骹车破尼-假名注音 | teochew_kana | 449 | 239 | 346 | 0 | 10 |
| bs_roformer | nextfire | padded | 003 - 撃槍・ガングニール | primary | 401 | 346 | 379 | 0 | 0 |
| bs_roformer | nextfire | padded | POWDER SNOW (Live Ver.) | primary | 347 | 279 | 317 | 0 | 1 |
| bs_roformer | nextfire | padded | Rainbow Flower | primary | 374 | 277 | 310 | 0 | 11 |
| bs_roformer | nextfire | padded | TSU-BA-SA | primary | 359 | 318 | 350 | 0 | 3 |
| bs_roformer | nextfire | padded | The Brave Under The Summer Sky | primary | 398 | 330 | 382 | 0 | 0 |
| bs_roformer | nextfire | padded | Worlds Pain | primary | 507 | 462 | 494 | 0 | 0 |
| bs_roformer | nextfire | padded | 両翼のBrilliance | primary | 506 | 414 | 462 | 0 | 12 |
| bs_roformer | nextfire | padded | 光陰の海原 | primary | 373 | 282 | 342 | 0 | 0 |
| bs_roformer | nextfire | padded | 恋のルチはや♡ローリング | primary | 402 | 367 | 399 | 0 | 0 |
| bs_roformer | nextfire | padded | 恋桜開花前線 | primary | 496 | 457 | 488 | 0 | 0 |
| bs_roformer | nextfire | padded | 白い季節 | primary | 427 | 375 | 404 | 1 | 0 |
| bs_roformer | nextfire | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 339 | 381 | 0 | 14 |
| bs_roformer | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| bs_roformer | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| bs_roformer | nextfire | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 273 | 354 | 3 | 8 |
| demucs | mms_fa | auto_mms | 003 - 撃槍・ガングニール | primary | 401 | 164 | 296 | 0 | 4 |
| demucs | mms_fa | auto_mms | POWDER SNOW (Live Ver.) | primary | 347 | 20 | 92 | 0 | 25 |
| demucs | mms_fa | auto_mms | Rainbow Flower | primary | 374 | 123 | 219 | 0 | 10 |
| demucs | mms_fa | auto_mms | TSU-BA-SA | primary | 359 | 117 | 239 | 0 | 7 |
| demucs | mms_fa | auto_mms | The Brave Under The Summer Sky | primary | 398 | 32 | 193 | 0 | 18 |
| demucs | mms_fa | auto_mms | Worlds Pain | primary | 507 | 151 | 280 | 0 | 7 |
| demucs | mms_fa | auto_mms | 両翼のBrilliance | primary | 506 | 0 | 0 | 506 | 0 |
| demucs | mms_fa | auto_mms | 光陰の海原 | primary | 373 | 31 | 144 | 0 | 10 |
| demucs | mms_fa | auto_mms | 恋のルチはや♡ローリング | primary | 402 | 0 | 0 | 402 | 0 |
| demucs | mms_fa | auto_mms | 恋桜開花前線 | primary | 496 | 52 | 294 | 0 | 19 |
| demucs | mms_fa | auto_mms | 白い季節 | primary | 427 | 46 | 157 | 0 | 22 |
| demucs | mms_fa | auto_mms | 036 - リトルミラクル -Grip it tight- | primary | 431 | 0 | 0 | 431 | 0 |
| demucs | mms_fa | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | mms_fa | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | mms_fa | auto_mms | 骹车破尼-假名注音 | teochew_kana | 449 | 164 | 336 | 0 | 5 |
| demucs | mms_fa | auto_mms_pause | 003 - 撃槍・ガングニール | primary | 401 | 159 | 286 | 0 | 5 |
| demucs | mms_fa | auto_mms_pause | POWDER SNOW (Live Ver.) | primary | 347 | 21 | 93 | 0 | 25 |
| demucs | mms_fa | auto_mms_pause | Rainbow Flower | primary | 374 | 123 | 222 | 0 | 15 |
| demucs | mms_fa | auto_mms_pause | TSU-BA-SA | primary | 359 | 117 | 237 | 0 | 7 |
| demucs | mms_fa | auto_mms_pause | The Brave Under The Summer Sky | primary | 398 | 33 | 191 | 0 | 17 |
| demucs | mms_fa | auto_mms_pause | Worlds Pain | primary | 507 | 148 | 287 | 0 | 7 |
| demucs | mms_fa | auto_mms_pause | 両翼のBrilliance | primary | 506 | 0 | 0 | 506 | 0 |
| demucs | mms_fa | auto_mms_pause | 光陰の海原 | primary | 373 | 29 | 141 | 0 | 9 |
| demucs | mms_fa | auto_mms_pause | 恋のルチはや♡ローリング | primary | 402 | 0 | 0 | 402 | 0 |
| demucs | mms_fa | auto_mms_pause | 恋桜開花前線 | primary | 496 | 53 | 292 | 0 | 19 |
| demucs | mms_fa | auto_mms_pause | 白い季節 | primary | 427 | 51 | 156 | 0 | 20 |
| demucs | mms_fa | auto_mms_pause | 036 - リトルミラクル -Grip it tight- | primary | 431 | 0 | 0 | 431 | 0 |
| demucs | mms_fa | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | mms_fa | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | mms_fa | auto_mms_pause | 骹车破尼-假名注音 | teochew_kana | 449 | 164 | 337 | 0 | 4 |
| demucs | mms_fa | auto_nf | 003 - 撃槍・ガングニール | primary | 401 | 156 | 281 | 20 | 4 |
| demucs | mms_fa | auto_nf | POWDER SNOW (Live Ver.) | primary | 347 | 20 | 80 | 56 | 20 |
| demucs | mms_fa | auto_nf | Rainbow Flower | primary | 374 | 122 | 221 | 0 | 13 |
| demucs | mms_fa | auto_nf | TSU-BA-SA | primary | 359 | 110 | 240 | 0 | 8 |
| demucs | mms_fa | auto_nf | The Brave Under The Summer Sky | primary | 398 | 30 | 176 | 39 | 15 |
| demucs | mms_fa | auto_nf | Worlds Pain | primary | 507 | 148 | 282 | 0 | 8 |
| demucs | mms_fa | auto_nf | 両翼のBrilliance | primary | 506 | 206 | 316 | 0 | 12 |
| demucs | mms_fa | auto_nf | 光陰の海原 | primary | 373 | 31 | 137 | 16 | 10 |
| demucs | mms_fa | auto_nf | 恋のルチはや♡ローリング | primary | 402 | 113 | 231 | 0 | 5 |
| demucs | mms_fa | auto_nf | 恋桜開花前線 | primary | 496 | 50 | 279 | 21 | 18 |
| demucs | mms_fa | auto_nf | 白い季節 | primary | 427 | 50 | 153 | 18 | 21 |
| demucs | mms_fa | auto_nf | 036 - リトルミラクル -Grip it tight- | primary | 431 | 153 | 267 | 0 | 27 |
| demucs | mms_fa | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | mms_fa | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | mms_fa | auto_nf | 骹车破尼-假名注音 | teochew_kana | 449 | 165 | 320 | 24 | 5 |
| demucs | mms_fa | concat | 003 - 撃槍・ガングニール | primary | 401 | 163 | 291 | 0 | 4 |
| demucs | mms_fa | concat | POWDER SNOW (Live Ver.) | primary | 347 | 22 | 92 | 1 | 24 |
| demucs | mms_fa | concat | Rainbow Flower | primary | 374 | 132 | 224 | 0 | 22 |
| demucs | mms_fa | concat | TSU-BA-SA | primary | 359 | 116 | 234 | 0 | 7 |
| demucs | mms_fa | concat | The Brave Under The Summer Sky | primary | 398 | 26 | 189 | 0 | 17 |
| demucs | mms_fa | concat | Worlds Pain | primary | 507 | 145 | 294 | 0 | 8 |
| demucs | mms_fa | concat | 両翼のBrilliance | primary | 506 | 179 | 273 | 1 | 53 |
| demucs | mms_fa | concat | 光陰の海原 | primary | 373 | 29 | 142 | 0 | 10 |
| demucs | mms_fa | concat | 恋のルチはや♡ローリング | primary | 402 | 107 | 210 | 0 | 33 |
| demucs | mms_fa | concat | 恋桜開花前線 | primary | 496 | 52 | 287 | 0 | 20 |
| demucs | mms_fa | concat | 白い季節 | primary | 427 | 50 | 160 | 1 | 22 |
| demucs | mms_fa | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 155 | 259 | 0 | 30 |
| demucs | mms_fa | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | mms_fa | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | mms_fa | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 172 | 338 | 3 | 4 |
| demucs | mms_fa | full | 003 - 撃槍・ガングニール | primary | 401 | 161 | 292 | 0 | 5 |
| demucs | mms_fa | full | POWDER SNOW (Live Ver.) | primary | 347 | 22 | 97 | 0 | 27 |
| demucs | mms_fa | full | Rainbow Flower | primary | 374 | 129 | 208 | 0 | 19 |
| demucs | mms_fa | full | TSU-BA-SA | primary | 359 | 121 | 238 | 0 | 7 |
| demucs | mms_fa | full | The Brave Under The Summer Sky | primary | 398 | 28 | 186 | 0 | 16 |
| demucs | mms_fa | full | Worlds Pain | primary | 507 | 147 | 301 | 0 | 7 |
| demucs | mms_fa | full | 両翼のBrilliance | primary | 506 | 207 | 311 | 0 | 14 |
| demucs | mms_fa | full | 光陰の海原 | primary | 373 | 35 | 140 | 0 | 10 |
| demucs | mms_fa | full | 恋のルチはや♡ローリング | primary | 402 | 115 | 227 | 0 | 15 |
| demucs | mms_fa | full | 恋桜開花前線 | primary | 496 | 57 | 288 | 0 | 19 |
| demucs | mms_fa | full | 白い季節 | primary | 427 | 47 | 162 | 0 | 24 |
| demucs | mms_fa | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 167 | 279 | 0 | 25 |
| demucs | mms_fa | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | mms_fa | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | mms_fa | full | 骹车破尼-假名注音 | teochew_kana | 449 | 165 | 338 | 0 | 5 |
| demucs | mms_fa | human | 003 - 撃槍・ガングニール | primary | 401 | 163 | 297 | 0 | 4 |
| demucs | mms_fa | human | POWDER SNOW (Live Ver.) | primary | 347 | 21 | 92 | 0 | 27 |
| demucs | mms_fa | human | Rainbow Flower | primary | 374 | 122 | 228 | 0 | 10 |
| demucs | mms_fa | human | TSU-BA-SA | primary | 359 | 120 | 238 | 0 | 7 |
| demucs | mms_fa | human | The Brave Under The Summer Sky | primary | 398 | 31 | 196 | 0 | 18 |
| demucs | mms_fa | human | Worlds Pain | primary | 507 | 145 | 286 | 0 | 9 |
| demucs | mms_fa | human | 両翼のBrilliance | primary | 506 | 201 | 308 | 0 | 11 |
| demucs | mms_fa | human | 光陰の海原 | primary | 373 | 30 | 142 | 0 | 10 |
| demucs | mms_fa | human | 恋のルチはや♡ローリング | primary | 402 | 116 | 230 | 0 | 5 |
| demucs | mms_fa | human | 恋桜開花前線 | primary | 496 | 57 | 293 | 0 | 19 |
| demucs | mms_fa | human | 白い季節 | primary | 427 | 45 | 158 | 0 | 21 |
| demucs | mms_fa | human | 036 - リトルミラクル -Grip it tight- | primary | 431 | 160 | 269 | 0 | 26 |
| demucs | mms_fa | human | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 5 | 37 | 0 | 15 |
| demucs | mms_fa | human | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | mms_fa | human | 骹车破尼-假名注音 | teochew_kana | 449 | 165 | 333 | 0 | 3 |
| demucs | mms_fa | padded | 003 - 撃槍・ガングニール | primary | 401 | 156 | 289 | 0 | 5 |
| demucs | mms_fa | padded | POWDER SNOW (Live Ver.) | primary | 347 | 21 | 95 | 0 | 26 |
| demucs | mms_fa | padded | Rainbow Flower | primary | 374 | 128 | 216 | 0 | 23 |
| demucs | mms_fa | padded | TSU-BA-SA | primary | 359 | 107 | 235 | 0 | 7 |
| demucs | mms_fa | padded | The Brave Under The Summer Sky | primary | 398 | 28 | 188 | 0 | 18 |
| demucs | mms_fa | padded | Worlds Pain | primary | 507 | 147 | 298 | 1 | 11 |
| demucs | mms_fa | padded | 両翼のBrilliance | primary | 506 | 175 | 266 | 2 | 57 |
| demucs | mms_fa | padded | 光陰の海原 | primary | 373 | 31 | 139 | 0 | 10 |
| demucs | mms_fa | padded | 恋のルチはや♡ローリング | primary | 402 | 111 | 213 | 1 | 29 |
| demucs | mms_fa | padded | 恋桜開花前線 | primary | 496 | 55 | 286 | 0 | 19 |
| demucs | mms_fa | padded | 白い季節 | primary | 427 | 46 | 159 | 0 | 22 |
| demucs | mms_fa | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 164 | 275 | 0 | 29 |
| demucs | mms_fa | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | mms_fa | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | mms_fa | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 176 | 337 | 1 | 5 |
| demucs | nextfire | auto_mms | 003 - 撃槍・ガングニール | primary | 401 | 345 | 371 | 0 | 5 |
| demucs | nextfire | auto_mms | POWDER SNOW (Live Ver.) | primary | 347 | 252 | 293 | 0 | 15 |
| demucs | nextfire | auto_mms | Rainbow Flower | primary | 374 | 217 | 297 | 0 | 18 |
| demucs | nextfire | auto_mms | TSU-BA-SA | primary | 359 | 282 | 336 | 0 | 3 |
| demucs | nextfire | auto_mms | The Brave Under The Summer Sky | primary | 398 | 265 | 346 | 0 | 10 |
| demucs | nextfire | auto_mms | Worlds Pain | primary | 507 | 415 | 456 | 0 | 8 |
| demucs | nextfire | auto_mms | 両翼のBrilliance | primary | 506 | 0 | 0 | 506 | 0 |
| demucs | nextfire | auto_mms | 光陰の海原 | primary | 373 | 240 | 318 | 0 | 4 |
| demucs | nextfire | auto_mms | 恋のルチはや♡ローリング | primary | 402 | 0 | 0 | 402 | 0 |
| demucs | nextfire | auto_mms | 恋桜開花前線 | primary | 496 | 403 | 459 | 0 | 13 |
| demucs | nextfire | auto_mms | 白い季節 | primary | 427 | 328 | 363 | 0 | 12 |
| demucs | nextfire | auto_mms | 036 - リトルミラクル -Grip it tight- | primary | 431 | 0 | 0 | 431 | 0 |
| demucs | nextfire | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | nextfire | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | nextfire | auto_mms | 骹车破尼-假名注音 | teochew_kana | 449 | 248 | 351 | 0 | 4 |
| demucs | nextfire | auto_mms_pause | 003 - 撃槍・ガングニール | primary | 401 | 341 | 367 | 0 | 2 |
| demucs | nextfire | auto_mms_pause | POWDER SNOW (Live Ver.) | primary | 347 | 262 | 307 | 0 | 5 |
| demucs | nextfire | auto_mms_pause | Rainbow Flower | primary | 374 | 239 | 296 | 0 | 25 |
| demucs | nextfire | auto_mms_pause | TSU-BA-SA | primary | 359 | 273 | 331 | 0 | 2 |
| demucs | nextfire | auto_mms_pause | The Brave Under The Summer Sky | primary | 398 | 261 | 346 | 0 | 5 |
| demucs | nextfire | auto_mms_pause | Worlds Pain | primary | 507 | 423 | 462 | 0 | 7 |
| demucs | nextfire | auto_mms_pause | 両翼のBrilliance | primary | 506 | 0 | 0 | 506 | 0 |
| demucs | nextfire | auto_mms_pause | 光陰の海原 | primary | 373 | 269 | 338 | 0 | 1 |
| demucs | nextfire | auto_mms_pause | 恋のルチはや♡ローリング | primary | 402 | 0 | 0 | 402 | 0 |
| demucs | nextfire | auto_mms_pause | 恋桜開花前線 | primary | 496 | 418 | 465 | 0 | 3 |
| demucs | nextfire | auto_mms_pause | 白い季節 | primary | 427 | 371 | 400 | 0 | 3 |
| demucs | nextfire | auto_mms_pause | 036 - リトルミラクル -Grip it tight- | primary | 431 | 0 | 0 | 431 | 0 |
| demucs | nextfire | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | nextfire | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | nextfire | auto_mms_pause | 骹车破尼-假名注音 | teochew_kana | 449 | 248 | 346 | 0 | 3 |
| demucs | nextfire | auto_nf | 003 - 撃槍・ガングニール | primary | 401 | 337 | 366 | 20 | 0 |
| demucs | nextfire | auto_nf | POWDER SNOW (Live Ver.) | primary | 347 | 228 | 258 | 56 | 4 |
| demucs | nextfire | auto_nf | Rainbow Flower | primary | 374 | 210 | 299 | 0 | 14 |
| demucs | nextfire | auto_nf | TSU-BA-SA | primary | 359 | 289 | 347 | 0 | 3 |
| demucs | nextfire | auto_nf | The Brave Under The Summer Sky | primary | 398 | 239 | 315 | 39 | 2 |
| demucs | nextfire | auto_nf | Worlds Pain | primary | 507 | 437 | 490 | 0 | 0 |
| demucs | nextfire | auto_nf | 両翼のBrilliance | primary | 506 | 335 | 417 | 0 | 22 |
| demucs | nextfire | auto_nf | 光陰の海原 | primary | 373 | 268 | 330 | 16 | 0 |
| demucs | nextfire | auto_nf | 恋のルチはや♡ローリング | primary | 402 | 342 | 375 | 0 | 0 |
| demucs | nextfire | auto_nf | 恋桜開花前線 | primary | 496 | 415 | 461 | 21 | 1 |
| demucs | nextfire | auto_nf | 白い季節 | primary | 427 | 352 | 388 | 18 | 0 |
| demucs | nextfire | auto_nf | 036 - リトルミラクル -Grip it tight- | primary | 431 | 287 | 376 | 0 | 15 |
| demucs | nextfire | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | nextfire | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | nextfire | auto_nf | 骹车破尼-假名注音 | teochew_kana | 449 | 230 | 333 | 24 | 11 |
| demucs | nextfire | concat | 003 - 撃槍・ガングニール | primary | 401 | 340 | 372 | 5 | 0 |
| demucs | nextfire | concat | POWDER SNOW (Live Ver.) | primary | 347 | 276 | 307 | 11 | 1 |
| demucs | nextfire | concat | Rainbow Flower | primary | 374 | 260 | 303 | 0 | 16 |
| demucs | nextfire | concat | TSU-BA-SA | primary | 359 | 311 | 346 | 0 | 3 |
| demucs | nextfire | concat | The Brave Under The Summer Sky | primary | 398 | 319 | 377 | 6 | 0 |
| demucs | nextfire | concat | Worlds Pain | primary | 507 | 459 | 494 | 2 | 0 |
| demucs | nextfire | concat | 両翼のBrilliance | primary | 506 | 405 | 455 | 1 | 15 |
| demucs | nextfire | concat | 光陰の海原 | primary | 373 | 283 | 351 | 1 | 0 |
| demucs | nextfire | concat | 恋のルチはや♡ローリング | primary | 402 | 361 | 396 | 0 | 0 |
| demucs | nextfire | concat | 恋桜開花前線 | primary | 496 | 463 | 485 | 2 | 1 |
| demucs | nextfire | concat | 白い季節 | primary | 427 | 396 | 406 | 5 | 0 |
| demucs | nextfire | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 350 | 395 | 0 | 7 |
| demucs | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | nextfire | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 335 | 382 | 4 | 9 |
| demucs | nextfire | full | 003 - 撃槍・ガングニール | primary | 401 | 320 | 376 | 0 | 0 |
| demucs | nextfire | full | POWDER SNOW (Live Ver.) | primary | 347 | 257 | 315 | 0 | 1 |
| demucs | nextfire | full | Rainbow Flower | primary | 374 | 226 | 311 | 0 | 13 |
| demucs | nextfire | full | TSU-BA-SA | primary | 359 | 282 | 346 | 0 | 3 |
| demucs | nextfire | full | The Brave Under The Summer Sky | primary | 398 | 271 | 370 | 0 | 2 |
| demucs | nextfire | full | Worlds Pain | primary | 507 | 400 | 486 | 0 | 0 |
| demucs | nextfire | full | 両翼のBrilliance | primary | 506 | 386 | 440 | 0 | 30 |
| demucs | nextfire | full | 光陰の海原 | primary | 373 | 233 | 334 | 0 | 4 |
| demucs | nextfire | full | 恋のルチはや♡ローリング | primary | 402 | 312 | 389 | 0 | 0 |
| demucs | nextfire | full | 恋桜開花前線 | primary | 496 | 412 | 488 | 0 | 2 |
| demucs | nextfire | full | 白い季節 | primary | 427 | 366 | 398 | 0 | 0 |
| demucs | nextfire | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 286 | 378 | 0 | 5 |
| demucs | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | nextfire | full | 骹车破尼-假名注音 | teochew_kana | 449 | 266 | 346 | 0 | 15 |
| demucs | nextfire | human | 003 - 撃槍・ガングニール | primary | 401 | 355 | 384 | 0 | 0 |
| demucs | nextfire | human | POWDER SNOW (Live Ver.) | primary | 347 | 283 | 319 | 0 | 2 |
| demucs | nextfire | human | Rainbow Flower | primary | 374 | 254 | 315 | 0 | 0 |
| demucs | nextfire | human | TSU-BA-SA | primary | 359 | 294 | 344 | 0 | 0 |
| demucs | nextfire | human | The Brave Under The Summer Sky | primary | 398 | 278 | 364 | 0 | 4 |
| demucs | nextfire | human | Worlds Pain | primary | 507 | 451 | 487 | 0 | 0 |
| demucs | nextfire | human | 両翼のBrilliance | primary | 506 | 362 | 447 | 0 | 13 |
| demucs | nextfire | human | 光陰の海原 | primary | 373 | 273 | 346 | 0 | 0 |
| demucs | nextfire | human | 恋のルチはや♡ローリング | primary | 402 | 341 | 388 | 0 | 0 |
| demucs | nextfire | human | 恋桜開花前線 | primary | 496 | 439 | 482 | 0 | 1 |
| demucs | nextfire | human | 白い季節 | primary | 427 | 374 | 400 | 0 | 0 |
| demucs | nextfire | human | 036 - リトルミラクル -Grip it tight- | primary | 431 | 312 | 382 | 0 | 5 |
| demucs | nextfire | human | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 66 | 95 | 0 | 0 |
| demucs | nextfire | human | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | nextfire | human | 骹车破尼-假名注音 | teochew_kana | 449 | 257 | 353 | 0 | 1 |
| demucs | nextfire | padded | 003 - 撃槍・ガングニール | primary | 401 | 345 | 378 | 1 | 0 |
| demucs | nextfire | padded | POWDER SNOW (Live Ver.) | primary | 347 | 267 | 315 | 1 | 1 |
| demucs | nextfire | padded | Rainbow Flower | primary | 374 | 261 | 312 | 0 | 13 |
| demucs | nextfire | padded | TSU-BA-SA | primary | 359 | 314 | 350 | 0 | 3 |
| demucs | nextfire | padded | The Brave Under The Summer Sky | primary | 398 | 319 | 377 | 1 | 0 |
| demucs | nextfire | padded | Worlds Pain | primary | 507 | 450 | 490 | 0 | 0 |
| demucs | nextfire | padded | 両翼のBrilliance | primary | 506 | 406 | 455 | 1 | 13 |
| demucs | nextfire | padded | 光陰の海原 | primary | 373 | 265 | 338 | 0 | 0 |
| demucs | nextfire | padded | 恋のルチはや♡ローリング | primary | 402 | 374 | 398 | 0 | 0 |
| demucs | nextfire | padded | 恋桜開花前線 | primary | 496 | 464 | 489 | 0 | 1 |
| demucs | nextfire | padded | 白い季節 | primary | 427 | 372 | 409 | 1 | 0 |
| demucs | nextfire | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 339 | 381 | 1 | 10 |
| demucs | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | nextfire | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 271 | 337 | 3 | 15 |
| demucs | tifa | auto_mms | 003 - 撃槍・ガングニール | primary | 401 | 368 | 388 | 0 | 4 |
| demucs | tifa | auto_mms | POWDER SNOW (Live Ver.) | primary | 347 | 250 | 287 | 0 | 16 |
| demucs | tifa | auto_mms | Rainbow Flower | primary | 374 | 321 | 347 | 0 | 3 |
| demucs | tifa | auto_mms | TSU-BA-SA | primary | 359 | 316 | 343 | 0 | 3 |
| demucs | tifa | auto_mms | The Brave Under The Summer Sky | primary | 398 | 230 | 364 | 0 | 6 |
| demucs | tifa | auto_mms | Worlds Pain | primary | 507 | 431 | 478 | 0 | 5 |
| demucs | tifa | auto_mms | 両翼のBrilliance | primary | 506 | 0 | 0 | 506 | 0 |
| demucs | tifa | auto_mms | 光陰の海原 | primary | 373 | 231 | 324 | 0 | 6 |
| demucs | tifa | auto_mms | 恋のルチはや♡ローリング | primary | 402 | 0 | 0 | 402 | 0 |
| demucs | tifa | auto_mms | 恋桜開花前線 | primary | 496 | 370 | 462 | 0 | 13 |
| demucs | tifa | auto_mms | 白い季節 | primary | 427 | 323 | 363 | 0 | 11 |
| demucs | tifa | auto_mms | 036 - リトルミラクル -Grip it tight- | primary | 431 | 0 | 0 | 431 | 0 |
| demucs | tifa | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | tifa | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | tifa | auto_mms | 骹车破尼-假名注音 | teochew_kana | 449 | 294 | 405 | 0 | 5 |
| demucs | tifa | auto_mms_pause | 003 - 撃槍・ガングニール | primary | 401 | 368 | 387 | 0 | 1 |
| demucs | tifa | auto_mms_pause | POWDER SNOW (Live Ver.) | primary | 347 | 267 | 310 | 0 | 6 |
| demucs | tifa | auto_mms_pause | Rainbow Flower | primary | 374 | 322 | 347 | 0 | 4 |
| demucs | tifa | auto_mms_pause | TSU-BA-SA | primary | 359 | 312 | 337 | 0 | 0 |
| demucs | tifa | auto_mms_pause | The Brave Under The Summer Sky | primary | 398 | 236 | 361 | 0 | 1 |
| demucs | tifa | auto_mms_pause | Worlds Pain | primary | 507 | 437 | 486 | 0 | 3 |
| demucs | tifa | auto_mms_pause | 両翼のBrilliance | primary | 506 | 0 | 0 | 506 | 0 |
| demucs | tifa | auto_mms_pause | 光陰の海原 | primary | 373 | 236 | 337 | 0 | 5 |
| demucs | tifa | auto_mms_pause | 恋のルチはや♡ローリング | primary | 402 | 0 | 0 | 402 | 0 |
| demucs | tifa | auto_mms_pause | 恋桜開花前線 | primary | 496 | 368 | 464 | 0 | 10 |
| demucs | tifa | auto_mms_pause | 白い季節 | primary | 427 | 338 | 389 | 0 | 5 |
| demucs | tifa | auto_mms_pause | 036 - リトルミラクル -Grip it tight- | primary | 431 | 0 | 0 | 431 | 0 |
| demucs | tifa | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | tifa | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | tifa | auto_mms_pause | 骹车破尼-假名注音 | teochew_kana | 449 | 287 | 402 | 0 | 4 |
| demucs | tifa | auto_nf | 003 - 撃槍・ガングニール | primary | 401 | 353 | 372 | 20 | 0 |
| demucs | tifa | auto_nf | POWDER SNOW (Live Ver.) | primary | 347 | 232 | 261 | 56 | 2 |
| demucs | tifa | auto_nf | Rainbow Flower | primary | 374 | 324 | 351 | 0 | 5 |
| demucs | tifa | auto_nf | TSU-BA-SA | primary | 359 | 317 | 348 | 0 | 1 |
| demucs | tifa | auto_nf | The Brave Under The Summer Sky | primary | 398 | 219 | 328 | 39 | 0 |
| demucs | tifa | auto_nf | Worlds Pain | primary | 507 | 456 | 496 | 0 | 0 |
| demucs | tifa | auto_nf | 両翼のBrilliance | primary | 506 | 413 | 470 | 0 | 14 |
| demucs | tifa | auto_nf | 光陰の海原 | primary | 373 | 228 | 321 | 16 | 4 |
| demucs | tifa | auto_nf | 恋のルチはや♡ローリング | primary | 402 | 347 | 383 | 0 | 2 |
| demucs | tifa | auto_nf | 恋桜開花前線 | primary | 496 | 381 | 461 | 21 | 1 |
| demucs | tifa | auto_nf | 白い季節 | primary | 427 | 329 | 375 | 18 | 1 |
| demucs | tifa | auto_nf | 036 - リトルミラクル -Grip it tight- | primary | 431 | 358 | 398 | 0 | 9 |
| demucs | tifa | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| demucs | tifa | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| demucs | tifa | auto_nf | 骹车破尼-假名注音 | teochew_kana | 449 | 281 | 385 | 24 | 6 |
| demucs | tifa | concat | 003 - 撃槍・ガングニール | primary | 401 | 150 | 161 | 24 | 199 |
| demucs | tifa | concat | POWDER SNOW (Live Ver.) | primary | 347 | 164 | 188 | 11 | 108 |
| demucs | tifa | concat | Rainbow Flower | primary | 374 | 148 | 170 | 18 | 153 |
| demucs | tifa | concat | TSU-BA-SA | primary | 359 | 264 | 315 | 0 | 5 |
| demucs | tifa | concat | The Brave Under The Summer Sky | primary | 398 | 122 | 218 | 21 | 125 |
| demucs | tifa | concat | Worlds Pain | primary | 507 | 269 | 322 | 15 | 132 |
| demucs | tifa | concat | 両翼のBrilliance | primary | 506 | 166 | 210 | 65 | 201 |
| demucs | tifa | concat | 光陰の海原 | primary | 373 | 126 | 192 | 46 | 115 |
| demucs | tifa | concat | 恋のルチはや♡ローリング | primary | 402 | 237 | 271 | 18 | 76 |
| demucs | tifa | concat | 恋桜開花前線 | primary | 496 | 215 | 289 | 27 | 136 |
| demucs | tifa | concat | 白い季節 | primary | 427 | 189 | 221 | 20 | 134 |
| demucs | tifa | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 124 | 148 | 37 | 229 |
| demucs | tifa | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 42 | 62 | 2 | 13 |
| demucs | tifa | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 22 | 36 | 51 | 57 |
| demucs | tifa | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 260 | 363 | 24 | 3 |
| demucs | tifa | full | 003 - 撃槍・ガングニール | primary | 401 | 241 | 260 | 3 | 88 |
| demucs | tifa | full | POWDER SNOW (Live Ver.) | primary | 347 | 1 | 3 | 80 | 255 |
| demucs | tifa | full | Rainbow Flower | primary | 374 | 181 | 213 | 1 | 121 |
| demucs | tifa | full | TSU-BA-SA | primary | 359 | 228 | 264 | 4 | 76 |
| demucs | tifa | full | The Brave Under The Summer Sky | primary | 398 | 96 | 182 | 28 | 141 |
| demucs | tifa | full | Worlds Pain | primary | 507 | 214 | 254 | 17 | 192 |
| demucs | tifa | full | 両翼のBrilliance | primary | 506 | 154 | 196 | 1 | 263 |
| demucs | tifa | full | 光陰の海原 | primary | 373 | 105 | 163 | 12 | 139 |
| demucs | tifa | full | 恋のルチはや♡ローリング | primary | 402 | 229 | 266 | 4 | 102 |
| demucs | tifa | full | 恋桜開花前線 | primary | 496 | 182 | 245 | 17 | 202 |
| demucs | tifa | full | 白い季節 | primary | 427 | 131 | 163 | 12 | 197 |
| demucs | tifa | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 172 | 194 | 8 | 204 |
| demucs | tifa | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 44 | 60 | 0 | 22 |
| demucs | tifa | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 14 | 26 | 2 | 105 |
| demucs | tifa | full | 骹车破尼-假名注音 | teochew_kana | 449 | 198 | 284 | 3 | 93 |
| demucs | tifa | human | 003 - 撃槍・ガングニール | primary | 401 | 375 | 395 | 0 | 0 |
| demucs | tifa | human | POWDER SNOW (Live Ver.) | primary | 347 | 278 | 320 | 0 | 1 |
| demucs | tifa | human | Rainbow Flower | primary | 374 | 340 | 363 | 0 | 0 |
| demucs | tifa | human | TSU-BA-SA | primary | 359 | 323 | 351 | 0 | 0 |
| demucs | tifa | human | The Brave Under The Summer Sky | primary | 398 | 251 | 372 | 0 | 0 |
| demucs | tifa | human | Worlds Pain | primary | 507 | 456 | 500 | 0 | 0 |
| demucs | tifa | human | 両翼のBrilliance | primary | 506 | 435 | 485 | 0 | 2 |
| demucs | tifa | human | 光陰の海原 | primary | 373 | 240 | 340 | 0 | 4 |
| demucs | tifa | human | 恋のルチはや♡ローリング | primary | 402 | 350 | 390 | 0 | 2 |
| demucs | tifa | human | 恋桜開花前線 | primary | 496 | 407 | 484 | 0 | 1 |
| demucs | tifa | human | 白い季節 | primary | 427 | 354 | 397 | 0 | 1 |
| demucs | tifa | human | 036 - リトルミラクル -Grip it tight- | primary | 431 | 377 | 410 | 0 | 4 |
| demucs | tifa | human | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 69 | 102 | 0 | 0 |
| demucs | tifa | human | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 103 | 142 | 0 | 0 |
| demucs | tifa | human | 骹车破尼-假名注音 | teochew_kana | 449 | 340 | 419 | 0 | 0 |
| demucs | tifa | padded | 003 - 撃槍・ガングニール | primary | 401 | 176 | 195 | 34 | 162 |
| demucs | tifa | padded | POWDER SNOW (Live Ver.) | primary | 347 | 158 | 182 | 2 | 125 |
| demucs | tifa | padded | Rainbow Flower | primary | 374 | 147 | 168 | 19 | 152 |
| demucs | tifa | padded | TSU-BA-SA | primary | 359 | 260 | 308 | 1 | 10 |
| demucs | tifa | padded | The Brave Under The Summer Sky | primary | 398 | 123 | 217 | 20 | 125 |
| demucs | tifa | padded | Worlds Pain | primary | 507 | 259 | 300 | 15 | 149 |
| demucs | tifa | padded | 両翼のBrilliance | primary | 506 | 170 | 212 | 65 | 207 |
| demucs | tifa | padded | 光陰の海原 | primary | 373 | 132 | 194 | 52 | 102 |
| demucs | tifa | padded | 恋のルチはや♡ローリング | primary | 402 | 244 | 274 | 8 | 82 |
| demucs | tifa | padded | 恋桜開花前線 | primary | 496 | 226 | 312 | 1 | 128 |
| demucs | tifa | padded | 白い季節 | primary | 427 | 179 | 219 | 5 | 145 |
| demucs | tifa | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 129 | 147 | 34 | 222 |
| demucs | tifa | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 46 | 65 | 1 | 12 |
| demucs | tifa | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 22 | 36 | 32 | 75 |
| demucs | tifa | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 259 | 368 | 2 | 3 |
| dttnet | nextfire | concat | 003 - 撃槍・ガングニール | primary | 401 | 349 | 382 | 2 | 0 |
| dttnet | nextfire | concat | POWDER SNOW (Live Ver.) | primary | 347 | 285 | 316 | 0 | 1 |
| dttnet | nextfire | concat | Rainbow Flower | primary | 374 | 273 | 306 | 0 | 13 |
| dttnet | nextfire | concat | TSU-BA-SA | primary | 359 | 322 | 349 | 0 | 4 |
| dttnet | nextfire | concat | The Brave Under The Summer Sky | primary | 398 | 340 | 379 | 4 | 2 |
| dttnet | nextfire | concat | Worlds Pain | primary | 507 | 457 | 490 | 1 | 0 |
| dttnet | nextfire | concat | 両翼のBrilliance | primary | 506 | 411 | 461 | 0 | 11 |
| dttnet | nextfire | concat | 光陰の海原 | primary | 373 | 273 | 351 | 1 | 0 |
| dttnet | nextfire | concat | 恋のルチはや♡ローリング | primary | 402 | 372 | 399 | 0 | 0 |
| dttnet | nextfire | concat | 恋桜開花前線 | primary | 496 | 460 | 490 | 0 | 0 |
| dttnet | nextfire | concat | 白い季節 | primary | 427 | 363 | 407 | 0 | 0 |
| dttnet | nextfire | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 324 | 364 | 1 | 21 |
| dttnet | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| dttnet | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| dttnet | nextfire | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 285 | 360 | 4 | 16 |
| dttnet | nextfire | full | 003 - 撃槍・ガングニール | primary | 401 | 330 | 372 | 0 | 0 |
| dttnet | nextfire | full | POWDER SNOW (Live Ver.) | primary | 347 | 259 | 316 | 0 | 1 |
| dttnet | nextfire | full | Rainbow Flower | primary | 374 | 241 | 304 | 0 | 12 |
| dttnet | nextfire | full | TSU-BA-SA | primary | 359 | 295 | 349 | 0 | 3 |
| dttnet | nextfire | full | The Brave Under The Summer Sky | primary | 398 | 311 | 373 | 0 | 1 |
| dttnet | nextfire | full | Worlds Pain | primary | 507 | 431 | 486 | 0 | 0 |
| dttnet | nextfire | full | 両翼のBrilliance | primary | 506 | 409 | 456 | 0 | 19 |
| dttnet | nextfire | full | 光陰の海原 | primary | 373 | 240 | 340 | 0 | 4 |
| dttnet | nextfire | full | 恋のルチはや♡ローリング | primary | 402 | 339 | 397 | 0 | 0 |
| dttnet | nextfire | full | 恋桜開花前線 | primary | 496 | 415 | 485 | 0 | 0 |
| dttnet | nextfire | full | 白い季節 | primary | 427 | 375 | 400 | 0 | 3 |
| dttnet | nextfire | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 309 | 364 | 0 | 19 |
| dttnet | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| dttnet | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| dttnet | nextfire | full | 骹车破尼-假名注音 | teochew_kana | 449 | 262 | 348 | 0 | 13 |
| dttnet | nextfire | padded | 003 - 撃槍・ガングニール | primary | 401 | 354 | 386 | 1 | 0 |
| dttnet | nextfire | padded | POWDER SNOW (Live Ver.) | primary | 347 | 271 | 316 | 0 | 1 |
| dttnet | nextfire | padded | Rainbow Flower | primary | 374 | 267 | 307 | 0 | 9 |
| dttnet | nextfire | padded | TSU-BA-SA | primary | 359 | 323 | 349 | 0 | 3 |
| dttnet | nextfire | padded | The Brave Under The Summer Sky | primary | 398 | 330 | 379 | 0 | 1 |
| dttnet | nextfire | padded | Worlds Pain | primary | 507 | 455 | 493 | 0 | 0 |
| dttnet | nextfire | padded | 両翼のBrilliance | primary | 506 | 414 | 465 | 0 | 10 |
| dttnet | nextfire | padded | 光陰の海原 | primary | 373 | 254 | 339 | 0 | 14 |
| dttnet | nextfire | padded | 恋のルチはや♡ローリング | primary | 402 | 377 | 399 | 0 | 0 |
| dttnet | nextfire | padded | 恋桜開花前線 | primary | 496 | 459 | 489 | 0 | 0 |
| dttnet | nextfire | padded | 白い季節 | primary | 427 | 379 | 407 | 0 | 0 |
| dttnet | nextfire | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 342 | 374 | 0 | 23 |
| dttnet | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| dttnet | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| dttnet | nextfire | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 249 | 352 | 2 | 19 |
| kim | mms_fa | auto_mms | 003 - 撃槍・ガングニール | primary | 401 | 157 | 288 | 0 | 4 |
| kim | mms_fa | auto_mms | POWDER SNOW (Live Ver.) | primary | 347 | 21 | 88 | 0 | 26 |
| kim | mms_fa | auto_mms | Rainbow Flower | primary | 374 | 129 | 230 | 0 | 11 |
| kim | mms_fa | auto_mms | TSU-BA-SA | primary | 359 | 124 | 240 | 0 | 7 |
| kim | mms_fa | auto_mms | The Brave Under The Summer Sky | primary | 398 | 29 | 187 | 0 | 17 |
| kim | mms_fa | auto_mms | Worlds Pain | primary | 507 | 144 | 291 | 0 | 7 |
| kim | mms_fa | auto_mms | 両翼のBrilliance | primary | 506 | 0 | 0 | 506 | 0 |
| kim | mms_fa | auto_mms | 光陰の海原 | primary | 373 | 33 | 144 | 0 | 10 |
| kim | mms_fa | auto_mms | 恋のルチはや♡ローリング | primary | 402 | 114 | 223 | 0 | 5 |
| kim | mms_fa | auto_mms | 恋桜開花前線 | primary | 496 | 51 | 292 | 0 | 19 |
| kim | mms_fa | auto_mms | 白い季節 | primary | 427 | 46 | 153 | 0 | 24 |
| kim | mms_fa | auto_mms | 036 - リトルミラクル -Grip it tight- | primary | 431 | 164 | 274 | 0 | 26 |
| kim | mms_fa | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | mms_fa | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | mms_fa | auto_mms | 骹车破尼-假名注音 | teochew_kana | 449 | 163 | 335 | 0 | 3 |
| kim | mms_fa | auto_mms_pause | 003 - 撃槍・ガングニール | primary | 401 | 154 | 291 | 0 | 4 |
| kim | mms_fa | auto_mms_pause | POWDER SNOW (Live Ver.) | primary | 347 | 21 | 90 | 0 | 26 |
| kim | mms_fa | auto_mms_pause | Rainbow Flower | primary | 374 | 128 | 229 | 0 | 13 |
| kim | mms_fa | auto_mms_pause | TSU-BA-SA | primary | 359 | 122 | 242 | 0 | 7 |
| kim | mms_fa | auto_mms_pause | The Brave Under The Summer Sky | primary | 398 | 28 | 186 | 0 | 20 |
| kim | mms_fa | auto_mms_pause | Worlds Pain | primary | 507 | 139 | 287 | 0 | 7 |
| kim | mms_fa | auto_mms_pause | 両翼のBrilliance | primary | 506 | 0 | 0 | 506 | 0 |
| kim | mms_fa | auto_mms_pause | 光陰の海原 | primary | 373 | 36 | 147 | 0 | 10 |
| kim | mms_fa | auto_mms_pause | 恋のルチはや♡ローリング | primary | 402 | 115 | 226 | 0 | 6 |
| kim | mms_fa | auto_mms_pause | 恋桜開花前線 | primary | 496 | 54 | 291 | 0 | 20 |
| kim | mms_fa | auto_mms_pause | 白い季節 | primary | 427 | 45 | 155 | 0 | 23 |
| kim | mms_fa | auto_mms_pause | 036 - リトルミラクル -Grip it tight- | primary | 431 | 166 | 280 | 0 | 26 |
| kim | mms_fa | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | mms_fa | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | mms_fa | auto_mms_pause | 骹车破尼-假名注音 | teochew_kana | 449 | 165 | 334 | 0 | 3 |
| kim | mms_fa | auto_nf | 003 - 撃槍・ガングニール | primary | 401 | 161 | 289 | 0 | 4 |
| kim | mms_fa | auto_nf | POWDER SNOW (Live Ver.) | primary | 347 | 22 | 93 | 10 | 26 |
| kim | mms_fa | auto_nf | Rainbow Flower | primary | 374 | 133 | 234 | 12 | 12 |
| kim | mms_fa | auto_nf | TSU-BA-SA | primary | 359 | 124 | 241 | 0 | 8 |
| kim | mms_fa | auto_nf | The Brave Under The Summer Sky | primary | 398 | 26 | 178 | 23 | 16 |
| kim | mms_fa | auto_nf | Worlds Pain | primary | 507 | 142 | 290 | 0 | 8 |
| kim | mms_fa | auto_nf | 両翼のBrilliance | primary | 506 | 207 | 322 | 0 | 9 |
| kim | mms_fa | auto_nf | 光陰の海原 | primary | 373 | 31 | 138 | 16 | 10 |
| kim | mms_fa | auto_nf | 恋のルチはや♡ローリング | primary | 402 | 102 | 226 | 0 | 5 |
| kim | mms_fa | auto_nf | 恋桜開花前線 | primary | 496 | 60 | 289 | 0 | 19 |
| kim | mms_fa | auto_nf | 白い季節 | primary | 427 | 44 | 151 | 8 | 21 |
| kim | mms_fa | auto_nf | 036 - リトルミラクル -Grip it tight- | primary | 431 | 154 | 269 | 0 | 31 |
| kim | mms_fa | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | mms_fa | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | mms_fa | auto_nf | 骹车破尼-假名注音 | teochew_kana | 449 | 163 | 326 | 0 | 4 |
| kim | mms_fa | concat | 003 - 撃槍・ガングニール | primary | 401 | 164 | 293 | 0 | 4 |
| kim | mms_fa | concat | POWDER SNOW (Live Ver.) | primary | 347 | 22 | 91 | 0 | 26 |
| kim | mms_fa | concat | Rainbow Flower | primary | 374 | 139 | 244 | 0 | 11 |
| kim | mms_fa | concat | TSU-BA-SA | primary | 359 | 121 | 235 | 0 | 7 |
| kim | mms_fa | concat | The Brave Under The Summer Sky | primary | 398 | 26 | 186 | 0 | 17 |
| kim | mms_fa | concat | Worlds Pain | primary | 507 | 144 | 283 | 0 | 8 |
| kim | mms_fa | concat | 両翼のBrilliance | primary | 506 | 187 | 289 | 1 | 42 |
| kim | mms_fa | concat | 光陰の海原 | primary | 373 | 30 | 138 | 1 | 10 |
| kim | mms_fa | concat | 恋のルチはや♡ローリング | primary | 402 | 98 | 213 | 0 | 35 |
| kim | mms_fa | concat | 恋桜開花前線 | primary | 496 | 61 | 288 | 0 | 20 |
| kim | mms_fa | concat | 白い季節 | primary | 427 | 47 | 156 | 0 | 21 |
| kim | mms_fa | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 158 | 261 | 0 | 27 |
| kim | mms_fa | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | mms_fa | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | mms_fa | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 169 | 331 | 1 | 3 |
| kim | mms_fa | fixed_cores | 003 - 撃槍・ガングニール | primary | 401 | 160 | 295 | 0 | 4 |
| kim | mms_fa | fixed_cores | POWDER SNOW (Live Ver.) | primary | 347 | 21 | 89 | 0 | 26 |
| kim | mms_fa | fixed_cores | Rainbow Flower | primary | 374 | 125 | 222 | 0 | 20 |
| kim | mms_fa | fixed_cores | TSU-BA-SA | primary | 359 | 116 | 232 | 0 | 7 |
| kim | mms_fa | fixed_cores | The Brave Under The Summer Sky | primary | 398 | 27 | 191 | 0 | 17 |
| kim | mms_fa | fixed_cores | Worlds Pain | primary | 507 | 144 | 282 | 0 | 7 |
| kim | mms_fa | fixed_cores | 両翼のBrilliance | primary | 506 | 192 | 292 | 0 | 44 |
| kim | mms_fa | fixed_cores | 光陰の海原 | primary | 373 | 32 | 140 | 0 | 10 |
| kim | mms_fa | fixed_cores | 恋のルチはや♡ローリング | primary | 402 | 105 | 215 | 1 | 14 |
| kim | mms_fa | fixed_cores | 恋桜開花前線 | primary | 496 | 48 | 284 | 0 | 20 |
| kim | mms_fa | fixed_cores | 白い季節 | primary | 427 | 48 | 160 | 1 | 23 |
| kim | mms_fa | fixed_cores | 036 - リトルミラクル -Grip it tight- | primary | 431 | 160 | 258 | 1 | 29 |
| kim | mms_fa | fixed_cores | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | mms_fa | fixed_cores | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | mms_fa | fixed_cores | 骹车破尼-假名注音 | teochew_kana | 449 | 175 | 335 | 2 | 4 |
| kim | mms_fa | full | 003 - 撃槍・ガングニール | primary | 401 | 160 | 290 | 0 | 5 |
| kim | mms_fa | full | POWDER SNOW (Live Ver.) | primary | 347 | 21 | 94 | 0 | 26 |
| kim | mms_fa | full | Rainbow Flower | primary | 374 | 128 | 223 | 0 | 11 |
| kim | mms_fa | full | TSU-BA-SA | primary | 359 | 119 | 232 | 0 | 6 |
| kim | mms_fa | full | The Brave Under The Summer Sky | primary | 398 | 29 | 185 | 0 | 17 |
| kim | mms_fa | full | Worlds Pain | primary | 507 | 140 | 296 | 0 | 7 |
| kim | mms_fa | full | 両翼のBrilliance | primary | 506 | 207 | 318 | 0 | 13 |
| kim | mms_fa | full | 光陰の海原 | primary | 373 | 32 | 139 | 0 | 10 |
| kim | mms_fa | full | 恋のルチはや♡ローリング | primary | 402 | 119 | 224 | 0 | 15 |
| kim | mms_fa | full | 恋桜開花前線 | primary | 496 | 57 | 288 | 0 | 20 |
| kim | mms_fa | full | 白い季節 | primary | 427 | 47 | 158 | 0 | 24 |
| kim | mms_fa | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 170 | 280 | 0 | 24 |
| kim | mms_fa | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | mms_fa | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | mms_fa | full | 骹车破尼-假名注音 | teochew_kana | 449 | 174 | 336 | 0 | 4 |
| kim | mms_fa | human | 003 - 撃槍・ガングニール | primary | 401 | 153 | 291 | 0 | 4 |
| kim | mms_fa | human | POWDER SNOW (Live Ver.) | primary | 347 | 19 | 90 | 0 | 26 |
| kim | mms_fa | human | Rainbow Flower | primary | 374 | 132 | 234 | 0 | 10 |
| kim | mms_fa | human | TSU-BA-SA | primary | 359 | 123 | 238 | 0 | 7 |
| kim | mms_fa | human | The Brave Under The Summer Sky | primary | 398 | 32 | 190 | 0 | 17 |
| kim | mms_fa | human | Worlds Pain | primary | 507 | 143 | 293 | 0 | 7 |
| kim | mms_fa | human | 両翼のBrilliance | primary | 506 | 199 | 315 | 0 | 10 |
| kim | mms_fa | human | 光陰の海原 | primary | 373 | 35 | 145 | 0 | 10 |
| kim | mms_fa | human | 恋のルチはや♡ローリング | primary | 402 | 114 | 225 | 0 | 5 |
| kim | mms_fa | human | 恋桜開花前線 | primary | 496 | 55 | 292 | 0 | 19 |
| kim | mms_fa | human | 白い季節 | primary | 427 | 45 | 154 | 0 | 24 |
| kim | mms_fa | human | 036 - リトルミラクル -Grip it tight- | primary | 431 | 161 | 269 | 0 | 24 |
| kim | mms_fa | human | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 4 | 36 | 0 | 15 |
| kim | mms_fa | human | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | mms_fa | human | 骹车破尼-假名注音 | teochew_kana | 449 | 164 | 331 | 0 | 3 |
| kim | mms_fa | padded | 003 - 撃槍・ガングニール | primary | 401 | 166 | 291 | 0 | 4 |
| kim | mms_fa | padded | POWDER SNOW (Live Ver.) | primary | 347 | 21 | 96 | 0 | 25 |
| kim | mms_fa | padded | Rainbow Flower | primary | 374 | 138 | 240 | 0 | 11 |
| kim | mms_fa | padded | TSU-BA-SA | primary | 359 | 109 | 233 | 0 | 7 |
| kim | mms_fa | padded | The Brave Under The Summer Sky | primary | 398 | 27 | 191 | 0 | 17 |
| kim | mms_fa | padded | Worlds Pain | primary | 507 | 142 | 282 | 0 | 8 |
| kim | mms_fa | padded | 両翼のBrilliance | primary | 506 | 180 | 274 | 1 | 55 |
| kim | mms_fa | padded | 光陰の海原 | primary | 373 | 29 | 141 | 0 | 10 |
| kim | mms_fa | padded | 恋のルチはや♡ローリング | primary | 402 | 102 | 224 | 0 | 5 |
| kim | mms_fa | padded | 恋桜開花前線 | primary | 496 | 61 | 288 | 0 | 20 |
| kim | mms_fa | padded | 白い季節 | primary | 427 | 53 | 164 | 0 | 21 |
| kim | mms_fa | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 156 | 264 | 0 | 29 |
| kim | mms_fa | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | mms_fa | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | mms_fa | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 173 | 329 | 0 | 3 |
| kim | nextfire | auto_mms | 003 - 撃槍・ガングニール | primary | 401 | 344 | 371 | 0 | 5 |
| kim | nextfire | auto_mms | POWDER SNOW (Live Ver.) | primary | 347 | 244 | 290 | 0 | 14 |
| kim | nextfire | auto_mms | Rainbow Flower | primary | 374 | 252 | 310 | 0 | 3 |
| kim | nextfire | auto_mms | TSU-BA-SA | primary | 359 | 290 | 338 | 0 | 4 |
| kim | nextfire | auto_mms | The Brave Under The Summer Sky | primary | 398 | 285 | 351 | 0 | 6 |
| kim | nextfire | auto_mms | Worlds Pain | primary | 507 | 438 | 472 | 0 | 4 |
| kim | nextfire | auto_mms | 両翼のBrilliance | primary | 506 | 0 | 0 | 506 | 0 |
| kim | nextfire | auto_mms | 光陰の海原 | primary | 373 | 250 | 322 | 0 | 4 |
| kim | nextfire | auto_mms | 恋のルチはや♡ローリング | primary | 402 | 338 | 373 | 0 | 4 |
| kim | nextfire | auto_mms | 恋桜開花前線 | primary | 496 | 427 | 462 | 0 | 12 |
| kim | nextfire | auto_mms | 白い季節 | primary | 427 | 336 | 364 | 0 | 14 |
| kim | nextfire | auto_mms | 036 - リトルミラクル -Grip it tight- | primary | 431 | 296 | 366 | 0 | 18 |
| kim | nextfire | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | nextfire | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | nextfire | auto_mms | 骹车破尼-假名注音 | teochew_kana | 449 | 214 | 335 | 0 | 2 |
| kim | nextfire | auto_mms_pause | 003 - 撃槍・ガングニール | primary | 401 | 336 | 370 | 0 | 2 |
| kim | nextfire | auto_mms_pause | POWDER SNOW (Live Ver.) | primary | 347 | 265 | 305 | 0 | 4 |
| kim | nextfire | auto_mms_pause | Rainbow Flower | primary | 374 | 250 | 287 | 0 | 19 |
| kim | nextfire | auto_mms_pause | TSU-BA-SA | primary | 359 | 291 | 331 | 0 | 0 |
| kim | nextfire | auto_mms_pause | The Brave Under The Summer Sky | primary | 398 | 269 | 342 | 0 | 3 |
| kim | nextfire | auto_mms_pause | Worlds Pain | primary | 507 | 442 | 469 | 0 | 3 |
| kim | nextfire | auto_mms_pause | 両翼のBrilliance | primary | 506 | 0 | 0 | 506 | 0 |
| kim | nextfire | auto_mms_pause | 光陰の海原 | primary | 373 | 272 | 345 | 0 | 0 |
| kim | nextfire | auto_mms_pause | 恋のルチはや♡ローリング | primary | 402 | 347 | 370 | 0 | 3 |
| kim | nextfire | auto_mms_pause | 恋桜開花前線 | primary | 496 | 429 | 465 | 0 | 1 |
| kim | nextfire | auto_mms_pause | 白い季節 | primary | 427 | 368 | 393 | 0 | 8 |
| kim | nextfire | auto_mms_pause | 036 - リトルミラクル -Grip it tight- | primary | 431 | 341 | 382 | 0 | 9 |
| kim | nextfire | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | nextfire | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | nextfire | auto_mms_pause | 骹车破尼-假名注音 | teochew_kana | 449 | 209 | 325 | 0 | 5 |
| kim | nextfire | auto_nf | 003 - 撃槍・ガングニール | primary | 401 | 337 | 381 | 0 | 0 |
| kim | nextfire | auto_nf | POWDER SNOW (Live Ver.) | primary | 347 | 267 | 305 | 10 | 4 |
| kim | nextfire | auto_nf | Rainbow Flower | primary | 374 | 230 | 278 | 12 | 18 |
| kim | nextfire | auto_nf | TSU-BA-SA | primary | 359 | 287 | 345 | 0 | 3 |
| kim | nextfire | auto_nf | The Brave Under The Summer Sky | primary | 398 | 267 | 336 | 23 | 0 |
| kim | nextfire | auto_nf | Worlds Pain | primary | 507 | 456 | 489 | 0 | 0 |
| kim | nextfire | auto_nf | 両翼のBrilliance | primary | 506 | 402 | 455 | 0 | 10 |
| kim | nextfire | auto_nf | 光陰の海原 | primary | 373 | 279 | 333 | 16 | 0 |
| kim | nextfire | auto_nf | 恋のルチはや♡ローリング | primary | 402 | 350 | 377 | 0 | 0 |
| kim | nextfire | auto_nf | 恋桜開花前線 | primary | 496 | 458 | 488 | 0 | 0 |
| kim | nextfire | auto_nf | 白い季節 | primary | 427 | 360 | 387 | 8 | 0 |
| kim | nextfire | auto_nf | 036 - リトルミラクル -Grip it tight- | primary | 431 | 310 | 371 | 0 | 23 |
| kim | nextfire | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | nextfire | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | nextfire | auto_nf | 骹车破尼-假名注音 | teochew_kana | 449 | 228 | 337 | 0 | 22 |
| kim | nextfire | concat | 003 - 撃槍・ガングニール | primary | 401 | 350 | 379 | 0 | 0 |
| kim | nextfire | concat | POWDER SNOW (Live Ver.) | primary | 347 | 282 | 316 | 1 | 1 |
| kim | nextfire | concat | Rainbow Flower | primary | 374 | 274 | 305 | 1 | 17 |
| kim | nextfire | concat | TSU-BA-SA | primary | 359 | 314 | 347 | 0 | 3 |
| kim | nextfire | concat | The Brave Under The Summer Sky | primary | 398 | 332 | 386 | 2 | 0 |
| kim | nextfire | concat | Worlds Pain | primary | 507 | 467 | 490 | 0 | 0 |
| kim | nextfire | concat | 両翼のBrilliance | primary | 506 | 416 | 473 | 0 | 10 |
| kim | nextfire | concat | 光陰の海原 | primary | 373 | 287 | 345 | 1 | 0 |
| kim | nextfire | concat | 恋のルチはや♡ローリング | primary | 402 | 369 | 397 | 0 | 0 |
| kim | nextfire | concat | 恋桜開花前線 | primary | 496 | 463 | 490 | 0 | 0 |
| kim | nextfire | concat | 白い季節 | primary | 427 | 361 | 403 | 2 | 0 |
| kim | nextfire | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 361 | 386 | 0 | 17 |
| kim | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | nextfire | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 319 | 379 | 1 | 8 |
| kim | nextfire | fixed_cores | 003 - 撃槍・ガングニール | primary | 401 | 353 | 377 | 6 | 0 |
| kim | nextfire | fixed_cores | POWDER SNOW (Live Ver.) | primary | 347 | 275 | 309 | 11 | 1 |
| kim | nextfire | fixed_cores | Rainbow Flower | primary | 374 | 272 | 306 | 1 | 11 |
| kim | nextfire | fixed_cores | TSU-BA-SA | primary | 359 | 315 | 349 | 0 | 3 |
| kim | nextfire | fixed_cores | The Brave Under The Summer Sky | primary | 398 | 321 | 375 | 6 | 0 |
| kim | nextfire | fixed_cores | Worlds Pain | primary | 507 | 474 | 495 | 2 | 0 |
| kim | nextfire | fixed_cores | 両翼のBrilliance | primary | 506 | 411 | 470 | 0 | 8 |
| kim | nextfire | fixed_cores | 光陰の海原 | primary | 373 | 282 | 349 | 2 | 0 |
| kim | nextfire | fixed_cores | 恋のルチはや♡ローリング | primary | 402 | 372 | 397 | 1 | 0 |
| kim | nextfire | fixed_cores | 恋桜開花前線 | primary | 496 | 460 | 487 | 1 | 0 |
| kim | nextfire | fixed_cores | 白い季節 | primary | 427 | 394 | 403 | 5 | 0 |
| kim | nextfire | fixed_cores | 036 - リトルミラクル -Grip it tight- | primary | 431 | 352 | 389 | 1 | 16 |
| kim | nextfire | fixed_cores | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | nextfire | fixed_cores | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | nextfire | fixed_cores | 骹车破尼-假名注音 | teochew_kana | 449 | 317 | 364 | 3 | 9 |
| kim | nextfire | full | 003 - 撃槍・ガングニール | primary | 401 | 321 | 372 | 0 | 0 |
| kim | nextfire | full | POWDER SNOW (Live Ver.) | primary | 347 | 249 | 310 | 0 | 1 |
| kim | nextfire | full | Rainbow Flower | primary | 374 | 244 | 309 | 0 | 12 |
| kim | nextfire | full | TSU-BA-SA | primary | 359 | 289 | 344 | 0 | 3 |
| kim | nextfire | full | The Brave Under The Summer Sky | primary | 398 | 281 | 378 | 0 | 0 |
| kim | nextfire | full | Worlds Pain | primary | 507 | 422 | 488 | 0 | 0 |
| kim | nextfire | full | 両翼のBrilliance | primary | 506 | 402 | 463 | 0 | 14 |
| kim | nextfire | full | 光陰の海原 | primary | 373 | 234 | 338 | 0 | 4 |
| kim | nextfire | full | 恋のルチはや♡ローリング | primary | 402 | 342 | 395 | 0 | 0 |
| kim | nextfire | full | 恋桜開花前線 | primary | 496 | 406 | 489 | 0 | 0 |
| kim | nextfire | full | 白い季節 | primary | 427 | 354 | 397 | 0 | 0 |
| kim | nextfire | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 330 | 382 | 0 | 14 |
| kim | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | nextfire | full | 骹车破尼-假名注音 | teochew_kana | 449 | 242 | 344 | 0 | 13 |
| kim | nextfire | human | 003 - 撃槍・ガングニール | primary | 401 | 356 | 383 | 0 | 0 |
| kim | nextfire | human | POWDER SNOW (Live Ver.) | primary | 347 | 278 | 317 | 0 | 0 |
| kim | nextfire | human | Rainbow Flower | primary | 374 | 287 | 323 | 0 | 0 |
| kim | nextfire | human | TSU-BA-SA | primary | 359 | 309 | 346 | 0 | 0 |
| kim | nextfire | human | The Brave Under The Summer Sky | primary | 398 | 294 | 368 | 0 | 0 |
| kim | nextfire | human | Worlds Pain | primary | 507 | 461 | 491 | 0 | 0 |
| kim | nextfire | human | 両翼のBrilliance | primary | 506 | 411 | 479 | 0 | 2 |
| kim | nextfire | human | 光陰の海原 | primary | 373 | 283 | 345 | 0 | 0 |
| kim | nextfire | human | 恋のルチはや♡ローリング | primary | 402 | 352 | 391 | 0 | 0 |
| kim | nextfire | human | 恋桜開花前線 | primary | 496 | 464 | 485 | 0 | 0 |
| kim | nextfire | human | 白い季節 | primary | 427 | 375 | 387 | 0 | 0 |
| kim | nextfire | human | 036 - リトルミラクル -Grip it tight- | primary | 431 | 324 | 388 | 0 | 8 |
| kim | nextfire | human | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 67 | 97 | 0 | 0 |
| kim | nextfire | human | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | nextfire | human | 骹车破尼-假名注音 | teochew_kana | 449 | 233 | 349 | 0 | 4 |
| kim | nextfire | padded | 003 - 撃槍・ガングニール | primary | 401 | 352 | 380 | 0 | 0 |
| kim | nextfire | padded | POWDER SNOW (Live Ver.) | primary | 347 | 271 | 314 | 0 | 1 |
| kim | nextfire | padded | Rainbow Flower | primary | 374 | 265 | 305 | 0 | 11 |
| kim | nextfire | padded | TSU-BA-SA | primary | 359 | 318 | 348 | 0 | 3 |
| kim | nextfire | padded | The Brave Under The Summer Sky | primary | 398 | 329 | 385 | 0 | 0 |
| kim | nextfire | padded | Worlds Pain | primary | 507 | 462 | 491 | 0 | 0 |
| kim | nextfire | padded | 両翼のBrilliance | primary | 506 | 411 | 470 | 0 | 11 |
| kim | nextfire | padded | 光陰の海原 | primary | 373 | 274 | 332 | 1 | 13 |
| kim | nextfire | padded | 恋のルチはや♡ローリング | primary | 402 | 367 | 397 | 0 | 0 |
| kim | nextfire | padded | 恋桜開花前線 | primary | 496 | 460 | 488 | 0 | 0 |
| kim | nextfire | padded | 白い季節 | primary | 427 | 361 | 402 | 0 | 0 |
| kim | nextfire | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 358 | 386 | 1 | 18 |
| kim | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | nextfire | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 260 | 352 | 1 | 16 |
| kim | tifa | auto_mms | 003 - 撃槍・ガングニール | primary | 401 | 362 | 383 | 0 | 4 |
| kim | tifa | auto_mms | POWDER SNOW (Live Ver.) | primary | 347 | 257 | 290 | 0 | 14 |
| kim | tifa | auto_mms | Rainbow Flower | primary | 374 | 310 | 343 | 0 | 3 |
| kim | tifa | auto_mms | TSU-BA-SA | primary | 359 | 314 | 342 | 0 | 4 |
| kim | tifa | auto_mms | The Brave Under The Summer Sky | primary | 398 | 233 | 361 | 0 | 6 |
| kim | tifa | auto_mms | Worlds Pain | primary | 507 | 439 | 481 | 0 | 3 |
| kim | tifa | auto_mms | 両翼のBrilliance | primary | 506 | 0 | 0 | 506 | 0 |
| kim | tifa | auto_mms | 光陰の海原 | primary | 373 | 233 | 324 | 0 | 4 |
| kim | tifa | auto_mms | 恋のルチはや♡ローリング | primary | 402 | 332 | 373 | 0 | 5 |
| kim | tifa | auto_mms | 恋桜開花前線 | primary | 496 | 363 | 461 | 0 | 12 |
| kim | tifa | auto_mms | 白い季節 | primary | 427 | 324 | 364 | 0 | 10 |
| kim | tifa | auto_mms | 036 - リトルミラクル -Grip it tight- | primary | 431 | 346 | 380 | 0 | 15 |
| kim | tifa | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | tifa | auto_mms | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | tifa | auto_mms | 骹车破尼-假名注音 | teochew_kana | 449 | 292 | 410 | 0 | 2 |
| kim | tifa | auto_mms_pause | 003 - 撃槍・ガングニール | primary | 401 | 362 | 386 | 0 | 1 |
| kim | tifa | auto_mms_pause | POWDER SNOW (Live Ver.) | primary | 347 | 267 | 311 | 0 | 1 |
| kim | tifa | auto_mms_pause | Rainbow Flower | primary | 374 | 305 | 340 | 0 | 7 |
| kim | tifa | auto_mms_pause | TSU-BA-SA | primary | 359 | 318 | 343 | 0 | 2 |
| kim | tifa | auto_mms_pause | The Brave Under The Summer Sky | primary | 398 | 230 | 360 | 0 | 1 |
| kim | tifa | auto_mms_pause | Worlds Pain | primary | 507 | 447 | 491 | 0 | 1 |
| kim | tifa | auto_mms_pause | 両翼のBrilliance | primary | 506 | 0 | 0 | 506 | 0 |
| kim | tifa | auto_mms_pause | 光陰の海原 | primary | 373 | 239 | 336 | 0 | 4 |
| kim | tifa | auto_mms_pause | 恋のルチはや♡ローリング | primary | 402 | 342 | 380 | 0 | 4 |
| kim | tifa | auto_mms_pause | 恋桜開花前線 | primary | 496 | 370 | 474 | 0 | 5 |
| kim | tifa | auto_mms_pause | 白い季節 | primary | 427 | 339 | 389 | 0 | 5 |
| kim | tifa | auto_mms_pause | 036 - リトルミラクル -Grip it tight- | primary | 431 | 345 | 379 | 0 | 20 |
| kim | tifa | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | tifa | auto_mms_pause | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | tifa | auto_mms_pause | 骹车破尼-假名注音 | teochew_kana | 449 | 290 | 413 | 0 | 1 |
| kim | tifa | auto_nf | 003 - 撃槍・ガングニール | primary | 401 | 370 | 389 | 0 | 0 |
| kim | tifa | auto_nf | POWDER SNOW (Live Ver.) | primary | 347 | 264 | 302 | 10 | 1 |
| kim | tifa | auto_nf | Rainbow Flower | primary | 374 | 296 | 330 | 12 | 5 |
| kim | tifa | auto_nf | TSU-BA-SA | primary | 359 | 316 | 346 | 0 | 1 |
| kim | tifa | auto_nf | The Brave Under The Summer Sky | primary | 398 | 226 | 344 | 23 | 0 |
| kim | tifa | auto_nf | Worlds Pain | primary | 507 | 455 | 497 | 0 | 0 |
| kim | tifa | auto_nf | 両翼のBrilliance | primary | 506 | 419 | 481 | 0 | 7 |
| kim | tifa | auto_nf | 光陰の海原 | primary | 373 | 230 | 321 | 16 | 4 |
| kim | tifa | auto_nf | 恋のルチはや♡ローリング | primary | 402 | 345 | 381 | 0 | 2 |
| kim | tifa | auto_nf | 恋桜開花前線 | primary | 496 | 387 | 482 | 0 | 0 |
| kim | tifa | auto_nf | 白い季節 | primary | 427 | 340 | 384 | 8 | 3 |
| kim | tifa | auto_nf | 036 - リトルミラクル -Grip it tight- | primary | 431 | 359 | 389 | 0 | 16 |
| kim | tifa | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| kim | tifa | auto_nf | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| kim | tifa | auto_nf | 骹车破尼-假名注音 | teochew_kana | 449 | 288 | 401 | 0 | 8 |
| kim | tifa | concat | 003 - 撃槍・ガングニール | primary | 401 | 225 | 246 | 26 | 97 |
| kim | tifa | concat | POWDER SNOW (Live Ver.) | primary | 347 | 169 | 191 | 2 | 121 |
| kim | tifa | concat | Rainbow Flower | primary | 374 | 208 | 228 | 5 | 109 |
| kim | tifa | concat | TSU-BA-SA | primary | 359 | 280 | 319 | 1 | 3 |
| kim | tifa | concat | The Brave Under The Summer Sky | primary | 398 | 128 | 233 | 19 | 131 |
| kim | tifa | concat | Worlds Pain | primary | 507 | 279 | 320 | 23 | 137 |
| kim | tifa | concat | 両翼のBrilliance | primary | 506 | 259 | 311 | 4 | 146 |
| kim | tifa | concat | 光陰の海原 | primary | 373 | 133 | 196 | 25 | 130 |
| kim | tifa | concat | 恋のルチはや♡ローリング | primary | 402 | 296 | 334 | 2 | 18 |
| kim | tifa | concat | 恋桜開花前線 | primary | 496 | 240 | 329 | 9 | 117 |
| kim | tifa | concat | 白い季節 | primary | 427 | 198 | 239 | 8 | 139 |
| kim | tifa | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 143 | 171 | 42 | 199 |
| kim | tifa | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 52 | 77 | 2 | 5 |
| kim | tifa | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 24 | 37 | 39 | 69 |
| kim | tifa | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 257 | 376 | 20 | 2 |
| kim | tifa | fixed_cores | 003 - 撃槍・ガングニール | primary | 401 | 293 | 344 | 7 | 3 |
| kim | tifa | fixed_cores | POWDER SNOW (Live Ver.) | primary | 347 | 169 | 194 | 14 | 102 |
| kim | tifa | fixed_cores | Rainbow Flower | primary | 374 | 165 | 189 | 8 | 128 |
| kim | tifa | fixed_cores | TSU-BA-SA | primary | 359 | 288 | 324 | 2 | 3 |
| kim | tifa | fixed_cores | The Brave Under The Summer Sky | primary | 398 | 124 | 232 | 27 | 124 |
| kim | tifa | fixed_cores | Worlds Pain | primary | 507 | 288 | 329 | 23 | 135 |
| kim | tifa | fixed_cores | 両翼のBrilliance | primary | 506 | 258 | 314 | 3 | 147 |
| kim | tifa | fixed_cores | 光陰の海原 | primary | 373 | 136 | 194 | 38 | 122 |
| kim | tifa | fixed_cores | 恋のルチはや♡ローリング | primary | 402 | 300 | 336 | 4 | 20 |
| kim | tifa | fixed_cores | 恋桜開花前線 | primary | 496 | 244 | 328 | 9 | 118 |
| kim | tifa | fixed_cores | 白い季節 | primary | 427 | 196 | 231 | 23 | 143 |
| kim | tifa | fixed_cores | 036 - リトルミラクル -Grip it tight- | primary | 431 | 145 | 169 | 51 | 192 |
| kim | tifa | fixed_cores | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 52 | 80 | 5 | 4 |
| kim | tifa | fixed_cores | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 24 | 39 | 52 | 56 |
| kim | tifa | fixed_cores | 骹车破尼-假名注音 | teochew_kana | 449 | 267 | 372 | 22 | 4 |
| kim | tifa | full | 003 - 撃槍・ガングニール | primary | 401 | 230 | 251 | 2 | 101 |
| kim | tifa | full | POWDER SNOW (Live Ver.) | primary | 347 | 1 | 2 | 80 | 261 |
| kim | tifa | full | Rainbow Flower | primary | 374 | 199 | 222 | 0 | 117 |
| kim | tifa | full | TSU-BA-SA | primary | 359 | 238 | 272 | 12 | 62 |
| kim | tifa | full | The Brave Under The Summer Sky | primary | 398 | 98 | 193 | 7 | 155 |
| kim | tifa | full | Worlds Pain | primary | 507 | 223 | 265 | 13 | 165 |
| kim | tifa | full | 両翼のBrilliance | primary | 506 | 156 | 200 | 14 | 247 |
| kim | tifa | full | 光陰の海原 | primary | 373 | 114 | 180 | 20 | 119 |
| kim | tifa | full | 恋のルチはや♡ローリング | primary | 402 | 241 | 280 | 3 | 90 |
| kim | tifa | full | 恋桜開花前線 | primary | 496 | 194 | 258 | 10 | 193 |
| kim | tifa | full | 白い季節 | primary | 427 | 134 | 168 | 9 | 225 |
| kim | tifa | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 166 | 193 | 9 | 187 |
| kim | tifa | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 60 | 86 | 0 | 1 |
| kim | tifa | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 9 | 20 | 7 | 99 |
| kim | tifa | full | 骹车破尼-假名注音 | teochew_kana | 449 | 155 | 212 | 67 | 137 |
| kim | tifa | human | 003 - 撃槍・ガングニール | primary | 401 | 373 | 391 | 0 | 0 |
| kim | tifa | human | POWDER SNOW (Live Ver.) | primary | 347 | 281 | 320 | 0 | 0 |
| kim | tifa | human | Rainbow Flower | primary | 374 | 330 | 359 | 0 | 2 |
| kim | tifa | human | TSU-BA-SA | primary | 359 | 327 | 353 | 0 | 0 |
| kim | tifa | human | The Brave Under The Summer Sky | primary | 398 | 245 | 373 | 0 | 0 |
| kim | tifa | human | Worlds Pain | primary | 507 | 462 | 502 | 0 | 0 |
| kim | tifa | human | 両翼のBrilliance | primary | 506 | 433 | 495 | 0 | 1 |
| kim | tifa | human | 光陰の海原 | primary | 373 | 246 | 338 | 0 | 4 |
| kim | tifa | human | 恋のルチはや♡ローリング | primary | 402 | 353 | 386 | 0 | 2 |
| kim | tifa | human | 恋桜開花前線 | primary | 496 | 393 | 483 | 0 | 0 |
| kim | tifa | human | 白い季節 | primary | 427 | 356 | 397 | 0 | 2 |
| kim | tifa | human | 036 - リトルミラクル -Grip it tight- | primary | 431 | 370 | 400 | 0 | 15 |
| kim | tifa | human | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 71 | 100 | 0 | 0 |
| kim | tifa | human | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 105 | 144 | 0 | 0 |
| kim | tifa | human | 骹车破尼-假名注音 | teochew_kana | 449 | 323 | 417 | 0 | 1 |
| kim | tifa | padded | 003 - 撃槍・ガングニール | primary | 401 | 231 | 253 | 14 | 113 |
| kim | tifa | padded | POWDER SNOW (Live Ver.) | primary | 347 | 161 | 183 | 2 | 113 |
| kim | tifa | padded | Rainbow Flower | primary | 374 | 206 | 228 | 1 | 114 |
| kim | tifa | padded | TSU-BA-SA | primary | 359 | 280 | 321 | 1 | 3 |
| kim | tifa | padded | The Brave Under The Summer Sky | primary | 398 | 127 | 231 | 20 | 130 |
| kim | tifa | padded | Worlds Pain | primary | 507 | 279 | 321 | 26 | 108 |
| kim | tifa | padded | 両翼のBrilliance | primary | 506 | 255 | 308 | 2 | 154 |
| kim | tifa | padded | 光陰の海原 | primary | 373 | 138 | 200 | 25 | 124 |
| kim | tifa | padded | 恋のルチはや♡ローリング | primary | 402 | 293 | 332 | 0 | 24 |
| kim | tifa | padded | 恋桜開花前線 | primary | 496 | 247 | 333 | 6 | 121 |
| kim | tifa | padded | 白い季節 | primary | 427 | 198 | 238 | 1 | 144 |
| kim | tifa | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 145 | 172 | 46 | 192 |
| kim | tifa | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 55 | 76 | 0 | 3 |
| kim | tifa | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 26 | 39 | 22 | 84 |
| kim | tifa | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 262 | 380 | 2 | 5 |
| mel_roformer | nextfire | concat | 003 - 撃槍・ガングニール | primary | 401 | 352 | 378 | 0 | 0 |
| mel_roformer | nextfire | concat | POWDER SNOW (Live Ver.) | primary | 347 | 276 | 316 | 1 | 1 |
| mel_roformer | nextfire | concat | Rainbow Flower | primary | 374 | 274 | 305 | 1 | 17 |
| mel_roformer | nextfire | concat | TSU-BA-SA | primary | 359 | 314 | 347 | 0 | 3 |
| mel_roformer | nextfire | concat | The Brave Under The Summer Sky | primary | 398 | 329 | 386 | 2 | 0 |
| mel_roformer | nextfire | concat | Worlds Pain | primary | 507 | 466 | 490 | 0 | 0 |
| mel_roformer | nextfire | concat | 両翼のBrilliance | primary | 506 | 413 | 471 | 0 | 10 |
| mel_roformer | nextfire | concat | 光陰の海原 | primary | 373 | 287 | 342 | 1 | 0 |
| mel_roformer | nextfire | concat | 恋のルチはや♡ローリング | primary | 402 | 369 | 397 | 0 | 0 |
| mel_roformer | nextfire | concat | 恋桜開花前線 | primary | 496 | 467 | 490 | 0 | 0 |
| mel_roformer | nextfire | concat | 白い季節 | primary | 427 | 366 | 407 | 2 | 0 |
| mel_roformer | nextfire | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 363 | 393 | 1 | 10 |
| mel_roformer | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| mel_roformer | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| mel_roformer | nextfire | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 307 | 370 | 2 | 9 |
| mel_roformer | nextfire | full | 003 - 撃槍・ガングニール | primary | 401 | 321 | 372 | 0 | 0 |
| mel_roformer | nextfire | full | POWDER SNOW (Live Ver.) | primary | 347 | 249 | 310 | 0 | 1 |
| mel_roformer | nextfire | full | Rainbow Flower | primary | 374 | 244 | 309 | 0 | 12 |
| mel_roformer | nextfire | full | TSU-BA-SA | primary | 359 | 289 | 344 | 0 | 3 |
| mel_roformer | nextfire | full | The Brave Under The Summer Sky | primary | 398 | 282 | 378 | 0 | 0 |
| mel_roformer | nextfire | full | Worlds Pain | primary | 507 | 422 | 488 | 0 | 0 |
| mel_roformer | nextfire | full | 両翼のBrilliance | primary | 506 | 402 | 463 | 0 | 14 |
| mel_roformer | nextfire | full | 光陰の海原 | primary | 373 | 234 | 338 | 0 | 4 |
| mel_roformer | nextfire | full | 恋のルチはや♡ローリング | primary | 402 | 342 | 395 | 0 | 0 |
| mel_roformer | nextfire | full | 恋桜開花前線 | primary | 496 | 405 | 489 | 0 | 0 |
| mel_roformer | nextfire | full | 白い季節 | primary | 427 | 354 | 397 | 0 | 0 |
| mel_roformer | nextfire | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 330 | 380 | 0 | 14 |
| mel_roformer | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| mel_roformer | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| mel_roformer | nextfire | full | 骹车破尼-假名注音 | teochew_kana | 449 | 242 | 344 | 0 | 12 |
| mel_roformer | nextfire | padded | 003 - 撃槍・ガングニール | primary | 401 | 347 | 381 | 0 | 0 |
| mel_roformer | nextfire | padded | POWDER SNOW (Live Ver.) | primary | 347 | 272 | 315 | 0 | 1 |
| mel_roformer | nextfire | padded | Rainbow Flower | primary | 374 | 265 | 305 | 0 | 11 |
| mel_roformer | nextfire | padded | TSU-BA-SA | primary | 359 | 317 | 348 | 0 | 3 |
| mel_roformer | nextfire | padded | The Brave Under The Summer Sky | primary | 398 | 329 | 385 | 0 | 0 |
| mel_roformer | nextfire | padded | Worlds Pain | primary | 507 | 462 | 491 | 0 | 0 |
| mel_roformer | nextfire | padded | 両翼のBrilliance | primary | 506 | 410 | 472 | 0 | 7 |
| mel_roformer | nextfire | padded | 光陰の海原 | primary | 373 | 280 | 329 | 1 | 13 |
| mel_roformer | nextfire | padded | 恋のルチはや♡ローリング | primary | 402 | 367 | 397 | 0 | 0 |
| mel_roformer | nextfire | padded | 恋桜開花前線 | primary | 496 | 457 | 489 | 0 | 0 |
| mel_roformer | nextfire | padded | 白い季節 | primary | 427 | 364 | 404 | 0 | 0 |
| mel_roformer | nextfire | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 358 | 386 | 1 | 18 |
| mel_roformer | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| mel_roformer | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| mel_roformer | nextfire | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 245 | 323 | 1 | 25 |
| scnet | nextfire | concat | 003 - 撃槍・ガングニール | primary | 401 | 344 | 382 | 2 | 0 |
| scnet | nextfire | concat | POWDER SNOW (Live Ver.) | primary | 347 | 276 | 314 | 9 | 1 |
| scnet | nextfire | concat | Rainbow Flower | primary | 374 | 262 | 310 | 0 | 12 |
| scnet | nextfire | concat | TSU-BA-SA | primary | 359 | 310 | 350 | 0 | 3 |
| scnet | nextfire | concat | The Brave Under The Summer Sky | primary | 398 | 311 | 368 | 7 | 4 |
| scnet | nextfire | concat | Worlds Pain | primary | 507 | 445 | 480 | 14 | 0 |
| scnet | nextfire | concat | 両翼のBrilliance | primary | 506 | 390 | 460 | 0 | 10 |
| scnet | nextfire | concat | 光陰の海原 | primary | 373 | 259 | 336 | 0 | 0 |
| scnet | nextfire | concat | 恋のルチはや♡ローリング | primary | 402 | 376 | 396 | 0 | 0 |
| scnet | nextfire | concat | 恋桜開花前線 | primary | 496 | 456 | 483 | 0 | 0 |
| scnet | nextfire | concat | 白い季節 | primary | 427 | 381 | 397 | 11 | 0 |
| scnet | nextfire | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 300 | 363 | 3 | 33 |
| scnet | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| scnet | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| scnet | nextfire | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 309 | 365 | 4 | 10 |
| scnet | nextfire | full | 003 - 撃槍・ガングニール | primary | 401 | 351 | 384 | 0 | 0 |
| scnet | nextfire | full | POWDER SNOW (Live Ver.) | primary | 347 | 276 | 318 | 0 | 1 |
| scnet | nextfire | full | Rainbow Flower | primary | 374 | 229 | 304 | 0 | 18 |
| scnet | nextfire | full | TSU-BA-SA | primary | 359 | 294 | 343 | 0 | 3 |
| scnet | nextfire | full | The Brave Under The Summer Sky | primary | 398 | 297 | 372 | 0 | 4 |
| scnet | nextfire | full | Worlds Pain | primary | 507 | 403 | 486 | 0 | 0 |
| scnet | nextfire | full | 両翼のBrilliance | primary | 506 | 394 | 454 | 0 | 12 |
| scnet | nextfire | full | 光陰の海原 | primary | 373 | 239 | 334 | 0 | 0 |
| scnet | nextfire | full | 恋のルチはや♡ローリング | primary | 402 | 340 | 394 | 0 | 0 |
| scnet | nextfire | full | 恋桜開花前線 | primary | 496 | 434 | 486 | 0 | 0 |
| scnet | nextfire | full | 白い季節 | primary | 427 | 357 | 399 | 0 | 0 |
| scnet | nextfire | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 321 | 380 | 0 | 19 |
| scnet | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| scnet | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| scnet | nextfire | full | 骹车破尼-假名注音 | teochew_kana | 449 | 270 | 344 | 0 | 24 |
| scnet | nextfire | padded | 003 - 撃槍・ガングニール | primary | 401 | 351 | 386 | 0 | 0 |
| scnet | nextfire | padded | POWDER SNOW (Live Ver.) | primary | 347 | 274 | 315 | 2 | 1 |
| scnet | nextfire | padded | Rainbow Flower | primary | 374 | 263 | 310 | 0 | 15 |
| scnet | nextfire | padded | TSU-BA-SA | primary | 359 | 316 | 349 | 0 | 3 |
| scnet | nextfire | padded | The Brave Under The Summer Sky | primary | 398 | 309 | 377 | 0 | 4 |
| scnet | nextfire | padded | Worlds Pain | primary | 507 | 456 | 492 | 1 | 0 |
| scnet | nextfire | padded | 両翼のBrilliance | primary | 506 | 392 | 455 | 0 | 11 |
| scnet | nextfire | padded | 光陰の海原 | primary | 373 | 261 | 333 | 0 | 14 |
| scnet | nextfire | padded | 恋のルチはや♡ローリング | primary | 402 | 367 | 397 | 0 | 0 |
| scnet | nextfire | padded | 恋桜開花前線 | primary | 496 | 449 | 484 | 0 | 0 |
| scnet | nextfire | padded | 白い季節 | primary | 427 | 382 | 407 | 0 | 3 |
| scnet | nextfire | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 340 | 382 | 4 | 19 |
| scnet | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| scnet | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| scnet | nextfire | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 303 | 379 | 2 | 7 |
| windowed | nextfire | concat | 003 - 撃槍・ガングニール | primary | 401 | 355 | 378 | 0 | 0 |
| windowed | nextfire | concat | POWDER SNOW (Live Ver.) | primary | 347 | 282 | 316 | 1 | 1 |
| windowed | nextfire | concat | Rainbow Flower | primary | 374 | 268 | 303 | 0 | 20 |
| windowed | nextfire | concat | TSU-BA-SA | primary | 359 | 317 | 347 | 0 | 3 |
| windowed | nextfire | concat | The Brave Under The Summer Sky | primary | 398 | 338 | 383 | 2 | 0 |
| windowed | nextfire | concat | Worlds Pain | primary | 507 | 463 | 496 | 1 | 0 |
| windowed | nextfire | concat | 両翼のBrilliance | primary | 506 | 407 | 464 | 1 | 12 |
| windowed | nextfire | concat | 光陰の海原 | primary | 373 | 282 | 347 | 1 | 0 |
| windowed | nextfire | concat | 恋のルチはや♡ローリング | primary | 402 | 367 | 395 | 0 | 0 |
| windowed | nextfire | concat | 恋桜開花前線 | primary | 496 | 465 | 490 | 0 | 0 |
| windowed | nextfire | concat | 白い季節 | primary | 427 | 387 | 408 | 1 | 0 |
| windowed | nextfire | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 351 | 385 | 0 | 15 |
| windowed | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| windowed | nextfire | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| windowed | nextfire | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 305 | 377 | 3 | 7 |
| windowed | nextfire | full | 003 - 撃槍・ガングニール | primary | 401 | 333 | 374 | 0 | 0 |
| windowed | nextfire | full | POWDER SNOW (Live Ver.) | primary | 347 | 258 | 311 | 0 | 1 |
| windowed | nextfire | full | Rainbow Flower | primary | 374 | 244 | 311 | 0 | 12 |
| windowed | nextfire | full | TSU-BA-SA | primary | 359 | 280 | 342 | 0 | 3 |
| windowed | nextfire | full | The Brave Under The Summer Sky | primary | 398 | 289 | 375 | 0 | 0 |
| windowed | nextfire | full | Worlds Pain | primary | 507 | 410 | 483 | 0 | 0 |
| windowed | nextfire | full | 両翼のBrilliance | primary | 506 | 409 | 464 | 0 | 11 |
| windowed | nextfire | full | 光陰の海原 | primary | 373 | 234 | 334 | 0 | 4 |
| windowed | nextfire | full | 恋のルチはや♡ローリング | primary | 402 | 336 | 395 | 0 | 0 |
| windowed | nextfire | full | 恋桜開花前線 | primary | 496 | 404 | 486 | 0 | 0 |
| windowed | nextfire | full | 白い季節 | primary | 427 | 348 | 393 | 0 | 0 |
| windowed | nextfire | full | 036 - リトルミラクル -Grip it tight- | primary | 431 | 295 | 380 | 0 | 14 |
| windowed | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| windowed | nextfire | full | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| windowed | nextfire | full | 骹车破尼-假名注音 | teochew_kana | 449 | 253 | 344 | 0 | 14 |
| windowed | nextfire | padded | 003 - 撃槍・ガングニール | primary | 401 | 350 | 386 | 0 | 0 |
| windowed | nextfire | padded | POWDER SNOW (Live Ver.) | primary | 347 | 282 | 315 | 0 | 1 |
| windowed | nextfire | padded | Rainbow Flower | primary | 374 | 266 | 310 | 0 | 14 |
| windowed | nextfire | padded | TSU-BA-SA | primary | 359 | 313 | 351 | 0 | 3 |
| windowed | nextfire | padded | The Brave Under The Summer Sky | primary | 398 | 331 | 383 | 0 | 0 |
| windowed | nextfire | padded | Worlds Pain | primary | 507 | 457 | 489 | 0 | 0 |
| windowed | nextfire | padded | 両翼のBrilliance | primary | 506 | 398 | 461 | 0 | 12 |
| windowed | nextfire | padded | 光陰の海原 | primary | 373 | 266 | 336 | 1 | 13 |
| windowed | nextfire | padded | 恋のルチはや♡ローリング | primary | 402 | 365 | 396 | 0 | 0 |
| windowed | nextfire | padded | 恋桜開花前線 | primary | 496 | 461 | 487 | 0 | 0 |
| windowed | nextfire | padded | 白い季節 | primary | 427 | 375 | 405 | 0 | 1 |
| windowed | nextfire | padded | 036 - リトルミラクル -Grip it tight- | primary | 431 | 360 | 383 | 1 | 13 |
| windowed | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| windowed | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| windowed | nextfire | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 265 | 356 | 1 | 23 |
| demucs | product | concat | 003 - 撃槍・ガングニール | primary | 401 | 347 | 373 | 2 | 0 |
| demucs | product | concat | POWDER SNOW (Live Ver.) | primary | 347 | 277 | 317 | 2 | 1 |
| demucs | product | concat | Rainbow Flower | primary | 374 | 270 | 306 | 0 | 15 |
| demucs | product | concat | TSU-BA-SA | primary | 359 | 311 | 344 | 0 | 3 |
| demucs | product | concat | The Brave Under The Summer Sky | primary | 398 | 325 | 380 | 0 | 0 |
| demucs | product | concat | Worlds Pain | primary | 507 | 462 | 495 | 1 | 0 |
| demucs | product | concat | 両翼のBrilliance | primary | 506 | 408 | 458 | 1 | 16 |
| demucs | product | concat | 光陰の海原 | primary | 373 | 288 | 351 | 0 | 0 |
| demucs | product | concat | 恋のルチはや♡ローリング | primary | 402 | 360 | 396 | 0 | 0 |
| demucs | product | concat | 恋桜開花前線 | primary | 496 | 464 | 487 | 1 | 0 |
| demucs | product | concat | 白い季節 | primary | 427 | 403 | 411 | 0 | 0 |
| demucs | product | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 345 | 393 | 0 | 7 |
| demucs | product | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 71 | 97 | 1 | 0 |
| demucs | product | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 8 | 25 | 4 | 82 |
| demucs | product | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 330 | 392 | 0 | 9 |
| bs | product | concat | 003 - 撃槍・ガングニール | primary | 401 | 338 | 384 | 0 | 0 |
| bs | product | concat | POWDER SNOW (Live Ver.) | primary | 347 | 285 | 313 | 0 | 1 |
| bs | product | concat | Rainbow Flower | primary | 374 | 287 | 330 | 5 | 4 |
| bs | product | concat | TSU-BA-SA | primary | 359 | 320 | 351 | 0 | 3 |
| bs | product | concat | The Brave Under The Summer Sky | primary | 398 | 315 | 382 | 0 | 0 |
| bs | product | concat | Worlds Pain | primary | 507 | 471 | 490 | 0 | 0 |
| bs | product | concat | 両翼のBrilliance | primary | 506 | 428 | 481 | 0 | 2 |
| bs | product | concat | 光陰の海原 | primary | 373 | 292 | 348 | 0 | 0 |
| bs | product | concat | 恋のルチはや♡ローリング | primary | 402 | 375 | 399 | 0 | 0 |
| bs | product | concat | 恋桜開花前線 | primary | 496 | 461 | 491 | 0 | 0 |
| bs | product | concat | 白い季節 | primary | 427 | 386 | 405 | 0 | 0 |
| bs | product | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 359 | 400 | 1 | 2 |
| bs | product | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 73 | 98 | 1 | 0 |
| bs | product | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 19 | 51 | 3 | 37 |
| bs | product | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 315 | 376 | 0 | 7 |
| kim | product | concat | 003 - 撃槍・ガングニール | primary | 401 | 349 | 381 | 0 | 0 |
| kim | product | concat | POWDER SNOW (Live Ver.) | primary | 347 | 285 | 316 | 0 | 1 |
| kim | product | concat | Rainbow Flower | primary | 374 | 272 | 306 | 0 | 17 |
| kim | product | concat | TSU-BA-SA | primary | 359 | 315 | 349 | 0 | 3 |
| kim | product | concat | The Brave Under The Summer Sky | primary | 398 | 330 | 388 | 0 | 0 |
| kim | product | concat | Worlds Pain | primary | 507 | 466 | 492 | 0 | 0 |
| kim | product | concat | 両翼のBrilliance | primary | 506 | 417 | 472 | 0 | 9 |
| kim | product | concat | 光陰の海原 | primary | 373 | 288 | 339 | 0 | 0 |
| kim | product | concat | 恋のルチはや♡ローリング | primary | 402 | 370 | 397 | 0 | 0 |
| kim | product | concat | 恋桜開花前線 | primary | 496 | 461 | 490 | 0 | 0 |
| kim | product | concat | 白い季節 | primary | 427 | 359 | 405 | 0 | 0 |
| kim | product | concat | 036 - リトルミラクル -Grip it tight- | primary | 431 | 353 | 383 | 0 | 14 |
| kim | product | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 80 | 98 | 1 | 0 |
| kim | product | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 16 | 58 | 1 | 31 |
| kim | product | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 336 | 382 | 2 | 5 |
