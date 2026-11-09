MK19位置图-软件工作图-射击落点图<img width="2553" height="1593" alt="2fa14568c6b3787a0ace56b90ce035f4" src="https://github.com/user-attachments/assets/1e08fa6b-9fda-43e7-a6e9-433f6b312ec3" />
<img width="2532" height="1434" alt="64ed31fe7d5b48f5d1e3141a3cf6a9a0" src="https://github.com/user-attachments/assets/6d3eec80-f25b-46f2-834a-918a2dd73afc" />
<img width="2559" height="1599" alt="b40d6a1fc1ac8b06e128dcd618aeb20f" src="https://github.com/user-attachments/assets/a5dbd021-9f99-4609-998c-0012708193bc" />
AGS-17位置图-软件工作图-射击落点图<img width="2559" height="1599" alt="a5bd1a6446a21868c4ebc87421b291a7" src="https://github.com/user-attachments/assets/ba15a1fb-637a-4fbb-851c-b20757c4a671" />
<img width="2559" height="1455" alt="e7f3fb1e158566bb34d85405a03a2a30" src="https://github.com/user-attachments/assets/88a8c6a9-1946-4321-93a7-32ac84ebb1f3" />
<img width="2559" height="1461" alt="4bc627a7ce99a3c6237182183809cc78" src="https://github.com/user-attachments/assets/9bb44978-9e0e-4753-a14e-72ea226426dc" />
<img width="2559" height="1599" alt="10a9530303ce906df9a90ece9241ff76" src="https://github.com/user-attachments/assets/69f32abe-56bf-472a-bee2-f8de30d635e1" />
QLZ-87位置图-软件工作图-射击落点图<img width="2559" height="1599" alt="a728fda616f153c6be6b9cd8f1de4098" src="https://github.com/user-attachments/assets/a8f76c01-2b46-4bbe-9632-6f1a13f35caa" />
<img width="2559" height="1466" alt="1a3291c9d75a98a951419418ff83fb9d" src="https://github.com/user-attachments/assets/7381d31b-3dc6-49c3-9e4b-52725a9dfed9" />
<img width="2559" height="1457" alt="1cc600b8017a2db45db4b6fe05ddb0d9" src="https://github.com/user-attachments/assets/83494304-1b1e-4b4d-8110-396d26bdc370" />
<img width="2559" height="1599" alt="e8b054d7e49cabfb0e239d169102e9e5" src="https://github.com/user-attachments/assets/01628de2-f6ef-433f-a70c-b8efc4bcf9b1" />


# Squad 终极准星 / Squad Ultimate Crosshair

> **自由开源软件（GPL v3.0）。** — **Free & open-source software (GPL v3.0).**

一个针对《Squad》的榴弹发射器 / 迫击炮弹道瞄准工具：输入距离与高差，自动算出目标仰角，并在屏幕覆盖层画出绿点，告诉你鼠标往哪挪。

A ballistic aiming tool for Squad's grenade launchers / mortars: enter distance & height difference, and it computes the elevation and draws a green dot overlay showing where to aim.

> ⚠️ **最终版声明**：本项目已是最终版本。由于学业原因，作者将不再更新，后续维护只能依赖后来者 / 社区贡献者。
> ⚠️ **Final version notice**: This is the FINAL version. Due to academic commitments, the author will no longer update it; future maintenance depends entirely on later contributors / the community.

---

## 项目来源 / Origin

- **作者 Author**： tiroday（GitHub）
- **实测数据**：作者在游戏内逐点实测落点（数据见 `TEST_DATA.md`）。
- **弹道拟合**：由 **DeepSeek** 根据实测数据拟合弹道函数。
- **Field-test data**: measured in-game by the author (see `TEST_DATA.md`).
- **Ballistic fitting**: performed by **DeepSeek** based on the field-test data.

---

## 支持的武器 / Supported Weapons

| 武器 Weapon | 弹道 Trajectory | 碉堡化 Bunker mode |
|---|---|---|
| Mk19 | 低抛 Low | ✅ 基准态可选 |
| AGS-17 | 低抛/高抛 Low/High | ✅ 独立机瞄数据 |
| QLZ-87 | 低抛 Low | ✅ 锁定标准态 |

---

## 使用说明 / Usage

1. 运行 `AGS_CH.pyw`（中文界面）或 `AGS_EN.pyw`（英文界面）（需 Python 3.12 + `pip install pillow pynput pytweening`）。
2. 选择武器、弹道（低抛/高抛）、是否碉堡化。
3. 输入距离（米）和高差（米，目标在上为正 +、在下为负 −）。
4. 按 **F7** 开始追踪，屏幕出现绿点；移动鼠标使绿点回到屏幕中心（十字线处），即完成瞄准。
5. **F8** 停止；散布键（默认 **F9**）切换覆盖模式。

1. Run `AGS_CH.pyw` (Chinese UI) or `AGS_EN.pyw` (English UI) (requires Python 3.12 + `pip install pillow pynput pytweening`).
2. Select weapon, trajectory (low/high), and bunker mode if needed.
3. Enter distance (m) and height difference (m; + for higher, − for lower target).
4. Press **F7** to start tracking; move the mouse until the green dot returns to the screen center (the crosshair).
5. **F8** stops; the spread key (default **F9**) toggles cover mode.

---

## 设置与校准 / Settings & Calibration

以下为作者的校准设置（**供参考**）。如果你的设置不同，**不必强行一致**——按 `USAGE.md` 里的校准方法重新校准 px（每度像素）即可。

These are the author's calibration settings (**for reference**). If your settings differ, you don't need to match them — just recalibrate px (pixels-per-degree) as described in `USAGE.md`.

- **FOV：100**
- **全局灵敏度 Global sensitivity：1.00**
- 完整灵敏度参数见 `SETTINGS.md`（仅供参考，不是硬性要求）。

- **唯一硬性要求**（技术前提，否则工具读到的鼠标计数与游戏不一致）：
  - 游戏内"鼠标平滑"（Mouse Smoothing）关闭
  - Windows 指针选项"提高指针精确度"（Enhance pointer precision）关闭

See `SETTINGS.md` for the full sensitivity list (reference only, not mandatory).
- **Only hard requirement** (technical prerequisite; otherwise raw mouse counts won't match the game):
  - Disable in-game "Mouse Smoothing"
  - Disable Windows "Enhance pointer precision" (in Pointer Options)

---

## 已知精度 / Known Accuracy

- 低抛平射 300~1930m：≈ ±2m
- 高抛平射 1180~1940m：≈ ±6m
- 大高差（任意轨迹）：≈ ±7~15m

详细实测与误差见 `TEST_DATA.md`。

Detailed field tests and errors are in `TEST_DATA.md`.

---

## 免责声明 / Disclaimer

本项目仅为弹道计算器与屏幕覆盖层，**不注入、不读取游戏内存、不自瞄**。使用需遵守《Squad》服务条款，风险自负。作者不对封号等任何后果负责。

This is only a ballistic calculator + screen overlay. It does NOT inject, read game memory, or auto-aim. Use at your own risk and in compliance with Squad's Terms of Service. The author is not responsible for bans or any other consequences.

---

## 许可证 / License

**GNU General Public License v3.0（GPL v3.0）**。自由使用、修改、分发；修改版必须以 GPL v3.0 开源（copyleft）。详见 `LICENSE`。

**GNU General Public License v3.0 (GPL v3.0)**. Free to use, modify and distribute; modifications must be released under GPL v3.0 (copyleft). See `LICENSE`.
