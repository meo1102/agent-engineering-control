# AECW 生态原型 v0.1：人类 / 集群 / 工作区

> **这是什么**：一个零依赖、文件系统级的生态原型，把 AECW v0.5–v0.9 的概念落成可运行的结构：三个域、六个接口、六个关键工件、一个 CLI。
> **v0.9 校准**：真实项目 `task-complete-toast-aecw` 证明“结构全绿 ≠ 事实一致”；部署到真实仓库前，先读 [v0.9 校准](../PLAN-v0.9-真实项目校准.md) 与 [真实项目证据](../REVIEW-task-complete-toast-aecw-2026-11-05.md)。
> **不是什么**：不是生产系统，不是 agent 运行时，不接模型 API，不做 UI；它先解决“结构、接口、状态、证据、异议”能不能跑通。
> **原则**：人类只做方向/S1/S2/最终验收/抽样；集群在边界内默认相信；工作区是唯一当前状态；异议必须到达有权者；事实必须有来源和状态。

---

## 1. 5 分钟跑通

在 `agent-engineering-control/prototype` 目录执行：

```powershell
node bin/aecw.mjs demo
node bin/aecw.mjs check examples/demo-project
```

然后按顺序读：

1. `examples/demo-project/STATUS.md` —— 唯一当前状态
2. `examples/demo-project/human/direction.md` —— 方向/边界/停止
3. `examples/demo-project/BLUEPRINT.md` —— 施工蓝图（本阶段）
4. `examples/demo-project/gates/2026-11-05-charter-freeze.md` —— 阶段基线冻结
5. `examples/demo-project/gates/2026-11-05-start-order.md` —— 人类开工令
6. `examples/demo-project/ledger.md` —— 异议/事实/变更
7. `examples/demo-project/gates/` —— 先看 `g2-blocked`，再看 `g2-resolved`
8. `examples/demo-project/workspace/landing/manifest.md` —— 落地清单

Demo 演示的是：

```text
宪章 + 蓝图（人类批准）
  → freeze：阶段基线冻结
  → start：人类下达开工令
  → 事实：G2 常驻提醒遮挡授权按钮（E2 人类目视）
  → S2 异议（直达人类）
  → 门禁 G2-blocked：开放 S1/S2 = 1，暂停
  → 人类裁决：进入会话即收起
  → DR-001 关闭
  → 门禁 G2-resolved：开放 S1/S2 = 0，有条件通过
  → 人类接受遗留（G2-8/G3-4b）
  → 发布 + 落地清单
```

---

## 2. 三域结构

```text
<project>/
├─ STATUS.md                 # 唯一当前状态（人先看这一页）
├─ BLUEPRINT.md              # 施工蓝图（本阶段；人类批准）
├─ human/                    # 人类域
│  ├─ direction.md           # 方向/非目标/失败定义/S1-S4/预算/停止
│  ├─ decisions.md           # 人类决策记录
│  └─ acceptance.md          # 真实使用/落地/遗留接受
├─ cluster/                  # 集群域
│  ├─ roster.md              # 角色/谁在做（默认单 agent + 人类）
│  ├─ board.md               # 任务板
│  ├─ runs.md                # 运行记录
│  └─ learning.md            # 观察/教训/候选（不自动晋升）
├─ workspace/                # 工作区域
│  ├─ work/                  # 产物/草稿/候选
│  ├─ evidence/              # 原始证据（E1）
│  ├─ memory/                # 项目记忆/负记忆
│  └─ landing/               # 落地清单/交接/退役
├─ gates/                    # 每道门一页
├─ inbox/                    # S1/S2 异议 + CR 变更详情
└─ ledger.md                 # 异议/事实/变更台账
```

### 三个域不可互相替代

| 域 | 回答 | 不可转移 |
|---|---|---|
| **人类** | 为什么做、什么不能牺牲、什么算失败、是否接受 | 方向、S1/S2、最终验收、遗留接受、元规则 |
| **集群** | 怎么做、怎么学、怎么验证 | 实现、举证、候选、暴露不确定性、提议进化 |
| **工作区** | 现在真实存在什么、证据在哪、如何交接 | 承载产物/证据/记忆/落地；不自证为真 |

