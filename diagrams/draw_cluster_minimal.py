# -*- coding: utf-8 -*-
"""Draw the simplified AECW agent-cluster structure as a PNG."""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2800, 1680
BG = "#F8FAFC"
TEXT = "#0F172A"
SECOND = "#334155"
MUTED = "#64748B"
BORDER = "#E2E8F0"
ARROW = "#475569"

HUMAN = "#B45309"
HUMAN_FILL = "#FFFBEB"
ORCH = "#1D4ED8"
ORCH_FILL = "#F8FAFC"
WORKER = "#0F766E"
WORKER_FILL = "#F0FDFA"
VERIFY = "#15803D"
VERIFY_FILL = "#F0FDF4"
STATE = "#6D28D9"
STATE_FILL = "#FAF5FF"
DECIDE = "#B91C1C"
DECIDE_FILL = "#FEF2F2"
RUNTIME = "#475569"

FONT_DIR = r"C:\Windows\Fonts"
_font_cache = {}


def F(size, bold=False):
    key = (size, bold)
    if key not in _font_cache:
        name = "msyhbd.ttc" if bold else "msyh.ttc"
        _font_cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size, index=0)
    return _font_cache[key]


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def tw(text, font):
    return d.textlength(text, font=font)


def wrap(text, font, maxw):
    lines = []
    for para in str(text).split("\n"):
        if para == "":
            lines.append("")
            continue
        cur = ""
        for ch in para:
            test = cur + ch
            if tw(test, font) <= maxw or cur == "":
                cur = test
            else:
                lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
    return lines


def shadow_round(x, y, w, h, r=24, off=6):
    d.rounded_rectangle([x + off, y + off + 2, x + w + off, y + h + off + 2],
                        radius=r, fill="#E2E8F0")


def panel(x, y, w, h, accent, fill, eyebrow, title, subtitle):
    shadow_round(x, y, w, h, r=26, off=7)
    d.rounded_rectangle([x, y, x + w, y + h], radius=26, fill=fill, outline=accent, width=2)
    d.text((x + 28, y + 20), eyebrow, font=F(14, True), fill=MUTED)
    d.text((x + 28, y + 42), title, font=F(27, True), fill=TEXT)
    d.text((x + 28, y + 82), subtitle, font=F(17, False), fill=MUTED)
    d.line([(x + 28, y + 108), (x + w - 28, y + 108)], fill=BORDER, width=1)


def card(x, y, w, h, title, body, accent, fill="#FFFFFF", title_size=21, body_size=18, dashed=False):
    d.rounded_rectangle([x + 4, y + 5, x + w + 4, y + h + 5], radius=16, fill="#E2E8F0")
    if dashed:
        d.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=fill, outline=accent, width=2)
        # simple dashed outline overlay (all four sides)
        for xx in range(x + 10, x + w - 10, 18):
            d.line([(xx, y), (xx + 8, y)], fill="#FFFFFF", width=3)
            d.line([(xx, y + h), (xx + 8, y + h)], fill="#FFFFFF", width=3)
        for yy in range(y + 10, y + h - 10, 18):
            d.line([(x, yy), (x, yy + 8)], fill="#FFFFFF", width=3)
            d.line([(x + w, yy), (x + w, yy + 8)], fill="#FFFFFF", width=3)
    else:
        d.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=fill, outline=accent, width=2)
    d.rectangle([x, y + 16, x + 6, y + h - 16], fill=accent)
    d.text((x + 20, y + 14), title, font=F(title_size, True), fill=TEXT)
    bf = F(body_size, False)
    lines = []
    for para in body:
        lines.extend(wrap(para, bf, w - 42))
    yy = y + 48
    for line in lines:
        d.text((x + 20, yy), line, font=bf, fill=SECOND)
        yy += 25


