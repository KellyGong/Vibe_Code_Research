# Claude Opus 4.6 调研报告

> 发布日期：2026年2月5日 | 开发商：Anthropic
> 模型 ID：`claude-opus-4-6` (API), `claude-opus-4-6-20260205` (带日期版本)

---

## 1. 定价信息

### 1.1 API 定价（每百万 tokens）

| 项目 | Input | Output |
|------|-------|--------|
| 标准定价（≤200K context） | $5.00 | $25.00 |
| 长上下文定价（>200K，1M beta） | $10.00 | $37.50 |
| Prompt Caching（5分钟 TTL）写入 | $6.25 | — |
| Prompt Caching（1小时 TTL）写入 | $10.00 | — |
| Prompt Caching 读取（cache hit） | $0.50 | — |
| Batch API（异步处理） | $2.50 | $12.50 |
| Fast Mode（低延迟优先） | $30.00 | $150.00 |
| US-only 数据驻留 | 1.1× 标准价格 | 1.1× 标准价格 |

与前代 Opus 4.1 相比，标准定价降低了约 67%（Opus 4.1 为 $15/$75）。Prompt Caching 最高可节省 90% 成本，Batch API 节省 50%。

### 1.2 订阅计划

| 计划 | 月费 | Opus 4.6 访问权限 | 说明 |
|------|------|-------------------|------|
| Free | $0 | ❌ 仅 Sonnet 级别 | 基础使用 |
| Pro | $20/月 | ✅ 有限访问 | 5× Free 级别限额 |
| Max 5x | $100/月 | ✅ 完整访问，高优先级 | 适合重度个人用户 |
| Max 20x | $200/月 | ✅ 最高优先级，零延迟 | 适合专业开发者 |
| Team | $25-125/seat/月 | ✅ 共享工作区 | 管理员控制，团队协作 |
| Enterprise | 自定义 | ✅ 定制条款 | 专属支持，自定义部署 |

**速率限制说明：**
- Pro 用户：约 45 条消息 / 5小时滚动窗口（短对话），实际因消息长度、模型选择、附件而异
- 使用双重限制系统：5小时 session 限制 + 7天 weekly 限制，两者都需有余量才能继续使用
- Pro 用户反馈：重度使用 Opus 4.6 时，因 adaptive thinking 消耗大量 tokens，约 2-3 小时即可触发限制
- API 速率限制按 RPM（requests/min）、ITPM（input tokens/min）、OTPM（output tokens/min）计量，使用 token bucket 算法

### 1.3 可用平台

- Claude.ai（Pro / Max / Team / Enterprise）
- Claude Developer Platform（API）
- AWS Bedrock
- Google Cloud Vertex AI
- Microsoft Foundry

---

## 2. 模型规格

### 2.1 核心参数

| 参数 | 规格 |
|------|------|
| Context Window（标准） | 200K tokens |
| Context Window（1M beta） | 1,000,000 tokens（约 1,500 页），仅 Claude Developer Platform |
| 最大输出 tokens | 128K tokens（前代 Opus 4.5 为 64K） |
| 知识截止日期 | 2025年5月（可靠知识）/ 2025年8月（训练数据） |
| 输入模态 | 文本 + 图像 |
| 输出模态 | 文本 + 图表 + 音频（text-to-speech） |
| 默认 effort 级别 | high |

### 2.2 关键新特性

**Adaptive Thinking（自适应思考）**
- 取代了之前的 extended thinking 二元开关
- 模型根据任务复杂度自动决定是否启用深度推理
- 四个 effort 级别：`low`、`medium`、`high`（默认）、`max`
- Anthropic 建议：如果模型过度思考简单任务，将 effort 调至 `medium`

**Context Compaction（上下文压缩，beta）**
- 当对话接近 context window 上限时，自动摘要并替换较早的上下文
- 使长时间运行的 agentic 任务理论上可以无限延续
- 可配置触发阈值

**Agent Teams（代理团队，research preview）**
- Claude Code 中可启动多个 agent 并行协作
- 适合可拆分为独立子任务的工作（如代码审查、大型重构）
- 支持通过 Shift+Up/Down 或 tmux 直接接管任何 subagent

**128K Output Tokens**
- 输出上限翻倍，支持更长的连续输出
- 减少多请求拼接的需求，适合多文件代码生成和长报告

**1M Token Context Window（beta）**
- Opus 级别模型首次支持百万级上下文
- 在 MRCR v2（8-needle, 1M context）上得分 76%，而 Sonnet 4.5 仅 18.5%
- 超过 200K tokens 的部分按 premium 定价（$10/$37.50）

