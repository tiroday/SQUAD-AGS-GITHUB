# Squad 终极准星 — 开发备忘录（双语）/ Squad Ultimate Crosshair — Developer Notes (Bilingual)

> 本文件记录工具的最终参数、核心公式和关键修正历史，供开发者/贡献者参考。
> This file records the final parameters, core formulas and key fix history, for developers/contributors.

---

## 依赖 / Dependencies

- Python 3.12
- `pip install pillow pynput pytweening`
- 运行 Run: `pythonw AGS_CH.pyw`（中文 Chinese）/ `pythonw AGS_EN.pyw`（英文 English）

## 运行方式 / How It Runs

- **F7** 开始追踪（重置鼠标累计）；**F8** 停止。/ F7 starts tracking (resets mouse accumulation); F8 stops.
- **散布键**（默认 F9）切换覆盖模式。/ Spread key (default F9) toggles cover mode.
- 配置自动保存到 `squad_tool_config.json`（STYLE + fire_key）。/ Config auto-saves to `squad_tool_config.json`.

---

## 三武器最终参数 / Final Weapon Parameters (WEAPON_DATA)

### Mk19（纯物理 + 阻力修正，无高抛 / pure physics + drag correction, no high arc）
```
v0=236.8, px=21.7, max_el=19.8, min_el=-33.9, ads_fov=95, explosive_radius=15, zero_dist=300
can_high=False, use_poly=False, std_base_el=0, max_range=3100, drag_coeff=1.8e-6
碉堡化 bunker: 仅基准态可选 base-mode selectable {标准态(0°), 最大仰角}, 数据不变 data unchanged.
```

### QLZ-87（等效距离二次式，无高抛 / equivalent-distance quadratic, no high arc）
```
v0=185, px=65.8, max_el=46, min_el=-20, ads_fov=20, explosive_radius=11, zero_dist=100
can_high=False, use_poly=False, std_base_el=2.10, max_range=3256
resist_coeff=[-1.657844e-05, 9.185536e-01, 4.558855e+02]
碉堡化 bunker: 基准态锁定 base-mode locked to 标准态(2.10°), 数据不变 data unchanged.
```

### AGS-17 光瞄 / Optical sight（use_poly，有高抛 / has high arc）
```
v0=185, px=53, max_el=86.1, min_el=-13, ads_fov=24, explosive_radius=18, zero_dist=300
can_high=True, use_poly=True, std_base_el=0, max_range=1930
low_coeff =[5.63291832e-09, -1.33851083e-05, 2.68805481e-02, -4.43898303e+00]   # 低抛三次 low cubic
high_coeff=[-3.381842e-09, 5.934077e-06, -1.860806e-02, 9.085597e+01]          # 高抛三次 high cubic
```

### AGS-17 碉堡化 / Bunker（机瞄 iron sight，独立数据 independent data）
```
bunker_px=21, bunker_std_base_el=3.57, bunker_ads_fov=90
bunker_max_el=67.6      # 最上沿 top edge（超了就红叉 → out-of-range）
bunker_base_el=86.1     # 高抛基准 high-arc base（参考值 reference only）
bunker_max_range=1950
bunker_low_ext=[1930.0, 38.078, 0.6253, -0.02071]   # 低抛最远段二次插值 low max-range quadratic
bunker_high_coeff=[-8.35991882e-13, 6.27922874e-09, -1.87560738e-05, 2.78381197e-02, -2.05467294e+01, 6.10632066e+03]  # 高抛五次 high quintic
bunker_auto_base=True   # 基准随弹道自动 base auto-switches: 低抛→标准态(3.57°), 高抛→最大仰角(86.1°)
```

---

## 核心计算公式 / Core Formulas

### 纯物理弹道 / Pure projectile `physics_el(d, h, v0, hi)`
```
tanθ = (v0² ± √(v0⁴ − G·(G·d² + 2·h·v0²))) / (G·d)    G=9.78
低抛取 −，高抛取 +   (low arc uses −, high arc uses +)
```

