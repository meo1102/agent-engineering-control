# PLAN v0.9.1：红队整改

> 依据：[`aecw-redteam-report.md`](../task-complete-toast-aecw/aecw-redteam-report.md)（按要求未点报告中的链接；只读正文与当前仓库）。
> 报告快照：HEAD `0550b37`；当前：HEAD `a71f87f`，布局 v3（产品代码在仓库根），AECW CLI `0.9.2`。
> 当前实测：`check` **FAIL 0｜WARN 0**、`probe` **7/7**、tests **169/169**、`node --check` **17/17**。
> 结论：**报告的核心判断成立**——当前更像“诚实的单 agent 开发记录 + checklist 原型”，还不是“可约束不完全可信 agent 的强制治理系统”。`check` 0/0 不能推翻这一点。

---

## 0. 先定威胁模型：不要用一个系统同时假装两种东西

报告最有价值的地方，不是列了 11 个问题，而是逼出一个选择：

| 模式 | 适用 | AECW 是什么 | 不承诺什么 |
|---|---|---|---|
| **L：local-trusted** | 单 agent、人类在场、低风险、本机自用 | 记录 + 检查单 + 可追溯证据 | 不承诺抵抗恶意 agent、不承诺批准不可伪造、不承诺并发强一致 |
| **E：enforced** | 多 agent、不完全可信执行者、高风险发布 | 强制边界：fail-closed verify、签名批准、原子存储 | 不承诺“零成本”；需要额外的身份/存储/运维 |

**当前项目应明确标为 L**，并在 `PROJECT.json` 写 `threat_model: "local-trusted"`。  
这不是自我贬低，而是停止过度承诺；要升级到 E，再按 §3 的 P0 做，不要用 L 的记录去冒充 E 的保证。

> 报告说“不能视为可靠的三柱治理系统”，准确。当前应先修**确定性、可执行、低成本的硬边界**，而不是先加角色或写更多文档。

---

## 1. 报告 vs 当前现状：哪些仍成立

> 报告写于布局 v2；当前布局 v3 已取消 `product/` 层，部分路径/哈希/坏链结论已过时。以下按“当前代码是否仍存在该问题”判断。

| 报告项 | 当前判断 | 说明 |
|---|---|---|
| RT-01 批准可自报/代写 | **仍成立** | `start --by` 只查非空、省略时填 owner；`accept`/`resolve`/`log` 无身份校验；`change --decision` 可直接接受 charter。 |
| RT-02 gate/release fail-open | **仍成立** | `gate` 仍可写“通过”并 exit 0；`check` 对开放 S1/S2 仍是 WARN，不是 FAIL；没有统一 release 命令。 |
| RT-03 closed 可重开/冻结可替换 | **仍成立** | `start` 只拒绝 executing；freeze 不保存 payload 哈希；同名门禁仍可覆盖。 |
| RT-04 台账并发丢写/重号 | **仍成立** | `fact` 等仍是读全文件→改字符串→覆盖写；无锁/CAS/原子 rename。 |
| RT-05 状态源与 checker 脱节 | **部分改善，仍成立** | 新增 `state.layout/install/remote` 与 check 对账；但 `freeze/start` 仍只改 `STATUS`，不改 `state.stage`；`init` 仍未生成 PROJECT/state/criteria。 |
| RT-06 探针假 PASS/写路由无防护 | **仍成立** | HTTP 两项仍只看状态码；settings 路由仍无认证/Origin/Content-Type/空 patch 防护；EV-001 仍 active。 |
| RT-07 哈希口径/坏链 | **部分改善** | 工具哈希已做 LF 归一化；当前 check 0/0，报告中的 6 条外链已不阻塞；但 `.gitattributes` 仍缺，产品发布哈希仍混用 LF/CRLF（尤其 `client.js`）。 |
| RT-08 验收/SLA/证据债不闭环 | **仍成立** | WP-4 仍整体 `met`（刷新/重启读取未单独证）；G1 P95 无样本；ED-003/004 到期不会自动阻断。 |
| RT-09 当前状态手抄漂移 | **部分改善，仍成立** | v0.9 修了 13 处；但 `g4-charter-impact`、`workspace/work/README`、`history-mapping`、`appearance-settings-design`、`board` 截图状态仍有旧话。 |
| RT-10 Markdown/ID 注入、半事务 | **仍成立** | 表格未转义 `|`/换行；`resolve`/`change --id` 不限定表类型；多文件写无 journal。 |
| RT-11 健壮性 | **仍成立** | demo 删除、枚举/占位符校验、路径/异常处理仍弱。 |

