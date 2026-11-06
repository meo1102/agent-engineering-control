# -*- coding: utf-8 -*-
"""Draw the AECW agent-cluster conceptual runtime flow as a PNG."""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 4200
BG = "#F8FAFC"
TEXT = "#0F172A"
SECOND = "#334155"
MUTED = "#64748B"
BORDER = "#E2E8F0"
ARROW = "#475569"

HUMAN = "#B45309"
HUMAN_BG = "#FFFBEB"
ORCH = "#1D4ED8"
ORCH_BG = "#EFF6FF"
WORKER = "#0F766E"
WORKER_BG = "#F0FDFA"
VERIFY = "#15803D"
VERIFY_BG = "#F0FDF4"
STATE = "#6D28D9"
STATE_BG = "#F5F3FF"
STOP = "#B91C1C"
STOP_BG = "#FEF2F2"
AMBER = "#B45309"

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


def text_block(x, y, w, lines, font, fill, lh, align="left"):
    for line in lines:
        if align == "center":
            lx = x + (w - tw(line, font)) / 2
        else:
            lx = x
        d.text((lx, y), line, font=font, fill=fill)
        y += lh
    return y


def shadow_round(x, y, w, h, r=20, off=6):
    d.rounded_rectangle([x + off, y + off + 2, x + w + off, y + h + off + 2],
                        radius=r, fill="#E2E8F0")


def box(x, y, w, h, title, body, accent, bg, title_size=27, body_size=19):
    shadow_round(x, y, w, h)
    d.rounded_rectangle([x, y, x + w, y + h], radius=20, fill=bg, outline=accent, width=2)
    # left accent bar
    d.rectangle([x, y + 22, x + 8, y + h - 22], fill=accent)
    tf = F(title_size, True)
    d.text((x + 30, y + 20), title, font=tf, fill=TEXT)
    bf = F(body_size, False)
    lines = []
    for para in body:
        lines.extend(wrap(para, bf, w - 62))
    yy = y + 64
    for line in lines:
        d.text((x + 30, yy), line, font=bf, fill=SECOND)
        yy += 27


def diamond(cx, top, w, h, text, accent, bg):
    half = w // 2
    pts = [(cx, top), (cx + half, top + h // 2), (cx, top + h), (cx - half, top + h // 2)]
    spts = [(px + 6, py + 8) for px, py in pts]
    d.polygon(spts, fill="#E2E8F0")
    d.polygon(pts, fill=bg, outline=accent, width=2)
    f = F(21, False)
    lines = []
    for para in text.split("\n"):
        lines.extend(wrap(para, f, w - 110))
    lh = 28
    total = len(lines) * lh
    yy = top + h // 2 - total // 2 + 2
    for line in lines:
        d.text((cx - tw(line, f) / 2, yy), line, font=f, fill=TEXT)
        yy += lh


def callout(x, y, w, h, title, body, accent, bg):
    shadow_round(x, y, w, h, r=16, off=4)
    d.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=bg, outline=accent, width=2)
    d.rectangle([x, y + 18, x + 6, y + h - 18], fill=accent)
    tf = F(22, True)
    d.text((x + 24, y + 16), title, font=tf, fill=TEXT)
    bf = F(18, False)
    lines = []
    for para in body:
        lines.extend(wrap(para, bf, w - 48))
    yy = y + 56
    for line in lines:
        d.text((x + 24, yy), line, font=bf, fill=SECOND)
        yy += 28


def dashed_segment(p1, p2, color, width=2, dash=12, gap=8):
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


def arrowhead(p1, p2, color, size=15):
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


def tag(text, x, y, color, bg="#FFFFFF", border=None, size=16, bold=True):
    f = F(size, bold)
    pad = 8
    w = tw(text, f) + pad * 2
    h = size + 9
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=bg, outline=border or bg, width=1)
    d.text((x + pad, y + 3), text, font=f, fill=color)
    return w


def phase(y, num, title, sub, accent):
    d.text((70, y), num, font=F(34, True), fill=accent)
    d.text((126, y + 2), title, font=F(24, True), fill=TEXT)
    d.text((390, y + 6), sub, font=F(19, False), fill=MUTED)
    d.line([(70, y + 42), (1450, y + 42)], fill=BORDER, width=1)


# ---------------- header ----------------
d.rectangle([0, 0, W, 8], fill="#0F172A")
d.text((80, 44), "AECW · Agent 集群概念运行全流程", font=F(54, True), fill=TEXT)
d.text((80, 116), "工单制多上下文：人类定方向，编排者单写，worker 生产候选，验证者独立复核",
       font=F(25, False), fill=SECOND)
