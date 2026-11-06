# START HERE · 5 分钟跑通 AECW 原型

> 目录：`agent-engineering-control/prototype`。零依赖，Node ≥18。

## 1. 跑 demo

```powershell
cd agent-engineering-control/prototype
node bin/aecw.mjs demo
node bin/aecw.mjs check examples/demo-project
```

`check` 应输出 `FAIL 0｜WARN 0`。

## 2. 按顺序看 8 个文件

1. `examples/demo-project/STATUS.md`
2. `examples/demo-project/human/direction.md`
3. `examples/demo-project/BLUEPRINT.md`
4. `examples/demo-project/gates/` 里的 `charter-freeze`
5. `examples/demo-project/gates/` 里的 `start-order`
6. `examples/demo-project/ledger.md`
7. `g2-blocked` → `g2-resolved`
8. `examples/demo-project/workspace/landing/manifest.md`

你要能回答：

- 现在是什么状态？
- 宪章、蓝图、冻结、开工令分别是什么？
- 什么已验证（E1/E2/E3）？
- 什么未测/被接受？
- 下一步是什么？
- 哪些结论不能信？

## 3. 建自己的项目

```powershell
node bin/aecw.mjs init D:\tmp\my-project --name my-project --owner "你的名字" --goal "一句话目标"
```

先填 `human/direction.md`（方向/非目标/失败定义/S1–S4/预算/停止），再写施工蓝图：

```powershell
node bin/aecw.mjs blueprint D:\tmp\my-project --stage grow-1
```

填 `BLUEPRINT.md` 的工作包/接口/未知/阶段验收；人类批准时，把：

```text
- 状态：draft
- 批准人：（待批准）
```

改为：

```text
- 状态：approved
- 批准人：你的名字
```

然后冻结 + 开工：

```powershell
node bin/aecw.mjs freeze D:\tmp\my-project --charter-confirmed `
  --stage grow-1 `
  --scope "只做 G1/G2；不含外部发布" `
  --budget "2 周 / 20 个 agent 回合" `
  --stop "S1 / 预算耗尽 / 连续两道门禁失败" `
  --acceptance "G1 5/5；G2 7/8；G2-8 可接受为遗留"

node bin/aecw.mjs start D:\tmp\my-project --by "你的名字" `
  --first-report "G2 门禁前，或触发 S2 时"

node bin/aecw.mjs check D:\tmp\my-project
```

`freeze` 要求：人类确认、owner 具名、蓝图已批准、无开放 S1/S2、direction 已填。`start` 要求：已 freeze、蓝图已批准、无开放 S1/S2。没有 freeze/start 的阶段，`check` 会 FAIL。

## 4. 第一次真实动作

```powershell
node bin/aecw.mjs fact D:\tmp\my-project --statement "测试 10/10 通过" --source "node --test 输出" --status 已核验 --verifier "另一个 agent"
node bin/aecw.mjs dissent D:\tmp\my-project --severity S2 --type 风险 --claim "这个改动会挡住用户操作" --evidence "真机目视"
node bin/aecw.mjs gate D:\tmp\my-project --name grow-1 --decision 暂停
```

S2 会生成 `inbox/DR-001.md`：**直达人类**。未解决前，`gate` 会显示开放 S1/S2，建议暂停高风险动作。

## 5. 中途有新需要

先判断它改的是哪一级，再走 `change`：

```powershell
# 任务级：同一工作包内换实现/补测试，不改验收
node bin/aecw.mjs change D:\tmp\my-project --type task --title "换实现方式" --by "agent"

# 蓝图级：加/删工作包、改接口/验收/顺序/依赖
node bin/aecw.mjs change D:\tmp\my-project --type blueprint --title "加导出" `
  --reason "用户需要" --impact "新依赖；+3 天" --by "你的名字"

# 宪章级：改目的/非目标/失败定义/S1-S4/预算
node bin/aecw.mjs change D:\tmp\my-project --type charter --title "改目标" `
  --reason "..." --impact "..." --by "你的名字"
```

裁决：

```powershell
node bin/aecw.mjs change D:\tmp\my-project --id CR-001 --decision 接受 --reason "接受；升 v2 后重新 freeze"
```

- task：阶段内处理；吃掉 20% 以上预算或改验收 → 升级 blueprint；
- blueprint：升蓝图版本 → 重新 `freeze` → 重新 `start`；
- charter：先停 → 重谈 → 新 freeze。

**不要口头加活，不要原地改冻结基线。**

## 6. 六条硬规则

1. **宪章无异议 + 蓝图批准 + 阶段基线冻结 + 开工令，四者同时成立，集群才开工；阶段结束就停。**
2. **人类只做方向/蓝图批准/S1/S2/开工/最终验收/抽样**；S3/S4 本地处理。
3. **异议必须到达有权者**；只留在聊天里不算提出。
4. **STATUS.md 是当前状态视图**；本原型以它为准，真实部署以 `state.json` 为源、STATUS 为视图（v0.9）。
5. **变更不原地改冻结基线**；蓝图/宪章变更要新版本 + 重新 freeze/start。
6. **动作完成 = 状态写回**；布局/安装/版本/tag/发布/远程变化后先写 `state` + `STATUS` + 证据，再回复；只做动作不写回视为未完成。

卡住时，先改 `STATUS.md`、`human/direction.md` 或 `BLUEPRINT.md`，不要先加角色/流程。

## 7. 真实项目部署

不要把这个三域目录直接当成真实仓库布局。真实项目按 v0.9：

```text
repo/
├─ package.json / index.js / client.js / lib/ / locale/ / test/  # 产品代码（产品根，可在根或 product/）
├─ aecw/           # STATUS/state/criteria/human/cluster/workspace/gates
├─ PROJECT.json    # 两个根、安装目标、命令、工具版本
├─ README.md       # 只指路
└─ AGENTS.md       # 只指路
```

先读 [`PLAN-v0.9`](../PLAN-v0.9-真实项目校准.md) 与 [`REVIEW`](../REVIEW-task-complete-toast-aecw-2026-11-05.md)；按“真话修复 → 项目清单 → 验收矩阵 → 状态源 → check 升级”做，不要先开新功能阶段。

**动作完成 = 状态写回**：布局/安装/版本/tag/发布/远程变化后，先写 `state` + `STATUS` + 证据，再回复；`state.layout`/`state.install`/`state.remote` 与 `PROJECT.json`、git origin 不一致时 `check` FAIL。
