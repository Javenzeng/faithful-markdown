# Faithful Markdown — Agent entry

## 核心规则

- 产品已公开发布（RELEASED）。目标：让不想安装重型编辑器的人，方便阅读、小范围修订和分享 Markdown；文件保真是信任基础。
- 最小范围、最小实现。禁止顺手优化、无关重构、推测性兼容/抽象/防御和重复验证；达到本次验收标准即停止。
- 功能请求不是路线图。先问用户要完成什么、缺少功能时怎么办，再按宪章评估；实施、打包、发布按 Human 当前授权执行，不把过去授权当作永久许可。
- 保留用户改动；普通源码靠 Git 恢复，不造备份或哈希体系。发布产物保留一次 SHA-256 对照即可。
- 单一写入者。明确区分源码测试、浏览器模拟、打包成功、远端发布与 Human 实机验收；不得相互替代。
- 不因可扩展性提前拆模块。当前是一个产品，下面的职责路由不是子项目；只有独立生命周期或真实重复出现才调整结构。

## 新 session：最小读取

1. 读本文件与 PROJECT_STATE.md，恢复当前版本、授权与下一步；不默认扫描全部历史。
2. 确认 checkout 的 remote、branch、工作区。GitHub Javenzeng/faithful-markdown 的 main 是源码和持久治理权威；本机常用 checkout 为 D:\Projects\faithful-markdown。Drive 同名目录是旧协调/归档面，不合并成第二套源码。
3. 写任务前核对远端；干净工作区可 git pull --ff-only，冲突或无法安全同步时报告，不覆盖本地改动。远端不可用时说明限制，不把历史访问成功当作当前证明。
4. 仅按任务读取下一节所需文档。输出被截断时按章节补读，不凭截断内容下结论。

## 薄路由

- 产品方向、需求取舍、非目标 → PROJECT_CHARTER.md。
- 代码修改 → CODE_CLEANLINESS_CONTRACT.md；状态/交互/持久化边界 → docs/foundation.md。
- 当前版本、证据限制、待办和授权 → PROJECT_STATE.md（唯一当前状态）；版本/历史入口 → MILESTONES.md；具体证据 → 其中指向的 records/ 文件。
- 用户使用与开发命令 → README.md。
- 文件保真、图片落盘与渲染 → core.py、tests/test_core.py、tests/test_fidelity.py、tests/test_images.py。
- Windows 窗口、对话框、剪贴板与文件关联 → app.py、tests/test_app_api_surface.py；bridge 方法有明确测试，窗口对象保持私有，防止 pywebview 遍历重入。
- 菜单、区域、查找、列表、图片入口、打印 → assets/index.html、tests/ui_navigation.cjs。该浏览器测试使用模拟 bridge，不能证明打包版原生操作。
- 构建/发布/网络故障 → build_windows.ps1、requirements*.txt、docs/OPERATIONAL_LESSONS.md（只读相关条目，最多五条）。

## 每阶段收口

- 用与改动风险相称的检查证明本次行为；通过后不重复扩大验证。
- 更新受影响的标准及 PROJECT_STATE.md，覆盖过期当前描述；只有版本推进才更新 MILESTONES.md，有必要证据才写简短 records/。
- 核对直接依赖处的旧名称、重复路径、死代码和失效说明。删掉无效当前内容，历史证据标明历史，不当作现行指令。
- 不把全文历史堆进入口，不为每个小功能新增路由文件或 AGENTS。现有文件够用就原位更新。
- 授权发布后：干净源码提交 → 现有隔离构建 → 版本专属本地 EXE → GitHub Release → 核对远端资产 → 更新状态；交付发布页与本地绝对路径。二进制不进 Git。
- 治理文档变更按授权同步 GitHub，无需重打 EXE。不能证明的验收保持 pending；无新授权时停在稳定使用/反馈阶段。