d.text((80, 156),
       "概念图，不是当前代码的调用图；当前治理原语已有 freeze / start / verify / lock / probe，集群编排仍由主 agent 驱动 workflow。",
       font=F(19, False), fill=MUTED)
d.line([(70, 192), (2320, 192)], fill=BORDER, width=1)

# ---------------- phases ----------------
phase(210, "01", "方向与授权", "人类定方向；只授权一个阶段", HUMAN)
phase(1130, "02", "拆单与执行", "编排者拆单；worker 隔离生产", ORCH)
phase(1925, "03", "独立验证", "另一个上下文只读产物", VERIFY)
phase(2365, "04", "集成与门禁", "单写者合并；verify + 人类验收", ORCH)
phase(3180, "05", "写回与记忆", "状态写回；复盘只产候选", STATE)

# ---------------- main boxes ----------------
box(330, 275, 1120, 120, "人类 · 定方向",
    ["目的 / 非目标 / 失败定义",
     "S1–S4 边界 / 预算 / 停止条件"], HUMAN, HUMAN_BG)

box(330, 435, 1120, 120, "阶段授权",
    ["宪章确认 + 施工蓝图批准（人类）",
     "只授权一个阶段，不授权整个项目"], HUMAN, HUMAN_BG)

diamond(890, 585, 560, 160, "蓝图已批准\n基线可冻结？", HUMAN, HUMAN_BG)

box(330, 785, 1120, 120, "freeze + start",
    ["写入方向 / 蓝图 / 判据 / 产品树的哈希",
     "签发开工令：owner 具名 + 首报"], ORCH, ORCH_BG)

diamond(890, 935, 620, 160,
        "开工校验通过？\nstage=frozen\npayload / owner / 无 S1·S2", ORCH, ORCH_BG)

box(330, 1195, 1120, 130, "RUN · 编排者生成 manifest + 工单",
    ["从冻结蓝图拆工作包；写集不重叠",
     "每单：输入哈希 / 验收命令 / 输出契约 / 预算"], ORCH, ORCH_BG)

box(330, 1365, 1120, 180, "实现 worker × N · 隔离 worktree",
    ["C1：1 个实现者｜C2：N 个并行，写集不重叠",
     "只读工单与权威输入；只交 patch + result",
     "不改 mainline / state / STATUS / ledger"], WORKER, WORKER_BG)

box(330, 1585, 1120, 115, "结果契约",
    ["status · changed_files+hash · commands+exit",
     "unknowns · dissent · session_id"], WORKER, WORKER_BG)

diamond(890, 1740, 540, 150, "结果完整、\n证据可复现？", WORKER, WORKER_BG)

box(330, 1990, 1120, 145, "独立验证者 · 新鲜上下文",
    ["只读工单 / diff / 日志 / 哈希 / 判据",
     "不读实现者推理与自评；不改代码",
     "重跑验收；检查测试是否被削弱"], VERIFY, VERIFY_BG)

diamond(890, 2175, 440, 155, "验证通过？", VERIFY, VERIFY_BG)

box(330, 2430, 1120, 150, "编排者 · 集成 + verify",
    ["串行 apply patch；冲突 → 新工单",
     "全量测试 + check --strict + probe + criteria",
     "开放 S1/S2 + 证据债 + tree attestation"], ORCH, ORCH_BG)

diamond(890, 2620, 420, 155, "verify PASS？", ORCH, ORCH_BG)

box(330, 2815, 1120, 135, "人类验收门 · 决策包",
    ["变更 / 证据 / 未决异议 / 残余风险 / 建议",
     "接受 / 拒绝 / 有条件接受"], HUMAN, HUMAN_BG)

diamond(890, 2990, 420, 155, "人类接受？", HUMAN, HUMAN_BG)

box(330, 3245, 1120, 100, "合并 mainline + tag",
    ["release 时打 tag；记录 merge commit"], VERIFY, VERIFY_BG)

box(330, 3385, 1120, 130, "状态写回 · 单写者",
    ["state.json / STATUS / ledger / board / evidence",
     "动作完成 = 状态写回；check FAIL 不得结束"], STATE, STATE_BG)

box(330, 3555, 1120, 115, "复盘 → 记忆候选",
    ["经验 / 负记忆 / 技能候选；不直接激活",
     "需人类或策展过门；协议变更走 CR"], STATE, STATE_BG)

diamond(890, 3710, 420, 150, "阶段完成？", STATE, STATE_BG)

box(330, 3900, 1120, 130, "阶段关闭 · closed（终态）",
    ["下一阶段：新蓝图 + 新 freeze + 新 start",
     "同一阶段不得续跑"], MUTED, "#F1F5F9")