**已过时/需按当前重验的**：报告中的 `product/` 路径、`check FAIL 7`、6 条坏链、工具哈希假漂移。  
**不能因这些过时点否定其余结论**：核心治理漏洞仍在当前代码里。

---

## 2. 整改原则

1. **先 fail-closed 的硬边界，后文档/角色。** 不再用“更多文档/更多角色”补偿执行器缺陷。
2. **一个入口 `verify`，不要让 README/AGENTS/manifest 各维护一套命令。**
3. **状态机优先于散文。** 阶段、批准、冻结、发布必须是可校验字段/哈希，不是一句“已确认”。
4. **确定性检查优先。** F/DR/CR 引用、文件存在、路径包含、枚举、哈希、命令执行，都是可以机器判定的，先做这些。
5. **单 agent 也能受益。** 不要求先上多 agent；先把“agent 自己写自己通过”堵住。
6. **不为 L 模式过度建设 PKI。** 当前先做 L 的 fail-closed；E 模式再引入签名/多 reviewer/强一致存储。

---

## 3. P0：在宣称下一次治理门/发布可靠之前完成

### P0-1 立刻停止“check 绿灯 = 治理可靠”的误读

**动作**：

- `check` 输出明确写：`结构/一致性检查；不是授权/发布证明`；
- 开放 S1/S2 从 `WARN` 改为 **FAIL**（大小写 `OPEN/Open/open` 统一）；
- `gate --decision 通过|有条件通过` 在开放 S1/S2、无 verify attestation、无人类签署时**拒绝生成**；只能生成“退回补证/暂停”；
- `gate`/`release` 只消费 `verify` 的成功 attestation，不接受自由文本 `--decision` 放行；
- `init` 必须生成 `PROJECT.json`、`state.json`、`criteria.md` 和状态头，保证 `init → check` 为 0/0（或明确 `--legacy` 并 FAIL 提示）。

**验收**：

- 开放 S1 + `gate --decision 通过` → 非零退出，且不生成“通过”门禁；
- `init` 新项目 → `check` 0/0；
- 当前 `check` 0/0 的说明文字不再暗示治理保证。

### P0-2 建立唯一 `verify-release`

**动作**：新增 `aecw verify`（或 `scripts/verify.mjs`），内部编排：

1. `check --strict`；
2. `probe`；
3. 从 `PROJECT.json.commands.test` 执行完整测试；
4. `criteria.md`：无 `failed/not-started`；`deferred/waived` 有人类裁决、到期、影响门；
5. 开放 S1/S2 = 0；
6. 证据债按 `impact` 分类（release/adoption/evolution），只阻塞对应门；
7. 记录开工树/发布树 hash、测试输出 hash、probe 结果、reviewer；
8. 写 `workspace/evidence/attestations/<id>.json`。

`gate`/`release` 只引用 attestation；attestation 失败/过期/树不一致 → 拒绝。

**验收**：任一项失败 → 非零退出；伪造 `--decision 通过` 不能生成发布门。

### P0-3 修阶段状态机与冻结 payload

**动作**：

- 明确 `seed → frozen → executing → closed`；`closed` 默认终态；`paused` 只能从 executing 进入；
- `start` 只能从 `frozen` 进入，不能从 `closed` 直接 start；
- 新阶段必须有新 stage id + 新 freeze；不能复用历史 freeze；
- `freeze` 写入 canonical hash：direction、blueprint、criteria、product tree（或至少关键文件集）；
- `start` 重算并比对；蓝图/判据任一字节变化 → FAIL；
- gate 文件名含唯一 ID，历史门禁禁止覆盖；`--force` 只能显式用于 demo/迁移。

