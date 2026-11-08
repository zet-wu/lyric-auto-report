# 自动生成的消融结果表

主表为 11 首歌曲等权的双端 100 ms 命中率。

## nextfire

| 策略 | Demucs | BS Karaoke | Kim |
| --- | ---: | ---: | ---: |
| concat | 83.91% | 86.05% | 84.88% |
| padded | 83.10% | 85.36% | 83.85% |
| full | 75.00% | 77.24% | 76.67% |
| auto_mms | 60.55% | 71.19% | 70.74% |
| auto_nf | 74.72% | 79.76% | 79.76% |
| human | 80.40% | 84.25% | 83.87% |

## tifa

| 策略 | Demucs | BS Karaoke | Kim |
| --- | ---: | ---: | ---: |
| concat | 44.97% | 52.10% | 52.80% |
| padded | 45.48% | 51.70% | 52.77% |
| full | 38.32% | 40.75% | 39.78% |
| auto_mms | 62.97% | 70.25% | 70.36% |
| auto_nf | 77.97% | 79.06% | 79.09% |
| human | 82.71% | 82.96% | 82.54% |

## mms_fa

| 策略 | Demucs | BS Karaoke | Kim |
| --- | ---: | ---: | ---: |
| concat | 21.97% | 22.19% | 22.34% |
| padded | 21.58% | 22.30% | 22.08% |
| full | 22.92% | 22.58% | 22.71% |
| auto_mms | 16.32% | 19.37% | 18.93% |
| auto_nf | 22.14% | 21.71% | 22.56% |
| human | 22.53% | 22.66% | 22.56% |

## 全部固定分母结果

| 分离 | 后端 | 策略 | 100 ms 数/固定分母 | 宏平均 | 200 ms 数 | 缺失 | >1s | 起/止 MAE ms |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| bs | mms_fa | auto_mms | 920/4590 | 19.37% | 2224 | 374 | 129 | 37.65/258.58 |
| bs | mms_fa | auto_mms_pause | 917/4590 | 19.33% | 2221 | 374 | 131 | 42.45/260.08 |
| bs | mms_fa | auto_nf | 1015/4590 | 21.71% | 2414 | 96 | 137 | 39.38/253.60 |
| bs | mms_fa | concat | 1037/4590 | 22.19% | 2419 | 2 | 182 | 65.09/280.48 |
| bs | mms_fa | fixed_cores | 1024/4590 | 21.93% | 2424 | 3 | 170 | 60.79/276.04 |
| bs | mms_fa | full | 1052/4590 | 22.58% | 2451 | 0 | 141 | 46.52/262.80 |
| bs | mms_fa | human | 1054/4590 | 22.66% | 2458 | 0 | 137 | 38.59/253.67 |
| bs | mms_fa | padded | 1045/4590 | 22.30% | 2426 | 1 | 185 | 69.67/285.28 |
| bs | nextfire | auto_mms | 3318/4590 | 71.19% | 3778 | 374 | 75 | 52.08/97.65 |
| bs | nextfire | auto_mms_pause | 3373/4590 | 72.49% | 3837 | 374 | 22 | 58.76/76.39 |
| bs | nextfire | auto_nf | 3688/4590 | 79.76% | 4183 | 96 | 15 | 43.08/55.09 |
| bs | nextfire | concat | 3969/4590 | 86.05% | 4368 | 15 | 10 | 35.54/45.18 |
| bs | nextfire | fixed_cores | 3928/4590 | 85.05% | 4341 | 35 | 10 | 40.79/49.98 |
| bs | nextfire | full | 3572/4590 | 77.24% | 4342 | 0 | 11 | 54.90/70.42 |
| bs | nextfire | human | 3885/4590 | 84.25% | 4352 | 0 | 4 | 37.61/47.91 |
| bs | nextfire | padded | 3938/4590 | 85.36% | 4373 | 4 | 13 | 38.79/48.61 |
| bs | tifa | auto_mms | 3272/4590 | 70.25% | 3864 | 374 | 71 | 51.91/98.94 |
| bs | tifa | auto_mms_pause | 3339/4590 | 71.71% | 3949 | 374 | 27 | 60.17/73.01 |
| bs | tifa | auto_nf | 3649/4590 | 79.06% | 4258 | 96 | 18 | 52.02/62.95 |
| bs | tifa | concat | 2389/4590 | 52.10% | 2908 | 180 | 1098 | 4526.13/4535.16 |
| bs | tifa | fixed_cores | 2431/4590 | 53.11% | 2954 | 191 | 1047 | 4826.62/4831.47 |
| bs | tifa | full | 1877/4590 | 40.75% | 2330 | 168 | 1751 | 12146.52/12086.26 |
| bs | tifa | human | 3817/4590 | 82.96% | 4412 | 0 | 9 | 46.28/55.60 |
| bs | tifa | padded | 2373/4590 | 51.70% | 2901 | 182 | 1115 | 5736.72/5727.58 |
| bs_roformer | nextfire | concat | 3920/4590 | 84.96% | 4335 | 7 | 28 | 43.27/53.50 |
| bs_roformer | nextfire | full | 3519/4590 | 76.06% | 4268 | 0 | 33 | 65.02/81.82 |
| bs_roformer | nextfire | padded | 3907/4590 | 84.73% | 4327 | 1 | 27 | 43.73/54.30 |
| demucs | mms_fa | auto_mms | 736/4590 | 16.32% | 1914 | 908 | 122 | 40.52/267.70 |
| demucs | mms_fa | auto_mms_pause | 734/4590 | 16.28% | 1905 | 908 | 124 | 44.32/267.70 |
| demucs | mms_fa | auto_nf | 1036/4590 | 22.14% | 2396 | 170 | 134 | 44.81/256.22 |
| demucs | mms_fa | concat | 1021/4590 | 21.97% | 2396 | 3 | 220 | 126.60/335.24 |
| demucs | mms_fa | full | 1069/4590 | 22.92% | 2450 | 0 | 163 | 75.40/288.03 |
| demucs | mms_fa | human | 1051/4590 | 22.53% | 2468 | 0 | 141 | 42.06/254.79 |
| demucs | mms_fa | padded | 1005/4590 | 21.58% | 2384 | 4 | 227 | 146.00/351.89 |
| demucs | nextfire | auto_mms | 2747/4590 | 60.55% | 3239 | 908 | 88 | 70.60/118.90 |
| demucs | nextfire | auto_mms_pause | 2857/4590 | 62.98% | 3312 | 908 | 53 | 78.48/97.06 |
| demucs | nextfire | auto_nf | 3452/4590 | 74.72% | 4046 | 170 | 46 | 73.58/86.14 |
| demucs | nextfire | concat | 3873/4590 | 83.91% | 4292 | 33 | 36 | 55.16/64.57 |
| demucs | nextfire | full | 3465/4590 | 75.00% | 4253 | 0 | 55 | 84.13/103.09 |
| demucs | nextfire | human | 3704/4590 | 80.40% | 4276 | 0 | 20 | 49.46/61.23 |
| demucs | nextfire | padded | 3837/4590 | 83.10% | 4311 | 5 | 31 | 55.97/66.72 |
| demucs | tifa | auto_mms | 2840/4590 | 62.97% | 3356 | 908 | 67 | 55.55/104.85 |
| demucs | tifa | auto_mms_pause | 2884/4590 | 63.98% | 3418 | 908 | 35 | 67.45/81.68 |
| demucs | tifa | auto_nf | 3599/4590 | 77.97% | 4166 | 170 | 30 | 62.18/72.20 |
| demucs | tifa | concat | 2050/4590 | 44.97% | 2557 | 265 | 1384 | 7561.17/7573.88 |
| demucs | tifa | full | 1762/4590 | 38.32% | 2209 | 179 | 1776 | 9472.14/9412.63 |
| demucs | tifa | human | 3809/4590 | 82.71% | 4397 | 0 | 11 | 47.79/58.15 |
| demucs | tifa | padded | 2074/4590 | 45.48% | 2581 | 222 | 1387 | 8063.94/8057.34 |
| dttnet | nextfire | concat | 3905/4590 | 84.74% | 4330 | 8 | 31 | 52.99/60.50 |
| dttnet | nextfire | full | 3645/4590 | 78.88% | 4278 | 0 | 43 | 81.10/96.49 |
| dttnet | nextfire | padded | 3883/4590 | 84.13% | 4329 | 1 | 38 | 86.30/90.87 |
| kim | mms_fa | auto_mms | 848/4590 | 18.93% | 2136 | 506 | 130 | 37.22/262.68 |
| kim | mms_fa | auto_mms_pause | 842/4590 | 18.80% | 2144 | 506 | 136 | 40.84/262.02 |
| kim | mms_fa | auto_nf | 1052/4590 | 22.56% | 2451 | 69 | 138 | 39.05/253.88 |
| kim | mms_fa | concat | 1039/4590 | 22.34% | 2416 | 2 | 201 | 95.71/313.33 |
| kim | mms_fa | fixed_cores | 1018/4590 | 21.86% | 2402 | 2 | 192 | 98.15/312.02 |
| kim | mms_fa | full | 1059/4590 | 22.71% | 2447 | 0 | 154 | 85.19/305.23 |
| kim | mms_fa | human | 1050/4590 | 22.56% | 2467 | 0 | 139 | 38.70/253.45 |
| kim | mms_fa | padded | 1028/4590 | 22.08% | 2424 | 1 | 183 | 73.67/292.76 |
| kim | nextfire | auto_mms | 3204/4590 | 70.74% | 3653 | 506 | 70 | 43.06/94.43 |
| kim | nextfire | auto_mms_pause | 3269/4590 | 72.25% | 3677 | 506 | 43 | 57.63/80.18 |
| kim | nextfire | auto_nf | 3693/4590 | 79.76% | 4174 | 69 | 35 | 51.77/63.39 |
| kim | nextfire | concat | 3915/4590 | 84.88% | 4331 | 7 | 31 | 42.08/53.11 |
| kim | nextfire | fixed_cores | 3929/4590 | 85.12% | 4317 | 35 | 23 | 42.05/51.50 |
| kim | nextfire | full | 3544/4590 | 76.67% | 4283 | 0 | 34 | 61.73/77.12 |
| kim | nextfire | human | 3870/4590 | 83.87% | 4315 | 0 | 2 | 40.19/50.61 |
| kim | nextfire | padded | 3870/4590 | 83.85% | 4312 | 1 | 39 | 68.44/77.96 |
| kim | tifa | auto_mms | 3167/4590 | 70.36% | 3722 | 506 | 65 | 51.47/99.25 |
| kim | tifa | auto_mms_pause | 3219/4590 | 71.49% | 3810 | 506 | 31 | 62.65/74.41 |
| kim | tifa | auto_nf | 3648/4590 | 79.09% | 4257 | 69 | 23 | 56.63/66.78 |
| kim | tifa | concat | 2415/4590 | 52.80% | 2946 | 124 | 1148 | 5666.23/5662.33 |
| kim | tifa | fixed_cores | 2461/4590 | 53.75% | 3015 | 158 | 1045 | 4313.17/4309.99 |
| kim | tifa | full | 1828/4590 | 39.78% | 2291 | 170 | 1735 | 9981.47/9917.02 |
| kim | tifa | human | 3799/4590 | 82.54% | 4397 | 0 | 11 | 48.67/56.83 |
| kim | tifa | padded | 2415/4590 | 52.77% | 2948 | 98 | 1148 | 5511.47/5505.42 |
| mel_roformer | nextfire | concat | 3913/4590 | 84.80% | 4329 | 7 | 31 | 42.67/53.70 |
| mel_roformer | nextfire | full | 3544/4590 | 76.68% | 4283 | 0 | 34 | 61.23/76.08 |
| mel_roformer | nextfire | padded | 3870/4590 | 83.88% | 4316 | 1 | 35 | 67.81/77.39 |
| scnet | nextfire | concat | 3810/4590 | 82.62% | 4276 | 43 | 30 | 72.17/83.51 |
| scnet | nextfire | full | 3614/4590 | 78.36% | 4274 | 0 | 38 | 79.82/86.09 |
| scnet | nextfire | padded | 3820/4590 | 82.83% | 4305 | 3 | 51 | 118.93/125.69 |
| windowed | nextfire | concat | 3931/4590 | 85.25% | 4327 | 7 | 36 | 44.48/54.73 |
| windowed | nextfire | full | 3545/4590 | 76.75% | 4268 | 0 | 31 | 62.29/77.98 |
| windowed | nextfire | padded | 3864/4590 | 83.79% | 4319 | 1 | 44 | 69.99/80.30 |
| demucs | product | concat | 3895/4590 | 84.40% | 4296 | 34 | 36 | 56.21/65.46 |
| bs | product | concat | 3950/4590 | 85.63% | 4367 | 14 | 9 | 34.79/44.93 |
| kim | product | concat | 3906/4590 | 84.70% | 4329 | 7 | 31 | 42.80/53.68 |

