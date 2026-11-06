# PLAN v0.9：真实项目校准——从单页状态到可校准状态

> 依据：[`REVIEW-task-complete-toast-aecw-2026-11-05.md`](REVIEW-task-complete-toast-aecw-2026-11-05.md)。
> 对象：第一次真实部署 `task-complete-toast-aecw`（产品根 + 治理 `aecw/`；2026-11-06 布局 v3 后产品根 = 仓库根）。
> 定位：**不推翻 v0.5–v0.8 的三域/信任优先/蓝图/开工令**；补的是“部署层”缺少的状态模型、项目清单、泳道与验收矩阵。
> 结论：**三域不变，两个根；单一状态，多种视图；四条泳道，一个矩阵；check 查事实，probe 查现场。**

---

## 0. 为什么是 v0.9，而不是 v1.0

v0.8 已经证明“结构能跑”：三域、六接口、CLI、demo、check、freeze/start 都能工作。  
真实项目又证明“结构能跑”不等于“事实能对上”：

- `check` = FAIL 0｜WARN 0，`probe` = 7/7 PASS；
- 但 `STATUS`、产品 README、任务板、决策记录、学习账、进化提案仍在说旧状态；
- 蓝图要求截图，阶段零截图仍“有条件通过”；
- G4 已验收但未发布，EV-001 已激活但有的文档还写 trial；
- adoption 门禁未签，但结构已经在用；
- 阶段已关闭，但迁移/分层/进化仍在继续，没有正式泳道。

所以 v0.9 不改“人类定方向、集群实现、工作区记忆/落地”的根，只改**部署后的状态如何被记录、核对、展示**。

---

## 1. 五条诊断

| # | 诊断 | 现实表现 | 后果 |
|---|---|---|---|
| 1 | 状态是散文，不是记录 | `STATUS` 同一页 §2.1 与 §2.2 互斥；README/board/decisions/learning 各写一份“当前” | 人一忙就漂移，`check` 看不出来 |
| 2 | 验收是自由文本，不是矩阵 | WP-5 要求截图，门禁零截图仍“有条件通过”；没有逐项 waiver | “有条件通过”成为万能出口 |
| 3 | 没有项目清单 | 布局 v2 后命令/目录树/安装说明多种写法；CLI 副本无版本 | 路径/命令漂移，工具与数据耦合 |
| 4 | 没有泳道 | 阶段 closed 后继续迁移/分层/进化，记作“阶段外” | 授权、预算、停止、证据不清楚 |
| 5 | 没有入口/通道模型 | slot 注册成功但人找不到设置页；抑制浮层把系统通知一起吞了 | “实现完成”不等于“人类可用” |

---

## 2. 概念模型：四个新增，三个不变

### 2.1 三个不变

1. **三域责任不变**：人类方向/验收；集群实现/学习；工作区证据/记忆/落地。
2. **人类注意力不变**：不新增四个常设角色；人类只做方向、S1/S2、最终验收/抽样、阶段边界。
3. **阶段边界不变**：蓝图批准 + freeze + start 才执行；阶段结束停；变更不原地改基线。

### 2.2 四个新增

#### A. 单一状态，多种视图

- **一个事实只在一个地方有值**：阶段、发布、进化、采纳、证据债写进 `state.json`。
- `STATUS.md` 是视图；`gates/`、`acceptance/`、`evolution/` 是记录；README/board 只引用。
- 现在先不做完整渲染器，但必须做到：`STATUS` 顶部有机器可读状态摘要，`check` 能对账；正文不再手写与摘要重复的字段。

#### B. 验收矩阵

每条判据一行：

| 字段 | 含义 |
|---|---|
| `id` | G4-1、WP-5-截图…… |
| `criterion` | 可观察判据 |
| `status` | `met / waived / deferred / failed / not-started` |
| `evidence` | F/DR/CR、文件、命令、E1/E2 |
| `verifier` | 谁核验（人/独立 agent/工具） |
| `human_decision` | 接受/豁免/推迟 + 日期 |
| `impact` | 阻塞哪个门/发布 |

门禁是矩阵的视图，不是自由散文。`有条件通过` 必须绑定具体行。

#### C. 四条泳道

| 泳道 | 做什么 | 授权 | 产物 | 停止 |
|---|---|---|---|---|
| **stage** | 产品行为变更 | 人类 freeze/start | 蓝图、阶段门禁、基线 | 阶段末/停止条件 |
| **maintenance** | 文档纠错、路径/命令修复、迁移、非行为重构 | 人类一次性指令或维护授权 | 维护记录、check 通过 | 超范围即停 |
| **evolution** | 工具/流程/技能候选 | 人类 trial/active 裁决 | 六项提案、正负控、EV 台账 | false pass/成本过高 |
| **release** | 版本、tag、manifest、发布说明 | 人类发布门 | release manifest、证据债结清 | 证据债未清即停 |