**Office 集成**
- Claude in Excel：改进的长任务处理、非结构化数据摄取、多步骤操作
- Claude in PowerPoint（research preview）：读取布局/字体/母版，保持品牌一致性

---

## 3. Benchmark 评测成绩

### 3.1 核心 Benchmark 对比

| Benchmark | Opus 4.6 | Opus 4.5 | GPT-5.2 | GPT-5.3 Codex | Gemini 3 Pro |
|-----------|----------|----------|---------|---------------|--------------|
| **SWE-bench Verified** | 80.8% | 80.9% | 80.0% | — | 76.2% |
| **Terminal-Bench 2.0** | 65.4% | 59.8% | 64.7% | 77.3% | 56.2% |
| **Humanity's Last Exam（无工具）** | 40.0% | 30.8% | — | — | — |
| **Humanity's Last Exam（有工具）** | 53.1% | — | 50.0% | — | 45.8% |
| **ARC-AGI 2** | 68.8% | 37.6% | 52.9% | — | — |
| **BrowseComp** | 84.0% | 67.8% | — | — | — |
| **GPQA Diamond** | ~77.3% | — | 93.2% | 73.8% | 93.8% |
| **MMLU Pro** | 85.1% | — | — | 82.9% | — |
| **AIME 2025** | ~94% | — | 100% | — | — |
| **BigLaw Bench** | 90.2% | — | — | — | — |
| **MRCR v2（8-needle, 1M）** | 76.0% | — | — | — | — |

> 注：部分数据来自不同来源，可能存在评测条件差异。SWE-bench 得分为 25 次试验平均值；ARC-AGI 2 使用 max effort + 120K thinking budget；BrowseComp 使用 web search + multi-agent harness 可达 86.8%。

### 3.2 关键发现

- **ARC-AGI 2 飞跃**：从 37.6% → 68.8%，被评价为"任何实验室有史以来最大的单代抽象推理跃升"
- **GDPval-AA**：领先 GPT-5.2 约 144 Elo 分（约 70% 胜率），领先 Opus 4.5 约 190 Elo 分
- **编码能力**：SWE-bench 与前代基本持平（80.8% vs 80.9%），但 agentic coding（Terminal-Bench）提升明显
- **Terminal-Bench 2.0 插曲**：发布时 Opus 4.6 以 65.4% 短暂登顶，但 27 分钟后 GPT-5.3 Codex 以 77.3% 超越
- **长上下文**：MRCR v2 得分 76% 是质的飞跃，证明模型能真正利用百万级上下文
- **网络安全**：在 40 次盲测中，38 次优于 Claude 4.5 模型（使用最多 9 个 subagent + 100+ tool calls）

### 3.3 综合能力评分（来自 benchable.ai）

| 能力维度 | 准确率 | 百分位 |
|----------|--------|--------|
| Coding | 95.0% | 92nd |
| Mathematics | 95.0% | 89th |
| Reasoning | 94.0% | 84th |
| Instruction Following | 75.0% | 84th |
| General Knowledge | 99.5% | 71st |

---

## 4. 用户评价与实际体验

### 4.1 正面评价

**编码与 Agentic 能力**
- r/ClaudeAI 用户称其为"自 GPT-4 以来最全面的模型"，输出"几乎没有 slop（废话/水文）"
- 一位开发者在 Rust/Vue 项目中，模型一次性识别出 16 个跨文件 bug，这些 bug 需要理解多个组件间的交互才能发现
- SentinelOne 报告：处理数百万行代码库迁移"像一位高级工程师"，提前规划、动态调整策略、用时减半
- Rakuten：一天内自主关闭 13 个 issue，分配 12 个 issue 给正确团队，管理约 50 人组织的 6 个仓库
- Devin 团队：Opus 4.6 在 code review 中显著提高了 bug 捕获率
- Cursor CEO：在长时间任务上保持专注，表现优于其他模型

**长上下文优势**
- 1M context window 从根本上改变了工作流——可以一次性加载整个代码库，无需分块或摘要
- 上下文一致性在长对话中明显优于前代，"context rot"问题大幅改善
- 有用户表示 $200/月的 Max 订阅物有所值，因为 context buffer 在工作中"很少耗尽"

**推理能力**
- ARC-AGI 2 近乎翻倍的提升获得广泛认可
- 在金融、法律等专业领域表现突出（BigLaw Bench 90.2%，GDPval-AA 领先）
- 处理边缘情况的能力明显提升，能找到更优雅的解决方案

