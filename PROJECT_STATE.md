# PROJECT_STATE.md

## Current Baseline

Project: Markdown Reader & Editor  
Accepted source baseline: V2.1  
Current milestone: V2.1 — Content Fidelity Contract  
Direction: APPROVED  
Execution: ACCEPTED  
Source implementation authorization: GRANTED  
Current owner: Human  
Baton: HUMAN

## Last Accepted Fact

2026-08-29：Human 完成 V2.1 Windows Real-Machine Acceptance，H1–H7 全部 PASS。V2.1 正式成为 accepted source baseline；P0 Cold Start/API Exposure Fix 同时 ACCEPTED。

Human acceptance evidence：`records/V2.1/V2_1_HUMAN_WINDOWS_ACCEPTANCE_2026-08-29.md`。

历史 V2 证据仍归档于 `records/V2/`。

## Accepted V2 Artifact

Canonical path:

`releases/V2/accepted/Markdown_Reader_Editor.exe`

Recorded SHA-256:

`E706126BA63F9FD7486430EF1227721FBB58A0725CF53497573CC9FADAECBF1E`

该产物是 V2 accepted Windows baseline，不因后续开发或打包自动覆盖。

## Cold Session Continuity Gate

Status: PASS (Human confirmed 2026-08-29)

The governance cold-session test successfully restored product positioning, accepted baseline, milestone, authorization, Baton, debt, and next action from canonical files. Human then authorized **V2.1 — Minimal Implementation Design & Change Boundary Review** only.

Design artifact:

`records/V2.1/V2_1_MINIMAL_IMPLEMENTATION_DESIGN_2026-08-29.md`

Design status: `APPROVED_WITH_AMENDMENTS / READY_FOR_IMPLEMENTATION_AUTHORIZATION`

Human Design Review result: `APPROVED_WITH_AMENDMENTS`. The approved amendments are now incorporated into the design artifact.

Human authorized V2.1 source implementation and direct unit-test execution within the approved Change Boundary. SOL has completed that implementation pass and returned the Baton for Human review. Build-script changes, packaging, and release remain unauthorized.

## Governance & Repository Hygiene Pass

Status: COMPLETE

已完成治理决策：
- 新增 `SESSION_STATE.md`，把短期执行检查点与长期项目事实分离。
- 里程碑状态拆为 Direction / Execution，消除 `ACTIVE` 与“未授权开工”的歧义。
- 统一新 session 的读取协议。
- Fidelity Contract 明确拆分 Content Fidelity 与后续 Filesystem Fidelity。
- V2.1 / V2.2 / V2.3 的 Safe Save 与 mixed-EOL 边界已切清。
- V2 accepted binary 使用独立 release 路径。
- 历史测试 / acceptance / handoff 证据使用 `records/` 归档。
- ephemeral build state 不属于 canonical project content。

## Active Decisions

- 产品长期定位以 `PROJECT_CHARTER.md` 为唯一权威来源。
- V2.1 方向与批准后的 Change Boundary 已通过；Human 已授权在该边界内实施源码与单元测试。
- V2.1 只强化 Content Fidelity Contract，不扩功能型 scope。
- 代码洁癖契约对 Sol / Codex 均生效。
- Single Writer Baton Rule 生效。首次 accepted public push 后，GitHub repository 成为 canonical source + Git history；Drive Relay surface 继续承担 Human / Sol / Codex coordination、Baton、short-lived session state 与 archival evidence mirror。
- 后续交接描述 required capabilities，不绑定某台机器的固定 Python 路径、启动器或目录布局。
- 当前 `build_windows.ps1` 会重新制造 `.venv/build/dist/.spec`；这是已知 build-hygiene debt，下次打包前再单独处理。

## V2.1 Approved Scope

1. No-op Save
2. External Change Guard
3. Minimal Safe Save
4. Read-only Upfront
5. File Facts
6. Fidelity Test Corpus

## V2.1 Source Implementation

Status: `ACCEPTED`

SOL implementation evidence:
- `records/V2.1/V2_1_IMPLEMENTATION_RECORD_2026-08-29.md`
- `records/V2.1/V2_1_UNIT_TEST_RESULT_2026-08-29.txt`

Verified implementation facts:
- `core.py` and `assets/index.html` changed only within the approved boundary.
- `tests/test_fidelity.py` and seven raw-byte fixtures added.
- canonical `tests/__pycache__/` deleted.
- direct unit tests: `21/21 PASS` (8 existing + 13 V2.1).
- new runtime dependencies: 0.
- new bridge APIs: 0.
- `app.py` diff: 0.
- packaging/build script: not run.