**阶段关闭只关闭 stage 泳道，不关闭项目。** 迁移/分层/复盘属于 maintenance；EV-001 属于 evolution；G4 发布属于 release。每条泳道都要有授权、范围、预算、停止、证据。

#### D. 入口与通道是验收对象

- **入口契约**：每个面向人类的功能必须写“从哪里点进去、看到什么、找不到时怎么办”。验收必须包含“人类在没有 agent 指路的情况下找到”。
- **通道矩阵**：应用内浮层 / 系统通知 / 无，按“同会话可见、同会话隐藏、其他会话、最小化、后台”逐格定义。
- **硬规则**：抑制浮层 ≠ 抑制系统通知；每个通道单独测。

---

## 3. 架构：两个根、一个清单、一个状态源、一个矩阵

### 3.1 两个根

```text
<repo>/
├─ package.json / index.js / client.js / lib/ / locale/ / test/  # 产品代码（产品根，可在仓库根或 product/）
├─ aecw/           # 治理（STATUS/ledger/human/cluster/workspace/gates/inbox）
├─ PROJECT.json    # 项目清单：roots.product 定义产品根
├─ README.md       # 仓库地图/产品说明（只指路）
└─ AGENTS.md       # 仓库级入口规则（只指路）
```

- **两个根 = 产品根 + 治理根，不强制产品根叫 `product/`。** `PROJECT.json.roots.product` 可以是 `.`（产品在仓库根），也可以是 `product/`；`roots.governance` 指向 `aecw/`。
- `workspace/` 不再放产品代码；只放证据/记忆/落地。
- 根 README/AGENTS 不是“第二份状态”，只负责把人和 agent 指到 `aecw/STATUS.md` 与 `aecw/AGENTS.md`。
- 产品版本与治理状态分离：`roots.product/package.json` 是产品版本；`aecw/state.json` 是治理状态。布局变化必须写回 `state.layout`。

### 3.2 项目清单 `PROJECT.json`

```json
{
  "project": "task-complete-toast-aecw",
  "roots": {
    "product": ".",
    "governance": "aecw",
    "workspace": "aecw/workspace"
  },
  "install": { "target": ".", "profile": "desktop" },
  "commands": {
    "test": "node --test --test-isolation=none test/*.test.js",
    "probe": "node aecw/scripts/probe.mjs",
    "check": "node aecw/bin/aecw.mjs check aecw"
  },
  "tool": { "name": "aecw", "version": "0.9.2", "mode": "vendored" }
}
```

规则：

- 文档不手抄命令；引用 manifest 的 `commands`。
- `check` 从 manifest 读 `roots`/`commands`，验证路径存在、命令指向的文件存在。
- `tool.mode=vendored` 时校验 `tool.version` 与副本头部的版本/哈希；不一致给 WARN/FAIL。
- 安装目标变了，只改 manifest + 重跑 probe，不改十几份文档。

### 3.3 状态源 `state.json`

```json
{
  "layout": { "root": ".", "governance": "aecw" },
  "install": { "target": ".", "profile": "desktop" },
  "remote": { "name": "origin", "url": "https://github.com/<owner>/<repo>.git", "branch": "main" },
  "stage": { "name": "grow-2", "state": "closed", "gate": "gates/2026-11-05-grow-2.md" },
  "features": {
    "G4": { "state": "accepted", "release": "unreleased", "evidence": ["F-040"] }
  },
  "release": { "version": "1.2.0", "state": "released", "tag": "v1.2.0" },
  "evolution": { "EV-001": "active" },
  "adoption": { "state": "pending", "gate": "gates/2026-11-05-adoption.md" },
  "evidence_debt": [
    {
      "id": "ED-001",
      "item": "G4 设置页截图",
      "owner": "meo1102",
      "due": "2026-11-12",
      "impact": "release"
    }
  ],
  "baseline": { "commit": "4589b91", "tag": "aecw-layout-v2-2026-11-05" }
}
```

规则：

- `stage.state` 只能是 `seed/frozen/executing/paused/closed`；
- `features.*.state` 只能是 `draft/candidate/accepted/released`；
- `evolution.*` 只能是 `candidate/trial/active/retired`；
- `adoption.state` 只能是 `pending/provisional/accepted`；
- `release.state` 只能是 `unreleased/release-candidate/released/superseded`。

这些不是“多一套流程”，而是**把已经在用的词固定下来**，避免“已验收/可用/已发布/已激活”互相替代。

#### 3.3.1 动作完成 = 状态写回

