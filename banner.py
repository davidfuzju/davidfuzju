#!/usr/bin/env python3
"""生成 assets/banner.png —— Tokendivers 横幅。立意与术语见 CONTEXT.md。

核心机制：**照度决定显形，不是深度**。

  这片海一直是 token 组成的，但只有海底那一点光照到的地方能看见真面目。
  灯外的洋流不是「还没变成 token」，是「你看不见它是 token」。
  于是从光源往外，依次退化：
      长短随机的 token + 冷暖分色  →  无冷暖  →  完全连续的 line。
  这就是 Divers 的定义落在画面上：能看见介质本身的人 —— 在光照到的范围内。

  场景画在一张更大的画布上（BIG），再用 viewBox 裁出横幅。
  这样光源和洋流都能延伸到画外，边缘不会露馅，构图焦点得以压到右下角。

跑一次: python3 banner.py（依赖 rsvg-convert）
"""
import math, random, subprocess, pathlib

W, H = 1200, 420               # 输出（裁切窗口）
BIGW, BIGH = 1900, 720         # 实际绘制画布
VX, VY = 330, 160              # 裁切窗口在大画布上的左上角
FRONT_X = 1110                 # 锋面（世界坐标）

TEXT = dict(kicker="TOKENDIVERS", name="David FU",
            tagline="Diving deep in an ocean of tokens.")

WHITE = (236, 252, 255)
SHALLOW_TOP = (116, 156, 190)  # 灯外的线：浅海
SHALLOW_BOT = (18, 30, 44)     # 灯外的线：深渊，随背景一起沉进黑里
MIDSEA = (132, 168, 210)       # 过渡：切开了，但还看不出冷暖
COLD = ((178, 198, 255), (92, 116, 210))
WARM = ((255, 226, 168), (196, 142, 50))

# 平行曲线族：一条基曲线上下平移出一整族，形状相同、间距恒定。
# 让每条线各自弯曲的话就不平行了，叠起来会读成一张曲面。
CURVE = ((26., 230., .6), (9., 105., 2.4), (14., 360., 1.1))


def smoothstep(a, b, t):
    t = max(0., min(1., (t - a) / (b - a)))
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def hexc(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v))) for v in c)


def curve(x):
    return sum(a * math.sin(x / w + p) for a, w, p in CURVE)


def curve_d(x):
    return sum(a / w * math.cos(x / w + p) for a, w, p in CURVE)


def front_at(y):
    """锋面会蜿蜒（meander），冷暖交界才呈舌状互相侵入。"""
    return FRONT_X + 52 * math.sin(y / 74.0 + .7) + 24 * math.sin(y / 31.0)


def vel(x, y, dirn, ph):
    """穿过锋面后冷水重 → 下沉、暖水轻 → 上升，一次楔入换层。
    做成持续位移的话，满屏平行斜线会读成一块倾斜的地板。"""
    vx, vy = float(dirn), 0.0
    fx = front_at(y)
    cross = (x - fx) * dirn
    vy += dirn * math.exp(-((cross - 70.) / 75.) ** 2) * .58
    vy += math.exp(-((x - fx) / 120.0) ** 2) * .22 * math.sin(y / 34.0 + dirn * 2.3)
    vy += .055 * math.sin(x / 210.0 + ph)
    n = math.hypot(vx, vy) or 1.0
    return vx / n, vy / n


# ── 冷暖温度场（只在被照亮处才显现为颜色） ───────────────────────────────
GS = 5
GW, GH = BIGW // GS + 2, BIGH // GS + 2


