# Comparisons using absolute values

## Device - EArch_tseng
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 0.18   | `0.09` | 0.10   | 0.10   | `0.09` |
| lookahead          | 0.37   | `0.10` | `0.10` | `0.10` | `0.10` |
| packing            | 0.67   | `0.66` | 0.69   | 0.67   | `0.66` |
| placement          | `0.28` | `0.28` | 0.30   | `0.28` | `0.28` |
| rr_graph delta_rss | 10.80  | 10.60  | 10.90  | `6.70` | 12.70  |
| max_rss            | 46.40  | 46.30  | 46.60  | `42.70`| 48.10  |
| entire flow        | 1.85   | `1.43` | 1.49   | 1.45   | 1.45   |
## Device - k6_arm_core
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 9.71   | `3.43` | 3.72   | 3.69   | `3.43` |
| lookahead          | 6.86   | `1.87` | 1.96   | 1.98   | 1.89   |
| packing            | 16.31  | 16.17  | 16.75  | 16.39  | `16.04`|
| placement          | 9.03   | 9.02   | 9.27   | 9.20   | `9.00` |
| rr_graph delta_rss | 191.90 | 182.20 | 190.90 | `97.70`| 222.10 |
| max_rss            | 387.00 | 377.70 | 386.50 | `293.30`| 417.20 |
| entire flow        | 47.07  | `34.23`| 35.38  | 35.18  | 34.24  |
## Device - stratixiv_cholesky
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 209.86 | 68.65  | 74.62  | 74.81  | `66.46`|
| lookahead          | 369.29 | 84.16  | 85.45  | 98.61  | `82.14`|
| packing            | 92.40  | 90.81  | 91.17  | 91.93  | `90.22`|
| placement          | 124.24 | 119.67 | 121.34 | `119.29`| 121.59 |
| rr_graph delta_rss | 4459.40| 4038.60| 4466.60| `2978.10`| 4808.00|
| max_rss            | 6619.90| 6199.30| 6613.00| `5138.80`| 6940.00|
| entire flow        | 1153.38| 510.30 | 533.28 | 550.15 | `508.49`|
## Device - directrf
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            |        | 1149.03| 1283.94| 1242.76| 1112.68|
| lookahead          |        | 708.90 | 738.25 | 804.25 | 688.91 |
| packing            | 811.01 | `796.17`| 800.25 | 820.92 | 799.62 |
| placement          |        | 5482.71| 5444.56| 5344.02| 5458.91|
| rr_graph delta_rss |        | 22366.60| 25132.20| 15070.50| 27123.10|
| max_rss            |        | 38746.20| 41510.70| 31449.80| 43575.20|
| entire flow        |        | 9270.08| 9506.01| 9449.42| 9189.60|
----
# SymbiFlow
## Device - minilitex_arty
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 491.20 | 173.54 | 178.19 | 199.23 | `169.80`|
| lookahead          |        |        |        |        |        |
| packing            | 31.81  | `30.39`| 32.21  | 32.53  | 31.00  |
| placement          | 19.56  | 19.44  | `19.31`| 19.59  | 19.38  |
| rr_graph delta_rss | 3151.70| 3443.10| 3150.10| `2777.00`| 3185.80|
| max_rss            | 3389.20| 3680.40| 3387.40| `3014.60`| 3423.30|
| entire flow        | 565.87 | 237.60 | 242.30 | 279.57 | `230.73`|
## Device - picosoc_basys3_full_50
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 86.90  | `42.72`| 43.52  | 50.88  | 42.82  |
| lookahead          |        |        |        |        |        |
| packing            | 21.67  | `20.99`| 21.94  | 22.00  | 21.29  |
| placement          | 11.04  | 11.15  | 11.15  | `10.99`| 11.27  |
| rr_graph delta_rss | 3187.90| 3478.90| 3185.80| `2813.20`| 3221.40|
| max_rss            | 3362.10| 3652.10| 3358.90| `2986.50`| 3394.80|
| entire flow        | 141.36 | 87.96  | 87.93  | 110.86 | `84.90`|
## Device - picosoc_basys3_full_100
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 275.79 | 109.80 | 112.57 | 125.49 | `109.43`|
| lookahead          |        |        |        |        |        |
| packing            | 21.22  | `20.34`| 21.47  | 21.54  | 20.75  |
| placement          | 14.23  | `13.56`| 13.64  | 13.71  | 13.88  |
| rr_graph delta_rss | 3188.20| 3479.40| 3185.90| `2813.50`| 3221.80|
| max_rss            | 3361.60| 3652.90| 3359.20| `2986.70`| 3395.40|
| entire flow        | 333.09 | 156.81 | 159.20 | 187.85 | `153.57`|
## Device - linux_arty
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 815.58 | `282.45`| 298.37 | 311.91 | 283.89 |
| lookahead          |        |        |        |        |        |
| packing            | 98.61  | `95.35`| 99.90  | 99.60  | 96.69  |
| placement          | 63.49  | `62.21`| 64.52  | 62.39  | 63.22  |
| rr_graph delta_rss | 2916.20| 3206.80| 2914.10| `2545.30`| 2948.30|
| max_rss            | 3513.10| 3803.80| 3511.10| `3142.10`| 3545.20|
| entire flow        | 1011.13| `463.27`| 484.33 | 510.82 | 466.86 |

