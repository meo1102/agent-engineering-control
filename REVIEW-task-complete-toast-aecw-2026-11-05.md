# 真实项目校准 · task-complete-toast-aecw（2026-11-05）

> 对象：`D:\DSH\task-complete-toast-aecw`（本文写于布局 v2：产品 `product/` + 治理 `aecw/`，独立 Git 仓库）。
> 方法：只读核对当前文件、运行 `check` 与 EV-001 探针，不修改产品代码、验收与人类决策。
> 证据快照：2026-11-05；行号以本快照为准，后续文件变化后按内容检索，不要按行号硬引用。
> **布局补记（2026-11-06）**：项目已改为布局 v3，取消 `product/` 层，产品代码回到仓库根；本文中 `product/` 路径是历史快照。当前布局以 [`PLAN-v0.9`](PLAN-v0.9-真实项目校准.md) §3.1 与项目 `PROJECT.json` 为准。
> 结论：**AECW 的三域/门禁/验收/基线/进化链是有效的；但“单一 STATUS”只解决了“以哪页为准”，没有解决“这页是否真实”。**

---

## 0. 一句话结论

这次实践真正暴露的不是“agent 会不会写代码”，而是：

> **结构检查全绿、运行探针全绿，当前状态文档仍然可以互相矛盾。**

`task-complete-toast-aecw` 的 `check` 是 `FAIL 0｜WARN 0`，EV-001 探针是 `7/7 PASS`；与此同时，`STATUS.md`、`product/README.md`、`cluster/board.md`、`human/decisions.md`、`cluster/learning.md`、`ev-001-runtime-probe.md` 里仍有“未确认/未安装/未激活/待真机/待人类”的旧话。  
这不是“文档写得不够多”，而是**状态只存在于散文里，没有可校验的记录**。

---

## 1. 实践底稿

### 1.1 这次实际发生了什么

| 项 | 结果 |
|---|---|
| 项目 | 从 `DSH_end/插件/task-complete-toast` 复制，按 prototype 三域改造，后迁为独立仓库 |
| 布局 | 产品 `product/`；治理 `aecw/`；profile link/junction → `...\product` |
| 功能 | G1/G2/G3 继承；新增 G4 外观设置 + 实时预览；修复 G2 遮挡时无 Windows 通知 |
| 测试 | 169/169；`node --check` 17/17 |
| 人类验收 | G4 设置页效果接受（E2，无截图）；G2 遮挡推送真机通过（E2，无截图） |
| 阶段 | `grow-2` **closed**（有条件通过）；基线 commit `4aff41a` / tag `aecw-grow-2-2026-11-05`（历史仓库） |
| 独立仓库 | initial `67809d0`；布局 v2 tag `aecw-layout-v2-2026-11-05` @ `4589b91` |
| 进化 | EV-001 运行态探针：trial 正控 7/7、负控 fail → 人类激活 |
| 结构检查 | `node aecw/bin/aecw.mjs check aecw` → **FAIL 0｜WARN 0** |
| 运行探针 | `node aecw/scripts/probe.mjs` → **7/7 PASS** |
| 仍未闭合 | 截图零；G2-8/G3-4b 接受为遗留；13 项 V + V01/V04/V23 未裁决；G4 未发布；adoption 门禁待人类签署；EV-001 分布外/回滚演练未做 |

### 1.2 关键运行事实

```text
检查：D:\DSH\task-complete-toast-aecw\aecw
  OK   必需文件/目录齐全
  OK   人类所有者：meo1102
  OK   无开放 S1/S2
  OK   无开放变更
  OK   STATUS.md 更新于 0.0 天前
  OK   阶段基线已冻结（charter-freeze）
  OK   蓝图已批准：v2（meo1102）
  OK   阶段状态为 closed（保留开工令历史）
结果：FAIL 0｜WARN 0
```

```text
PASS  宿主 package.json — @local/task-complete-toast@1.2.0 (...\product)
PASS  profile dependency link — link:D:/DSH/task-complete-toast-aecw/product
PASS  profile bundles — @local/task-complete-toast
PASS  junction target — D:\DSH\task-complete-toast-aecw\product
PASS  profile patch config — task-complete-toast + appearance
PASS  HTTP outcome route (expect 400) — 400
PASS  HTTP settings route (expect 400/422, no write) — 400

AECW EV-001 probe: 7/7 passed
```

