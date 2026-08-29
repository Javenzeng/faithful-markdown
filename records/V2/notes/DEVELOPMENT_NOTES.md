# V2 开发与审核记录

## V1 审核结论

原版核心源码只有约 80 行，没有明显的历史兼容层或大段冗余。主要问题不是代码量，而是一次性浏览器架构：

1. 运行时依赖 `marked.js` CDN 与 GitHub Markdown CSS CDN。
2. Markdown 被写入系统临时 HTML；文件不会主动删除。
3. 临时 HTML 位于 `%TEMP%`，导致 Markdown 相对图片以错误目录解析。
4. `except Exception: sys.exit(1)` 会把文件选择器等异常静默吞掉。
5. 文件读取固定为 UTF-8，没有明确错误提示策略。
6. Drive 中 EXE 时间早于源码，二进制与当前源码没有可验证的一致性。

## V2 取舍

V2 原计划采用本地 `marked.js + DOMPurify`。实现阶段进一步收口为 **Python 侧 Mistune 渲染 + pywebview UI**：

- 不需要额外 vendored JS 资源；
- 不需要浏览器侧 HTML sanitizer；
- `escape=True` 默认转义 Markdown 中原始 HTML；
- Mistune 会把 `javascript:` 等危险 URL 处理成 `#harmful-link`；
- 最终仍为完全离线渲染；
- 依赖数量更少，构建与后续维护更简单。

这不是兼容层，而是对 V2 最小产品目标的进一步简化。

## 当前验证范围

已覆盖核心层：

- UTF-8 读写
- UTF-8 BOM 保留
- 现有 CRLF / LF 换行风格保留
- 非 UTF-8 明确拒绝
- Save As 自动补 `.md`
- 原始 HTML 转义
- `javascript:` 链接中和
- 相对图片内联
- 保存不重置编辑光标/滚动位置
- 相对链接不允许接管 WebView 导航
- Windows 强制 Edge Chromium / WebView2，禁止退回 MSHTML

当前运行环境无法完成 Windows GUI 实机启动，因此 GUI 层仍需要在 Windows 10/11 目标机器做一次实际启动与 EXE 冒烟验收。开发侧最终核心单元测试为 8/8 通过，Python 静态编译与前端 JavaScript 语法检查通过。
