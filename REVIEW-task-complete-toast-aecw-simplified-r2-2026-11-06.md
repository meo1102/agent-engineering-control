# AECW 精简化改造复验 · 进化试点专项

> 性质：agent 独立审计，不是人类验收；不替代 `meo1102` 的最终决定。
> 日期：2026-11-06
> 对象：AECW 0.10.0 精简化改造第二轮、1.3.2 conditional 发布、首次进化试用 `EV-2026-11-06-01`。
> 结论：**技术层通过；框架层有条件通过。进化试点“机械闭环成立”，但“变好”尚未被因果证明。**

## 1. 复验结果

| 项 | 结果 |
|---|---|
| 产品 tests | **178 / 178** |
| 治理 tests | **10 / 10** |
| `check` | FAIL 0｜WARN 0；tree `7B994592…` |
| probe | **7 / 7** |
| 远程 main | `042e012` |
| 远程 `v1.3.2` | `93bbe39`（tag） |
| 工作树 | clean |
| conditions | **8 open / 10**；远程 push 条件已 closed |
| evolution | **1 active**：`EV-2026-11-06-01` |

相比上一轮，**condition 生命周期**和**进化工件/指标/ledger**确实落地了；不是空机制。

## 2. 先看进化：这次试行做到了什么

### 2.1 机械闭环成立

候选：`aecw/workspace/evolution/candidates/EV-2026-11-06-01.json`

- type `workflow`，scope `project`；
- artifact：`aecw/bin/aecw.mjs`，sha256 `3C2B2FC6…`，version `0.10.0+condition-lifecycle`；
- metric：`open-conditions`，direction `lower`；
- evaluation：baseline `9` → candidate `8`，delta `-1`，`improved: true`；
- tests/probe 日志有 hash；
- eval log：`aecw/workspace/evidence/evolution/2026-11-06-condition-lifecycle.json`；
- ledger 三条：`proposed → evaluated → adopted`；
- `state.evolution.active = ["EV-2026-11-06-01"]`，`versions` 记录 artifact path/hash/version；
- `check` 会校验 artifact 哈希、metric、baseline/candidate/delta、eval_log、tests/probe 日志；
- 当前 CLI 实际哈希 `3C2B2FC6…`，与 artifact/state 一致。

这比上一轮“ledger 0 字节”有实质进步：**候选、评估、采纳、版本、证据链都真实存在**。

### 2.2 但“变好”没有被证明

这次 trial 的核心问题是：**指标和变化不是因果闭环。**

- 指标是 `open-conditions`，从 9 降到 8；
- 降低的直接原因是关闭了 `C-2026-11-06-09`（远程 push 已完成）；
- 候选变化是“condition lifecycle + close with evidence + decision baseline”；
- 远程 push 不是这个候选做的；关闭条件也不是“相同任务下 A/B”的结果。

所以它证明了：
> “我们可以用新流程记录一次 workflow 变化，并把 open-conditions 从 9 记到 8。”

它没有证明：
> “这个变化让集群更准确或更省人类注意力。”

### 2.3 评估证据太薄

- `eval_log` 只有 8 行：metric/baseline/candidate/note/measured_at；没有测量命令、样本、时间窗、对照组。
- `candidate.evidence = []`；候选本身没有引用 observation 的证据（例如条件清单、remote 证据、closed 前后截图/命令）。
- `DR-1.3.2` 的 `facts` 提到“evolution adopted”，但 `evidence[]` 没有 candidate JSON、eval log、ledger；release decision 没有绑定这次进化。
- E1 自动采纳只要求 `improved=true` + tests/probe；`improved` 来自 `--baseline/--candidate` 两个人工传入的数字，不是独立测量。
- `open-conditions` 是治理过程指标，可被“关闭/归档条件”改善，不必改善产品准确率或人类注意力。

**判断：这是一次合格的“进化管线试运行”，不是一次合格的“进化效果验证”。**

## 3. 仍未闭合的 P0

### P0-1 baseline commit 与 tree 不一致

`DR-1.3.2`：

```json
"baseline": {
  "tree_hash": "sha256:7B994592…",
  "commit": "e956725e9a07848b4232ee8cab7344d29bd41726"
}
```

实测：

