# GPT-5.3-Codex 深度调研报告

> 调研日期：2026年2月19日
> 模型发布日期：2026年2月5日（GPT-5.3-Codex）/ 2026年2月12日（GPT-5.3-Codex-Spark）

---

## 1. 模型概述

GPT-5.3-Codex 是 OpenAI 于 2026年2月5日发布的最新 agentic coding 模型，融合了 Codex 和 GPT-5 的训练栈，代表了从"代码生成"到"通用编程智能体（agent）"的范式转变。

核心亮点：
- 比前代 GPT-5.2-Codex 快 25%
- 首个参与自身创建的模型——早期版本被用于调试自身训练、管理部署和诊断测试结果（self-improvement）
- 首个在 OpenAI Preparedness Framework 网络安全领域被分类为 "High capability" 的模型
- 支持长时间运行的复杂任务（8小时以上），涵盖研究、工具使用和复杂执行
- 可在任务执行过程中实时交互引导（mid-task steering），不丢失上下文

---

## 2. 模型规格

### 2.1 GPT-5.3-Codex（旗舰版）

| 参数 | 值 |
|---|---|
| 发布日期 | 2026年2月5日 |
| Context Window | 400K tokens |
| 最大输出 tokens | 128K tokens |
| 推理速度 | ~65-70 tokens/s |
| 多模态 | 支持文本和图像输入 |
| 许可证 | Proprietary |
| 支持功能 | Vision、Tools、Streaming、Reasoning、Function Calling、Structured Outputs |

### 2.2 GPT-5.3-Codex-Spark（极速版）

| 参数 | 值 |
|---|---|
| 发布日期 | 2026年2月12日（Research Preview） |
| Context Window | 128K tokens（仅文本） |
| 推理速度 | 1,000+ tokens/s（旗舰版的 ~15倍） |
| 运行硬件 | Cerebras Wafer Scale Engine 3 (WSE-3) |
| 可用性 | 仅 ChatGPT Pro 用户，通过 Codex App / CLI / VS Code 扩展访问 |
| API 状态 | 发布时不可通过 API 访问 |

Spark 版本的平台级延迟优化：
- Time-to-first-token 减少 50%
- 每 token 开销减少 30%
- 客户端/服务器往返开销减少 80%（使用持久 WebSocket 连接）

### 2.3 Reasoning Effort Levels（推理努力等级）

GPT-5.3-Codex 作为 reasoning model，支持通过 `reasoning.effort` 参数控制推理深度。通过 Responses API 调用：

```python
response = client.responses.create(
    model="gpt-5.3-codex",
    reasoning={"effort": "medium"},
    input=[{"role": "user", "content": "your prompt"}]
)
```

| 等级 | 说明 | 适用场景 |
|---|---|---|
| `low` | 偏向速度和经济的 token 使用 | 高吞吐、低复杂度任务（文本分类、简单问答） |
| `medium`（默认） | 平衡速度和推理准确性 | 日常编程任务、一般性问题 |
| `high` | 偏向更完整的推理，生成更多 reasoning tokens | 复杂多步骤问题、架构设计、深度调试 |

注意事项：
- Reasoning tokens 不可见，但占用 context window 空间
- Reasoning tokens 按 output tokens 计费
- GPT-5.2 额外支持 `none` 等级（无推理，低延迟），但 GPT-5.3-Codex 文档中未明确提及此选项
- OpenAI 建议在实验初期至少预留 25,000 tokens 给 reasoning + output

### 2.4 与 GPT-4o 和 o3 的对比

| 特性 | GPT-5.3-Codex | o3 | GPT-4o |
|---|---|---|---|
| 发布时间 | 2026年2月 | 2025年4月 | 2024年5月 |
| Context Window | 400K | 200K | 128K |
| 定位 | Agentic coding 专用 | 通用深度推理 | 通用多模态 |
| Reasoning Effort | 支持 low/medium/high | 支持 low/medium/high | 不支持（非 reasoning model） |
| 自主执行能力 | 极强（8小时+长任务） | 中等 | 弱 |
| 退役状态 | 当前最新 | 仍可用 | 计划于2026年4月3日全面退役 |

---

## 3. 定价

### 3.1 API 定价

#### GPT-5.3-Codex / GPT-5.2（旗舰 API 定价相同）

| 类型 | 价格（每百万 tokens） |
|---|---|
| Input | $1.75 |
| Cached Input | $0.175 |
| Output（含 reasoning tokens） | $14.00 |

注：不同 reasoning effort 等级不会改变单价，但 `high` 等级会生成更多 reasoning tokens（按 output 计费），因此实际成本更高。`low` 等级生成较少 reasoning tokens，实际成本更低。

#### GPT-5.2 Pro（最高精度版本）

| 类型 | 价格（每百万 tokens） |
|---|---|
| Input | $21.00 |
| Output | $168.00 |

#### GPT-5 Mini

| 类型 | 价格（每百万 tokens） |
|---|---|
| Input | $0.25 |
| Cached Input | $0.025 |
| Output | $2.00 |