def build_field():
    acc = [[0.0] * GW for _ in range(GH)]
    wgt = [[0.0] * GW for _ in range(GH)]
    rnd = random.Random(13)
    y0 = -80.0
    while y0 < BIGH + 80:
        for x0, dirn in ((-190.0, +1), (BIGW + 190.0, -1)):
            ph = rnd.uniform(0, 6.283)
            x, y = x0, y0
            for _ in range(1100):
                vx, vy = vel(x, y, dirn, ph)
                x += vx * 3.4
                y += vy * 3.4
                if not (-210 < x < BIGW + 210 and -100 < y < BIGH + 100):
                    break
                gx, gy = int(x / GS), int(y / GS)
                if 0 <= gx < GW and 0 <= gy < GH:
                    # 穿越衰减：每股流在自己一侧占优，只在交汇带交错
                    cr = (x - front_at(y)) * dirn
                    wt = 1.0 if cr < 0 else math.exp(-cr / 175.0)
                    acc[gy][gx] += -dirn * wt
                    wgt[gy][gx] += wt
        y0 += 5.5
    F = [[(acc[j][i] / wgt[j][i]) if wgt[j][i] > 0
          else (1.0 if i * GS > FRONT_X else -1.0)
          for i in range(GW)] for j in range(GH)]
    for _ in range(2):
        G = [row[:] for row in F]
        for j in range(GH):
            for i in range(GW):
                t, c = 0.0, 0
                for dj in (-1, 0, 1):
                    for di in (-1, 0, 1):
                        jj, ii = j + dj, i + di
                        if 0 <= jj < GH and 0 <= ii < GW:
                            t += G[jj][ii]
                            c += 1
                F[j][i] = t / c
    return F


def sample(F, x, y):
    return F[min(GH - 1, max(0, int(y / GS)))][min(GW - 1, max(0, int(x / GS)))]


# ── 光源（世界坐标） ─────────────────────────────────────────────
LAMP = (1189.3, 535.7)   # 光源（世界坐标）：圆心在窗口 86% 高，只露上方 2/3
CORE, HALO = 66., 140.         # 深海一粟：光只照亮很小一片


def illum(x, y):
    """照度：以光源为心的正圆径向光晕。水下的灯被水散射，本来就是个球，
    锥形硬边光柱是空气里才有的东西。核心 + 散射拖尾两层叠加。
    这一个量驱动全部：切多细、有没有冷暖、多清晰、多虚。"""
    dx, dy = x - LAMP[0], y - LAMP[1]
    d = math.hypot(dx, dy)
    return min(1., .88 * math.exp(-(d / CORE) ** 2)
               + .38 * math.exp(-(d / HALO) ** 2))