> 这两段绿色很关键：它们证明“结构/安装/路由”是通的，但**不能证明当前文档的说法一致**。

---

## 2. 有效的部分：哪些机制真的接住了问题

1. **三域责任结构有效。** 人类方向、集群实现/学习、工作区证据/记忆/落地，在真实功能演进和缺陷修复中没有被角色混乱吞掉。
2. **门禁抓住了真机问题。** G2 遮挡不是单测发现的，是人类真机目视 → S2/DR-002 → `G2-blocked` → 修复 → `G2-resolved`。这是 AECW 最有效的路径。
3. **`freeze`/`start` 分离有效。** 蓝图 v2 批准、冻结、开工令、阶段关闭，形成了可追溯的授权链；阶段结束真的停住了。
4. **基线冻结 + tag + 哈希有效。** 迁移、目录搬动、profile 重装后还能对照基线；EV-001 探针在迁移后立刻抓到了路径/安装问题。
5. **人类验收 + E2 纪律有效。** 没有把“人类口述”写成 E1；零截图被反复标为证据缺口，没有宣称“全部通过”。
6. **进化试验的六项结构有效。** 假设/证据/影响/评估/回滚/可证伪，正控 7/7 + 负控 fail，足以支持“trial → active”的人类裁决。
7. **adoption 门禁把“结构完成”与“功能完成”分开了。** 这是一个正确的区分，虽然后来没有及时签署（见 §3.10）。
8. **所有者按 Git 提交人记录有效。** `meo1102` 解决了“未具名所有者”对 freeze/发布声明的阻断。
9. **产品/治理物理分离方向正确。** 经历“根目录混放 → 独立目录 → product/aecw 分层”两次修正后，边界终于清楚；这应成为默认部署形态，而不是事后补救。

---

## 3. 疏漏：哪些地方没有接住

### 3.1 当前状态页自身失真

`STATUS.md` 是“唯一当前状态”，但同一文件内已经有两处互斥：

| 位置 | 旧话 | 同一文件/同一事实 |
|---|---|---|
| `aecw/STATUS.md:37` | “客户端 UI 未确认……需刷新后人工复测” | `aecw/STATUS.md:42` 已写“G4 设置页：人类目视后验收”；`gates/2026-11-05-grow-2.md` 也写已接受 |
| `aecw/STATUS.md:94` | “进化台账（EV-001 trial）” | `aecw/STATUS.md:111` “EV-001 已激活”；`cluster/evolution.md` 状态 active |

这不是“少更新一行”，而是**同一页的不同小节各自维护、没有生成关系**。  
`STATUS` 一旦要靠人记住“§2.1 要跟 §2.2 一起改、§5 要跟 §6 一起改”，它就已经不是单一状态，而是多份手写摘要。

### 3.2 产品 README 与 STATUS 互相打架

`product/README.md` 是“当前摘要”，但多处仍是旧状态：

| 位置 | 旧话 | 与当前事实冲突 |
|---|---|---|
| `product/README.md:60` | “G4 外观设置（grow-2，代码完成、真机未验）” | `:8`/`:17` 写“G4 已由人类验收”；`STATUS:42` 同 |
| `product/README.md:65` | “本副本未安装” | `:7` 写 profile link/junction 指向 `...\product`；探针 7/7 |
| `product/README.md:132` | “配置面板不支持” | G4 已提供 `settings.plugins.tab` 设置页；`:133` 自己写了设置页入口 |
| `product/README.md:133` | “G2 遮挡推送修复待真机” | `:129` 写“2026-11-05 真机通过”；`STATUS:43` 同 |
| `product/README.md:139-158` | 目录树仍是“仓库根混放”，`STATUS.md` 在根 | 实际是 `product/` + `aecw/`；当前树应看根 `README.md` |

**根因**：`product/README.md` 被当作“产品说明 + 当前状态摘要 + 历史”三种东西；一句“以 STATUS 为准”不能阻止它继续写旧事实。  
**教训**：指针不是同步；**指向 STATUS 的文档仍然可以撒谎**。

### 3.3 任务板/决策/学习账/进化提案各有一份“当前”