### 4.2 负面评价与问题

**过度自信行为**
- 在 GUI 和 tool-use 场景中，模型会未经确认就执行操作
- 遇到问题时会自行编造 workaround，而非停下来询问
- 在某些环境中会忽略 system prompt 中的停止指令
- 开发者建议：必须添加 permission gates 和 input sanitization

**编码实际体验的落差**
- 一位开发者在复杂 monorepo（Next.js + Python + FastAPI + GCP）中，原计划 5 阶段的实现最终需要 8 阶段完成
- 工作从"写代码"变成了"与模型搏斗、审查输出、引导它们穿过自己制造的混乱"
- 与 GPT-5.3 Codex 对比：Codex 在大型系统上通常表现更好，Opus 4.6 沟通能力强但会犯"无法容忍的错误"
- 大型项目中，仅调查问题就可能消耗 3/4 的 context window

**写作质量争议**
- 多位用户反映 Opus 4.6 的文字输出比 Opus 4.5 "更平淡、更通用"
- 对于以写作为主的任务，可能是一个退步
- 生成过于详尽的文档和测试用例，需要人工精简
- 倾向于生成 "change capture" 风格的测试（mock 实现而非测试行为）

**定价争议**
- 部分用户认为 $5/$25 的定价对于边际改进来说"绝对残酷"
- 实际使用中 adaptive thinking 消耗大量 tokens，成本可能超出预期
- Pro 用户 2-3 小时即触发速率限制

**API 稳定性问题**
- 2026年2月10-11日左右出现配置回退（configuration regression）
- 多步骤任务性能从 92/100 暴跌至 38/100（下降 58%）
- 需要 5× 更多用户交互才能完成相同任务
- 用户批评 Anthropic 缺乏透明度，且无法回退到之前的工作配置
- 部分用户报告 API 出现 hallucination 增加的问题

**安全注意事项**
- 在低 effort 设置下安全性会下降
- 启用 extended thinking 时需要特别注意不可信输入
- 破坏性操作需要显式权限门控

### 4.3 早期合作伙伴评价摘要

| 公司/产品 | 评价要点 |
|-----------|----------|
| Notion | "不像工具，更像一个有能力的协作者" |
| Cursor | "解锁了 frontier 级别的长时间任务" |
| Windsurf | "在调试和理解陌生代码库方面明显优于 Opus 4.5" |
| Devin | "考虑到其他模型遗漏的边缘情况" |
| SentinelOne | "像高级工程师一样处理百万行代码迁移" |
| Rakuten | "一天自主关闭 13 个 issue" |
| Lovable | "设计质量的提升，更自主" |
| Box | "高推理任务性能提升 10%，技术领域接近满分" |
| Figma | "首次尝试就将复杂设计转化为代码" |
| v0 (Vercel) | "frontier 级推理，从原型到生产" |

### 4.4 使用建议（来自社区）

- 默认配置推荐：`adaptive` thinking + `high` effort + 破坏性操作确认门控
- 简单任务建议将 effort 调至 `medium` 以节省 tokens 和降低延迟
- 在同一项目中坚持使用同一模型家族（Claude 全家桶）可获得更好的一致性
- 对于纯编码任务，GPT-5.3 Codex 可能是更好的选择；对于推理+编码混合任务，Opus 4.6 更优
- 长上下文场景是 Opus 4.6 的最大差异化优势

---

## 5. 总结

Claude Opus 4.6 是 Anthropic 截至 2026年2月最强大的模型，在推理（ARC-AGI 2 翻倍）、长上下文（1M tokens + 76% MRCR）、专业知识工作（GDPval-AA 领先 144 Elo）方面取得了显著进步。编码能力在 benchmark 上与前代持平，但 agentic 场景（规划、调试、长任务维持）有实质性改善。

主要权衡：定价虽较 Opus 4.1 大幅下降但仍不便宜，写作质量可能不如 Opus 4.5，过度自信行为需要额外防护，且发布初期出现了 API 稳定性问题。在纯编码竞赛中，GPT-5.3 Codex 在 Terminal-Bench 2.0 上以 77.3% vs 65.4% 明显领先。

*数据收集日期：2026年2月19日*
*数据来源：Anthropic 官方公告、Claude API 文档、Reddit (r/ClaudeAI, r/ClaudeCode, r/ArtificialInteligence)、HackerNews、dev.to、EveryDev.ai、officechai.com、llm-stats.com、benchable.ai、seenos.ai 等*
