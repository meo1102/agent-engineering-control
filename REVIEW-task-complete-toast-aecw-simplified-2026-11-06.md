# AECW 精简化改造验收 · 概念框架审计

> 性质：agent 独立审计，不是人类验收；不替代 `meo1102` 的最终决定。
> 日期：2026-11-06
> 对象：`task-complete-toast-aecw` 的 AECW 0.10.0 精简化改造、1.3.2 conditional 发布、进化闭环。
> 结论一句话：**技术落地通过；概念框架有条件通过，不能称“已闭环”。**

## 1. 结论

| 层面 | 结论 | 依据 |
|---|---|---|
| 产品回归 | **通过** | 178/178 |
| 治理回归 | **通过** | 10/10；含 L2、32 路并发、E1/E2/retire 合成测试 |
| 结构/探针 | **通过** | `check` 0/0；probe 7/7 |
| 远程发布 | **通过** | `origin/main` = `55ed23e`；`v1.3.2` 已推送 |
| 单一源/单一门 | **基本落地** | state + generated STATUS/criteria；decisions/ |
| L2 freeze 绑定 | **不通过** | freeze 树 `270621…` ≠ 当前树 `2D817…`，仍被接受 |
| 条件生命周期 | **不通过** | 9 条永远 open；远程已完成仍 open；上限 10 将卡下一轮 |
| 进化闭环 | **条件不成立** | ledger 为空；E1 只跑 tests/probe，不证明“变好” |
| 当前文档一致性 | **不通过** | README/AGENTS/direction/decisions README 仍说未发布/未推送/待决定 |
| **总体** | **有条件通过** | 技术可用；概念层需补 4 个 P0 |

## 2. 实测

```text
产品 tests        178 / 178
治理 tests         10 / 10
check              FAIL 0｜WARN 0；tree 2D817AAD…
probe              7 / 7
remote main        55ed23e
remote v1.3.2      0f0da9c（tag）
工作树             clean
```

说明：远程已推送，`STATUS`/`criteria` 仍把“远程 push”列为 open，是条件未闭合，不是远程失败。

## 3. P0：框架层阻断

### P0-1 freeze 不是冻结，只是“文件存在”

- `state.stage.freeze` 指向 `FREEZE-product-hardening.json`，其 `tree_hash = 270621…`。
- 当前 `check` 树 = `2D817AAD…`；`DR-2026-11-06-1.3.2` 是 high risk，仍被接受。
- `aecw/bin/aecw.mjs:1180-1185` 只检查 stage 为 frozen/active、freeze 文件存在、有 `tree_hash`、verify independent；**没有比较 freeze.tree_hash 与 attestation.tree_hash**。
- 后果：L2 的“冻结”没有绑定实际交付树；freeze 可以是一个旧基线，release 仍通过。这直接违背“准确”。

**改法**：L2 `decide` 必须校验 `freeze.tree_hash === attestation.tree_hash`；或明确把 freeze 降级为“阶段授权”，删除 tree 绑定语义，不能两者混用。

### P0-2 条件只会 open，不会 close

- `DR-1.3.2` 有 9 条 conditions；其中“远程 push main + v1.3.2”已完成（remote 已确认），但 `STATUS`/`criteria` 仍显示 open。
- `collectConditions` 把所有 conditions 一律标 `open`（`aecw.mjs:454-461`、`:535`）；没有 `close/waive` 命令，也没有条件证据。
- `MAX_CRITERIA = 10`（`:30`）；当前 9/10。下一份 release decision 只要有 2 条条件就会失败。
- 后果：条件不是“待办”，而是永久积压；人类注意力被已完成项占用，下一轮被硬上限卡住。

**改法**：把 condition 变成独立生命周期：
`workspace/conditions/<id>.json` 或 `condition-events.jsonl`，字段 `open/closed/waived + evidence + closed_by/at`；`decide` 只建 open；`resolve-condition` 关闭；`render` 只显示 open；`check` 验证关闭项有证据；cap 只数 open。

### P0-3 进化闭环“有代码、无真实进化”

- `workspace/evolution/ledger.jsonl` 为 **0 字节**；`state.evolution.active = []`。
- `evolve evaluate` 对 project 候选只做“tests/probe 都 pass”（`aecw.mjs:1297-1312`），**没有 A/B、没有基线指标、没有 improvement**；`candidate.change` 是自由文本，没有 artifact path/hash/version；`adopt` 只把 id 写进 state（`:1354-1360`）。
- 后果：任何不破坏测试的候选都可被“采纳”；它可能只是空操作或未测退化。当前没有一次真实 candidate，无法证明“集群会学习”。

