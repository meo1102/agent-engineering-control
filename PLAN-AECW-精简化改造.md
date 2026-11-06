# AECW 精简化改造方案 v2（一次整改）

> 状态：proposal｜日期：2026-11-06
> 目标：**准确优先，效率其次；解放人的注意力，让集群在边界内自我实现。**
> 原则：**一个源、一个门、一个验证、一个进化闭环、按风险分级；先删后加。**
> 非目标：不加新角色、不做新 dashboard、不重写产品、不追求所有历史文档一致（归档即可）。
> 配套图：[精简结构图](diagrams/cluster-minimal-structure.png)
> 审计依据：[红队整改验收](REVIEW-task-complete-toast-aecw-redteam-acceptance-2026-11-06.md)
> 执行方式：**一个整改批次、一个分支、一次最终验收；不再分 S1–S5 等人类逐段批准。**

---

## 0. 一句话

把治理从“多文档、多道门、每步签字”改成：

> **state.json 一个源 + evidence 一份证据 + decision 一份人类决定 + evolution 一个学习闭环；标准变更默认放行，高风险才加 freeze/独立验证。**

不是再设计一套更漂亮的流程，而是删掉不改善“准确/注意力”的机制；进化也不是新角色/新阶段，而是 run 后的候选—评估—采纳/淘汰。

---

## 1. 目标结构

| 域 | 只保留 | 不再做 |
|---|---|---|
| **人类** | 方向/边界/停止；一次阶段或发布决定；S1/S2 例外；真实使用验收；直读 state/evidence | 逐单审批、维护台账、每门签字、替集群写方案 |
| **集群** | 编排者单写；worker 隔离实现；高风险独立验证；按需红队/策展 | 常设四角色、空 gate、形式化审查、自己批 charter |
| **工作区** | `state.json`、`evidence/`、`decisions/`、`evolution/`、`product` | 多份 board/release/manifest 当前值、32 行活矩阵、证据债分类账 |
| **底座** | DSH workflow、worktree、原子写/锁、tests/probe | 为治理再造运行时 |

核心不变量：

1. **单写者**：只有编排者写 mainline 与 state。
2. **证据绑定**：verify 记录绑定当前树、日志、reviewer。
3. **人类只决定**：不替集群执行，不被空模板绑架。
4. **风险分级**：不是所有变更都走全套阶段仪式。
5. **进化闭环**：每轮最多 1 个候选；E1 自动、E2 人类；不在 run 中途改基线。

---

## 2. 保留 / 合并 / 删除

| 现有机制 | 处理 | 替代/原因 |
|---|---|---|
| `state.json` | **保留** | 唯一当前状态源 |
| `STATUS.md` | **改为生成视图** | 只读；不再手改当前值 |
| `cluster/board.md` | **归档** | 任务板并入 state/run 记录；不再维护当前副本 |
| `cluster/release.md` | **归档** | 发布状态进 state + decision |
| `landing/manifest.md` | **归档** | 由 state/渲染生成 |
| `criteria.md` 32 行 | **压缩到 ≤10 行当前阻塞项** | 历史验收归档，不再作为活矩阵 |
| `gates/*.md` | **归档** | 新模型只留 `decisions/<id>.json` |
| `gate` 命令/六段模板 | **废弃/兼容别名** | 改为 `decide`；拒绝空模板 |
| `verify` | **保留并加绑定** | 绑定 tree、日志、reviewer session |
| `freeze/start` | **只保留给高风险/多周阶段** | 标准变更不再 freeze/start |
| `evidence_debt` | **只保留“阻塞某个门”的条目** | 其余写 known issue，不建债务 ID |
| 常设红队/策展/验证者 | **取消常设** | 高风险按需临时指定 |
| 四平面/三域术语 | **只留文档解释** | 不作为运营流程/工件 |

删除原则：**一个机制如果既不提高准确，也不减少人类注意力，就删。**

---

## 3. 风险分级（方案核心）

| 级别 | 触发 | 流程 | 人类介入 |
|---|---|---|---|
| **L0 轻量** | 文档、注释、非行为性修改 | `check` + 相关测试 | 不预批；摘要通知 |
| **L1 标准** | 普通产品行为、低/中风险 | worker + tests/probe + 单写者合并；阶段/发布时一份决定记录 | 不逐单批；抽样/阶段验收 |
| **L2 高风险** | 安全边界、发布、不可逆、外部副作用、并发共享写、预算超限 | freeze + 独立验证 + 一份人类决定记录 + 可回滚 | 合并前一次决定 |

