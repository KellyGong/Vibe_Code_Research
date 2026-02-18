# Claude Sonnet 4.6 调研报告

> 发布日期：2026年2月17日 | 开发商：Anthropic
> 本报告基于公开信息整理，数据截至2026年2月18日

---

## 1. 定价信息

### 1.1 API 定价

Claude Sonnet 4.6 的 API 定价与前代 Sonnet 4.5 保持一致：

| 项目 | 价格 (每百万 tokens) |
|---|---|
| 基础 Input Tokens | $3 |
| Output Tokens | $15 |
| 5分钟 Cache Writes | $3.75 |
| 1小时 Cache Writes | $6 |
| Cache Hits & Refreshes | $0.30 |

**Batch API（批量处理，享50%折扣）：**

| 项目 | 价格 (每百万 tokens) |
|---|---|
| Batch Input | $1.50 |
| Batch Output | $7.50 |

**长上下文定价（超过200K input tokens时触发）：**

| 项目 | ≤200K input tokens | >200K input tokens |
|---|---|---|
| Input | $3/MTok | $6/MTok |
| Output | $15/MTok | $22.50/MTok |

**成本优化方式：**
- Prompt Caching：最高可节省 90% 成本
- Batch Processing：节省 50% 成本
- 两者可叠加使用

**与同系列模型对比：**

| 模型 | Input | Output |
|---|---|---|
| Claude Opus 4.6 | $5/MTok | $25/MTok |
| Claude Sonnet 4.6 | $3/MTok | $15/MTok |
| Claude Haiku 4.5 | $1/MTok | $5/MTok |

### 1.2 订阅计划

Claude Sonnet 4.6 现已成为 Free 和 Pro 用户的默认模型。

| 计划 | 价格 | 说明 |
|---|---|---|
| Free | $0 | Sonnet 4.6 为默认模型，含文件创建、Connectors、Skills、Compaction 功能；用量受限，每5小时重置 |
| Pro | $20/月（年付 $17/月） | 更多用量、可使用更多模型（含 Opus）、Memory、Research、Claude Code、Cowork |
| Max 5x | $100/月起 | Pro 的 5 倍用量、优先访问、高级功能早期体验 |
| Max 20x | 更高价格 | Pro 的 20 倍用量、最高优先级 |
| Team（标准席位） | $25/月（年付 $20/月） | 5-150人团队，SSO、管理控制台、Enterprise Search |
| Team（高级席位） | $125/月（年付 $100/月） | 标准席位的 5 倍用量 |
| Enterprise | 联系销售 | HIPAA-ready、SCIM、审计日志、自定义数据保留、增强上下文窗口 |

### 1.3 可用平台

- claude.ai（Web、iOS、Android、Desktop）
- Claude API（模型 ID：`claude-sonnet-4-6`）
- AWS Bedrock
- Google Vertex AI
- Microsoft Foundry
- GitHub Copilot（已集成）
- Claude Code、Claude Cowork

---

## 2. 模型规格

### 2.1 核心参数

| 参数 | 值 |
|---|---|
| 模型 ID | `claude-sonnet-4-6` |
| 发布日期 | 2026年2月17日 |
| Context Window（标准） | 200K tokens |
| Context Window（Beta，1M） | 1,000,000 tokens（API beta，需 Tier 4 或自定义限额） |
| Max Output Tokens | 64K tokens |
| 知识截止日期（Reliable Knowledge Cutoff） | 2025年8月 |
| 训练数据截止日期（Training Data Cutoff） | 2026年1月 |
| 支持 Extended Thinking | ✅ |
| 支持 Adaptive Thinking | ✅ |
| 支持 Context Compaction | ✅（Beta） |
| 支持 Computer Use | ✅ |
| 支持 Tool Use | ✅ |
| 支持 Web Search / Fetch | ✅ |
| 支持 Code Execution | ✅ |

### 2.2 关键特性

- **Hybrid Reasoning Model**：同时支持 Adaptive Thinking 和 Extended Thinking，可根据任务复杂度自动调节推理深度
- **1M Token Context Window（Beta）**：可在单次请求中容纳整个代码库、大量合同文档或数十篇研究论文
- **Context Compaction**：自动压缩旧上下文，有效延长对话长度
- **Computer Use 大幅提升**：在 OSWorld 基准上从 Sonnet 4.5 的 61.4% 提升至 72.5%，用户报告在复杂电子表格导航和多步骤网页表单填写上接近人类水平
- **编码能力显著增强**：更好的指令遵循、更少的过度工程化、更少的"懒惰"行为、更少的虚假成功声明
- **前端设计能力**：客户独立评价其视觉输出"明显更精致"，布局、动画和设计感优于前代模型，迭代次数更少即可达到生产质量

