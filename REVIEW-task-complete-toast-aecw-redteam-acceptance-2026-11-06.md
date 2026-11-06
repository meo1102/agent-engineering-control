# 红队整改验收 · 独立审计（2026-11-06）

> 性质：**agent 独立审计**，不是人类验收，不替代 `meo1102` 的接受/拒绝。
> 范围：`task-complete-toast-aecw` 的 S1–S5 红队整改、1.3.1 发布门与当前治理记录。
> 结论一句话：**技术回归通过；治理验收不通过，退回补证。1.3.1 只能保持“有条件发布”，不能称“整改完成/验收通过”。**

## 1. 结论

| 层面 | 结论 | 依据 |
|---|---|---|
| 产品回归 | **通过** | 174/174；probe 7/7；check 0/0 |
| 治理工具回归 | **通过** | 25/25；S1/S2/S3/S5 负控 |
| S4 服务端安全 | **通过（有未测）** | security 5 项；live 矩阵；浏览器/307/routePath/lim 未真机 |
| 最终 release gate | **不通过** | 正文为空模板；仅表头有决策/attestation/签署 |
| attestation 可信性 | **不通过** | `gate` 接受临时副本里的伪造 attestation，exit 0 |
| 发布范围/人类记录 | **不通过** | 蓝图写明不发布 1.3.1；CR-007/验收记录未闭合 |
| 当前治理记录 | **不通过** | criteria/ledger/board/release/acceptance 仍漂移 |
| **总体** | **不通过（退回补证）** | 以上阻断项未清 |

## 2. 我复跑了什么

在仓库根 `D:\DSH\task-complete-toast-aecw`：

| 命令 | 结果 |
|---|---|
| `node aecw/bin/aecw.mjs check aecw` | FAIL 0｜WARN 0，exit 0 |
| `node aecw/bin/aecw.mjs check aecw --strict` | FAIL 0｜WARN 0（strict），exit 0 |
| `node aecw/scripts/probe.mjs` | 7/7 PASS，exit 0 |
| 产品 11 个测试文件 | tests 174 / pass 174 / fail 0 |
| 治理 S1+S2+S3+S5 | tests 25 / pass 25 / fail 0 |
| `probe --url http://127.0.0.1:1` | 5/7，exit 1（预期） |
| `probe --url .../?x=1` | 5/7，exit 1（query 拒绝，预期） |
| `probe --url .../#x` | 5/7，exit 1（fragment 拒绝，预期） |

这些结果说明 **S1–S3 的确定性检查、S4 的 probe 负控、S5 的结构/引用校验基本有效**，也说明产品测试没有被破坏。

## 3. 阻断项

### B1（P0）`gate` 可以接受伪造 attestation，并生成空内容“通过”门

证据：

- `aecw/bin/aecw.mjs:1060` `cmdGate` 读取 attestation 后，只校验 `kind/ok/open_s1s2/tree_hash/project/expires_at/git.dirty`（`readAttestation`，`:372`），**不校验**：
  - attestation 是否位于 `workspace/evidence/attestations/`；
  - 文件名与 `id` 是否一致；
  - `checks` 的日志是否存在、哈希是否匹配；
  - `reviewer` 是否是独立/新鲜上下文；
  - 是否有签名或不可伪造的来源。
- 在临时副本中，把最终 attestation 复制成 `forged.json`，只改 `id=VA-FORGED-000000`、`reviewer=attacker`、时间，`gate --decision 通过 --signed-by meo1102` **仍 exit 0**，并生成：
  `2026-11-06-forged-audit-07245951f6.md`
- 生成的门禁正文是 `aecw/core/gate.template.md` 的空表：关键事实、主张 vs 事实、异议、负事实、决策理由、签署全部为空。

后果：

- “verify 是唯一通过类证据”在当前实现里是**字段校验**，不是来源校验；agent 可以手写/改写 JSON 通过门。
- `gate` 默认产出空模板，且没有任何“必须填写”的校验；通过类门禁可以以“表头 + 空正文”存在。
- 这不是“L 模式没有密码学签名”的可接受限制；即使 L 模式，也应至少绑定 verify 日志、文件名、reviewer session，并拒绝空正文。

### B2（P0）最终 release gate 本身就是空模板

文件：`aecw/gates/2026-11-06-release-v1-3-1-final-0711355f20.md`

