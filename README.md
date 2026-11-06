# Agent 工程控制工作流（AECW）

> 用「方向契约 → 生长治理 → 记忆与落地」构成一个人类定方向、agent 集群学习进化、项目工作区承载记忆与落地的三元控制模型。

## 这是什么

本项目讨论并沉淀一套**通用的 agent 工程控制模型**：当工程的主要执行者是 agent 时，如何把“方向、目标、实现、学习、进化、验收、记忆、落地”组织成一个能复利、可问责、可停止的系统，而不是一串依赖对话上下文和临场发挥的临时协作。

本项目从**概念构想**进入**概念 + 原型 + 真实部署校准**：早期轮次只讨论概念的完成度、逻辑自洽、漏洞与优势；v0.8 起用可跑原型和真实项目作证据，不再停留在纸面。

当前主交付是 **v0.5 三元生长模型**：人类负责方向、目标与真实使用验收；agent 集群负责实现、学习与进化；项目工作区是目标与实现的生长环境、记忆与最后落地区。v0.5 在 v0.4 的交付—验收链之上，补上了选择压力、记忆宪法、问责主体、预算停止与失败出口。

v0.6 是**执行补充（重版本）**：把“agent 集群向上对接人类的异议返回通道”与“整个生命周期所有活动根据事实而行”落成可执行的角色、工件、SLA、模板与 90 天路线图，见 [PLAN-v0.6-异议通道与事实运行.md](PLAN-v0.6-异议通道与事实运行.md)。

v0.7 是对 v0.6 的**精简修订（当前执行版）**：取消四个常设新角色，人类只保留方向/目标/高风险例外/最终验收；**边界清晰 → 默认相信 → 例外升级 → 抽样验证 → 失信收紧**，见 [PLAN-v0.7-信任优先.md](PLAN-v0.7-信任优先.md)。

v0.7.1 是试点后的**上下文卫生增补**：运行态事实优先、单一状态页、旧文档审计、证据硬度、自证上限、新 agent 接手测试、集群声称纪律，见 [PLAN-v0.7](PLAN-v0.7-信任优先.md) 第 10 节。真实试点复核见 [PILOT-REVIEW-task-complete-toast.md](PILOT-REVIEW-task-complete-toast.md)，新 agent 状态五问实测见 [HANDOVER-TEST-task-complete-toast-2026-11-04.md](HANDOVER-TEST-task-complete-toast-2026-11-04.md)。

v0.7.2 是原型讨论后的**开工门增补**：宪章定方向，**施工蓝图**定做法，`freeze` 锁阶段基线，`start` 才是人类开工令；中途改目标走 task/blueprint/charter 三级变更，不原地改冻结基线，见 [PLAN-v0.7](PLAN-v0.7-信任优先.md) 第 11 节。

v0.8 是**生态原型 v0.1**：把三域（人类/集群/工作区）、六接口、蓝图/冻结/开工令/变更、STATUS/异议/事实/门禁/验收落成一个零依赖 CLI 与可跑 demo，见 [prototype/README.md](prototype/README.md)。

v0.9 是**真实项目校准**：第一次真实部署 `task-complete-toast-aecw` 证明“结构全绿 ≠ 事实一致”。保留三域与信任优先，补上**两个根、项目清单、单一状态源、验收矩阵、四条泳道、入口/通道矩阵**；见 [PLAN-v0.9-真实项目校准.md](PLAN-v0.9-真实项目校准.md)，证据与矛盾清单见 [REVIEW-task-complete-toast-aecw-2026-11-05.md](REVIEW-task-complete-toast-aecw-2026-11-05.md)。

2026-11-06 的真实项目布局 v3 进一步验证：**产品根可以由 `PROJECT.json.roots.product` 定义为仓库根**，不必叫 `product/`；同时补上“**动作完成 = 状态写回**”——布局/安装/版本/tag/发布/远程变化后，必须写回 `state`/`STATUS`/证据，`check` 校验 `layout`/`install`/`remote`。见 [REVIEW](REVIEW-task-complete-toast-aecw-2026-11-05.md) §10。

v0.9.1 是**红队整改方案**：报告证明当前 AECW 更像“诚实的单 agent 记录 + checklist”，不是强制治理边界。方案先定 L（local-trusted）/E（enforced）威胁模型，再按 P0 修 `verify`、状态机、原子台账、批准绑定、探针/写路由；见 [PLAN-v0.9.1-红队整改.md](PLAN-v0.9.1-红队整改.md)。