| 文件 | 旧状态 | 当前事实 |
|---|---|---|
| `aecw/cluster/board.md:3` | “当前阶段：grow-2（已冻结/已开工）” | `STATUS:13-14` 阶段 `closed` |
| `aecw/cluster/board.md:11` | T-003 “done（tab 已注册；UI 待确认）” | G4 设置页已人类验收（F-040） |
| `aecw/cluster/board.md:12` | T-004 “done（未真机）” | G4 预览随设置页一起验收（E2） |
| `aecw/cluster/board.md:28` | B-004 “grow-2 WP-5 会补截图” | 阶段已关闭，截图仍为零；WP-5 没有补 |
| `aecw/human/decisions.md:26-32` | “待人类（阶段门禁时，不阻塞开工）”仍列阶段验收/截图 | 阶段已关闭，G4 已接受；该表未关闭 |
| `aecw/cluster/learning.md:23` | EV-001 “试用通过（trial）” | `cluster/evolution.md` 已 active |
| `aecw/workspace/memory/ev-001-runtime-probe.md:1` | 标题“已激活” | `:77` “未激活”；`:57` 仍是旧路径 |
| `aecw/workspace/memory/README.md:16` | EV-001 “trial（试用通过，未激活）” | 已 active |

**根因**：这些文件都在“当前”目录里，却没有 `current/historical` 状态头；读者无法一眼判断该信哪一行。  
**教训**：**目录位置不等于时效**；必须有显式文档状态。

### 3.4 验收判据没有逐项闭环

蓝图 v2 的 WP-5 写“至少一张设置页 + 一张预览效果的真机截图”，阶段验收也写“WP-5 有测试与真机截图”（`aecw/BLUEPRINT.md:38,74`）。  
实际：

- `gates/2026-11-05-grow-2.md:34` 明确“真机截图/录屏仍为零”；
- `gates/2026-11-05-grow-2.md:43` 仍给“有条件通过”；
- `cluster/board.md:14` T-006 写“done（阶段关闭）”，同一行承认“截图仍为零”；
- `human/acceptance.md:12` 接受 G4，但只接受“设置页效果”，没有逐项接受“无截图”这个偏差。

这不是说不能有条件通过；而是**条件没有被写成可核对的裁决**：谁接受、接受哪一条、到什么日期、影响哪个发布门。  
**教训**：`有条件通过` 不能是万能出口；每个未满足的判据要有 `waived/deferred` + 人类签署 + 证据缺口登记。

### 3.5 发布/验收/激活/采纳四种状态混在一起

当前至少四种不同状态被同一套“已通过/已验证/已接受”词汇混用：

| 对象 | 真实状态 | 文档里常见的说法 |
|---|---|---|
| G4 设置页 | 人类验收接受（E2，无截图），**未发布** | “已验收”“可用”“未发布”混用 |
| 产品 v1.2.0 | 已发布（tag `v1.2.0`，旧基线） | 与 G4 的“未发布”混在一起 |
| EV-001 | **active**（人类激活，写入 AGENTS） | “trial”“已激活”“未激活”并存 |
| AECW 结构迁移 | **adoption 门禁待人类签署** | “已迁移”“已使用”“已通过”混用 |

**教训**：需要显式状态机：`draft → candidate → accepted → released → active/retired`，并且 **feature / release / evolution / adoption 各自一条**，不能用一个“通过”概括。

### 3.6 布局迁移后命令/路径没有单一来源

布局 v2 后，至少三种写法同时存在：

- 根 `README.md`：`node aecw/bin/aecw.mjs check aecw`（正确）
- `aecw/AGENTS.md`：`node bin/aecw.mjs check .`（在 `aecw/` 内正确）
- `aecw/workspace/evidence/2026-11-05-development-retrospective.md:126`：`node bin/aecw.mjs check .`（从仓库根执行会失败）
- 同文件 `:127`：`node scripts/probe.mjs`（从仓库根应为 `node aecw/scripts/probe.mjs`）
- 同文件 `:233`：多出一个未闭合的代码围栏
- `product/README.md:139-158`：目录树仍是布局 v1

**根因**：没有项目清单（manifest）统一定义 `product_root` / `governance_root` / `check` / `probe` / `test`；每个文档自己抄命令。  
**教训**：布局一变，所有手抄命令都会漂移；**路径和命令必须有单一来源**。

### 3.7 入口与通道没有被当作验收对象

设置页“找不到”是这次最典型的 UX 缺口：