- 表头：决策“有条件通过”、attestation、人类签署 `meo1102`；
- 正文：`关键事实` 三行全空；`主张 vs 事实` 空；`异议` 只有 `__`；`负事实` 空；`决策与理由` 空；`签署` 空。
- 对比：被取代的 `2026-11-06-release-v1-3-1-0700071129.md` 有完整事实/条件/理由，但它已标 `superseded`；当前 `state.release.gate` 和 `STATUS` 指向的是**空模板** final gate。
- 结果：当前 release 的“有条件通过”没有可审阅的条件、事实、剩余风险与签署正文；条件只散落在 release 证据/S5 证据里，未进入门禁。

### B3（P0/P1）1.3.1 发布越出冻结蓝图，CR/验收记录未闭合

- `aecw/BLUEPRINT.md:49` 明确本阶段不做：“**不发布 1.3.1 版本/tag**（本阶段只做候选代码与门禁；发布由后续决定）”。
- 但 1.3.1 已发布：`state.release.version=1.3.1`，tag `v1.3.1`，release gate final。
- `CR-007`（blueprint）头部写“accepted”，但：
  - `aecw/inbox/CR-007.md` 的影响分析、选项、裁决正文全空；
  - `ledger.md` 的 CR-007 行没有记录人类裁决人 `meo1102`（`cmdChange` 计算了 `by`，但没有写进台账）；
  - `aecw/human/acceptance.md` 没有 1.3.1 发布/安全收口的验收行，最后核对仍是 2026-11-05；
  - `aecw/human/decisions.md` 有 2026-11-06 发布指令，但最后核对仍写 2026-11-05。
- 结论：人类“全部完成后发布新版本”的指令可以构成发布授权，但当前记录没有把它闭合为“release 泳道独立授权”或“新 stage + 新 freeze/start”；蓝图与发布状态直接矛盾。

### B4（P1，阻断验收）当前治理记录仍漂移，`check 0/0` 抓不到

| 文件 | 现状 | 问题 |
|---|---|---|
| `aecw/criteria.md:4` | 最后核对 2026-11-05 | 1.3.1 已发布，矩阵未复核 |
| `aecw/criteria.md:23` | `G4-RELEASE` 只写 v1.3.0 | 没有 1.3.1 release 判据 |
| `aecw/criteria.md:29` | `WP-5` 证据 169/169 | 当前产品 174/174 |
| `aecw/ledger.md:3` | 最后核对 2026-11-05 | F-057 仍引用旧 release gate `0700071129` 与旧 attestation `...065956`；当前 final 是 `0711355f20` / `...071124` |
| `aecw/cluster/board.md:4` | 当前阶段写 `grow-2` | 实际 `security-1` 已 closed |
| `aecw/cluster/board.md:47` | release 泳道写 v1.3.0 | 实际 1.3.1 已发布 |
| `aecw/cluster/board.md:54` | “本阶段前置…蓝图 v2” | 当前蓝图 v3 |
| `aecw/cluster/release.md:19` | 发布门链接 `0700071129` | 该门已 superseded；final 是 `0711355f20` |
| `aecw/human/acceptance.md:3` | 最后核对 2026-11-05 | 无 1.3.1/security-1 验收 |
| `aecw/human/decisions.md:3` | 最后核对 2026-11-05 | 已有 2026-11-06 决策 |

`check` 的“当前文档关键词一致性”没有比较这些语义值，所以 0/0 不代表当前记录一致。S5 证据也自认“只保证机器块，不保证散文自动生成”；这次验收正是被散文漂移卡住。

## 4. 非阻断但必须披露

1. **独立 reviewer 未进入最终 attestation**：`VA-20261106071124-fd647e.json` 的 `reviewer.name` 是 `meo1102`；release 证据却写独立 reviewer `release-review-1.3.1`。S5 的独立复核结论没有绑定到最终 verify/gate。
2. **发布后条件未进入最终 gate**：浏览器设置页保存、307、自定义 routePath、live 限速、G1-P95、WP-4-RELOAD、SEC-E2E、ED-003/004 只在证据/旧 gate 里；final gate 空正文没有携带条件和到期。
3. **1.3.1 未推送远程**：release 证据自述 `git push` 因无 GitHub 凭证失败；`state.remote.last_pushed_tag` 仍是布局 v3。发布是本地发布，不是远程同步。
4. **S4 未验项**：真实浏览器 CSRF 保存、307 跨源、routePath live、live 限速仍未真机；这些可以 waived，但必须由当前 gate 明确承接，而不是空表。
5. **L 模式限制**：没有密码学签名、没有抗伪造身份；这是已披露的 local-trusted 限制。但 B1 的“任意 JSON 通过 gate”不是 L 模式可接受的合理降级。

