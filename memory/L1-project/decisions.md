# 决策记录（L1 项目记忆）

> 本项目自身也是工作流概念的一次演练：关键选择记录"为什么"，而不只是"选了什么"。

## DR-001 推演席位的模型切换

- **背景**：任务要求用 `kimi-for-coding` 与 `deepseek-flash` 两个模型做独立推演。
- **选项**：
  1. 坚持 `kimi-for-coding`，等待凭据修复；
  2. 用 `deepseek-reasoner` 替补；
  3. 改用 `kimi-k3`（Moonshot 通道）重跑。
- **事实**：`kimi-for-coding` 首步返回 401（API Key invalid or expired）；`deepseek-reasoner` 替补完成（推理强度记录为 high）；用户指示改用 `kimi-k3` 重跑。
- **决定**：以 `kimi-k3`（provider `moonshotai`）作为正式 A 席位；`deepseek-reasoner` 保留为备用证据，不参与主对照。
- **理由**：满足"Kimi 席 + DeepSeek 席"的模型多样性要求；k3 与 B 不同模型家族，独立性优于替补；替补结果仍有独立价值，归档不删除。
- **后果**：k3 通道未在会话记录中暴露 `reasoningEffort`，max 推理强度只能由任务书要求保证；报告第 10.3 节如实标注。
- **否决记录**：没有采用"只保留 deepseek-flash + 主控"方案，因为会丢失一个模型家族的独立视角；没有等待 `kimi-for-coding` 凭据修复，因为用户明确要求用 k3 重跑。
- **日期 / 决策者**：2026-11-02 / 用户指示 + 主控执行