规则：

- **L2 才 freeze**；L0/L1 不冻结、不设独立验证者。
- **L1 仍要 tests/probe**；没有证据不能合并。
- **L2 的独立验证**必须是新鲜上下文，只读产物；不读实现者推理。
- **L0/L1 的异常**（测试失败、S1/S2、范围变化）自动升级到 L2 或人类。

这套分级替代“每次改动都五阶段、每阶段多道门”。

### 3.5 进化机制：候选 → 评估 → 采纳/淘汰

**位置**：进化不在人类域，也不设新角色；它发生在每一轮 run 的 `evidence/decision` 之后、下一次 run 之前。是一个闭环，不是一道门。

```text
run
  → evidence + decision
    → 复盘：最多 1 个候选
      → 评估
        ├─ E1 项目级：tests/probe A/B → 自动采纳/淘汰（通知人类）
        └─ E2 治理级：独立复核 + 人类决定 → 采纳/拒绝
          → 版本化 prompt/skill/workflow/memory
            → 下一轮 run pin 版本
```

**三档进化**：

| 档 | 范围 | 谁决定 | 生效 |
|---|---|---|---|
| **E0 局部** | 当前 run 内的提示顺序、工具选择、临时策略 | 执行 agent | 只在本 run 生效，不持久化 |
| **E1 项目级** | 提示、技能、检查单、测试、工作流步骤、记忆条目 | 集群自动采纳；人类可抽样否决 | 过测试/无回归；版本化，可回滚 |
| **E2 治理级** | 目标、判据、门禁、权限、风险分级、reviewer 独立性、安全边界 | 人类 + 独立复核 | 绝不自动；新版本 + 人类决定 |

**候选格式**（`workspace/evolution/candidates/<id>.json`）：

```json
{
  "id": "EV-2026-11-06-01",
  "type": "skill|prompt|test|workflow|memory|tool",
  "scope": "project|governance",
  "observation": "这次哪里慢/错/重复",
  "evidence": ["attestation/log/hash"],
  "change": "具体改什么",
  "expected": "预期减少什么成本/错误",
  "risk": "low|high",
  "rollback": "怎么撤回"
}
```

**硬规则**：

- 每轮 run 最多 1 个候选；10 分钟复盘，不开常设会议。
- 单次轶事不够；至少 2 次 run 的证据，或 1 次高风险事故复盘。
- E1 必须过 tests/probe，且无准确率回归；人类收到通知，可抽样否决。
- E2 必须人类决定 + 独立复核；agent 不得自批。
- 不允许在 run 中途改基线；版本 pin 在 run manifest，下一轮才生效。
- 无效候选 3 次使用后仍无改善 → 淘汰；保留负记忆，不删除。
- `workspace/evolution/ledger.jsonl` 只追加：候选、评估、决定、回滚。
- 只有被采纳的才进 `workspace/memory/`；候选不得当事实。

**进化验收**（dry run 必须过）：

1. 一个 E1 候选：A/B 通过 → 自动采纳，下一轮生效；
2. 一个 E2 候选：未获人类决定 → 拒绝，不得生效；
3. 一个失败候选：回归/无效 → 标记 retired，留负记忆。

---

## 4. 目标数据模型

### 4.1 `state.json`（唯一源）

只保留当前值：

```json
{
  "project": "task-complete-toast-aecw",
  "owner": { "name": "meo1102" },
  "stage": { "name": "security-1", "state": "closed" },
  "release": { "version": "1.3.1", "state": "released", "decision": "workspace/decisions/DR-2026-...json" },
  "risk": "high",
  "evolution": { "active": ["skill-2026-11-06-01"] },
  "links": { "product": ".", "evidence": "aecw/workspace/evidence" }
}
```

不再手写 `board/release/manifest` 的当前值；`STATUS.md` 由 `render` 生成。

### 4.2 `workspace/decisions/<id>.json`（唯一的门）

