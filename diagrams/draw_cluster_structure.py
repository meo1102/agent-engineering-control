# -*- coding: utf-8 -*-
"""Draw the AECW agent-cluster conceptual structure diagram as a PNG."""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 2820
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
STOP = "#B91C1C"
STOP_FILL = "#FEF2F2"
RUNTIME = "#475569"
RUNTIME_FILL = "#F1F5F9"

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
    d.text((x + 30, y + 20), eyebrow, font=F(14, True), fill=MUTED)
    d.text((x + 30, y + 42), title, font=F(26, True), fill=TEXT)
    d.text((x + 30, y + 82), subtitle, font=F(16, False), fill=MUTED)
    d.line([(x + 30, y + 108), (x + w - 30, y + 108)], fill=BORDER, width=1)


def card(x, y, w, h, title, body, accent, fill="#FFFFFF", title_size=20, body_size=16):
    d.rounded_rectangle([x + 4, y + 5, x + w + 4, y + h + 5], radius=16, fill="#E2E8F0")
    d.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=fill, outline=accent, width=2)
    d.rectangle([x, y + 16, x + 6, y + h - 16], fill=accent)
    d.text((x + 22, y + 14), title, font=F(title_size, True), fill=TEXT)
    bf = F(body_size, False)
    lines = []
    for para in body:
        lines.extend(wrap(para, bf, w - 44))
    yy = y + 48
    for line in lines:
        d.text((x + 22, yy), line, font=bf, fill=SECOND)
        yy += 24


def chip(x, y, w, h, title, body, accent, fill="#FFFFFF"):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=fill, outline=accent, width=2)
    d.text((x + 18, y + 14), title, font=F(16, True), fill=TEXT)
    bf = F(14, False)
    yy = y + 44
    for para in body:
        for line in wrap(para, bf, w - 36):
            d.text((x + 18, yy), line, font=bf, fill=SECOND)
            yy += 21


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


def tag(text, x, y, color, bg="#FFFFFF", border=None, size=15, bold=True):
    f = F(size, bold)
    pad = 8
    w = tw(text, f) + pad * 2
    h = size + 9
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=bg, outline=border or bg, width=1)
    d.text((x + pad, y + 3), text, font=f, fill=color)
    return w


def badge(cx, cy, label, color):
    r = 19
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#FFFFFF", outline=color, width=2)
    f = F(12, True)
    d.text((cx - tw(label, f) / 2, cy - 8), label, font=f, fill=color)


def legend_item(x, y, color, label):
    d.rounded_rectangle([x, y, x + 18, y + 18], radius=4, fill=color)
    d.text((x + 26, y - 2), label, font=F(15, False), fill=SECOND)


# ---------------- header ----------------
d.rectangle([0, 0, W, 8], fill="#0F172A")
d.text((70, 40), "AECW · Agent 集群概念结构图", font=F(52, True), fill=TEXT)
d.text((70, 112), "三域责任 + 四平面 + 治理内核：人类定方向，集群在边界内实现，工作区承载状态/证据/记忆",
       font=F(23, False), fill=SECOND)
d.text((70, 152),
       "概念结构图，不是部署图；当前 DSH 运行时是短生命周期 batch cluster，L 模式。",
       font=F(18, False), fill=MUTED)
d.line([(70, 205), (2490, 205)], fill=BORDER, width=1)

# ---------------- panels ----------------
panel(70, 300, 620, 1700, HUMAN, HUMAN_FILL, "DOMAIN 01 · HUMAN",
      "人类域 · 权威", "方向 / 边界 / 阶段门 / 最终验收")
panel(780, 300, 1040, 1700, ORCH, ORCH_FILL, "DOMAIN 02 · CLUSTER",
      "Agent 集群 · 执行主体", "编排者单写；worker 隔离生产；验证者独立复核")
panel(1910, 300, 600, 1700, STATE, STATE_FILL, "DOMAIN 03 · WORKSPACE",
      "项目工作区 · 状态与落地", "当前状态 / 证据 / 记忆 / 产品")

