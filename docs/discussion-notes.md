# 讨论记录：Human-Agent 协作深层设计

> 来源：2026-04-09 ~ 04-10 brainstorming 会话
> 保存原因：这些洞察将影响 Conductor v0.2-v0.4 的设计及未来独立项目

---

## 0. 整个讨论是怎么开始的

### 起点：GitHub 涨星计划
最初的目标是整理 GitHub 个人主页（Profile README、pinned repos）+ 文渊项目宣传。在做这些的时候，我们开始讨论"人和 AI agent 交互中有哪些没考虑到的事情"。

### 12 维度的诞生
从用户的实际痛点（跨 session 上下文丢失、agent 犯重复错误、不知道何时信任 agent）出发，我们总结出了 12 个维度的 Human-Agent 交互模型：交接管理、知识沉淀、信任校准、认知负荷、Prompt 质量、Agent 画像、工具选择、反馈循环、注意力分配、分歧解决、跨 Agent 一致性、精力管理。

### 从方法论到产品
用户提出："这些想法能不能变成具体的东西？" 于是决定做 Conductor — 一个框架，包含方法论文档 + 即用模板 + CLI 工具。命名灵感：交响乐指挥家（Conductor）编排多个乐手（Agent），人类是指挥家。

### MVP 边界
通过 brainstorming 确定：MVP = 方法论 3 篇 + 模板 4 个 + CLI 2 命令。技术选型：Python 3.9+ / click / rich / hatchling。

---

## 1. awesome-design-md 的启发（2026-04-09）

### 触发：用户发了这个链接
用户发现 https://github.com/VoltAgent/awesome-design-md （35k stars），问"对我们有什么借鉴"。

### 分析
这个项目的核心模式极简：**一个 .md 文件丢进项目 → AI agent 立即能用**。它收集了 50+ 知名网站的 DESIGN.md（Stripe、Vercel、Linear、Notion 等），基于 Google Stitch 提出的 DESIGN.md 概念。

### 借鉴出的三个方向
- **方向 A**：给 Conductor 加 DESIGN.md 模板 → ✅ 已完成
- **方向 B**：做 awesome-agent-rules 仓库 → ⏳ 待做
- **方向 C**：参考 awesome-design-md 排版优化 Conductor README → ✅ 已完成

### 衍生思考：还有什么领域可以做？
用户追问："awesome-design-md 是前端的，还有哪些类似套路？"

结论：.md 是 AI 时代最低成本的知识传递方式（人能读、AI 能读、Git 能追踪）。不只是前端：
- 后端架构（ARCHITECTURE.md）
- DevOps（INFRA.md）
- ML/AI（TRAINING.md）
- 安全、测试、文档等

由此产生了 awesome-xxx 系列项目 ideas，详见 `docs/future-projects.md`。

---

## 2. 记忆系统讨论（2026-04-10）

### 触发：用户提问 "openmemory 是做什么的"

### 什么是 OpenMemory（Mem0）
开源的 AI 记忆层，用向量数据库存储，agent 可以跨 session 自动检索相关记忆。

### 我们的方案 vs OpenMemory

| | 我们的方案 | OpenMemory |
|---|---|---|
| 存储 | .md 文件（HANDOFF/ERROR_BOOK） | 向量数据库 |
| 检索 | 人/agent 手动读文件 | **自动语义检索** ← 我们缺的 |
| 跨 agent | 需要每个 agent 主动读对方的文件 | **自动共享** ← 我们缺的 |
| 维护 | 人手动整理 | 自动入库 |
| 安装成本 | 零 | 需要搭服务 |

### 用户的关键追问
"agent 返回的东西全是记忆吗？QA 和错题本跟记忆一样吗？"

答案：**不全是记忆**。需要分层：

| 类型 | 例子 | 是记忆吗 | 处理方式 |
|------|------|---------|---------|
| 事实 | "项目用 FastAPI + PostgreSQL" | ✅ 长期有效 | 存入 CONTEXT.md |
| 决策 | "选了 JWT 不选 session" | ✅ 防止重复讨论 | 存入 HANDOFF.md |
| QA 对 | "用户问了 X，agent 答了 Y" | ❌ 原始素材 | 需要提炼后才有价值 |
| 错题本 | "agent 用了废弃的 API" | ❌ 是教训 | 转化为规则写入 CLAUDE.md |

