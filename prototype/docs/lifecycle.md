# 生命周期：seed → grow → land → steward → compost

## 1. 总表

| 阶段 | 目标 | 关键动作 | 出门条件 | 命令 |
|---|---|---|---|---|
| **seed** | 立边界 | 填 direction；写蓝图并批准；freeze；start；第一道门 | 目标可判断、S1–S4 明确、所有者具名、蓝图批准、freeze/start 已签 | `init` / `blueprint` / `freeze` / `start` / `fact` / `gate` |
| **grow** | 做与证 | 任务板、实现、证据、异议/事实、阶段门、变更 | 集成可用、开放 S1/S2=0、目标轨迹正常 | `dissent` / `fact` / `gate` / `change` |
| **land** | 真实使用/落地 | 真实使用、验收、落地清单、照护者 | 遗留有人接受、可运维/交接/退役 | `accept` / `gate` |
| **steward** | 照护 | 观察、复审、再验证、退役 | 有照护者/预算/唤醒条件 | `log` / `gate` |
| **compost** | 失败/终止 | 封存、归因、墓碑、教训候选 | 失败事实不可改写、资源释放 | `log` / `accept` |

## 2. seed

- 人类填 `human/direction.md`：目的、非目标、失败定义、S1–S4、预算、停止、升级触发。
- 集群起草 `BLUEPRINT.md`：本阶段目标、工作包、接口、未知、不做、阶段验收；人类修改并批准（`- 状态：approved` + 具名批准人）。
- 写 `STATUS.md`：阶段、所有者、当前目标、基线事实。
- 异议窗口：开放 S1/S2 必须清零；S3/S4 有主/有期限。
- 第一条事实：运行态（安装/版本/入口/测试），不是文档声明。
- **freeze**：`freeze --charter-confirmed --stage ... --scope ... --budget ... --stop ... --acceptance ...`；写 `charter-freeze` 门禁 + STATUS 阶段授权。要求蓝图已批准、无开放 S1/S2。
- **start**：`start --by <人类> --first-report <报告点>`；写 `start-order` + STATUS 开工令；只有这时才可执行。
- **出门**：人类所有者具名；失败定义至少一个反例；S1/S2 清零；蓝图批准；**charter-freeze 与 start-order 已签**。

## 3. grow

> 前提：seed 的 `charter-freeze` 与 `start-order` 都已签；只执行授权阶段；阶段结束停，不自动续跑。

- 任务板每行：ID、任务、负责人、状态、输入、输出、验收；只接蓝图内工作包。
- 每个任务至少一条事实/证据；候选写 `workspace/work/`，不写“已验收”。
- 异议：S3/S4 一行；S1/S2 进 `inbox/` 直达人类。
- 变更：task 级记 board/runs；blueprint/charter 级走 `change`，人类裁决后再动；不原地改冻结基线。
- 门禁：`gate --name <stage>`；开放 S1/S2 阻断高风险；开放 blueprint/charter 变更时不得扩大范围。
- **出门**：集成证据、开放 S1/S2=0、目标轨迹检查、剩余风险有主；**到阶段边界停、报告、等下一道门**。

## 4. land

- 真实使用：谁、什么目的、什么情境、失败/代价/副作用；E2 要写“无截图”或附截图。
- 验收：`accept --item ... --decision 有条件接受 --risk ... --by <人类>`。
- 落地清单：可用、可运维、可交接、可审计、成本、遗留接受、照护者、退役。
- **出门**：具名照护者；遗留有人接受；退役路径；STATUS 更新。

## 5. steward

- 观察范围、复审周期、唤醒条件、预算、照护者。
- 新证据追加，不改历史；旧结论不跨代继承。
- 退役：条件、数据处置、责任转移。
- **出门**：有人照护；有复审/退役条件；无照护即降级，不假装活跃。

## 6. compost

- 终止/失败/放弃：封存证据、归因（允许“不明”）、墓碑（“我们曾相信 X，X 被证伪”）、教训候选、资源释放。
- 失败事实不可改写；教训是独立且可能出错的判断。
- **出门**：失败记录保留；学习账结账；资源释放；不把失败洗成“成功”。

## 7. 状态与门禁

- `STATUS.md` 的阶段字段：seed/grow/land/steward/compost；阶段状态：seed/frozen/executing/paused/closed。
- 每道门一页；`charter-freeze` 锁基线，`start-order` 是开工令；有开放 S1/S2 时高风险动作暂停。
- 门禁决策：通过 / 有条件通过 / 退回补证 / 暂停 / 拒绝。
- 旧门禁是历史；当前状态看 STATUS。

## 8. 项目中途改目标

- **task 级**：同一工作包内换实现/补测试，不改验收；集群管家在阶段预算内处理，记 board/runs。
- **blueprint 级**：加/删工作包、改接口/验收/顺序/依赖；写 `change`，人类裁决；接受后升蓝图版本、重新 freeze、重新 start。
- **charter 级**：改目的/非目标/失败定义/S1–S4/预算；先停，重谈宪章，新 freeze；可能按新项目处理。
- **当前阶段**：默认做完再切；也可检查点停车；新需求使方向失效则中止进 compost。
- **硬规则**：不原地改冻结基线；不静默改验收；每阶段设变更预算；人类可随时叫停。
