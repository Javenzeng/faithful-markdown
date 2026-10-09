# PROJECT_CHARTER.md — Long-Term Product Goal

## 1. Mission

Markdown Reader & Editor 的长期目标不是成为功能最多的 Markdown 编辑器，而是成为一个用户可以放心对项目 Markdown 执行快速阅读与小范围修订的 Windows 工具。

核心表达：

> **A Markdown editor that changes only what you changed.**

这是一条产品原则，不应被解释成对所有文件系统元数据的无限承诺。

## 2. V2.1 Content Fidelity Contract

V2.1 将以下三条建设为可测试、可证明的内容保真契约：

1. **No change means no write.**
   - 用户内容未发生变化时，不进行磁盘写入。
   - `Open -> Save` 后原文件 SHA-256 必须保持一致。

2. **External changes are never silently overwritten.**
   - 文件在应用打开后被其他程序、Agent、同步工具或编辑器修改时，保存必须阻止静默覆盖。

3. **Saving should not create unrelated content churn.**
   - 用户进行正常小范围编辑时，不得额外制造编码、UTF-8 BOM、文件级 EOL 或整文件无意义 diff。

### Contract Boundary

V2.1 的 Fidelity Contract 主要针对 Markdown 内容及已声明的编码/BOM/EOL 行为。

以下属于后续 Filesystem Fidelity 研究范围，不在 V2.1 作绝对保证：
- ACL / DACL
- creation / modification metadata
- Windows file attributes
- Alternate Data Streams
- compression / encryption metadata
- symlink / junction 语义
- 网络盘 / 同步盘的底层替换语义

这些只有在真实测试与需求证据出现后，才进入 V2.2 及后续里程碑。

## 3. Target Users

优先用户：
- 开发者
- Git 仓库维护者
- AI coding / agent workflow 用户
- README / AGENTS / PROJECT_STATE / SESSION_STATE 等项目 Markdown 的维护者
- 需要快速阅读并偶尔修订 Markdown 的 Windows 用户

本项目不是长篇写作平台，也不是知识管理工具。

## 4. Product Principles

### 4.1 Stable workflow, evidence-led improvements
核心用户流程保持稳定：

`Open -> Review -> Fix -> Save -> Close`

允许补齐该流程中的实际功能缺口。高频反馈、重复反馈或明确的使用障碍是评估依据，不自动构成开发授权；单个明确缺口也可进入评估，不要求先收集大量反馈。

新增功能必须同时满足：
- 直接帮助用户阅读、定位问题或进行小范围修订。
- 有真实使用反馈或可说明的核心流程缺口。
- 用最小完整实现解决，维护成本与预期使用收益相称。
- 保持文件保真、操作明确和轻量本地使用。

Human 按具体功能批准范围；一次批准不授权相邻功能或持续扩展。搜索、可调整分栏和当前文档标题目录属于已批准的阅读与校对增强；行号仍暂缓，不因本宪章升级自动进入开发。

版本以用户完成核心任务的改善和工程质量为依据，不以功能数量为目标。验收关注用户是否更容易读懂、找到并修订问题，同时确认文件保真行为没有退化。

### 4.2 Useful and trustworthy
实用性不可或缺；功能增加不得牺牲用户对已有文件的信任。产品的独特价值是：放心打开已有 Markdown，快速找到并修改问题，保存时只改变自己改过的内容。

优先提高：
- 文件保真
- 保存可靠性
- 并发保护
- 确定性
- 可审计性
- 可测试性

### 4.3 Small behavior surface
长期保持：
- 无后台常驻服务
- 无云账户
- 无索引器
- 无插件生命周期
- 无遥测依赖
- 无不必要文件 watcher
- 无大规模兼容矩阵

### 4.4 Small auditable codebase
理想长期状态：
- 运行时代码尽量少
- 测试覆盖持续增加
- 重复逻辑持续减少
- 错误路径持续删除
- 任何复杂度都有真实故障或需求证据

代码量是维护成本的信号，不是功能价值的唯一标准。允许为明确收益增加必要代码；优先复用现有实现，不为未来假设增加状态、依赖或抽象。验证随实际风险安排，不以测试数量增长为目标。

## 5. Long-Term Optimization Axes

未来改进沿以下方向推进；新增功能仍须满足 4.1 的准入条件：

1. Fidelity — 文件内容保真
2. Reliability — 写入与生命周期可靠性
3. Determinism — 相同输入得到确定行为
4. Performance — 启动、渲染、保存效率
5. Auditability — 源码、依赖、构建、release 可验证
6. Code Reduction — 用更少代码维持或提高同等能力
7. Usability — 减少核心阅读、定位与小范围修订中的实际障碍

## 6. Permanent Non-Goals

以下能力原则上不进入产品路线：
- 多标签
- Workspace / 文件树
- Git 客户端或复杂 Git 集成
- AI 功能
- 云同步
- 插件系统
- 知识库
- WYSIWYG
- Mermaid
- LaTeX
- PDF / Office 导出功能竞赛
- 复杂主题系统
- legacy OS compatibility

若未来确有真实需求，必须先由 Human 明确修改本宪章，而不是在实现阶段顺手加入。

## 7. V3 Rule

允许存在 V3，但 V3 不等于“更多功能”。

只有真实证据证明当前 Python + pywebview 架构成为主要瓶颈时，才允许评估原生重写，例如：
- 体积成为实际采用障碍
- bridge 生命周期持续产生结构性故障
- 打包维护成本持续过高
- 原生实现可同时减少代码、依赖与故障面

重写必须满足：

> **新实现比旧实现更少、更清晰、更可靠。**

否则不重写。
