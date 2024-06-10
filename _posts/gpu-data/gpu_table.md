### NVIDIA GPU Performance and Efficiency Comparison

**Last Updated**: `June 09, 2024`

||
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|**Rank**|**Model**|**&nbsp;FP32 RPeak&nbsp;<br>(TFlops)**|**&nbsp;Mem Bdw&nbsp;<br>(GB/s)**|**&nbsp;TDP&nbsp;<br>(W)**|**&nbsp;TFlop/Watt&nbsp;**|**&nbsp;Flops/Bdw&nbsp;**|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | NVIDIA RTX 4090 (24GB) | 82.60 | 1008  | 450 | 0.18 | 81.94 |
| 2 | NVIDIA RTX 4080 Super (16GB) | 52.20 | 736  | 320 | 0.16 | 70.92 |
| 3 | NVIDIA RTX 4080 (16GB) | 48.70 | 717  | 320 | 0.15 | 67.92 |
| 4 | NVIDIA RTX 4070 Ti Super (16GB) | 44.00 | 672  | 285 | 0.15 | 65.48 |
| 5 | NVIDIA RTX 3090 Ti (24GB) | 40.00 | 1008  | 450 | 0.09 | 39.68 |
| 6 | NVIDIA RTX 4070 Ti (12GB) | 40.00 | 504  | 285 | 0.14 | 79.37 |
| 7 | NVIDIA RTX 3090 (24GB) | 35.60 | 936  | 350 | 0.10 | 38.03 |
| 8 | NVIDIA RTX 4070 Super (12GB) | 35.48 | 504  | 220 | 0.16 | 70.40 |
| 9 | NVIDIA RTX 3080 Ti (12GB) | 34.10 | 912  | 350 | 0.10 | 37.39 |
| 10 | NVIDIA RTX 3080 (12GB) | 30.64 | 912  | 350 | 0.09 | 33.60 |
|**Rank**|**Model**|**&nbsp;FP32 RPeak&nbsp;**|**&nbsp;Mem Bdw&nbsp;**|**&nbsp;TDP&nbsp;**|**&nbsp;TFlop/Watt&nbsp;**|**&nbsp;Flops/Bdw&nbsp;**|
| 11 | NVIDIA RTX 3080 (10GB) | 29.77 | 760  | 320 | 0.09 | 39.17 |
| 12 | NVIDIA RTX 4070 (12GB) | 29.15 | 504  | 200 | 0.15 | 57.84 |
| 13 | NVIDIA RTX 4060 Ti (16GB) | 22.06 | 288  | 165 | 0.13 | 76.60 |
| 14 | NVIDIA RTX 4060 Ti (8GB) | 22.06 | 288  | 160 | 0.14 | 76.60 |
| 15 | NVIDIA RTX 3070 Ti (8GB) | 21.70 | 608  | 290 | 0.07 | 35.69 |
| 16 | NVIDIA RTX 3070 (8GB) | 20.30 | 448  | 220 | 0.09 | 45.31 |
| 17 | NVIDIA RTX 4060 (8GB) | 18.90 | 288  | 115 | 0.16 | 65.62 |
| 18 | NVIDIA RTX 3060 Ti (8GB) | 16.20 | 448  | 200 | 0.08 | 36.16 |
| 19 | NVIDIA RTX 4050 (6GB) | 13.52 | 216  | 150 | 0.09 | 62.59 |
| 20 | NVIDIA RTX 3060 (12GB) | 12.70 | 360  | 170 | 0.07 | 35.28 |
|**Rank**|**Model**|**&nbsp;FP32 RPeak&nbsp;**|**&nbsp;Mem Bdw&nbsp;**|**&nbsp;TDP&nbsp;**|**&nbsp;TFlop/Watt&nbsp;**|**&nbsp;Flops/Bdw&nbsp;**|
| 21 | NVIDIA RTX 3050 (8GB) | 9.10 | 224  | 130 | 0.07 | 40.62 |
| 22 | NVIDIA RTX 3050 (4GB) | 7.13 | 192  | 90 | 0.08 | 37.12 |
| 23 | NVIDIA RTX 3050 (6GB) | 6.77 | 168  | 70 | 0.10 | 40.32 |
||

### Understanding the Metrics

- **Rank**: GPUs are ranked primarily by FP32 Flop, then by bandwidth, and finally by inverse of TDP.
- **FP32 TFlops**: Single precision floating-point operations per second in teraflops.
- **Bandwidth (GB/s)**: Memory bandwidth in GB/s.
- **TDP (W)**: Thermal Design Power in watts.
- **Flop/W**: TFlop per watt. Higher is better.
- **Flop/Bdw**: Flop per unit of bandwidth. Lower is better
