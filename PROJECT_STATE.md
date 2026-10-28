# Current state — 2026-10-28

## 版本与事实

- 产品：Faithful Markdown；RELEASED；GitHub Javenzeng/faithful-markdown，main。
- 最新发布：v2.12，https://github.com/Javenzeng/faithful-markdown/releases/tag/v2.12 。
- 发布源码：057f5176851c6155a86eca676b1c237c7627c1bc；后续治理提交不改变该产物。
- 本地 EXE：D:\Projects\faithful-markdown\releases\v2.12\FaithfulMarkdown.exe（仅此工作机路径；其他环境从 Release 下载）。
- 产物：13,345,708 bytes；SHA-256 4799D844FFAFF167D466CB2D8C68948815FD6E7161ED33FF89A999F8013F525B；发布时已核对远端资产。
- 最新验证：31 项 Python 测试、模拟 bridge 的 Edge UI smoke、隔离构建通过；不是 GitHub CI 或 Human 打包版验收。
- v2.12 将已有操作收进文件/视图/设置，仅打开/保存常驻；无新增运行时依赖。

## 当前方向与授权

稳定使用 v2.12，等待测试人员的实际反馈，不主动增加功能或重写架构。Human 已同意“方便阅读、修改和分享一份 Markdown”的方向；功能需求须逐项评估，不因无 bug 或有人提出就自动开发。

本阶段授权：整理过期治理、精简入口与路由、同步 GitHub。无新的功能/打包授权。治理完成后 Owner/Baton 回到 Human，下一项工作等待具体反馈和授权。

## 验收边界与待观察项

- 历史明确 Human 验收：V2.1 内容保真、v2.7 Windows identity；见 MILESTONES 路由。
- Human 曾报告个人使用 v2.9 没问题；不是全部后续版本的完整验收。聊天暂无 bug 报告，不等于零缺陷证明。
- v2.10 实际原生剪贴板图片保存/预览通过；打包版图片选择、Explorer 文件粘贴仍未记录完整 Human 验收。
- v2.11 浏览器 PDF 生成通过；打包版原生打印窗口仍未记录 Human 验收。
- v2.12 菜单打包版等待测试人员反馈。不得因此启动泛化测试工程。
- EXE 未付费签名；旧 Defender 误报申请已被 Human 取消，不自行恢复提交。
- V2.5 大文件专项暂缓；V3 重写无授权；行号、Word 和多格式导出无授权。

## 接手下一步

先按 AGENTS 恢复状态并简短报告；有具体 issue 时只读取对应模块和证据。没有新任务时保持现状。每阶段结束覆盖更新本文件，不累积旧“下一步”。