## 5. 复验条件（建议按此退回补证）

### P0（不清不得称“整改完成”）

1. **让 gate 内容可核验**：`gate` 必须要求/生成关键事实、主张 vs 事实、负事实、决策理由、剩余风险与条件；空模板、全 `__`、全 `-` 由 `check` 或 `gate` 拒绝。final release gate 用当前 attestation 重出并填实。
2. **绑定 attestation 来源**：至少校验 `id` 与文件名一致、`checks` 日志存在且哈希匹配、`reviewer`/session 记录、attestation 文件自身哈希写入 gate；通过类门禁拒绝“项目根下的任意 JSON”。若不做密码学签名，明确写“L 模式仅防误用，不抗伪造”，不能宣称“唯一通过类证据”已经足够。
3. **闭合人类记录**：补 `human/acceptance.md` 的 1.3.1/security-1 验收；补 `decisions.md` 的发布/例外授权；CR-007 填影响分析、裁决正文、人类裁决人；说明 1.3.1 是 release 泳道独立授权，还是应新 stage + 新 freeze/start。
4. **把发布条件写入 final gate**：浏览器保存、307、routePath、限速、G1-P95、WP-4-RELOAD、SEC-E2E、ED-003/004，写清到期与接受者。

### P1（同轮修完）

5. 更新 `criteria.md`：加 1.3.1 release 判据；`WP-5` 改 174；复核全部 `met/waived/deferred`。
6. 更新 `ledger.md`：F-057 改为 final gate/attestation；记录本轮审计发现；最后核对改 2026-11-06。
7. 更新 `cluster/board.md`：当前阶段 `security-1/closed`；release 泳道 1.3.1；去掉蓝图 v2 旧话。
8. 更新 `cluster/release.md`：链接 final gate，不链接 superseded。
9. `human/acceptance.md`、`human/decisions.md` 最后核对改 2026-11-06。
10. 由 `release-review-1.3.1` 或新的新鲜上下文对最终树再做一次 reviewer，并把 reviewer/session/结论写入最终 attestation 或独立 review 记录；不要只用 owner 的 verify 作为“独立”。

### P2（不阻断，但披露）

11. 推送 `main` 与 `v1.3.1` 到远程；未推送前不要写“远程发布完成”。
12. 发布后条件到期复核；未完成不得称“条件已闭”。

## 6. 不得宣称

- 不得说“红队整改全部完成/验收通过”；
- 不得说“最终 release gate 已有条件通过”（它是空表）；
- 不得说“verify 是不可伪造的唯一通过证据”；
- 不得说“1.3.1 已远程发布”；
- 不得说“浏览器 CSRF 端到端已验”；
- 不得说“adoption/EV-001 分布外已完成”。

## 7. 建议结论

- **技术层：通过。** S1–S3 的 fail-closed/锁/冻结、S4 的服务端 guard/probe、S5 的结构校验都有可复现证据；产品 174/174、probe 7/7。
- **治理层：不通过，退回补证。** 问题不是“再写更多文档”，而是：
  1. gate 仍是空模板；
  2. attestation 仍是可伪造的字段文件；
  3. 发布范围/人类验收/当前记录没有闭合。
- **1.3.1：保持有条件发布。** 不建议因文档问题回滚产品；但 release gate 必须重出并填实，才能把“有条件通过”变成可审计的结论。

## 8. 审计证据位置

- 最终 release gate：`aecw/gates/2026-11-06-release-v1-3-1-final-0711355f20.md`
- 被取代的完整 gate：`aecw/gates/2026-11-06-release-v1-3-1-0700071129.md`
- 最终 attestation：`aecw/workspace/evidence/attestations/VA-20261106071124-fd647e.json`
- 空门模板：`aecw/core/gate.template.md`
- `gate`/`readAttestation`：`aecw/bin/aecw.mjs:372`、`:1060`
- 蓝图非目标：`aecw/BLUEPRINT.md:49`
- 当前漂移：`aecw/criteria.md`、`aecw/ledger.md`、`aecw/cluster/board.md`、`aecw/cluster/release.md`、`aecw/human/acceptance.md`
- 临时副本负控：`D:\DSH\.audit-forge`（审计后已删除；输出见本报告 §3 B1）