# Comparisons using flat as the baseline (negative percentages mean the value is smaller than flat)

## Device - EArch_tseng
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 100.00%| `0.00%`| 11.11% | 11.11% | `0.00%`|
| lookahead          | 270.00%| `0.00%`| `0.00%`| `0.00%`| `0.00%`|
| packing            | 1.52%  | `0.00%`| 4.55%  | 1.52%  | `0.00%`|
| placement          | `0.00%`| `0.00%`| 7.14%  | `0.00%`| `0.00%`|
| rr_graph delta_rss | -14.96%| -16.54%| -14.17%| `-47.24%`| 0.00%  |
| max_rss            | -3.53% | -3.74% | -3.12% | `-11.23%`| 0.00%  |
| entire flow        | 27.59% | `-1.38%`| 2.76%  | 0.00%  | 0.00%  |
## Device - k6_arm_core
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 183.09%| `0.00%`| 8.45%  | 7.58%  | `0.00%`|
| lookahead          | 262.96%| `-1.06%`| 3.70%  | 4.76%  | 0.00%  |
| packing            | 1.68%  | 0.81%  | 4.43%  | 2.18%  | `0.00%`|
| placement          | 0.33%  | 0.22%  | 3.00%  | 2.22%  | `0.00%`|
| rr_graph delta_rss | -13.60%| -17.96%| -14.05%| `-56.01%`| 0.00%  |
| max_rss            | -7.24% | -9.47% | -7.36% | `-29.70%`| 0.00%  |
| entire flow        | 37.47% | `-0.03%`| 3.33%  | 2.75%  | 0.00%  |
## Device - stratixiv_cholesky
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 215.77%| 3.30%  | 12.28% | 12.56% | `0.00%`|
| lookahead          | 349.59%| 2.46%  | 4.03%  | 20.05% | `0.00%`|
| packing            | 2.42%  | 0.65%  | 1.05%  | 1.90%  | `0.00%`|
| placement          | 2.18%  | -1.58% | -0.21% | `-1.89%`| 0.00%  |
| rr_graph delta_rss | -7.25% | -16.00%| -7.10% | `-38.06%`| 0.00%  |
| max_rss            | -4.61% | -10.67%| -4.71% | `-25.95%`| 0.00%  |
| entire flow        | 126.82%| 0.36%  | 4.88%  | 8.19%  | `0.00%`|
## Device - directrf
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            |        | 3.27%  | 15.39% | 11.69% | 0.00%  |
| lookahead          |        | 2.90%  | 7.16%  | 16.74% | 0.00%  |
| packing            | 1.42%  | `-0.43%`| 0.08%  | 2.66%  | 0.00%  |
| placement          |        | 0.44%  | -0.26% | -2.10% | 0.00%  |
| rr_graph delta_rss |        | -17.54%| -7.34% | -44.44%| 0.00%  |
| max_rss            |        | -11.08%| -4.74% | -27.83%| 0.00%  |
| entire flow        |        | 0.88%  | 3.44%  | 2.83%  | 0.00%  |
---
# SymbiFlow
## Device - minilitex_arty
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 189.28%| 2.20%  | 4.94%  | 17.33% | `0.00%`|
| lookahead          |        |        |        |        |        |
| packing            | 2.61%  | `-1.97%`| 3.90%  | 4.94%  | 0.00%  |
| placement          | 0.93%  | 0.31%  | `-0.36%`| 1.08%  | 0.00%  |
| rr_graph delta_rss | -1.07% | 8.08%  | -1.12% | `-12.83%`| 0.00%  |
| max_rss            | -1.00% | 7.51%  | -1.05% | `-11.94%`| 0.00%  |
| entire flow        | 145.25%| 2.98%  | 5.01%  | 21.17% | `0.00%`|
## Device - picosoc_basys3_full_50
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 102.94%| `-0.23%`| 1.63%  | 18.82% | 0.00%  |
| lookahead          |        |        |        |        |        |
| packing            | 1.78%  | `-1.41%`| 3.05%  | 3.33%  | 0.00%  |
| placement          | -2.04% | -1.06% | -1.06% | `-2.48%`| 0.00%  |
| rr_graph delta_rss | -1.04% | 7.99%  | -1.11% | `-12.67%`| 0.00%  |
| max_rss            | -0.96% | 7.58%  | -1.06% | `-12.03%`| 0.00%  |
| entire flow        | 66.50% | 3.60%  | 3.57%  | 30.58% | `0.00%`|
## Device - picosoc_basys3_full_100
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 152.02%| 0.34%  | 2.87%  | 14.68% | `0.00%`|
| lookahead          |        |        |        |        |        |
| packing            | 2.27%  | `-1.98%`| 3.47%  | 3.81%  | 0.00%  |
| placement          | 2.52%  | `-2.31%`| -1.73% | -1.22% | 0.00%  |
| rr_graph delta_rss | -1.04% | 8.00%  | -1.11% | `-12.67%`| 0.00%  |
| max_rss            | -1.00% | 7.58%  | -1.07% | `-12.04%`| 0.00%  |
| entire flow        | 116.90%| 2.11%  | 3.67%  | 22.32% | `0.00%`|
## Device - linux_arty
| category |nodes_all_attr_binary_search|switches_subsets|nodes_all_attr|edge_switch_subsets|flat|
|---|---|---|---|---|---|
| routing            | 187.29%| `-0.51%`| 5.10%  | 9.87%  | 0.00%  |
| lookahead          |        |        |        |        |        |
| packing            | 1.99%  | `-1.39%`| 3.32%  | 3.01%  | 0.00%  |
| placement          | 0.43%  | `-1.60%`| 2.06%  | -1.31% | 0.00%  |
| rr_graph delta_rss | -1.09% | 8.77%  | -1.16% | `-13.67%`| 0.00%  |
| max_rss            | -0.91% | 7.29%  | -0.96% | `-11.37%`| 0.00%  |
| entire flow        | 116.58%| `-0.77%`| 3.74%  | 9.42%  | 0.00%  |

# Tables with updated results

## nodes_all_attr results for several benchmarks
![nodes_all_attr](https://user-images.githubusercontent.com/55202333/159975133-dc5718ed-17a7-4821-925c-6dc30fa7fc2b.PNG)

## switches_subsets results for several benchmarks
![switches_subsets](https://user-images.githubusercontent.com/55202333/159975083-a943647c-a40b-4cf2-90b4-692fbc8622f9.PNG)

## dest_switch_subsets results for several benchmarks
![dest_switch_subsets](https://user-images.githubusercontent.com/55202333/159974161-ce0c6642-73e0-48b6-8095-2216fa4b3390.PNG)

## nodes_edges results for several benchmarks
![nodes_edges](https://user-images.githubusercontent.com/55202333/159974983-f2ff8b21-2553-41ba-9929-0f492f85de54.PNG)

## F4PGA Folded Devices Sizes
![f4pga_sizes](https://user-images.githubusercontent.com/55202333/159974973-1650538d-2e23-45f2-b452-654b46ed1696.PNG)