---

## 3. 六个协调接口

| # | 接口 | 方向 | 最小内容 | 硬规则 |
|---|---|---|---|---|
| **I1** | 方向与边界 | 人类 → 集群 | 目的、非目标、失败定义、S1–S4、预算、停止、升级触发 | 没有边界就没有“默认相信” |
| **I2** | 决策包 | 集群 → 人类 | 要决定什么、选项/代价、证据、异议、建议、期限 | 必须含“不做/更差但更便宜/集群不建议”的选项 |
| **I3** | 写入与证据 | 集群 ↔ 工作区 | 任务、产物、证据、事实、状态 | 候选不得当已验收事实；E1/E2/E3 分级 |
| **I4** | 原始现场 | 工作区 → 人类 | STATUS、ledger、evidence、open S1/S2 | 人类可绕过摘要直读；摘要要声明删了什么 |
| **I5** | 验收与落地 | 人类 → 工作区 | 接受/有条件/拒绝、剩余风险、照护者、退役 | 没有具名照护者不算落地 |
| **I6** | 交接与验证 | 集群 ↔ 集群 | 任务、产物、证据、未决、验证记录 | 验证者只读产物/证据，不读实现者推理 |

详细字段与失败模式见 [`docs/interfaces.md`](docs/interfaces.md)。

---

## 3.5 宪章交接：先冻结阶段基线，再授权集群

**宪章不是“交给某个 agent 去执行”的任务。** 它是人类与 agent 共同讨论出来的**共享基线**；输出不是 `direction.md` 一个文件，而是“宪章 + 已批准蓝图 + 异议状态 + 阶段基线 + 开工令”的一包东西。

### 交接五步

| 步 | 谁 | 产物 | 硬条件 |
|---|---|---|---|
| 1. 共写宪章 | 人类 + agent（起草/反例） | `human/direction.md` 草案、`human/decisions.md`（含被否决选项） | 人类所有者具名 |
| 2. 写施工蓝图 | 集群起草，人类修改 | `BLUEPRINT.md`（工作包/接口/未知/验收） | 一页为限；写清“本阶段不做什么” |
| 3. 异议清零 | 集群/人类 | `ledger.md`：开放 S1/S2 = 0；S3/S4 有主/有期限 | 宪章与蓝图的方向/价值/边界异议必须关闭 |
| 4. 冻结阶段基线 | 人类确认，集群管家记录 | `gates/<date>-charter-freeze.md` + `STATUS.md` 阶段授权 | 蓝图已批准；范围/预算/停止/验收写明；`freeze --charter-confirmed` |
| 5. 下达开工令 | 人类 | `gates/<date>-start-order.md` + `STATUS.md` 开工令 | 只授权**一个阶段**；写明首次报告点；阶段结束必须停 |

### 谁接、接什么

- **集群管家**是宪章/蓝图的**保管/路由者**，不是解释者，也不是“拿到文件就开做”的人。
- **实现 agent** 接到的是**阶段授权包**：宪章版本 + 已批准蓝图 + freeze 门禁 + start 开工令 + 任务板 + 开放/已关闭异议 + 验收判据；不是只有 `direction.md`。
- **新 agent 单独接手**时，必须同时拿到：宪章、蓝图、决策记录（含否决）、异议状态、阶段授权、开工令、当前 STATUS、证据；只给宪章等于让它重新解释一遍。
- **人类**保留：宪章批准、蓝图批准、S1/S2、阶段继续/收缩/停止、开工/暂停、最终验收。

### 集群不能做什么

- 不能把“宪章通过”或“蓝图批准”理解成“整个项目授权”；
- 不能在阶段结束后自动进入下一阶段；
- 不能在没有 `freeze` 的情况下开工；
- 不能在没有 `start` 的情况下开工；
- 不能带着开放 S1/S2 进入高风险执行；
- 不能自行扩大范围；新增范围要重新冻结/授权。

**一句话**：**宪章无异议 + 蓝图批准 + 阶段基线冻结 + 开工令，四者同时成立，集群才开工；阶段结束就停。**