## sustained_600ms

| 分离 | 后端 | 策略 | 分母 | 100ms 命中 | 缺失 | 结束 MAE ms | 结束偏差 ms | 时长比中位数 | 塌缩 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| bs | mms_fa | auto_mms | 488 | 0 | 24 | 904.86 | -903.32 | 0.129 | 441 |
| bs | mms_fa | auto_mms_pause | 488 | 0 | 24 | 893.40 | -884.48 | 0.131 | 436 |
| bs | mms_fa | auto_nf | 488 | 1 | 7 | 899.74 | -897.65 | 0.130 | 455 |
| bs | mms_fa | concat | 488 | 0 | 1 | 922.62 | -917.35 | 0.129 | 471 |
| bs | mms_fa | fixed_cores | 488 | 0 | 2 | 927.43 | -889.80 | 0.129 | 472 |
| bs | mms_fa | full | 488 | 0 | 0 | 918.01 | -914.97 | 0.132 | 471 |
| bs | mms_fa | human | 488 | 4 | 0 | 902.06 | -901.65 | 0.128 | 460 |
| bs | mms_fa | padded | 488 | 0 | 1 | 944.36 | -939.09 | 0.128 | 469 |
| bs | nextfire | auto_mms | 488 | 140 | 24 | 460.40 | -438.79 | 0.713 | 56 |
| bs | nextfire | auto_mms_pause | 488 | 252 | 24 | 141.71 | -41.73 | 0.972 | 12 |
| bs | nextfire | auto_nf | 488 | 275 | 7 | 116.48 | -65.97 | 0.967 | 9 |
| bs | nextfire | concat | 488 | 330 | 3 | 101.59 | -56.35 | 0.988 | 7 |
| bs | nextfire | fixed_cores | 488 | 313 | 22 | 99.18 | -63.80 | 0.980 | 10 |
| bs | nextfire | full | 488 | 284 | 0 | 162.18 | -13.82 | 0.983 | 8 |
| bs | nextfire | human | 488 | 303 | 0 | 102.41 | -79.76 | 0.951 | 7 |
| bs | nextfire | padded | 488 | 318 | 0 | 105.14 | -48.48 | 0.989 | 7 |
| bs | tifa | auto_mms | 488 | 115 | 24 | 463.16 | -455.17 | 0.726 | 46 |
| bs | tifa | auto_mms_pause | 488 | 217 | 24 | 164.35 | -91.06 | 0.961 | 12 |
| bs | tifa | auto_nf | 488 | 238 | 7 | 139.55 | -98.09 | 0.972 | 10 |
| bs | tifa | concat | 488 | 135 | 46 | 6347.70 | -2023.37 | 0.782 | 153 |
| bs | tifa | fixed_cores | 488 | 126 | 66 | 7805.70 | -2117.47 | 0.772 | 138 |
| bs | tifa | full | 488 | 111 | 28 | 17015.74 | 14212.70 | 0.334 | 219 |
| bs | tifa | human | 488 | 279 | 0 | 115.44 | -106.50 | 0.975 | 7 |
| bs | tifa | padded | 488 | 134 | 34 | 7818.98 | 913.86 | 0.773 | 166 |
| bs_roformer | nextfire | concat | 488 | 320 | 4 | 106.79 | -50.59 | 0.986 | 9 |
| bs_roformer | nextfire | full | 488 | 277 | 0 | 182.28 | 1.47 | 0.986 | 10 |
| bs_roformer | nextfire | padded | 488 | 311 | 1 | 108.80 | -47.16 | 0.983 | 9 |
| demucs | mms_fa | auto_mms | 488 | 0 | 49 | 907.50 | -905.38 | 0.128 | 413 |
| demucs | mms_fa | auto_mms_pause | 488 | 0 | 49 | 896.20 | -884.47 | 0.132 | 407 |
| demucs | mms_fa | auto_nf | 488 | 1 | 29 | 918.32 | -877.80 | 0.129 | 429 |
| demucs | mms_fa | concat | 488 | 0 | 0 | 979.55 | -849.73 | 0.128 | 469 |
| demucs | mms_fa | full | 488 | 0 | 0 | 1013.39 | -778.08 | 0.131 | 462 |
| demucs | mms_fa | human | 488 | 0 | 0 | 902.60 | -897.88 | 0.129 | 451 |
| demucs | mms_fa | padded | 488 | 0 | 1 | 1022.13 | -790.41 | 0.130 | 460 |
| demucs | nextfire | auto_mms | 488 | 127 | 49 | 454.22 | -433.35 | 0.708 | 52 |
| demucs | nextfire | auto_mms_pause | 488 | 234 | 49 | 166.14 | -71.39 | 0.968 | 15 |
| demucs | nextfire | auto_nf | 488 | 264 | 29 | 163.77 | -43.24 | 0.960 | 16 |
| demucs | nextfire | concat | 488 | 303 | 19 | 134.79 | -21.52 | 0.984 | 10 |
| demucs | nextfire | full | 488 | 262 | 0 | 212.76 | 7.17 | 0.978 | 12 |
| demucs | nextfire | human | 488 | 296 | 0 | 115.03 | -96.60 | 0.957 | 14 |
| demucs | nextfire | padded | 488 | 298 | 2 | 143.38 | -20.56 | 0.984 | 10 |
| demucs | tifa | auto_mms | 488 | 106 | 49 | 458.63 | -451.64 | 0.726 | 40 |
| demucs | tifa | auto_mms_pause | 488 | 199 | 49 | 186.09 | -135.97 | 0.953 | 14 |
| demucs | tifa | auto_nf | 488 | 223 | 29 | 164.43 | -87.51 | 0.962 | 13 |
| demucs | tifa | concat | 488 | 112 | 47 | 8392.53 | -4968.85 | 0.690 | 152 |
| demucs | tifa | full | 488 | 96 | 34 | 11831.63 | 6384.86 | 0.197 | 236 |
| demucs | tifa | human | 488 | 268 | 0 | 125.37 | -117.20 | 0.968 | 8 |
| demucs | tifa | padded | 488 | 120 | 30 | 8561.40 | -2984.28 | 0.696 | 158 |
| dttnet | nextfire | concat | 488 | 310 | 4 | 108.18 | -53.21 | 0.981 | 10 |
| dttnet | nextfire | full | 488 | 271 | 0 | 268.76 | 74.38 | 0.978 | 15 |
| dttnet | nextfire | padded | 488 | 305 | 0 | 161.50 | -101.29 | 0.984 | 12 |
| kim | mms_fa | auto_mms | 488 | 2 | 28 | 908.21 | -907.51 | 0.127 | 437 |
| kim | mms_fa | auto_mms_pause | 488 | 2 | 28 | 894.64 | -884.03 | 0.131 | 433 |
| kim | mms_fa | auto_nf | 488 | 0 | 11 | 911.40 | -907.32 | 0.131 | 451 |
| kim | mms_fa | concat | 488 | 0 | 1 | 942.52 | -933.58 | 0.126 | 472 |
| kim | mms_fa | fixed_cores | 488 | 0 | 0 | 971.67 | -859.05 | 0.126 | 474 |
| kim | mms_fa | full | 488 | 0 | 0 | 1071.95 | -742.30 | 0.131 | 469 |
| kim | mms_fa | human | 488 | 3 | 0 | 902.62 | -901.81 | 0.129 | 461 |
| kim | mms_fa | padded | 488 | 1 | 0 | 948.08 | -944.11 | 0.128 | 469 |
| kim | nextfire | auto_mms | 488 | 140 | 28 | 457.87 | -439.60 | 0.711 | 54 |
| kim | nextfire | auto_mms_pause | 488 | 265 | 28 | 152.57 | -43.03 | 0.967 | 12 |
| kim | nextfire | auto_nf | 488 | 281 | 11 | 108.40 | -57.39 | 0.967 | 9 |
| kim | nextfire | concat | 488 | 315 | 4 | 103.35 | -49.55 | 0.988 | 7 |
| kim | nextfire | fixed_cores | 488 | 319 | 20 | 96.37 | -52.94 | 0.980 | 6 |
| kim | nextfire | full | 488 | 286 | 0 | 157.07 | -20.33 | 0.980 | 9 |
| kim | nextfire | human | 488 | 311 | 0 | 95.64 | -75.99 | 0.955 | 8 |
| kim | nextfire | padded | 488 | 313 | 0 | 153.02 | -97.52 | 0.988 | 7 |
| kim | tifa | auto_mms | 488 | 112 | 28 | 462.54 | -455.64 | 0.720 | 42 |
| kim | tifa | auto_mms_pause | 488 | 215 | 28 | 172.45 | -99.93 | 0.959 | 14 |
| kim | tifa | auto_nf | 488 | 237 | 11 | 143.70 | -96.53 | 0.969 | 12 |
| kim | tifa | concat | 488 | 138 | 22 | 8170.98 | -1556.74 | 0.833 | 154 |
| kim | tifa | fixed_cores | 488 | 126 | 58 | 7268.68 | -1613.03 | 0.778 | 147 |
| kim | tifa | full | 488 | 110 | 32 | 15194.32 | 12708.55 | 0.352 | 214 |
| kim | tifa | human | 488 | 277 | 0 | 113.70 | -105.09 | 0.975 | 9 |
| kim | tifa | padded | 488 | 139 | 16 | 7479.75 | -721.65 | 0.812 | 161 |
| mel_roformer | nextfire | concat | 488 | 315 | 4 | 105.37 | -49.47 | 0.985 | 7 |
| mel_roformer | nextfire | full | 488 | 286 | 0 | 152.44 | -25.13 | 0.980 | 9 |
| mel_roformer | nextfire | padded | 488 | 312 | 0 | 154.16 | -96.63 | 0.988 | 7 |
| scnet | nextfire | concat | 488 | 304 | 16 | 134.93 | -61.05 | 0.967 | 8 |
| scnet | nextfire | full | 488 | 280 | 0 | 135.66 | -47.59 | 0.979 | 8 |
| scnet | nextfire | padded | 488 | 300 | 2 | 266.18 | -0.27 | 0.980 | 12 |
| windowed | nextfire | concat | 488 | 320 | 4 | 103.16 | -55.87 | 0.983 | 10 |
| windowed | nextfire | full | 488 | 281 | 0 | 161.31 | -23.49 | 0.987 | 10 |
| windowed | nextfire | padded | 488 | 310 | 0 | 155.62 | -102.50 | 0.985 | 11 |
| demucs | product | concat | 488 | 307 | 19 | 133.16 | -24.60 | 0.984 | 10 |
| bs | product | concat | 488 | 328 | 2 | 104.71 | -53.65 | 0.988 | 7 |
| kim | product | concat | 488 | 312 | 4 | 104.58 | -48.18 | 0.986 | 6 |