Execution: `ACCEPTED`.  
Source implementation authorization: `GRANTED` for the completed approved pass.  
Windows real-machine acceptance: `PASS`.  
Baton: `HUMAN`.

## V2.1 Windows Real-Machine Acceptance

Status: `PASS`

Human final acceptance (2026-08-29):
- H1 Cold Start Retest: **PASS 5/5** — five consecutive source launches started, responded, and closed normally; no `(未响应)`, `AccessibilityObject...`, or `maximum recursion depth exceeded`.
- H2 File Facts + Edit/Save: **PASS** — Windows NTFS UTF-8/LF file showed `UTF-8 | LF`; edit + Ctrl+S succeeded and disk readback confirmed the write.
- H3 No-op Save: **PASS** — unchanged Ctrl+S preserved both SHA-256 and LastWriteTime exactly; **No change means no write.**
- H4 External Change Guard: **PASS** — local unsaved edit plus external PowerShell modification caused Ctrl+S to be blocked with the explicit external-change message; external bytes remained intact and UI stayed responsive.
- H5 Windows Read-only + Save As: **PASS** — `attrib +R` file opened as `Read Only`, editing was blocked, Save As remained available, omitted extension became `.md`, new copy was writable, original retained Windows R attribute.
- H6 UTF-8 BOM + CRLF: **PASS** — after edit/save, UI still showed `UTF-8 BOM | CRLF`; raw BOM remained `EF-BB-BF` and EOL remained `0D-0A`.
- H7 Dirty Close / Lifecycle: **PASS** — dirty state and native unsaved confirmation behaved correctly; Cancel preserved the window/content; discard confirmation exited normally; no hang or bridge deadlock.

P0 Cold Start/API Exposure Fix: `ACCEPTED`.

Acceptance evidence:
- `records/V2.1/V2_1_HUMAN_WINDOWS_ACCEPTANCE_2026-08-29.md`
- `records/V2.1/V2_1_P0_COLD_START_FIX_2026-08-29.md`
- `records/V2.1/V2_1_P0_UNIT_TEST_RESULT_2026-08-29.txt`

V2.1 Execution: `ACCEPTED`.  
Baton: `HUMAN`.  
Blocker: `None`.  
Packaging: `NOT_AUTHORIZED`.

## Current Authorization Boundary

V2.1 is accepted as the current source baseline. This acceptance does not authorize packaging, build-script changes, release creation, or product-scope expansion.

Still NOT authorized:
- source modification outside a new Human-approved task
- `build_windows.ps1`
- packaging / release
- product scope changes

## GitHub Initial Import Transition

Repository: `faithful-markdown`  
License: `MIT`  
Accepted source baseline: `V2.1`

Publication preflight: `APPROVED_BY_HUMAN`.

The local initial import is being prepared from the byte-verified accepted V2.1 Drive baseline.

Current transition facts:
- non-synced Windows working tree: prepared outside Drive
- baseline import inventory before publication edits: `33/33` files matched
- baseline byte-integrity gate: `PASS`
- public `README.md` transformation: completed
- public `AGENTS.md` dual-plane governance transformation: completed
- Git repository initialization: not yet performed
- GitHub remote repository: not yet created
- push: `NOT_AUTHORIZED`
- packaging: `NOT_AUTHORIZED`

Current blocker: `None`.

### Canonical transition rule

Until the first accepted public push is completed and read back:
- the accepted Drive V2.1 source baseline remains the provenance anchor for this initial import.

After the first accepted public push:
- **GitHub repository** = canonical source + Git history.
- **Drive Relay governance surface** = Human / Sol / Codex coordination, Baton, short-lived `SESSION_STATE.md`, and archival evidence mirror.
- Drive remains an active governance plane; it is not the canonical Git source and is not a discarded backup.
- public binaries belong in GitHub Releases rather than Git history.

Baton: `HUMAN`

## Canonical Governance

Repository-only cold start:
1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `MILESTONES.md`
4. current-task-relevant `records/`

Human / Sol / Codex Relay environment:
- additionally read external `SESSION_STATE.md` when available.

修改源码：再读 `CODE_CLEANLINESS_CONTRACT.md`。

改变 scope / 长期方向：再读 `PROJECT_CHARTER.md`。