**验收**：报告 §7 的 closed 重开、蓝图替换、同名覆盖、冻结后追加范围 → 全部拒绝。

### P0-4 共享台账原子化

**动作**（零依赖可行）：

- 采用 lockfile（`open(..., 'wx')` + 超时/重试）或 CAS；写临时文件 + `rename` 原子替换；
- ID 分配在锁内完成，按表类型前缀（F/DR/CR）分配；
- 多文件写（ledger + inbox）用 journal：先写 journal/临时文件，再提交；失败回滚或至少留下明确“未提交”标记；
- `fact`/`dissent`/`change`/`resolve` 全部走同一存储层；
- 32 路并发回归：成功记录数 = 持久化数；无重复 ID、无截断、无“成功但丢失”。

**验收**：报告 §7 并发测试；连续 10 轮 32 路无失败。

### P0-5 批准绑定 payload，禁止自签

**动作（L 模式最小版）**：

- `start --by` 必须等于 `state.owner` 或显式 allowlist；省略不再自动填 owner；
- `accept`/`resolve`/`log` 的 `--by` 必须是具名人类；agent 不得作为接受者；
- `change --decision 接受` 不能在同一条命令里接受 charter；charter 变更只能由人类在单独步骤确认；
- `freeze/start/gate` 的批准内容写入 `payload_hash`：project、stage、blueprint version/hash、criteria version/hash、product tree hash、waiver、到期、时间戳；
- **E 模式**再加人类持有密钥的签名（SSH/GPG/OS credential），agent 无法代替签名；
- L 模式明确记录“批准是记录，不是抗恶意证明”，不宣称抗伪造。

**验收**：非 owner `start`、agent 自批准 charter、agent 代写人类验收 → 拒绝；payload hash 不一致 → 拒绝。

### P0-6 收口探针与设置写路由

**动作**：

- 新增只读 health/dry-run 端点，返回 `{plugin, version, instance, capabilities}`；probe 校验服务身份、版本、实例、URL canonical（拒绝 query/fragment/跨源重定向）；
- 停止用“任意 400/422”证明路由健康；不再向写端点 POST 探测 body；
- settings 路由增加：认证/CSRF/Origin/Host allowlist、`application/json`、非空 patch、速率限制；
- 在克隆 profile 做恶意 Origin/text/plain/空 patch/跨源测试；
- **EV-001 先降级为 trial 或 suspended**：报告已复现 false PASS，按它自己的中止条件处理；修复后再激活。

**验收**：无关 400 假服务、自定义 routePath、307、恶意 Origin、空 patch → 不得 PASS；写请求必须被拒绝。

**注意**：这属于产品行为/安全变更，需要新蓝图 + freeze/start，不能走 maintenance 直接改。

### P0-7 Markdown/ID 类型安全

**动作**：

- 所有写入表格的字段转义 `|`、CR/LF、控制字符；拒绝或替换；
- `resolve` 只能操作 DR；`change --id` 只能操作 CR；`accept` 只能写 acceptance；按 section 限定类型；
- `nextId` 只扫描对应表的 ID 列，不扫自由文本；
- `gate name` 白名单/长度/换行拒绝；
- 多文件写 journal/回滚；
- `accept --by` 必填具名人类。

**验收**：报告 §7 的列注入、换行注入、DR/CR 跨类型、伪 F ID、inbox 半写 → 全部拒绝或可检测。

---

## 4. P1：恢复证据可信度与最小独立制衡

