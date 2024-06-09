---
layout: post
title:  Rank of GPU performance 
date:   2024-06-9 0:00:00
description: Why NVIDIA doesn't offer such simple comparision chart? 
tags: hpc
categories: personal_posts
---


## NVIDIA GPU Performance Comparison

| Rank | Model | FP32 RPeak<br>(TFlops) | Mem Bdw<br>(GB/s) | VRAM<br>(GB) | GFlops/bdw |
|:------:|-------------|:----:|:----:|:----:|:----:|
| 1 | NVIDIA RTX 4090 | 82.6 | 1,008 | 24 | 82.0 |
| 2 | NVIDIA RTX 4080 Super | 52.2 | 736 | 16 | 70.9 |
| 3 | NVIDIA RTX 4080 | 48.7 | 717 | 16 | 67.9 |
| 4 | NVIDIA RTX 4070 Ti Super | 44.0 | 672* | 16* | 65.5* |
| 5 | NVIDIA RTX 4070 Ti | 40.0 | 504 | 12 | 79.4 |
| 5 | NVIDIA RTX 3090 Ti | 40.0 | 1,008 | 24 | 39.7 |
| 6 | NVIDIA RTX 3090 | 35.6 | 936 | 24 | 38.0 |
| 7 | NVIDIA RTX 3080 Ti | 34.1 | 912 | 12 | 37.4 |
| 8 | NVIDIA RTX 3080 | 29.8 | 760 / 912 | 10 / 12 | 39.2 / 32.7 |
| 9 | NVIDIA RTX 4070 | 29.15 | 504 | 12 | 57.8 |
| 10 | NVIDIA RTX 4060 Ti | 22.4 | 288 | 8 / 16 | 77.8 |
| 11 | NVIDIA RTX 3070 Ti | 21.7 | 608 | 8 | 35.7 |
| 12 | NVIDIA RTX 3070 | 20.3 | 448 | 8 | 45.3 |
| 13 | NVIDIA RTX 4060 | 18.9 | 288 | 8 | 65.6 |
| 14 | NVIDIA RTX 3060 Ti | 16.2 | 448 | 8 | 36.2 |
| 15 | NVIDIA RTX 3060 | 12.7 | 360 | 12 | 35.3 |


**Notes:**
- FP32 performance is theoretical peak. Real-world performance may vary.
- Memory bandwidth can significantly impact performance in memory-intensive tasks.
- Other factors like VRAM size, ray tracing performance, and power efficiency are also important.