## written_long_mark

| 分离 | 后端 | 策略 | 分母 | 100ms 命中 | 缺失 | 结束 MAE ms | 结束偏差 ms | 时长比中位数 | 塌缩 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| bs | mms_fa | auto_mms | 10 | 0 | 0 | 438.10 | -438.10 | 0.266 | 5 |
| bs | mms_fa | auto_mms_pause | 10 | 0 | 0 | 436.10 | -436.10 | 0.289 | 4 |
| bs | mms_fa | auto_nf | 10 | 0 | 0 | 513.35 | -513.35 | 0.162 | 7 |
| bs | mms_fa | concat | 10 | 0 | 0 | 513.35 | -513.35 | 0.166 | 7 |
| bs | mms_fa | fixed_cores | 10 | 0 | 0 | 509.60 | -509.60 | 0.162 | 7 |
| bs | mms_fa | full | 10 | 0 | 0 | 476.10 | -476.10 | 0.195 | 6 |
| bs | mms_fa | human | 10 | 0 | 0 | 438.10 | -438.10 | 0.266 | 5 |
| bs | mms_fa | padded | 10 | 0 | 0 | 472.40 | -472.40 | 0.162 | 6 |
| bs | nextfire | auto_mms | 10 | 4 | 0 | 224.10 | -126.10 | 0.653 | 2 |
| bs | nextfire | auto_mms_pause | 10 | 5 | 0 | 142.90 | -112.10 | 0.810 | 1 |
| bs | nextfire | auto_nf | 10 | 6 | 0 | 167.45 | -145.35 | 0.819 | 1 |
| bs | nextfire | concat | 10 | 5 | 0 | 133.84 | -107.35 | 0.932 | 1 |
| bs | nextfire | fixed_cores | 10 | 6 | 0 | 118.27 | -91.60 | 0.975 | 1 |
| bs | nextfire | full | 10 | 6 | 0 | 114.70 | -88.10 | 1.023 | 1 |
| bs | nextfire | human | 10 | 5 | 0 | 164.90 | -134.10 | 0.773 | 1 |
| bs | nextfire | padded | 10 | 5 | 0 | 148.56 | -134.40 | 0.734 | 2 |
| bs | tifa | auto_mms | 10 | 10 | 0 | 40.50 | -37.10 | 1.009 | 0 |
| bs | tifa | auto_mms_pause | 10 | 10 | 0 | 41.50 | -38.10 | 1.014 | 0 |
| bs | tifa | auto_nf | 10 | 10 | 0 | 38.92 | -35.35 | 1.014 | 0 |
| bs | tifa | concat | 10 | 5 | 1 | 17480.80 | -17480.80 | 0.989 | 2 |
| bs | tifa | fixed_cores | 10 | 8 | 0 | 8047.84 | -8047.84 | 0.994 | 0 |
| bs | tifa | full | 10 | 5 | 1 | 2084.89 | 1897.77 | 0.970 | 3 |
| bs | tifa | human | 10 | 10 | 0 | 41.50 | -38.10 | 1.014 | 0 |
| bs | tifa | padded | 10 | 5 | 2 | 5283.92 | -5283.92 | 0.961 | 2 |
| bs_roformer | nextfire | concat | 10 | 5 | 0 | 143.69 | -122.59 | 0.815 | 2 |
| bs_roformer | nextfire | full | 10 | 4 | 0 | 172.90 | -150.10 | 0.758 | 2 |
| bs_roformer | nextfire | padded | 10 | 5 | 0 | 177.70 | -161.97 | 0.779 | 2 |
| demucs | mms_fa | auto_mms | 10 | 0 | 0 | 472.10 | -472.10 | 0.218 | 5 |
| demucs | mms_fa | auto_mms_pause | 10 | 0 | 0 | 472.10 | -472.10 | 0.218 | 5 |
| demucs | mms_fa | auto_nf | 10 | 0 | 0 | 473.77 | -473.77 | 0.229 | 5 |
| demucs | mms_fa | concat | 10 | 0 | 0 | 451.60 | -451.60 | 0.312 | 4 |
| demucs | mms_fa | full | 10 | 0 | 0 | 470.10 | -470.10 | 0.195 | 6 |
| demucs | mms_fa | human | 10 | 0 | 0 | 472.10 | -472.10 | 0.225 | 5 |
| demucs | mms_fa | padded | 10 | 0 | 0 | 473.67 | -473.67 | 0.199 | 6 |
| demucs | nextfire | auto_mms | 10 | 3 | 0 | 234.10 | -132.10 | 0.557 | 2 |
| demucs | nextfire | auto_mms_pause | 10 | 4 | 0 | 194.30 | -32.10 | 0.835 | 2 |
| demucs | nextfire | auto_nf | 10 | 3 | 0 | 286.10 | -223.77 | 0.842 | 2 |
| demucs | nextfire | concat | 10 | 4 | 0 | 123.66 | -77.60 | 0.992 | 2 |
| demucs | nextfire | full | 10 | 4 | 0 | 176.90 | -162.10 | 0.723 | 2 |
| demucs | nextfire | human | 10 | 4 | 0 | 158.90 | -100.10 | 0.842 | 1 |
| demucs | nextfire | padded | 10 | 5 | 0 | 148.15 | -121.67 | 0.794 | 1 |
| demucs | tifa | auto_mms | 10 | 10 | 0 | 43.50 | -40.10 | 1.014 | 0 |
| demucs | tifa | auto_mms_pause | 10 | 10 | 0 | 42.50 | -39.10 | 1.014 | 0 |
| demucs | tifa | auto_nf | 10 | 9 | 0 | 57.59 | -53.77 | 0.987 | 0 |
| demucs | tifa | concat | 10 | 3 | 1 | 17471.32 | -12406.54 | 1.009 | 1 |
| demucs | tifa | full | 10 | 6 | 0 | 2194.30 | 2001.90 | 0.987 | 4 |
| demucs | tifa | human | 10 | 10 | 0 | 43.50 | -40.10 | 1.014 | 0 |
| demucs | tifa | padded | 10 | 3 | 2 | 19583.09 | -17756.98 | 0.667 | 3 |
| dttnet | nextfire | concat | 10 | 3 | 0 | 199.75 | -186.66 | 0.724 | 2 |
| dttnet | nextfire | full | 10 | 5 | 0 | 192.70 | -166.10 | 0.780 | 2 |
| dttnet | nextfire | padded | 10 | 4 | 0 | 183.00 | -137.77 | 0.706 | 2 |
| kim | mms_fa | auto_mms | 10 | 0 | 0 | 478.10 | -478.10 | 0.199 | 6 |
| kim | mms_fa | auto_mms_pause | 10 | 0 | 0 | 476.10 | -476.10 | 0.195 | 6 |
| kim | mms_fa | auto_nf | 10 | 0 | 0 | 476.13 | -476.13 | 0.218 | 5 |
| kim | mms_fa | concat | 10 | 0 | 0 | 512.12 | -512.12 | 0.151 | 6 |
| kim | mms_fa | fixed_cores | 10 | 0 | 0 | 513.60 | -513.60 | 0.162 | 7 |
| kim | mms_fa | full | 10 | 0 | 0 | 514.10 | -514.10 | 0.151 | 7 |
| kim | mms_fa | human | 10 | 0 | 0 | 476.10 | -476.10 | 0.199 | 6 |
| kim | mms_fa | padded | 10 | 0 | 0 | 511.57 | -511.57 | 0.162 | 7 |
| kim | nextfire | auto_mms | 10 | 5 | 0 | 191.90 | -98.10 | 0.804 | 2 |
| kim | nextfire | auto_mms_pause | 10 | 5 | 0 | 225.90 | -72.10 | 0.762 | 2 |
| kim | nextfire | auto_nf | 10 | 6 | 0 | 97.11 | -64.13 | 0.956 | 1 |
| kim | nextfire | concat | 10 | 4 | 0 | 152.04 | -112.12 | 0.906 | 1 |
| kim | nextfire | fixed_cores | 10 | 6 | 0 | 128.27 | -97.60 | 0.994 | 1 |
| kim | nextfire | full | 10 | 4 | 0 | 172.70 | -158.10 | 0.980 | 1 |
| kim | nextfire | human | 10 | 5 | 0 | 152.30 | -118.10 | 0.828 | 1 |
| kim | nextfire | padded | 10 | 4 | 0 | 178.31 | -149.57 | 0.768 | 1 |
| kim | tifa | auto_mms | 10 | 10 | 0 | 39.50 | -36.10 | 1.016 | 0 |
| kim | tifa | auto_mms_pause | 10 | 10 | 0 | 43.50 | -40.10 | 1.009 | 0 |
| kim | tifa | auto_nf | 10 | 10 | 0 | 40.66 | -37.13 | 1.009 | 0 |
| kim | tifa | concat | 10 | 5 | 0 | 16857.00 | -16857.00 | 0.966 | 2 |
| kim | tifa | fixed_cores | 10 | 8 | 0 | 4811.67 | -4172.93 | 1.031 | 0 |
| kim | tifa | full | 10 | 6 | 3 | 1779.29 | 1721.00 | 1.054 | 1 |
| kim | tifa | human | 10 | 10 | 0 | 42.50 | -39.10 | 1.009 | 0 |
| kim | tifa | padded | 10 | 6 | 1 | 4768.61 | -4182.54 | 1.016 | 2 |
| mel_roformer | nextfire | concat | 10 | 3 | 0 | 140.23 | -99.79 | 0.906 | 2 |
| mel_roformer | nextfire | full | 10 | 4 | 0 | 172.70 | -158.10 | 0.980 | 1 |
| mel_roformer | nextfire | padded | 10 | 4 | 0 | 170.63 | -137.24 | 0.748 | 2 |
| scnet | nextfire | concat | 10 | 1 | 0 | 217.89 | -180.87 | 0.724 | 2 |
| scnet | nextfire | full | 10 | 4 | 0 | 204.70 | -190.10 | 0.892 | 2 |
| scnet | nextfire | padded | 10 | 5 | 0 | 175.98 | -160.22 | 0.882 | 1 |
| windowed | nextfire | concat | 10 | 4 | 0 | 152.38 | -118.57 | 0.892 | 1 |
| windowed | nextfire | full | 10 | 3 | 0 | 218.70 | -204.10 | 0.492 | 2 |
| windowed | nextfire | padded | 10 | 6 | 0 | 117.01 | -92.50 | 0.954 | 2 |
| demucs | product | concat | 10 | 7 | 0 | 119.71 | -78.16 | 0.992 | 2 |
| bs | product | concat | 10 | 6 | 0 | 115.47 | -89.62 | 0.893 | 1 |
| kim | product | concat | 10 | 5 | 0 | 136.53 | -64.44 | 0.960 | 1 |

