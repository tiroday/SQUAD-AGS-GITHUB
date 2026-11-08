# -*- coding: utf-8 -*-
# Squad 终极准星 —— 《Squad》榴弹发射器/迫击炮弹道瞄准工具
# Copyright (C) 2025  tiroday（GitHub）
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Squad 终极准星 v53（三武器定案）
- Mk19：纯物理 + 阻力修正 drag_coeff·d²；px=21.7 / max_el=19.8 / max_range=3100
- QLZ：等效距离（二次拟合，覆盖 1200~3256m，全段 ±6.5m）；max_range=3256
- AGS：三次函数 + 高差修正 k=1.64→0.88(低抛)/0.76(高抛)；max_el=86.1/min_el=-13.0
"""
import math, threading, ctypes, json, os
from ctypes import wintypes
import tkinter as tk
from tkinter import messagebox, colorchooser, ttk

try:
    from PIL import Image, ImageDraw, ImageTk
except ImportError:
    r = tk.Tk(); r.withdraw()
    messagebox.showerror("缺少组件", "请先安装 Pillow:\npip install pillow")
    raise SystemExit

try:
    import pytweening; _TWEEN = True
except ImportError:
    _TWEEN = False

from pynput import keyboard

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

G = 9.78

# ==================== 配置保存/读取 ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "squad_tool_config.json")

def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
BG, CARD, FIELD = "#12121a", "#1c1c26", "#2a2a38"
FG, MUTED, ACC = "#d8d8e0", "#7a7a88", "#4da6ff"
GOOD, WARN, BAD = "#22c55e", "#f59e0b", "#ef4444"
TRANSPARENT = "#010101"
FONT = ("KaiTi", 10); FONT_B = ("KaiTi", 10, "bold"); FONT_T = ("KaiTi", 12, "bold")
FONT_M = ("Consolas", 11, "bold")

WEAPON_DATA = {
    "Mk19": {"name": "Mk19", "v0": 236.8, "px": 21.7, "max_el": 19.8, "min_el": -33.9,
             "ads_fov": 95.0, "explosive_radius": 15.0, "zero_dist": 300.0,
             "can_high": False, "can_zero": True, "use_poly": False, "use_resist": False,
             "std_base_el": 0.0, "max_range": 3100.0, "drag_coeff": 1.8e-6,
             "bunker_modes": ["标准态 (0°)", "最大仰角"]},
    "AGS-17": {"name": "AGS-17", "v0": 185.0, "px": 53.0, "max_el": 86.1, "min_el": -13.0,
               "ads_fov": 24.0, "explosive_radius": 18.0, "zero_dist": 300.0,
               "can_high": True, "can_zero": False, "use_poly": True, "use_resist": False,
               "std_base_el": 0.0,
               "low_coeff": [5.63291832e-09, -1.33851083e-05, 2.68805481e-02, -4.43898303e+00],
               "high_coeff": [-3.381842e-09, 5.934077e-06, -1.860806e-02, 9.085597e+01],
               "low_height_coeff": 1.64, "high_height_coeff": 0.76,
               "max_range": 1930.0,
               "bunker_modes": ["标准态 (0°)"],
               "bunker_auto_base": True,
               "bunker_px": 21.0, "bunker_std_base_el": 3.57, "bunker_ads_fov": 90.0, "bunker_max_el": 67.6, "bunker_base_el": 86.1, "bunker_max_range": 1950.0,
               "bunker_low_ext": [1930.0, 38.078, 0.6253, -0.02071],
               "bunker_high_coeff": [-8.35991882e-13, 6.27922874e-09, -1.87560738e-05, 2.78381197e-02, -2.05467294e+01, 6.10632066e+03]},
    "QLZ-87": {"name": "QLZ-87", "v0": 185.0, "px": 65.8, "max_el": 46.0, "min_el": -20.0,
               "ads_fov": 20.0, "explosive_radius": 11.0, "zero_dist": 100.0,
               "can_high": False, "can_zero": False, "use_poly": False,
               "resist_coeff": [-1.657844e-05, 9.185536e-01, 4.558855e+02],
               "std_base_el": 2.10, "max_range": 3256.0,
               "bunker_modes": ["标准态 (0°)"]},
}

STYLE = {
    "dot_color": "#00ff00", "dot_size": 5, "cross_size": 12, "opacity": 1.0,
    "hint_color": "#FFFFFF", "hint_size": 45,
    "arrow_color": "#FF7700", "arrow_fill": "#000000",
    "tick_color": "#FFFFFF", "tick_count": 12, "tick_len": 8,
    "spread_color": "#eab308", "spread_width": 2,
    "spread_dot_color": "#ffffff", "spread_scale": 1.0,
    "x_color": "#ff3333", "x_size": 30,
}

def hex_rgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
def rgba(h, a):
    r, g, b = hex_rgb(h); return (r, g, b, int(max(0, min(1, a)) * 255))
def ease(p, n="easeOutCubic"):
    if _TWEEN and hasattr(pytweening, n): return getattr(pytweening, n)(max(0.0, min(1.0, p)))
    return max(0.0, min(1.0, p))
def lerp(a, b, t): return a + (b - a) * t
def fade_hex(h, a):
    r, g, b = hex_rgb(h); a = max(0.0, min(1.0, a))
    return f"#{int(r*a+1*(1-a)):02x}{int(g*a+1*(1-a)):02x}{int(b*a+1*(1-a)):02x}"

def eval_poly(c, x):
    n = len(c)
    return sum(c[i] * x**(n-1-i) for i in range(n))
def physics_el(d, h, v0, hi):
    if d <= 0: return None
    v2 = v0**2; disc = v2**2 - G*(G*d**2 + 2*h*v2)
    if disc < 0: return None
    root = math.sqrt(disc)
    tan_t = (v2 + root if hi else v2 - root) / (G*d)
    return math.degrees(math.atan(tan_t))
def get_target_el(w, d, h, hi):
    if d > w["max_range"]:
        return None
    x = d
    if w.get("resist_coeff"):
        # QLZ：等效距离（二次拟合，覆盖 1200~3256m）
        x = eval_poly(w["resist_coeff"], d)
    elif w.get("drag_coeff"):
        # Mk19：阻力修正（长程炮弹打近）
        x = d - w["drag_coeff"] * d * d
    if w.get("use_poly"):
        # AGS-17：平射用多项式，高差用纯物理反推（大高差也准）
        if hi:
            el_flat = eval_poly(w["high_coeff"], x)
        else:
            ext = w.get("bunker_low_ext")
            if ext is not None and x > ext[0]:
                dd = x - ext[0]
                el_flat = ext[1] + ext[2] * dd + ext[3] * dd * dd
            else:
                el_flat = eval_poly(w["low_coeff"], x)
        t_no = physics_el(x, h, w["v0"], hi)
        t_flat = physics_el(x, 0.0, w["v0"], hi)
        if t_no is None or t_flat is None:
            el = None
        else:
            el = el_flat + (t_no - t_flat)
    else:
        el = physics_el(x, h, w["v0"], hi)
    if el is None or el > w["max_el"] or el < w["min_el"]: return None
    return el
def flight_time(w, d, el):
    return d / (w["v0"] * math.cos(math.radians(el))) if (el is not None and d > 0) else 0.0

# ==================== Raw Input ====================
user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
WM_INPUT, RIDEV_INPUTSINK, RID_INPUT = 0x00FF, 0x00000100, 0x10000003
RIM_TYPEMOUSE, MOUSE_MOVE_ABSOLUTE = 0, 0x0001
WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_longlong, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

class WNDCLASSEX(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.UINT), ("style", wintypes.UINT), ("lpfnWndProc", WNDPROC),
                ("cbClsExtra", ctypes.c_int), ("cbWndExtra", ctypes.c_int), ("hInstance", wintypes.HINSTANCE),
                ("hIcon", wintypes.HICON), ("hCursor", wintypes.HANDLE), ("hbrBackground", wintypes.HBRUSH),
                ("lpszMenuName", wintypes.LPCWSTR), ("lpszClassName", wintypes.LPCWSTR), ("hIconSm", wintypes.HICON)]
class RAWINPUTDEVICE(ctypes.Structure):
    _fields_ = [("usUsagePage", wintypes.USHORT), ("usUsage", wintypes.USHORT), ("dwFlags", wintypes.DWORD), ("hwndTarget", wintypes.HWND)]
class RAWINPUTHEADER(ctypes.Structure):
    _fields_ = [("dwType", wintypes.DWORD), ("dwSize", wintypes.DWORD), ("hDevice", wintypes.HANDLE), ("wParam", wintypes.WPARAM)]
class RAWMOUSE(ctypes.Structure):
    _fields_ = [("usFlags", wintypes.USHORT), ("usButtonFlags", wintypes.USHORT), ("usButtonData", wintypes.USHORT),
                ("ulRawButtons", wintypes.ULONG), ("lLastX", wintypes.LONG), ("lLastY", wintypes.LONG), ("ulExtraInformation", wintypes.ULONG)]
class RAWINPUT(ctypes.Structure):
    _fields_ = [("header", RAWINPUTHEADER), ("mouse", RAWMOUSE)]

class RawInputListener:
    def __init__(self, on_move):
        self.on_move = on_move; self.thread = self.hwnd = None
        self.ready = threading.Event(); self._stop = False
        self._wndproc = WNDPROC(self._wnd_proc)
    def start(self):
        self.thread = threading.Thread(target=self._run, daemon=True); self.thread.start(); self.ready.wait(timeout=2.0)
    def _run(self):
        hinst = kernel32.GetModuleHandleW(None)
        wc = WNDCLASSEX(ctypes.sizeof(WNDCLASSEX), 0, self._wndproc, 0, 0, hinst, None, None, None, None, "HAJIMI_V53", None)
        user32.RegisterClassExW(ctypes.byref(wc))
        hwnd = user32.CreateWindowExW(0, "HAJIMI_V53", "hidden", 0, 0, 0, 0, 0, None, None, hinst, None)
        self.hwnd = hwnd
        rid = RAWINPUTDEVICE(0x01, 0x02, RIDEV_INPUTSINK, hwnd)
        user32.RegisterRawInputDevices(ctypes.byref(rid), 1, ctypes.sizeof(RAWINPUTDEVICE))
        self.ready.set(); msg = wintypes.MSG()
        while not self._stop and user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(msg)); user32.DispatchMessageW(ctypes.byref(msg))
    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_INPUT:
            try:
                size = wintypes.UINT(0)
                user32.GetRawInputData(lparam, RID_INPUT, None, ctypes.byref(size), ctypes.sizeof(RAWINPUTHEADER))
                if size.value > 0:
                    buf = ctypes.create_string_buffer(size.value)
                    user32.GetRawInputData(lparam, RID_INPUT, buf, ctypes.byref(size), ctypes.sizeof(RAWINPUTHEADER))
                    raw = ctypes.cast(buf, ctypes.POINTER(RAWINPUT)).contents
                    if raw.header.dwType == RIM_TYPEMOUSE:
                        if raw.mouse.lLastX or raw.mouse.lLastY: self.on_move(raw.mouse.lLastX, raw.mouse.lLastY)
            except Exception: pass
            return 0
        return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

class App:
    def __init__(self):
        _cfg = load_config()
        STYLE.update(_cfg.get("style", {}))
        self.root = tk.Tk()
        self.lock = threading.Lock()
        self.active = False; self.mouse_dx = self.mouse_dy = 0
        self.fire_mode = False; self.fire_key = _cfg.get("fire_key", "f9"); self.recording_key = False
        self.sx = self.sy = 0.0; self.sr = 0.0
        self.s_arrow_a = self.s_dot_a = self.s_spread_a = self.s_x_a = 0.0
        self._tk_img = None; self.style_open = False
        self._last_input = None
        self.raw = RawInputListener(self._on_raw_move); self.raw.start()
        self.kl = keyboard.Listener(on_press=self._on_press); self.kl.start()
        self.build_ui(); self.build_overlay(); self.refresh()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def save_config_now(self):
        save_config({"style": STYLE, "fire_key": self.fire_key})

    def _on_close(self):
        self.save_config_now()
        self.root.destroy()

    def _on_raw_move(self, dx, dy):
        with self.lock:
            if self.active: self.mouse_dx += dx; self.mouse_dy += dy

    def _on_press(self, key):
        try:
            k = str(key).replace("Key.", "").replace("'", "").lower()
            if self.recording_key:
                self.fire_key = k
                self.root.after(0, self._finish_record)
                return
            if k == "f7": self.root.after(0, self.start_tracking)
            elif k == "f8": self.root.after(0, self.stop_tracking)
            elif k == self.fire_key: self.root.after(0, self.toggle_fire_mode)
        except Exception: pass

    def start_tracking(self):
        with self.lock: self.mouse_dx = self.mouse_dy = 0; self.active = True
        self.fire_mode = False
        self.status_lbl.config(text="● 追踪中 (F8 锁定)", fg=GOOD)

    def stop_tracking(self):
        with self.lock: self.active = False
        self.fire_mode = False
        self.status_lbl.config(text="● 已锁定", fg=WARN)

    def toggle_fire_mode(self):
        self.fire_mode = not self.fire_mode
        if self.fire_mode:
            self.status_lbl.config(text="● 覆盖模式 (散布线跟随)", fg=ACC)
        else:
            self.status_lbl.config(text="● 追踪中 (F8 锁定)", fg=GOOD)

    def start_record(self):
        self.recording_key = True
        self.record_btn.config(text="按任意键...")

    def _finish_record(self):
        self.recording_key = False
        self.fire_key_btn.config(text=self.fire_key.upper())
        self.record_btn.config(text="设置")
        self.save_config_now()

    def pick_color(self, key, btn):
        c = colorchooser.askcolor(color=STYLE[key])[1]
        if c: STYLE[key] = c; btn.config(bg=c); self.save_config_now()

    # ---------- UI ----------
    def build_ui(self):
        self.root.title("Squad 终极准星 v53"); self.root.configure(bg=BG); self.root.attributes("-topmost", True)
        self.root.geometry("340x560")

        self.status_lbl = tk.Label(self.root, text="● 按 F7 开始", font=FONT_B, fg=MUTED, bg=BG)
        self.status_lbl.pack(anchor="w", padx=14, pady=(10, 2))

        left = tk.Frame(self.root, bg=BG); left.pack(side="left", fill="both", expand=True, padx=10, pady=4)

        c1 = tk.LabelFrame(left, text="武器与弹道", bg=BG, fg=ACC, font=FONT_B, bd=1, relief="solid")
        c1.pack(fill="x", pady=4)
        r = tk.Frame(c1, bg=BG); r.pack(fill="x", pady=3)
        tk.Label(r, text="武器", bg=BG, fg=FG, font=FONT).pack(side="left", padx=(8, 4))
        self.w_var = tk.StringVar(value="QLZ-87")
        self.w_cb = ttk.Combobox(r, textvariable=self.w_var, values=list(WEAPON_DATA.keys()), state="readonly", width=9, font=FONT)
        self.w_cb.pack(side="left"); self.w_cb.bind("<<ComboboxSelected>>", lambda e: self.on_weapon_change())
        tk.Label(r, text="弹道", bg=BG, fg=FG, font=FONT).pack(side="left", padx=(8, 4))
        self.a_var = tk.StringVar(value="低抛")
        self.a_cb = ttk.Combobox(r, textvariable=self.a_var, values=["低抛"], state="readonly", width=5, font=FONT)
        self.a_cb.pack(side="left"); self.a_cb.bind("<<ComboboxSelected>>", lambda e: (self.stop_tracking(), self._sync_base_mode()))
        r2 = tk.Frame(c1, bg=BG); r2.pack(fill="x", pady=3)
        tk.Label(r2, text="基准", bg=BG, fg=FG, font=FONT).pack(side="left", padx=(8, 4))
        self.b_var = tk.StringVar(value="标准态 (0°)")
        self.b_cb = ttk.Combobox(r2, textvariable=self.b_var, values=[], state="readonly", width=12, font=FONT)
        self.b_cb.pack(side="left"); self.b_cb.bind("<<ComboboxSelected>>", lambda e: self.stop_tracking())
        self.bunker_var = tk.BooleanVar(value=False)
        self.bunker_cb = tk.Checkbutton(r2, text="碉堡化", variable=self.bunker_var, bg=BG, fg=FG,
                                        selectcolor=FIELD, activebackground=BG, activeforeground=FG,
                                        font=FONT, command=self.on_bunker_toggle)
        self.bunker_cb.pack(side="left", padx=(10, 0))

        c2 = tk.LabelFrame(left, text="目标", bg=BG, fg=ACC, font=FONT_B, bd=1, relief="solid")
        c2.pack(fill="x", pady=4)
        r3 = tk.Frame(c2, bg=BG); r3.pack(fill="x", pady=3)
        tk.Label(r3, text="距离", bg=BG, fg=FG, font=FONT).pack(side="left", padx=(8, 4))
        self.dist_entry = tk.Entry(r3, width=6, bg=FIELD, fg=GOOD, font=FONT_M, relief="flat", insertbackground=FG)
        self.dist_entry.insert(0, "1500"); self.dist_entry.pack(side="left", padx=2)
        tk.Label(r3, text="高差", bg=BG, fg=FG, font=FONT).pack(side="left", padx=(8, 4))
        self.height_entry = tk.Entry(r3, width=6, bg=FIELD, fg=FG, font=FONT_M, relief="flat", insertbackground=FG)
        self.height_entry.insert(0, "0"); self.height_entry.pack(side="left", padx=2)
        r4 = tk.Frame(c2, bg=BG); r4.pack(fill="x", pady=3)
        tk.Label(r4, text="当前方位", bg=BG, fg=FG, font=FONT).pack(side="left", padx=(8, 4))
        self.az_cur = tk.Entry(r4, width=5, bg=FIELD, fg=FG, font=FONT_M, relief="flat", insertbackground=FG)
        self.az_cur.insert(0, "0"); self.az_cur.pack(side="left", padx=2)
        tk.Label(r4, text="目标方位", bg=BG, fg=FG, font=FONT).pack(side="left", padx=(8, 4))
        self.az_tgt = tk.Entry(r4, width=5, bg=FIELD, fg=FG, font=FONT_M, relief="flat", insertbackground=FG)
        self.az_tgt.insert(0, "0"); self.az_tgt.pack(side="left", padx=2)

        fk = tk.Frame(left, bg=BG); fk.pack(fill="x", pady=4)
        tk.Label(fk, text="散布键", bg=BG, fg=FG, font=FONT).pack(side="left", padx=(8, 4))
        self.fire_key_btn = tk.Label(fk, text=self.fire_key.upper(), bg=FIELD, fg=ACC, font=FONT_B, width=6)
        self.fire_key_btn.pack(side="left")
        self.record_btn = tk.Button(fk, text="设置", font=FONT, bg=FIELD, fg=FG, relief="flat",
                                    activebackground="#33334a", activeforeground=FG, cursor="hand2",
                                    command=self.start_record)
        self.record_btn.pack(side="left", padx=4)
        self.weapon_info_lbl = tk.Label(left, text="", font=FONT_T, fg=ACC, bg=BG, justify="left")
        self.weapon_info_lbl.pack(anchor="w", padx=12, pady=(6, 0))

        self.result_lbl = tk.Label(left, text="等待计算...", font=FONT_T, fg=WARN, bg=BG, justify="left")
        self.result_lbl.pack(anchor="w", padx=12, pady=(10, 2))
        self.info_lbl = tk.Label(left, text="", font=("Consolas", 9), fg=MUTED, bg=BG, justify="left")
        self.info_lbl.pack(anchor="w", padx=12, pady=2)

        self.style_btn = tk.Button(left, text="⚙ 自定义", font=FONT_B, bg=FIELD, fg=ACC, relief="flat",
                                   activebackground="#33334a", activeforeground=FG, cursor="hand2",
                                   command=self.toggle_style)
        self.style_btn.pack(pady=(8, 0))

        self.style_frame = tk.Frame(self.root, bg=CARD, width=230)
        self.style_frame.pack_propagate(False)
        self._build_style(self.style_frame)
        self.on_weapon_change()

    def _build_style(self, frame):
        tk.Label(frame, text="样式自定义", bg=CARD, fg=FG, font=FONT_T).pack(pady=(10, 4))
        cv = tk.Canvas(frame, bg=CARD, width=230, highlightthickness=0)
        sb = tk.Scrollbar(frame, orient="vertical", command=cv.yview)
        inner = tk.Frame(cv, bg=CARD)
        inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.create_window((0, 0), window=inner, anchor="nw"); cv.configure(yscrollcommand=sb.set)
        cv.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")
        cv.bind_all("<MouseWheel>", lambda e: cv.yview_scroll(-1*(e.delta//120), "units"))

        def color_row(p, label, key):
            f = tk.Frame(p, bg=CARD); f.pack(fill="x", pady=2)
            tk.Label(f, text=label, bg=CARD, fg=FG, font=FONT).pack(side="left", padx=(10, 4))
            b = tk.Button(f, bg=STYLE[key], width=3, relief="flat", bd=0, cursor="hand2",
                          command=lambda: self.pick_color(key, b)); b.pack(side="right", padx=10)
            return b
        def scale_row(p, label, lo, hi, default):
            f = tk.Frame(p, bg=CARD); f.pack(fill="x", pady=2)
            tk.Label(f, text=label, bg=CARD, fg=FG, font=FONT).pack(side="left", padx=(10, 4))
            s = tk.Scale(f, from_=lo, to=hi, orient="horizontal", bg=CARD, fg=FG, highlightthickness=0,
                         troughcolor=FIELD, length=90, showvalue=False, font=("Arial", 7))
            s.set(default); s.pack(side="right", padx=10)
            return s

        tk.Label(inner, text="— 绿点 —", bg=CARD, fg=MUTED, font=FONT).pack(anchor="w", padx=10, pady=(6, 0))
        color_row(inner, "颜色", "dot_color")
        self.dot_size_s = scale_row(inner, "大小", 3, 12, STYLE["dot_size"])
        self.opacity_s = scale_row(inner, "透明度", 10, 100, int(STYLE["opacity"]*100))

        tk.Label(inner, text="— 提示圆 —", bg=CARD, fg=MUTED, font=FONT).pack(anchor="w", padx=10, pady=(6, 0))
        color_row(inner, "颜色", "hint_color")
        self.hint_size_s = scale_row(inner, "大小", 20, 80, STYLE["hint_size"])

        tk.Label(inner, text="— 箭头（随提示圆） —", bg=CARD, fg=MUTED, font=FONT).pack(anchor="w", padx=10, pady=(6, 0))
        color_row(inner, "颜色", "arrow_color")
        color_row(inner, "填充", "arrow_fill")

        tk.Label(inner, text="— 刻度(毛刺) —", bg=CARD, fg=MUTED, font=FONT).pack(anchor="w", padx=10, pady=(6, 0))
        color_row(inner, "颜色", "tick_color")
        self.tick_count_s = scale_row(inner, "数量", 0, 24, STYLE["tick_count"])
        self.tick_len_s = scale_row(inner, "长度", 0, 30, STYLE["tick_len"])

        tk.Label(inner, text="— 散布线 —", bg=CARD, fg=MUTED, font=FONT).pack(anchor="w", padx=10, pady=(6, 0))
        color_row(inner, "颜色", "spread_color")
        color_row(inner, "参照点", "spread_dot_color")
        self.kill_range_lbl = tk.Label(inner, text="", bg=CARD, fg=WARN, font=("KaiTi", 9))
        self.kill_range_lbl.pack(anchor="w", padx=10, pady=2)
        f = tk.Frame(inner, bg=CARD); f.pack(fill="x", pady=2)
        tk.Label(f, text="覆盖半径(m)", bg=CARD, fg=FG, font=FONT).pack(side="left", padx=(10, 4))
        self.cover_entry = tk.Entry(f, width=5, bg=FIELD, fg=FG, font=FONT_M, relief="flat", insertbackground=FG)
        self.cover_entry.pack(side="right", padx=10)
        self.spread_scale_s = scale_row(inner, "散布线倍率", 20, 200, int(STYLE["spread_scale"]*100))

        tk.Label(inner, text="— 红叉(超射程) —", bg=CARD, fg=MUTED, font=FONT).pack(anchor="w", padx=10, pady=(6, 0))
        color_row(inner, "颜色", "x_color")
        self.x_size_s = scale_row(inner, "大小", 15, 80, STYLE["x_size"])

    def toggle_style(self):
        self.style_open = not self.style_open
        if self.style_open: self.style_frame.pack(side="right", fill="y", padx=(4, 0))
        else: self.style_frame.pack_forget()
        self._animate_width(570 if self.style_open else 340)

    def _animate_width(self, target):
        cur = self.root.winfo_width(); new = int(cur + (target - cur) * 0.35)
        self.root.geometry(f"{new}x560")
        if abs(new - target) > 2: self.root.after(16, lambda: self._animate_width(target))
        else: self.root.geometry(f"{target}x560")

    def on_weapon_change(self):
        w = WEAPON_DATA[self.w_var.get()]
        if w["can_high"]:
            self.a_cb["values"] = ["低抛", "高抛"]; self.a_cb.config(state="readonly")
        else:
            self.a_var.set("低抛"); self.a_cb["values"] = ["低抛"]; self.a_cb.config(state="disabled")
        self.bunker_var.set(False)
        self._apply_base_options(w)
        self._sync_base_mode()
        self.kill_range_lbl.config(text=f"武器杀伤范围: {w['explosive_radius']:.0f}m（默认）")
        self.cover_entry.delete(0, "end")
        self.cover_entry.insert(0, str(w["explosive_radius"]))

    def on_bunker_toggle(self):
        self.stop_tracking()
        self._apply_base_options(WEAPON_DATA[self.w_var.get()])
        self._sync_base_mode()

    def _apply_base_options(self, w):
        opts = ["标准态 (0°)", "最大仰角", "最大俯角"]
        if w["can_zero"]: opts = ["标准态 (0°)", "300m 归零", "最大仰角", "最大俯角"]
        if self.bunker_var.get():
            if w.get("bunker_auto_base"):
                opts = ["标准态 (0°)", "最大仰角"]
            else:
                opts = list(w.get("bunker_modes", ["标准态 (0°)"]))
        if self.b_var.get() not in opts: self.b_var.set(opts[0])
        self.b_cb["values"] = opts
        if self.bunker_var.get() and w.get("bunker_auto_base"):
            self.b_cb.config(state="disabled")
        else:
            self.b_cb.config(state="readonly" if len(opts) > 1 else "disabled")

    def _sync_base_mode(self):
        if self.bunker_var.get() and WEAPON_DATA[self.w_var.get()].get("bunker_auto_base"):
            hi = self.a_var.get() == "高抛"
            self.b_var.set("最大仰角" if hi else "标准态 (0°)")

    def get_weapon(self):
        w = dict(WEAPON_DATA[self.w_var.get()])
        if self.bunker_var.get():
            for k in ("px", "ads_fov", "max_el", "max_range", "low_coeff", "high_coeff", "std_base_el"):
                bk = "bunker_" + k
                if bk in w:
                    w[k] = w[bk]
        return w

    # ---------- Overlay ----------
    def build_overlay(self):
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes("-topmost", True, "-transparentcolor", TRANSPARENT)
        self.overlay.overrideredirect(True); self.overlay.attributes("-toolwindow", True)
        self.sw = self.overlay.winfo_screenwidth(); self.sh = self.overlay.winfo_screenheight()
        self.overlay.geometry(f"{self.sw}x{self.sh}+0+0"); self.overlay.configure(bg=TRANSPARENT)
        self.canvas = tk.Canvas(self.overlay, bg=TRANSPARENT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

    def get_base_el(self, w, hi):
        if self.bunker_var.get() and w.get("bunker_auto_base"):
            if hi:
                return w.get("bunker_base_el", w["max_el"])
            return w.get("std_base_el", 0.0)
        s = self.b_var.get()
        if "300m" in s:
            t = get_target_el(w, w["zero_dist"], 0.0, hi); return t if t is not None else 0.0
        if "最大仰角" in s: return w["max_el"]
        if "最大俯角" in s: return w["min_el"]
        return w.get("std_base_el", 0.0)

    def render_indicator(self, angle, alpha):
        S = 400; img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        cx = cy = S // 2; R = 150
        d.ellipse([cx-R, cy-R, cx+R, cy+R], fill=rgba(STYLE["hint_color"], alpha*0.12),
                  outline=rgba(STYLE["hint_color"], alpha), width=3)
        n = int(STYLE["tick_count"]); tl = R + int(STYLE["tick_len"])
        for i in range(n):
            a = 2 * math.pi * i / max(1, n)
            d.line([cx+R*math.cos(a), cy+R*math.sin(a), cx+tl*math.cos(a), cy+tl*math.sin(a)],
                   fill=rgba(STYLE["tick_color"], alpha), width=2)
        ca, sa = math.cos(angle), math.sin(angle)
        pts = [(R*0.8, 0), (R*0.2, -R*0.4), (R*0.2, -R*0.1), (-R*0.5, -R*0.1),
               (-R*0.5, R*0.1), (R*0.2, R*0.1), (R*0.2, R*0.4)]
        rot = [(cx + x*ca - y*sa, cy + x*sa + y*ca) for x, y in pts]
        d.polygon(rot, fill=rgba(STYLE["arrow_fill"], alpha*0.55), outline=rgba(STYLE["arrow_color"], alpha), width=2)
        return img

    def refresh(self):
        self.canvas.delete("all")
        try:
            dist = float(self.dist_entry.get()); height = float(self.height_entry.get())
            az_cur = float(self.az_cur.get() or 0); az_tgt = float(self.az_tgt.get() or 0)
            STYLE["opacity"] = self.opacity_s.get() / 100.0
            STYLE["dot_size"] = int(self.dot_size_s.get()); STYLE["hint_size"] = int(self.hint_size_s.get())
            STYLE["tick_count"] = int(self.tick_count_s.get()); STYLE["tick_len"] = int(self.tick_len_s.get())
            STYLE["x_size"] = int(self.x_size_s.get())
            STYLE["spread_scale"] = self.spread_scale_s.get() / 100.0
            cover_radius = float(self.cover_entry.get() or 0)
        except Exception:
            self.root.after(16, self.refresh); return

        w = self.get_weapon(); hi = self.a_var.get() == "高抛"
        wtag = w["name"] + ("碉堡" if self.bunker_var.get() else "")
        traj = "高抛" if hi else "低抛"
        cur_input = (self.w_var.get(), self.a_var.get(), self.b_var.get(), self.bunker_var.get(),
                     self.dist_entry.get(), self.height_entry.get(), self.az_cur.get(), self.az_tgt.get())
        if cur_input != self._last_input:
            self._last_input = cur_input
            with self.lock: self.mouse_dx = self.mouse_dy = 0
        cx, cy = self.sw / 2, self.sh / 2
        tgt = get_target_el(w, dist, height, hi)
        with self.lock: mdx, mdy = self.mouse_dx, self.mouse_dy; active = self.active

        if tgt is None:
            self.result_lbl.config(text="✖ 无法打到（超射程）", fg=BAD); self.info_lbl.config(text="")
            self.weapon_info_lbl.config(text=f"{wtag} · {traj} · 无法打到", fg=BAD)
            self.s_x_a = lerp(self.s_x_a, 1.0, 0.2)
            self.s_dot_a = lerp(self.s_dot_a, 0.0, 0.15)
            self.s_arrow_a = lerp(self.s_arrow_a, 0.0, 0.15)
            self.s_spread_a = lerp(self.s_spread_a, 0.0, 0.15)
        else:
            base_el = self.get_base_el(w, hi); need_dy = (base_el - tgt) * w["px"]
            rem = need_dy - mdy; abs_rem = abs(rem)
            daz = (az_tgt - az_cur + 180) % 360 - 180
            tx = cx + mdx + daz * w["px"]; ty = cy + rem
            self.sx = lerp(self.sx, tx, 0.35); self.sy = lerp(self.sy, ty, 0.35)

            max_dy, min_dy = 1200, 300
            if active and not self.fire_mode and abs_rem > min_dy:
                sc = 1.0 if abs_rem >= max_dy else (abs_rem - min_dy) / (max_dy - min_dy)
                sc = ease(sc); tr = STYLE["hint_size"] * sc; ta = 0.25 + 0.75 * sc
            else: tr, ta = 0.0, 0.0
            self.sr = lerp(self.sr, tr, 0.15); self.s_arrow_a = lerp(self.s_arrow_a, ta, 0.15)

            self.s_dot_a = lerp(self.s_dot_a, 1.0 if (active and not self.fire_mode) else 0.0, 0.2)
            self.s_spread_a = lerp(self.s_spread_a, 1.0 if (active and self.fire_mode) else 0.0, 0.2)
            self.s_x_a = lerp(self.s_x_a, 0.0, 0.15)

            if self.fire_mode:
                self.result_lbl.config(text="覆盖模式", fg=ACC)
                self.info_lbl.config(text=f"散布线随鼠标移动 | 覆盖半径 {cover_radius:.0f}m")
                self.weapon_info_lbl.config(text=f"{wtag} · {traj} · 覆盖模式", fg=ACC)
            elif active:
                self.result_lbl.config(text=f"剩余 {rem:+.0f} dy | 仰角 {tgt:.2f}°", fg=GOOD)
                self.info_lbl.config(text=f"方位差 {daz:+.1f}° | 最大射程 {w['max_range']:.0f}m | 飞行 {flight_time(w, dist, tgt):.1f}s")
                self.weapon_info_lbl.config(text=f"{wtag} · {traj} · 飞行 {flight_time(w, dist, tgt):.1f}s", fg=ACC)
            else:
                self.result_lbl.config(text="按 F7 开始追踪", fg=MUTED); self.info_lbl.config(text="")
                self.weapon_info_lbl.config(text=f"{wtag} · {traj}", fg=MUTED)

        if self.s_spread_a > 0.02 and tgt is not None and dist > 0:
            focal = (self.sw / 2.0) / math.tan(math.radians(w["ads_fov"]) / 2.0)
            half = focal * (cover_radius / dist) * STYLE["spread_scale"]
            half = max(3, min(500, half))
            sc = fade_hex(STYLE["spread_color"], self.s_spread_a * 0.85)
            self.canvas.create_line(self.sx - half, self.sy, self.sx + half, self.sy, fill=sc, width=STYLE["spread_width"])
            dc = fade_hex(STYLE["spread_dot_color"], self.s_spread_a)
            self.canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill=dc, outline=dc)

        if self.sr > 1.5 and self.s_arrow_a > 0.02:
            angle = math.atan2(self.sy - cy, self.sx - cx)
            base = self.render_indicator(angle, self.s_arrow_a)
            ns = int(self.sr * 2.7); img = base.resize((ns, ns), Image.Resampling.LANCZOS)
            self._tk_img = ImageTk.PhotoImage(img); self.canvas.create_image(cx, cy, image=self._tk_img)

        if self.s_dot_a > 0.02:
            gx = max(0, min(self.sw, self.sx)); gy = max(0, min(self.sh, self.sy))
            dc = fade_hex(STYLE["dot_color"], self.s_dot_a * STYLE["opacity"])
            ds = STYLE["dot_size"]; cs = STYLE["cross_size"]
            self.canvas.create_oval(gx-ds, gy-ds, gx+ds, gy+ds, fill=dc, outline=dc)
            for a, b, cc, d in [(gx-cs, gy, gx-ds, gy), (gx+ds, gy, gx+cs, gy),
                                (gx, gy-cs, gx, gy-ds), (gx, gy+ds, gx, gy+cs)]:
                self.canvas.create_line(a, b, cc, d, fill=dc)
            if tgt is not None and active and not self.fire_mode:
                ft = flight_time(w, dist, tgt)
                tag = f"{wtag} {traj} {ft:.1f}s"
                ttx = min(self.sw - 160, gx + ds + 14)
                tty = max(20, gy - ds - 16)
                self.canvas.create_text(ttx, tty, text=tag, fill=dc, font=("KaiTi", 14, "bold"), anchor="w")

        if self.s_x_a > 0.02:
            xc = fade_hex(STYLE["x_color"], self.s_x_a); s = STYLE["x_size"]
            self.canvas.create_line(cx-s, cy-s, cx+s, cy+s, fill=xc, width=4)
            self.canvas.create_line(cx-s, cy+s, cx+s, cy-s, fill=xc, width=4)

        self.root.after(16, self.refresh)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        App().run()
    except Exception:
        import traceback
        root = tk.Tk(); root.withdraw(); messagebox.showerror("错误", traceback.format_exc())
