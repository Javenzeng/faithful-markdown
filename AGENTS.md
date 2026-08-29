# AGENTS.md — Markdown Reader & Editor

本文件是 Human / Sol / Codex 的永久治理入口。它只规定“如何接手和行动”，产品方向以 `PROJECT_CHARTER.md` 为准，代码约束以 `CODE_CLEANLINESS_CONTRACT.md` 为准。

## 1. Cold Start Protocol

任何新会话先读：

1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `MILESTONES.md`

然后按环境与任务追加读取：

- **Repository-only / public checkout**：继续当前任务时读取相关 `records/`；不得假设 repository 内存在 `SESSION_STATE.md`。
- **Human / Sol / Codex Relay environment**：如果外部 Drive Relay surface 提供 `SESSION_STATE.md`，额外读取它作为当前 Baton / short-lived execution checkpoint。
- 要修改源码或构建脚本：再读 `CODE_CLEANLINESS_CONTRACT.md`。
- 要改变 scope、产品定位、长期路线：再读 `PROJECT_CHARTER.md`。

除非当前任务明确要求，不重读整个项目历史。

## 2. Role Model

### Human
- 最终 scope、里程碑、发布、破坏性变更和执行授权者。
- 可随时收回 Baton 或暂停当前里程碑。

### Sol
- 架构 Owner 与主要开发者。
- 负责长上下文审阅、实现设计、主要代码修改、代码审计、测试设计、里程碑维护与 Codex handoff。
- 不把本地环境事实当作已验证事实；需要 Codex / Human 实机确认时必须明确标记。

### Codex
- 本地执行与事实验收 Agent。
- 负责 Windows 实机运行、测试、构建、封装、日志、环境事实和明确授权范围内的最小阻塞修复。
- 不擅自重构、扩功能、替换架构或修改产品边界。

## 3. Baton Rule — Single Writer

任何时刻只有一个写入 Owner。

允许的 Baton：`HUMAN | SOL | CODEX | NONE`

典型流转：

`HUMAN -> SOL -> CODEX -> SOL -> HUMAN`

禁止 Sol 与 Codex 同时修改同一批源码。首次 accepted public push 后，GitHub repository 是 canonical source 与 Git history；Drive Relay surface 继续承担 Human / Sol / Codex coordination、Baton、short-lived session state 与 archival evidence mirror。两者都不是并行合并系统。

在 Relay environment 中，`SESSION_STATE.md` 是当前 Baton 与短期执行状态的权威来源；repository-only checkout 不依赖该文件。

## 4. Direction 与 Execution 分离

不得用一个 `ACTIVE` 同时表达“方向已批准”和“已经授权开工”。

里程碑使用两个维度：

- Direction: `APPROVED | PENDING | CONDITIONAL`
- Execution: `NOT_STARTED | IN_PROGRESS | BLOCKED | READY_FOR_REVIEW | ACCEPTED`

`Direction: APPROVED` 不等于可以修改源码。

是否允许实际执行，以 `PROJECT_STATE.md` 的 `Execution authorization` 和 Human 当前明确指令为准。

## 5. Product Boundary

产品长期定位、Fidelity Contract 与永久 Non-goals 只以 `PROJECT_CHARTER.md` 为准。

任何 Agent 不得因为竞品有、实现方便或“以后可能有用”而自行扩大 scope。

## 6. Code Change Rules

所有代码修改必须遵守 `CODE_CLEANLINESS_CONTRACT.md`。

默认优先顺序：

1. 复现并确认事实
2. 找根因
3. 删除错误路径 / 冗余状态
4. 增加回归测试
5. 实现最小修复
6. 最后才考虑新增抽象或依赖

不要用 timeout、retry、fallback、watchdog 或兼容层掩盖结构问题。

## 7. Durable State vs Session State

`PROJECT_STATE.md`：长期项目事实，只记录 baseline、当前 milestone、重大决定、授权状态和 accepted artifact。

`SESSION_STATE.md`：仅属于 Relay governance surface 的短生命周期工作检查点，只记录当前 Baton、当前任务、已完成、未完成、已验证/未验证、blocker、最后动作和下一唯一动作；它不是 public repository 的必需文件。

在 Relay environment 中，每次 Agent 结束、额度中断前、交接前或发生 blocker 时更新 `SESSION_STATE.md`。

## 8. Evidence Discipline

- Agent 执行事实、测试记录、打包记录放 `records/`。
- Human acceptance 与 Agent 自测结果不得混写成同一事实。
- `DONE` / `ACCEPTED` 必须有证据；没有证据不得宣称完成。
- accepted binary 必须有 SHA-256；public Git history 不存放二进制。未来公开 artifact 使用 GitHub Releases，Drive 可保留历史 archival copy。

## 9. Authorization Boundary

读取治理文件不等于授权开发。

没有 Human 明确授权当前执行阶段时，可以：
- 读取
- 总结
- 审计
- 提出方案

不得：
- 修改源码
- 运行新测试
- 重新打包
- 发布

## 10. Cold Session Acceptance Test

治理层必须能够通过以下测试：

只向全新 session 提供项目路径和“按 AGENTS 接手”，它应能准确恢复：
- 产品定位
- accepted baseline
- 当前 milestone
- Direction / Execution
- execution authorization
- durable authorization / governance state
- 最后验收事实
- 在 Relay environment 中：当前 Baton 与 blocker
- 在 Relay environment 中：下一唯一动作

如果还需要 Human 重述大量历史，治理视为未通过。