def chip(x, y, w, h, title, body, accent, fill="#FFFFFF", title_size=19, body_size=16):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=fill, outline=accent, width=2)
    d.text((x + 16, y + 12), title, font=F(title_size, True), fill=TEXT)
    bf = F(body_size, False)
    yy = y + 42
    for para in body:
        for line in wrap(para, bf, w - 32):
            d.text((x + 16, yy), line, font=bf, fill=SECOND)
            yy += 22


def dashed_segment(p1, p2, color, width=2, dash=10, gap=8):
    x1, y1 = p1
    x2, y2 = p2
    dist = math.hypot(x2 - x1, y2 - y1)
    if dist == 0:
        return
    dx = (x2 - x1) / dist
    dy = (y2 - y1) / dist
    pos = 0.0
    while pos < dist:
        end = min(pos + dash, dist)
        d.line([(x1 + dx * pos, y1 + dy * pos), (x1 + dx * end, y1 + dy * end)],
               fill=color, width=width)
        pos = end + gap


def dashed_polyline(points, color, width=2):
    for p1, p2 in zip(points[:-1], points[1:]):
        dashed_segment(p1, p2, color, width)


def arrowhead(p1, p2, color, size=14):
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    left = (p2[0] - size * math.cos(ang - 0.48), p2[1] - size * math.sin(ang - 0.48))
    right = (p2[0] - size * math.cos(ang + 0.48), p2[1] - size * math.sin(ang + 0.48))
    d.polygon([p2, left, right], fill=color)


def arrow(points, color=ARROW, width=3, dashed=False, head=True, underlay=True):
    if dashed:
        dashed_polyline(points, color, width)
    else:
        if underlay:
            d.line(points, fill=BG, width=width + 4, joint="curve")
        d.line(points, fill=color, width=width, joint="curve")
    if head:
        arrowhead(points[-2], points[-1], color)


def double_arrow(points, color=ARROW, width=3):
    d.line(points, fill=color, width=width, joint="curve")
    arrowhead(points[0], points[1], color)
    arrowhead(points[-1], points[-2], color)


def tag(text, x, y, color, bg="#FFFFFF", border=None, size=15, bold=True):
    f = F(size, bold)
    pad = 8
    w = tw(text, f) + pad * 2
    h = size + 9
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=bg, outline=border or bg, width=1)
    d.text((x + pad, y + 3), text, font=f, fill=color)
    return w


def badge(cx, cy, label, color):
    r = 18
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#FFFFFF", outline=color, width=2)
    f = F(12, True)
    d.text((cx - tw(label, f) / 2, cy - 8), label, font=f, fill=color)


# ---------------- header ----------------
d.rectangle([0, 0, W, 8], fill="#0F172A")
d.text((70, 38), "AECW · 精简结构（一页版）", font=F(50, True), fill=TEXT)
d.text((70, 106), "三域保留；一个源、一个门、一个验证；按风险分级，不再为每次改动套全套仪式。",
       font=F(23, False), fill=SECOND)
d.text((70, 146), "目标结构，不是 0.9.6 现状：当前仍有多视图、空 gate、32 行矩阵；本图是精简后的目标。",
       font=F(17, False), fill=MUTED)
d.line([(70, 196), (2730, 196)], fill=BORDER, width=1)

# ---------------- panels ----------------
panel(70, 300, 620, 1020, HUMAN, HUMAN_FILL, "DOMAIN 01 · HUMAN",
      "人类 · 方向与验收", "定方向 / 过一次门 / 例外裁决")
panel(770, 300, 1160, 1020, ORCH, ORCH_FILL, "DOMAIN 02 · CLUSTER",
      "Agent 集群 · 执行", "编排者单写；worker 隔离；验证按需")
panel(2010, 300, 720, 1020, STATE, STATE_FILL, "DOMAIN 03 · WORKSPACE",
      "工作区 · 一个源", "state / evidence / product / 决定记录")

# ---------------- human ----------------
hx, hw = 100, 560
card(hx, 440, hw, 150, "定方向",
     ["目的 / 非目标 / 停止 / 预算", "不指定实现路线"], HUMAN)
