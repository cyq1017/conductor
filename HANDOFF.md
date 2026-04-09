# HANDOFF

## 2026-04-09

### Done
- Conductor MVP 完成并上线 GitHub: https://github.com/cyq1017/conductor
- 方法论 3 篇（handoff-protocol / trust-calibration / task-sizing）
- 模板 4 个（HANDOFF / CLAUDE / ERROR_BOOK / TRUST_PROFILE）
- CLI 2 命令（status / init），本机验证通过
- README 英文 + 中文版，支持 11 个 AI coding agent（按 CLI/IDE 分类）
- orbit 优化建议文档产出（orbit_optimization_feedback.md）
- AGENTS.md 增加「工具选择规则」（从浏览器卡死踩坑中提炼）

### Decisions
- 项目名定为 Conductor（交响乐指挥隐喻）
- MVP 范围：方法论 + 模板 + CLI status 命令
- Python 3.9+（兼容系统自带版本）
- click + rich 做 CLI
- 先在 github-profile/conductor 子目录开发，已 push 为独立仓库

### Pitfalls
- 浏览器子代理验证 GitHub 页面卡死 18 分钟 → 已加规则：验证类任务用命令行
- pyproject.toml 需要 `[tool.hatch.build.targets.wheel] packages = ["src/conductor"]`
- click.version_option() 需要显式传 version 和 prog_name

### Next Steps
1. 讨论 awesome-design-md 借鉴方向（A: 加 DESIGN.md 支持 / B: awesome-agent-rules 仓库 / C: README 排版优化）
2. conductor 迁移为独立项目目录（脱离 github-profile 子目录）
3. 配 PATH 让 conductor 命令全局可用
4. 考虑 PyPI 发布