# ---------------- callouts ----------------
callout(1540, 270, 760, 200, "怎么读这张图",
        ["概念运行图，不是代码调用图。",
         "DSH 用 workflow 扇出短生命周期 worker；",
         "没有持久队列 / 点对点消息 / 按 agent ACL。"], MUTED, "#F8FAFC")

callout(1540, 520, 760, 520, "停止 / 不得开工",
        ["• 蓝图未批准 → 退回修订；不得 freeze/start",
         "• 无 freeze / start → 不执行",
         "• start 哈希 / owner / 开放 S1·S2 失败 → 停",
         "• closed 阶段 → 不得重启；新 stage + 新 freeze",
         "• worker 写 state / ledger → 拒绝 patch，记事件",
         "• verifier 读实现者推理 → 验证无效"], STOP, STOP_BG)
# stop-panel lower blocks: give D2's "no" branch a concrete target
d.line([(1568, 760), (2272, 760)], fill="#FECACA", width=1)
d.text((1568, 780), "开工校验失败 = 停", font=F(18, True), fill=STOP)
d.text((1568, 808), "hash 不符 / owner 不符 / 开放 S1·S2", font=F(17, False), fill=SECOND)
d.text((1568, 834), "→ 不进入 run；先写 dissent / 回人类", font=F(17, False), fill=SECOND)
d.line([(1568, 874), (2272, 874)], fill="#FECACA", width=1)
d.text((1568, 894), "触发后的动作", font=F(18, True), fill=STOP)
d.text((1568, 922), "停 run → 写 dissent → 通知人类", font=F(17, False), fill=SECOND)
d.text((1568, 948), "禁止：带病继续 / 自批 / 静默重试", font=F(17, False), fill=SECOND)
d.text((1568, 984), "以上任一条成立，不进入下一阶段。", font=F(17, False), fill=STOP)

callout(1540, 1300, 760, 230, "单写者",
        ["worker 只写自己的 worktree + result。",
         "mainline / state / STATUS / ledger 只由编排者写。",
         "D3 不完整 → 补证/重试 1 次；冲突 → 新工单。"], ORCH, ORCH_BG)

callout(1540, 1900, 760, 190, "独立验证",
        ["只读工单 / diff / 日志 / 哈希；不读推理。",
         "不改代码；重跑验收，检查测试是否被削弱。",
         "D4 不通过 → 退回修复 ≤1 次；再失败 → 人类。"], VERIFY, VERIFY_BG)

callout(1540, 2410, 760, 190, "verify 是唯一通过类证据",
        ["check --strict + probe + 全量测试 + criteria",
         "开放 S1/S2 + 按 impact 证据债 + tree attestation",
         "gate 只消费 attestation，不接受自由文本放行"], WORKER, WORKER_BG)

callout(1540, 2800, 760, 180, "人类只过门",
        ["决策包：变更 / 证据 / 未决异议 / 残余风险。",
         "agent 不得代写验收或自批 charter。",
         "人类可以拒绝、有条件接受、或缩小范围。"], HUMAN, HUMAN_BG)

callout(1540, 3270, 760, 190, "动作完成 = 状态写回",
        ["state.json 是唯一状态源；STATUS 是视图。",
         "state/STATUS/ledger/board/evidence 全部写回。",
         "check FAIL 不得结束；不写回视为未完成。"], STATE, STATE_BG)

callout(1540, 3520, 760, 180, "记忆不直接激活",
        ["复盘只产出候选；负记忆与拒绝 patch 保留。",
         "需人类/策展过门；协议变更走 CR。",
         "防止集群只学自己的输出。"], STATE, "#FAF5FF")

callout(1540, 3730, 760, 300, "边界 / 落地阶梯",
        ["• C1 先做：实现者 + 独立验证者",
         "• C2 才并行：写集不重叠；C3 再做记忆/红队",
         "• 同模型多席 ≠ 异构验证",
         "• 32 路并发是进程测试，不是 32 个 agent",
         "• 范围/判据变更 → change 门 + 新 freeze/start"], MUTED, "#F8FAFC")

# ---------------- main arrows ----------------
arrow([(890, 395), (890, 435)])
arrow([(890, 555), (890, 585)])
arrow([(890, 745), (890, 785)])
arrow([(890, 905), (890, 935)])
arrow([(890, 1095), (890, 1195)])
arrow([(890, 1325), (890, 1365)])
arrow([(890, 1545), (890, 1585)])
arrow([(890, 1700), (890, 1740)])
arrow([(890, 1890), (890, 1990)])
arrow([(890, 2135), (890, 2175)])
arrow([(890, 2330), (890, 2430)])
arrow([(890, 2580), (890, 2620)])
arrow([(890, 2775), (890, 2815)])
arrow([(890, 2950), (890, 2990)])
arrow([(890, 3145), (890, 3245)])
arrow([(890, 3345), (890, 3385)])
arrow([(890, 3515), (890, 3555)])
arrow([(890, 3670), (890, 3710)])
arrow([(890, 3860), (890, 3900)])

