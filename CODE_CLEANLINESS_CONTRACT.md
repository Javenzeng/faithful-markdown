# CODE_CLEANLINESS_CONTRACT.md

本契约适用于 Markdown Reader & Editor 的所有 Sol / Codex 修改。

目标不是“看起来优雅”，而是长期控制复杂度、状态、依赖、兼容债务和仓库污染。

## 1. Scope Gate

任何新增行为必须至少满足一项：
- 提高文件保真
- 提高保存可靠性
- 提高确定性
- 提高性能
- 提高可审计性
- 删除既有复杂度

仅“看起来方便”“竞品有”“以后可能有用”不构成开发理由。

## 2. Dependency Budget

- 新增运行时依赖前，必须说明标准库 / 当前依赖为什么不足。
- 不为一个小功能引入大型框架。
- 长期目标：运行时依赖保持在极小集合，优先减少而不是增加。
- 未使用依赖必须删除。

## 3. State Budget

- 能从已有事实计算出的状态，不额外存储。
- 同一事实尽量只有一个权威来源。
- 避免 JS / Python 双份状态同步。
- 新增跨 bridge 状态前，必须证明无法通过单向调用或即时计算解决。
- 文件外部变化判断优先使用单一 authoritative fingerprint，而不是维护多套 mtime/size/hash 同步状态。

> **Derived state is cheaper than synchronized state.**

## 4. Abstraction Budget

- 不在出现真实重复之前建立抽象。
- 不创建只有一个实现的 Strategy / Factory / Provider / Manager 层级，除非有明确边界价值。
- 小工具优先直接、可读的函数和小类。

> **No abstraction before duplication.**

## 5. Compatibility Budget

- 明确支持当前目标环境，不维护“也许还能运行”的遗留系统。
- 不为 Win7/Win8、旧 WebView、旧 Python 等增加兼容分支。
- 不为单台机器的偶发现象永久加入环境特判。
- 构建与交接文档描述 required capabilities，不把治理绑定到某个固定解释器路径、启动器或机器目录。

## 6. Error-Handling Budget

允许：
- 对可预期用户错误给出明确提示
- 对文件权限、编码、外部修改等现实错误进行最小处理

禁止：
- `except Exception: pass`
- 静默失败
- 无证据的 retry / timeout / backoff
- fallback of fallback
- watchdog 掩盖根因
- 捕获程序 bug 后继续假装成功

程序错误应暴露，现实错误应清楚处理。

## 7. Root Cause Before Defense

遇到 bug：
1. 复现
2. 找根因
3. 删除错误路径 / 冗余状态
4. 加回归测试
5. 最小修复

不要先增加延迟、重试、线程、锁或兼容层。

本项目已出现过 pywebview bridge 重入死锁；该事件是永久反例：复杂状态同步可以为了一个小 UI 状态制造系统级故障。

## 8. Test > Defensive Code

- 真实 bug 优先转化为 regression test。
- Fidelity 行为优先由 fixture、hash 或 byte-level assertions 证明。
- 测试可以增长，运行时代码不应同比膨胀。
- 不为了测试方便改变产品行为。

## 9. Change Budget

每次修改主动检查：
- 是否可以删除旧路径
- 是否引入重复逻辑
- 是否留下兼容分支
- 是否增加不必要状态
- 是否存在更小实现

推荐在里程碑审查中记录新增行、删除行、净增长及其必要性。

大规模“新增很多、删除很少”必须重新审视。

## 10. Dead Code Policy

禁止保留：
- 注释掉的旧实现
- 已废弃 fallback
- 未引用函数 / 类
- 失效 feature flag
- “以后可能用”的代码

历史由版本控制或 `records/` 保存，不由源码垃圾保存。

## 11. Comment Budget

注释只解释：
- 为什么这里必须这样做
- 哪个系统边界或已知故障要求这样做

不解释代码下一行在做什么。

## 12. File / Module Discipline

- 文件按真实职责拆分，不按架构图拆分。
- 不为追求“企业级结构”制造目录层级。
- 一个模块如果仍然清晰，不为了 LOC 数字机械拆文件。
- 模块一旦承担多个独立生命周期或状态源，再考虑拆分。

## 13. Repository Hygiene

Canonical project root 只保留：
- 治理入口
- README / requirements / build entrypoints
- 产品源码
- `assets/`
- `tests/`
- `records/`
- `releases/`

以下属于 ephemeral local state，不得被视为 canonical project content：
- `.venv/`
- `__pycache__/`
- `build/`、`build_*`
- `dist/`、`dist_*`
- 工具缓存
- 临时日志
- 自动生成且非构建输入的 `.spec`

Accepted 二进制只进入 `releases/<version>/accepted/`，不得放在源码根目录，也不得被下一次构建自动覆盖。

当前 Windows 构建脚本仍会在同步项目目录创建 `.venv/build/dist/.spec`；这是已知 build-hygiene debt。下次打包前必须单独设计更干净的 ephemeral build path，但不得在未授权时顺手改构建逻辑。

## 14. UI Discipline

- 新 UI 元素必须直接表达文件事实或必要操作。
- 不增加功能型 toolbar / panel 竞争。
- 状态优先简短、可解释、可验证。

## 15. Performance Discipline

- 不提前优化想象中的瓶颈。
- 只有 profiling、测试或真实用户反馈证明问题后才优化。
- 优先删除工作，而不是引入 cache / worker / background service。

## 16. Release Cleanliness Gate

任何 milestone 合并 / release 前检查：
- 所有要求的测试通过
- 无新增无意义依赖
- 无死代码
- 无 broad silent exception
- 无未经批准的 compatibility shim
- 无重复状态源
- 无临时调试代码
- 无 ephemeral build state 混入 canonical root
- README / state / milestone 与实际实现一致
- 关键二进制有 SHA-256

## 17. Definition of Beautiful Code

> **更少的状态，更少的依赖，更少的分支，更少的隐藏行为；更多的测试，更明确的不变量，更直接的失败方式。**