card(hx, 610, hw, 150, "过一次门",
     ["阶段或发布：接受 / 拒绝 / 有条件", "一次决定，不逐单审批"], HUMAN)
card(hx, 780, hw, 150, "例外裁决",
     ["S1/S2、不可逆、范围变更", "只处理例外，不做常规分诊"], HUMAN)
card(hx, 950, hw, 160, "不做什么",
     ["不逐条核事实 / 不维护台账", "不替集群写方案 / 不每门签字"], MUTED, "#FFFFFF", 20, 17)
card(hx, 1130, hw, 140, "直读",
     ["state / evidence / verify", "不经集群摘要"], STATE, "#FFFFFF", 20, 17)
d.text((100, 1290), "人类只保留“批”位；其余在边界内默认相信。",
       font=F(16, True), fill=MUTED)

# ---------------- cluster ----------------
cx, cw = 810, 1080
card(cx, 440, cw, 170, "编排者 · 单写者",
     ["拆单 / 派发 / 合并 / 写 state",
      "工单：目标 / 允许路径 / 验收 / 预算",
      "只有编排者写 mainline 与当前状态"], ORCH, "#FFFFFF", 24, 18)
# work-order bus
d.rounded_rectangle([cx + 4, 635, cx + cw + 4, 715], radius=14, fill="#E2E8F0")
d.rounded_rectangle([cx, 630, cx + cw, 710], radius=14, fill="#F8FAFC", outline=ORCH, width=2)
d.rectangle([cx, 646, cx + 6, 694], fill=ORCH)
d.text((cx + 22, 642), "工单 / 结果", font=F(20, True), fill=TEXT)
d.text((cx + 22, 672), "目标 · 路径 · 验收 · 预算  →  patch + 证据 + 未决项", font=F(17, False), fill=SECOND)

card(cx, 750, 520, 210, "Worker × N · 标准路径",
     ["隔离 worktree；只读工单",
      "只交 patch + 证据 + 未决项",
      "不写 state / mainline"], WORKER, "#FFFFFF", 21, 18)
card(cx + 560, 750, 520, 210, "独立验证 · 高风险才启用",
     ["新鲜上下文；只读产物 / 日志 / 哈希",
      "不改代码；输出 verdict",
      "标准路径跳过，不设常设角色"], VERIFY, "#FFFFFF", 21, 18, dashed=True)

# risk ladder
d.text((cx, 990), "按风险分级，不套全套", font=F(20, True), fill=MUTED)
chip(cx, 1025, 520, 120, "标准（大多数）",
     ["worker + tests/probe → 人类验收",
      "不 freeze / 不独立验证 / 不写 gate 文档"], VERIFY, "#F0FDF4", 19, 16)
chip(cx + 560, 1025, 520, 120, "高风险（安全/发布/不可逆）",
     ["+ 独立验证 + freeze hash",
      "+ 一次决定记录"], DECIDE, "#FEF2F2", 19, 16)
d.text((cx, 1170), "红队 / 策展：按需临时指定，不设常设角色。",
       font=F(16, True), fill=MUTED)

# ---------------- workspace ----------------
wx, ww = 2040, 660
card(wx, 440, ww, 160, "state.json · 唯一当前状态",
     ["stage / release / owner / links", "其他当前值由它生成"], STATE, "#FFFFFF", 21, 18)
card(wx, 620, ww, 180, "evidence/ · 只追加",
     ["tests / probe 日志、哈希", "verify 记录：绑定当前树"], STATE, "#FFFFFF", 21, 18)
card(wx, 820, ww, 150, "product",
     ["代码 / 测试 / 安装", "repo root；不混治理文档"], STATE, "#FFFFFF", 21, 18)
card(wx, 990, ww, 180, "决定记录 · 唯一的门",
     ["事实 / 证据链接 / 条件 / 剩余风险",
      "人类签；编排者写入"], DECIDE, "#FFF7F7", 22, 17)
