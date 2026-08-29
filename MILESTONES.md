# MILESTONES.md — Markdown Reader & Editor

## Status Model

每个里程碑使用两个独立维度：

- Direction: `APPROVED | PENDING | CONDITIONAL`
- Execution: `NOT_STARTED | IN_PROGRESS | BLOCKED | READY_FOR_REVIEW | ACCEPTED`

`APPROVED` 只代表方向通过，不代表已经授权修改源码。实际执行授权以 `PROJECT_STATE.md` 与 Human 当前明确指令为准。

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
- Human 实机启动确认：最终 EXE 未再发生启动锁死

V2 是后续版本的 accepted Windows baseline。

---

## V2.1 — Content Fidelity Contract

**Direction: APPROVED**  
**Execution: ACCEPTED**

目标：让“不会弄脏 Markdown 文件”从工程倾向变成可测试、可证明的内容保真契约。

范围只包含：

1. **No-op Save**
   - 内容未变时不写磁盘
   - `Open -> Save` SHA-256 保持一致

2. **External Change Guard**
   - 保存前检查磁盘文件是否已被外部修改
   - 检测到变化时禁止 silent overwrite
   - 优先单一 authoritative fingerprint，避免增加同步状态源

3. **Minimal Safe Save**
   - 确实需要写入时，不采用容易留下截断原文件的粗暴路径
   - 写入失败必须明确失败，不假装成功
   - 不引入自研持久化框架
   - V2.1 不研究完整 Windows filesystem metadata fidelity；深层 replace / fsync / ACL 语义留给 V2.2

4. **Read-only Upfront**
   - 打开时即识别明显只读 / 不可写状态
   - 不允许用户编辑很久后才发现无法保存

5. **File Facts**
   - 状态栏只显示必要、可验证的文件事实：encoding / BOM / EOL / Clean|Modified / Read Only 等

6. **Fidelity Test Corpus**
   - UTF-8、BOM、LF、CRLF、尾部换行、Unicode、emoji、mixed-EOL 等 fixture
   - No-op、small-edit、external-change 形成回归测试
   - mixed-EOL 在 V2.1 只承诺 **no-op save byte-identical**；编辑后的逐处 mixed-EOL 保留不在本里程碑承诺

### Windows Real-Machine Acceptance Status

- Unit-level source implementation: **PASS**.
- Windows Real-Machine Acceptance: **PASS**.
- H1 Cold Start Retest: **PASS 5/5**.
- H2 File Facts + Edit/Save: **PASS**.
- H3 No-op Save: **PASS** — unchanged save preserved SHA-256 and LastWriteTime.
- H4 External Change Guard: **PASS**.
- H5 Windows Read-only + Save As: **PASS**.
- H6 UTF-8 BOM + CRLF: **PASS**.
- H7 Dirty Close / Lifecycle: **PASS**.
- P0 Cold Start/API Exposure Fix: **ACCEPTED**.
- V2.1 accepted source baseline: **YES**.
- Blocker: **None**.
- Packaging: **NOT_AUTHORIZED**.
- Next Gate: **GitHub Repository Initialization**.

### V2.1 Acceptance Gate

必须证明：
- No-op save 不改变 SHA-256
- 外部修改不会被静默覆盖
- UTF-8/BOM/文件级 EOL 现有保证不退化
- Minimal Safe Save 不引入明显临时残留或无意义内容 churn
- 只读行为明确
- 核心行为有自动回归测试
- 不新增大型运行时依赖
- 不新增后台 watcher / daemon
- 不新增产品功能型 UI
- 运行时代码增长必须有测试与不变量证明其必要性

---

## V2.2 — Filesystem Save Integrity

**Direction: PENDING**  
**Execution: NOT_STARTED**

目标：在不增加用户功能的前提下，研究并强化 Windows 文件系统层保存可靠性。

候选研究项：
- flush / fsync / replace 语义
- Windows 文件属性与 ACL 保留
- file lock
- 保存过程中权限变化
- 同步盘与网络盘边界
- 删除 / 替换 race
- safe failure semantics
- metadata / Alternate Data Streams 等是否需要保证

原则：只有真实测试、故障或采用需求支持的项才进入实现。

---

## V2.3 — Fidelity Edge Cases

**Direction: PENDING**  
**Execution: NOT_STARTED**

目标：主要扩测试矩阵，少量修复真实边缘问题。

重点覆盖：
- mixed-EOL **发生编辑后的**行为
- final / no-final newline
- CJK / emoji / combining characters
- 空文件 / 极短文件
- 超长单行
- 中文与特殊字符路径
- 深层路径
- 相对图片路径边界

理想演进比例：测试代码增长显著高于运行时代码增长。

---

## V2.4 — External State Integrity

**Direction: PENDING**  
**Execution: NOT_STARTED**

目标：强化 Agent / IDE / sync 工具并发环境下的确定行为。

覆盖：
- 文件被其他程序保存
- 文件被删除
- 文件被移动 / 替换
- 权限发生变化
- 同步盘替换文件

原则：不引入长期后台 watcher；优先在打开、保存等必要操作节点核验事实。

---

## V2.5 — Large-File Discipline

**Direction: CONDITIONAL**  
**Execution: NOT_STARTED**

仅在真实用户或测试证明大文件成为问题时启动。

目标不是追求夸张文件大小，而是建立明确性能边界与必要降级策略。

不得提前为想象中的大文件需求增加复杂度。

---

## V2.6 — Reproducible Release

**Direction: PENDING**  
**Execution: NOT_STARTED**

目标：提高 release 可验证性与开源可信度。

包括：
- source commit <-> release artifact 对应
- dependency lock / build provenance
- release SHA-256
- Fidelity Test result
- 可重复或至少可审计的 Windows 构建流程

正式 GitHub release 与 OpenAI 开源支持申请应以这一阶段的可审计产物为基础。

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
