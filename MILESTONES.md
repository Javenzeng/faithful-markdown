# MILESTONES.md — Faithful Markdown

## Status Model

每个 milestone 使用两个独立维度：

- Direction: `APPROVED | PENDING | CONDITIONAL`
- Execution: `NOT_STARTED | IN_PROGRESS | BLOCKED | READY_FOR_REVIEW | ACCEPTED`

`APPROVED` 只代表方向通过，不等于已经授权修改源码。实际 execution authorization 以 `PROJECT_STATE.md` 与 Human 当前明确指令为准。

---

## V2 — Editor Baseline

**Direction: APPROVED**
**Execution: ACCEPTED**

目标：从只读浏览器升级为轻量、离线、可编辑、可保存的 Windows Markdown Reader & Editor。

已完成：
- 打开 / 编辑 / 阅读模式
- 实时预览
- Save / Save As / shortcuts
- UTF-8 / UTF-8 BOM
- CRLF / LF 基础保留
- 相对图片处理
- 外链安全处理
- 无 CDN 渲染
- 未保存状态与关闭确认
- Windows EXE 封装
- 无参数启动 bridge 重入死锁根因修复
- Human 实机启动确认

V2 是历史 accepted Windows binary baseline。

---

## V2.1 — Content Fidelity Contract

**Direction: APPROVED**
**Execution: ACCEPTED**

目标：让“不会弄脏 Markdown 文件”成为可测试、可证明的内容保真契约。

Accepted scope：

1. **No-op Save**
   - 内容未变时不写磁盘
   - `Open -> Save` SHA-256 保持一致

2. **External Change Guard**
   - 保存前检查磁盘文件是否被外部修改
   - 检测到变化时禁止 silent overwrite

3. **Minimal Safe Save**
   - 需要写入时使用 same-directory temp + replace 路径
   - 写入失败明确失败
   - 不引入自研持久化框架

4. **Read-only Upfront**
   - 打开时识别明显只读 / 不可写状态

5. **File Facts**
   - encoding / BOM / EOL / Clean|Modified / Read Only

6. **Fidelity Test Corpus**
   - UTF-8、BOM、LF、CRLF、Unicode、emoji、mixed-EOL 等 fixture
   - mixed-EOL 在 V2.1 只承诺 no-op byte-identical

Acceptance:
- source tests: **24/24 PASS**
- Windows Real-Machine Acceptance: **H1–H7 PASS**
- P0 Cold Start/API Exposure Fix: **ACCEPTED**
- accepted source baseline: **YES**

### GitHub Initial Import

**Status: ACCEPTED / CLOSED — 2026-08-30**

Repository: `Javenzeng/faithful-markdown`
Default branch: `main`
Accepted root import commit:

`fab1072af42f78b758b425a61ce2173df39a79fd`

GitHub 已成为 canonical source + durable governance + Git history。

Fresh-session GitHub Capability Probe: **PASS**.

Evidence:
- `records/GitHub/GITHUB_INITIAL_IMPORT_ACCEPTANCE_AND_CAPABILITY_PROBE_2026-08-30.md`

**Next Gate: V2.2 Design / Evidence / Change Boundary Review**

---

## V2.2 — Filesystem Save Integrity

**Direction: APPROVED**
**Execution: ACCEPTED**
**Outcome: NO_CHANGE**

Windows local NTFS evidence 1–4 PASS。无 temp residue、target corruption 或 state corruption；无 runtime change justified。runtime LOC +0，dependency +0，state +0，abstraction +0；accepted source baseline remains V2.1 — Content Fidelity Contract。

Next Gate: **V2.3 — Fidelity Edge Cases: Scope / Test Matrix Review**

---

## V2.3 — Fidelity Edge Cases

**Direction: APPROVED**
**Execution: ACCEPTED**
**Outcome: TEST_ONLY**