- 当前 tree：`7B994592…`
- 用当前 CLI 在 `e956725` 的干净 worktree 上跑 `check`：tree = **`6C675321…`**
- 即 `baseline.commit` 指向的 commit，并不包含 `baseline.tree_hash` 对应的树。
- `aecw.mjs` 只校验 `baseline.tree_hash === currentTree` 和 commit 字符串格式；**不校验 commit 的实际树**。
- `VA-20261106103641-fdea52` 仍是 `git.dirty: true`，head `e956725`；发布 commit 是 `042e012`。

结论：**baseline 仍然是“标签”，不是可复现的提交绑定。** 这是准确性 P0。

修法：
- high-risk verify 拒绝 dirty；或显式记录 dirty diff hash + 原因；
- `decide` 必须验证 `baseline.commit` 的实际树 = `baseline.tree_hash`；
- release decision 的 baseline commit 必须是发布 commit/tag，不是 verify 时的旧 head；
- 或者明确只使用 content tree，不再声称 commit baseline。

### P0-2 发布 tag 被移动，条件关闭证据仍是旧状态

- `aecw/workspace/evidence/2026-11-06-remote-push.md` 记录：`origin/main = 55ed23e`、`v1.3.2 = 0f0da9c`。
- 当前实际：`origin/main = 042e012`；`v1.3.2` tag 对象 = `93bbe39`，peeled commit = `042e012`。
- 即 `v1.3.2` 已被重新指向新 commit；发布 tag 不是不可变的。
- `C-2026-11-06-09`（远程 push）已 closed，证据正是这份旧 remote-push 记录（hash `C7233C…`）；关闭时没有重新验证当前 tag/main。
- `2026-11-06-product-1.3.2.md:19/40` 仍写“远程未推送”；当前已推送。
- `check` 0/0；它不校验 release tag 是否移动、条件证据是否仍对应当前事实。

结论：**发布 tag 可以移动，条件可以用旧证据关闭；这会让 release decision 指向一个已经变化的“1.3.2”。** 这是准确性 P0。

修法：
- release decision/state 写入 `tag`、`tag_object`、`commit`、`tree_hash`，并校验 tag 不可变；
- 移动 tag 必须视为新 release（新版本或显式 supersede），不能原地改 `v1.3.2`；
- condition close 的 evidence 必须包含“当前事实”的复核（`git ls-remote` 输出/tag peeled commit），不能只引用旧文件 hash；
- `check` 校验 release tag 与 baseline commit/tree 一致；条件关闭证据过期则 FAIL。

## 4. P1：概念框架要改的地方

### 4.1 进化评估要“预注册 + 对照”

当前 E1 是“人工填 baseline/candidate，tests pass 就自动采纳”。  
应改成：
- 候选提出时预注册：metric、direction、eval set、baseline 值、测量命令、成功阈值；
- 评估时跑同一组任务/样本，记录 baseline/candidate 原始输出；
- 只有 `delta` 达到阈值且无回归，E1 才自动采纳；
- 否则 human review 或 retired。

至少要求 `eval_log` 含：命令、样本 id、原始值、时间、执行者；不能只有 8 行摘要。

### 4.2 指标要贴“准确/效率”，不要只用过程指标

`open-conditions` 是治理过程指标，不是产品/集群效果指标。建议优先：
- human minutes / 决策次数；
- 缺陷逃逸 / 假 PASS / 返工；
- time-to-accept；
- L1 自主完成率。

`open-conditions` 可以作为辅助指标，但不能单独支撑“进化有效”。

### 4.3 decision 必须绑定它声称的 evolution

`DR-1.3.2` facts 说“evolution adopted”，但 evidence 没有 candidate/eval log/ledger。  
应把 `evolution: [{id, artifact, version, sha256, eval_log}]` 写进 decision，或至少在 evidence 中列 candidate/eval log；否则 release 记录不能重现“当时采纳了什么”。

### 4.4 freeze / baseline / stage 三者要分清

- `FREEZE-product-hardening` 的 tree 是 `270621…`，当前 tree `7B994…`；stage 是 active，`check` 只在 frozen 时校验 freeze tree，所以不报错。
- 现在 decision 有 `baseline`，这是正确的方向；但 freeze 文件仍带旧 tree，语义混在一起。
- 建议：
  - **stage authorization**：范围/预算/停止，不绑定 tree；
  - **release baseline**：commit + tree，必须与 attestation 一致；
  - 不再让 `FREEZE` 同时承担两者。