def ocean():
    F = build_field()
    rnd = random.Random(7)
    groups, ROW, BW, STEP = {}, 8.6, 4.4, 2.2
    base = -70.0
    while base < BIGH + 70:
        pts, x = [], -60.0
        while x < BIGW + 60:
            pts.append((x, base + curve(x)))
            x += STEP
        # 深度取整行的 base，而不是每段的实际 y —— 段与段之间只要有一丝色差，
        # 量化就会把它们拆进不同 path，接缝处又会烧出砖墙纹理。
        dep_row = max(0., min(1., (base - VY) / H))
        # 线色跟背景同一条曲线往黑里沉：前段慢、后段快，底部与全黑背景合一
        unlit = lerp(SHALLOW_TOP, SHALLOW_BOT, dep_row ** .80)
        i, seg_left, seg_warm = 0, 0, False
        while i < len(pts) - 1:
            lx, ly = pts[i]
            il = illum(*pts[min(len(pts) - 1, i + 9)])   # 前瞻约 20px，别用段起点
            # token 长度与照度无关：凡是显形的地方，都是正常比例的长短随机。
            # 之前把长度绑在照度上（照度越低越长），光晕外围整圈被拉成清一色的长条。
            # 照度只管缝宽（见下方 vgap）：灯外缝为 0、同色合并 → 连续的线。
            r = rnd.random()
            mult = .54 if r < .38 else (.95 if r < .92 else 1.78)   # 短 38% / 中 54% / 长 8%
            if il < .05:
                tlen = 46.          # 缝宽恒为 0，切多长都看不出来；取长段省体积
            else:
                tlen = 20. * mult * rnd.uniform(.85, 1.18)
            polar = smoothstep(.38, .78, il)      # 冷暖只在照亮处显现

            if seg_left <= 0:
                seg_left = rnd.randint(3, 15)
                t = sample(F, lx, max(0., min(float(BIGH), ly - curve(lx))))
                seg_warm = rnd.random() < .50 + .28 * math.tanh(t * 1.8 + .30)
            seg_left -= 1

            # 段长必须封顶：洋流横贯全幅，起点必然在光照外，
            # 若照度低就一路画到末尾，整条线一段画完会直接跨过光照区，
            # 照亮处根本没机会切分。灯外的段照样切，只是缝宽为 0、
            # 同色合并成一个 path —— 视觉上仍是连续的线。
            j = min(len(pts) - 1, i + max(2, round((min(tlen, 46.) - BW) / STEP)))
            mx, my = pts[(i + j) // 2]
            if -20 < my < BIGH + 20:
                im = illum(mx, my)
                col = lerp(unlit, MIDSEA, smoothstep(.17, .44, im))
                if polar > .01:
                    col = lerp(col, lerp(*(WARM if seg_warm else COLD), dep_row), polar)
                col = lerp(col, WHITE, smoothstep(.62, 1., im) * .38)
                op = .32 + .62 * smoothstep(.17, .74, im)
                # 海底全黑：灯外的线到最底部连透明度一起退掉，只剩灯照到的部分
                op *= 1 - smoothstep(.46, .78, dep_row) * (1 - smoothstep(.10, .45, im))
                tier = 0 if im > .52 else (1 if im > .26 else 2)
                key = (tier, hexc(tuple(int(v / 6) * 6 for v in col)),
                       round(min(op, .95) / .04) * .04)
                # 灯外的段远多于灯内，但曲线在几十像素内近乎直线 ——
                # 抽稀掉中间点，抵消段数增长带来的体积
                st = 1 if tier == 0 else (2 if tier == 1 else 4)
                sub = pts[i:j + 1:st]
                if sub[-1] != pts[j]:
                    sub.append(pts[j])
                groups.setdefault(key, []).append(
                    "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in sub))
            # 线帽各向外伸 BW/2，间距要把它算进去，否则接缝处 alpha 叠加会烧出白点
            vgap = smoothstep(.05, .45, il) * (
                rnd.uniform(8., 16.) if seg_left <= 0 else rnd.uniform(1.8, 3.4))
            adv = max(1, round((BW + vgap) / STEP))
            if vgap < .5:
                # 灯外的段本就同色同透明度、合并在一个 path 里。让它们略微重叠：
                # 圆帽严丝合缝地对接时，两侧的抗锯齿加起来不足 1，会烧出一条竖直暗带；
                # 同一 path 的自重叠不叠加 alpha，所以重叠是安全的。
                adv = max(1, adv - 1)
            i = j + adv
        base += ROW
    out = []
    for tier, fid in ((2, "blurB"), (1, "blurA"), (0, None)):
        body = [f'<path d="{"".join(v)}" stroke="{c}" stroke-width="{BW}" '
                f'stroke-linecap="round" fill="none" opacity="{o:.3f}"/>'
                for (tr, c, o), v in sorted(groups.items()) if tr == tier]
        if not body:
            continue
        inner = "\n   ".join(body)
        out.append(f'<g filter="url(#{fid})">\n   {inner}\n  </g>' if fid else inner)
    return "\n  ".join(out)


def beam_shape():
    """光源：正圆径向发散。外层是被水散射开的光雾，内层是光源本体的亮核。"""
    cx, cy = LAMP
    return (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{HALO * 1.7:.0f}" fill="url(#glow)"/>'
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="9" fill="url(#core)"/>')


TX, TY = VX + 80, VY + 232          # 文字锚点（世界坐标）
SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="{VX} {VY} {W} {H}">
 <defs>
  <linearGradient id="bg" x1="0" y1="{VY}" x2="0" y2="{VY + H}"
     gradientUnits="userSpaceOnUse">
   <stop offset="0%" stop-color="#174a6b"/>
   <stop offset="12%" stop-color="#103854"/>
   <stop offset="28%" stop-color="#08223a"/>
   <stop offset="46%" stop-color="#03101e"/>
   <stop offset="64%" stop-color="#01050a"/>
   <stop offset="78%" stop-color="#000000"/>
   <stop offset="100%" stop-color="#000000"/>
  </linearGradient>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
   <stop offset="0%" stop-color="#eefbff" stop-opacity=".70"/>
   <stop offset="4%" stop-color="#c8edfc" stop-opacity=".48"/>
   <stop offset="18%" stop-color="#94d3f0" stop-opacity=".36"/>
   <stop offset="38%" stop-color="#5eaad6" stop-opacity=".16"/>
   <stop offset="66%" stop-color="#3a86b8" stop-opacity=".05"/>
   <stop offset="100%" stop-color="#2a6e9e" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="core" cx="50%" cy="50%" r="50%">
   <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
   <stop offset="22%" stop-color="#ffffff" stop-opacity="1"/>
   <stop offset="55%" stop-color="#d8f3ff" stop-opacity=".45"/>
   <stop offset="100%" stop-color="#a8def6" stop-opacity="0"/>
  </radialGradient>
  <filter id="blurB" x="-4%" y="-4%" width="108%" height="108%">
   <feGaussianBlur stdDeviation="1.4"/>
  </filter>
  <filter id="blurA" x="-4%" y="-4%" width="108%" height="108%">
   <feGaussianBlur stdDeviation="0.7"/>
  </filter>
  <filter id="halo" x="-35%" y="-35%" width="170%" height="170%">
   <feGaussianBlur stdDeviation="7"/>
  </filter>
 </defs>

 <rect x="{VX}" y="{VY}" width="{W}" height="{H}" fill="url(#bg)"/>
 <g>
  {ocean()}
 </g>
 {beam_shape()}


 <g filter="url(#halo)" opacity=".92">
  <rect x="{TX - 28}" y="{TY - 120}" width="3" height="184" fill="#02121e"/>
  <text x="{TX + 4}" y="{TY - 86}" font-family="Menlo, monospace" font-size="17"
        letter-spacing="4.5" fill="#02121e">{TEXT['kicker']}</text>
  <text x="{TX}" y="{TY}" font-family="Helvetica Neue, Helvetica, Arial" font-size="78"
        font-weight="600" letter-spacing="-2.2" fill="#02121e">{TEXT['name']}</text>
  <text x="{TX + 4}" y="{TY + 48}" font-family="Helvetica Neue, Helvetica, Arial"
        font-size="22" fill="#02121e">{TEXT['tagline']}</text>
 </g>
 <rect x="{TX - 28}" y="{TY - 120}" width="3" height="184" fill="#4cc9f0"/>
 <text x="{TX + 4}" y="{TY - 86}" font-family="Menlo, monospace" font-size="17"
       letter-spacing="4.5" fill="#7fdcff">{TEXT['kicker']}</text>
 <text x="{TX}" y="{TY}" font-family="Helvetica Neue, Helvetica, Arial" font-size="78"
       font-weight="600" letter-spacing="-2.2" fill="#f2fbff">{TEXT['name']}</text>
 <text x="{TX + 4}" y="{TY + 48}" font-family="Helvetica Neue, Helvetica, Arial"
       font-size="22" fill="#bcdcec">{TEXT['tagline']}</text>
</svg>'''

root = pathlib.Path(__file__).parent
(root / "assets").mkdir(exist_ok=True)
src = root / "assets/banner.svg"
src.write_text(SVG)
subprocess.run(["rsvg-convert", "-w", str(W * 2), str(src),
                "-o", str(root / "assets/banner.png")], check=True)
print("ok", src.stat().st_size // 1024, "KB svg")