真实项目最后几轮暴露了一个行为缺口：**发布/迁移/推送已经完成，但 `state`/`STATUS` 没有跟着写回**，回复里说“完成”，状态页仍是旧的。

规则：

- 任何改变**布局 / 安装路径 / 版本 / tag / 发布 / 远程仓库 / 配置**的动作，完成后必须先写 `state.json` + `STATUS.md` + 证据，再回复；
- `state.layout.root` / `state.install.target` 必须与 `PROJECT.json` 一致；不一致 `check` FAIL；
- `state.remote.url` 必须与 `git origin` 一致；不一致 `check` FAIL；
- 只做动作、不写回状态，视为**未完成**；不得用“我已经做了”替代状态记录。

这不是增加审批，而是**把动作的结果落到唯一状态源**；人类只需要看 `STATUS`/`state`，不需要从聊天记录里猜。

### 3.4 验收矩阵 `criteria.md`

```markdown
| ID | 判据 | 状态 | 证据 | 核验人 | 人类裁决 |
|---|---|---|---|---|---|
| G4-1 | 设置页可打开、控件可操作 | met | F-040（E2） | 人类 | 接受 2026-11-05 |
| G4-2 | 字号 12/18、宽度 280/480、联动 | met | F-037 + F-040 | 人类 | 接受 2026-11-05 |
| G4-3 | 至少一张设置页截图 | deferred | 无 | — | 待签（ED-001） |
| G2-8 | 双会话并发 | waived | F-028 | 人类 | 接受为遗留 |
```

门禁规则：

- `met` 必须有证据；
- `waived/deferred` 必须有人类裁决 + 日期 + 影响门；
- 有 `failed/not-started` 时只能“暂停/退回”，不能“通过”；
- “有条件通过”必须写清绑定哪几行、条件何时到期、谁接受。

### 3.5 检查器：`check` 查事实，`probe` 查现场

| 层 | 查什么 | 失败后果 |
|---|---|---|
| `check` | 必需文件、owner、S1/S2、freeze/start、蓝图批准、state 与 STATUS 一致、criteria 状态合法、路径/命令存在、Markdown 围栏/链接、历史文档状态头 | FAIL 不开门 |
| `probe` | 安装、link/junction、bundles、patch、路由、slot/版本 | FAIL 不开门 |
| 人类 E2 | 入口、视觉、真实使用 | 没有 E2 不得称“人类可用” |

**重要**：`check` 不能只查“文件在不在”；要查“当前文档说的是不是同一件事”。  
`probe` PASS 不能替代人类 E2；`check` PASS 不能替代 probe。

### 3.6 文档状态

每个文档头部：

```text
> 状态：current | historical | superseded
> 最后核对：2026-11-05
> 替代/被替代：...
```

规则：

- `current` 文档之间不能互相矛盾；`check` 抽查关键字段；
- `historical/superseded` 不参与当前结论；旧路径/旧命令允许存在，但必须有状态头；
- `STATUS` 只列 `current` 文档；
- 迁移/门禁/复盘默认 `historical`，除非明确“当前仍有效”。

### 3.7 工具/数据分离

- **首选**：AECW CLI 作为外部工具（全局包/共享目录），项目只放数据；`check --project <dir>`。
- **允许**：vendored 到 `aecw/bin`，但必须 `tool.version` + 哈希 + `check` 漂移检查；升级时显式提交。
- **禁止**：无版本地复制 CLI/模板，然后各项目各自演化。
- 模板 `core/` 同样带版本；项目的 `core/` 与工具版本不一致时给 WARN。

---

## 4. 人类与集群怎么用

### 4.1 人类

- 只做：方向/边界、蓝图批准、freeze/start、S1/S2、发布/采纳、最终验收/抽样、泳道授权。
- 不需要：维护 `STATUS` 的每一行、逐条核事实、每道门签字、追每个文档的命令。
- 新增的一个动作：**发布门/采纳门签一次**（release/adoption），而不是每道门都签。

### 4.2 集群

- 先读 `PROJECT.json` → `aecw/STATUS.md` → `state.json` → `criteria.md`；
- 任何当前状态变化先改 `state.json`，再让 `STATUS` 视图更新；
- 阶段内只做蓝图/矩阵内工作；阶段外工作必须选泳道；
- 文档只引用 manifest/state，不手抄当前状态；
- `check`/`probe` 失败不得开门；`check`/`probe` 通过也不得替代人类 E2。

### 4.3 人类注意力合同（保持不变）