- `settings.plugins.tab` slot 已注册（F-039，E1），但人类在侧边栏“插件”页的插件卡片里找不到设置项；
- 正确入口是 **设置 → 插件 → 任务完成提示设置**；
- 修复主要靠“告诉用户入口 + 加错误边界/诊断”，而不是把“人类能自己找到”写成验收判据。

同类问题还有 G2：

- 原逻辑“已进入会话 → dismiss”，把**浮层卡片**和**系统通知**一起抑制；
- 人类场景是“授权出现后切到别的应用，DSH 被遮挡”，于是系统通知也没了；
- 修复后区分“卡片隐藏”与“页面不可见时仍发系统通知”。

**教训**：
- **注册成功 ≠ 人类找得到**；入口、标签、回退路径是验收对象。
- **抑制一个通道 ≠ 抑制所有通道**；需要“上下文 × 通道”矩阵（同会话可见/同会话隐藏/其他会话/最小化/后台）。

### 3.8 阶段关闭后仍在工作，但没有阶段外泳道

`grow-2` 在 16:05 关闭；之后又做了：

- EV-001 试用/激活；
- 独立目录迁移 + 独立 Git 仓库；
- 产品/AECW 分层；
- 全量复盘；
- `gates/2026-11-05-adoption.md` 仍未签。

这些工作都记在 `cluster/board.md` 的“阶段外”或 `cluster/runs.md`，但没有正式的**维护/迁移/进化泳道**：授权、预算、停止条件、证据要求都没有单独定义。  
**结果**：`STATUS` 说“阶段 closed”，但项目仍在持续改动；读者无法判断哪些改动受哪个授权约束。  
**教训**：**“阶段关闭”只关闭阶段，不关闭项目**；阶段外工作必须有泳道，不能靠“人类口头说了”悬空。

### 3.9 证据债没有账

零截图不是新问题，但它一直没有“账”：

- `STATUS` 说“零截图”；
- `gates/grow-2` 说“零截图”；
- `human/acceptance` 说“无截图”；
- `BLUEPRINT` 要求截图；
- 没有任何一张“证据债”表写：谁欠、欠哪一项、影响哪个门、何时补、谁接受不补。

**教训**：证据缺口不是一句“零截图”就能关闭；它需要**证据债台账**，并在发布门前逐项裁决。

### 3.10 adoption 未签，但结构已经在用

`gates/2026-11-05-adoption.md` 的人类签署仍是“待确认”（`:55`）；`human/acceptance.md:14` 也写“待人类验收”。  
但项目已经按 AECW 结构运行、迁移、发布阶段门禁、激活 EV-001。  
**教训**：治理结构本身也需要“采纳”状态；未签但已在用，应标为 **provisional adoption**（临时采纳，具名、有到期/补签条件），而不是假装已签或假装没发生。

### 3.11 `check` 的绿色太容易

当前 `check` 只查：

- 必需文件/目录；
- 所有者具名；
- 开放 S1/S2；
- STATUS 新鲜度；
- freeze/start/blueprint 状态。

它**不查**：

- 当前文档是否互相矛盾；
- 蓝图判据是否有逐项证据；
- 文档中的命令/路径是否存在；
- Markdown 围栏/链接是否完整；
- 历史文档是否标 `HISTORICAL/SUPERSEDED`；
- adoption/release/evolution 状态是否一致；
- 产品根/安装目标是否与 manifest 一致；
- 当前状态是否与 git HEAD/tag 对齐。

所以 `FAIL 0｜WARN 0` 是**结构绿灯**，不是**事实绿灯**。这次实践把这个区别演示得非常清楚。

---

## 4. 根因：不是“文档不够多”，是“状态没有模型”

把上面现象归并，只有五个根因：

1. **状态是散文，不是记录。** `STATUS`、README、board、decisions、learning 各写一份“当前”，没有生成关系；人一忙就漂移。
2. **验收是自由文本，不是矩阵。** 判据、证据、豁免、剩余风险没有一一对应；`有条件通过` 可以覆盖任何缺口。
3. **没有项目清单，工具/数据/路径没有单一来源。** 布局一改，命令、目录树、安装说明全漂移；CLI 复制进项目，未来还会漂移。
4. **没有泳道。** 阶段、维护、进化、发布混在“阶段外”，授权与停止条件不清楚。
5. **没有通道/入口模型。** 浮层、系统通知、设置入口被当作实现细节，而不是验收对象。

---

## 5. 概念优化：从“单一 STATUS”到“单一状态，多种视图”