1. **真正的 SSOT**：`freeze/start/gate` 先写 `state.json`，`STATUS` 由它生成；禁止手改 STATUS 当前字段；`board/release/manifest` 当前值由 state 渲染。
2. **引用校验**：F/DR/CR 必须存在；`release.gate` 必须存在；`deferred/waived` 必须有真实人类决定/到期/影响；`commands` 必须存在且可执行；roots/install 不得逃逸项目根。
3. **统一字节口径**：加 `.gitattributes` 固定 EOL；发布哈希从 tag 的 Git blob（LF）生成；重发产品哈希，修 `client.js` 的 CRLF/LF 混用。
4. **独立 reviewer**：每次高风险发布至少一个新鲜上下文的非作者 reviewer；记录 session id、输入 hash、发现、结论。一个真 reviewer 比五个兼任角色有效。
5. **判据修正**：WP-4 补刷新/重启读取；G1 P95 无样本就标未验；G2 范围变化补 CR/新 freeze；release/adoption/evolution 债按 impact 分离。
6. **清理 current 漂移**：`g4-charter-impact`、`workspace/work/README`、`history-mapping`、`appearance-settings-design`、`board` 截图状态；历史方案标 historical，不手抄版本。

---

## 5. P2：降低长期维护成本

- SLA/有效回合/人类分钟/连续失败/waiver expiry 变成结构化字段 + 自动提醒/阻断；
- 统一输入 schema、Markdown 转义、异常处理；
- demo 移出生产 CLI；`demo --force` 才允许删除；
- 删除重复的当前状态手抄，只留生成视图 + 历史证据；
- 把 `verify` 作为唯一入口，README/AGENTS 只引用它。

---

## 6. 建议顺序（不要一次全做）

| 阶段 | 内容 | 相对工作量 | 是否改产品 |
|---|---|---|---|
| **S1** | P0-1（open S1 FAIL、gate 拒绝、init green、check 声明）+ P0-7（转义/ID/半事务） | 小 | 否 |
| **S2** | P0-2（verify）+ P0-3（状态机/freeze hash） | 中 | 否 |
| **S3** | P0-4（原子台账 + 32 路回归） | 中 | 否 |
| **S4** | P0-6（探针/写路由安全） | 中—大 | **是**，需新 stage |
| **S5** | P1（SSOT/引用/字节/独立 reviewer/判据修正） | 中 | 部分 |

**门**：S1–S3 未过，不开新功能阶段；S4 必须新蓝图 + freeze/start；S5 完成前不宣称“治理可靠/全部通过”。

---

## 7. 整改后的红队回归（最小集）

1. 非 owner `start`、agent 自批准 charter、agent 代写验收 → 拒绝；
2. closed 无新 freeze 重开、冻结后蓝图改一字节、同名历史覆盖 → 拒绝；
3. 开放 S1/S2、空授权门、伪 F 引用、缺失 release.gate、全 `-` deferred、空 commands、路径逃逸 → FAIL 且非零退出；
4. 列/换行注入、DR/CR 跨类型、伪 F ID、inbox 半写 → 不得伪造状态；
5. 32 路并发写：成功全持久化、无重号/丢写/截断；
6. 干净 Windows/Linux checkout 同一 tree 同一哈希/同一 check；
7. 假 400 服务、默认路由冒充、自定义 routePath、query/fragment/307 → 不得 probe PASS；恶意 Origin/无凭证/text/plain/空 patch 写 → 拒绝；
8. `init` 生成项目演进到 check PASS；所有生成器输出能过自己的检查；
9. WP-4 刷新/重启读取有证据；G1 P95 有样本或保持未验。

---

## 8. 不做什么

- **不新增四个常设角色**；问题不是“没人负责”，是“执行器不 fail-closed”。
- **不为 L 模式强上 PKI**；L 先做记录 + fail-closed，E 再签名。
- **不因为报告就回滚 v1.3.0 产品**；报告否定的是治理保证，不是全部产品功能；但应停止“治理可靠”的宣传。
- **不把“更多文档/更多 agent”当修复**；多 agent 只会放大并发与身份问题。
- **不一次性重写 CLI**；先做 P0-1/P0-7 小修，再 verify/state machine，再存储。
- **不覆盖历史证据**；旧门禁/证据保留，新增整改证据和 superseded 标记。

---

## 9. 一句话建议

> **先把 AECW 从“会写文档的 checklist”修成“会拒绝的 verify”，再谈多 agent 和治理规模。**  
> 当前项目应先标 `local-trusted`，完成 P0-1/2/3/4/7；产品安全 P0-6 另开 stage；在 `verify-release` 通过前，不再宣称“门禁/发布可靠”。
