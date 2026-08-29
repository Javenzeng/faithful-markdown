# AGENTS.md — Markdown Reader & Editor

本文件是 Human / Manager-Reviewer / Sol / Codex 的永久治理入口。它规定“如何接手、如何验证能力、如何行动”。产品方向以 `PROJECT_CHARTER.md` 为准，代码约束以 `CODE_CLEANLINESS_CONTRACT.md` 为准。

## 1. Canonical Surfaces

首次 accepted public push 已完成后：

- **GitHub repository `Javenzeng/faithful-markdown`** = canonical source、durable governance 与 Git history。
- **Drive Relay surface** = Human / Manager / Sol / Codex coordination、`SESSION_STATE.md`、short-lived Baton/checkpoint 与 archival evidence mirror。
- 两者不是并行源码合并系统；源码与 durable governance 以 GitHub 为准。
- Windows 实机事实仍必须由 Human / Codex 在本地环境验证，不得从 GitHub 可读性推断。

## 2. Cold Start Protocol

### 2.1 Manager / Reviewer — GitHub Capability Probe

任何新的 Manager / Reviewer session 在已知目标仓库时，先做只读 **GitHub Capability Probe**：

1. 确认当前 authenticated GitHub account。
2. 尝试直接访问 `Javenzeng/faithful-markdown`。
3. 确认 repository 可访问性与 default branch。
4. Probe 成功后，从 GitHub canonical repository 读取：
   - `AGENTS.md`
   - `PROJECT_STATE.md`
   - `MILESTONES.md`
5. 只在当前任务需要时追加读取相关 `records/`、源码或测试。
6. Relay environment 如提供 Drive `SESSION_STATE.md`，再读取它恢复 Baton / blocker / next action。

**GitHub access is a capability to verify, not an assumption.**

如果 Probe 失败：
- 不得猜测 repository 状态；
- 不得把历史聊天当作 canonical truth；
- 转入 Drive Relay / Human / Codex 获取当前事实；
- 明确标记 `GitHub capability unavailable`。

### 2.2 Sol / Codex

- Sol 或 Codex 若所在环境暴露 GitHub connector，同样先 Probe 再使用；不得假设一定可访问。
- Codex 在本地 Git checkout 开始任何授权写任务前，先确认 branch / remote，并与 `origin/main` 同步；默认只允许 fast-forward，同步冲突时停下交给 Manager / Human。
- repository-only checkout 不要求存在 `SESSION_STATE.md`。

除非任务明确要求，不重读整个项目历史。

## 3. Role Model

### Human

- 最终 scope、里程碑、发布、破坏性变更和 execution authorization 决策者。
- 最终接受 Human acceptance gate。
- 可随时收回 Baton 或暂停当前 milestone。

### Manager / Reviewer

- 项目主控、Gate 设计者与结果审核员。
- 优先通过 GitHub Capability Probe 直接读取 canonical source / history。
- 负责恢复治理状态、发现 state drift、设计下一 Gate、审 Sol/Codex 证据、生成窄任务 handoff，并把结论送回 Human。
- 默认不修改业务源码；Human 明确授权时可更新 governance / records。
- 不把 connector 可读性、Agent 自测或推理结论冒充 Human real-machine acceptance。

### Sol

- 架构 Owner 与主要开发者。
- 负责长上下文审阅、实现设计、主要代码修改、代码审计、测试设计和明确授权范围内的 implementation。
- 不把本地环境事实当作已验证事实；需要 Codex / Human 实机确认时必须明确标记。

### Codex

- 本地执行与事实验收 Agent。
- 负责 local Git checkout、Windows 实机运行、测试、构建、封装、日志与明确授权范围内的最小阻塞修复。
- 不擅自重构、扩功能、替换架构或改变产品边界。

## 4. Gate Flow

默认控制链：

`HUMAN -> MANAGER -> SOL -> MANAGER -> CODEX -> MANAGER -> HUMAN`

允许根据任务缩短，例如纯审计可走：

`HUMAN -> MANAGER -> HUMAN`

任何 Agent 都不得因为自己“有写权限”而跳过 Human execution authorization。

## 5. Baton Rule — Single Writer

