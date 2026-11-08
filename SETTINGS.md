# 设置参数 / Settings

> 以下为作者校准本工具时的游戏与系统设置。**其他玩家必须保持一致**，否则 px（每度像素）会变，瞄准会偏。
> The following are the author's in-game & system settings used to calibrate this tool. **Other players MUST match them**, or px (pixels-per-degree) changes and aiming drifts.

---

## 视角 / Field of View

| 项 Item | 值 Value |
|---|---|
| FOV | **100** |

---

## 基础灵敏度 / Base Sensitivity

| 项 Item | 值 Value |
|---|---|
| 全局灵敏度 Global Sensitivity | **1.00** |
| 自由观看灵敏度 Free-look Sensitivity | **1.00** |
| 稳定瞄准灵敏度 Aim Sensitivity | **0.40** |

---

## 直升机灵敏度 / Helicopter Sensitivity

| 项 Item | 值 Value |
|---|---|
| 反转直升机俯仰（鼠标 Y 轴）Invert Heli Pitch (mouse Y) | **未勾选 / Unchecked** |
| 直升机俯仰灵敏度 Heli Pitch Sensitivity | **1.00** |
| 直升机滚转灵敏度 Heli Roll Sensitivity | **1.00** |

---

## 士兵灵敏度倍数 / Soldier Sensitivity Multiplier

| 倍率 Zoom | 值 Value |
|---|---|
| 指向性射击（腰射）Point-fire (hip) | **1.00** |
| 非放大瞄准镜 Non-magnified scope | **1.00** |
| 2 倍 2× | **0.50** |
| 3 倍 3× | **0.33** |
| 4 倍 4× | **0.25** |
| 6 倍 6× | **0.17** |
| 8 倍 8× | **0.13** |
| 12 倍 12× | **0.08** |

---

## 载具灵敏度乘数 / Vehicle Sensitivity Multiplier

| 倍率 Zoom | 值 Value |
|---|---|
| 载具灵敏度 Vehicle Sensitivity | **1.00** |
| 1 倍 1× | **1.00** |
| 4 倍 4× | **0.50** |

---

## 必须禁用的项 / Must-Disable

| 项 Item | 位置 Where | 说明 Note |
|---|---|---|
| 鼠标平滑 Mouse Smoothing | 游戏内设置 | 会导致游戏准星移动与工具读到的原始鼠标计数不一致 |
| 提高指针精确度 Enhance pointer precision | Windows 设置 → 鼠标 → 指针选项 | 即"鼠标加速"，会导致非线性移动 |

以上两项**必须关闭**，否则工具的 Raw Input 读到的计数与游戏实际视角转动对不上（表现为"绿点到了但没打准"）。

Both items MUST be off. Otherwise the tool's Raw Input counts won't match the game's actual view rotation (symptom: "green dot aligned but shots miss").