### 5.1 保留不变

- 人类只做方向、S1/S2、最终验收/抽样；**不新增四个常设角色**。
- 三域责任不变：人类 / 集群 / 工作区。
- `freeze`/`start` 的阶段边界不变；阶段结束停。
- E1/E2/E3 不变；E2 不得写成 E1。
- 信任优先不变：边界清晰 → 默认相信 → 例外升级 → 抽样验证。

### 5.2 核心改动

> **单一状态，不是单一文档。**  
> `STATUS.md` 是当前状态的**视图**；权威来自结构化记录（state + criteria + ledger + gates + acceptance + evolution）。

具体：

1. **一个事实只在一个地方有值。** 阶段/发布/进化/采纳/证据债写在 `state.json`；`STATUS` 由它渲染，其他文档只引用，不复制。
2. **验收判据变成矩阵。** 每条判据一行：`id / criterion / status / evidence / verifier / human decision / date`。门禁是矩阵的视图，不是自由散文。
3. **状态显式分型。** `feature`、`release`、`evolution`、`adoption` 各有状态；不再用“通过/可用/已验收”一个词覆盖。
4. **阶段外有泳道。** stage / maintenance / evolution / release 四条泳道，各有授权、范围、预算、停止、证据。
5. **入口与通道是验收对象。** 人能找到、能看到、能操作；抑制一个通道不等于抑制全部。
6. **证据债有账。** 每个缺口有 owner、due、影响门、waiver；发布门逐项结清或人类签署不补。

### 5.3 四条泳道

| 泳道 | 做什么 | 谁授权 | 产物 | 停止 |
|---|---|---|---|---|
| **stage** | 产品行为变更 | 人类 freeze/start | 蓝图、门禁、阶段基线 | 阶段末/停止条件 |
| **maintenance** | 文档纠错、路径/命令修复、迁移、非行为重构 | 人类一次性指令 or 维护授权 | 维护记录、check 通过 | 范围外即停 |
| **evolution** | 工具/流程/技能候选 | 人类 trial/active 裁决 | 六项提案、正负控、EV 台账 | false pass/成本过高 |
| **release** | 版本、tag、manifest、发布说明 | 人类发布门 | release manifest、证据债结清 | 证据债未清即停 |

**关键**：`grow-2 closed` 之后，EV-001、迁移、分层都应归入 maintenance/evolution，而不是“阶段外黑盒”。

### 5.4 状态机（最小）

```text
feature:   draft → candidate → accepted → released
evolution: candidate → trial → active → retired
adoption:  pending → provisional → accepted
release:   unreleased → release-candidate → released → superseded
```

允许 `accepted-but-unreleased`，但必须显式写；不能把“人类验收”直接说成“已发布”。

### 5.5 通道矩阵（最小）

| 上下文 | 应用内浮层 | 系统通知 | 说明 |
|---|---|---|---|
| 同会话、页面可见 | 不显示（避免遮挡授权） | 可选/不显示 | 进入会话即收起 |
| 同会话、页面隐藏/最小化 | 不显示 | **必须显示** | 这次 G2 bug 的修复点 |
| 其他会话、页面可见 | 显示 | 可选 | 不遮挡当前授权 |
| 其他会话、页面隐藏 | 显示/队列 | **必须显示** | 后台也要到达 |
| 已解决/取消 | 清除 | 关闭对应通知 | 不留过期提醒 |

**规则**：抑制浮层 ≠ 抑制系统通知；每个通道单独测，不能只测“有没有卡片”。

---

## 6. 架构优化：两个根、一个清单、一个状态源、一个矩阵

### 6.1 推荐布局

```text
<repo>/
├─ PROJECT.json              # 项目清单：两个根、安装目标、命令、工具版本
├─ README.md                 # 仓库地图（只指路）
├─ AGENTS.md                 # 仓库级入口规则（只指路）
├─ product/                  # 产品代码/可安装包
└─ aecw/                     # 治理
   ├─ STATUS.md              # 当前状态视图（由 state 渲染/校验）
   ├─ state.json             # 机器可读当前状态（唯一状态源）
   ├─ criteria.md            # 验收矩阵（判据/证据/豁免）
   ├─ BLUEPRINT.md           # 本阶段蓝图（引用 criteria）
   ├─ ledger.md              # 异议/事实/变更
   ├─ human/ cluster/ workspace/ gates/ inbox/
   ├─ bin/ core/             # 工具（外部或 vendored，带版本）
   └─ scripts/probe.mjs      # 运行态探针
```