#### GPT-5.3-Codex-Spark

- 目前处于 Research Preview 阶段，尚未公布独立 API 定价
- 使用独立于标准 Codex 模型的 rate limit
- 仅通过 ChatGPT Pro 订阅访问

#### 成本对比参考

据报道，GPT-5.3-Codex 的成本约为其最近竞争对手 Claude Opus 4.6 的 **1/7**。

### 3.2 ChatGPT 订阅计划

| 计划 | 月费 | 主要特性 |
|---|---|---|
| Free | $0 | 有限 GPT-5.2 访问 |
| Go | $8/月 | 扩展 GPT-5.2 Instant 访问，更多消息和上传 |
| Plus | $20/月 | 高级推理模型、Codex agent、Sora 视频生成、早期新功能访问 |
| Pro | $200/月 | 无限 GPT-5.2 和文件上传、GPT-5.2 Pro、最大深度研究、扩展优先速度 Codex agent、Spark 研究预览 |
| Business | $25/用户/月（年付）或 $30/用户/月（月付） | 无限 GPT-5.2 消息、60+ 集成应用、SAML SSO、MFA、合规支持 |
| Enterprise | 联系销售（自定义定价） | 扩展 context window、企业级安全、数据驻留（10个区域）、24/7 优先支持 |

### 3.3 Codex 使用限制（按计划）

| 计划 | 本地消息（每5小时） | 云端任务（每5小时） | 代码审查（每周） |
|---|---|---|---|
| Plus | 45-225 | 10-60 | 10-25 |
| Pro | 300-1,500 | 50-400 | 100-250 |
| Business | 45-225 | 10-60 | 10-25 |
| Enterprise/Edu | 无固定限制（按 credits 扩展） | 无固定限制 | 无固定限制 |

所有付费订阅用户享有 API 用户 2 倍的 Codex rate limit。

---

## 4. Benchmark 评测成绩

### 4.1 官方 Benchmark 对比

| Benchmark | GPT-5.3-Codex | GPT-5.2-Codex | GPT-5.2 | 测量内容 |
|---|---|---|---|---|
| Terminal-Bench 2.0 | **77.3%** | 64.0% | 62.2% | 终端操作的 agent 执行能力 |
| SWE-Bench Pro (Public) | **56.8%** | 56.4% | 55.6% | 实际软件工程任务 |
| OSWorld-Verified | **64.7%** | 38.2% | 37.9% | 桌面操作任务 |
| SWE-Lancer IC Diamond | **81.4%** | 76.0% | 74.6% | 真实世界自由职业任务 |
| Cybersecurity CTF | **77.6%** | 67.4% | 67.7% | 安全挑战（含防御） |
| GDPval (wins or ties) | **70.9%** | - | 70.9% (high) | 知识工作胜率 |

关键解读：
- **Terminal-Bench 2.0** 提升最大（+13.3个百分点），说明在"执行工具并完成任务"场景优化显著
- **SWE-Bench Pro** 仅微幅提升（+0.4个百分点），纯修复类任务差异不明显
- **OSWorld-Verified** 提升巨大（+26.5个百分点），桌面操作能力大幅增强

### 4.2 GPT-5.3-Codex-Spark Benchmark

| Benchmark | Codex-Spark | GPT-5.3-Codex（旗舰） | 说明 |
|---|---|---|---|
| SWE-Bench Pro | ~56-57% | ~56.8% | 准确率接近，但速度快 5-8 倍 |
| Terminal-Bench 2.0 | 58.4% | 77.3% | 牺牲推理深度换取速度 |
| SWE-Bench Pro 完成时间 | 2-3 分钟 | 15-17 分钟 | 速度优势明显 |

注意：OpenAI 最初宣称 Spark 在 SWE-Bench Pro 上有 15× 加速，但 HackerNews 开发者重新计算后认为在相似准确率下实际加速约为 **~1.37×**，速度提升主要来自 Cerebras 硬件而非算法改进。

### 4.3 行业排行榜参考（2026年2月）

- SWE-Bench Verified 排行榜领先者：Claude 4 Sonnet 77.2%
- GPQA 排行榜：Claude Opus 4.6 (91.3%) > Claude 3.7 Sonnet (84.8%) > o3 (83.0%)
- GPT-5.3-Codex 在 MMLU、GPQA、MATH、HumanEval、Codeforces 等通用 benchmark 上的具体分数尚未公开发布

---

## 5. 可用平台

| 平台 | 可用性 | 说明 |
|---|---|---|
| Codex App（桌面） | ✅ | 多任务并行监控的"指挥中心" |
| Codex CLI | ✅ | 终端优先，细粒度审批控制 |
| VS Code 扩展 | ✅ | IDE 集成 |
| Web 版 | ✅ | 浏览器访问 |
| GitHub Copilot | ✅（2026年2月9日起） | Pro、Pro+、Business、Enterprise 用户可用 |
| API | 🔄 逐步开放中 | "safely enabling access" 阶段 |

---

## 6. 用户评价与社区反馈

### 6.1 正面评价