# ---------------- human cards ----------------
hx, hw = 100, 560
card(hx, 410, hw, 160, "方向与边界",
     ["目的 / 非目标 / 失败定义", "S1–S4 / 预算 / 停止条件"], HUMAN)
card(hx, 590, hw, 140, "阶段授权",
     ["宪章确认 + 蓝图批准", "只授权一个阶段"], HUMAN)
card(hx, 750, hw, 140, "例外与裁决",
     ["S1/S2 裁决", "重大遗留 / 范围变更"], HUMAN)
card(hx, 910, hw, 140, "真实使用验收",
     ["接受 / 拒绝 / 有条件", "基于实际使用，不是摘要"], HUMAN)
card(hx, 1070, hw, 180, "不可委托",
     ["方向 / 边界 / 验收 / charter 批准", "agent 不得代写或自批"], STOP, "#FFF7F7")
card(hx, 1270, hw, 140, "注意力合同",
     ["只过阶段/验收门；S1/S2 另计", "常规分诊 / 台账交给集群"], HUMAN)
card(hx, 1430, hw, 120, "不替代集群",
     ["不逐单审批 / 不逐条核事实", "不替集群写蓝图/拆任务"], HUMAN)
card(hx, 1570, hw, 140, "直读权",
     ["STATUS / attestation / evidence", "可绕过集群摘要直接读"], STATE)
card(hx, 1730, hw, 110, "具名 owner",
     ["没有具名人类所有者，不得发布"], HUMAN)
d.text((100, 1880), "人类保留“批”位；集群的“决”只能在已授权范围内。",
       font=F(16, True), fill=MUTED)

# ---------------- cluster ----------------
cx, cw = 810, 980
card(cx, 410, cw, 180, "编排者 · 控制面",
     ["run manifest · 工单拆解 · 写集/依赖校验",
      "合并队列 · 单写者 · 状态写回",
      "人类门禁前不合并 mainline"], ORCH, "#FFFFFF", 22, 17)
# bus is a band, not a normal card
d.rounded_rectangle([cx + 4, 625, cx + cw + 4, 745], radius=16, fill="#E2E8F0")
d.rounded_rectangle([cx, 620, cx + cw, 740], radius=16, fill="#F8FAFC", outline=ORCH, width=2)
d.rectangle([cx, 636, cx + 6, 724], fill=ORCH)
d.text((cx + 22, 634), "工单 / 结果总线 · 证据面", font=F(20, True), fill=TEXT)
bf = F(16, False)
d.text((cx + 22, 666), "work-order.json → result.json → verdict.json → VA-*.json", font=bf, fill=SECOND)
d.text((cx + 22, 694), "文件协议；worker 无点对点消息，所有协调经编排者", font=bf, fill=SECOND)

card(cx, 770, 480, 270, "实现 worker × N · 执行面",
     ["C1=1 个实现者｜C2=N 个并行，写集不重叠",
      "隔离 worktree；只读工单；只交 patch + result",
      "不写 mainline / state / STATUS / ledger"], WORKER, "#FFFFFF", 21, 16)
card(cx + 500, 770, 480, 270, "独立验证者 · 证据边界",
     ["新鲜上下文；只读工单 / diff / 日志 / 哈希",
      "不读实现者推理；不改代码；重跑验收",
      "检查测试是否被削弱"], VERIFY, "#FFFFFF", 21, 16)
card(cx, 1070, 480, 220, "红队（可选）",
     ["高风险才启动；攻击假设 / 边界 / 反例",
      "输出 dissent；不替代独立验证"], VERIFY, "#FFFFFF", 20, 16)
card(cx + 500, 1070, 480, 220, "策展（可选）",
     ["复盘 / 记忆候选 / 负记忆",
      "不直接激活；协议变更走 CR"], STATE, "#FFFFFF", 20, 16)

