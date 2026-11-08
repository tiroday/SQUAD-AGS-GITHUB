# 使用指南 / Usage Guide

> 自由开源软件（GPL v3.0）。Free & open-source software (GPL v3.0).

---

## 1. 安装 / Installation

1. 安装 **Python 3.12 或更高**（Windows 安装时勾选 "Add Python to PATH"）。
2. 打开命令行，进入本目录，安装依赖：
   ```
   pip install -r requirements.txt
   ```
   （需要 Pillow、pynput、pytweening 三个包，详见 requirements.txt。）

1. Install **Python 3.12+** (on Windows, tick "Add Python to PATH").
2. In a terminal, cd to this folder and run:
   ```
   pip install -r requirements.txt
   ```
   (Needs three packages: Pillow, pynput, pytweening — see requirements.txt.)

---

## 2. 启动 / Launch

- 双击 `AGS_CH.pyw`（中文界面）或 `AGS_EN.pyw`（英文界面），或命令行运行 `pythonw AGS_CH.pyw` / `pythonw AGS_EN.pyw`。
- Double-click `AGS_CH.pyw` (Chinese UI) or `AGS_EN.pyw` (English UI), or run `pythonw AGS_CH.pyw` / `pythonw AGS_EN.pyw`.

---

## 3. 界面 / Interface

| 项 Item | 说明 Note |
|---|---|
| 武器 Weapon | Mk19 / AGS-17 / QLZ-87 |
| 弹道 Trajectory | 低抛 Low / 高抛 High（只有 AGS-17 有高抛） |
| 基准 Base | 标准态(0°) / 最大仰角 / 最大俯角（部分武器有 300m 归零） |
| 碉堡化 Bunker | 勾选后切换到机瞄独立数据（AGS-17），或锁定基准（QLZ/Mk19） |
| 距离 Distance | 米 m |
| 高差 Height | 米 m；目标在上为正 +，在下为负 − |
| 当前/目标方位 Azimuth | 度 °，用于水平方向瞄准 |

---

## 4. 瞄准流程 / Aiming Flow

1. 选好武器、弹道、基准（需要时勾碉堡化）。
2. 输入距离、高差（方位角可选）。
3. 按 **F7** 开始追踪。
4. 屏幕中央会出现**绿点 + 十字线**；**移动鼠标，让绿点回到屏幕中心的十字线处**。
5. 绿点在中心 = 炮口已抬到正确仰角，直接开火。
6. 按 **F8** 停止追踪。

1. Choose weapon, trajectory and base (tick "碉堡化/bunker" if needed).
2. Enter distance and height (azimuth optional).
3. Press **F7** to start tracking.
4. A **green dot + crosshair** appears; **move the mouse until the green dot returns to the screen-center crosshair**.
5. Green dot centered = barrel is at the correct elevation; fire.
6. Press **F8** to stop.

---

## 5. 散布 / 覆盖模式 Spread Mode

- 按**散布键**（默认 **F9**）切换。
- 覆盖模式下显示以绿点为中心的**散布线**，表示爆炸覆盖半径。
- 覆盖半径可在「自定义 → 武器杀伤范围」里改。
- Press the **spread key** (default **F9**) to toggle.
- Spread mode shows a **spread line** around the green dot, representing the blast coverage radius.
- Coverage radius can be changed in "Customize → weapon kill range".

---

## 6. 基准态说明 / Base Mode

> 基准态 = 开火前先把炮口放到哪个"参考角"，工具再从这个参考角算出你需要压/抬多少鼠标。
> Base mode = the reference angle you set the barrel to before firing; the tool then computes how much to adjust from there.

| 基准 Base | 说明 Note |
|---|---|
| 标准态 Standard | 武器的默认归零基准角，不同武器不同：AGS-17 光瞄 = 0°、AGS-17 碉堡机瞄 = 3.57°、QLZ-87 = 2.10°、Mk19 = 0° |
| 300m 归零 300m zero（Mk19 专属 only） | 把瞄具归零到 300m：300m 处弹道与准星重合，以此为基准计算 |
| 最大仰角 Max elevation | 先把炮口抬到最高仰角，再往下压瞄准（适合高抛/远距离） |
| 最大俯角 Max depression | 先把炮口压到最低俯角，再往上抬瞄准 |

> 各武器的默认标准态角度：The default standard angle per weapon: AGS-17 光瞄 0° / AGS-17 碉堡 3.57° / QLZ-87 2.10° / Mk19 0°（另有 300m 归零选项）。

---

## 7. 碉堡化说明 / Bunker Mode

| 武器 Weapon | 碉堡化行为 Bunker behavior |
|---|---|
| AGS-17 | 换用机瞄独立数据（px/max_el/低抛最远段/高抛五次式），基准随弹道自动：低抛→标准态，高抛→最大仰角 |
| Mk19 | 数据不变，基准态可选 {标准态, 最大仰角} |
| QLZ-87 | 数据不变，基准态锁定标准态 |

---

## 8. 校准（重要！）/ Calibration (Important!)

- **px（每度像素）是"玩家专属"的**，取决于游戏内灵敏度和 FOV。
- 作者是按 `SETTINGS.md` 里的设置校准的；**其他玩家如果灵敏度/FOV 不同，需要重算 px**，否则会偏。
- **必须禁用**：游戏内"鼠标平滑" + Windows"提高指针精确度"（否则工具读到的鼠标计数和游戏对不上）。
- **px is player-specific**: it depends on in-game sensitivity and FOV.
- The author calibrated with the settings in `SETTINGS.md`; **other players with different sensitivity/FOV must recalibrate px**, or shots will drift.
- **Must disable**: in-game "Mouse Smoothing" + Windows "Enhance pointer precision" (otherwise the raw mouse counts won't match the game).

---

## 9. 常见问题 / FAQ

- **绿点到了中心但没打准？** → 检查灵敏度/FOV 是否和 `SETTINGS.md` 一致，鼠标平滑/指针加速是否关了。
- **显示"无法打到（超射程）"？** → 距离超出该武器最大射程，或仰角超出上下限。
- **"Green dot centered but shots miss?"** → check sensitivity/FOV matches `SETTINGS.md`, and smoothing/acceleration are off.
- **"Unreachable (out of range)?"** → distance exceeds max range, or elevation out of limits.