### 结论
OpenMemory 解决了"多 agent 间记忆互通"问题，但它是底层基建。我们的 HANDOFF/ERROR_BOOK 是上层协议。**两者未来可结合**：上层 Conductor 协议 + 底层 OpenMemory 存储。但短期继续用文件方案。

---

## 3. 人类记忆与 Agent 记忆的关系（2026-04-10）

### 触发：用户问 "人和agent的记忆的关系是什么，agent的记忆能做成人类记忆的延伸吗"

### 核心洞察

```
人类记忆：模糊、会忘、但有大方向判断力
Agent记忆：精确、不会忘、但需要人维护
理想关系：Agent 记忆 = 人类记忆的外置硬盘
  → 你忘了没关系，问 agent 就行
  → Agent 记住细节，你只需记住大方向
```

### 双向笔记本模式（值得探索的方向）
- 人类侧：每天给 agent 一个"明日优先级"
- Agent 侧：每天给人一个"今日摘要"
- 交汇点：这其实就是 orbit 里 `/start-my-day` 和 `/end-my-day` 的雏形

用户追问"有没有更巧妙的设计" — 这个问题暂未完全回答，标记为 **开放问题**，在 v0.4 Memory System 中继续探索。

---

## 4. 项目边界讨论（2026-04-10）

### 触发：用户问 "多人指多个agent这种场景要怎么做"

### 讨论过程
1. 我最初把"多人场景"和"Telegram 通信"都放进了 Conductor 的 Roadmap
2. 用户指出：**这些是独立项目，不该放在 Conductor 里**
3. 我立即修正，从 Roadmap 中删除

### 最终决策

| 功能 | 归属 | 用户原话/理由 |
|------|------|-------------|
| 1人管N个agent | **Conductor** | 核心定位 |
| M人管N个agent | **独立新项目** | "conductor只做好个人管理多个agent，多人多agent可以是新的项目" |
| Telegram/IM 通信 | **独立新项目** | "移动端通过IM控制agent有必要都放到conductor里面吗" |
| Agent Delegation Chain | **独立新项目** | "agent delegation chain跟conductor有必要硬融吗" |

### 用户的远见
"人与agent关系相关的应用肯定大有可为" — 这意味着这些不是随便丢弃的 idea，而是有潜力的独立方向。详见 `docs/future-projects.md`。

---

## 5. 踩坑与规则沉淀

### 浏览器卡死事件（2026-04-09）
- **发生**：用浏览器子代理验证 GitHub 页面渲染，卡了 18 分钟
- **用户反馈**："出现问题了就不要一直加载了"
- **更深层问题**：用户追问 "你记下了下次能避免吗" → 抛出了 agent 跨 session 记忆的本质问题
- **解决方案**：写入 AGENTS.md 规则（工具选择规则），确保未来 agent 会读到
- **教训**：验证类任务用命令行、浏览器只用于必须交互的操作

### Roadmap 越界事件（2026-04-10）
- **发生**：把多人场景写入 Conductor Roadmap
- **用户指出**："为什么做多人场景，这不是单独的项目吗"
- **教训**：严格遵守已确认的项目边界，不顺便扩展 scope

---

## 6. Conductor 版本规划

| 版本 | 功能 | 状态 |
|------|------|------|
| v0.1 | 方法论 + 模板 + CLI（status/init） | ✅ 已完成 |
| v0.2 | `conductor digest` — 从对话日志提取决策/错误 | ⏳ 待做 |
| v0.3 | Agent Retrospective — 结构化 session 后复盘 | ⏳ 待做 |
| v0.4 | Memory System — 跨 session 持久化知识库 | ⏳ 待做 |

---

## 7. 开放问题（尚未解决）

1. 人-agent 记忆有没有更巧妙的设计？双向笔记本模式之外？
2. 人和 agent 的配合有没有更巧妙的设计？
3. awesome-agent-rules 的分类体系怎么设计？
4. 任务规模如何让 agent 自动判断（而不是用户判断）？信任问题？

---

*最后更新：2026-04-10*
*关联文件：docs/future-projects.md（独立项目 ideas）*
