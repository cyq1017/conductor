# 未来项目待做清单

> 从 Conductor brainstorming 中产生的独立项目 ideas
> 创建日期：2026-04-10
> 原则：每个 idea 记录来源和触发思路

---

## 一、Awesome 系列（「复制 .md 即用」模式）

来源：分析 awesome-design-md（35k stars）后发现，「一个 .md 丢进项目 → AI 立即可用」是高传播模式。

### 1.1 awesome-agent-rules 🔴 高优先级
- **内容**：各类项目的 CLAUDE.md / AGENTS.md / .cursorrules 最佳实践集合
- **来源**：Conductor brainstorming 中发现，所有 AI coding agent 都支持项目级规则文件，但没人整理过最佳实践
- **为什么值得做**：Claude Code / Cursor / Windsurf / Codex 用户都需要，市场空白
- **种子内容**：从自己的 GitHub 涨星计划 / wenyuan / network-optimization 项目中提取
- **与 Conductor 的关系**：互补 — Conductor 是方法论，awesome-agent-rules 是实践集合

### 1.2 awesome-context-md 🟡 中优先级
- **内容**：CONTEXT.md — 让 AI 秒懂项目架构的说明文件集合
- **来源**：发现 agent 每次进入新项目都要重新理解代码库，如果有标准的 CONTEXT.md 可以节省大量 token
- **分类**：按技术栈（Python/Node/Go）、按项目类型（CLI/Web/ML）

### 1.3 awesome-spec-md 🟡 中优先级
- **内容**：不同类型项目的需求文档模板（Web / CLI / ML / API）
- **来源**：分析 OpenSpec（38k stars）后发现它是工具，但缺少按项目类型分类的 spec 模板集合
- **与 OpenSpec 的关系**：OpenSpec 是流程工具，awesome-spec-md 是模板集合

### 1.4 awesome-prompt-engineering 🟢 低优先级
- **内容**：给 AI coding agent（非聊天）用的 prompt 模板
- **来源**：awesome-chatgpt-prompts（300k stars）证明了需求，但它是聊天场景的，coding agent 场景没人做
- **分类**：debug / refactor / review / migration / test-writing

---

## 二、通信层项目

### 2.1 Agent IM Bridge（暂未命名）🟡 中优先级
- **内容**：通过 Telegram bot 在移动端管理 agent
- **来源**：讨论 Conductor 时提出 — 不在电脑前也想知道项目进展、给 agent 下指令
- **核心功能**：
  - `/status` — 移动版 conductor status
  - `/handoff <项目名>` — 读某个项目的最新 HANDOFF
  - 主动推送 — 项目 stale 超过 X 小时 → 通知
  - `/tell <项目名> "指令"` — 远程触发 agent（远期）
- **为什么不放 Conductor 里**：Conductor 是 CLI 工具管"文件协议"，Telegram bot 是独立的"通信层"，塞进去会臃肿
- **技术方案**：Python + python-telegram-bot + 读取 HANDOFF.md 文件

---

## 三、Agent 编排项目

### 3.1 Agent Delegation Chain（暂未命名）🟡 中优先级
- **内容**：人定义 agent 链条，Conductor 执行路由
- **来源**：讨论中提出的场景 — "在 Antigravity 里聊想法 → 让 Codex 执行 → Claude Code review"
- **与 CrewAI/LangGraph 的区别**：
  - CrewAI：agent 自己决定下一步给谁（全自动）
  - 我们：人决定链条，工具执行（半自动，人在关键节点决策）
- **为什么不放 Conductor 里**：Conductor 管人→agent 交接，agent→agent 编排是另一个维度
- **前置条件**：需要统一的任务格式、agent 间通信协议

---

## 四、团队协作项目

### 4.1 Multi-Operator Agent Management（暂未命名）🟢 低优先级
- **内容**：多人指挥多 agent 的团队协作框架
- **来源**：讨论 Conductor 时自然延伸 — 公司场景中多人同时让 agent 改同一代码库会混乱
- **核心挑战**：
  - 决策权分配（谁负责哪个模块）
  - 冲突解决（A 说用 Flask，B 说用 FastAPI）
  - 团队级信任画像
  - Git branch 级别的 agent 隔离
- **为什么不放 Conductor 里**：复杂度指数级增长，没有真实用户反馈做出来也是猜
- **时机**：等 Conductor 有用户后，从用户反馈中验证需求

---

## 五、记忆系统项目

### 5.1 Agent Memory Layer 🟡 中优先级
- **内容**：多 agent 共享记忆系统
- **来源**：讨论 OpenMemory（Mem0）时发现，我们的文件方案（HANDOFF.md / ERROR_BOOK.md）够用但不优雅，agent 间记忆不互通
- **现状对比**：
  - 我们：文件即记忆，手动维护，agent 间不互通
  - OpenMemory：向量数据库，自动检索，但增加基础设施依赖
- **设计思路**：
  - 轻量实现：不用向量数据库，用结构化 JSON/YAML + 全文搜索
  - 分层记忆：事实层（不变）→ 决策层（项目级）→ 教训层（从错题本提炼）
  - 人类记忆延伸："你忘了没关系，问 agent 就行"
- **与 Conductor 的关系**：这是 Conductor v0.4 的核心功能方向

---

## 六、领域知识 .md 共享（Research 方向）

### 6.1 各领域的 .md 标准化
- **来源**：从 awesome-design-md（前端设计 .md）推导 — 任何领域的知识都可以编码成 .md 给 AI 消费
- **可做的领域**：
  - 后端架构：ARCHITECTURE.md（API 设计模式、数据库 schema）
  - DevOps：INFRA.md（Dockerfile / CI-CD / K8s 配置）
  - ML/AI：TRAINING.md（训练配置、评估 setup）
  - 安全：SECURITY.md（认证流程、输入验证）
  - 测试：TESTING.md（测试策略、fixtures）
  - 文档：DOCS_STYLE.md（API 文档风格）
- **核心洞察**：.md 是 AI 时代最低成本的知识传递方式 — 人能读、AI 能读、Git 能追踪
- **实现方式**：可以做成 awesome-xxx 系列，也可以整合为一个大仓库

---

*最后更新：2026-04-10*
*下次审阅：有新 idea 时随时追加*
