# 实测数据 / Field-Test Data

> 全部为作者在《Squad》内逐点实测的落点。格式：**输入(距离 高差) → 落点(距离 高差)**，误差 = 落点距离 − 输入距离（正=打远，负=打近）。
> All points were field-tested by the author in Squad. Format: **input(distance height) → impact(distance height)**, error = impact − input (+ = long, − = short).

> 说明：部分数据标注了「修正前/修正后」。修正前是拟合过程中的中间值，修正后是最终定案；最终以「✅ 准 / 定案」为准。
> Note: some rows are marked "before/after fix". "Before" are intermediate values during fitting; "after" are final. Trust the ✅ / final rows.

---

## 1. AGS-17 光瞄 · 低抛 / AGS-17 Optical · Low trajectory

| 输入 Input | 落点 Impact | 误差 Error | 状态 |
|---|---|---|---|
| 771.9 / −63.8 | 925.8 / −63.8 | +154 m | ⚠️ 修正前（线性高差崩了） |
| 771.9 / −63.8 | ≈准 | ≈0 | ✅ 修正后（物理反推高差） |
| 492.4 / −23.4 | 准 | 0 | ✅ |
| 510.2 / +21.0 | 503.1 / +19.4 | −7.1 m | ⚠️ 略近（正高差小残差） |
| 905.9 / +30.3 | 准 | 0 | ✅ |
| 1540.5 / −56.6 | 准 | 0 | ✅ |
| 1500 / 0 | 准 | 0 | ✅ |

## 2. AGS-17 光瞄 · 高抛 / AGS-17 Optical · High trajectory

| 输入 Input | 落点 Impact | 误差 Error | 状态 |
|---|---|---|---|
| 960.7 / −74.7 | 准 | 0 | ✅ |
| 871.8 / −69.1 | 准 | 0 | ✅ |

## 3. AGS-17 碉堡化 · 高抛（dy 规律）/ AGS-17 Bunker · High (dy rule)

> 从最上沿（1255m 瞄点）往下压 dy 的实测规律。The dy rule measured by pulling down from the top edge (1255m aim point).

| 下移 dy | 落点 Impact | 高差 Height | 状态 |
|---|---|---|---|
| 0（最上沿） | 1255 m | 0 | ✅ 锚点 |
| 70 | 1410 m | 0 | ✅ |
| 140 | 1550 m | +4.9 | ✅ |
| 210 | 1680 m | +0.6 | ✅ |
| 280 | 1785 m | −0.4 | ✅ |

## 4. AGS-17 碉堡化 · 高抛 最远段 / AGS-17 Bunker · High (max range)

| 条件/输入 Condition/Input | 结果 Result | 状态 |
|---|---|---|
| 86.1° 下移 389dy（最顶部可发射） | 1180 m | ✅ 最小射程锚点 |
| 2040 / 0 | 1940 m | ⚠️ 修正前（外推过头） |
| 1950 / 0 | 1910 m | ⚠️ 修正前 |
| 最远 Max range | 1950 m | ✅ 定案封顶 |

## 5. AGS-17 碉堡化 · 低抛 / AGS-17 Bunker · Low trajectory

| 输入 Input | 落点 Impact | 误差 Error | 状态 |
|---|---|---|---|
| 1950 / 0 | 1910 / −5.2 | −40 m | ⚠️ 修正前 |
| 1940 / 0 | 1905 / −8.0 | −35 m | ⚠️ 修正前 |
| 1785 / 0 | 1780 / +1.8 | −5 m | ✅ |
| 1680 / 0 | 1686 | +6 m | ✅ |
| 1500 / 0 | 准 | 0 | ✅ |

## 6. AGS-17 碉堡化 · 最大俯角 / AGS-17 Bunker · Max depression

| 条件 Condition | 落点 Impact |
|---|---|
| 最大俯角开火 Max depression | 339.7 / −75.9 |

## 7. Mk19（含碉堡化）/ Mk19 (incl. bunker)

| 输入 Input | 落点 Impact | 状态 |
|---|---|---|
| 1463.2 / −71.9 | 准 | ✅ |

## 8. QLZ-87（含碉堡化）/ QLZ-87 (incl. bunker)

| 输入 Input | 落点 Impact | 状态 |
|---|---|---|
| 1463.2 / −71.9 | 准 | ✅ |

---

## 汇总 / Summary

| 项 Item | 精度 Accuracy |
|---|---|
| 低抛平射 300~1930m Low flat | ≈ ±2 m |
| 高抛平射 1180~1940m High flat | ≈ ±6 m |
| 大高差（任意轨迹）Large height diff | ≈ ±7~15 m |

> 已知待验证 Known gaps：AGS 高抛大高差、AGS 碉堡化大高差、MK19/QLZ 大高差、低抛 300m 以内与极远端。
> Still to verify: AGS high-trajectory large height diff, AGS bunker large height diff, MK19/QLZ large height diff, low trajectory below 300m and extreme far end.

---

> ⚠️ **注意事项 / Note**：数据全部由本人手动测量，AI（DeepSeek）进行运算，误差是无可避免的。
> ⚠️ **Note**: All data was manually measured by the author and computed by AI (DeepSeek); errors are unavoidable.