fidelity test-only coverage added：mixed-EOL edited behavior follows current file-level EOL policy；final/no-final newline；CJK / emoji / decomposed combining sequences；empty / 1-char。runtime LOC +0，dependency +0，state +0，abstraction +0；no runtime defect found。accepted source baseline remains V2.1。

Next Gate: **V2.4 — External State Integrity: Scope / Evidence Review**

---

## V2.4 — External State Integrity

**Direction: APPROVED**
**Execution: ACCEPTED**
**Outcome: TEST_ONLY**

current-path deleted before Save invariant covered：Save 明确失败，`_safe_write` 不进入，原 path 不被重建，baseline fingerprints 不推进，pending edited content 可通过 explicit Save As 恢复。

fidelity 18/18 PASS；broader suite 29/29 PASS。runtime LOC +0，dependency +0，state +0，abstraction +0；no runtime defect found。accepted source baseline remains V2.1。

Next Gate: **V2.5 — Large-File Discipline: Entry Criteria / Evidence Review**

---

## V2.5 — Large-File Discipline

**Direction: CONDITIONAL**
**Execution: NOT_STARTED**

**Entry Criteria Decision: `DEFER / NOT_ACTIVATED` — 2026-08-30**

无真实证据触发 activation；runtime / test / benchmark changes: NONE。仅在未来真实证据出现时重新评估。

仅在真实用户或测试证明大文件成为问题时启动。

目标不是追求夸张文件大小，而是建立明确性能边界与必要降级策略。

不得提前为想象中的大文件需求增加复杂度。

---

## V2.6 — Reproducible Release

**Direction: APPROVED**
**Execution: ACCEPTED**

- Windows release build: PASS
- Full unittest: 29/29 PASS
- Human Smoke: PASS
- Release source commit: `cb6c3a62f5cf8eeb2ec21d1530123cd18f4bc4a6`
- Artifact SHA-256: `F2E15FC962B2765F7957349593045B907BD0F2AE35E3E772956DD9E8BCF74605`
- GitHub Release: `v2.6`
- Auditable release achieved; no bit-for-bit reproducibility claim.

Next Gate: Operational use / evidence collection. No active implementation milestone. V2.5 or V3 may be reconsidered only when real evidence triggers them.

目标：提高 release 可验证性与开源可信度。

包括：
- source commit <-> release artifact 对应
- dependency lock / build provenance
- release SHA-256
- Fidelity Test result
- 可重复或至少可审计的 Windows 构建流程

正式 GitHub Release 应以这一阶段的可审计产物为基础。

---

## V2.7 — Windows App Identity

**Direction: APPROVED**
**Execution: ACCEPTED**

- product display name: Faithful Markdown
- EXE: `FaithfulMarkdown.exe`
- window / EXE / taskbar identity unified
- `.md/.markdown` per-user Windows registration
- no silent default-app takeover
- default-handler guard uses Windows Shell association resolution
- Register / guard / unregister Windows evidence PASS
- 29/29 tests PASS
- release source commit: `5e1644d6a661c3a07f8c49787ae6fd1c1342402c`
- artifact SHA-256: `9846C856267D15EB350211BB1B0AE2640322430AE0E61640DAEDB8F0829D044E`
- GitHub Release: `v2.7`
- accepted source baseline remains V2.1

Next Gate: Operational use / evidence collection. No active implementation milestone. Do not start V2.8 or V3。

---

## V3 — Architecture Reduction

**Direction: CONDITIONAL**
**Execution: NOT_STARTED**

V3 不是功能升级。

只有当前 Python + pywebview 架构被真实证据证明为主要负担时，才评估原生重写。

进入条件至少满足一项：
- bridge 生命周期成为持续结构性故障源
- 打包 / 依赖成为显著维护负担
- EXE 体积或启动性能成为实际采用障碍
- 原生实现能够明显减少代码、依赖和故障面

成功标准：

> **同样的产品能力，用更少、更清晰、更可靠的实现完成。**
