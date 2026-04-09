<div align="center">

# 🎵 Conductor

**给同时管理多个 AI 编程助手的人用的协作框架**

结构化交接 · 信任校准 · 持续进化

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org)

[English](README.md) · **中文**

</div>

---

## 痛点

你在一个终端里用 Claude Code，另一个窗口开着 Cursor，可能还有 Codex 在做 review——同时跑着不同的项目。到了一天结束的时候：

- 🤯 记不清每个 agent 做了什么决定
- 🔁 新 session 重复昨天已经踩过的坑
- 📂 交接记录、开发日志、错误记录散落各处
- 🤔 不知道什么时候该信任 agent、什么时候该仔细审查

**Conductor** 就是解决这些问题的。

---

## 支持的 AI 编程工具

<table>
<tr>
<td align="center"><b>⌨️ CLI</b></td>
<td align="center"><b>Claude Code</b><br/>Anthropic</td>
<td align="center"><b>Codex CLI</b><br/>OpenAI</td>
<td align="center"><b>Gemini CLI</b><br/>Google</td>
<td align="center"><b>Kimi Code</b><br/>Moonshot AI</td>
</tr>
<tr>
<td align="center"><b>🖥️ IDE</b></td>
<td align="center"><b>Cursor</b><br/>AI IDE</td>
<td align="center"><b>Windsurf</b><br/>Codeium</td>
<td align="center"><b>Antigravity</b><br/>Google DeepMind</td>
<td align="center"><b>GitHub Copilot</b><br/>Chat</td>
</tr>
<tr>
<td></td>
<td align="center"><b>Aider</b><br/>开源</td>
<td align="center"><b>OpenCode</b><br/>开源</td>
<td align="center"><b>Continue</b><br/>开源插件</td>
<td align="center"><i>+ 任何能读写<br/>文件的工具</i></td>
</tr>
</table>

> 任何能读写文件的 AI 编程工具都兼容 Conductor——我们基于文件协议，不绑定特定工具。

---

## 核心内容

### 📖 方法论 — Human-Agent 交互的 12 个维度

我们从实战中总结出人与 AI agent 协作时需要关注的 12 个维度：

| # | 维度 | 说明 |
|---|------|------|
| 1 | **交接管理** | session 之间如何传递上下文、避免信息丢失 |
| 2 | **知识沉淀** | 记录决策、错误和 QA 对 |
| 3 | **信任校准** | 什么时候该审查、什么时候可以放手 |
| 4 | **认知负荷** | 并行管理多个 agent 时的脑力瓶颈 |
| 5 | **Prompt 质量** | 你给 agent 的指令是否越来越精准 |
| 6 | **Agent 画像** | 每个 agent 在不同领域的可靠度 |
| 7 | **工具选择** | 什么任务交给哪个 agent 最合适 |
| 8 | **反馈循环** | agent 犯的错有没有被转化为预防规则 |
| 9 | **注意力分配** | 多个项目并行时，此刻该看哪个 |
| 10 | **分歧解决** | 你和 agent 意见不同时怎么办 |
| 11 | **跨 Agent 一致性** | 多个 agent 给出矛盾建议时怎么处理 |
| 12 | **精力管理** | 疲劳时降低审查标准的风险 |

详细文档：[docs/](docs/)

---

### 📁 模板 — 复制即用

| 模板 | 用途 |
|------|------|
| [`HANDOFF.md`](templates/HANDOFF.md.template) | session 结束时的上下文交接 |
| [`CLAUDE.md`](templates/CLAUDE.md.template) | Agent 行为规则（含交接协议和任务启动协议） |
| [`ERROR_BOOK.md`](templates/ERROR_BOOK.md.template) | AI 错题本 — 追踪 AI 犯的错 |
| [`TRUST_PROFILE.md`](templates/TRUST_PROFILE.md.template) | Agent 信任画像 — 各领域可靠度评分 |
| [`DESIGN.md`](templates/DESIGN.md.template) | UI 设计系统 — 统一 agent 产出的界面风格 |

---

### 🧰 CLI — 一条命令看全局