`workspace/` 只放证据/记忆/落地，**不再放产品代码**；产品代码只在 `product/`。

### 6.2 `PROJECT.json` 示例

```json
{
  "project": "task-complete-toast-aecw",
  "roots": {
    "product": "product",
    "governance": "aecw",
    "workspace": "aecw/workspace"
  },
  "install": { "target": "product", "profile": "desktop" },
  "commands": {
    "test": "cd product && node --test --test-isolation=none test/*.test.js",
    "probe": "node aecw/scripts/probe.mjs",
    "check": "node aecw/bin/aecw.mjs check aecw"
  },
  "tool": { "name": "aecw", "version": "0.9.0", "mode": "vendored" }
}
```

**规则**：文档不手抄命令；`check` 从 manifest 读路径/命令并验证存在；`tool.mode=vendored` 时校验版本/哈希，防止 CLI 副本漂移。

### 6.3 `state.json` 示例

```json
{
  "stage": { "name": "grow-2", "state": "closed", "gate": "gates/2026-11-05-grow-2.md" },
  "features": {
    "G4": { "state": "accepted", "release": "unreleased", "evidence": ["F-040"] }
  },
  "release": { "version": "1.2.0", "state": "released", "tag": "v1.2.0" },
  "evolution": { "EV-001": "active" },
  "adoption": { "state": "pending", "gate": "gates/2026-11-05-adoption.md" },
  "evidence_debt": [
    { "id": "ED-001", "item": "G4 设置页截图", "owner": "meo1102", "due": "2026-11-12", "impact": "release" }
  ],
  "baseline": { "commit": "4589b91", "tag": "aecw-layout-v2-2026-11-05" }
}
```

`STATUS.md` 只保留渲染后的当前段 + 叙述；**不再允许手写与 state 重复的字段**。  
如果暂时不做渲染器，至少让 `STATUS` 顶部有一个 `state` 摘要块，`check` 校验它与正文关键句一致。

### 6.4 `criteria.md` 示例

| ID | 判据 | 状态 | 证据 | 核验人 | 人类裁决 |
|---|---|---|---|---|---|
| G4-1 | 设置页可打开、控件可操作 | met | F-040（E2） | 人类 | 接受（2026-11-05） |
| G4-2 | 字号 12/18、宽度 280/480、联动 | met | F-037 + F-040 | 人类 | 接受 |
| G4-3 | 至少一张设置页截图 | deferred | 无 | — | 人类待签（ED-001） |
| G2-8 | 双会话并发 | waived | F-028 | 人类 | 接受为遗留 |

**门禁规则**：

- `met` 必须有证据；
- `waived/deferred` 必须有人类裁决 + 日期 + 影响门；
- 有 `failed/not-started` 时不能“通过”，只能“暂停/退回”；
- `有条件通过` 必须绑定矩阵里的具体行，不能是自由文本。

### 6.5 检查器分两层

| 层 | 查什么 | 失败后果 |
|---|---|---|
| `check`（静态/语义） | 文件、owner、S1/S2、freeze/start、蓝图批准、state/criteria 一致性、路径/命令存在、Markdown 围栏/链接、历史文档状态 | FAIL 不开门 |
| `probe`（运行态） | 安装、link/junction、bundles、patch、路由、slot/版本 | FAIL 不开门 |
| 人类 E2 | 入口、视觉、真实使用 | 没有 E2 不得称“人类可用” |

**关键**：`check` 不能只看“文件在不在”；要查“当前文档说的是不是同一件事”。

### 6.6 文档状态

每个文档头部加：

```text
> 状态：current | historical | superseded
> 最后核对：2026-11-05
> 替代/被替代：...
```

规则：

- `current` 文档之间不能互相矛盾；`check` 抽查关键字段；
- `historical/superseded` 文档不参与当前结论；旧路径/旧命令允许存在，但必须有状态头；
- `STATUS` 只列 `current` 文档；
- 迁移/门禁/复盘默认 `historical`，除非明确“当前仍有效”。

---

## 7. 最小落地顺序（不要一次做大）