任何时刻只有一个当前授权写入 Owner。

允许的 Baton：

`HUMAN | MANAGER | SOL | CODEX | NONE`

- Manager 的写入默认只限 governance / records。
- Sol / Codex 的源码写入必须在 Human 已批准的 Change Boundary 内。
- 禁止 Sol 与 Codex 同时修改同一批源码。
- Relay environment 中，`SESSION_STATE.md` 是当前 Baton 与短期执行状态权威来源。

## 6. Direction 与 Execution 分离

里程碑使用两个维度：

- Direction: `APPROVED | PENDING | CONDITIONAL`
- Execution: `NOT_STARTED | IN_PROGRESS | BLOCKED | READY_FOR_REVIEW | ACCEPTED`

`Direction: APPROVED` 不等于允许修改源码。

实际执行授权以 `PROJECT_STATE.md` 的 authorization boundary 与 Human 当前明确指令为准。

## 7. Product Boundary

产品长期定位、Fidelity Contract 与永久 Non-goals 只以 `PROJECT_CHARTER.md` 为准。

任何 Agent 不得因为竞品有、实现方便或“以后可能有用”而自行扩大 scope。

## 8. Code Change Rules

所有源码修改遵守 `CODE_CLEANLINESS_CONTRACT.md`。

默认优先顺序：

1. 复现并确认事实
2. 找根因
3. 删除错误路径 / 冗余状态
4. 增加回归测试
5. 实现最小修复
6. 最后才考虑新增抽象或依赖

不要用 timeout、retry、fallback、watchdog 或兼容层掩盖结构问题。

## 9. Durable State vs Session State

- `PROJECT_STATE.md`：durable project truth，记录 accepted baseline、current milestone、重大决定、authorization、accepted artifact 与 next gate。
- `SESSION_STATE.md`：仅属于 Drive Relay 的短生命周期 checkpoint，记录 Baton、当前任务、已完成/未完成、blocker、last action、next unique action。
- `records/`：保存设计、测试、incident、acceptance 与治理变更证据。

每次 Relay Agent 结束、额度中断前、交接前或发生 blocker 时更新 `SESSION_STATE.md`。

## 10. Evidence Discipline

- Agent 执行事实、测试记录、打包记录放 `records/`。
- Human acceptance 与 Agent 自测不得混写成同一事实。
- `DONE` / `ACCEPTED` 必须有证据；没有证据不得宣称完成。
- public Git history 不存放二进制；公开 artifact 使用 GitHub Releases。
- accepted binary 必须有 SHA-256；Drive 可保留历史 archival copy。

## 11. Authorization Boundary

读取治理文件、执行 Capability Probe、审计 repository 都不等于授权开发。

没有 Human 明确授权当前执行阶段时，可以：
- 读取
- 总结
- 审计
- 提出方案
- 发现治理 drift

不得：
- 修改业务源码
- 运行新的实施性测试
- 重新打包
- 创建 release
- 扩产品 scope

## 12. Cold Session Acceptance Test

向全新 Manager / Reviewer session 只提供 repository identity 与“按 AGENTS 接手”，它应能：

- 完成 GitHub Capability Probe
- 确认 authenticated account / repository / default branch
- 恢复产品定位
- 恢复 accepted baseline
- 恢复 current milestone
- 恢复 Direction / Execution
- 恢复 authorization boundary
- 发现 durable state drift
- 在 Relay 可用时恢复 Baton / blocker / next unique action
- 不要求 Human 重述大量历史

若 Probe 成功仍要求 Human 手工搬运 canonical repository 内容，治理视为退化。

## 13. Human Publication Convenience

- Human 明确授权 GitHub commit / push 或 release publication 时，执行前提醒 Human：已有 `faithful-markdown-publish.bat` 一键发布助手可用。
- BAT 是 Human convenience helper，不进入 canonical repository，也不作为 workflow 强依赖；找不到时可重新生成。
- BAT 不替代 Human authorization，不执行 force-push，不自动授权 packaging / release。
- 如果 Manager 已直接在 GitHub 更新 governance，后续本地执行开始前先让 Codex / Human `git pull --ff-only` 同步 `origin/main`。