---

## 3.6 施工蓝图与开工令：冻结不等于开工

**蓝图回答“怎么做”，开工令回答“现在开始”。** 两者都不是“整个项目授权”。

### 为什么需要蓝图

宪章只给“为什么/边界/什么算失败”，不给工作包、接口、顺序、阶段验收。没有蓝图，agent 会各自发明范围；有蓝图但没有边界，蓝图会变成“什么都想做”的完整设计文档，很快过期。

所以蓝图必须是**一页纸、按阶段、可版本化**的“施工合同”，不是完整设计文档。它由集群起草、人类批准；未批准不能 freeze。

最小内容：

1. 本阶段目标/非目标；
2. 工作包（输出 + 验收判据 + 依赖）；
3. 接口与契约（输入/输出/错误/兼容）；
4. 未知与假设（怎么验证、什么时候必须有答案）；
5. 本阶段不做；
6. 阶段验收（聚合判据、证据要求、允许的遗留）；
7. 变更记录（版本/理由/批准人）。

### 为什么开工令要独立

- **freeze 是“基线锁定”，不是“开始执行”。** 冻结后可以等预算、等窗口、等人类确认；冻结本身不产生工作。
- **start 是人类的显式 go。** 它把“计划已冻结”与“现在可以动手”分开，避免 freeze 被读成自动开工。
- 开工令只授权**一个阶段**，写清下达人、首次报告点、预算/停止引用、暂停权；阶段结束或触发停止条件必须停。

### 顺序

```text
起草宪章 → 清 S1/S2 → 起草蓝图 → 人类批准蓝图
  → freeze（锁宪章 + 蓝图 + 阶段范围/预算/停止/验收）
  → start（人类开工令）
  → 执行；阶段末停、报告、等下一道门
```

### 硬规则

- 蓝图未批准 → 不 freeze；
- 没有 freeze → 不 start；
- 没有 start → 不执行；
- start 只授权本阶段；阶段结束/停止条件触发必须停；
- 变更不得原地改冻结基线（见 3.7）。

CLI：

```powershell
node bin/aecw.mjs blueprint <dir> --stage grow-1   # 生成一页蓝图模板
# 人类填完并把 “- 状态：draft” 改为 “- 状态：approved”，填 “- 批准人：<人类>”
node bin/aecw.mjs freeze <dir> --charter-confirmed ...
node bin/aecw.mjs start <dir> --by <人类> --first-report "阶段末/触发 S2"
```

---

## 3.7 项目中途改目标：走变更请求，不是口头加活

项目进行中人类有新需要，是正常的；**不正常的是静默改基线**。变更分三级，处理成本不同：

| 级别 | 例子 | 谁决定 | 怎么处理 | 是否重新 freeze/start |
|---|---|---|---|---|
| **task** | 同一工作包内换实现、补测试、修文案 | 集群管家（阶段预算内） | 记 `board/runs`；不改变验收 | 否 |
| **blueprint** | 加/删工作包、改接口、改阶段验收、改顺序、加依赖 | **人类** | `change` + 影响分析 + 新蓝图版本 | **是**（新版本 + 重新 freeze/start） |
| **charter** | 改目的、非目标、失败定义、S1–S4、预算/停止 | **人类** | 先停；重谈宪章；新 freeze | **是**（可能按新项目处理） |

### 处理流程

1. **提出**：`change --type ... --title ... --reason ... --impact ...`；人类和 agent 都可以提。
2. **影响分析**：影响哪个阶段/工作包；已完成什么会作废/返工；预算/时间；验收判据是否改变；风险/外部性。
3. **裁决**：人类选接受/拒绝/挂起；不接受“默认通过”。
4. **执行**：
   - task：阶段内吸收；若吃掉阶段预算的 20% 以上或改验收，升级为 blueprint；
   - blueprint：升蓝图版本（旧版保留）→ 重新 freeze → 重新 start；
   - charter：先停 → 重谈 → 新 freeze；不要在原宪章上偷偷改。
5. **当前阶段怎么办**（人类选）：
   - **做完再切**（默认）：当前工作包接近完成且不被新需求作废；
   - **检查点停车**：保存证据、停、重新规划；
   - **中止**：新需求使当前方向失效，直接进 compost/重立项目。