1. **真话修复（maintenance 泳道）**：先修 `STATUS`、`product/README`、`board`、`decisions`、`learning`、`ev-001`、`retrospective` 的当前矛盾；历史文档加 `HISTORICAL` 头。不要改产品行为。
2. **加 `PROJECT.json`**：两个根、安装目标、三条命令、工具版本；把文档里的手抄命令换成引用。
3. **加 `criteria.md`**：把 G1–G4、WP-0–6 的判据/证据/豁免逐项落表；`grow-2` 的“有条件通过”补成具体行。
4. **加 `state.json` + `STATUS` 视图**：先只做“阶段/发布/进化/采纳/证据债”五个字段；不追求全自动渲染，先让 `check` 能对账。
5. **升级 `check`**：路径/命令存在、Markdown 围栏、当前文档关键词矛盾、历史文档状态头；`check` 失败不得开门。
6. **再开下一阶段**：新蓝图必须引用 `criteria.md`；发布门必须先结清证据债或人类签署不补。

**不要**在真话修复之前开新功能阶段；否则新状态会继续叠在旧矛盾上。

---

## 8. 不做什么（防止过度反应）

- **不新增四个常设角色。** 问题不是“没人负责”，是“状态没有模型”；加角色只会增加同步成本。
- **不要求所有文档都自动生成。** 只生成“当前状态/门禁/验收”三类高频视图；证据/复盘保留手写。
- **不把 `state.json` 做成数据库/仪表盘。** 一个文件、五个字段、`check` 能读即可。
- **不因为这次矛盾就否定“单一 STATUS”。** 它仍然必要；只是必须从“手写摘要”升级为“状态视图”。
- **不把 `有条件通过` 当常规出口。** 条件必须可核对、可到期、有人签。
- **不把 E2 升级成 E1。** 零截图仍然是缺口，不能因为“人类说了”就变成运行事实。

---

## 9. 结论

这次实践最有价值的发现，不是“AECW 结构能跑”，而是：

> **结构能跑，不等于事实能对上；文档齐全，不等于状态一致。**

AECW 下一版的重点不应是再加门禁/角色/模板，而是：

1. **把状态从散文变成记录**（state + criteria）；
2. **把路径/命令/工具从手抄变成清单**（PROJECT.json）；
3. **把阶段外工作变成泳道**（maintenance/evolution/release）；
4. **把入口/通道/证据债变成验收对象**。

一句话：

> **三域不变，两个根；单一状态，多种视图；四条泳道，一个矩阵；check 查事实，probe 查现场。**

---

## 10. 补记（2026-11-06）：最后四回合与“动作完成不写回”

回看 `插件改造与设置页开发 (1)` 最后四回合，问题不是“agent 不会做”，而是：

> **agent 把动作做完就回复了，没有把动作结果写回状态。**

具体表现：

- 发布 v1.3.0 后，代码/门禁更新了，但 `state` 与 `STATUS` 的更新依赖人工提醒；
- “产品/AECW 分层”后，`PROJECT.json`/`state` 还没有 `layout` 字段，布局不是状态的一部分；
- 推 GitHub 后，remote URL/分支没有写进 `state`，只在回复里说“已推送”；
- 结果：下一回合的 agent 要从聊天记录里推断“现在是什么布局/装在哪/推到哪”，而不是从状态源读。

修复（已落到真实项目）：

1. `state.json` 增加 `layout` / `install` / `remote`：布局根、治理根、安装目标、remote URL/分支；
2. `AGENTS.md` 增加硬规则：**动作完成 = 状态写回**；只做动作不写回视为未完成；
3. `check` 增加对账：`state.layout` / `state.install.target` 与 `PROJECT.json` 不一致 FAIL；`state.remote.url` 与 git origin 不一致 FAIL；
4. 本次布局 v3（取消 `product/` 层）按“改布局 → 写 state/STATUS/证据 → check → commit → push → 再写 remote → check”执行，并把过程写入证据。

仍有的缺口：

- `check` 只校验 remote URL，不校验“本地是否已 push / 远端 HEAD 是否一致”；
- 没有 `aecw state` 命令，写回仍是手工编辑 + check 拦截；
- `state.remote.last_pushed_tag` 是人工写回，不是从 git 自动推导。

下一步若继续做，应加一个 **`aecw state` / `aecw sync` 命令**：从 `PROJECT.json`、git remote、package.json、probe 结果生成 `state` 候选，再让人类/agent 确认写回；这样“写回”从提醒变成默认动作。