| 人类做 | 人类不做 |
|---|---|
| 定方向/目标/非目标/红线/预算/停止 | 常规异议分诊 |
| 批准蓝图、freeze/start | 替集群写蓝图/做任务分解 |
| S1/S2、不可逆、重大外部性、价值冲突 | 逐条核事实 |
| 发布/采纳、最终验收/遗留接受 | 每道门签字 |
| 每周抽样 1–3 条 S3/S4 | 维护台账/角色行政、逐条批 task 变更 |

---

## 5. 最小迁移顺序

> 原则：先真话，后结构；先清单，后状态；先矩阵，后渲染。不要一次做大。

1. **真话修复（maintenance 泳道）**
   - 修 `STATUS`、根 `README`、`board`、`decisions`、`learning`、`ev-001`、`retrospective` 的当前矛盾；
   - 历史文档加 `HISTORICAL/SUPERSEDED` 头；
   - 不改产品行为、不改人类验收/决策。
2. **加 `PROJECT.json`**
   - 两个根、安装目标、三条命令、工具版本；
   - 文档命令改为引用；`check` 校验路径/命令存在。
3. **加 `criteria.md`**
   - 把 G1–G4、WP-0–6 的判据/证据/豁免逐项落表；
   - `grow-2` 的“有条件通过”补成具体行。
4. **加 `state.json` + `STATUS` 摘要**
   - 先只做 `stage/release/evolution/adoption/evidence_debt` 五个字段；
   - `check` 对账，暂不做完整渲染。
5. **升级 `check`**
   - Markdown 围栏/链接；
   - 当前文档关键词矛盾（如 `trial` vs `active`、`未安装` vs `profile → product`）；
   - 历史文档状态头。
6. **再开下一阶段**
   - 新蓝图必须引用 `criteria.md`；
   - 发布门必须先结清证据债或人类签署不补；
   - adoption 未签前，结构只能标 `provisional`，不能称“已采纳”。

---

## 6. 不做什么

- 不新增四个常设角色；问题不是“没人负责”，是“状态没有模型”。
- 不要求所有文档自动生成；只生成“当前状态/门禁/验收”三类高频视图。
- 不把 `state.json` 做成数据库/仪表盘；一个文件、五个字段、`check` 能读即可。
- 不因为这次矛盾否定“单一 STATUS”；它仍然必要，只是要从“手写摘要”升级为“状态视图”。
- 不把 `有条件通过` 当常规出口；条件必须可核对、可到期、有人签。
- 不把 E2 升级成 E1；零截图仍是缺口。
- 不把 maintenance/evolution 当成“偷偷开新阶段”；它们有独立授权，但不改产品行为/验收。

---

## 7. v0.9 的验收标准

v0.9 不是“文档更多”，而是能通过这五个测试：

1. **真话测试**：故意把 `STATUS` 的某句旧话留着，`check` 能报出来；把 `state.json` 的 `EV-001` 改成 `trial`，`check` 能报与 `evolution.md` 不一致。
2. **清单测试**：把项目从 `D:\A` 移到 `D:\B`，只改 `PROJECT.json` + 重跑 probe；文档不需要批量改命令。
3. **矩阵测试**：某判据没证据，门禁不能“通过”；只能 `deferred` + 人类签署 + 证据债 ID。
4. **泳道测试**：阶段 closed 后做迁移/文档修复，必须出现在 maintenance 记录里；做 EV-002，必须走 evolution 门；发版，必须走 release 门。
5. **写回测试**：改布局/安装/remote 后先不写 `state`，`check` 必须 FAIL；写回 `state.layout`/`state.install`/`state.remote` 后 PASS。

五个测试都过，才叫“可校准状态”；否则只是“文档写得更整齐”。

---

## 8. 结论

> **v0.9 不增加控制点，而是把已经存在的控制点接上状态。**  
> 人类仍然只做方向/边界/验收/阶段门；集群仍然在边界内实现；工作区仍然承载证据/记忆/落地。  
> 变的只是：当前状态从“多份手写摘要”变成一个可核对的状态源；验收从“自由文本”变成矩阵；阶段外工作从“黑盒”变成泳道；路径/命令/工具从“手抄”变成清单。

**一句话**：**三域不变，两个根；单一状态，多种视图；四条泳道，一个矩阵；check 查事实，probe 查现场。**

---

## 9. 红队整改（v0.9.1）

红队报告指出：当前实现仍是“诚实的单 agent 记录 + checklist”，不是强制治理边界。v0.9 解决了“状态/事实一致”，但没有解决“批准不可伪造、门禁 fail-closed、并发原子写、探针/写路由安全”。整改方案见 [`PLAN-v0.9.1-红队整改.md`](PLAN-v0.9.1-红队整改.md)：先定 L/E 威胁模型，再做 P0 `verify`、状态机/freeze hash、原子台账、批准绑定、探针/写路由；在 `verify-release` 通过前不宣称治理可靠。