### 硬规则

- **不得原地修改冻结基线**：v1 保留，v2 写 diff + 理由 + 批准人；
- 变更不得静默改验收判据；改了就要重新 freeze/start；
- 每个阶段设**变更预算**（例如最多 2 次 blueprint 级变更）；超了就停、重规划，不硬扛；
- 人类可以随时叫停，影响分析在停之后做，不是停的前置条件；
- 集群不能自行裁决 charter 级变更；技术发现走同一 CR 通道，不静默扩范围。

### 不做什么

- 不把每件小事都开成委员会：task 级变更留在阶段内；
- 不让“新需求”直接变成“加个功能”：先判断它改的是任务、蓝图还是宪章；
- 不用“变更”逃避阶段门：变更后仍要过验收/门禁。

CLI：

```powershell
node bin/aecw.mjs change <dir> --type blueprint --title "加导出" --reason "用户需要" --impact "新依赖；+3 天" --by <提出者>
node bin/aecw.mjs change <dir> --id CR-001 --decision 接受 --reason "接受；升 v2 后重新 freeze"
```

---

## 4. 角色：功能，不是人头

默认形态是 **单 agent + 人类**；角色是功能，不是必须新增的常设岗位。

| 角色 | 默认由谁 | 职责 | 不做什么 |
|---|---|---|---|
| 人类方向所有者 | 人类（具名） | 方向/边界、蓝图批准、S1/S2、开工/暂停、最终验收/抽样 | 不做常规分诊、不逐条核事实、不替集群写蓝图 |
| 集群管家 | 一个 agent | 起草蓝图、路由、任务板、变更分诊、S3/S4、升级、STATUS 维护 | 不独自裁决 S1/S2、不删异议、不替人类下开工令 |
| 实现者 | 一个 agent | 按冻结蓝图实现、测试、事实记录 | 不给自己发验收结论、不改蓝图/验收判据 |
| 验证者（可选/轮值） | 另一个上下文/红队 | 高影响事实复核、S1 调查 | 不读实现者推理、不与执行共目标 |
| 工作区策展 | agent/人 | STATUS、台账、证据、时效 | 不改写记录、不泄露匿名来源 |

单 agent 可以兼任实现/测试/记录，但**高影响验收必须有一次非作者检查**（人类真机/另一个 agent/独立工具）。蓝图由集群起草、人类批准；开工令只由人类下；两者都不覆盖整个项目。详见 [`docs/roles.md`](docs/roles.md)。

---

## 5. 五阶段生命周期

| 阶段 | 目标 | 关键动作 | 出门条件 |
|---|---|---|---|
| **seed** | 立边界 | 填 direction、写蓝图并批准、异议清零、`freeze`、`start`、第一道门 | 目标可判断、S1–S4 明确、所有者具名、蓝图已批准、charter-freeze/start-order 已签 |
| **grow** | 做与证 | 任务板、实现、证据、异议/事实、阶段门 | 集成可用、开放 S1/S2=0、目标轨迹正常 |
| **land** | 真实使用与落地 | 真实使用、验收、落地清单、照护者 | 遗留有人接受、可运维/可交接/可退役 |
| **steward** | 照护 | 观察、复审、再验证、退役 | 有照护者/预算/唤醒条件 |
| **compost** | 失败/终止 | 封存、归因、墓碑、教训候选 | 失败事实不可改写、资源释放 |

详见 [`docs/lifecycle.md`](docs/lifecycle.md)。

---

## 6. 状态与权威

- **`STATUS.md` 是唯一当前状态**；其他文档是证据/历史。
- 冲突时以 STATUS 为准；旧文档标 `SUPERSEDED`。
- 每次门禁/发布先更新 STATUS，再更新其他文档。
- 任何“通过”标 **E1/E2/E3**；E2（人类目视、无截图）不得写成 E1。
- 没有具名人类所有者，`check` 直接 FAIL，不发布。

---

## 7. CLI