card(cx, 1320, cw, 190, "集成 / 合并队列 · 单写者",
     ["串行 apply patch；冲突 → 新工单",
      "全量测试 + verify；生成 attestation",
      "人类门禁；失败 → 退回 / 补证"], ORCH, "#FFFFFF", 22, 17)

d.text((cx, 1545), "四条不变量", font=F(18, True), fill=MUTED)
chip(cx, 1580, 480, 85, "单写者", ["只有编排者写 mainline/state"], ORCH)
chip(cx + 500, 1580, 480, 85, "独立验证", ["验证者不读实现者推理"], VERIFY)
chip(cx, 1685, 480, 85, "无工单不开工", ["目标/路径/验收/预算"], WORKER)
chip(cx + 500, 1685, 480, 85, "变更走 change", ["范围/判据变更 → 新 freeze"], HUMAN)
d.text((cx, 1810), "集群不能改方向/判据/门禁；只能提议 + 举证。",
       font=F(16, True), fill=STOP)

# ---------------- workspace ----------------
wx, ww = 1940, 540
card(wx, 410, ww, 140, "当前状态",
     ["state.json（唯一状态源）", "STATUS（视图）/ stage machine"], STATE)
card(wx, 570, ww, 140, "治理记录",
     ["ledger / criteria / gates", "human decisions / change"], STATE)
card(wx, 730, ww, 160, "证据",
     ["run manifests / results / logs", "attestations VA-* / hashes"], STATE)
card(wx, 910, ww, 160, "记忆",
     ["memory candidates / ADR", "negative memory / rejected"], STATE)
card(wx, 1090, ww, 140, "产品",
     ["repo root / tests", "DSH plugin / package"], STATE)
card(wx, 1250, ww, 160, "落地",
     ["DSH host / real use", "acceptance evidence / feedback"], STATE)
card(wx, 1430, ww, 230, "写入规则",
     ["只有编排者写当前状态",
      "worker 只写 worktree/result",
      "证据只追加；旧文档标 SUPERSEDED",
      "记忆候选不直接激活"], STATE, "#FFFFFF", 20, 16)
card(wx, 1680, ww, 100, "人类可直读",
     ["STATUS / attestation / evidence"], HUMAN, "#FFFDF5", 18, 15)
card(wx, 1800, ww, 120, "历史与代谢",
     ["拒绝 patch / 失败 run / 旧基线保留", "可归档，不可改写"], MUTED, "#FFFFFF", 18, 15)

# ---------------- interfaces ----------------
# domain boundary lines
dashed_polyline([(735, 330), (735, 1980)], "#CBD5E1", 2)
dashed_polyline([(1865, 330), (1865, 1980)], "#CBD5E1", 2)
tag("授权边界", 692, 308, HUMAN, "#FFFFFF", "#FCD34D", 13, False)
tag("写入边界", 1822, 308, ORCH, "#FFFFFF", "#BFDBFE", 13, False)

arrow([(690, 450), (780, 450)], HUMAN, 3)
badge(735, 450, "I1", HUMAN)
arrow([(780, 1850), (690, 1850)], HUMAN, 3)
badge(735, 1850, "I2", HUMAN)
arrow([(1820, 450), (1910, 450)], ORCH, 3)
badge(1865, 450, "I3", ORCH)
arrow([(1910, 1850), (1820, 1850)], STATE, 3)
badge(1865, 1850, "I4", STATE)

# I5: human can read workspace directly
arrow([(2210, 300), (2210, 250), (380, 250), (380, 300)], STATE, 2, dashed=True)
tag("I5 人类可直读 STATUS / attestation（不经集群摘要）",
    900, 216, STATE, "#FFFFFF", "#DDD6FE", 15, False)

# ---------------- governance kernel ----------------
gx, gy, gw, gh = 70, 2080, 2420, 220
shadow_round(gx, gy, gw, gh, r=22, off=6)
d.rounded_rectangle([gx, gy, gx + gw, gy + gh], radius=22, fill=STOP_FILL, outline="#FCA5A5", width=2)
d.text((gx + 30, gy + 22), "治理内核 · 边界与拒绝权", font=F(26, True), fill=STOP)
d.text((gx + 30, gy + 60), "不是文档集合；是会让动作失败的检查、状态机与哈希边界。",
       font=F(16, False), fill=MUTED)