**自主执行能力获高度认可：**
- Matt Shumer（知名开发者）评价："这是第一个我可以启动一个任务、离开几个小时、回来看到完全可运行软件的编程模型"，任务可持续 8 小时以上不偏离目标
- Reddit r/codex 用户："第一个真正替代通用模型的 Codex 模型"
- 代码质量更高，架构更清晰，累积 bug 更少

**速度提升有实感：**
- 25% 的速度提升在迭代密集型工作流中最为明显（fail → fix → re-run 循环）
- Spark 版本被形容为 "BLAZING fast"、"crazy fast"，"比你打字或口述后续指令还快"

**工作流变革：**
- 开发者推荐组合使用：Claude Opus 4.6 做头脑风暴和架构设计，GPT-5.3-Codex 做实现和执行
- 社区共识："Opus 像一个规划的高级开发者；Codex 像一个执行的开发者"

### 6.2 负面评价与问题

**静默路由问题（HackerNews）：**
- 有 Codex Pro 用户报告 GPT-5.3-Codex 请求被静默路由到 GPT-5.2，导致性能下降，日志显示明显变慢和行为差异

**Spark 版本的局限性（Reddit）：**
- 精确任务表现不佳——有用户反映连将 "AND" 改为 "BUT" 都做不好
- 有限的 context window，倾向于在请求范围外做不必要的修改
- 实现"很少逻辑错误，但会添加垃圾代码"
- 有用户花了 $100 让 Claude Opus 4.6 清理 Codex 创建的 dashboard，因为"一团糟"

**其他问题：**
- Mac 上资源占用和发热问题
- Work tree / thread 显示 bug
- 终端输出处理较弱，导致过多复制粘贴
- 复杂任务运行时间长（数小时），状态报告有时不透明
- 对需要理解多文件依赖的深度复杂任务仍有局限

**Benchmark 争议（HackerNews）：**
- OpenAI 宣称 Spark 有 15× 加速，但开发者重新计算后认为在同等准确率下实际仅 ~1.37×
- 社区对营销宣传与实际性能之间的差距表示怀疑

### 6.3 Spark 最佳使用场景（社区共识）

适合：
- 顺序工具调用（sequential tool calls）
- 快速文档编写
- 代码审计
- 快速重构
- 不需要大量推理但需要大量顺序操作的工作流

不适合：
- 多步骤架构设计
- 复杂调试
- 长上下文代码库分析
- 需要深度推理的精确任务

---

## 7. 安全与合规

- 首个在 OpenAI Preparedness Framework 网络安全领域被分类为 **"High capability"** 的模型
- 部署了"综合网络安全栈"：安全训练、监控、Trusted Access、威胁情报
- 推出 **Trusted Access for Cyber**（试点项目）
- 2026年2月13日推出 **Lockdown Mode** 和 **Elevated Risk labels**，覆盖 ChatGPT、ChatGPT Atlas 和 Codex，防范 prompt injection 攻击
- API 采用渐进式开放策略，企业级治理优先于无限制 API 访问

---

## 8. 总结与建议

| 维度 | GPT-5.3-Codex | GPT-5.3-Codex-Spark |
|---|---|---|
| 核心优势 | 深度推理、长任务自主执行、高代码质量 | 极速响应（1000+ tok/s）、实时交互 |
| 核心劣势 | 速度较慢（65-70 tok/s）、复杂任务耗时长 | 推理深度不足、context window 较小（128K） |
| 最佳场景 | 复杂多步骤项目、全生命周期开发、需要深度推理的任务 | 快速迭代、单文件编辑、前端开发、代码审计 |
| 推荐策略 | 与 Claude Opus 4.6 配合使用：Opus 做规划，Codex 做执行 | 与旗舰版配合：Spark 做快速迭代，旗舰版做复杂推理 |

---

## 参考来源

- [OpenAI: Introducing GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex)
- [OpenAI: Introducing GPT-5.3-Codex-Spark](https://openai.com/index/introducing-gpt-5-3-codex-spark)
- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [OpenAI Reasoning Models Guide](https://platform.openai.com/docs/guides/reasoning)
- [Codex Pricing](https://developers.openai.com/codex/pricing)
- [ChatGPT Plans](https://openai.com/pricing/)
- [llm-stats.com: GPT-5.3 Codex](https://llm-stats.com/models/gpt-5.3-codex)
- [SmartScope: GPT-5.3-Codex Complete Guide](https://smartscope.blog/en/blog/gpt-5-3-codex-complete-guide/)
- [Matt Shumer: GPT-5.3-Codex Review](https://shumer.dev/gpt53-codex-review)
- [GitHub Blog: GPT-5.3-Codex for Copilot](https://github.blog/changelog/2026-02-09-gpt-5-3-codex-is-now-generally-available-for-github-copilot)
- [HackerNews 讨论](https://news.ycombinator.com/item?id=46994955)
- [Reddit r/codex](https://www.reddit.com/r/codex/comments/1r4kspv/)
- [Reddit r/ChatGPTCoding](https://www.reddit.com/r/ChatGPTCoding/comments/1r3c6a5/)