v0.10 是**精简化改造 + 首次进化试点**：从“多文档、多道门、每步签字”收成“一个源、一个门、一个验证、一个进化闭环、按风险分级”；`gate` 模板废弃，改为 decision + condition 生命周期；`EV-2026-11-06-01` 是第一次真实候选/工件/指标/ledger 试行。方案见 [PLAN-AECW-精简化改造.md](PLAN-AECW-精简化改造.md)，结构图见 [diagrams/cluster-minimal-structure.png](diagrams/cluster-minimal-structure.png)，复验见 [简化改造复验](REVIEW-task-complete-toast-aecw-simplified-r2-2026-11-06.md)。

## 目录导航

| 路径 | 内容 |
| --- | --- |
| [REPORT-v4.md](REPORT-v4.md) | **第四轮汇总报告 v0.5（概念主交付）**：三元宪约、工作区/记忆/落地、集群学习与进化、三基线/两本账/四时钟/六门、优点、缺口、失效模式、基线 |
| [PLAN-v0.7-信任优先.md](PLAN-v0.7-信任优先.md) | **v0.7/v0.7.1/v0.7.2 执行版（当前）**：取消四个常设角色、边界宪章、默认信任、例外升级、人类注意力合同、轻量台账与门禁检查单、上下文卫生、蓝图/开工令/三级变更 |
| [PILOT-REVIEW-task-complete-toast.md](PILOT-REVIEW-task-complete-toast.md) | **真实试点复核**：task-complete-toast 的概念偏差、上下文污染、agent 集群实况、优点/冗余/难实现点、下一轮对照实验 |
| [HANDOVER-TEST-task-complete-toast-2026-11-04.md](HANDOVER-TEST-task-complete-toast-2026-11-04.md) | **新 agent 接手测试数据**：状态五问、11 个分叉、3 个缺口、1 次确认误读、9 个作者问题；单一状态页的实证 |
| [prototype/](prototype/) | **AECW 生态原型 v0.1**：三域/六接口/五阶段、蓝图/冻结/开工令/变更、零依赖 CLI、可跑 demo、落地文档 |
| [REVIEW-task-complete-toast-aecw-2026-11-05.md](REVIEW-task-complete-toast-aecw-2026-11-05.md) | **真实项目校准证据**：check/probe 全绿但 STATUS/README/board/decisions 互相矛盾；判据/证据/发布/采纳/泳道/入口/通道的疏漏清单 |
| [PLAN-v0.9-真实项目校准.md](PLAN-v0.9-真实项目校准.md) | **v0.9 部署架构（当前设计基线）**：两个根、PROJECT.json、state.json、criteria.md、四条泳道、check/probe 分层、文档状态 |
| [PLAN-v0.9.1-红队整改.md](PLAN-v0.9.1-红队整改.md) | **红队整改方案（已执行到 S1–S5）**：报告 vs 现状、L/E 威胁模型、P0 fail-closed/verify/状态机/原子存储/批准绑定/探针安全、P1/P2 顺序 |
| [PLAN-AECW-精简化改造.md](PLAN-AECW-精简化改造.md) | **v0.10 精简化改造方案**：一个源、一个门、一个验证、一个进化闭环、L0/L1/L2；W0–W6 一次整改；不新增角色/仪表盘 |
| [diagrams/cluster-minimal-structure.png](diagrams/cluster-minimal-structure.png) | **精简结构图（一页版）**：三域 + 编排者/worker/按需验证 + state/evidence/decision/evolution |
| [REVIEW-task-complete-toast-aecw-simplified-r2-2026-11-06.md](REVIEW-task-complete-toast-aecw-simplified-r2-2026-11-06.md) | **v0.10 复验（最近）**：condition 生命周期、baseline/tag、首次进化 `EV-2026-11-06-01` 的机械闭环与效果缺口 |
| [templates/status.md](templates/status.md) | **单一状态页模板**：当前发布、E1/E2/E3 证据、已接受遗留、未测项、文档时效表、矛盾裁决 |
| [PLAN-v0.6-异议通道与事实运行.md](PLAN-v0.6-异议通道与事实运行.md) | v0.6 详细重版本（已被 v0.7 精简，保留作为严格场景参考）：四角色、SLA、完整事实包/异议审查 |
| [templates/异议与事实台账.md](templates/异议与事实台账.md)、[templates/门禁检查单.md](templates/门禁检查单.md) | **v0.7 轻量模板（默认用）**：一张台账、一页门禁检查 |
| [templates/](templates/) | v0.6 详细模板（可选）：异议记录、事实记录、门禁事实包、门禁异议审查 |
| [REPORT-v3.md](REPORT-v3.md) | 第三轮汇总报告 v0.4：文档可用性、阶段工作区验收、真实使用、验收后学习 |
| [REPORT-v2.md](REPORT-v2.md) | 第二轮汇总报告 v0.3：角色权限、交付物四分、三态投影、观测分派、三层验收与三环错误收敛 |
| [REPORT.md](REPORT.md) | 第一轮汇总报告 v0.2：七要点控制回路、判据信任根、工作区一致性与记忆治理 |
| [BRIEF-v4.md](BRIEF-v4.md) | 第四轮任务书：方向—生长—落地三元模型与生长治理 |
| [BRIEF-v3.md](BRIEF-v3.md) | 第三轮任务书：目标锚定的工作区交付、真实使用验收与验收后进化 |
| [BRIEF-v2.md](BRIEF-v2.md) | 第二轮任务书：角色—交付物—反馈控制生态 |
| [BRIEF.md](BRIEF.md) | 第一轮任务书：原始构想、系统性约束、讨论边界、核心问题 |
| [docs/00-术语表.md](docs/00-术语表.md) | v0.2 项目共同语言与概念定义 |
| [docs/01-概念模型.md](docs/01-概念模型.md) | 七要点的重新定位、核心概念定义、双环结构、三个基本假说 |
| [docs/02-通用工作流.md](docs/02-通用工作流.md) | 七段主干、两道侧环、五道门禁、角色、状态机、工件契约 |
| [docs/03-解耦与工作区协作.md](docs/03-解耦与工作区协作.md) | 工作区作为协议、中断恢复、新 agent 接手 |
| [docs/04-记忆分级与进化.md](docs/04-记忆分级与进化.md) | 记忆分层、晋升与淘汰、错误→教训→技能链 |
| [docs/05-漏洞缺陷与不足.md](docs/05-漏洞缺陷与不足.md) | v0.2 概念漏洞、失效模式、反模式、边界条件 |
| [docs/06-优势与适用边界.md](docs/06-优势与适用边界.md) | 优异点、代价、适用/不适用场景、度量方式 |
| [docs/07-开放问题与下一步.md](docs/07-开放问题与下一步.md) | v0.2 未决问题、优先次序、概念验证设计 |
| [deductions/](deductions/) | 第一轮独立推演原文与任务书 |
| [deductions/round2/](deductions/round2/) | 第二轮四席独立推演原文与执行记录 |
| [deductions/round3/](deductions/round3/) | 第三轮四席独立推演原文与执行记录 |
| [deductions/round4/](deductions/round4/) | 第四轮四席独立推演原文与执行记录（Kimi K3.1 Pro ×2、DeepSeek Flash ×2） |
| [memory/](memory/) | 分级记忆的概念骨架与条目模板（示例，不是实现） |