## adjacent_identical_phones

| 分离 | 后端 | 策略 | 分母 | 100ms 命中 | 缺失 | 结束 MAE ms | 结束偏差 ms | 时长比中位数 | 塌缩 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| bs | mms_fa | auto_mms | 96 | 17 | 6 | 246.53 | -246.35 | 0.321 | 32 |
| bs | mms_fa | auto_mms_pause | 96 | 17 | 6 | 243.88 | -240.13 | 0.331 | 31 |
| bs | mms_fa | auto_nf | 96 | 12 | 4 | 213.31 | -209.95 | 0.346 | 29 |
| bs | mms_fa | concat | 96 | 15 | 0 | 242.26 | -242.26 | 0.313 | 32 |
| bs | mms_fa | fixed_cores | 96 | 20 | 0 | 241.63 | -221.13 | 0.317 | 30 |
| bs | mms_fa | full | 96 | 18 | 0 | 247.45 | -247.45 | 0.325 | 32 |
| bs | mms_fa | human | 96 | 17 | 0 | 245.95 | -245.78 | 0.323 | 36 |
| bs | mms_fa | padded | 96 | 19 | 0 | 248.68 | -238.45 | 0.318 | 31 |
| bs | nextfire | auto_mms | 96 | 60 | 6 | 119.86 | -91.91 | 0.998 | 9 |
| bs | nextfire | auto_mms_pause | 96 | 69 | 6 | 72.52 | -15.46 | 1.006 | 6 |
| bs | nextfire | auto_nf | 96 | 72 | 4 | 52.38 | -22.34 | 0.998 | 6 |
| bs | nextfire | concat | 96 | 77 | 1 | 46.84 | -22.37 | 1.019 | 4 |
| bs | nextfire | fixed_cores | 96 | 76 | 2 | 57.53 | -43.17 | 1.036 | 4 |
| bs | nextfire | full | 96 | 73 | 0 | 62.93 | -39.11 | 1.013 | 5 |
| bs | nextfire | human | 96 | 74 | 0 | 54.39 | -35.78 | 0.998 | 8 |
| bs | nextfire | padded | 96 | 76 | 0 | 56.08 | -23.24 | 1.022 | 5 |
| bs | tifa | auto_mms | 96 | 64 | 6 | 99.70 | -95.91 | 1.048 | 1 |
| bs | tifa | auto_mms_pause | 96 | 66 | 6 | 76.95 | -49.24 | 1.034 | 0 |
| bs | tifa | auto_nf | 96 | 68 | 4 | 71.68 | -64.41 | 1.048 | 0 |
| bs | tifa | concat | 96 | 44 | 5 | 6318.93 | -4363.97 | 1.000 | 12 |
| bs | tifa | fixed_cores | 96 | 47 | 7 | 3505.92 | -1651.19 | 0.996 | 13 |
| bs | tifa | full | 96 | 34 | 2 | 16561.76 | 16405.78 | 0.825 | 25 |
| bs | tifa | human | 96 | 74 | 0 | 64.80 | -60.16 | 1.001 | 0 |
| bs | tifa | padded | 96 | 44 | 5 | 6602.15 | -2639.44 | 0.957 | 19 |
| bs_roformer | nextfire | concat | 96 | 74 | 0 | 74.38 | -34.01 | 1.039 | 4 |
| bs_roformer | nextfire | full | 96 | 67 | 0 | 76.41 | -47.03 | 1.008 | 6 |
| bs_roformer | nextfire | padded | 96 | 73 | 0 | 69.55 | -32.80 | 1.046 | 5 |
| demucs | mms_fa | auto_mms | 96 | 13 | 18 | 232.89 | -232.68 | 0.359 | 26 |
| demucs | mms_fa | auto_mms_pause | 96 | 14 | 18 | 217.22 | -201.91 | 0.368 | 24 |
| demucs | mms_fa | auto_nf | 96 | 15 | 8 | 282.25 | -282.25 | 0.326 | 29 |
| demucs | mms_fa | concat | 96 | 20 | 0 | 242.12 | -242.09 | 0.334 | 30 |
| demucs | mms_fa | full | 96 | 18 | 0 | 239.95 | -239.95 | 0.328 | 30 |
| demucs | mms_fa | human | 96 | 19 | 0 | 243.66 | -241.62 | 0.324 | 33 |
| demucs | mms_fa | padded | 96 | 15 | 0 | 246.49 | -246.49 | 0.334 | 31 |
| demucs | nextfire | auto_mms | 96 | 53 | 18 | 101.78 | -70.12 | 0.983 | 7 |
| demucs | nextfire | auto_mms_pause | 96 | 60 | 18 | 59.22 | -28.58 | 1.000 | 4 |
| demucs | nextfire | auto_nf | 96 | 62 | 8 | 302.69 | 170.48 | 0.973 | 7 |
| demucs | nextfire | concat | 96 | 71 | 2 | 263.28 | 162.41 | 1.000 | 6 |
| demucs | nextfire | full | 96 | 62 | 0 | 357.30 | 66.51 | 1.034 | 7 |
| demucs | nextfire | human | 96 | 70 | 0 | 89.97 | -5.16 | 0.992 | 8 |
| demucs | nextfire | padded | 96 | 67 | 0 | 267.60 | 163.15 | 1.015 | 7 |
| demucs | tifa | auto_mms | 96 | 55 | 18 | 73.27 | -69.61 | 1.045 | 0 |
| demucs | tifa | auto_mms_pause | 96 | 56 | 18 | 78.71 | -45.76 | 1.029 | 0 |
| demucs | tifa | auto_nf | 96 | 58 | 8 | 113.90 | -105.43 | 1.034 | 1 |
| demucs | tifa | concat | 96 | 29 | 8 | 7680.93 | -4840.49 | 0.998 | 20 |
| demucs | tifa | full | 96 | 32 | 1 | 9545.81 | 5331.70 | 0.808 | 33 |
| demucs | tifa | human | 96 | 73 | 0 | 65.05 | -60.89 | 1.011 | 1 |
| demucs | tifa | padded | 96 | 35 | 7 | 7781.11 | -5926.55 | 1.000 | 18 |
| dttnet | nextfire | concat | 96 | 71 | 0 | 67.14 | -15.58 | 1.029 | 3 |
| dttnet | nextfire | full | 96 | 66 | 0 | 155.16 | -115.78 | 1.039 | 7 |
| dttnet | nextfire | padded | 96 | 73 | 0 | 125.15 | -97.33 | 1.008 | 5 |
| kim | mms_fa | auto_mms | 96 | 15 | 14 | 231.98 | -231.78 | 0.323 | 29 |
| kim | mms_fa | auto_mms_pause | 96 | 15 | 14 | 217.83 | -217.64 | 0.323 | 27 |
| kim | mms_fa | auto_nf | 96 | 20 | 2 | 247.94 | -244.10 | 0.316 | 31 |
| kim | mms_fa | concat | 96 | 19 | 0 | 241.31 | -231.10 | 0.314 | 31 |
| kim | mms_fa | fixed_cores | 96 | 19 | 0 | 242.46 | -221.55 | 0.324 | 31 |
| kim | mms_fa | full | 96 | 17 | 0 | 245.57 | -245.57 | 0.323 | 34 |
| kim | mms_fa | human | 96 | 16 | 0 | 254.59 | -230.16 | 0.323 | 37 |
| kim | mms_fa | padded | 96 | 15 | 0 | 251.34 | -240.46 | 0.312 | 32 |
| kim | nextfire | auto_mms | 96 | 57 | 14 | 96.78 | -76.17 | 0.994 | 7 |
| kim | nextfire | auto_mms_pause | 96 | 67 | 14 | 49.93 | -26.42 | 1.000 | 4 |
| kim | nextfire | auto_nf | 96 | 69 | 2 | 66.15 | -29.85 | 1.003 | 6 |
| kim | nextfire | concat | 96 | 72 | 0 | 59.20 | -25.48 | 1.000 | 4 |
| kim | nextfire | fixed_cores | 96 | 73 | 2 | 58.02 | -20.19 | 1.005 | 4 |
| kim | nextfire | full | 96 | 65 | 0 | 77.28 | -52.03 | 1.039 | 6 |
| kim | nextfire | human | 96 | 74 | 0 | 65.32 | -36.82 | 0.996 | 4 |
| kim | nextfire | padded | 96 | 65 | 0 | 131.74 | -92.13 | 1.037 | 3 |
| kim | tifa | auto_mms | 96 | 61 | 14 | 75.39 | -71.91 | 1.033 | 0 |
| kim | tifa | auto_mms_pause | 96 | 59 | 14 | 70.22 | -56.05 | 1.029 | 2 |
| kim | tifa | auto_nf | 96 | 66 | 2 | 100.24 | -93.36 | 1.025 | 4 |
| kim | tifa | concat | 96 | 49 | 3 | 6227.18 | -4677.91 | 0.995 | 15 |
| kim | tifa | fixed_cores | 96 | 46 | 5 | 4134.47 | -2963.54 | 0.958 | 18 |
| kim | tifa | full | 96 | 35 | 2 | 12199.79 | 11395.42 | 0.749 | 27 |
| kim | tifa | human | 96 | 75 | 0 | 65.12 | -60.16 | 0.998 | 0 |
| kim | tifa | padded | 96 | 46 | 4 | 5488.19 | -3782.12 | 0.961 | 15 |
| mel_roformer | nextfire | concat | 96 | 74 | 0 | 58.61 | -25.51 | 1.000 | 5 |
| mel_roformer | nextfire | full | 96 | 65 | 0 | 76.86 | -52.03 | 1.039 | 6 |
| mel_roformer | nextfire | padded | 96 | 67 | 0 | 136.55 | -97.51 | 1.056 | 5 |
| scnet | nextfire | concat | 96 | 72 | 1 | 56.06 | -43.34 | 1.006 | 4 |
| scnet | nextfire | full | 96 | 73 | 0 | 78.66 | -49.74 | 1.030 | 6 |
| scnet | nextfire | padded | 96 | 70 | 0 | 116.02 | -98.53 | 1.030 | 5 |
| windowed | nextfire | concat | 96 | 72 | 0 | 62.47 | -36.11 | 1.007 | 4 |
| windowed | nextfire | full | 96 | 61 | 0 | 84.59 | -58.07 | 1.039 | 7 |
| windowed | nextfire | padded | 96 | 69 | 0 | 144.83 | -106.81 | 1.046 | 6 |
| demucs | product | concat | 96 | 69 | 2 | 267.42 | 167.33 | 1.000 | 5 |
| bs | product | concat | 96 | 77 | 0 | 53.60 | -28.14 | 1.026 | 4 |
| kim | product | concat | 96 | 76 | 0 | 57.98 | -24.64 | 1.002 | 4 |