```json
{
  "id": "DR-2026-11-06-1.3.1",
  "scope": "release 1.3.1",
  "risk": "high",
  "facts": ["产品 174/174", "probe 7/7", "check 0/0"],
  "evidence": [
    { "path": "aecw/workspace/evidence/attestations/VA-....json", "sha256": "..." }
  ],
  "conditions": [
    { "text": "浏览器保存真机复验", "due": "2026-11-20", "owner": "meo1102" }
  ],
  "residual_risk": "307/routePath/live 限速未真机",
  "human": { "name": "meo1102", "decision": "有条件接受", "at": "..." },
  "attestation": { "tree_hash": "sha256:...", "path": "..." }
}
```

硬规则：

- `facts`、`evidence` 不能为空；`conditions` 可以为空（无条件通过），但必须显式写 `[]`。
- `human.name` 必须是 owner；agent 不得代写。
- `attestation.tree_hash` 必须等于当前树；否则拒绝。
- 不允许“表头齐全、正文空”的 gate。

### 4.3 `evidence/`

- 只追加：测试/探针日志、哈希、verify 记录、reviewer 结论。
- 不再为每道门复制一份摘要。
- 旧 gates 归档到 `workspace/archive/gates/`，只读。

### 4.4 目录就这些

```text
aecw/
  state.json                 # 唯一当前状态
  STATUS.md                  # 生成视图
  workspace/
    evidence/                # 只追加
    decisions/               # 唯一的门（一份决定一个 JSON）
    evolution/               # 候选 JSON + ledger.jsonl
    memory/                  # 仅已采纳
    archive/gates/           # 旧门禁只读归档
  bin/aecw.mjs               # check / verify / decide / evolve / render
```

`board`、`release`、`manifest`、`criteria` 不再各自维护当前值；需要的当前信息从 state/render 来，历史进 archive。


---

## 5. 命令面（尽量少）

| 命令 | 作用 | 说明 |
|---|---|---|
| `aecw check` | 结构/一致性 | 不是授权；发现空 decision/状态漂移即 FAIL |
| `aecw verify` | tests + probe + 树/日志/reviewer 绑定 | 写 attestation；不接受伪造 JSON |
| `aecw decide` | 从 attestation + 人类输入生成 decision | 替代 gate；拒绝空 facts/evidence |
| `aecw evolve` | 候选、评估、采纳/淘汰 | 每轮最多 1 候选；E2 需人类 |
| `aecw render` | 生成 STATUS | 只读视图 |
| `aecw change` | 范围/判据变更 | 仍由人类裁决；不原地改冻结基线 |
| `aecw freeze/start` | **仅 L2** | 不再用于 L0/L1 |
| `aecw dissent/resolve` | S1/S2 例外 | 保留，不常设角色 |

兼容策略：

- `gate` 保留一个版本作为别名：调用时提示“已废弃，请用 decide”，**不再生成空模板**。
- 旧 gate 文件归档，不删除；新 decision 可引用旧 attestation/证据。

---

## 6. 一次性整改（一个分支、一次最终验收）

**不再分 S1–S5 等人类逐段批准。** 所有工作包在同一个整改分支完成，最后只做一次人类验收。内部顺序如下，能并行的并行。

### W0 · 冻结、备份、归档（0.5 天）

- 打 tag `pre-simplify-2026-11-06`，记录回滚点。
- 旧 gates/board/release/manifest 复制到 `workspace/archive/`，只读，不删除。
- 记录基线：人类分钟、当前状态活文档数、每 release 门禁数、缺陷逃逸/假 PASS。
- **不改产品、不改 1.3.1 发布结论。**

### W1 · 单一状态源（1 天）

- `state.json` 补 `decision`/`risk`/`evolution` 字段；`STATUS` 改为生成。
- `board/release/manifest` 当前值合并进 state，旧文件归档。
- `criteria` 压到当前阻塞项（≤10 行）；历史进 archive。
- `check` 增加：state 与 STATUS 不一致、空 decision、重复当前源 → FAIL。

### W2 · 一个门（1.5 天）

- 新增 `workspace/decisions/` 与 `decide`；从 1.3.1 的 attestation、`0700071129`（superseded 但有完整事实/条件）与 release 证据**回填一份 decision**（不重新发布；不复制 final 空 gate）。
- `gate` 改为废弃别名，拒绝空模板；旧 gates 归档。
- `verify` 增加：attestation ID/文件名/日志哈希/reviewer session 绑定；拒绝任意路径 JSON。
- `check` 拒绝空 facts/evidence、缺人类签名、tree 不一致。

### W3 · 风险分级（1 天）