## 当前状态

- 阶段：概念构想 v0.5 ＋ 执行补充 v0.6/v0.7/v0.7.1/v0.7.2 ＋ 生态原型 v0.1 ＋ 真实项目校准 v0.9 ＋ 红队整改 v0.9.1 ＋ 精简化 v0.10
- 日期：2026-11-06
- 已完成：v0.2 控制与治理骨架；v0.3 交付物调度与权责交接；v0.4 文档可用性、工作区阶段验收、真实使用、验收后学习；v0.5 三元生长模型、生长治理、记忆宪法、集群进化、失败/堆肥出口、落地与照管；v0.6 异议返回通道、事实驱动运行、完整模板与路线图；v0.7 信任优先的最小机制；v0.7.1 上下文卫生增补；v0.7.2 蓝图/开工令/三级变更；task-complete-toast 真实试点复核；新 agent 状态五问实测与 `STATUS.md` 修复；v0.8 生态原型 v0.1（三域/六接口/CLI/demo）；v0.9 真实项目校准（两个根/项目清单/状态源/验收矩阵/四条泳道/入口通道）；v0.9.1 红队整改 S1–S5（verify/freeze/锁/探针/SSOT）；v0.10 精简化（一个源/一个门/一个验证/进化闭环/风险分级）与首次进化试点 `EV-2026-11-06-01`
- 未做（且本阶段不做）：生产级 agent 运行时、模型路由、自动探针/截图、UI/数据库、真实多 agent 编排
- 已知限制：第四轮两席 Kimi 通道未暴露逐席 `reasoningEffort`；两席 DeepSeek 前几轮记录为 `high` 而非任务书要求的 `max`；四席为单轮生成，无交叉质询；v0.6/v0.7 未经过真实试点，v0.7.1 基于单项目单日试点；试点是单 agent + 人类，不是多 agent 集群；新 agent 接手测试被 `PILOT-REVIEW` 污染（下一轮需隔离）；v0.9 是设计基线，`PROJECT.json`/`state.json`/`criteria.md` 尚未在原型 CLI 全部实现；详见 [PILOT-REVIEW](PILOT-REVIEW-task-complete-toast.md)、[HANDOVER-TEST](HANDOVER-TEST-task-complete-toast-2026-11-04.md)、[v0.9 校准](PLAN-v0.9-真实项目校准.md)
- v0.10 首次进化只证明“候选→评估→采纳/淘汰”管线能跑：指标是 `open-conditions` 9→8，且来自关闭 remote 条件，不是同任务 A/B；尚不能证明准确率/效率提升。baseline commit 与 tree、release tag 不可变、条件关闭证据仍有缺口，见 [v0.10 复验](REVIEW-task-complete-toast-aecw-simplified-r2-2026-11-06.md)。

