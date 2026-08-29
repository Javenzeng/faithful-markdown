# Markdown Reader & Editor V2 打包与测试事实记录

日期：2026-08-29  
性质：问题、处理和当前状态记录。本文件不包含优化方案，也不授权继续修改。

## 一、测试与打包期间出现的问题

### 1. Windows 换行测试受测试写入方式影响

`tests/test_core.py` 原先通过 `Path.write_text()` 构造 LF 测试文件。在 Windows
环境中，该写入方式可能自动转换换行符，导致测试输入本身不再是预期的 LF。
测试已改为将 UTF-8 编码后的内容直接写入字节，以确保测试夹具中的换行符不被
运行环境改写。修改后核心单元测试 8/8 通过。

### 2. 未保存关闭确认曾造成桥接锁死

开发过程中，pywebview 自带的 `confirm_close=True` 以及关闭事件中同步执行
JavaScript 的方式都出现过窗口初始化或关闭阶段锁死。最终实现没有使用这两条
路径，而是在 Python 关闭事件中通过独立线程显示 Windows 原生确认框。

### 3. 脏状态同步造成无参数启动后永久“未响应”

首次打包后的实机反馈显示：应用窗口和 WebView2 子进程已经创建，但主窗口长期
处于 `Responding=False`，并非正常的单文件解压等待，也不是内存不足。

实际原因是 `assets/index.html` 的通用 `updateChrome()` 在
`initial_state()` 尚未完成桥接返回时再次调用 Python `set_dirty()`，形成间歇性
桥接重入死锁。把调用延迟到 `setTimeout(..., 0)` 只能降低出现概率，没有消除问题。

最终实现已将 `set_dirty()` 从通用界面刷新和初始化路径中移除。现在只有用户真实
编辑并且 clean/dirty 状态发生变化时，前端才向 Python 同步一次；打开、保存和
另存为成功后，由 Python 端直接将状态设为 clean。

### 4. 受控冒烟测试没有暴露间歇性无参数启动问题

此前开发侧曾对源码入口和当时生成的 EXE 执行 GUI 冒烟，其中带 Markdown 文件
参数的启动路径通过。该次验证是单次受控运行，没有对“无参数冷启动”进行重复测试，
因此没有暴露后续实机出现的间歇性死锁。

完成最终桥接修复后，按项目所有者要求，没有再运行 GUI 冒烟测试，也没有启动最终
EXE。最终 EXE 的实机验证状态由项目所有者后续反馈决定。

### 5. PyInstaller 清理旧缓存时出现权限错误

执行 `build_windows.ps1` 时，PyInstaller 清理
`build/Markdown_Reader_Editor/localpycs` 发生 `WinError 5: Access denied`。
项目位于同步盘目录，旧构建缓存当时无法正常删除。本次封装改用新的
`build_startup_fix` 工作目录和 `dist_startup_fix` 输出目录后成功完成。

### 6. 中文同步盘路径在构建日志中显示乱码

PyInstaller 和 pip 的部分控制台输出把 `<Google Drive synced root>` 显示成乱码，但本次依赖
读取、源码分析和 EXE 生成均完成。乱码发生在日志显示层面。

### 7. Markdown 连续空行的实际表现

当前渲染遵循标准 Markdown/HTML 行为。单个空行用于分隔段落；连续多个空行在生成
HTML 后会被折叠，不会在预览区形成与回车次数相同的垂直空白。当前渲染同时会转义
原始 HTML，因此正文中直接输入 `<br>` 不会作为 HTML 换行标签执行。

## 二、环境依赖记录

当前 `build_windows.ps1` 明确限制 Python 3.10–3.13 x64，并依赖项目 `.venv`、
PyInstaller、pywebview、pythonnet、Mistune 以及本机 WebView2 Runtime。脚本还会在
封装前安装依赖并自动运行全部单元测试。

项目所有者对后续工作的明确约束是：环境依赖需要放宽，交接和执行过程最好不要指定
某个特定 Python 版本、启动器、固定解释器路径或某一台机器的具体环境；记录应以实际
所需能力和依赖是否可用为准。本条是项目所有者要求的工作边界，当前脚本尚未据此修改。

## 三、本次最终实现状态

- `app.py`
  - 保留 Python 侧 dirty 状态。
  - 成功打开、保存、另存为后直接重置 dirty 状态。
  - 未保存关闭确认使用独立线程中的 Windows 原生确认框。
- `assets/index.html`
  - 初始化、打开文档、保存后的通用界面刷新不再调用 `set_dirty()`。
  - 仅在编辑器输入导致 clean/dirty 状态切换时调用一次 `set_dirty()`。
- `tests/test_core.py`
  - 换行测试数据改为字节写入，避免 Windows 文本模式改写测试输入。
- `build_windows.ps1`
  - 已启用 PowerShell 原生命令错误传播，PyInstaller 非零退出码不会再被误报为成功。
- 核心单元测试
  - 构建脚本在首次封装尝试前自动运行：8/8 通过。
- 最终 GUI/EXE 测试
  - 最终修复后未执行，遵从项目所有者要求。

## 四、当前封装产物

项目根目录：`Markdown_Reader_Editor.exe`  
文件大小：14,508,178 bytes  
SHA-256：`E706126BA63F9FD7486430EF1227721FBB58A0725CF53497573CC9FADAECBF1E`

本次最终封装使用 `dist_startup_fix/Markdown_Reader_Editor.exe` 生成，并复制到项目根目录。
