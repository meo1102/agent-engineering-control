# 与试点/概念的对应：原型解决什么、不解决什么

## 1. 试点失败 → 原型机制

| 试点问题 | 原型机制 | 能不能自动防 |
|---|---|---|
| README 说“已安装”，实际插件未加载 | `check` 要求 STATUS/证据；`context-hygiene` 要求运行态探针优先 | 部分：原型不替你跑探针，但把“先探针”写成门禁规则 |
| G2 常驻提醒遮挡按钮，单测没发现 | demo 的 S2 异议 + `G2-blocked`/`G2-resolved`；S1/S2 直达人类 | **结构上防**：开放 S2 时 gate 显示阻断 |
| 测试替身比真实宽松，真机崩溃 | 验证者上下文隔离 + E1/E2 + 角色规则 | 规则防；原型不自动生成真实签名桩 |
| PowerShell 默认编码破坏中文 | context-hygiene 编码规则；原型文件 UTF-8 | 规则防；CLI 用 UTF-8 写文件 |
| 11 份文档互相打架 | v0.9 单一状态源 + STATUS 视图 + 文档状态；v0.8 只用单一 STATUS | 部分：v0.8 只能防结构；真实项目证明手写 STATUS 仍会漂移 |
| 人类所有者未具名 | `check` 对“待补/未具名”直接 FAIL | **结构上防** |
| 无截图、口述当证据 | E2 定义 + context-hygiene 截图规则 | 规则防；原型不自动截图 |
| 单 agent 自写自验 | 角色规则：高影响验收非作者；验证者新鲜上下文 | 规则防；原型不强制多 agent |
| 六道门/事实包过重 | 默认单 agent + 一页门禁 + 一行台账 | **结构上减负** |
| 发布合规未闭合 | STATUS 区分“技术发布/治理待追认”；`check` 查所有者 | 部分：原型不替人追认，但把矛盾显式化 |
| 拿到宪章就一股脑做下去 | 蓝图 + `freeze` + `start` + `check` 无 freeze/start FAIL | **结构上防**：蓝图/冻结/开工令三段分离，只授权一个阶段，阶段结束停 |
| 没有蓝图，agent 各自发明范围 | `BLUEPRINT.md` 工作包/接口/未知/不做/验收 + 人类批准 | **结构上防**：未批准不 freeze；`start` 拒绝 |
| 把 freeze 当开工令 | `start-order` 独立门禁 + STATUS `executing` + `check` 无 start FAIL | **结构上防**：冻结后仍需人类显式 go |
| 中途改需求变成范围蔓延 | `change` 三级（task/blueprint/charter）+ 开放变更 WARN + 新版本 re-freeze/start | **结构上防**：不原地改冻结基线；charter/blueprint 变更未裁决时提示不得扩范围 |
| `check`/`probe` 全绿，但 STATUS/README/board 仍互相矛盾 | v0.9：`state.json` + `criteria.md` + 文档状态 + `check` 查事实 | 设计已给出；原型尚未实现全部 |
| 设置页 slot 注册成功，但人类找不到入口 | 入口契约：写清“设置 → 插件 → 页签”；人类 E2 “自己找到” | 规则防；原型不生成 UI |
| 抑制浮层时把系统通知一起吞了 | 通道矩阵：浮层/系统通知分列；抑制一个通道 ≠ 抑制全部 | 规则防；需要单测覆盖每个通道 |
| 布局迁移后命令/路径多处漂移 | `PROJECT.json` 单一命令源；文档引用，不手抄 | 结构上防；原型待实现 manifest |

## 2. 概念映射

| 概念 | 原型落点 |
|---|---|
| 人类方向权包 | `human/direction.md` + `human/decisions.md` |
| 施工蓝图/开工令 | `BLUEPRINT.md` + `gates/<date>-charter-freeze.md` + `gates/<date>-start-order.md` |
| 项目中途变更 | `ledger.md` C. 变更台账 + `inbox/CR-xxx.md` + 新蓝图版本 |
| 真实使用/遗留接受 | `human/acceptance.md` + `workspace/landing/manifest.md` |
| 集群实现/学习/进化 | `cluster/board.md`、`runs.md`、`learning.md`（进化只留候选，不自动生效） |
| 工作区生长/记忆/落地 | `workspace/{work,evidence,memory,landing}` + `STATUS.md` |
| 三基线 | 方向（direction）、验收（acceptance/gates）、能力（roster/runs/learning） |
| 两本账 | 交付（board/evidence/acceptance）+ 学习（learning，不自动晋升） |
| 六接口 | `docs/interfaces.md` + `ledger.md`/`inbox/`/`gates/` |
| 三区/五平面 | 轻量化为 work/evidence/memory/landing + STATUS；不强制三区 |
| 异议通道 | `ledger.md` + `inbox/` + S1/S2 直达人类 |
| 事实驱动 | `ledger.md` 事实表 + E1/E2/E3 + 门禁事实区 |
| 上下文卫生 | `docs/context-hygiene.md` + `STATUS.md` + SUPERSEDED |

## 3. 原型不解决什么

- **agent 运行时**：不调度模型、不管理多 agent 进程、不做上下文窗口管理。
- **自动探针/截图**：`check` 只查结构，不替你跑测试/装插件/截图。
- **真实多 agent 隔离**：只给规则与工件；真正的上下文隔离要靠运行环境。
- **变更影响分析自动化**：`change` 只记录 CR 与提示，不计算返工/排期；影响分析由人/agent 填。
- **进化制度化**：learning ledger 只记录候选，不自动晋升技能/规则/模型。
- **外部真实使用**：原型只能记录，不能替代外部用户。
- **法律/合规**：不替代合规审查。

## 4. 下一步

1. 用原型跑一个真实小项目（2–4 周），记录卡点。
2. 记录一次真实变更（最好是 blueprint 级），检验“影响分析 + 新版本 + 重新 freeze/start”是否过重。
3. 如果 `check` 的所有者/开放 S1/S2/蓝图/开工令规则有效，再考虑自动化探针。
4. 如果单 agent + 人类够用，不引入多 agent；需要时再加“验证者”一个上下文隔离角色。
5. 把 pilot 的 G2-1/G2-8 类问题作为 demo 固定用例，防止原型退化。