- 实现 L0/L1/L2 判定与路径。
- L0/L1 不再 freeze/start；L2 才 freeze + 独立验证。
- 更新 AGENTS/README：默认相信、例外升级；人类只做一次决定/抽样。
- 保留 `change` 处理范围变化。

### W4 · 进化闭环（1 天）

- 新增 `workspace/evolution/`：`candidates/` + `ledger.jsonl`。
- 实现 E0/E1/E2 评估与采纳/淘汰；E1 自动采纳需 tests/probe + 无回归；E2 必须人类 + 独立复核。
- 复盘最多 1 个候选；版本化 prompt/skill/workflow/memory；下一轮 pin 版本。
- dry run：E1 采纳、E2 拒绝、失败候选 retired 各一次。

### W5 · 迁移与兼容（0.5 天）

- 旧 gate 保留一个版本别名，提示“请用 decide”；不再生成空模板。
- 旧当前视图归档，不双轨超过一个迭代。
- 更新 STATUS/README/AGENTS 的入口与命令；清理断链。
- 确认 `check`/`verify`/`decide`/`evolve`/`render` 五条主命令可用。

### W6 · 验收与度量（0.5 天）

- 跑完整产品/治理测试、probe、负控（伪造 attestation/空 decision/状态漂移）。
- 用 3 个真实变更测：人类分钟/介入次数、缺陷逃逸/假 PASS、L1 自主完成率。
- 人类只做一次最终验收：接受 / 有条件 / 退回。
- 指标不达标就回退对应机制；不带着新复杂度进入下一轮。

**批次出口**：上述 W0–W6 全过，或整体退回；不允许“只做一半就宣布完成”。

---

## 7. 验收标准

### 准确（硬约束）

- 0 个伪造 attestation 被接受；
- 0 个空 decision/空 gate 被接受；
- 0 个 state/STATUS 当前值矛盾；
- 缺陷逃逸不高于基线；
- 32 路并发写不丢、不重、不截断；
- L2 有独立验证与 tree 绑定；
- E2 未获人类决定不得生效；E1 回归即撤回；失败候选 retired 且留负记忆。

### 效率（目标）

- live 当前文档：6 → 2（state + 生成 STATUS）；
- 每 release 门禁：多份 → 1 份 decision；
- criteria 活行：32 → ≤10；
- 标准变更人类预批：0 次；
- 人类分钟/变更：下降 ≥30%（3 个变更的实测，不虚构）。

### 自我实现

- ≥70% L1 变更由集群计划/实现/合并，无需人类逐单介入；
- 异常升级准确：该升级的升级，不该升级的不打扰；
- 每轮 run 最多 1 个进化候选；E1 自动采纳、E2 人类决定、失败淘汰；
- 每次 run 留 1 条记忆/技能候选；不自动激活。

---

## 8. 风险与不做

| 风险 | 缓解 |
|---|---|
| 简化后漏掉真实风险 | L2 触发清单 + 独立验证 + 抽样 |
| 旧 gate/证据断链 | 归档不删除；decision 引用旧证据 |
| 工具迁移破坏现有命令 | `gate` 兼容别名；一个批次；tag 回滚 |
| 人类失去控制感 | 一次决定 + 直读 state/evidence + S1/S2 |
| 集群自我扩权 | 单写者 + 人类签名 + change 门 + 审计 |
| 又变成空模板 | `decide` 从 attestation 生成 facts/evidence；空字段 FAIL |

不做：

- 不新增常设角色/新 dashboard/新“治理层”。
- 不重写产品代码；不改 1.3.1 发布结论。
- 不追求历史文档全部一致；归档即可。
- 不把 decision 做成新的六段空模板。

---

## 9. 执行方式

**不再分 Phase 等批准。** 按 §6 的 W0–W6 在同一整改分支一次做完：

- 中途只在 S1/S2、不可逆风险、预算耗尽时停；
- 人类只在两处出现：**异常裁决**和 **W6 最终验收**；
- 一个 tag、一个分支、一次最终决定：接受 / 有条件 / 退回；
- 不接受“做一半先上线”，也不接受“旧新双轨长期并存”。

这样即使方向有偏差，也能在一个 tag 内整体回滚，不会把现有 1.3.1 证据链拆坏。

---

## 10. 一句话总结

> **保留准确所需的硬边界，删掉效率不需要的仪式；让人类只做一次决定，让集群自己把事做完、把经验留下。**