### 4.5 “独立验证”仍是记录位

`VA-fdea52.reviewer.independent=true`，但仍是本地 JSON；`reviewer` 是 `aecw-product-independent`。  
L 模式下可以接受“新鲜上下文 + 非作者”的记录，但不能宣称抗伪造；建议在 state/decision 写 `threat_model: local-trusted`，并强制 `reviewer != owner`。

### 4.6 “集群”仍是单 agent 多上下文

这次 evolution 是 **治理工具/工作流变化**，不是 agent 技能/行为进化；当前没有多 worker 并行、没有独立 verifier 被真实采纳。  
概念上应叫“工单制多上下文执行 + 工具进化试点”，不要宣称“自组织集群/集群自我实现”。

### 4.7 条件生命周期已修，但还有两个问题

- 条件上限 10；当前 8 open，下一轮如果新增 3 条会失败；需要 aging/waiver/priority，而不是硬上限。
- `condition close` 的 evidence 是文件 hash；C-09 已关闭，但证据记录的是旧 `main/tag`（55ed23e/0f0da9c），当前是 042e012/93bbe39；关闭证据没有随事实更新。
- `criteria` 只显示 open，不显示“最近关闭”/关闭证据；人类看不到“已做了什么”，只看到剩余。

## 5. 本轮通过项

- condition 生命周期真实落地：8 open / 10，remote 条件已 closed（但证据需刷新）。
- 进化管线真实落地：candidate/artifact/version/metric/eval_log/ledger/state active，`check` 校验。
- 1.3.2 decision 有 baseline、condition_ids、independent review、attestation。
- 产品 178/178、治理 10/10、check 0/0、probe 7/7。
- 远程 main/tag 已推送。
- `README`/`AGENTS`/`direction`/`decisions/README` 的当前状态已更新到 1.3.2/已推送；旧 decision 归档。
- 剩余陈旧的是 `2026-11-06-product-1.3.2.md:19/40` 与 `2026-11-06-remote-push.md`（旧 commit/tag）。

## 6. 结论与建议

**结论：技术层通过；框架层有条件通过。**

本轮不能给“accepted/闭环”，因为：
1. baseline commit 与 tree 对不上（准确 P0）；
2. `v1.3.2` tag 被移动、C-09 用旧 tag 证据关闭（发布不可变/条件证据 P0）；
3. 进化试点只证明管线能跑，不证明变好（概念 P1）。

建议按顺序：
1. 修 baseline：clean verify + commit tree 校验 + release commit/tag 绑定；重出 1.3.2 decision（不重新发布产品）。
2. 修 release tag/条件证据：tag 不可变；C-09 用当前 `git ls-remote` 重新关闭；更新 product/remote-push 证据。
3. 进化第二次 trial：固定 eval set、对照、outcome metric、eval_log 原始输出；再决定 E1 是否自动。
4. 把 evolution 写进 decision evidence；修 freeze/stage 语义；L 模式声明。

**进化试点的评价：方向正确，机制真实，但效果未证。** 这是一次合格的“第一次”，不是“进化已成立”。

## 7. 证据位置

- 进化候选：`aecw/workspace/evolution/candidates/EV-2026-11-06-01.json`
- 进化 ledger：`aecw/workspace/evolution/ledger.jsonl`
- eval log：`aecw/workspace/evidence/evolution/2026-11-06-condition-lifecycle.json`
- state evolution：`aecw/state.json:20-31`
- 1.3.2 decision：`aecw/workspace/decisions/DR-2026-11-06-1.3.2.json`
- 1.3.2 attestation：`aecw/workspace/evidence/attestations/VA-20261106103641-fdea52.json`（`git.dirty=true`，head `e956725`）
- 条件：`aecw/workspace/conditions/`（C-09 closed；8 open）
- 当前树：`7B994592…`；`e956725` worktree tree：`6C675321…`
- 远程：`origin/main 042e012`；`v1.3.2` tag `93bbe39`（peeled `042e012`）；旧证据 `55ed23e/0f0da9c`
- 陈旧证据：`aecw/workspace/evidence/2026-11-06-remote-push.md`、`2026-11-06-product-1.3.2.md:19/40`
- 当前文档已更新：`README.md`、`AGENTS.md`、`aecw/workspace/memory/direction.md`、`aecw/workspace/decisions/README.md`