card(wx, 1190, ww, 100, "STATUS · 生成视图",
     ["只读，不手改"], MUTED, "#FFFFFF", 19, 16)
d.text((wx, 1290), "旧 board / release / manifest / 32 行矩阵：合并或归档。",
       font=F(15, False), fill=MUTED)

# ---------------- boundaries & interfaces ----------------
dashed_polyline([(730, 330), (730, 1290)], "#CBD5E1", 2)
dashed_polyline([(1970, 330), (1970, 1290)], "#CBD5E1", 2)
tag("授权边界", 686, 310, HUMAN, "#FFFFFF", "#FCD34D", 13, False)
tag("写入边界", 1918, 310, ORCH, "#FFFFFF", "#BFDBFE", 13, False)

arrow([(690, 480), (770, 480)], HUMAN, 3)
badge(730, 480, "I1", HUMAN)
arrow([(770, 1220), (690, 1220)], HUMAN, 3)
badge(730, 1220, "I2", HUMAN)
arrow([(1930, 480), (2010, 480)], ORCH, 3)
badge(1970, 480, "I3", ORCH)
arrow([(2010, 1220), (1930, 1220)], STATE, 3)
badge(1970, 1220, "I4", STATE)

# I5 direct read
arrow([(2370, 300), (2370, 240), (380, 240), (380, 300)], STATE, 2, dashed=True)
tag("I5 人类直读 state / evidence（不经摘要）", 990, 208, STATE, "#FFFFFF", "#DDD6FE", 15, False)

# internal cluster arrows
arrow([(1050, 610), (1050, 630)], ORCH, 3)
double_arrow([(1050, 710), (1050, 750)], ORCH, 3)
tag("工单 / 结果", 1064, 714, MUTED, "#FFFFFF", "#E2E8F0", 13, False)
dashed_segment((1330, 855), (1370, 855), VERIFY, 2, 10, 7)
arrowhead((1330, 855), (1370, 855), VERIFY, 11)
tag("高风险", 1300, 820, VERIFY, "#FFFFFF", "#BBF7D0", 12, False)
dashed_polyline([(1890, 750), (1905, 750), (1905, 520), (1890, 520)], VERIFY, 2)
arrowhead((1905, 520), (1890, 520), VERIFY, 11)
tag("verdict", 1912, 585, VERIFY, "#FFFFFF", "#BBF7D0", 12, False)

# ---------------- bottom rules ----------------
ry = 1380
d.rounded_rectangle([70, ry, 2730, ry + 120], radius=18, fill="#FFFFFF", outline="#CBD5E1", width=2)
d.text((95, ry + 16), "精简规则", font=F(21, True), fill=TEXT)
rules = [
    ("一个源", ["state.json；STATUS 只读生成"], STATE),
    ("一个门", ["人类决定记录；没有空模板"], DECIDE),
    ("一个验证", ["tests + probe；高风险加独立复核"], VERIFY),
    ("按风险分级", ["标准默认；高风险才加 freeze/验证"], HUMAN),
]
rx = 300
for title, body, color in rules:
    d.text((rx, ry + 18), title, font=F(18, True), fill=color)
    d.text((rx, ry + 48), body[0], font=F(15, False), fill=SECOND)
    rx += 600

d.text((70, 1530), "运行底座：DSH workflow 扇出 · git worktree · 原子写/锁 · tests/probe",
       font=F(16, False), fill=MUTED)
d.line([(70, 1565), (2730, 1565)], fill=BORDER, width=1)
d.text((70, 1580), "AECW · 精简结构 · 2026-11-06 · 目标态；不宣称已是 0.9.6 现状。",
       font=F(15, False), fill=MUTED)

out = os.path.join(os.path.dirname(__file__), "cluster-minimal-structure.png")
img.save(out, "PNG", optimize=True)
print(out, img.size)