**改法**：候选必须带：
`artifact {path, sha256, version}`、`evaluation {baseline, candidate, metric, delta, eval_set, logs}`、`run_id`；E1 只在“指标改善且无回归”时自动采纳；adopt 写版本/hash 到 state；verify 记录 active versions；失败/无改善 retire。

### P0-4 “一个源”没覆盖人读文档

- `README.md:122` 仍写“1.3.2 候选未发布；远程 main/v1.3.2 未推送”，但当前已 conditional 发布且远程已推送。
- `AGENTS.md:50` 仍写“远程未推送”。
- `direction.md:44-46` 仍写“1.3.2 发布 decision 待人类”，实际已有 `DR-1.3.2`。
- `decisions/README.md:7` 只列 1.3.1，并链接已归档、当前不存在的 `DR-2026-11-06-1.3.1.json`；当前 decisions 只有 1.3.2。
- `check` 0/0；它只校验 state/STATUS/criteria/decision，不校验这些“人读当前文档”。

**改法**：二选一：
1. README/AGENTS/direction/decisions README 的当前状态段由 `render` 生成；
2. 明确标记它们为 narrative，删除当前状态断言，只留“以 STATUS 为准”。
并修 `decisions/README` 的索引/链接。

## 4. P1：概念框架需要改进的地方

### 4.1 condition 是“承诺”，不是“状态”

当前模型把 condition 写进已签 decision，导致：
- 决定不可改，条件也不可关；
- 已完成的条件继续阻塞；
- 条件上限 10 会卡下一轮。

**概念修正**：decision 记录“当时承诺了哪些条件”；condition 是独立对象，有生命周期和证据。  
不要把“条件文本”当“当前阻塞项”；当前阻塞项应是 condition 的投影。

### 4.2 freeze 的语义混在一起

现在 freeze 同时像：
- 阶段授权（start 前）；
- 交付树基线（tree_hash）；
- L2 的“冻结”。

三者没有区分，代码只检查“存在”。  
**概念修正**：明确两类：
- **Stage authorization**：谁可以开始、范围/预算/停止；不绑定交付树。
- **Release baseline**：这一版绑定的 tree/commit；必须与 attestation 相等。
不要用一个 `FREEZE` 同时承担两者。

### 4.3 进化需要“评估函数”，不是“测试通过”

`E1 = tests/probe pass` 只是非回归，不是 improvement。  
**概念修正**：每个候选必须声明：
- 目标指标（如 human minutes、rework、false pass、latency）；
- 固定 eval set / 对照 run；
- 基线值、候选值、delta；
- 失败/回滚条件。
没有指标的候选只能进 `retired` 或 human review，不能自动 adopt。

### 4.4 “独立验证”仍是声明位

`reviewer.independent` 是布尔标志；`attestation` 仍是本地 JSON。  
**概念修正**：
- L 模式写清 `threat_model: local-trusted`；`independent` 只表示“新鲜上下文 + 非作者”，不表示抗伪造。
- 至少要求 `reviewer != owner`，记录 session、输入 hash、review 文件 hash。
- 要抗伪造，必须 E 模式签名/外部身份；不要在当前 L 模式宣称“0 伪造”。

### 4.5 风险分级是自报

`state.risk` / `decide --risk` 由人/agent 选；L2 只检查 freeze 文件和 independent 布尔。  
**概念修正**：增加确定性触发：
- 改 `lib/host.js`、`index.js`、`package.json`、权限/路由/发布脚本 → 至少 high；
- 安全边界、外部副作用、不可逆、并发共享写 → high；
- 只有文档/测试/非行为改动才允许 low。
否则“风险分级”只是标签。

### 4.6 stage 与 release 生命周期重叠

`state.stage = product-hardening/active`，同时 `release = 1.3.2/conditional`。  
当前 freeze 是 stage 的旧树，release 是新树；两个生命周期没有闭合。  
**概念修正**：
- stage closed 才能 release；或 release 走独立 lane，有自己的 baseline，不继承 stage freeze。
- 不能一边 stage active、一边 release conditional、一边 freeze 还是旧树。