chips = [
    ("freeze / start", ["哈希边界；无开工令不执行"]),
    ("verify / gate", ["唯一通过类证据；attestation"]),
    ("lock / journal", ["原子台账；崩溃恢复"]),
    ("probe", ["运行态身份/健康；不替代真机"]),
    ("criteria / ledger", ["判据/事实/异议；S1/S2"]),
    ("change", ["范围/判据变更 → 新 freeze/start"]),
]
chx = gx + 30
chw = 365
for i, (title, body) in enumerate(chips):
    chip(chx, gy + 94, chw, 100, title, body, STOP, "#FFFFFF")
    chx += chw + 18

# governance constrains the three domains
for x in (380, 1250, 2120):
    arrow([(x, gy), (x, 2000)], STOP, 2, dashed=True, head=True, underlay=False)
tag("约束 / 拒绝权", 1170, 2028, STOP, "#FFFFFF", "#FECACA", 14, False)

# ---------------- runtime substrate ----------------
rx, ry, rw, rh = 70, 2360, 2420, 200
shadow_round(rx, ry, rw, rh, r=22, off=6)
d.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=22, fill=RUNTIME_FILL, outline="#CBD5E1", width=2)
d.text((rx + 30, ry + 22), "DSH 运行时底座", font=F(24, True), fill=TEXT)
d.text((rx + 30, ry + 58), "短生命周期 batch：workflow 扇出 + worktree + 文件/锁；不是常驻集群。",
       font=F(16, False), fill=MUTED)
runtime_chips = [
    ("workflow", ["短生命周期 fan-out"]),
    ("git worktree", ["隔离写域"]),
    ("filesystem", ["工件 / 状态"]),
    ("Node / Git", ["测试 / 提交"]),
    ("sandbox", ["workspace-write"]),
    ("lock / journal", ["原子写 / 恢复"]),
]
chx = rx + 30
for i, (title, body) in enumerate(runtime_chips):
    chip(chx, ry + 88, 365, 84, title, body, RUNTIME, "#FFFFFF")
    chx += 365 + 18
tag("L 模式 · local-trusted", 2100, ry + 22, STOP, "#FFFFFF", "#FECACA", 14, False)
d.text((rx + 30, ry + 180), "没有持久队列 / 点对点消息 / 按 agent ACL；验证隔离是认知隔离，不是安全边界。",
       font=F(15, False), fill=MUTED)

# ---------------- footer ----------------
legend_y = 2620
legend_x = 70
for color, label in [(HUMAN, "人类"), (ORCH, "集群"), (WORKER, "worker"),
                     (VERIFY, "验证"), (STATE, "工作区"), (STOP, "治理"), (RUNTIME, "运行时")]:
    legend_item(legend_x, legend_y, color, label)
    legend_x += 150

iy = 2660
interfaces = [
    ("I1", "方向 / 阶段授权"),
    ("I2", "决策包 / 验收请求"),
    ("I3", "工单 / 结果 / 证据"),
    ("I4", "状态 / 证据读回"),
    ("I5", "人类直读"),
]
ix = 70
for code, label in interfaces:
    d.text((ix, iy), code, font=F(16, True), fill=MUTED)
    d.text((ix + 34, iy), label, font=F(15, False), fill=SECOND)
    ix += 300

d.line([(70, 2700), (2490, 2700)], fill=BORDER, width=1)
d.text((70, 2720),
       "AECW · 概念结构图 · 2026-11-06 · 概念图，不代表已实现常驻集群；当前治理原语已具备 freeze/start/verify/lock/probe。",
       font=F(15, False), fill=MUTED)

out = os.path.join(os.path.dirname(__file__), "cluster-concept-structure.png")
img.save(out, "PNG", optimize=True)
print(out, img.size)
