# Squad 终极准星 / Squad Ultimate Crosshair

> **自由开源软件（GPL v3.0）。** — **Free & open-source software (GPL v3.0).**

一个针对《Squad》的榴弹发射器 / 迫击炮弹道瞄准工具：输入距离与高差，自动算出目标仰角，并在屏幕覆盖层画出绿点，告诉你鼠标往哪挪。

A ballistic aiming tool for Squad's grenade launchers / mortars: enter distance & height difference, and it computes the elevation and draws a green dot overlay showing where to aim.

> ⚠️ **最终版声明**：本项目已是最终版本。由于学业原因，作者将不再更新，后续维护只能依赖后来者 / 社区贡献者。
> ⚠️ **Final version notice**: This is the FINAL version. Due to academic commitments, the author will no longer update it; future maintenance depends entirely on later contributors / the community.

---

## 项目来源 / Origin

- **作者 Author**：清靖易（游戏内名 in-game）/ tiroday（GitHub）
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

## 重要设置要求 / Required Settings（务必一致，否则不准）

你的鼠标/视角设置必须与作者一致，否则 px（每度像素）会变，工具就不准：

Your mouse/FOV settings MUST match the author's, or the px (pixels-per-degree) changes and the tool will be off:

- **FOV：100**
- **全局灵敏度 Global sensitivity：1.00**
- 完整灵敏度参数见 `SETTINGS.md`。
- **必须禁用**（否则工具读到的鼠标计数与游戏不一致）：
  - 游戏内"鼠标平滑"（Mouse Smoothing）
  - Windows 指针选项里的"提高指针精确度"（Enhance pointer precision）

See `SETTINGS.md` for the full sensitivity list.
- **Must disable** (otherwise the raw mouse counts won't match the game):
  - In-game "Mouse Smoothing"
  - Windows "Enhance pointer precision" (in Pointer Options)

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