### 2.3 与 Sonnet 4.5 的对比

Sonnet 4.6 是自2025年9月 Sonnet 4.5 以来的首次 Sonnet 系列升级，改进覆盖多个维度：

| 维度 | Sonnet 4.5 | Sonnet 4.6 | 变化 |
|---|---|---|---|
| Computer Use (OSWorld) | 61.4% | 72.5% | +11.1pp |
| 重度推理任务（Box 测试） | 62% | 77% | +15pp |
| 数学计算（Box 测试） | 62% | 89% | +27pp |
| 零售运营准确率 | — | 94% | — |
| 医疗任务准确率 | — | 78% | — |
| 数据提取准确率 | — | >80% | — |
| Claude Code 用户偏好 | 基准 | 70% 偏好 4.6 | 大幅领先 |
| 价格 | $3/$15 | $3/$15 | 不变 |
| Context Window | 200K（1M beta） | 200K（1M beta） | 不变 |

Anthropic 官方表示：Sonnet 4.6 在"几乎所有测试中都碾压 Sonnet 4.5"，在 agentic financial analysis 和 office tasks 上甚至超越了更大的 Opus 模型。

---

## 3. Benchmark 成绩

### 3.1 已公布的 Benchmark 分数

| Benchmark | Sonnet 4.6 分数 | 说明 |
|---|---|---|
| GPQA Diamond | 89.9% | 研究生级别科学问答 |
| MMMLU | 89.3% | 多语言大规模多任务理解 |
| SWE-bench Verified | 79.6%（10次试验平均）| 真实开源项目 bug 修复；修改 prompt 后可达 80.2% |
| ARC-AGI-2 | 58.3%（max effort）/ 60.4%（high effort） | 抽象推理泛化测试（François Chollet 设计） |
| HLE (Humanity's Last Exam) | 49.0%（with tools）/ 33.2%（without tools） | 人类最后考试 |
| OSWorld (Computer Use) | 72.5% | 真实桌面环境计算机操作任务 |

### 3.2 行业/企业 Benchmark

| 测试方 | 领域 | 结果 |
|---|---|---|
| Box | 重度推理 Q&A | 77%（比 Sonnet 4.5 高 15pp） |
| Box | 数学计算 | 89%（比 Sonnet 4.5 高 27pp） |
| Pace (保险公司) | 保险 Computer Use | 94%，所有 Claude 模型中最高 |
| 匿名金融客户 | Financial Services Benchmark | Answer match rate 显著高于 Sonnet 4.5 |
| Rakuten AI | iOS 代码生成 | "我们测试过的最佳 iOS 代码"，规范合规性和架构质量最优 |
| Artificial Analysis | GDPVal (Office Tasks) | 超越 Gemini 3 Pro、GPT 5.2，甚至超越 Opus 4.6 |
| Vending-Bench Arena | 长期商业模拟 | 显著优于 Sonnet 4.5，采用独特的"先投资后盈利"策略 |
| OfficeQA | 企业文档理解 | 匹配 Opus 4.6 水平 |

### 3.3 与竞品定位

根据 Anthropic 和第三方评测：
- Sonnet 4.6 在 office tasks 和 agentic financial analysis 上**超越** Gemini 3 Pro、GPT 5.2 和 Opus 4.6
- 在某些 leaderboard 上仍**落后于** Opus 4.6、Gemini 3 Deep Think、GPT 5.2
- 性价比极高：以 Opus 40% 的价格（$3/$15 vs $5/$25）提供接近甚至超越 Opus 4.5 的性能

---

## 4. 用户评价

### 4.1 Reddit (r/ClaudeAI) 用户反馈

**正面评价：**

- > "Sonnet 4.6 feels like Opus 4.5 at Sonnet pricing." — u/Own-Equipment-5454
  
  该帖获得大量认同，核心观点是 Sonnet 4.6 以 Sonnet 的价格提供了接近 Opus 4.5 的能力。

- > "Tested Sonnet 4.6 for coding and it's genuinely very good. It finished all my outstanding tasks using like 20% of my 5 hour limit, which Opus would have used up more than twice." — u/5xaaaaa
  
  编码效率极高，token 消耗远低于 Opus。

- > "I am also seeing very good performance, it still gave subpar results for a complex issue involving db and UI, but man, very happy with the performance, so far." — u/Own-Equipment-5454

**中性/负面评价：**

- > "Not completely agreed, task complex opus is still way better, because it thinks more and better." — u/Artistic_Unit_5570
  
  对于高复杂度任务，Opus 仍然更强。

- > "I have been testing 4.6 out, and I feel it uses too many tokens. Found similar observations by other people on reddit as well. Something is def different about the 4.6 architecture for both opus and sonnet." — u/Own-Equipment-5454
  
  部分用户反映 4.6 系列（包括 Opus 和 Sonnet）的 token 消耗偏高。

- > "1mil context is more expensive than regular price." — u/Steus_au
  
  提醒 1M 上下文窗口的额外成本。

### 4.2 Hacker News 讨论

Sonnet 4.6 发布帖在 HN 获得 **1257 points** 和 **1122 comments**，热度极高。

**关键讨论主题：**

- **编码能力的进步**：多位开发者认为 Sonnet 4.6 在编码方面已接近甚至超越部分 Opus 场景
  > "Opus 4.6 is incredible compared to previous models." — HN 用户
  
  > "It is certainly already better than most humans, even better than most humans who occasionally code." — HN 用户（讨论 Claude 系列整体能力）

- **Vibe Coding 讨论**：大量讨论围绕 AI 编码对 SaaS 行业的影响，Sonnet 4.6 的发布被视为这一趋势的加速器

- **Computer Use 关注度高**：
  > "I see a big focus on computer use - you can tell they think there is a lot of value there and in truth it may be as big as coding if they convincingly pull it off." — HN 用户

- **务实的质疑**：部分资深开发者指出 AI 编码仍有局限
  > "They're pattern matching. That gives the illusion of usefulness for coding when your problem is very similar to others, but falls apart as soon as you need any sort of depth or novelty." — HN 用户

### 4.3 Simon Willison（知名开发者/博主）评价

Simon Willison 在发布当天即进行了测试，并发布了 llm-anthropic 0.24 以支持 Sonnet 4.6。他指出：
- Sonnet 4.6 提供了与 Opus 4.5 相似的性能，但价格仅为 Sonnet 级别（$3/$15 vs $5/$25）
- 知识截止日期为2025年8月，比 Opus 4.6（2025年5月）更新
- Claude Code 完成了大部分 llm-anthropic 插件的迁移工作，包括 Adaptive Thinking 和 prefix 移除等细节

### 4.4 企业客户评价（来自 Anthropic 官方博客引用）

| 客户 | 评价摘要 |
|---|---|
| 匿名（代码审查） | "Sonnet 4.6 has meaningfully closed the gap with Opus on bug detection, letting us run more reviewers in parallel" |
| 匿名（金融服务） | "Significant jump in answer match rate compared to Sonnet 4.5 in our Financial Services Benchmark" |
| Box | "Outperforming Claude Sonnet 4.5 in heavy reasoning Q&A by 15 percentage points" |
| Pace（保险） | "94% on our insurance benchmark, making it the highest-performing model we've tested for computer use" |
| Rakuten AI | "Produced the best iOS code we've tested... Better spec compliance, better architecture" |
| 匿名（前端） | "Perfect design taste when building frontend pages and data reports" |
| 匿名（法律） | "Exceptionally responsive to direction — delivering precise figures and structured comparisons" |
| 匿名（编码平台） | "Delivers frontier-level results on complex app builds and bug-fixing. It's becoming our go-to for deep codebase work" |

### 4.5 综合评价总结

**优势：**
- 性价比极高，以 Sonnet 价格提供接近 Opus 4.5 的能力
- 编码能力大幅提升，指令遵循更好，过度工程化和"懒惰"行为减少
- Computer Use 能力显著进步（OSWorld 72.5%）
- 前端/设计输出质量明显提升
- 1M token context window 对大型代码库和长文档工作流意义重大
- 幻觉率低，安全性评估良好

**不足：**
- 高复杂度深度推理任务仍不如 Opus 4.6
- 部分用户反映 token 消耗偏高
- 1M 上下文窗口仍为 Beta，且超过 200K tokens 后价格翻倍
- 在某些 leaderboard 上仍落后于 Opus 4.6、Gemini 3 Deep Think、GPT 5.2

---

## 5. 安全性

根据 [Sonnet 4.6 System Card](https://www-cdn.anthropic.com/78073f739564e986ff3e28522761a7a0b4484f84.pdf)：
- 整体安全性"与其他近期 Claude 模型持平或更优"
- 幻觉倾向低，sycophancy（谄媚）行为少
- Prompt Injection 抵抗能力相比 Sonnet 4.5 有"重大改进"，与 Opus 4.6 表现相当
- 安全研究人员评价："broadly warm, honest, prosocial, and at times funny character, very strong safety behaviors, and no signs of major concerns around high-stakes forms of misalignment"

---

*数据来源：Anthropic 官方博客、Anthropic API 文档、Mashable、9to5Mac、VentureBeat、FindArticles、Simon Willison's Weblog、Reddit r/ClaudeAI、Hacker News*