# stop branches
arrow([(1170, 665), (1540, 665)], STOP, 3)
tag("否", 1230, 635, STOP, "#FFFFFF", "#FECACA", 16)
arrow([(1200, 1015), (1490, 1015), (1490, 984), (1540, 984)], STOP, 3)
tag("否", 1260, 985, STOP, "#FFFFFF", "#FECACA", 16)

# verification fail loop -> implementer
arrow([(620, 1815), (300, 1815), (300, 1455), (330, 1455)], AMBER, 2, dashed=True)
arrow([(670, 2255), (270, 2255), (270, 1500), (330, 1500)], AMBER, 2, dashed=True)
tag("补证 / 重试 1 次", 340, 1784, AMBER, "#FFFFFF", "#FDE68A", 14, False)
tag("退回修复 ≤1 次", 340, 2224, AMBER, "#FFFFFF", "#FDE68A", 14, False)

# verify fail loop -> integration
arrow([(1100, 2695), (1495, 2695), (1495, 2505), (1450, 2505)], AMBER, 2, dashed=True)
tag("否 → 补证/回退", 1150, 2658, AMBER, "#FFFFFF", "#FDE68A", 16)

# human reject annotation
arrow([(1100, 3065), (1112, 3065)], STOP, 3)
d.text((1124, 3016), "拒绝 / 有条件", font=F(19, True), fill=STOP)
d.text((1124, 3044), "记录 → 回规划或关闭", font=F(19, True), fill=STOP)

# next run loop -> orchestrator
arrow([(1100, 3785), (1515, 3785), (1515, 1260), (1450, 1260)], "#94A3B8", 2, dashed=True)
tag("否 → 下一 run", 1118, 3748, "#475569", "#FFFFFF", "#CBD5E1", 16)
tag("下一 run", 1462, 1228, "#475569", "#FFFFFF", "#CBD5E1", 14, False)

# artifact labels
tag("patch + result", 905, 1550, MUTED, "#FFFFFF", "#E2E8F0", 15, False)
tag("VA-*.json", 905, 2590, MUTED, "#FFFFFF", "#E2E8F0", 15, False)
tag("merge commit", 905, 3352, MUTED, "#FFFFFF", "#E2E8F0", 15, False)

# connector dots to callouts
for y in (1455, 2060, 2505, 2880, 3450, 3610):
    d.line([(1450, y), (1540, y)], fill="#CBD5E1", width=2)
    d.ellipse([1444, y - 4, 1452, y + 4], fill="#94A3B8")
    d.ellipse([1536, y - 4, 1544, y + 4], fill="#94A3B8")

# ---------------- legend ----------------
lx, ly = 70, 4062
items = [("人类", HUMAN), ("编排者", ORCH), ("worker", WORKER),
         ("验证者", VERIFY), ("工作区/状态", STATE), ("停止/拒绝", STOP)]
for label, color in items:
    d.rounded_rectangle([lx, ly, lx + 18, ly + 18], radius=4, fill=color)
    d.text((lx + 26, ly - 2), label, font=F(17, False), fill=SECOND)
    lx += 175

ly2 = 4098
d.line([(70, ly2 + 10), (120, ly2 + 10)], fill=ARROW, width=3)
arrowhead((90, ly2 + 10), (120, ly2 + 10), ARROW, 12)
d.text((130, ly2), "正常流", font=F(17, False), fill=SECOND)
dashed_segment((250, ly2 + 10), (310, ly2 + 10), AMBER, 2, 10, 7)
arrowhead((280, ly2 + 10), (310, ly2 + 10), AMBER, 11)
d.text((320, ly2), "退回 / 重试", font=F(17, False), fill=SECOND)
d.line([(460, ly2 + 10), (510, ly2 + 10)], fill=STOP, width=3)
arrowhead((480, ly2 + 10), (510, ly2 + 10), STOP, 12)
d.text((520, ly2), "停止 / 拒绝", font=F(17, False), fill=SECOND)

d.text((80, 4155),
       "AECW · 概念运行全流程 · 2026-11-06 · 概念图，不代表已实现常驻集群",
       font=F(17, False), fill=MUTED)

out = os.path.join(os.path.dirname(__file__), "cluster-concept-flow.png")
img.save(out, "PNG", optimize=True)
print(out, img.size)