## same_phone_at_next_boundary

| 分离 | 后端 | 策略 | 分母 | 100ms 命中 | 缺失 | 结束 MAE ms | 结束偏差 ms | 时长比中位数 | 塌缩 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| bs | mms_fa | auto_mms | 75 | 13 | 6 | 273.28 | -264.12 | 0.322 | 20 |
| bs | mms_fa | auto_mms_pause | 75 | 14 | 6 | 270.96 | -261.80 | 0.321 | 22 |
| bs | mms_fa | auto_nf | 75 | 13 | 2 | 267.64 | -265.67 | 0.322 | 21 |
| bs | mms_fa | concat | 75 | 13 | 0 | 289.83 | -276.99 | 0.319 | 21 |
| bs | mms_fa | fixed_cores | 75 | 15 | 0 | 267.04 | -267.04 | 0.322 | 21 |
| bs | mms_fa | full | 75 | 16 | 0 | 271.05 | -258.17 | 0.351 | 21 |
| bs | mms_fa | human | 75 | 15 | 0 | 270.15 | -257.37 | 0.321 | 23 |
| bs | mms_fa | padded | 75 | 13 | 0 | 291.47 | -271.46 | 0.322 | 22 |
| bs | nextfire | auto_mms | 75 | 27 | 6 | 224.38 | -3.25 | 1.000 | 8 |
| bs | nextfire | auto_mms_pause | 75 | 28 | 6 | 194.93 | 86.02 | 1.060 | 6 |
| bs | nextfire | auto_nf | 75 | 30 | 2 | 175.61 | 74.06 | 1.066 | 5 |
| bs | nextfire | concat | 75 | 34 | 0 | 178.44 | 76.34 | 1.062 | 4 |
| bs | nextfire | fixed_cores | 75 | 35 | 0 | 187.77 | 67.36 | 1.000 | 4 |
| bs | nextfire | full | 75 | 30 | 0 | 183.13 | 57.29 | 1.042 | 3 |
| bs | nextfire | human | 75 | 33 | 0 | 165.91 | 52.23 | 1.020 | 6 |
| bs | nextfire | padded | 75 | 29 | 0 | 192.30 | 77.34 | 1.022 | 5 |
| bs | tifa | auto_mms | 75 | 53 | 6 | 100.84 | -70.93 | 1.056 | 1 |
| bs | tifa | auto_mms_pause | 75 | 51 | 6 | 107.30 | -61.51 | 1.056 | 1 |
| bs | tifa | auto_nf | 75 | 56 | 2 | 101.99 | -66.35 | 1.088 | 1 |
| bs | tifa | concat | 75 | 31 | 3 | 6455.26 | -1806.60 | 0.888 | 15 |
| bs | tifa | fixed_cores | 75 | 34 | 3 | 5454.80 | -1234.52 | 0.908 | 11 |
| bs | tifa | full | 75 | 25 | 3 | 12895.14 | 12459.14 | 0.654 | 32 |
| bs | tifa | human | 75 | 58 | 0 | 92.52 | -57.51 | 1.086 | 1 |
| bs | tifa | padded | 75 | 30 | 5 | 6912.60 | -135.95 | 0.840 | 15 |
| bs_roformer | nextfire | concat | 75 | 34 | 0 | 185.00 | 86.12 | 1.037 | 3 |
| bs_roformer | nextfire | full | 75 | 29 | 0 | 202.87 | 43.43 | 1.028 | 6 |
| bs_roformer | nextfire | padded | 75 | 29 | 0 | 185.84 | 86.95 | 1.056 | 4 |
| demucs | mms_fa | auto_mms | 75 | 13 | 12 | 284.86 | -282.45 | 0.322 | 18 |
| demucs | mms_fa | auto_mms_pause | 75 | 12 | 12 | 280.42 | -274.20 | 0.322 | 18 |
| demucs | mms_fa | auto_nf | 75 | 12 | 4 | 284.68 | -258.31 | 0.333 | 20 |
| demucs | mms_fa | concat | 75 | 15 | 0 | 279.00 | -276.90 | 0.327 | 24 |
| demucs | mms_fa | full | 75 | 16 | 0 | 266.39 | -257.64 | 0.353 | 21 |
| demucs | mms_fa | human | 75 | 13 | 0 | 281.83 | -248.57 | 0.322 | 22 |
| demucs | mms_fa | padded | 75 | 13 | 0 | 277.79 | -275.82 | 0.327 | 22 |
| demucs | nextfire | auto_mms | 75 | 24 | 12 | 202.76 | -9.12 | 0.927 | 7 |
| demucs | nextfire | auto_mms_pause | 75 | 26 | 12 | 178.54 | 74.06 | 1.079 | 4 |
| demucs | nextfire | auto_nf | 75 | 29 | 4 | 183.99 | 64.79 | 0.976 | 5 |
| demucs | nextfire | concat | 75 | 33 | 0 | 177.98 | 68.43 | 1.000 | 4 |
| demucs | nextfire | full | 75 | 27 | 0 | 186.55 | 37.56 | 1.066 | 6 |
| demucs | nextfire | human | 75 | 31 | 0 | 170.31 | 67.96 | 1.000 | 5 |
| demucs | nextfire | padded | 75 | 27 | 0 | 182.85 | 67.65 | 1.000 | 5 |
| demucs | tifa | auto_mms | 75 | 48 | 12 | 109.08 | -69.91 | 1.102 | 1 |
| demucs | tifa | auto_mms_pause | 75 | 50 | 12 | 98.19 | -64.67 | 1.111 | 0 |
| demucs | tifa | auto_nf | 75 | 53 | 4 | 120.18 | -46.90 | 1.102 | 0 |
| demucs | tifa | concat | 75 | 29 | 1 | 8817.43 | -5007.41 | 0.794 | 20 |
| demucs | tifa | full | 75 | 26 | 3 | 13824.78 | 8971.33 | 0.521 | 32 |
| demucs | tifa | human | 75 | 57 | 0 | 98.95 | -60.97 | 1.091 | 1 |
| demucs | tifa | padded | 75 | 31 | 1 | 9403.75 | -4309.07 | 0.800 | 19 |
| dttnet | nextfire | concat | 75 | 32 | 0 | 172.90 | 71.00 | 1.000 | 3 |
| dttnet | nextfire | full | 75 | 37 | 0 | 187.59 | 55.43 | 1.042 | 5 |
| dttnet | nextfire | padded | 75 | 32 | 0 | 229.60 | 15.05 | 1.042 | 5 |
| kim | mms_fa | auto_mms | 75 | 12 | 7 | 274.92 | -267.98 | 0.330 | 18 |
| kim | mms_fa | auto_mms_pause | 75 | 12 | 7 | 269.33 | -262.39 | 0.330 | 19 |
| kim | mms_fa | auto_nf | 75 | 15 | 1 | 270.80 | -251.06 | 0.321 | 21 |
| kim | mms_fa | concat | 75 | 16 | 0 | 301.29 | -301.16 | 0.322 | 21 |
| kim | mms_fa | fixed_cores | 75 | 17 | 0 | 266.93 | -266.77 | 0.327 | 21 |
| kim | mms_fa | full | 75 | 17 | 0 | 269.64 | -269.64 | 0.327 | 22 |
| kim | mms_fa | human | 75 | 16 | 0 | 262.95 | -245.91 | 0.322 | 20 |
| kim | mms_fa | padded | 75 | 16 | 0 | 272.10 | -271.72 | 0.322 | 22 |
| kim | nextfire | auto_mms | 75 | 26 | 7 | 210.50 | -8.27 | 1.017 | 9 |
| kim | nextfire | auto_mms_pause | 75 | 30 | 7 | 170.85 | 70.55 | 1.042 | 5 |
| kim | nextfire | auto_nf | 75 | 30 | 1 | 176.43 | 87.05 | 1.091 | 5 |
| kim | nextfire | concat | 75 | 32 | 0 | 182.17 | 93.50 | 1.072 | 3 |
| kim | nextfire | fixed_cores | 75 | 33 | 0 | 178.86 | 76.16 | 0.973 | 3 |
| kim | nextfire | full | 75 | 25 | 0 | 191.48 | 58.63 | 1.037 | 5 |
| kim | nextfire | human | 75 | 33 | 0 | 172.17 | 40.49 | 1.000 | 5 |
| kim | nextfire | padded | 75 | 28 | 0 | 212.18 | 50.68 | 1.019 | 2 |
| kim | tifa | auto_mms | 75 | 54 | 7 | 101.18 | -62.09 | 1.107 | 1 |
| kim | tifa | auto_mms_pause | 75 | 53 | 7 | 99.03 | -56.95 | 1.107 | 2 |
| kim | tifa | auto_nf | 75 | 57 | 1 | 104.04 | -61.47 | 1.114 | 2 |
| kim | tifa | concat | 75 | 32 | 4 | 5489.55 | -242.86 | 0.886 | 16 |
| kim | tifa | fixed_cores | 75 | 34 | 6 | 4242.49 | -491.86 | 0.909 | 10 |
| kim | tifa | full | 75 | 24 | 2 | 10475.85 | 10152.28 | 0.422 | 31 |
| kim | tifa | human | 75 | 57 | 0 | 94.52 | -52.31 | 1.091 | 1 |
| kim | tifa | padded | 75 | 31 | 4 | 6016.25 | -946.02 | 0.934 | 17 |
| mel_roformer | nextfire | concat | 75 | 33 | 0 | 179.46 | 88.64 | 1.020 | 4 |
| mel_roformer | nextfire | full | 75 | 25 | 0 | 191.21 | 58.36 | 1.042 | 5 |
| mel_roformer | nextfire | padded | 75 | 29 | 0 | 213.94 | 43.61 | 1.066 | 4 |
| scnet | nextfire | concat | 75 | 31 | 0 | 179.36 | 62.50 | 1.000 | 4 |
| scnet | nextfire | full | 75 | 31 | 0 | 184.52 | 54.36 | 1.019 | 5 |
| scnet | nextfire | padded | 75 | 32 | 0 | 228.56 | 8.52 | 1.018 | 5 |
| windowed | nextfire | concat | 75 | 34 | 0 | 175.61 | 89.94 | 1.066 | 3 |
| windowed | nextfire | full | 75 | 29 | 0 | 194.44 | 64.49 | 1.091 | 5 |
| windowed | nextfire | padded | 75 | 34 | 0 | 222.49 | 28.50 | 1.083 | 5 |
| demucs | product | concat | 75 | 34 | 0 | 178.84 | 68.26 | 0.990 | 3 |
| bs | product | concat | 75 | 35 | 0 | 175.47 | 75.25 | 1.040 | 4 |
| kim | product | concat | 75 | 31 | 0 | 181.44 | 90.36 | 1.066 | 3 |

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
| windowed | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 0 | 0 | 104 | 0 |
| windowed | nextfire | padded | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 0 | 0 | 147 | 0 |
| windowed | nextfire | padded | 骹车破尼-假名注音 | teochew_kana | 449 | 265 | 356 | 1 | 23 |
| demucs | product | concat | 003 - 撃槍・ガングニール | primary | 401 | 344 | 370 | 5 | 0 |
| demucs | product | concat | POWDER SNOW (Live Ver.) | primary | 347 | 272 | 311 | 11 | 1 |
| demucs | product | concat | Rainbow Flower | primary | 374 | 269 | 305 | 1 | 15 |
| demucs | product | concat | TSU-BA-SA | primary | 359 | 311 | 344 | 0 | 3 |
| demucs | product | concat | The Brave Under The Summer Sky | primary | 398 | 323 | 377 | 6 | 0 |
| demucs | product | concat | Worlds Pain | primary | 507 | 461 | 494 | 2 | 0 |
| demucs | product | concat | 両翼のBrilliance | primary | 506 | 406 | 458 | 1 | 16 |
| demucs | product | concat | 光陰の海原 | primary | 373 | 288 | 350 | 1 | 0 |
| demucs | product | concat | 恋のルチはや♡ローリング | primary | 402 | 360 | 396 | 0 | 0 |
| demucs | product | concat | 恋桜開花前線 | primary | 496 | 463 | 485 | 2 | 1 |
| demucs | product | concat | 白い季節 | primary | 427 | 398 | 406 | 5 | 0 |
| demucs | product | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 68 | 94 | 4 | 0 |
| demucs | product | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 8 | 24 | 7 | 80 |
| demucs | product | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 330 | 391 | 2 | 9 |
| bs | product | concat | 003 - 撃槍・ガングニール | primary | 401 | 338 | 384 | 0 | 0 |
| bs | product | concat | POWDER SNOW (Live Ver.) | primary | 347 | 285 | 313 | 0 | 1 |
| bs | product | concat | Rainbow Flower | primary | 374 | 284 | 327 | 10 | 2 |
| bs | product | concat | TSU-BA-SA | primary | 359 | 320 | 351 | 0 | 3 |
| bs | product | concat | The Brave Under The Summer Sky | primary | 398 | 314 | 380 | 2 | 0 |
| bs | product | concat | Worlds Pain | primary | 507 | 471 | 490 | 0 | 0 |
| bs | product | concat | 両翼のBrilliance | primary | 506 | 425 | 480 | 0 | 3 |
| bs | product | concat | 光陰の海原 | primary | 373 | 292 | 348 | 1 | 0 |
| bs | product | concat | 恋のルチはや♡ローリング | primary | 402 | 375 | 399 | 0 | 0 |
| bs | product | concat | 恋桜開花前線 | primary | 496 | 461 | 491 | 0 | 0 |
| bs | product | concat | 白い季節 | primary | 427 | 385 | 404 | 1 | 0 |
| bs | product | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 73 | 98 | 1 | 0 |
| bs | product | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 18 | 50 | 6 | 37 |
| bs | product | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 315 | 375 | 2 | 7 |
| kim | product | concat | 003 - 撃槍・ガングニール | primary | 401 | 349 | 381 | 0 | 0 |
| kim | product | concat | POWDER SNOW (Live Ver.) | primary | 347 | 284 | 315 | 1 | 1 |
| kim | product | concat | Rainbow Flower | primary | 374 | 271 | 305 | 1 | 17 |
| kim | product | concat | TSU-BA-SA | primary | 359 | 315 | 349 | 0 | 3 |
| kim | product | concat | The Brave Under The Summer Sky | primary | 398 | 329 | 386 | 2 | 0 |
| kim | product | concat | Worlds Pain | primary | 507 | 466 | 492 | 0 | 0 |
| kim | product | concat | 両翼のBrilliance | primary | 506 | 416 | 472 | 0 | 10 |
| kim | product | concat | 光陰の海原 | primary | 373 | 288 | 339 | 1 | 0 |
| kim | product | concat | 恋のルチはや♡ローリング | primary | 402 | 370 | 397 | 0 | 0 |
| kim | product | concat | 恋桜開花前線 | primary | 496 | 461 | 490 | 0 | 0 |
| kim | product | concat | 白い季節 | primary | 427 | 357 | 403 | 2 | 0 |
| kim | product | concat | 星 (鄧麗君演唱會1982 live) | mixed_japanese | 104 | 80 | 98 | 1 | 0 |
| kim | product | concat | 星 (鄧麗君演唱會1982 live) | mixed_yue_fixed_reading | 147 | 15 | 57 | 4 | 30 |
| kim | product | concat | 骹车破尼-假名注音 | teochew_kana | 449 | 336 | 382 | 2 | 5 |