## 阅读顺序建议

1. **只需了解当前完整框架时，直接读 [REPORT-v4.md](REPORT-v4.md)。** 它自成体系，不要求先读前三轮。
2. 需要把“异议 + 事实”落到项目里，直接读 [PLAN-v0.7-信任优先.md](PLAN-v0.7-信任优先.md) 第 8 节“下一轮怎么做”，并复制 [异议与事实台账](templates/异议与事实台账.md)、[门禁检查单](templates/门禁检查单.md) 两个轻量模板；蓝图/开工令/变更见第 11 节。
3. 需要直接跑结构原型，读 [prototype/README.md](prototype/README.md)，在 `prototype` 目录执行 `node bin/aecw.mjs demo` 和 `node bin/aecw.mjs check examples/demo-project`。
4. 需要看真实项目怎么打脸概念，读 [PILOT-REVIEW-task-complete-toast.md](PILOT-REVIEW-task-complete-toast.md) 与 [HANDOVER-TEST](HANDOVER-TEST-task-complete-toast-2026-11-04.md)。
5. 需要把 AECW 部署到真实仓库，读 [PLAN-v0.9-真实项目校准.md](PLAN-v0.9-真实项目校准.md)，先看 [REVIEW](REVIEW-task-complete-toast-aecw-2026-11-05.md) 的矛盾清单，再按 §5 的最小迁移顺序做“真话修复 → 项目清单 → 验收矩阵 → 状态源 → check 升级”。
6. 需要严格场景/完整角色与 SLA 时，读 [PLAN-v0.6-异议通道与事实运行.md](PLAN-v0.6-异议通道与事实运行.md)；它与 v0.7 冲突时，以 v0.7 为准。
7. 需要追溯交付与验收控制基础时读 [REPORT-v3.md](REPORT-v3.md)；需要追溯交付物调度时读 [REPORT-v2.md](REPORT-v2.md)；需要追溯原始七要点时读 [REPORT.md](REPORT.md)。
8. 需要核对第四轮原始推演，读 [deductions/round4/](deductions/round4/) 下的四席原文与执行记录。
9. `docs/` 主要保存 v0.2 的分主题细节，术语与结论若与 v0.5–v0.9 不同，以最新文档的显式裁决为准。

## 一句话结论

v0.5 以人类方向权为罗盘，以 agent 集群的选择压力为生长引擎，以工作区为生长环境、记忆与落地之家；验收用真实使用，进化用证据与授权。**生长 = 学习 × 验收 ÷ 遗忘**：没有选择压力的生长是堆积，没有真实使用的验收是表演，没有遗忘的记忆是噪声。v0.6 再加两道结构：**异议必须到达有权者，事实必须带来源与状态**。v0.7 进一步把结构做薄：**边界清晰 → 默认相信 → 例外升级 → 抽样验证 → 失信收紧**；不能为了保证而保证。v0.8 把以上落成可跑的三域原型：**人类定方向，集群在边界内工作，工作区记住并落地。** v0.7.2 再补一道最容易被忽略的门：**宪章定方向，蓝图定做法，freeze 锁基线，start 才开工；变更走 CR，不偷偷改基线。** v0.9 用真实项目补上部署层：**三域不变，两个根；单一状态，多种视图；四条泳道，一个矩阵；check 查事实，probe 查现场；动作完成 = 状态写回。**