### 目标仰角 / Target elevation `get_target_el(w, d, h, hi)`
```
1. d > max_range → None（超射程 out-of-range）
2. x = d
   - QLZ：x = eval_poly(resist_coeff, d)
   - Mk19：x = d − drag_coeff·d²
3. use_poly（AGS-17）：
   平射 flat el_flat：
     - 高抛 high：el_flat = eval_poly(high_coeff, x)
     - 低抛 low：若 bunker_low_ext 且 x>阈值 → 二次插值 quadratic；否则 eval_poly(low_coeff, x)
   高差修正（物理反推 height correction via physics）：
     el = el_flat + [physics_el(x, h, v0, hi) − physics_el(x, 0, v0, hi)]
4. 非 use_poly（Mk19/QLZ）：el = physics_el(x, h, v0, hi)
5. el 超 [min_el, max_el] → None
```

### 鼠标位移 / Mouse offset `need_dy`
```
need_dy = (基准仰角 base_el − 目标仰角 tgt) × px
绿点 y = 屏幕中心 + (need_dy − 累计鼠标dy)   (green-dot y = screen center + (need_dy − accumulated mouse dy))
```

### 基准 / Base `get_base_el(w, hi)`
```
碉堡化(bunker_auto_base)：高抛→bunker_base_el(86.1°)，低抛→std_base_el(3.57°)
普通 normal：按基准态下拉（标准态/300m归零/最大仰角/最大俯角）→ via base-mode dropdown
```

### 飞行时间 / Flight time `flight_time`
```
t = d / (v0 · cos(仰角 elevation))
```

### 碉堡参数替换 / Bunker param swap `get_weapon()`
```
碉堡化时，把 key ∈ ("px","ads_fov","max_el","max_range","low_coeff","high_coeff","std_base_el")
替换为 "bunker_"+key（若存在 if present）。
```

---

## 关键修正历史 / Key Fix History（重要决策，勿回退 / important decisions — do NOT revert）

1. **鼠标过滤 Mouse filter**：`MOUSE_MOVE_ABSOLUTE` 过滤已**移除 removed**（所有鼠标增量都累计 all deltas accumulate）。
2. **AGS-17 低抛 std_base_el=0**（不是 0.64，那是污染数据推导的错值；not 0.64, which was a wrong value from contaminated data）。
3. **碉堡高抛基准 Bunker high-arc base**：曾试过 86.1° 直接当基准 → 错 wrong；最终是**平射用多项式 + 高差用物理反推**（el_flat + Δphysics）。86.1° 只是 bunker_base_el 参考 reference only。
4. **碉堡高抛 Bunker high arc**：`bunker_high_coeff` 用 5 次多项式 quintic（dy 规律 + 1180/1940/1950 锚点拟合）。之前 4 次式会在 <1500m 外推振荡（871m 算出 3657°），已弃用 the old quartic oscillated below 1500m, discarded。
5. **碉堡低抛最远段 Bunker low max-range**：用 `bunker_low_ext` 二次插值 quadratic（1930→38.078°、1940→42.26°、1950→42.3°），<1930m 用共享 low_coeff。
6. **高差修正 Height correction**：从线性 `x=d+k·h` 改成物理反推 changed from linear to physics-inversion，大高差才准（771.9/-63.8 从 9.2° 修正到 6.15°）。
7. **绿点 Green dot**：保持单个绿点 + 十字线 single dot + crosshair（左右衍生点那版已撤销 side-dots version reverted）。

## 已知待验证 / Known Gaps（不影响稳定性 / not stability-critical）

- AGS 高抛大高差（阻力大，误差可能比低抛大）。/ AGS high-arc large height diff (drag is large).
- AGS 碉堡化大高差。/ AGS bunker large height diff.
- MK19/QLZ 大高差（阻力修正只看距离，大高差有小幅系统误差）。/ MK19/QLZ large height diff (drag correction is distance-only).
- 低抛 300m 以内、极远端边界。/ Low arc below 300m and extreme far end.

## 相关新项目 / Related (separate) projects

- **Squad-Ballistics**（PyQt6 桌面应用）：已汉化、离线 SquadCalc、绿点左右衍生。独立项目，不在本仓库。
- **Squad-Ballistics** (PyQt6 desktop app): localized (zh), offline SquadCalc, green-dot side dots. A separate project, not in this repo.
- **SquadCalc**：本地版（localhost:3000），本工具的地图数据参考来源。
- **SquadCalc**: local build (localhost:3000), the map-data reference source.
