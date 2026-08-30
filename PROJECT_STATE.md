# PROJECT_STATE.md

## Current Baseline

Project: Markdown Reader & Editor
Repository: `Javenzeng/faithful-markdown`
Default branch: `main`
Canonical source + durable governance: GitHub
Accepted source baseline: **V2.1 — Content Fidelity Contract**
Current milestone: **None — operational use / evidence collection**
V2.6 Direction: `APPROVED`
V2.6 Execution: `ACCEPTED`
Latest accepted release source commit: `cb6c3a62f5cf8eeb2ec21d1530123cd18f4bc4a6`
Latest accepted public release: `v2.6`
Artifact SHA-256: `F2E15FC962B2765F7957349593045B907BD0F2AE35E3E772956DD9E8BCF74605`
Current owner: Human
Baton: `HUMAN`
Blocker: `None`
Packaging: `COMPLETED`

## Last Accepted Fact

2026-08-30：V2.6 — Reproducible Release **ACCEPTED**。

GitHub Release `v2.6` published from source commit `cb6c3a62f5cf8eeb2ec21d1530123cd18f4bc4a6`；EXE SHA-256 为 `F2E15FC962B2765F7957349593045B907BD0F2AE35E3E772956DD9E8BCF74605`。29/29 tests、packaged cold start、icon、Human Smoke 与远端 artifact hash verification 均 PASS。V2.5 remains `DEFER / NOT_ACTIVATED`；V3 remains `CONDITIONAL / NOT_STARTED`。

无真实大文件缺陷、性能、hang 或 crash 证据；long-single-line DEFER。benchmark +0，test +0，runtime +0，dependency +0，state +0，abstraction +0。V2.5 remains `CONDITIONAL / NOT_STARTED`，source authorization remains `NOT_GRANTED`。V2.5 was not executed or accepted；仅在未来真实证据触发时重新评估。accepted source baseline 仍为 V2.1 — Content Fidelity Contract。

After this accepted public push:
- GitHub = canonical source + durable governance + Git history.
- Drive Relay = `SESSION_STATE.md`, Baton / short-lived coordination, archival evidence mirror.
- public binaries belong in GitHub Releases, not Git history.

Acceptance / capability evidence:
- `records/GitHub/GITHUB_INITIAL_IMPORT_ACCEPTANCE_AND_CAPABILITY_PROBE_2026-08-30.md`

## GitHub Capability Probe

Status: **PASS**

2026-08-30 已完成两层验证：

1. 当前 Manager session 能确认 authenticated GitHub account `Javenzeng`，并直接访问 `Javenzeng/faithful-markdown`。
2. Human 在一个全新 ChatGPT session 中只提供 repository identity 与 Capability Probe 指令；该 session 无聊天历史仍成功：
   - 识别 authenticated account `Javenzeng`
   - 直接读取 repository / default branch
   - 读取 `AGENTS.md` / `PROJECT_STATE.md` / `MILESTONES.md`
   - 恢复 accepted V2.1 baseline / Baton / packaging state
   - 主动发现旧 `PROJECT_STATE.md` 与真实 GitHub 状态的 drift
   - 保持只读并停在 Human Gate

治理结论：

> **GitHub access is a capability to verify, not an assumption.**

新的 Manager / Reviewer session 应先执行 GitHub Capability Probe；Probe 成功则直接从 GitHub canonical repository 接手，失败才转 Drive Relay。

## Manager / Reviewer Governance Upgrade

Status: **ENABLED**

Human 于 2026-08-30 授权完成治理升级。

角色：
- Human：最终 scope / milestone / release / destructive change / execution authority。
- Manager / Reviewer：主控、GitHub canonical reader、Gate designer、结果审核员；默认不改业务源码。
- Sol：架构与授权范围内的主要 implementation。
- Codex：local Git / Windows factual execution、tests、build、package。
- Drive Relay：Baton / `SESSION_STATE.md` / short-lived coordination。

默认 Gate flow：

`HUMAN -> MANAGER -> SOL -> MANAGER -> CODEX -> MANAGER -> HUMAN`

## Accepted V2 Artifact

Canonical archival path:

`releases/V2/accepted/Markdown_Reader_Editor.exe`

Recorded SHA-256:

`E706126BA63F9FD7486430EF1227721FBB58A0725CF53497573CC9FADAECBF1E`

该产物是 V2 accepted Windows baseline，不因后续开发或打包自动覆盖；public Git history 不包含该 EXE。

## V2.1 Accepted Source Baseline

V2.1 Execution: `ACCEPTED`
Windows Real-Machine Acceptance: `PASS`
P0 Cold Start/API Exposure Fix: `ACCEPTED`

Accepted scope:
1. No-op Save
2. External Change Guard
3. Minimal Safe Save
4. Read-only Upfront
5. File Facts
6. Fidelity Test Corpus

Final source test evidence:
- baseline 8/8 PASS
- fidelity 13/13 PASS
- P0 regression 3/3 PASS
- total 24/24 PASS

Human Windows acceptance:
- H1 Cold Start 5/5 PASS
- H2 File Facts + Edit/Save PASS
- H3 No-op Save PASS
- H4 External Change Guard PASS
- H5 Windows Read-only + Save As PASS
- H6 UTF-8 BOM + CRLF PASS
- H7 Dirty Close PASS

Evidence:
- `records/V2.1/V2_1_HUMAN_WINDOWS_ACCEPTANCE_2026-08-29.md`
- `records/V2.1/V2_1_IMPLEMENTATION_RECORD_2026-08-29.md`
- `records/V2.1/V2_1_P0_COLD_START_FIX_2026-08-29.md`

## Active Decisions

- 产品长期定位以 `PROJECT_CHARTER.md` 为唯一权威来源。
- Single Writer Baton Rule 生效。
- GitHub 已是 canonical source + durable governance + Git history。
- Drive Relay 不再作为 canonical Git source；仍是 active coordination / session state / archival plane。
- Agent/session 不得假设 GitHub connector 一定可用，必须 Probe。
- Manager / Reviewer 默认不改业务源码。
- Windows runtime / filesystem facts 仍必须由 Human / Codex 本地验证。
- public Git history 不存放二进制。

## Current Authorization Boundary

No active implementation authorization.

V2.5 remains `DEFER / NOT_ACTIVATED`。V3 remains `CONDITIONAL / NOT_STARTED`。Future source changes require a new Human authorization based on real evidence。

## Next Gate

Operational use / evidence collection。No active implementation milestone。V2.5 or V3 may be reconsidered only when real evidence triggers them。

Baton: `HUMAN`