```powershell
node bin/aecw.mjs init <dir> --name <名字> --owner <人类所有者> [--goal <目标>]
node bin/aecw.mjs blueprint <dir> [--stage <阶段>] [--force]
node bin/aecw.mjs freeze <dir> --charter-confirmed --stage <阶段> --scope <范围> --budget <预算> --stop <停止> --acceptance <验收>
node bin/aecw.mjs start <dir> [--by <人类>] [--first-report <报告点>]
node bin/aecw.mjs change <dir> --type task|blueprint|charter --title <变更> [--reason <理由>] [--impact <影响>] [--by <提出者>]
node bin/aecw.mjs change <dir> --id CR-001 --decision 接受|拒绝|挂起 [--reason <理由>]
node bin/aecw.mjs status <dir>
node bin/aecw.mjs dissent <dir> --severity S2 --type 风险 --claim "..." --evidence "..."
node bin/aecw.mjs fact <dir> --statement "..." --source "..." --status 已核验 --verifier "..."
node bin/aecw.mjs gate <dir> --name G2 --decision 有条件通过
node bin/aecw.mjs resolve <dir> --id DR-001 --decision "接受：..."
node bin/aecw.mjs accept <dir> --item "..." --decision 有条件接受 --risk "..." --by "人类所有者"
node bin/aecw.mjs log <dir> --decision "..." --reason "..."
node bin/aecw.mjs check <dir>
node bin/aecw.mjs demo
```

- `blueprint` 生成一页施工蓝图；人类批准（`- 状态：approved` + 具名批准人）后才能 freeze。
- `freeze` 是阶段基线门：要求 `--charter-confirmed`、人类所有者具名、蓝图已批准、无开放 S1/S2、direction 已填；写 `charter-freeze` 门禁 + STATUS 阶段授权。**没有 freeze 的阶段，check 直接 FAIL；没有 start 就进入执行，也 FAIL。**
- `start` 是开工令：要求已 freeze、蓝图已批准、无开放 S1/S2；写 `start-order` 门禁，把 STATUS 阶段状态改为 executing。**没有 start 就执行，check 直接 FAIL。**
- `change` 记录 task/blueprint/charter 三级变更；`--id` 用于裁决。开放 blueprint/charter 变更时 `check` 给 WARN，提醒不得扩大范围。
- `dissent` 对 S1/S2 自动写 `inbox/DR-xxx.md`，提示直达人类。
- `gate` 读 ledger，自动显示开放 S1/S2；有开放 S1/S2 时提示高风险动作暂停。
- `resolve` 关闭异议；`check` 检查必需文件、具名所有者、开放 S1/S2、开放变更、STATUS 新鲜度、蓝图/冻结/开工令是否一致。
- 零依赖，Node ≥18；不写数据库、不联网。

---

## 8. 这个原型实现了什么

**已实现（结构层）**：

- 三域目录与职责边界；
- 六个接口的工件/规则；
- 方向/边界/失败定义/S1–S4；
- 施工蓝图（一页、按阶段、人类批准、版本化）；
- `freeze` 阶段基线 + `start` 开工令 + 无 freeze/start 的 `check` FAIL；
- 变更请求台账（task/blueprint/charter 三级）+ 开放变更 WARN；
- 异议台账 + S1/S2 inbox + 反报复提示；
- 事实台账 + E1/E2/E3；
- 门禁一页纸 + 开放 S1/S2 阻断提示；
- 人类验收/遗留接受记录；
- STATUS 单一当前状态 + `check`；
- 五阶段生命周期文档；
- Demo 一条完整“蓝图→冻结→开工→事实→S2→门禁阻断→裁决→复验→接受→发布”的链。

**未实现（故意留给下一版）**：

- 真实 agent 运行时/模型路由/多 agent 编排；
- 自动运行测试、自动探针、自动截图；
- UI/通知/数据库/权限系统；
- 真正的多 agent 上下文隔离（原型只给规则与工件）；
- 自动变更影响分析/自动重排期（`change` 只记录 CR，影响分析仍由人/agent 填）；
- 自动进化/技能晋升（只留 learning ledger）。

---

## 9. 与概念/试点的对应