```bash
$ conductor status

🎵 Conductor · Project Status
┌─────────────────────┬─────────────┬────────┬──────────────────────────┐
│ Project             │ Last Active │ Status │ Next Step                │
├─────────────────────┼─────────────┼────────┼──────────────────────────┤
│ wenyuan             │      6h ago │   ✅   │ 重构 README              │
│ network-opt         │      2h ago │   ✅   │ VPS 方案确认             │
│ conductor           │     30m ago │   ✅   │ 写测试                   │
│ old-project         │      3d ago │   🔴   │ 归档还是继续？            │
└─────────────────────┴─────────────┴────────┴──────────────────────────┘
 📅 2026-04-09 │ 4 projects │ 5 decisions │ 12 files Δ
```

---

## 快速开始

### 方案 A：只用模板（不需要安装）

1. 复制 [`templates/HANDOFF.md.template`](templates/HANDOFF.md.template) 到你的项目根目录，改名为 `HANDOFF.md`
2. 把 [`templates/CLAUDE.md.template`](templates/CLAUDE.md.template) 中的交接协议复制到你项目的 `CLAUDE.md` 里
3. 告诉你的 AI：*"开始时先读 HANDOFF.md，结束时更新 HANDOFF.md"*

### 方案 B：安装 CLI

```bash
pip install conductor-ai
conductor init ./my-project
conductor status
```

---

## 核心概念

### 🤝 交接协议

每次 session 结束时写一段结构化交接：

```markdown
## 2026-04-09
- done: 完成了用户认证模块
- decisions: 选 JWT 不选 session（无状态、可扩展）
- pitfall: bcrypt 5.x 改了默认轮数——会破坏现有哈希
- next: 添加密码重置功能
```

**500 token 上限。** 写不出来就说明你自己也没理解清楚。

→ [完整协议文档](docs/handoff-protocol.md)

### 🎯 信任校准

不要盲信，也不要盲疑。按领域精细校准：

| 层级 | 方法 |
|------|------|
| L1 | **验结果** — 代码能跑吗？测试过了吗？ |
| L2 | **交叉验证** — 让另一个 agent 审查 |
| L3 | **渐进信任** — 先在一个文件上试 |
| L4 | **要求解释** — 问为什么，不只是问做什么 |

→ [完整框架](docs/trust-calibration.md)

### 📏 任务分级 (S/M/L)

不是每个任务都需要完整规划：

| 等级 | 耗时 | 流程 |
|------|------|------|
| **S** | < 30 分钟 | 直接做 → 测试 → 提交 → 交接 |
| **M** | 1-3 小时 | 简要计划 → 执行 → 交接 |
| **L** | > 3 小时 | 脑暴 → 设计 → TDD → 审查 → 交接 |

→ [完整指南](docs/task-sizing.md)

---

## 为什么选 Conductor？

| 对比 | 区别 |
|------|------|
| **CrewAI / LangGraph** | 它们编排 agent 之间的协作。我们编排**人与 agent** 的协作。 |
| **OpenSpec** | OpenSpec 管理单个 session 内的 spec。我们管理**跨 session、跨 agent** 的协作。 |
| **只用 CLAUDE.md** | CLAUDE.md 只是一个文件。我们是**完整的方法论 + 工具链**。 |
| **什么都不用** | 你在丢失决策、重复犯错、浪费 context window token。 |

---

## 路线图

- [x] v0.1 — 方法论 + 模板 + `conductor status`
- [ ] v0.2 — `conductor digest` — 从对话日志自动提取决策/错误
- [ ] v0.3 — Agent Retrospective — 结构化的 session 后复盘
- [ ] v0.4 — 记忆系统 — 跨 session 的持久化知识库
- [ ] v0.5 — 移动端通知（Telegram 集成）
- [ ] v1.0 — 多人协作支持（团队工作流）

---

## 理念

> *"如果你只是驱动 AI 干活，干完就走——你永远不知道自己哪里表达不清楚，不知道 AI 在哪个环节容易出问题。「不知道自己不知道」是 AI 时代的原罪。"*

Conductor 基于三个原则：

1. **结构胜于仪式** — 轻量级的协议实际被执行，好过沉重的流程被跳过
2. **观察后再信任** — 通过数据（错题本、信任画像）建立信任，而不是假设
3. **人也要进步** — 不只是让 AI 变好，更是让你自己在 AI 协作中持续进化

---

## 贡献

欢迎贡献！请先阅读 [docs/](docs/) 下的方法论文档了解设计理念。

## 开源协议

[MIT](LICENSE)