### 4.7 “集群”仍是单 agent 多上下文

产品构建、验证、发布基本由一个 agent + 可选 fresh-context reviewer 完成；`worker × N` 没有真实并行证据，`evolution` 无候选。  
**概念修正**：
- 当前应叫 **“工单制多上下文执行”**，不宣称“自组织集群”。
- 只有出现多个独立 worker、真实并行写集、独立 verifier 产出被采纳，才升级“集群”叙事。
- 否则“自我实现”只是“单 agent 自动执行”，没有种群/选择/代谢的证据。

### 4.8 人类注意力指标未测

计划 §7 要求人类分钟下降 ≥30%、L1 自主率 ≥70%，当前没有 3 个样本。  
**概念修正**：把“人类分钟/决策次数/被打断次数”作为一等工作指标；没有测量，就不能证明“解放注意力”。

### 4.9 发布 verify 在 dirty tree 上完成

- `VA-20261106095521-fb09f8.json` 记录 `git.head=47c1cef`、`git.dirty=true`；1.3.2 发布 commit 是 `55ed23e`。
- `verify` 不拒绝 dirty；`decide` 只比较内容 tree，不绑定 commit/tag。
- 内容 tree 匹配当前树，所以不是“内容错”；但发布验证不是在干净、已提交的发布点上做的，可复现性和“发布 commit”关系不明确。

**概念修正**：high-risk verify 要求 clean tree，或显式记录 dirty 原因 + diff hash；decision 绑定 `release_commit`/tag，而不只 tree。


## 5. 建议修复顺序

1. **P0-2 条件生命周期**（最高优先）：关闭 remote push 条件，修 9/10 上限；否则下一轮 release 无法创建。
2. **P0-1 freeze 绑定**：L2 比较 freeze/attestation tree；或明确降级 freeze 语义。
3. **P0-3 进化工件**：候选加 artifact/version/metric；跑一次真实 E1；ledger 不能为空。
4. **P0-4 文档收口**：README/AGENTS/direction/decisions README 去当前状态断言或生成；修坏链。
5. **P1**：risk 触发、reviewer != owner、stage/release 分离、指标测量。

## 6. 不得宣称

- 不得说“条件已闭环”：remote push 已完成但仍 open。
- 不得说“L2 freeze 已绑定”：freeze 树与当前树不一致。
- 不得说“集群会进化”：ledger 为空，E1 只证明测试通过。
- 不得说“一个源覆盖所有当前文档”：README/AGENTS/direction 仍漂移。
- 不得说“独立验证抗伪造”：`independent` 是布尔记录位，L 模式。
- 不得说“人类注意力已下降”：没有 3 个样本。

## 7. 验收结论

**技术层：通过。** 简化结构、单 decision、verify 绑定、并发锁、1.3.2 修复、远程推送都成立。

**框架层：有条件通过。** 不是“再写文档”，而是四个结构性修正：
1. condition 要有生命周期；
2. freeze 要真绑定树；
3. evolution 要有工件/指标；
4. 人读文档也要受一个源约束。

在这四条修完之前，AECW 0.10.0 可以叫“可用”，不能叫“闭环”。

## 8. 证据位置

- 当前树：`aecw/STATUS.md`、`aecw/state.json`；`check` tree `2D817AAD…`
- 1.3.2 decision：`aecw/workspace/decisions/DR-2026-11-06-1.3.2.json`
- 1.3.2 attestation：`aecw/workspace/evidence/attestations/VA-20261106095521-fb09f8.json`（`git.dirty=true`，head `47c1cef`）
- freeze：`aecw/workspace/decisions/FREEZE-product-hardening.json`（tree `270621…`）
- 条件生成：`aecw/bin/aecw.mjs:454-461`、`:535`；上限 `:30`、`:1155`
- L2 检查：`aecw/bin/aecw.mjs:1180-1185`
- 进化评估：`aecw/bin/aecw.mjs:1297-1312`；adopt `:1354-1360`
- 进化 ledger：`aecw/workspace/evolution/ledger.jsonl`（0 字节）
- 文档漂移：`README.md:122`、`AGENTS.md:50`、`aecw/workspace/memory/direction.md:44-46`、`aecw/workspace/decisions/README.md:7`
- 远程：`git ls-remote` main `55ed23e`；tag `v1.3.2` `0f0da9c`