- v0.7 的“边界清晰 → 默认相信 → 例外升级 → 抽样验证” → `direction.md` + S1–S4 + 人类只处理 S1/S2。
- v0.7.1 的“上下文卫生” → `STATUS.md` + E1/E2/E3 + `SUPERSEDED` + `check`。
- 试点的 G2-1 遮挡 → demo 的 S2 异议 + `G2-blocked` / `G2-resolved` 两道门。
- 试点的“无具名所有者” → `check` 直接 FAIL。
- 试点的“测试替身/旧文档污染” → 验证者上下文隔离规则 + E1/E2 分级 + 事实来源。
- 试点的“11 个分叉” → 单一 STATUS + 文档时效表 + 冲突以 STATUS 为准。
- 试点的“拿到宪章就一股脑做下去” → 蓝图/ freeze / start 三段分离，阶段结束停。
- 试点的“中途改需求变成范围蔓延” → 三级变更请求 + 新蓝图版本 + 重新 freeze/start。

详见 [`docs/pilot-mapping.md`](docs/pilot-mapping.md)。

---

## 10. 怎么用到真实项目

1. `init` 一个真实项目目录（或空目录）；
2. 人类填 `human/direction.md`（方向/非目标/失败定义/S1–S4/预算/停止）；
3. 集群起草 `BLUEPRINT.md`，人类改完并批准（工作包/接口/未知/验收）；
4. `freeze` 阶段基线；`start` 下达开工令；
5. 第一个 agent 任务：把任务板第一行填上，产出第一个证据；
6. 每道门用 `gate` 生成一页；有 S1/S2 时先 `resolve` 再通过；
7. 中途有新需要：用 `change` 分 task/blueprint/charter 处理，不口头加活；
8. 真实使用后，用 `accept` 记录人类接受/遗留；
9. 每次阶段结束更新 `STATUS.md`，旧文档标 `SUPERSEDED`；
10. 每周人类抽样 1–2 条 S3/S4；`check` 保持 FAIL=0。

**一句话**：先用原型机跑一个真实小项目，再根据卡点改原型；不要先扩写成大系统。

---

## 11. 真实项目校准（v0.9）：结构全绿不等于事实一致

`task-complete-toast-aecw` 的 `check` 是 `FAIL 0｜WARN 0`，EV-001 探针是 `7/7 PASS`；但它的 `STATUS`、产品 README、任务板、决策记录、学习账、进化提案里仍有“未确认/未安装/未激活/待真机”的旧话。这不是“文档写得少”，而是**状态只存在于散文里**。

v0.9 的部署修订：

1. **两个根**：产品根（可在仓库根或 `product/`，由 `PROJECT.json.roots.product` 定义）+ 治理根 `aecw/`；`workspace/` 只放证据/记忆/落地，不放产品代码。
2. **项目清单** `PROJECT.json`：两个根、安装目标、`test`/`probe`/`check` 命令、工具版本；文档不手抄命令。
3. **单一状态源** `state.json` + `STATUS.md` 视图：阶段/发布/进化/采纳/证据债只在一个地方有值。
4. **验收矩阵** `criteria.md`：每条判据一行；`met/waived/deferred` 必须有证据/人类裁决；`有条件通过` 必须绑定具体行。
5. **四条泳道**：stage / maintenance / evolution / release；阶段关闭只关闭 stage，不关闭项目。
6. **动作完成 = 状态写回**：布局/安装/版本/tag/发布/远程变化后，先写 `state` + `STATUS` + 证据，再回复；`check` 校验 `state.layout`/`state.install`/`state.remote` 与 `PROJECT.json`、git origin 一致。
7. **入口与通道**：设置页“人找得到”是验收对象；抑制浮层 ≠ 抑制系统通知。
8. **check 查事实，probe 查现场**：`check` 升级到路径/命令/文档状态/Markdown 围栏/状态一致性；`probe` 查安装/路由/slot。

**不要**把本原型的三域目录直接当成真实仓库布局；真实部署按 [v0.9 迁移顺序](../PLAN-v0.9-真实项目校准.md) §5 做“真话修复 → 项目清单 → 验收矩阵 → 状态源 → check 升级”。
